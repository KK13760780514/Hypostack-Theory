#!/usr/bin/env python3
"""Q3 convergence check for XD-P1-PHASE-001 (math-foundations.md Q3).

Question: does the discrete sum S = Σ(E_i × ΔN_i) converge under mesh
refinement of the temperature steps? This is the lowest-cost entry point
listed in math-foundations.md for the continuum-limit question.

Method: fix total MC work per run at 4000 sweeps (same as Path A's
20×200). Vary the number of temperature steps n_steps ∈ {2,5,10,20,50,
100,200,400} with sweeps_per_step = 4000/n_steps. Reuse the E/N/S
definitions and seed handling of phase_transition.py. Report S(n) and
the ratio S(n)/S(20) to expose whether a continuum limit appears to
exist. 12 seeds are used so that mean/std give a sense of variance.

This is a numerical exploration, NOT a claim submission. Classification
column is advisory only.
"""

from __future__ import annotations

import json
import math
import random

LATTICE_SIZE = 20
T_HIGH = 3.0
T_LOW = 1.0
T_C = 2.0 / math.log(1.0 + math.sqrt(2.0))  # ≈ 2.269
TOTAL_SWEEPS = 4000  # fixed total MC work, matching Path A (20×200)
N_STEPS_GRID = [2, 5, 10, 20, 50, 100, 200, 400]
SEEDS = list(range(12))  # 12 seeds (strengthened from the 3-seed exploration)


def init_lattice(size: int, rng: random.Random) -> list[list[int]]:
    return [[1 if rng.random() > 0.5 else -1 for _ in range(size)] for _ in range(size)]


def metropolis_sweep(lattice: list[list[int]], T: float, rng: random.Random) -> int:
    n = len(lattice)
    J = 1.0
    accepted = 0
    for _ in range(n * n):
        i = rng.randint(0, n - 1)
        j = rng.randint(0, n - 1)
        s = lattice[i][j]
        nb = (
            lattice[(i - 1) % n][j]
            + lattice[(i + 1) % n][j]
            + lattice[i][(j - 1) % n]
            + lattice[i][(j + 1) % n]
        )
        dE = 2.0 * J * s * nb
        if dE <= 0 or rng.random() < math.exp(-dE / T):
            lattice[i][j] = -s
            accepted += 1
    return accepted


def compute_S(n_steps: int, seed: int) -> float:
    """Run cooling with n_steps temperature steps and fixed total sweeps."""
    sweeps_per_step = TOTAL_SWEEPS // n_steps
    rng = random.Random(seed)
    lat = init_lattice(LATTICE_SIZE, rng)

    # Equilibrate at T_high (same as reference implementation)
    for _ in range(100):
        metropolis_sweep(lat, T_HIGH, rng)

    dt = (T_HIGH - T_LOW) / n_steps
    S_total = 0.0
    for step in range(n_steps):
        T_i = T_HIGH - step * dt
        E_i = abs(T_i - T_C) / T_C
        N_i = 0
        for _ in range(sweeps_per_step):
            N_i += metropolis_sweep(lat, T_i, rng)
        S_total += E_i * N_i
    return S_total


def main() -> None:
    results: dict[str, list[float]] = {str(n): [] for n in N_STEPS_GRID}
    for n in N_STEPS_GRID:
        for seed in SEEDS:
            results[str(n)].append(compute_S(n, seed))

    means = {int(n): sum(v) / len(v) for n, v in results.items()}
    stds = {
        int(n): math.sqrt(sum((x - means[int(n)]) ** 2 for x in v) / len(v))
        for n, v in results.items()
    }
    s20 = means[20]
    ratios = {n: means[n] / s20 for n in means}

    # Convergence diagnostic: relative range of the last two grid points
    last_two = N_STEPS_GRID[-2:]
    rel_range = (means[last_two[1]] - means[last_two[0]]) / means[last_two[0]] if means[last_two[0]] else float("nan")

    print(json.dumps({
        "purpose": "Q3 mesh-refinement convergence check (math-foundations.md Q3)",
        "config": {
            "lattice": f"{LATTICE_SIZE}x{LATTICE_SIZE}",
            "T_high": T_HIGH, "T_low": T_LOW, "T_c": T_C,
            "total_sweeps_per_run": TOTAL_SWEEPS,
            "n_steps_grid": N_STEPS_GRID,
            "seeds": SEEDS,
        },
        "mean_S_per_n_steps": means,
        "std_S_per_n_steps": stds,
        "ratio_vs_n_steps_20": ratios,
        "convergence_diagnostic": {
            "last_two_n_steps": last_two,
            "relative_change_between_last_two": rel_range,
        },
        "interpretation": (
            "If relative_change_between_last_two -> 0 as n_steps grows, the discrete sum "
            "appears to converge (continuum limit plausible). If it stays large or oscillates, "
            "the discrete definition is grid-dependent and needs the theory work in "
            "math-foundations.md Q1/Q2 before a continuum statement is justified."
        ),
        "classification_advisory": "exploratory",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
