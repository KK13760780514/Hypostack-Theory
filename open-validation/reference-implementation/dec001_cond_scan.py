#!/usr/bin/env python3
"""DEC-001 decision-support scan: Adam advantage vs Hessian condition number.

Background: XD-AI-ADAM-001 V2 raised X2_SCALE from 10 to 20 (empirical Hessian
condition number ~1e2 -> ~4e2), which amplified Adam's S savings from ~12% to
~50%. DEC-001 default recommendation (option C): do not change the criterion
immediately, but report a sensitivity curve so the community can judge the
fairness/discriminability trade-off. This script provides exactly that.

Method:
  For each X2_SCALE in {5, 7.5, 10, 12.5, 15, 20, 30, 40}, run the identical
  12-seed Adam vs best fixed-lr SGD protocol (same seeds, lr grid, tolerance,
  no-baseline rule as adam_dynamics.py V2) and report:
    - empirical Hessian condition number (max/min eigenvalue of the MSE
      Hessian, Jacobi eigensolver, averaged over seeds)
    - mean S_adam / mean S_best_sgd ratio and % savings
    - per-seed successes (>=11/12 with one-sided binomial p<0.01 => support)

  Read-out (per DEC-001 options):
    - ratio ~ 1 until ~4e2 and favorable only there  -> 4e2 choice is suspect (option B)
    - ratio improves monotonically/smoothly from ~1e2 -> gradual discriminability
      trade-off (option C: keep 4e2, publish the curve)

This is a decision-support tool (same status as issue001_sweep.py), NOT a new
claim submission. Output is JSON for direct review.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import random
import sys
from datetime import datetime, timezone

import adam_dynamics as ad

SCALES = [5.0, 7.5, 10.0, 12.5, 15.0, 20.0, 30.0, 40.0]


def make_dataset_scale(seed: int, scale: float) -> list[tuple[float, float, float]]:
    """Same data generator as adam_dynamics.make_dataset but with a tunable X2 scale."""
    rng = random.Random(seed)
    xs1 = [-1.0, -0.5, 0.0, 0.5, 1.0]
    data = []
    for x1 in xs1:
        x2 = rng.uniform(-1.0, 1.0) * scale
        y = ad.TRUE_W1 * x1 + ad.TRUE_W2 * x2 + ad.TRUE_B + rng.uniform(-0.05, 0.05)
        data.append((x1, x2, y))
    return data


def hessian_condition_number(data: list[tuple[float, float, float]]) -> float:
    """Empirical condition number of the MSE Hessian (3x3, w1/w2/b).

    H = (2/n) * sum_i [ [x1^2, x1*x2, x1], [x1*x2, x2^2, x2], [x1, x2, 1] ]
    Eigenvalues via the Jacobi rotation method (stdlib only).
    """
    n = len(data)
    h11 = sum(2 * x1 * x1 for x1, _, _ in data) / n
    h12 = sum(2 * x1 * x2 for x1, x2, _ in data) / n
    h13 = sum(2 * x1 for x1, _, _ in data) / n
    h22 = sum(2 * x2 * x2 for _, x2, _ in data) / n
    h23 = sum(2 * x2 for _, x2, _ in data) / n
    h33 = sum(2 * 1.0 for _, _, _ in data) / n

    a = [[h11, h12, h13], [h12, h22, h23], [h13, h23, h33]]

    def jacobi(A: list[list[float]]) -> list[float]:
        A = [row[:] for row in A]
        n_ = len(A)
        for _ in range(50):
            pm, qm, mx = 0, 1, 0.0
            for i in range(n_):
                for j in range(i + 1, n_):
                    if abs(A[i][j]) > mx:
                        mx, pm, qm = abs(A[i][j]), i, j
            if mx < 1e-12:
                break
            if A[pm][pm] == A[qm][qm]:
                theta = math.pi / 4
            else:
                theta = 0.5 * math.atan2(2 * A[pm][qm], A[qm][qm] - A[pm][pm])
            c, s = math.cos(theta), math.sin(theta)
            for k in range(n_):
                akp, akq = A[k][pm], A[k][qm]
                A[k][pm] = c * akp - s * akq
                A[k][qm] = s * akp + c * akq
            for k in range(n_):
                apk, aqk = A[pm][k], A[qm][k]
                A[pm][k] = c * apk - s * aqk
                A[qm][k] = s * apk + c * aqk
        return [A[i][i] for i in range(n_)]

    evs = jacobi(a)
    evs = sorted(evs)
    return evs[-1] / max(evs[0], 1e-12)


def run_protocol(scale: float) -> dict:
    """Run the exact V2 protocol (12 seeds) at a given feature scale."""
    per_seed = []
    successes = 0
    for seed in ad.SEEDS:
        data = make_dataset_scale(seed, scale)
        adam = ad.run_adam(data)
        sgd_results = {lr: ad.run_sgd(data, lr) for lr in ad.SGD_LR_GRID}
        sgd_converged = {lr: r for lr, r in sgd_results.items() if r["converged"]}
        if sgd_converged:
            best_sgd_S = min(r["S"] for r in sgd_converged.values())
        else:
            best_sgd_S = None
        if best_sgd_S is not None:
            ok = adam["converged"] and adam["S"] <= ad.TOLERANCE * best_sgd_S
        else:
            ok = adam["converged"]  # no-baseline rule (DEC-002 default A)
        successes += int(ok)
        no_baseline = best_sgd_S is None
        per_seed.append({
            "seed": seed, "adam_S": adam["S"], "best_sgd_S": best_sgd_S,
            "ok": ok, "no_sgd_baseline": no_baseline,
        })

    n = len(ad.SEEDS)
    p_value = ad.binom_sf(successes, n, ad.P0)
    sgd_Ss = [p["best_sgd_S"] for p in per_seed if p["best_sgd_S"] is not None]
    mean_adam = sum(p["adam_S"] for p in per_seed) / n
    mean_sgd = sum(sgd_Ss) / max(len(sgd_Ss), 1)
    ratio = mean_adam / mean_sgd if mean_sgd > 0 else float("nan")
    no_baseline_count = sum(1 for p in per_seed if p["no_sgd_baseline"])
    return {
        "scale": scale,
        "successes": successes,
        "n": n,
        "p_value": p_value,
        "support": successes >= 11 and p_value < ad.ALPHA,
        "mean_S_adam": mean_adam,
        "mean_S_sgd_best": mean_sgd,
        "ratio_adam_over_sgd": ratio,
        "savings_pct": (1 - ratio) * 100 if math.isfinite(ratio) else None,
        "no_sgd_baseline_seeds": no_baseline_count,
    }


def main() -> None:
    scan = []
    for scale in SCALES:
        conds = [
            hessian_condition_number(make_dataset_scale(seed, scale))
            for seed in ad.SEEDS
        ]
        mean_cond = sum(conds) / len(conds)
        row = run_protocol(scale)
        row["mean_hessian_cond"] = mean_cond
        scan.append(row)
        print(f"scale={scale:>5}: cond={mean_cond:9.1f}  "
              f"ratio={row['ratio_adam_over_sgd']:.3f}  "
              f"successes={row['successes']}/12  p={row['p_value']:.4f}  "
              f"{'SUPPORT' if row['support'] else 'challenge'}", file=sys.stderr)

    output = {
        "purpose": "DEC-001 decision support (option C): Adam S-ratio vs Hessian condition number",
        "protocol": {
            "claim_id": "XD-AI-ADAM-001",
            "seeds": ad.SEEDS,
            "sgd_lr_grid": ad.SGD_LR_GRID,
            "max_steps": ad.MAX_STEPS,
            "tolerance": ad.TOLERANCE,
            "target_loss": ad.TARGET_LOSS,
            "no_baseline_rule": "Adam converges + no SGD baseline converges => Adam wins (DEC-002 default A)",
            "success_threshold": ">=11/12, one-sided binomial p<0.01",
        },
        "scan": scan,
        "read_out": (
            "If ratio~1 until ~4e2 and favorable only there, the 4e2 choice is "
            "suspect (DEC-001 option B). If the ratio improves smoothly/monotonically "
            "from ~1e2, the effect is a gradual discriminability trade-off (option C)."
        ),
        "code_hash": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
        "environment": {
            "os": platform.platform(),
            "python_version": sys.version.split()[0],
            "dependencies": "python-stdlib-only (imports adam_dynamics.py)",
        },
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
