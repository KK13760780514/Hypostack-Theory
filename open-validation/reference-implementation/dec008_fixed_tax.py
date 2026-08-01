#!/usr/bin/env python3
"""XD-P2-ECO-001 V3 development run -- DEC-008 option B (fixed per-trade tax).

Background (ISSUE-008 / DEC-008): V1 (proportional commission) produced
S_A < S_B in 12/12 seeds but the S difference was ~97% explained by the
commission-ratio factor (ratio_dev=0.970 > 0.85) -- a constructive artifact,
not market behavior. V2 (learning traders, option A) fixed convergence but the
speed sub-prediction was not supported (5/12, p=0.774) and the S secondary
criterion was still commission-ratio dominated (ratio_dev=0.981).

This V3 development run implements DEC-008 option B: E = FIXED per-trade tax
(not proportional to price). Then S = TAX * number of fills, so S_A/S_B reflects
BEHAVIORAL fill differences directly; the constructive price-ratio factor is
gone by construction.

Scientific-integrity guard (same as V2): the Roth-Erev learning rule reinforces
the chosen price action with the realized profit only -- no reference to S, the
tax, or any "prefer the frugal path" term. Faster convergence on the low-tax
path must EMERGE from the market mechanism (tax widens the effective spread ->
fewer/slower matches), not from the trader model.

Treatments:
  Path A: TAX_A = 0.1  (low fixed tax per trade)
  Path B: TAX_B = 2.0  (high fixed tax per trade; 20x, same ratio as V1 commission)

Preregistered metrics (V3, per DEC-008 option B):
  Primary : convergence_round -- first round t>=10 where the trailing-10-round
            mean transaction price has std <= PRICE_BAND with >= MIN_FILLS fills.
            speed_A < speed_B means the low-consumption path equilibrates first.
  Secondary: S = sum(TAX * 1) over fills (behavioral efficiency contrast);
            ratio_dev = |ln(S_B/S_A)| / |ln(TAX_B/TAX_A)| (<=0.85 desired);
            fills, price deviation from E_EQ=100.

Classification (statistical outcome; ledger row exploratory per ISSUE-006):
  Support   : speed_A < speed_B in >= 10/12 seeds (two-sided binomial p<0.05)
              AND activity guard (mean fills_B >= 0.25 * mean fills_A)
              AND robustness (direction holds in >= 4/6 (lambda, phi) combos).
  Falsification: speed_A < speed_B in <= 4/12 seeds.
  Challenge : otherwise.

Honest statement: proposer-run development result for DEC-008 (issue #1). It
enters the ledger as exploratory per ISSUE-006 and is subject to the 14-day
cooldown and committee review. It neither confirms nor refutes the economics
prediction by itself.
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
VERSION = "v3-fixed-tax"

NUM_BUYERS = 25
NUM_SELLERS = 25
VALUE_MIN, VALUE_MAX = 50.0, 150.0
ROUNDS = 80
NUM_SEEDS = 12

TAX_A = 0.1
TAX_B = 2.0
EQ_PRICE = 100.0

CONV_WINDOW = 10
PRICE_BAND = 1.0
MIN_FILLS = 3

GRID = list(range(50, 151))
LAMBDA_REF = 1.0
PHI_REF = 0.05
ROBUSTNESS_COMBOS = [(1.0, 0.00), (1.0, 0.05), (1.0, 0.10), (2.0, 0.00), (2.0, 0.05), (2.0, 0.10)]


def _choose(rng: random.Random, q: list[float], lam: float) -> int:
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
    for i in range(len(q)):
        q[i] *= (1.0 - phi)
    q[idx] += payoff
    if q[idx] < 0.0:
        q[idx] = 0.0


def run_market(tax: float, seed: int, lam: float = LAMBDA_REF, phi: float = PHI_REF) -> dict:
    """Run one learning double-auction market under a fixed per-trade tax."""
    rng = random.Random(seed)
    S_total = 0.0
    fills = 0
    fills_per_round: list[int] = []
    price_series: list[float] = []
    all_prices: list[float] = []

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

        # Fixed tax: buyer net cost = price + tax, seller net revenue = price - tax.
        # Effective prices used for matching: bid - tax, ask + tax.
        eff_bids = sorted(((bids[i] - tax, i) for i in range(NUM_BUYERS)), reverse=True)
        eff_asks = sorted(((asks[j] + tax, j) for j in range(NUM_SELLERS)))

        matches: list[tuple[int, int, float]] = []
        bi = si = 0
        while bi < NUM_BUYERS and si < NUM_SELLERS:
            ebid, i = eff_bids[bi]
            eask, j = eff_asks[si]
            if ebid >= eask:
                p = (bids[i] + asks[j]) / 2.0
                S_total += tax  # E = fixed tax, delta_N = 1
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

        for i, j, p in matches:
            b_payoff = buyers[i]["v"] - (p + tax)
            s_payoff = (p - tax) - sellers[j]["c"]
            _reinforce(buyers[i]["q"], bid_choices[i], b_payoff, phi)
            _reinforce(sellers[j]["q"], ask_choices[j], s_payoff, phi)

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
        ra = run_market(TAX_A, seed, lam, phi)
        rb = run_market(TAX_B, seed, lam, phi)
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
    ratio_dev = abs(math.log(mean_SB / mean_SA)) / abs(math.log(TAX_B / TAX_A)) if mean_SA > 0 else float("nan")
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
    ref = summarize(LAMBDA_REF, PHI_REF)
    scan = [summarize(lam, phi) for lam, phi in ROBUSTNESS_COMBOS]

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
        "purpose": "XD-P2-ECO-001 V3 (DEC-008 option B): fixed per-trade tax removes the price-ratio artifact",
        "config": {
            "claim_id": CLAIM_ID, "version": VERSION,
            "buyers": NUM_BUYERS, "sellers": NUM_SELLERS,
            "value_cost_range": [VALUE_MIN, VALUE_MAX], "rounds": ROUNDS,
            "tax_A": TAX_A, "tax_B": TAX_B,
            "convergence": {"window": CONV_WINDOW, "price_band": PRICE_BAND, "min_fills": MIN_FILLS},
            "learning": {"lambda_ref": LAMBDA_REF, "phi_ref": PHI_REF,
                         "robustness_combos": [[l, p] for l, p in ROBUSTNESS_COMBOS],
                         "note": "choice P(a)~q(a)^lambda; q<-(1-phi)q then q[chosen]+=realized_profit; no S/tax term"},
        },
        "learning_reference": ref,
        "robustness_scan": [{k: v for k, v in s.items() if k != "per_seed"} for s in scan],
        "classification": classification,
        "summary": (
            f"fixed-tax (lambda={LAMBDA_REF}, phi={PHI_REF}): speed_A<speed_B in {speed_holds}/12 (p={p_value:.4f}); "
            f"mean conv_A={ref['mean_conv_A']:.1f} vs conv_B={ref['mean_conv_B']:.1f}; "
            f"activity guard: fills_B={ref['mean_fills_B']:.1f} vs fills_A={ref['mean_fills_A']:.1f} "
            f"(ratio {ref['mean_fills_B'] / max(ref['mean_fills_A'], 1e-9):.2f}, {'OK' if activity_guard else 'FAIL'}); "
            f"robustness: direction holds in {robust_dir}/6 combos; "
            f"S contrast: S_A={ref['mean_SA']:.1f}, S_B={ref['mean_SB']:.1f}, "
            f"ratio_dev={ref['ratio_dev']:.3f} (V1 was 0.970, V2 was 0.981); "
            f"statistical outcome={classification}"
        ),
        "honest_statement": (
            "Proposer-run development result for DEC-008 (issue #1). Per ISSUE-006, this "
            "new-caliber result enters the ledger as exploratory and is subject to the "
            "14-day cooldown and committee review. It neither confirms nor refutes the "
            "economics prediction by itself."
        ),
        "classification_ledger": "exploratory",
        "code_hash": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
        "environment": {
            "os": platform.platform(),
            "python_version": sys.version.split()[0],
            "dependencies": "python-stdlib-only",
        },
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
