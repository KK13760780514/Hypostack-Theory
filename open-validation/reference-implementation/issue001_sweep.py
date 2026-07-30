#!/usr/bin/env python3
"""Parameter sweep for ISSUE-001: AI toy path E-accounting analysis.

Scans compute_weight x learning_rate and reports where S_A < S_B holds.
Also evaluates three candidate E definitions:

- V0 (current): E_i = |dloss| + compute_weight * learning_rate
- V1 (fixed step cost): E_i = 1.0 + compute_weight * learning_rate
- V2 (progress-normalized): E_i = compute_weight * learning_rate / max(|dloss|, eps)
"""

from __future__ import annotations

import json
import random

SEED = 20260728
TARGET_LOSS = 0.01
MAX_STEPS = 500
TRUE_W = 2.0
TRUE_B = 1.0
EPS = 1e-12

LEARNING_RATES = [0.02, 0.05, 0.1, 0.2, 0.4]
COMPUTE_WEIGHTS = [0.0, 0.001, 0.01, 0.05, 0.1, 0.5]


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


def train(
    lr: float,
    compute_weight: float,
    version: str,
    data: list[tuple[float, float]],
) -> dict[str, float | int | bool]:
    w = 0.0
    b = 0.0
    prev_loss = mse(data, w, b)
    s_total = 0.0

    for step in range(1, MAX_STEPS + 1):
        grad_w, grad_b = gradients(data, w, b)
        w -= lr * grad_w
        b -= lr * grad_b
        cur_loss = mse(data, w, b)
        dloss = abs(prev_loss - cur_loss)

        if version == "V0":
            e_i = dloss + compute_weight * lr
        elif version == "V1":
            e_i = 1.0 + compute_weight * lr
        elif version == "V2":
            e_i = compute_weight * lr / max(dloss, EPS)
        else:
            raise ValueError(version)

        s_total += e_i
        prev_loss = cur_loss

        if cur_loss <= TARGET_LOSS:
            return {"steps": step, "S": s_total, "converged": True}

    return {"steps": MAX_STEPS, "S": s_total, "converged": False}


def main() -> None:
    data = make_dataset()
    report: dict[str, dict] = {}

    for version in ["V0", "V1", "V2"]:
        grid: list[dict] = []
        for cw in COMPUTE_WEIGHTS:
            results = {}
            for lr in LEARNING_RATES:
                results[lr] = train(lr, cw, version, data)
            converged = {lr: r for lr, r in results.items() if r["converged"]}
            if len(converged) >= 2:
                best_lr = min(converged, key=lambda lr: converged[lr]["S"])
                grid.append(
                    {
                        "compute_weight": cw,
                        "best_lr": best_lr,
                        "S_by_lr": {str(lr): round(r["S"], 4) for lr, r in results.items()},
                        "steps_by_lr": {str(lr): r["steps"] for lr, r in results.items()},
                    }
                )
        report[version] = {"grid": grid}

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
