#!/usr/bin/env python3
"""Validate a XuanDie open-validation submission and append it to the evidence ledger.

This validator intentionally uses only the Python standard library. It supports the
subset of JSON Schema used by submission-schema.json.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_SCHEMA = Path(__file__).with_name("submission-schema.json")
DEFAULT_LEDGER = Path(__file__).with_name("evidence-ledger.csv")

HEX64_RE = re.compile(r"^[0-9a-fA-F]{64}$")
PLACEHOLDER_HASHES = {"in-script-preregistered-constants", "in-script-preregistered-constants-v2"}

LEDGER_FIELDS = [
    "evidence_id",
    "claim_id",
    "submission_id",
    "classification",
    "evidence_level",
    "status",
    "preferred_path",
    "S_A",
    "S_B",
    "p_value",
    "author",
    "code_hash",
    "timestamp_utc",
    "notes",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def is_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate_date_time(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def validate(value: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    expected_type = schema.get("type")
    if expected_type is not None:
        expected_types = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(is_type(value, item) for item in expected_types):
            errors.append(f"{path}: expected type {expected_type}, got {type(value).__name__}")
            return

    if "oneOf" in schema:
        one_of_errors = []
        matches = 0
        for idx, subschema in enumerate(schema["oneOf"]):
            sub_errors: list[str] = []
            validate(value, subschema, f"{path}.oneOf[{idx}]", sub_errors)
            if not sub_errors:
                matches += 1
            else:
                one_of_errors.extend(sub_errors)
        if matches == 0:
            errors.append(f"{path}: does not match any of oneOf schemas")
            errors.extend(one_of_errors)
        elif matches > 1:
            errors.append(f"{path}: matches {matches} oneOf schemas, expected exactly 1")
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is not in enum {schema['enum']!r}")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra_keys = sorted(set(value) - set(properties))
            if extra_keys:
                errors.append(f"{path}: additional properties not allowed: {extra_keys}")

        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required property {key!r}")

        for key, subschema in properties.items():
            if key in value and isinstance(subschema, dict):
                validate(value[key], subschema, f"{path}.{key}", errors)

    if isinstance(value, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < min_items:
            errors.append(f"{path}: array has {len(value)} items, minItems is {min_items}")
        items_schema = schema.get("items")
        if items_schema and isinstance(items_schema, dict):
            for idx, item in enumerate(value):
                validate(item, items_schema, f"{path}[{idx}]", errors)

    if isinstance(value, str):
        min_length = schema.get("minLength")
        if min_length is not None and len(value) < min_length:
            errors.append(f"{path}: string shorter than minLength {min_length}")
        if schema.get("format") == "date-time" and not validate_date_time(value):
            errors.append(f"{path}: invalid date-time format")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if minimum is not None and value < minimum:
            errors.append(f"{path}: value {value} < minimum {minimum}")
        if maximum is not None and value > maximum:
            errors.append(f"{path}: value {value} > maximum {maximum}")


def evidence_level(classification: str, valid: bool) -> tuple[str, str]:
    if not valid:
        return "needs_review", "form_check_failed"
    if classification == "support":
        return "L4_candidate", "form_check_passed"
    if classification == "falsification":
        return "L5_candidate", "form_check_passed"
    return "exploratory", "form_check_passed"


def mark_superseded(ledger_path: Path, submission_id: str, new_evidence_id: str) -> int:
    """Mark prior form_check_failed rows with the same submission_id as superseded.

    Returns the number of rows marked.  This preserves the historical record
    (rows are never deleted) while making it clear they were later resolved.
    """
    if not ledger_path.exists():
        return 0

    with ledger_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or LEDGER_FIELDS

    marked = 0
    for row in rows:
        if (
            row.get("submission_id") == submission_id
            and row.get("status") == "form_check_failed"
            and "superseded_by:" not in row.get("notes", "")
        ):
            row["notes"] = f"superseded_by:{new_evidence_id}; " + row.get("notes", "")
            marked += 1

    if marked:
        with ledger_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    return marked


def append_ledger(submission: dict[str, Any], errors: list[str], ledger_path: Path) -> dict[str, str]:
    result = submission.get("result", {})
    implementation = submission.get("implementation", {})
    author = submission.get("author", {})
    classification = submission.get("classification", "exploratory")
    level, status = evidence_level(classification, not errors)
    timestamp = submission.get("timestamp_utc") or datetime.now(timezone.utc).isoformat()

    canonical = json.dumps(submission, ensure_ascii=False, sort_keys=True)
    evidence_id = "EV-" + hashlib.sha256((canonical + timestamp).encode("utf-8")).hexdigest()[:16]

    submission_id = submission.get("submission_id", "")
    notes = "schema_valid" if not errors else "; ".join(errors)

    # If this submission passed, mark prior failures as superseded.
    if not errors:
        count = mark_superseded(ledger_path, submission_id, evidence_id)
        if count:
            notes += f"; superseded_{count}_prior_failures"

    row = {
        "evidence_id": evidence_id,
        "claim_id": submission.get("claim_id", ""),
        "submission_id": submission_id,
        "classification": classification,
        "evidence_level": level,
        "status": status,
        "preferred_path": result.get("preferred_path", ""),
        "S_A": result.get("S_A", ""),
        "S_B": result.get("S_B", ""),
        "p_value": result.get("p_value", ""),
        "author": author.get("name", ""),
        "code_hash": implementation.get("code_hash", ""),
        "timestamp_utc": timestamp,
        "notes": notes,
    }

    ledger_exists = ledger_path.exists()

    # Prevent duplicate submissions (same evidence_id already in ledger)
    if ledger_exists:
        with ledger_path.open("r", encoding="utf-8", newline="") as f:
            existing_ids = {row["evidence_id"] for row in csv.DictReader(f)}
        if evidence_id in existing_ids:
            row["notes"] = "duplicate_submission_skipped; " + notes
            return row

    with ledger_path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
        if not ledger_exists:
            writer.writeheader()
        writer.writerow(row)

    return row


def preregistration_checks(submission: dict[str, Any], warnings: list[str]) -> None:
    """Advisory pre-registration compliance checks (non-fatal).

    A placeholder hash or a missing timestamp is reported as a warning so
    reviewers are aware, without rejecting historically valid submissions.
    """
    prereg = submission.get("preregistration") or {}
    hash_val = str(prereg.get("hash", "")).strip()
    if not hash_val:
        warnings.append("preregistration.hash: empty")
    elif not HEX64_RE.match(hash_val):
        if hash_val in PLACEHOLDER_HASHES:
            warnings.append(
                f"preregistration.hash: placeholder {hash_val!r} (requires manual review)"
            )
        else:
            warnings.append(
                f"preregistration.hash: not a 64-char hex SHA-256 ({hash_val!r})"
            )

    pre_ts = prereg.get("timestamp_utc")
    post_ts = submission.get("timestamp_utc")
    if pre_ts and post_ts:
        try:
            t0 = datetime.fromisoformat(str(pre_ts).replace("Z", "+00:00"))
            t1 = datetime.fromisoformat(str(post_ts).replace("Z", "+00:00"))
            if t0 > t1:
                warnings.append(
                    "preregistration.timestamp_utc is later than submission timestamp_utc"
                )
        except ValueError:
            warnings.append("preregistration.timestamp_utc: invalid date-time")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a XuanDie submission JSON file.")
    parser.add_argument("submission", type=Path, help="Path to submission JSON.")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Path to submission schema.")
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER, help="Path to evidence ledger CSV.")
    parser.add_argument("--no-ledger", action="store_true", help="Validate without appending to evidence ledger.")
    args = parser.parse_args()

    submission = load_json(args.submission)
    schema = load_json(args.schema)
    errors: list[str] = []
    warnings: list[str] = []
    validate(submission, schema, "$", errors)
    preregistration_checks(submission, warnings)

    report: dict[str, Any] = {
        "submission": str(args.submission),
        "schema": str(args.schema),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }

    if not args.no_ledger:
        report["ledger_row"] = append_ledger(submission, errors, args.ledger)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
