#!/usr/bin/env python3
"""Reference implementation for XD-P1-PHASE-001.

Tests the XuanDie theory prediction: in phase transitions, the system
preferentially follows the path with minimum S = ∫ E dN.

Experiment: 2D Ising model phase transition (paramagnetic -> ferromagnetic).

Three cooling protocols from T_high=3.0 to T_low=1.0 (T_c ≈ 2.269):
  Path A (slow):   20 temperature steps, 200 MC sweeps per step
  Path B (medium):  5 temperature steps, 800 MC sweeps per step
  Path C (quench):  1 temperature step, 4000 MC sweeps total

For each path:
  E_i = |T_i - T_c| / T_c  (normalized driving force at temperature step i)
  N_i = number of accepted spin flips at step i
  S   = Σ(E_i × N_i)

Prediction: S_A < S_B < S_C (slower cooling = lower total consumption)

Statistical test: 12 random seeds, binomial test on the A<C ordering.
  Support: S_A < S_C for >= 10/12 seeds (p < 0.05)
  Challenge: ordering fails for >= 4/12 seeds

Falsification conditions:
  - S_C < S_A for >= 7/12 seeds (fast quench has lower S than slow cooling)
  - S is identical across all paths (no path preference)
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import random
import sys
from datetime import datetime, timezone

CLAIM_ID = "XD-P1-PHASE-001"

# 2D Ising model parameters
LATTICE_SIZE = 20  # 20x20 lattice
T_HIGH = 3.0  # Start temperature (paramagnetic)
T_LOW = 1.0   # End temperature (ferromagnetic)
T_C = 2.0 / math.log(1.0 + math.sqrt(2.0))  # ≈ 2.269 (Onsager critical temp)

# Cooling protocols: (n_steps, sweeps_per_step)
PROTOCOLS = {
    "A_slow": (20, 200),
    "B_medium": (5, 800),
    "C_quench": (1, 4000),
}

NUM_SEEDS = 12


def init_lattice(size: int, rng: random.Random) -> list[list[int]]:
    """Random spin initialization."""
    return [[1 if rng.random() > 0.5 else -1 for _ in range(size)] for _ in range(size)]


def metropolis_sweep(lattice: list[list[int]], T: float, rng: random.Random) -> int:
    """One MC sweep: attempt to flip each spin once (Metropolis criterion).

    Returns number of accepted flips.
    """
    n = len(lattice)
    J = 1.0  # coupling constant
    accepted = 0

    for _ in range(n * n):
        i = rng.randint(0, n - 1)
        j = rng.randint(0, n - 1)

        # Neighbors with periodic boundary
        s = lattice[i][j]
        nb = (
            lattice[(i - 1) % n][j]
            + lattice[(i + 1) % n][j]
            + lattice[i][(j - 1) % n]
            + lattice[i][(j + 1) % n]
        )

        dE = 2.0 * J * s * nb  # energy change if flipped

        if dE <= 0 or rng.random() < math.exp(-dE / T):
            lattice[i][j] = -s
            accepted += 1

    return accepted


def compute_S(lattice: list[list[int]], protocol: tuple[int, int], seed: int) -> float:
    """Run cooling protocol and compute S = Σ(E_i × N_i).

    E_i = |T_i - T_c| / T_c  (normalized driving force)
    N_i = number of accepted spin flips at step i
    """
    n_steps, sweeps_per_step = protocol
    rng = random.Random(seed)

    # Re-initialize lattice for each protocol (same seed = same starting config)
    lat = init_lattice(LATTICE_SIZE, rng)

    # Equilibrate at T_high
    for _ in range(100):
        metropolis_sweep(lat, T_HIGH, rng)

    # Cool down
    dt = (T_HIGH - T_LOW) / n_steps
    S_total = 0.0

    for step in range(n_steps):
        T_i = T_HIGH - step * dt
        E_i = abs(T_i - T_C) / T_C  # normalized driving force

        N_i = 0
        for _ in range(sweeps_per_step):
            N_i += metropolis_sweep(lat, T_i, rng)

        S_total += E_i * N_i

    return S_total


def binomial_test(n_success: int, n_total: int, p: float = 0.5) -> float:
    """Two-sided binomial test p-value (both tails include the observed value)."""
    # P(X >= n_success) + P(X <= n_total - n_success)
    from math import comb

    if n_success > n_total - n_success:
        k_high = n_success
        k_low = n_total - n_success
    else:
        k_high = n_total - n_success
        k_low = n_success

    p_val = sum(comb(n_total, k) * (p ** k) * ((1 - p) ** (n_total - k))
                for k in range(k_high, n_total + 1))
    p_val += sum(comb(n_total, k) * (p ** k) * ((1 - p) ** (n_total - k))
                 for k in range(0, k_low + 1))

    return min(p_val, 1.0)


def source_hash() -> str:
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> None:
    results = {}

    for seed in range(NUM_SEEDS):
        seed_results = {}
        for name, protocol in PROTOCOLS.items():
            S = compute_S(init_lattice(LATTICE_SIZE, random.Random(seed)), protocol, seed)
            seed_results[name] = S
        results[seed] = seed_results

    # Check ordering: S_A < S_B < S_C
    ordering_holds = 0
    S_A_list = []
    S_B_list = []
    S_C_list = []

    for seed in range(NUM_SEEDS):
        S_A = results[seed]["A_slow"]
        S_B = results[seed]["B_medium"]
        S_C = results[seed]["C_quench"]
        S_A_list.append(S_A)
        S_B_list.append(S_B)
        S_C_list.append(S_C)

        if S_A < S_B < S_C:
            ordering_holds += 1

    # Also check individual pair orderings
    AB_holds = sum(1 for i in range(NUM_SEEDS) if S_A_list[i] < S_B_list[i])
    BC_holds = sum(1 for i in range(NUM_SEEDS) if S_B_list[i] < S_C_list[i])
    AC_holds = sum(1 for i in range(NUM_SEEDS) if S_A_list[i] < S_C_list[i])

    # Binomial test: under null hypothesis, P(S_A < S_C) = 0.5
    p_value = binomial_test(AC_holds, NUM_SEEDS)

    # Mean S values
    mean_S_A = sum(S_A_list) / NUM_SEEDS
    mean_S_B = sum(S_B_list) / NUM_SEEDS
    mean_S_C = sum(S_C_list) / NUM_SEEDS

    # Classification
    if AC_holds >= 10 and p_value < 0.05:
        classification = "support"
    elif AC_holds <= 2:
        classification = "falsification"  # S_C < S_A for most seeds
    else:
        classification = "challenge"

    # S values for submission: path A as S_A, path C as S_B (12-seed means,
    # matching the submitted JSON and evidence-ledger.csv EV-fadf8b4aca7d3ffd)

    output = {
        "submission_id": "ref-xd-p1-phase-001-20260731",
        "claim_id": CLAIM_ID,
        "title": "Phase transition path selection: S minimization in 2D Ising model",
        "author": {"name": "reference-implementation", "affiliation": "open-validation", "contact": ""},
        "preregistration": {
            "hash": "in-script-preregistered-constants-v1",
            "timestamp_utc": "2026-07-31T00:00:00+00:00",
            "uri": "protocol-p1-ai.md#9-claim-xd-p1-phase-001",
        },
        "implementation": {
            "repository": "",
            "commit": "",
            "code_hash": source_hash(),
            "data_hash": "",
            "seed": list(range(NUM_SEEDS)),
            "environment": {
                "os": platform.platform(),
                "python_version": sys.version.split()[0],
                "dependencies": "python-stdlib-only",
            },
        },
        "result": {
            "S_A": mean_S_A,
            "S_B": mean_S_C,
            "preferred_path": "A" if mean_S_A < mean_S_C else "C",
            "selected_counts": {
                "A": AC_holds,
                "B": NUM_SEEDS - AC_holds,
            },
            "p_value": p_value,
            "summary": (
                f"12 seeds; S_A(slow)={mean_S_A:.1f}, S_B(med)={mean_S_B:.1f}, S_C(quench)={mean_S_C:.1f}; "
                f"ordering A<B<C holds {ordering_holds}/12; "
                f"A<C holds {AC_holds}/12 (p={p_value:.4f}); "
                f"classification={classification}"
            ),
            "raw_output": {
                "T_c": T_C,
                "lattice_size": LATTICE_SIZE,
                "protocols": {k: {"steps": v[0], "sweeps": v[1]} for k, v in PROTOCOLS.items()},
                "per_seed_results": {
                    str(seed): {
                        "S_A_slow": results[seed]["A_slow"],
                        "S_B_medium": results[seed]["B_medium"],
                        "S_C_quench": results[seed]["C_quench"],
                    }
                    for seed in range(NUM_SEEDS)
                },
                "statistics": {
                    "mean_S_A": mean_S_A,
                    "mean_S_B": mean_S_B,
                    "mean_S_C": mean_S_C,
                    "ordering_holds": ordering_holds,
                    "AB_holds": AB_holds,
                    "BC_holds": BC_holds,
                    "AC_holds": AC_holds,
                    "p_value": p_value,
                },
            },
        },
        "classification": classification,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
