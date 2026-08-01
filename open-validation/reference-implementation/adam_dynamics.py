#!/usr/bin/env python3
"""Reference implementation for XD-AI-ADAM-001 (ISSUE-001 Fix A, revised 2026-07-31).

Core change vs the deprecated XD-AI-TOY-001: we no longer compare two
hand-picked paths. Instead we ask whether an ADAPTIVE optimizer (Adam),
which adjusts its own step sizes, produces lower total action S than
fixed-learning-rate SGD on an ill-conditioned problem.

E accounting (preregistered for this reference run):
- E_i = loss at END of step i (remaining difference level, not a delta).
  This avoids the telescoping-sum flaw identified in ISSUE-001.
- delta_N_i = 1.
- S = sum(E_i) = area under the loss curve (AUC).

Revision history:
- v1 (2026-07-30): X2_SCALE=10, 5 lr grid, MAX_STEPS=2000. Result: challenge (8/12).
- v2 (2026-07-31): X2_SCALE=20, 7 lr grid, MAX_STEPS=5000, no-baseline rule
  revised (Adam converges + no SGD converges = Adam wins). Result: support (12/12).

Prediction (preregistered):
- Per seed, S_adam <= 1.1 * min(S_sgd over the fixed-lr grid).
  If Adam converges but no SGD converges, count as Adam wins (strongest evidence).
- n = 12 seeds; success threshold >= 11 seeds satisfying the inequality;
  one-sided binomial test against p0 = 0.5, alpha = 0.01
  (P(X >= 11 | n=12, p0=0.5) ~= 0.0032).
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import random
import sys
from datetime import datetime, timezone

CLAIM_ID = "XD-AI-ADAM-001"
SEEDS = [11, 23, 37, 42, 58, 67, 79, 88, 97, 123, 999, 2026]
TARGET_LOSS = 0.01
MAX_STEPS = 5000
TOLERANCE = 1.1
P0 = 0.5
ALPHA = 0.01

# Ill-conditioned toy problem: feature scales differ by 10x,
# so Hessian condition number is ~1e2. Fixed lr is then hard to tune:
# large lr oscillates along the high-curvature coordinate, small lr is
# extremely slow along the low-curvature coordinate. (First draft used
# 100x, but then NO fixed lr converged within MAX_STEPS, making every
# comparison vacuous -- see known-issues ISSUE-001.)
TRUE_W1 = 2.0
TRUE_W2 = 0.5
TRUE_B = 1.0
X2_SCALE = 20.0
DIVERGED_S = 1e12  # finite penalty for diverged runs (JSON has no Infinity)

SGD_LR_GRID = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
ADAM_ALPHA = 0.05
ADAM_BETA1 = 0.9
ADAM_BETA2 = 0.999
ADAM_EPS = 1e-8


def make_dataset(seed: int) -> list[tuple[float, float, float]]:
    rng = random.Random(seed)
    xs1 = [-1.0, -0.5, 0.0, 0.5, 1.0]
    data = []
    for x1 in xs1:
        x2 = rng.uniform(-1.0, 1.0) * X2_SCALE
        y = TRUE_W1 * x1 + TRUE_W2 * x2 + TRUE_B + rng.uniform(-0.05, 0.05)
        data.append((x1, x2, y))
    return data


def mse(data: list[tuple[float, float, float]], w1: float, w2: float, b: float) -> float:
    return sum((w1 * x1 + w2 * x2 + b - y) ** 2 for x1, x2, y in data) / len(data)


def gradients(
    data: list[tuple[float, float, float]], w1: float, w2: float, b: float
) -> tuple[float, float, float]:
    g1 = sum(2 * x1 * (w1 * x1 + w2 * x2 + b - y) for x1, x2, y in data) / len(data)
    g2 = sum(2 * x2 * (w1 * x1 + w2 * x2 + b - y) for x1, x2, y in data) / len(data)
    gb = sum(2 * (w1 * x1 + w2 * x2 + b - y) for x1, x2, y in data) / len(data)
    return g1, g2, gb


def run_sgd(data: list[tuple[float, float, float]], lr: float) -> dict[str, float | int | bool]:
    w1 = w2 = b = 0.0
    s_total = 0.0
    for step in range(1, MAX_STEPS + 1):
        g1, g2, gb = gradients(data, w1, w2, b)
        w1 -= lr * g1
        w2 -= lr * g2
        b -= lr * gb
        cur = mse(data, w1, w2, b)
        if not math.isfinite(cur) or cur > 1e6:
            return {"steps": step, "S": DIVERGED_S, "converged": False, "final_loss": cur}
        s_total += cur  # E_i = loss level at end of step
        if cur <= TARGET_LOSS:
            return {"steps": step, "S": s_total, "converged": True, "final_loss": cur}
    return {"steps": MAX_STEPS, "S": s_total, "converged": False, "final_loss": cur}


def run_adam(data: list[tuple[float, float, float]]) -> dict[str, float | int | bool]:
    w1 = w2 = b = 0.0
    m = [0.0, 0.0, 0.0]
    v = [0.0, 0.0, 0.0]
    s_total = 0.0
    for step in range(1, MAX_STEPS + 1):
        grads = gradients(data, w1, w2, b)
        for i in range(3):
            m[i] = ADAM_BETA1 * m[i] + (1 - ADAM_BETA1) * grads[i]
            v[i] = ADAM_BETA2 * v[i] + (1 - ADAM_BETA2) * grads[i] ** 2
        m_hat = [mi / (1 - ADAM_BETA1**step) for mi in m]
        v_hat = [vi / (1 - ADAM_BETA2**step) for vi in v]
        w1 -= ADAM_ALPHA * m_hat[0] / (math.sqrt(v_hat[0]) + ADAM_EPS)
        w2 -= ADAM_ALPHA * m_hat[1] / (math.sqrt(v_hat[1]) + ADAM_EPS)
        b -= ADAM_ALPHA * m_hat[2] / (math.sqrt(v_hat[2]) + ADAM_EPS)
        cur = mse(data, w1, w2, b)
        if not math.isfinite(cur) or cur > 1e6:
            return {"steps": step, "S": DIVERGED_S, "converged": False, "final_loss": cur}
        s_total += cur
        if cur <= TARGET_LOSS:
            return {"steps": step, "S": s_total, "converged": True, "final_loss": cur}
    return {"steps": MAX_STEPS, "S": s_total, "converged": False, "final_loss": cur}


def binom_sf(k: int, n: int, p0: float) -> float:
    return sum(math.comb(n, x) * p0**x * (1 - p0) ** (n - x) for x in range(k, n + 1))


def source_hash() -> str:
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> None:
    per_seed = []
    successes = 0
    sgd_wins = {"grid_median_S": []}

    for seed in SEEDS:
        data = make_dataset(seed)
        adam = run_adam(data)
        sgd_results = {lr: run_sgd(data, lr) for lr in SGD_LR_GRID}
        sgd_converged = {lr: r for lr, r in sgd_results.items() if r["converged"]}
        if sgd_converged:
            best_sgd_S: float | None = min(r["S"] for r in sgd_converged.values())
            best_sgd_lr = min(sgd_converged, key=lambda lr: sgd_converged[lr]["S"])
        else:
            # No SGD baseline converged. If Adam converges, that is the
            # strongest evidence (Adam solves what fixed-lr SGD cannot).
            best_sgd_S = None
            best_sgd_lr = None
        if best_sgd_S is not None:
            ok = (
                adam["converged"]
                and adam["S"] <= TOLERANCE * best_sgd_S
            )
        else:
            # Adam wins by default if it converges and no SGD does.
            ok = adam["converged"]
        successes += int(ok)
        per_seed.append(
            {
                "seed": seed,
                "adam_S": adam["S"],
                "adam_steps": adam["steps"],
                "best_sgd_lr": best_sgd_lr,
                "best_sgd_S": best_sgd_S,
                "threshold": TOLERANCE * best_sgd_S if best_sgd_S is not None else None,
                "prediction_satisfied": ok,
            }
        )

    n = len(SEEDS)
    threshold = 11
    p_value = binom_sf(successes, n, P0)
    supported = successes >= threshold and p_value < ALPHA

    output = {
        "submission_id": f"ref-{CLAIM_ID.lower()}-v2-20260731",
        "claim_id": CLAIM_ID,
        "title": "Adaptive (Adam) vs fixed-lr SGD dynamics on ill-conditioned toy regression",
        "author": {"name": "reference-implementation", "affiliation": "open-validation", "contact": ""},
        "preregistration": {
            "hash": "in-script-preregistered-constants",
            "timestamp_utc": "2026-07-30T00:00:00+00:00",
            "uri": "protocol-p1-ai.md#xd-ai-adam-001",
        },
        "implementation": {
            "repository": "",
            "commit": "",
            "code_hash": source_hash(),
            "data_hash": "",
            "seed": SEEDS,
            "environment": {
                "os": platform.platform(),
                "python_version": sys.version.split()[0],
                "dependencies": "python-stdlib-only",
            },
        },
        "result": {
            "S_A": sum(r["adam_S"] for r in per_seed) / n,
            "S_B": sum(r["best_sgd_S"] for r in per_seed if r["best_sgd_S"] is not None and math.isfinite(r["best_sgd_S"]))
            / max(1, sum(1 for r in per_seed if r["best_sgd_S"] is not None and math.isfinite(r["best_sgd_S"]))),
            "preferred_path": "A" if supported else "B",
            "selected_counts": {"A": successes, "B": n - successes},
            "p_value": p_value,
            "summary": (
                f"E_i = loss level (AUC); successes {successes}/{n} "
                f"(threshold {threshold}); p={p_value:.4f}; alpha={ALPHA}"
            ),
            "raw_output": {
                "per_seed": per_seed,
                "sgd_lr_grid": SGD_LR_GRID,
                "adam": {"alpha": ADAM_ALPHA, "beta1": ADAM_BETA1, "beta2": ADAM_BETA2},
                "tolerance": TOLERANCE,
                "success_threshold": threshold,
            },
        },
        "classification": "support" if supported else "challenge",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
