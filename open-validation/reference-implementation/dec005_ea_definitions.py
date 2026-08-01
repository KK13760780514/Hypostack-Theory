#!/usr/bin/env python3
"""DEC-005 decision-support scan: which E definition best predicts the path?

Background (ISSUE-004 / DEC-004 / DEC-005): V1 used S = sum(Ea_i) (total
barrier) and was challenged (8/8 temps picked the Arrhenius path, 0/8 matched).
V2 uses S = E_eff (effective activation energy from the steady-state
approximation, N = 1) and passed 16/16. Two other candidate definitions from
DEC-005 remain: rate-limiting-step Ea = max(Ea_i), and free-energy barrier
dG_double_dagger (needs entropy data, out of scope here).

This script re-runs the same ODE kinetics with three E definitions:
  - E_eff      (V2 default, steady-state approximation)
  - E_maxstep  (rate-limiting step, max(Ea1, Ea2))
  - E_sum      (V1 total barrier, sum(Ea_i))
across the two preregistered configs (symmetric, asymmetric) PLUS a
"comparable-rates" config (Ea1=25, Ea2=35, Ea3=55) where the two steps have
similar rates so E_eff and E_maxstep are pushed furthest apart.

Read-out for DEC-005:
  - If E_eff and E_maxstep agree on every config, the existing 16/16 result
    cannot distinguish them (both consistent with the evidence; DEC-005 option
    A confirmed with the caveat that the E_eff vs E_maxstep choice is
    underdetermined by current data).
  - If E_sum fails while E_eff/E_maxstep pass, V1's challenge is reaffirmed.

This is a decision-support tool (same status as issue001_sweep.py), NOT a new
claim submission. Output is JSON for direct review.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone

import chemical_path_v2 as cp

# Extra config to maximally separate E_eff from E_maxstep (steps with
# comparable rates; not part of the preregistered V2 configs).
COMPARABLE_CONFIG = ("comparable_rates", 25e3, 35e3, 55e3)

ALL_CONFIGS = cp.CONFIGS + [COMPARABLE_CONFIG]


def e_definitions(ea1: float, ea2: float, ea3: float, T: float) -> dict:
    """Return S under each candidate E definition (path A is 2-step, path B 1-step)."""
    return {
        "E_eff": cp.effective_ea(ea1, ea2, T),
        "E_maxstep": max(ea1, ea2),
        "E_sum": ea1 + ea2,
        "E_B_single": ea3,  # path B: single step, all definitions coincide
    }


def main() -> None:
    per_config = []
    summary = {}
    for name, ea1, ea2, ea3 in ALL_CONFIGS:
        correct = {"E_eff": 0, "E_maxstep": 0, "E_sum": 0}
        details = []
        for T in cp.TEMPS:
            sim = cp.simulate(ea1, ea2, ea3, T)
            actual = sim["actual_path"]
            defs = e_definitions(ea1, ea2, ea3, T)
            # Predictions: each definition's S_A compared against S_B (single step).
            s_b = defs["E_B_single"]
            preds = {
                "E_eff": "B" if defs["E_eff"] > s_b else "A",
                "E_maxstep": "B" if defs["E_maxstep"] > s_b else "A",
                "E_sum": "B" if defs["E_sum"] > s_b else "A",
            }
            for k, p in preds.items():
                if p == actual:
                    correct[k] += 1
            details.append({
                "T": T,
                "actual": actual,
                "S_eff_A": round(defs["E_eff"], 1),
                "S_maxstep_A": defs["E_maxstep"],
                "S_sum_A": defs["E_sum"],
                "S_B": s_b,
                "pred_eff": preds["E_eff"],
                "pred_maxstep": preds["E_maxstep"],
                "pred_sum": preds["E_sum"],
            })
        n = len(cp.TEMPS)
        per_config.append({
            "config": name,
            "Ea": {"Ea1": ea1, "Ea2": ea2, "Ea3": ea3},
            "matches": correct,
            "n": n,
            "per_temp": details,
        })
        for k in correct:
            summary.setdefault(k, []).append(correct[k])

    # Aggregate across configs.
    totals = {k: sum(v) for k, v in summary.items()}
    total_n = len(ALL_CONFIGS) * len(cp.TEMPS)

    output = {
        "purpose": "DEC-005 decision support: candidate E definitions vs Arrhenius path selection",
        "configs": ALL_CONFIGS,
        "n_temps": cp.TEMPS,
        "per_config": per_config,
        "aggregate_matches": totals,
        "total_n": total_n,
        "read_out": (
            f"E_eff {totals['E_eff']}/{total_n}, E_maxstep {totals['E_maxstep']}/{total_n}, "
            f"E_sum {totals['E_sum']}/{total_n}. "
            "If E_eff == E_maxstep on every config, current evidence cannot distinguish "
            "them (DEC-005 option A: keep E_eff, note the underdetermination). "
            "If E_sum < the others, V1 challenge reaffirmed."
        ),
        "code_hash": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
        "environment": {
            "os": platform.platform(),
            "python_version": sys.version.split()[0],
            "dependencies": "python-stdlib-only (imports chemical_path_v2.py)",
        },
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
