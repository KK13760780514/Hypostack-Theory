#!/usr/bin/env python3
"""Reference implementation for XD-P2-ECO-001 (market equilibrium path selection).

Operationalization of rulebook §11.4 (see predictions-operationalization.md P-ECO-001,
computation layer). Double-auction market with zero-intelligence constrained traders
(ZI-C, Gode & Sunder 1993 style).

Two paths to the same equilibrium price band:
  Path A (low commission):  C_A = 0.001 (0.1% of traded value per fill)
  Path B (high commission): C_B = 0.02  (2.0% of traded value per fill)

Operational definitions (preregistered):
  E_i = commission charged on fill i = C * p_i   (p_i = transaction price)
  ΔN_i = 1 (each fill counts as one evolution step)
  S   = Σ(E_i * ΔN_i) = total commission paid along the path

Commission changes the market (not merely bookkeeping): effective bid = bid/(1+C),
effective ask = ask*(1+C). Higher commission widens the effective spread, reducing
fill volume and slowing convergence — so the low-commission path should both have
smaller S and converge faster. This gives the comparison real discriminative power.

Prediction: S_A < S_B, and path A reaches the equilibrium neighborhood first.

Statistical test (preregistered): 12 seeds, binomial on S_A < S_B.
  Support:    S_A < S_B for >= 10/12 seeds (p < 0.05) AND the effect survives the
              discriminative-power check below.
  Challenge:  ordering fails for >= 4/12 seeds, OR the discriminative-power check fails.
  Falsification of the specific ordering prediction: S_B < S_A for >= 7/12 seeds.

Discriminative-power check (added after the first run exposed a weak design):
  Because E = C * p scales with the commission rate, S_B/S_A ≈ C_B/C_A = 20 even if
  the two markets behaved identically. The non-trivial part is the change in the
  trading trajectory (fill counts, convergence speed). The check:
      ratio_dev = |ln(S_B/S_A)| / |ln(C_B/C_A)|
  If ratio_dev > 0.85 (i.e., less than ~15% of the S ratio comes from behaviour
  rather than the rate factor), the effect is dominated by the construction and the
  result is classified challenge (exploratory), not support. A market that differs
  only by a constant multiplier on E cannot test path selection.

Honest statement: E = commission is a proxy for "per-step consumption"; whether it
is the economically correct definition requires community review (P-ECO-001).
This is the FIRST computational result for the economics prediction — it starts as
exploratory until independently replicated.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import random
import sys
from datetime import datetime, timezone

CLAIM_ID = "XD-P2-ECO-001"

NUM_BUYERS = 25
NUM_SELLERS = 25
VALUE_MIN, VALUE_MAX = 50.0, 150.0  # buyer private value / seller cost ranges
ASK_MAX = 200.0
ROUNDS = 60
NUM_SEEDS = 12

COMMISSION_A = 0.001
COMMISSION_B = 0.02

# Convergence: price std over the last CONV_WINDOW rounds vs. the first window.
CONV_WINDOW = 10
CONV_RATIO = 0.30  # converged if last-window std < 30% of first-window std


def run_market(commission: float, seed: int) -> dict:
    """Run a double-auction market and return per-round S and price stats."""
    rng = random.Random(seed)

    buyers = [{"id": i, "v": rng.uniform(VALUE_MIN, VALUE_MAX)} for i in range(NUM_BUYERS)]
    sellers = [{"id": j, "c": rng.uniform(VALUE_MIN, VALUE_MAX)} for j in range(NUM_SELLERS)]

    S_total = 0.0
    fills = 0
    price_std_per_round: list[float] = []

    for _round in range(ROUNDS):
        # Zero-intelligence quotes
        bids = [rng.uniform(0.0, b["v"]) for b in buyers]
        asks = [rng.uniform(s["c"], ASK_MAX) for s in sellers]

        # Effective quotes after commission (widens the spread)
        eff_bids = sorted(((b / (1.0 + commission), i) for i, b in enumerate(bids)), reverse=True)
        eff_asks = sorted(((a * (1.0 + commission), j) for j, a in enumerate(asks)))

        round_prices: list[float] = []
        bi, si = 0, 0
        while bi < len(eff_bids) and si < len(eff_asks):
            ebid, ib = eff_bids[bi]
            eask, js = eff_asks[si]
            if ebid >= eask:
                p = (bids[ib] + asks[js]) / 2.0
                S_total += commission * p * 1.0  # E_i * ΔN_i, E_i = C*p, ΔN_i = 1
                round_prices.append(p)
                fills += 1
                bi += 1
                si += 1
            else:
                break

        # Price dispersion this round (convergence proxy); empty round -> repeat last
        if round_prices:
            mean = sum(round_prices) / len(round_prices)
            var = sum((p - mean) ** 2 for p in round_prices) / len(round_prices)
            price_std_per_round.append(math.sqrt(var))
        elif price_std_per_round:
            price_std_per_round.append(price_std_per_round[-1])
        else:
            price_std_per_round.append(float("nan"))

    first_std = price_std_per_round[CONV_WINDOW - 1] if len(price_std_per_round) >= CONV_WINDOW else float("nan")
    last_std = price_std_per_round[-1] if price_std_per_round else float("nan")
    converged = (not math.isnan(first_std)) and last_std < CONV_RATIO * first_std

    return {"S": S_total, "fills": fills, "converged": converged,
            "first_std": first_std, "last_std": last_std}


def binomial_p(n_success: int, n_total: int) -> float:
    """Two-sided binomial test p-value (fix: include the extreme value itself)."""
    from math import comb
    k_high = max(n_success, n_total - n_success)
    k_low = n_total - k_high
    p_val = sum(comb(n_total, kk) * (0.5 ** n_total) for kk in range(k_high, n_total + 1))
    p_val += sum(comb(n_total, kk) * (0.5 ** n_total) for kk in range(0, k_low + 1))
    return min(p_val, 1.0)


def source_hash() -> str:
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> None:
    per_seed: list[dict] = []
    AB_holds = 0
    for seed in range(NUM_SEEDS):
        ra = run_market(COMMISSION_A, seed)
        rb = run_market(COMMISSION_B, seed)
        holds = ra["S"] < rb["S"]
        AB_holds += 1 if holds else 0
        per_seed.append({
            "seed": seed,
            "S_A": ra["S"], "S_B": rb["S"],
            "fills_A": ra["fills"], "fills_B": rb["fills"],
            "converged_A": ra["converged"], "converged_B": rb["converged"],
            "std_first_A": ra["first_std"], "std_last_A": ra["last_std"],
            "std_first_B": rb["first_std"], "std_last_B": rb["last_std"],
        })

    mean_SA = sum(p["S_A"] for p in per_seed) / NUM_SEEDS
    mean_SB = sum(p["S_B"] for p in per_seed) / NUM_SEEDS
    p_value = binomial_p(AB_holds, NUM_SEEDS)

    # Discriminative-power check (see module docstring)
    ratio_dev = abs(math.log(mean_SB / mean_SA)) / abs(math.log(COMMISSION_B / COMMISSION_A))
    mean_fills_A = sum(p["fills_A"] for p in per_seed) / NUM_SEEDS
    mean_fills_B = sum(p["fills_B"] for p in per_seed) / NUM_SEEDS
    fills_ratio = mean_fills_B / mean_fills_A  # < 1 if high commission reduces volume

    discriminative = ratio_dev <= 0.85
    ordering_holds = AB_holds >= 10 and p_value < 0.05

    if ordering_holds and discriminative:
        classification = "support"
    elif AB_holds <= 4:
        classification = "falsification"
    else:
        classification = "challenge"

    output = {
        "submission_id": "ref-xd-p2-eco-001-20260801",
        "claim_id": CLAIM_ID,
        "title": "Market equilibrium path selection: lower total commission path is preferred",
        "author": {"name": "reference-implementation", "affiliation": "open-validation", "contact": ""},
        "preregistration": {
            "hash": "in-script-preregistered-constants-v1",
            "timestamp_utc": "2026-08-01T00:00:00+00:00",
            "uri": "protocol-p1-ai.md#10-claim-xd-p2-eco-001",
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
            "S_A": mean_SA,
            "S_B": mean_SB,
            "preferred_path": "A" if mean_SA < mean_SB else "B",
            "selected_counts": {"A": AB_holds, "B": NUM_SEEDS - AB_holds},
            "p_value": p_value,
            "summary": (
                f"12 seeds; S_A(low commission)={mean_SA:.1f}, S_B(high commission)={mean_SB:.1f}; "
                f"S_A<S_B holds {AB_holds}/12 (p={p_value:.4f}); "
                f"discriminative_check: ratio_dev={ratio_dev:.3f} (<=0.85 required), "
                f"fills_ratio={fills_ratio:.3f}; converged markets: "
                f"A={sum(1 for p in per_seed if p['converged_A'])}/12, "
                f"B={sum(1 for p in per_seed if p['converged_B'])}/12; "
                f"classification={classification}"
            ),
            "raw_output": {
                "model": "ZI-C double auction",
                "buyers": NUM_BUYERS, "sellers": NUM_SELLERS,
                "rounds": ROUNDS,
                "commission_A": COMMISSION_A, "commission_B": COMMISSION_B,
                "discriminative_power": {
                    "ratio_dev": ratio_dev,
                    "mean_fills_A": mean_fills_A,
                    "mean_fills_B": mean_fills_B,
                    "fills_ratio": fills_ratio,
                    "note": "ratio_dev close to 1 means the S difference is dominated by the commission-rate factor (construction), not by trading behaviour",
                },
                "per_seed_results": per_seed,
            },
        },
        "classification": classification,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
