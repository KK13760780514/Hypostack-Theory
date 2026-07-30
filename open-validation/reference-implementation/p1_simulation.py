#!/usr/bin/env python3
"""Reference simulation for XD-P1-SIM-001.

The simulation checks whether a softmax path selector prefers the path with
lower information action S = sum(E_i * delta_N_i).
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import random
import sys
from datetime import datetime, timezone

CLAIM_ID = "XD-P1-SIM-001"
RUNS = 100
SEED = 20260728
TEMPERATURE = 0.2
ALPHA = 0.01

PATH_A = {"E_i": 1.0, "steps": 8}
PATH_B = {"E_i": 3.0, "steps": 3}


def action(path: dict[str, float | int]) -> float:
    return float(path["E_i"]) * int(path["steps"])


def softmax_probability(s_a: float, s_b: float) -> float:
    z_a = -s_a / TEMPERATURE
    z_b = -s_b / TEMPERATURE
    max_z = max(z_a, z_b)
    exp_a = math.exp(z_a - max_z)
    exp_b = math.exp(z_b - max_z)
    return exp_a / (exp_a + exp_b)


def exact_one_sided_binomial_p_value(k: int, n: int, p0: float = 0.5) -> float:
    return sum(math.comb(n, x) * (p0**x) * ((1 - p0) ** (n - x)) for x in range(k, n + 1))


def source_hash() -> str:
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> None:
    s_a = action(PATH_A)
    s_b = action(PATH_B)
    p_a = softmax_probability(s_a, s_b)

    rng = random.Random(SEED)
    selected_a = sum(1 for _ in range(RUNS) if rng.random() < p_a)
    selected_b = RUNS - selected_a
    p_value = exact_one_sided_binomial_p_value(selected_a, RUNS)

    if s_a < s_b and selected_a > RUNS / 2 and p_value < ALPHA:
        classification = "support"
    elif selected_a <= RUNS / 2 or p_value >= ALPHA:
        classification = "challenge"
    else:
        classification = "exploratory"

    output = {
        "submission_id": f"ref-{CLAIM_ID.lower()}-{SEED}",
        "claim_id": CLAIM_ID,
        "title": "Reference implementation for P1 enhanced simulation",
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
            "S_A": s_a,
            "S_B": s_b,
            "preferred_path": "A" if s_a < s_b else "B" if s_b < s_a else "tie",
            "selected_counts": {"A": selected_a, "B": selected_b},
            "p_value": p_value,
            "summary": f"P(A)={p_a:.6f}; selected A {selected_a}/{RUNS}; alpha={ALPHA}",
            "raw_output": {
                "temperature": TEMPERATURE,
                "runs": RUNS,
                "path_A": PATH_A,
                "path_B": PATH_B
            }
        },
        "classification": classification,
        "timestamp_utc": datetime.now(timezone.utc).isoformat()
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
