#!/usr/bin/env python3
"""Toy implementation for XD-AI-TOY-001.

This script compares two gradient-descent training paths on a tiny linear
regression problem. It only defines a reproducible E/N/S accounting method;
it is not a complete validation of the AI prediction.
"""

from __future__ import annotations

import hashlib
import json
import platform
import random
import sys
from datetime import datetime, timezone

CLAIM_ID = "XD-AI-TOY-001"
SEED = 20260728
TARGET_LOSS = 0.01
MAX_STEPS = 200
COMPUTE_WEIGHT = 0.01
TRUE_W = 2.0
TRUE_B = 1.0

PATHS = {
    "A": {"learning_rate": 0.05, "description": "lower step cost, more steps"},
    "B": {"learning_rate": 0.20, "description": "higher step cost, fewer steps"},
}


def make_dataset() -> list[tuple[float, float]]:
    rng = random.Random(SEED)
    xs = [-1.0, -0.5, 0.0, 0.5, 1.0]
    return [(x, TRUE_W * x + TRUE_B + rng.uniform(-0.05, 0.05)) for x in xs]


def mse(data: list[tuple[float, float]], w: float, b: float) -> float:
    return sum((w * x + b - y) ** 2 for x, y in data) / len(data)


def gradients(data: list[tuple[float, float]], w: float, b: float) -> tuple[float, float]:
    grad_w = sum(2 * x * (w * x + b - y) for x, y in data) / len(data)
    grad_b = sum(2 * (w * x + b - y) for x, y in data) / len(data)
    return grad_w, grad_b


def train_path(learning_rate: float, data: list[tuple[float, float]]) -> dict[str, float | int]:
    w = 0.0
    b = 0.0
    previous_loss = mse(data, w, b)
    s_total = 0.0

    for step in range(1, MAX_STEPS + 1):
        grad_w, grad_b = gradients(data, w, b)
        w -= learning_rate * grad_w
        b -= learning_rate * grad_b
        current_loss = mse(data, w, b)
        e_i = abs(previous_loss - current_loss) + COMPUTE_WEIGHT * learning_rate
        s_total += e_i
        previous_loss = current_loss

        if current_loss <= TARGET_LOSS:
            return {
                "steps": step,
                "S": s_total,
                "final_loss": current_loss,
                "w": w,
                "b": b,
            }

    return {
        "steps": MAX_STEPS,
        "S": s_total,
        "final_loss": previous_loss,
        "w": w,
        "b": b,
    }


def source_hash() -> str:
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> None:
    data = make_dataset()
    results = {name: train_path(cfg["learning_rate"], data) for name, cfg in PATHS.items()}
    preferred_path = "A" if results["A"]["S"] < results["B"]["S"] else "B" if results["B"]["S"] < results["A"]["S"] else "tie"

    output = {
        "submission_id": f"ref-{CLAIM_ID.lower()}-{SEED}",
        "claim_id": CLAIM_ID,
        "title": "Toy E/N/S accounting for AI training path selection",
        "author": {
            "name": "reference-implementation",
            "affiliation": "open-validation",
            "contact": ""
        },
        "preregistration": {
            "hash": "replace-with-preregistration-file-hash",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "uri": ""
        },
        "implementation": {
            "repository": "",
            "commit": "",
            "code_hash": source_hash(),
            "data_hash": "",
            "seed": SEED,
            "environment": {
                "os": platform.platform(),
                "python_version": sys.version.split()[0],
                "dependencies": "python-stdlib-only"
            }
        },
        "result": {
            "S_A": float(results["A"]["S"]),
            "S_B": float(results["B"]["S"]),
            "preferred_path": preferred_path,
            "p_value": None,
            "summary": "Toy accounting only; formal validation requires multi-seed and multi-optimizer experiments.",
            "raw_output": {
                "target_loss": TARGET_LOSS,
                "compute_weight": COMPUTE_WEIGHT,
                "results": results,
            }
        },
        "classification": "exploratory",
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
