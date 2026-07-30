#!/usr/bin/env python3
"""Reference implementation for XD-P1-CHEM-001.

Replaces the circular XD-P1-SIM-001 (softmax selector) with a natural
system governed by an independent physical law: Arrhenius chemical kinetics.

DESIGN -- why this has genuine discriminating power:
  Two reaction paths from R to P:

    Path A (multi-step, low barriers):  R --k1--> I --k2--> P
    Path B (single-step, high barrier): R --k3--> P

  E_i = activation energy Ea_i (J/mol) -- an independent physical quantity,
        NOT a function we defined to prefer low-S.
  N   = number of steps.
  S   = sum(Ea_i) -- total barrier height (NOT a telescoping sum; each Ea
        is an independent property of each reaction step).

  XuanDie prediction: system prefers the path with lower S.
  Arrhenius prediction: system prefers the path whose rate-limiting step
        has the lowest Ea.

  We choose parameters so these predictions CONFLICT:
    Ea1 = Ea2 = 30 kJ/mol  => S_A = 60 kJ/mol (lower total? NO, see below)
    Ea3 = 55 kJ/mol          => S_B = 55 kJ/mol

  S_B < S_A  =>  XuanDie predicts path B.
  Ea1 < Ea3  =>  Arrhenius predicts path A (k1 >> k3).

  If the system produces more P via path A, XuanDie's S-definition is
  challenged for path selection. This is a falsifiable, non-circular test.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone

CLAIM_ID = "XD-P1-CHEM-001"

# --- Reaction parameters (preregistered) ---
EA1 = 30e3   # J/mol, path A step 1
EA2 = 30e3   # J/mol, path A step 2
EA3 = 55e3   # J/mol, path B single step
A_PRE = 1e10  # pre-exponential factor, 1/s
T = 300.0     # K
R_GAS = 8.314  # J/(mol·K)

# XuanDie S (total barrier)
S_A = EA1 + EA2   # 60 kJ/mol
S_B = EA3          # 55 kJ/mol
XUANDIE_PRED = "B" if S_B < S_A else "A"

# Arrhenius rate constants
K1 = A_PRE * math.exp(-EA1 / (R_GAS * T))
K2 = A_PRE * math.exp(-EA2 / (R_GAS * T))
K3 = A_PRE * math.exp(-EA3 / (R_GAS * T))

# Simulation
DT = 1e-6     # s, base step
T_END = 0.1   # s (reaction mostly completes well before 0.1s at all temps)
R_INIT = 1.0  # mol/L
MAX_STEPS = 2_000_000  # safety cap

# Statistics: 8 temperature points to check robustness
TEMPS = [280.0, 290.0, 300.0, 310.0, 320.0, 350.0, 400.0, 500.0]
ALPHA = 0.01


def simulate(T_sim: float) -> dict:
    """Run ODE integration at temperature T_sim, return path yields."""
    k1 = A_PRE * math.exp(-EA1 / (R_GAS * T_sim))
    k2 = A_PRE * math.exp(-EA2 / (R_GAS * T_sim))
    k3 = A_PRE * math.exp(-EA3 / (R_GAS * T_sim))

    # Adaptive dt: keep dt * k_max < 0.01 for Euler stability,
    # but cap total steps to avoid runaway at high T.
    k_max = max(k1, k2, k3)
    dt = min(DT, 0.01 / k_max) if k_max > 0 else DT
    n_steps = min(int(T_END / dt), MAX_STEPS)
    dt = T_END / n_steps  # recompute dt to exactly hit T_END

    r = R_INIT
    i_conc = 0.0
    p_a = 0.0
    p_b = 0.0

    for _ in range(n_steps):
        dr = -(k1 + k3) * r
        di = k1 * r - k2 * i_conc
        dpa = k2 * i_conc
        dpb = k3 * r

        r += dr * dt
        i_conc += di * dt
        p_a += dpa * dt
        p_b += dpb * dt

    return {
        "T": T_sim,
        "k1": k1,
        "k2": k2,
        "k3": k3,
        "dt_used": dt,
        "P_A": p_a,
        "P_B": p_b,
        "actual_path": "A" if p_a > p_b else "B",
        "ratio_A_over_B": p_a / max(p_b, 1e-30),
    }


def source_hash() -> str:
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> None:
    results = [simulate(t) for t in TEMPS]

    # XuanDie predicts B (lower S). Count how many temps produce B.
    xuandie_correct = sum(1 for r in results if r["actual_path"] == XUANDIE_PRED)
    n = len(TEMPS)

    # Binomial test: H0 = random (p0=0.5), H1 = XuanDie correct more often
    p_value = sum(
        math.comb(n, x) * 0.5**x * 0.5**(n - x)
        for x in range(xuandie_correct, n + 1)
    )

    supported = xuandie_correct >= 7 and p_value < ALPHA
    classification = "support" if supported else "challenge"

    output = {
        "submission_id": f"ref-{CLAIM_ID.lower()}-20260730",
        "claim_id": CLAIM_ID,
        "title": "Chemical path competition: XuanDie S vs Arrhenius kinetics",
        "author": {"name": "reference-implementation", "affiliation": "open-validation", "contact": ""},
        "preregistration": {
            "hash": "in-script-preregistered-constants",
            "timestamp_utc": "2026-07-30T00:00:00+00:00",
            "uri": "protocol-p1-ai.md#xd-p1-chem-001",
        },
        "implementation": {
            "repository": "",
            "commit": "",
            "code_hash": source_hash(),
            "data_hash": "",
            "seed": 0,
            "environment": {
                "os": platform.platform(),
                "python_version": sys.version.split()[0],
                "dependencies": "python-stdlib-only",
            },
        },
        "result": {
            "S_A": S_A,
            "S_B": S_B,
            "preferred_path": XUANDIE_PRED,
            "selected_counts": {
                "A": n - xuandie_correct,
                "B": xuandie_correct,
            },
            "p_value": p_value,
            "summary": (
                f"XuanDie predicts {XUANDIE_PRED} (S_{XUANDIE_PRED}={min(S_A,S_B):.0f} < "
                f"S_{'A' if XUANDIE_PRED=='B' else 'B'}={max(S_A,S_B):.0f}); "
                f"actual: {xuandie_correct}/{n} temps match; p={p_value:.4f}"
            ),
            "raw_output": {
                "Ea": {"Ea1": EA1, "Ea2": EA2, "Ea3": EA3},
                "S_A": S_A,
                "S_B": S_B,
                "xuandie_prediction": XUANDIE_PRED,
                "temperatures": TEMPS,
                "results": [
                    {
                        "T": r["T"],
                        "P_A": round(r["P_A"], 6),
                        "P_B": round(r["P_B"], 6),
                        "actual_path": r["actual_path"],
                        "ratio_A_over_B": round(r["ratio_A_over_B"], 2),
                    }
                    for r in results
                ],
            },
        },
        "classification": classification,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
