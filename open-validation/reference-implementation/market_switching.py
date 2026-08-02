#!/usr/bin/env python3
"""P-ECO-002: Market "auto-switching" experiment (choice/switching test).

This is a STRONGER test than the ordering tests (P-ECO-001 V1-V3). Instead of
comparing S values of two imposed paths, it directly tests the theory's
"selection/switching" assertion: when path costs change mid-course, does the
market automatically shift to the lower-cost path?

Design (per predictions-operationalization.md P-ECO-002):
  - Two parallel ZI-C double auction markets (A and B)
  - Each round, each trader chooses ONE market (Roth-Erev 2-armed bandit
    over market choice; learning rule contains NO S/tax preference term)
  - Fixed tax per trade (TAX_LOW=0.1, TAX_HIGH=2.0; 20x gap, same as V3)
  - Phase 1 (rounds 1-40):  market A = TAX_LOW, market B = TAX_HIGH
  - Phase 2 (rounds 41-80): taxes SWAP -- A = TAX_HIGH, B = TAX_LOW
  - Metric: p_low = trades in low-tax market / total trades
    (phase 1: low-tax = A; phase 2: low-tax = B)
  - Prediction: p_low(phase2 last 10) > p_low(phase1 last 10) + 0.15

Integrity guard:
  The Roth-Erev learning reinforces market choice with REALIZED PROFIT only.
  It contains no S, tax, or "frugal path" term. Any switching must EMERGE
  from profit-seeking behavior (lower tax -> higher profit -> more likely
  to choose that market), not from explicit cost minimization.

Classification:
  Support:        p_low shift >= 0.15 in >= 10/12 seeds (p < 0.05)
  Falsification:  p_low shift >= 0.15 in <= 4/12 seeds
  Challenge:      otherwise
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import random
import sys
from datetime import datetime, timezone

NUM_BUYERS = 25
NUM_SELLERS = 25
VALUE_MIN, VALUE_MAX = 50.0, 150.0
ASK_MAX = 200.0
ROUNDS = 80
PHASE_SWITCH = 40  # round at which taxes swap
NUM_SEEDS = 12

TAX_LOW = 0.1
TAX_HIGH = 2.0

# Roth-Erev parameters (same as double_auction_learning.py)
LAMBDA_REF = 1.0
PHI_REF = 0.05
SHIFT_THRESHOLD = 0.15  # p_low must increase by at least this


def run_switching_experiment(seed: int, lam: float = LAMBDA_REF,
                              phi: float = PHI_REF) -> dict:
    """Run one seed of the two-market switching experiment."""
    rng = random.Random(seed)

    # Initialize traders with private values/costs
    buyers = [{"v": rng.uniform(VALUE_MIN, VALUE_MAX)} for _ in range(NUM_BUYERS)]
    sellers = [{"c": rng.uniform(VALUE_MIN, VALUE_MAX)} for _ in range(NUM_SELLERS)]

    # Each trader has Roth-Erev propensities for 2 markets: q[0]=market A, q[1]=market B
    buyer_q = [[1.0, 1.0] for _ in range(NUM_BUYERS)]
    seller_q = [[1.0, 1.0] for _ in range(NUM_SELLERS)]

    fills_A_per_round = []
    fills_B_per_round = []

    for round_idx in range(ROUNDS):
        # Determine tax for each market in this round
        if round_idx < PHASE_SWITCH:
            tax_A, tax_B = TAX_LOW, TAX_HIGH
        else:
            tax_A, tax_B = TAX_HIGH, TAX_LOW

        # Traders choose market (Roth-Erev 2-armed bandit)
        buyer_market = []
        for i in range(NUM_BUYERS):
            w = [q ** lam for q in buyer_q[i]]
            tot = sum(w)
            buyer_market.append(0 if rng.random() * tot <= w[0] else 1)

        seller_market = []
        for j in range(NUM_SELLERS):
            w = [q ** lam for q in seller_q[j]]
            tot = sum(w)
            seller_market.append(0 if rng.random() * tot <= w[0] else 1)

        # ZI-C pricing within each market
        # Market A
        a_buyers = [i for i in range(NUM_BUYERS) if buyer_market[i] == 0]
        a_sellers = [j for j in range(NUM_SELLERS) if seller_market[j] == 0]
        b_buyers = [i for i in range(NUM_BUYERS) if buyer_market[i] == 1]
        b_sellers = [j for j in range(NUM_SELLERS) if seller_market[j] == 1]

        def run_one_market(b_idx_list, s_idx_list, tax):
            """ZI-C matching in one market. Returns (fills, matches_with_profit)."""
            if not b_idx_list or not s_idx_list:
                return 0, []
            bids = [(rng.uniform(0.0, buyers[i]["v"]), i) for i in b_idx_list]
            asks = [(rng.uniform(sellers[j]["c"], ASK_MAX), j) for j in s_idx_list]
            # Effective prices: bid - tax (buyer side), ask + tax (seller side)
            eff_bids = sorted(((b - tax, i) for b, i in bids), reverse=True)
            eff_asks = sorted(((a + tax, j) for a, j in asks))
            matches = []
            bi = si = 0
            while bi < len(eff_bids) and si < len(eff_asks):
                ebid, i = eff_bids[bi]
                eask, j = eff_asks[si]
                if ebid >= eask:
                    p = (bids[bi][0] + asks[si][0]) / 2.0  # raw mid-price
                    b_payoff = buyers[i]["v"] - p - tax
                    s_payoff = p - tax - sellers[j]["c"]
                    matches.append((i, j, p, b_payoff, s_payoff))
                    bi += 1; si += 1
                else:
                    break
            return len(matches), matches

        fills_A, matches_A = run_one_market(a_buyers, a_sellers, tax_A)
        fills_B, matches_B = run_one_market(b_buyers, b_sellers, tax_B)
        fills_A_per_round.append(fills_A)
        fills_B_per_round.append(fills_B)

        # Reinforce market choice with realized profit (Roth-Erev with forgetting)
        for i, j, p, b_payoff, s_payoff in matches_A:
            for q_list, idx, payoff in [(buyer_q, i, b_payoff), (seller_q, j, s_payoff)]:
                q_list[idx][0] *= (1.0 - phi)
                q_list[idx][1] *= (1.0 - phi)
                q_list[idx][0] += max(payoff, 0.0)
        for i, j, p, b_payoff, s_payoff in matches_B:
            for q_list, idx, payoff in [(buyer_q, i, b_payoff), (seller_q, j, s_payoff)]:
                q_list[idx][0] *= (1.0 - phi)
                q_list[idx][1] *= (1.0 - phi)
                q_list[idx][1] += max(payoff, 0.0)

    # Compute p_low for last 10 rounds of each phase
    phase1_fills_A = fills_A_per_round[PHASE_SWITCH - 10: PHASE_SWITCH]
    phase1_fills_B = fills_B_per_round[PHASE_SWITCH - 10: PHASE_SWITCH]
    phase2_fills_A = fills_A_per_round[ROUNDS - 10: ROUNDS]
    phase2_fills_B = fills_B_per_round[ROUNDS - 10: ROUNDS]

    p1_total = sum(phase1_fills_A) + sum(phase1_fills_B)
    p2_total = sum(phase2_fills_A) + sum(phase2_fills_B)

    # Phase 1: low-tax = market A; Phase 2: low-tax = market B
    p_low_phase1 = sum(phase1_fills_A) / max(p1_total, 1)
    p_low_phase2 = sum(phase2_fills_B) / max(p2_total, 1)
    shift = p_low_phase2 - p_low_phase1

    return {
        "seed": seed,
        "p_low_phase1": round(p_low_phase1, 4),
        "p_low_phase2": round(p_low_phase2, 4),
        "shift": round(shift, 4),
        "shift_holds": shift >= SHIFT_THRESHOLD,
        "phase1_fills_A": sum(phase1_fills_A),
        "phase1_fills_B": sum(phase1_fills_B),
        "phase2_fills_A": sum(phase2_fills_A),
        "phase2_fills_B": sum(phase2_fills_B),
    }


def binomial_p(k: int, n: int) -> float:
    k_high = max(k, n - k)
    k_low = n - k_high
    p = sum(math.comb(n, x) * 0.5**n for x in range(k_high, n + 1))
    p += sum(math.comb(n, x) * 0.5**n for x in range(0, k_low + 1))
    return min(p, 1.0)


def source_hash() -> str:
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> None:
    per_seed = [run_switching_experiment(s) for s in range(NUM_SEEDS)]
    shifts_holds = sum(1 for r in per_seed if r["shift_holds"])
    p_value = binomial_p(shifts_holds, NUM_SEEDS)

    mean_p1 = sum(r["p_low_phase1"] for r in per_seed) / NUM_SEEDS
    mean_p2 = sum(r["p_low_phase2"] for r in per_seed) / NUM_SEEDS
    mean_shift = sum(r["shift"] for r in per_seed) / NUM_SEEDS

    if shifts_holds >= 10 and p_value < 0.05:
        classification = "support"
    elif shifts_holds <= 4:
        classification = "falsification"
    else:
        classification = "challenge"

    output = {
        "purpose": "P-ECO-002: Market auto-switching (choice/switching test) for XD-P2-ECO-001",
        "config": {
            "markets": 2,
            "buyers": NUM_BUYERS, "sellers": NUM_SELLERS,
            "value_cost_range": [VALUE_MIN, VALUE_MAX],
            "rounds": ROUNDS, "phase_switch": PHASE_SWITCH,
            "tax_low": TAX_LOW, "tax_high": TAX_HIGH,
            "learning": {"lambda": LAMBDA_REF, "phi": PHI_REF,
                         "rule": "Roth-Erev 2-armed bandit over market choice; "
                                 "reinforce with realized profit; NO S/tax term"},
            "shift_threshold": SHIFT_THRESHOLD,
            "seeds": NUM_SEEDS,
        },
        "results": {
            "shifts_holds": shifts_holds,
            "n_seeds": NUM_SEEDS,
            "p_value": p_value,
            "mean_p_low_phase1": round(mean_p1, 4),
            "mean_p_low_phase2": round(mean_p2, 4),
            "mean_shift": round(mean_shift, 4),
            "classification": classification,
        },
        "per_seed": per_seed,
        "summary": (
            f"Switching: p_low shift >= {SHIFT_THRESHOLD} in {shifts_holds}/{NUM_SEEDS} seeds "
            f"(p={p_value:.4f}); mean p_low: phase1={mean_p1:.3f} -> phase2={mean_p2:.3f} "
            f"(shift={mean_shift:+.3f}); classification={classification}"
        ),
        "honest_statement": (
            "This is a proposer-run development result for P-ECO-002 (switching test). "
            "Per ISSUE-006, it enters the ledger as exploratory. The learning rule "
            "contains no S/tax preference term; any switching must emerge from "
            "profit-seeking behavior."
        ),
        "code_hash": source_hash(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
