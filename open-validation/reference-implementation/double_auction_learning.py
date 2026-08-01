#!/usr/bin/env python3
"""Reference implementation for XD-P2-ECO-001 V2 -- DEC-008 option A (learning traders).

Addresses ISSUE-008 (first run: S ratio dominated by the commission-rate factor,
ratio_dev=0.970>0.85, and the ZI-C market barely converges so the "converges faster"
sub-prediction was untestable). DEC-008 recommends learning traders (EWA/Roth-Erev)
so the market genuinely converges; the PRIMARY criterion becomes convergence speed.

Scientific-integrity guard (anti "caliber shopping"):
  The learning rule reinforces the CHOSEN price action with the REALIZED profit only.
  It contains no reference to S, the commission rate, or any "prefer the frugal
  path" term. Any faster convergence on the low-commission path must EMERGE from the
  market mechanism (commission widens the effective bid/ask spread -> fewer and slower
  matches), not from the trader model. Hyper-parameters (lambda, phi) are fixed before
  the run; a small robustness scan over them is reported so the result cannot be tuned.

Modes:
  static   -- ZI-C quotes (control; reproduces the EV-22c7db69115c4ffc setup)
  learning -- Roth-Erev with exponential forgetting over the integer price grid 50..150

Treatments:
  Path A: C_A = 0.001 (low commission), Path B: C_B = 0.02 (high commission)

Preregistered metrics (V2, per DEC-008):
  Primary : convergence_round -- first round t >= 10 where the trailing-10-round mean
            transaction price has std <= PRICE_BAND (1.0) with >= MIN_FILLS (3) fills.
            If never reached -> ROUNDS. speed_A < speed_B means the low-consumption
            path reaches the equilibrium neighborhood first.
  Secondary (V1-caliber contrast, ISSUE-006 rule 3):
            S = sum(E_i * delta_N_i), E_i = C * p_i, delta_N_i = 1 per fill
            ratio_dev = |ln(S_B/S_A)| / |ln(C_B/C_A)|  (discriminative check, <=0.85)
            fills, price deviation from E_EQ=100.

Classification (new-caliber statistical outcome; ledger row is exploratory per ISSUE-006):
  Support   : speed_A < speed_B in >= 10/12 seeds (two-sided binomial p<0.05)
              AND activity guard: mean fills_B >= 0.25 * mean fills_A (B not dead)
              AND robustness: direction (mean conv_A < mean conv_B) holds in >= 4/6
              of the (lambda, phi) scan combos.
  Falsification: speed_A < speed_B in <= 4/12 seeds.
  Challenge : otherwise (including when B's market is too inactive to compare).

Honest statement: this is a proposer-run development result for DEC-008 (issue #1,
"paused until consensus"). Per ISSUE-006 it enters the ledger as exploratory and is
subject to the 14-day cooldown / committee review. It neither confirms nor refutes
the economics prediction by itself.
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
VERSION = "v2-learning"

NUM_BUYERS = 25
NUM_SELLERS = 25
VALUE_MIN, VALUE_MAX = 50.0, 150.0
ASK_MAX = 200.0  # static-mode ask upper bound (matches V1)
ROUNDS = 80
NUM_SEEDS = 12

COMMISSION_A = 0.001
COMMISSION_B = 0.02
EQ_PRICE = 100.0  # theoretical equilibrium of the symmetric value/cost distribution

# Convergence definition (V2): trailing-10-round mean-price std <= PRICE_BAND,
# with at least MIN_FILLS fills in the window (guards against spurious flat series).
CONV_WINDOW = 10
PRICE_BAND = 1.0
MIN_FILLS = 3

# Learning hyper-parameters (fixed before the run).
GRID = list(range(50, 151))  # integer price action grid
LAMBDA_REF = 1.0   # choice exponent (higher = more exploitative)
PHI_REF = 0.05     # per-round forgetting of propensities
ROBUSTNESS_COMBOS = [(1.0, 0.00), (1.0, 0.05), (1.0, 0.10), (2.0, 0.00), (2.0, 0.05), (2.0, 0.10)]


def _choose(rng: random.Random, q: list[float], lam: float) -> int:
    """Logit-style choice: P(action) ∝ q^lambda. Returns an action index."""
    w = [qi ** lam for qi in q]
    tot = sum(w)
    if tot <= 0.0:
        return rng.randrange(len(q))
    r = rng.random() * tot
    acc = 0.0
    for i, wi in enumerate(w):
        acc += wi
        if r <= acc:
            return i
    return len(q) - 1


def _reinforce(q: list[float], idx: int, payoff: float, phi: float) -> None:
    """Roth-Erev with exponential forgetting; propensities floored at 0."""
    for i in range(len(q)):
        q[i] *= (1.0 - phi)
    q[idx] += payoff
    if q[idx] < 0.0:
        q[idx] = 0.0


def run_market(commission: float, seed: int, mode: str,
               lam: float = LAMBDA_REF, phi: float = PHI_REF) -> dict:
    """Run one double-auction market; return S, fills, price stats, convergence round."""
    rng = random.Random(seed)
    S_total = 0.0
    fills = 0
    fills_per_round: list[int] = []
    price_series: list[float] = []  # mean transaction price per round (carry forward)
    all_prices: list[float] = []

    if mode == "static":
        buyers = [{"v": rng.uniform(VALUE_MIN, VALUE_MAX)} for _ in range(NUM_BUYERS)]
        sellers = [{"c": rng.uniform(VALUE_MIN, VALUE_MAX)} for _ in range(NUM_SELLERS)]
    else:
        buyers = []
        for _ in range(NUM_BUYERS):
            v = rng.uniform(VALUE_MIN, VALUE_MAX)
            acts = [p for p in GRID if p <= v]
            buyers.append({"v": v, "acts": acts, "q": [1.0] * len(acts)})
        sellers = []
        for _ in range(NUM_SELLERS):
            c = rng.uniform(VALUE_MIN, VALUE_MAX)
            acts = [p for p in GRID if p >= c]
            sellers.append({"c": c, "acts": acts, "q": [1.0] * len(acts)})

    for _round in range(ROUNDS):
        if mode == "static":
            bids = [rng.uniform(0.0, b["v"]) for b in buyers]
            asks = [rng.uniform(s["c"], ASK_MAX) for s in sellers]
            bid_choices = ask_choices = None
        else:
            bids, bid_choices = [], []
            for b in buyers:
                idx = _choose(rng, b["q"], lam)
                bids.append(b["acts"][idx])
                bid_choices.append(idx)
            asks, ask_choices = [], []
            for s in sellers:
                idx = _choose(rng, s["q"], lam)
                asks.append(s["acts"][idx])
                ask_choices.append(idx)

        eff_bids = sorted(((bids[i] / (1.0 + commission), i) for i in range(NUM_BUYERS)), reverse=True)
        eff_asks = sorted(((asks[j] * (1.0 + commission), j) for j in range(NUM_SELLERS)))

        matches: list[tuple[int, int, float]] = []  # (buyer_idx, seller_idx, trade_price)
        bi = si = 0
        while bi < NUM_BUYERS and si < NUM_SELLERS:
            ebid, i = eff_bids[bi]
            eask, j = eff_asks[si]
            if ebid >= eask:
                p = (bids[i] + asks[j]) / 2.0
                S_total += commission * p * 1.0
                all_prices.append(p)
                matches.append((i, j, p))
                fills += 1
                bi += 1
                si += 1
            else:
                break

        fills_per_round.append(len(matches))
        if matches:
            price_series.append(sum(p for _, _, p in matches) / len(matches))
        elif price_series:
            price_series.append(price_series[-1])
        else:
            price_series.append(float("nan"))

        if mode == "learning":
            for i, j, p in matches:
                b_payoff = buyers[i]["v"] - p * (1.0 + commission)
                s_payoff = p * (1.0 - commission) - sellers[j]["c"]
                _reinforce(buyers[i]["q"], bid_choices[i], b_payoff, phi)
                _reinforce(sellers[j]["q"], ask_choices[j], s_payoff, phi)

    # Primary metric: convergence round (first stable 10-round price window).
    conv_round = ROUNDS
    for t in range(CONV_WINDOW - 1, ROUNDS):
        window = price_series[t - CONV_WINDOW + 1: t + 1]
        if any(isinstance(x, float) and math.isnan(x) for x in window):
            continue
        if sum(fills_per_round[t - CONV_WINDOW + 1: t + 1]) < MIN_FILLS:
            continue
        m = sum(window) / len(window)
        var = sum((x - m) ** 2 for x in window) / len(window)
        if math.sqrt(var) <= PRICE_BAND:
            conv_round = t + 1
            break

    price_dev = (sum(abs(p - EQ_PRICE) for p in all_prices) / len(all_prices)) if all_prices else float("nan")

    return {"S": S_total, "fills": fills, "convergence_round": conv_round,
            "price_dev": price_dev, "fills_per_round": fills_per_round}


def binomial_p(n_success: int, n_total: int) -> float:
    from math import comb
    k_high = max(n_success, n_total - n_success)
    k_low = n_total - k_high
    p_val = sum(comb(n_total, kk) * (0.5 ** n_total) for kk in range(k_high, n_total + 1))
    p_val += sum(comb(n_total, kk) * (0.5 ** n_total) for kk in range(0, k_low + 1))
    return min(p_val, 1.0)


def summarize(lam: float, phi: float) -> dict:
    per_seed = []
    speed_holds = 0
    for seed in range(NUM_SEEDS):
        ra = run_market(COMMISSION_A, seed, "learning", lam, phi)
        rb = run_market(COMMISSION_B, seed, "learning", lam, phi)
        speed_holds += 1 if ra["convergence_round"] < rb["convergence_round"] else 0
        per_seed.append({
            "seed": seed,
            "conv_A": ra["convergence_round"], "conv_B": rb["convergence_round"],
            "S_A": ra["S"], "S_B": rb["S"],
            "fills_A": ra["fills"], "fills_B": rb["fills"],
            "price_dev_A": ra["price_dev"], "price_dev_B": rb["price_dev"],
        })
    mean_conv_A = sum(p["conv_A"] for p in per_seed) / NUM_SEEDS
    mean_conv_B = sum(p["conv_B"] for p in per_seed) / NUM_SEEDS
    mean_SA = sum(p["S_A"] for p in per_seed) / NUM_SEEDS
    mean_SB = sum(p["S_B"] for p in per_seed) / NUM_SEEDS
    mean_fills_A = sum(p["fills_A"] for p in per_seed) / NUM_SEEDS
    mean_fills_B = sum(p["fills_B"] for p in per_seed) / NUM_SEEDS
    mean_dev_A = sum(p["price_dev_A"] for p in per_seed) / NUM_SEEDS
    mean_dev_B = sum(p["price_dev_B"] for p in per_seed) / NUM_SEEDS
    p_value = binomial_p(speed_holds, NUM_SEEDS)
    ratio_dev = abs(math.log(mean_SB / mean_SA)) / abs(math.log(COMMISSION_B / COMMISSION_A)) if mean_SA > 0 else float("nan")
    return {
        "lambda": lam, "phi": phi,
        "speed_holds": speed_holds, "p_value": p_value,
        "mean_conv_A": mean_conv_A, "mean_conv_B": mean_conv_B,
        "mean_SA": mean_SA, "mean_SB": mean_SB, "ratio_dev": ratio_dev,
        "mean_fills_A": mean_fills_A, "mean_fills_B": mean_fills_B,
        "mean_price_dev_A": mean_dev_A, "mean_price_dev_B": mean_dev_B,
        "per_seed": per_seed,
    }


def main() -> None:
    # Static control (baseline; expected: rarely/never converge under the V2 metric).
    static_A = [run_market(COMMISSION_A, s, "static") for s in range(NUM_SEEDS)]
    static_B = [run_market(COMMISSION_B, s, "static") for s in range(NUM_SEEDS)]
    static = {
        "converged_A": sum(1 for r in static_A if r["convergence_round"] < ROUNDS),
        "converged_B": sum(1 for r in static_B if r["convergence_round"] < ROUNDS),
        "mean_conv_A": sum(r["convergence_round"] for r in static_A) / NUM_SEEDS,
        "mean_conv_B": sum(r["convergence_round"] for r in static_B) / NUM_SEEDS,
        "mean_fills_A": sum(r["fills"] for r in static_A) / NUM_SEEDS,
        "mean_fills_B": sum(r["fills"] for r in static_B) / NUM_SEEDS,
    }

    ref = summarize(LAMBDA_REF, PHI_REF)
    scan = [summarize(lam, phi) for lam, phi in ROBUSTNESS_COMBOS]

    # Classification (statistical outcome only; ledger row is exploratory per ISSUE-006).
    speed_holds = ref["speed_holds"]
    p_value = ref["p_value"]
    activity_guard = ref["mean_fills_B"] >= 0.25 * ref["mean_fills_A"]
    robust_dir = sum(1 for s in scan if s["mean_conv_A"] < s["mean_conv_B"])
    ordering_holds = speed_holds >= 10 and p_value < 0.05
    if ordering_holds and activity_guard and robust_dir >= 4:
        classification = "support"
    elif speed_holds <= 4:
        classification = "falsification"
    else:
        classification = "challenge"

    output = {
        "purpose": "XD-P2-ECO-001 V2 (DEC-008 option A): learning traders make convergence testable",
        "config": {
            "claim_id": CLAIM_ID, "version": VERSION,
            "buyers": NUM_BUYERS, "sellers": NUM_SELLERS,
            "value_cost_range": [VALUE_MIN, VALUE_MAX], "rounds": ROUNDS,
            "commission_A": COMMISSION_A, "commission_B": COMMISSION_B,
            "convergence": {"window": CONV_WINDOW, "price_band": PRICE_BAND, "min_fills": MIN_FILLS},
            "learning": {"lambda_ref": LAMBDA_REF, "phi_ref": PHI_REF,
                         "robustness_combos": [[l, p] for l, p in ROBUSTNESS_COMBOS],
                         "note": "choice P(a)∝q(a)^lambda; q←(1-phi)q then q[chosen]+=realized_profit; no S/commission term"},
        },
        "static_baseline_control": static,
        "learning_reference": ref,
        "robustness_scan": [{k: v for k, v in s.items() if k != "per_seed"} for s in scan],
        "classification": classification,
        "summary": (
            f"learning (λ={LAMBDA_REF}, φ={PHI_REF}): speed_A<speed_B in {speed_holds}/12 (p={p_value:.4f}); "
            f"mean conv_A={ref['mean_conv_A']:.1f} vs conv_B={ref['mean_conv_B']:.1f}; "
            f"activity guard: fills_B={ref['mean_fills_B']:.1f} vs fills_A={ref['mean_fills_A']:.1f} "
            f"(ratio {ref['mean_fills_B'] / max(ref['mean_fills_A'], 1e-9):.2f}, {'OK' if activity_guard else 'FAIL'}); "
            f"robustness: direction holds in {robust_dir}/6 combos; "
            f"V1-caliber contrast: S_A={ref['mean_SA']:.1f}, S_B={ref['mean_SB']:.1f}, "
            f"ratio_dev={ref['ratio_dev']:.3f} (V1 was 13.4 / 245.8 / 0.970); "
            f"static control converged A={static['converged_A']}/12, B={static['converged_B']}/12; "
            f"statistical outcome={classification}"
        ),
        "honest_statement": (
            "Proposer-run development result for DEC-008 (issue #1). Per ISSUE-006, this "
            "new-caliber result enters the ledger as exploratory and is subject to the "
            "14-day cooldown and committee review. It neither confirms nor refutes the "
            "economics prediction by itself."
        ),
        "classification_ledger": "exploratory",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
