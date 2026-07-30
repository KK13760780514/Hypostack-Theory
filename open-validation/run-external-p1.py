#!/usr/bin/env python3
"""External contributor reproduction of XD-P1-SIM-001 with 3 seeds."""

import json
import math
import random
import platform
import sys
from datetime import datetime, timezone

CLAIM_ID = "XD-P1-SIM-001"
RUNS = 100
TEMPERATURE = 0.2
ALPHA = 0.01
SEEDS = [42, 123, 999]

PATH_A = {"E_i": 1.0, "steps": 8}
PATH_B = {"E_i": 3.0, "steps": 3}


def action(path):
    return float(path["E_i"]) * int(path["steps"])


def softmax_probability(s_a, s_b):
    z_a = -s_a / TEMPERATURE
    z_b = -s_b / TEMPERATURE
    max_z = max(z_a, z_b)
    exp_a = math.exp(z_a - max_z)
    exp_b = math.exp(z_b - max_z)
    return exp_a / (exp_a + exp_b)


def exact_one_sided_binomial_p_value(k, n, p0=0.5):
    return sum(
        math.comb(n, x) * (p0**x) * ((1 - p0) ** (n - x))
        for x in range(k, n + 1)
    )


def main():
    s_a = action(PATH_A)
    s_b = action(PATH_B)
    p_a = softmax_probability(s_a, s_b)

    total_selected_a = 0
    total_selected_b = 0
    p_values = []
    seed_results = []

    for seed in SEEDS:
        rng = random.Random(seed)
        selected_a = sum(1 for _ in range(RUNS) if rng.random() < p_a)
        selected_b = RUNS - selected_a
        p_value = exact_one_sided_binomial_p_value(selected_a, RUNS)
        total_selected_a += selected_a
        total_selected_b += selected_b
        p_values.append(p_value)
        seed_results.append(
            {"seed": seed, "selected_A": selected_a, "selected_B": selected_b, "p_value": p_value}
        )

    all_supported = all(p < ALPHA for p in p_values)
    classification = "support" if all_supported else "challenge"

    seed_a_counts = [r["selected_A"] for r in seed_results]
    summary = f"3 seeds: {seed_a_counts} selections for A; min p={min(p_values):.2e}"

    output = {
        "submission_id": "external-contributor-20260730-p1",
        "claim_id": CLAIM_ID,
        "title": "External reproduction of XD-P1-SIM-001 with 3 seeds",
        "author": {
            "name": "external-contributor",
            "affiliation": "independent",
            "contact": "",
        },
        "preregistration": {
            "hash": "",
            "timestamp_utc": "2026-07-30T00:30:00+00:00",
            "uri": "submissions/prereg-external-contributor.yaml",
        },
        "implementation": {
            "repository": "local",
            "commit": "local",
            "code_hash": "external-impl-v1",
            "data_hash": "",
            "seed": SEEDS,
            "environment": {
                "os": platform.platform(),
                "python_version": sys.version.split()[0],
                "dependencies": "python-stdlib-only",
            },
        },
        "result": {
            "S_A": s_a,
            "S_B": s_b,
            "preferred_path": "A" if s_a < s_b else "B",
            "selected_counts": {"A": total_selected_a, "B": total_selected_b},
            "p_value": min(p_values),
            "summary": summary,
            "raw_output": {
                "seeds": SEEDS,
                "seed_results": seed_results,
                "temperature": TEMPERATURE,
                "runs_per_seed": RUNS,
            },
        },
        "classification": classification,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    output_path = (
        "open-validation/submissions/2026-07-30-external-contributor-XD-P1-SIM-001.json"
    )
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
