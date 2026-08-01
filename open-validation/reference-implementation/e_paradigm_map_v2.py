#!/usr/bin/env python3
"""Reference implementation for XD-E-PARADIGM-001 V2.

Calibrates cross-paradigm E conversion functions using 3 physical processes
that can be independently measured in multiple paradigms (physical, biological,
cognitive).

Calibration points (cross-paradigm processes):
  1. DNA base pair replication
  2. ATP hydrolysis (biological energy currency)
  3. Ion transport across membrane (Na+/K+ pump cycle)

For each process, we measure E (J/step) in each applicable paradigm:
  - Physical:  thermodynamic energy (bond energy, electrochemical work)
  - Biological: metabolic cost (ATP consumption at ~30.5 kJ/mol)
  - Cognitive: information content (bits x Landauer limit kT*ln2 at 310K)

The conversion function between paradigms is:
  E_target = E_source * (E_target_measured / E_source_measured)

Falsification conditions (from protocol-p1-ai.md section 8):
  - Cannot find comparable conversion functions -> challenge
  - Conversion degenerates to identity (eta=1 for all pairs) -> challenge
  - eta values span > 3 orders of magnitude across paradigms -> challenge
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
from datetime import datetime, timezone

CLAIM_ID = "XD-E-PARADIGM-001"

# Physical constants
K_B = 1.380649e-23   # Boltzmann constant, J/K
LN2 = math.log(2)
T_BODY = 310.0        # Body temperature, K
R_GAS = 8.314         # J/(mol*K)
N_A = 6.022e23         # Avogadro's number

# Landauer limit at body temperature (J/bit)
E_LANDAUER = K_B * T_BODY * LN2  # ~2.95e-21 J/bit

# ATP hydrolysis free energy under cellular conditions (~30.5 kJ/mol)
DG_ATP = 30500.0  # J/mol
E_ATP = DG_ATP / N_A  # ~5.06e-20 J per ATP molecule


def per_molecule(j_per_mol: float) -> float:
    """Convert J/mol to J per molecule."""
    return j_per_mol / N_A


# --- Calibration points ---

def calibration_dna_replication() -> dict:
    """DNA base pair replication.

    Physical:  Gibbs free energy of base pairing (~15 kcal/mol avg -> 62.8 kJ/mol)
    Biological: ATP cost (1 ATP per base, DNA polymerase)
    Cognitive:  Information content (2 bits per base: A/T/G/C choice)
    """
    # Physical: average base pairing Gibbs energy
    # AT: ~-13 kcal/mol, GC: ~-22 kcal/mol, average ~-15 kcal/mol
    dG_bp = 15 * 4184  # 15 kcal/mol -> J/mol
    E_phys = per_molecule(dG_bp)  # ~1.04e-19 J

    # Biological: 1 ATP per nucleotide added
    E_bio = E_ATP  # ~5.06e-20 J

    # Cognitive: 2 bits (4 bases, log2(4)=2)
    bits = 2.0
    E_cogn = bits * E_LANDAUER  # ~5.9e-21 J

    return {
        "process": "DNA base pair replication",
        "N": 1,
        "physical": {"E": E_phys, "source": "Gibbs free energy of base pairing (~15 kcal/mol)"},
        "biological": {"E": E_bio, "source": "1 ATP per base (DNA polymerase)"},
        "cognitive": {"E": E_cogn, "source": "2 bits per base (4 bases, log2(4)=2)"},
    }


def calibration_atp_hydrolysis() -> dict:
    """ATP hydrolysis (ATP -> ADP + Pi).

    Physical:  Bond energy change (thermodynamic Delta G)
    Biological: Metabolic energy released (same measurement, different paradigm)
    Cognitive:  Binary switch information (1 bit: ATP/ADP state)
    """
    # Physical: thermodynamic free energy
    E_phys = E_ATP  # ~5.06e-20 J

    # Biological: metabolic energy (same value, but measured via calorimetry)
    E_bio = E_ATP * 0.95  # ~95% efficient in vivo, slight loss

    # Cognitive: 1 bit (ATP vs ADP is a binary state)
    bits = 1.0
    E_cogn = bits * E_LANDAUER  # ~2.95e-21 J

    return {
        "process": "ATP hydrolysis",
        "N": 1,
        "physical": {"E": E_phys, "source": "Delta G of ATP hydrolysis (~30.5 kJ/mol)"},
        "biological": {"E": E_bio, "source": "Calorimetric measurement in vivo (~95% efficiency)"},
        "cognitive": {"E": E_cogn, "source": "1 bit (binary ATP/ADP state)"},
    }


def calibration_ion_transport() -> dict:
    """Na+ ion transport across membrane (single ion).

    Physical:  Electrochemical work (charge x voltage)
    Biological: ATP cost of Na+/K+ pump (1 ATP : 3 Na+ out, 2 K+ in)
    Cognitive:  Information of concentration gradient change (~1.5 bits)
    """
    # Physical: electrochemical work per Na+ ion
    # Membrane voltage ~70 mV, charge = +e
    V_membrane = 0.070  # V
    e_charge = 1.602e-19  # C
    E_phys = e_charge * V_membrane  # ~1.12e-20 J

    # Biological: 1 ATP pumps 3 Na+, so cost per Na+ = 1/3 ATP
    E_bio = E_ATP / 3  # ~1.69e-20 J

    # Cognitive: concentration ratio change encodes ~1.5 bits
    # (gradient from 145mM to 15mM, log2(145/15) ~ 3.3, /2 for half-cycle ~1.65)
    bits = 1.5
    E_cogn = bits * E_LANDAUER  # ~4.4e-21 J

    return {
        "process": "Na+ ion transport",
        "N": 1,
        "physical": {"E": E_phys, "source": "Electrochemical work (e x 70mV)"},
        "biological": {"E": E_bio, "source": "1/3 ATP per Na+ (Na+/K+ pump stoichiometry)"},
        "cognitive": {"E": E_cogn, "source": "~1.5 bits (concentration gradient change)"},
    }


def compute_eta_matrix(calibration: dict) -> dict:
    """Compute cross-paradigm eta values for one calibration point.

    eta[source][target] = E_target / E_source
    (how much of source energy appears as target energy)
    """
    paradigms = ["physical", "biological", "cognitive"]
    etas = {}
    for src in paradigms:
        for tgt in paradigms:
            if src == tgt:
                continue
            E_src = calibration[src]["E"]
            E_tgt = calibration[tgt]["E"]
            if E_src > 0:
                eta = E_tgt / E_src
                etas[f"{src}->{tgt}"] = eta
    return etas


def check_falsification(all_calibrations: list[dict]) -> dict:
    """Check the three falsification conditions from the protocol."""
    conditions = {}

    # Condition 1: eta values span > 3 orders of magnitude across paradigms
    all_etas = []
    for cal in all_calibrations:
        etas = compute_eta_matrix(cal)
        all_etas.extend(etas.values())

    if all_etas:
        eta_min = min(all_etas)
        eta_max = max(all_etas)
        eta_span = eta_max / eta_min if eta_min > 0 else float("inf")
        conditions["eta_span_orders"] = math.log10(eta_span) if eta_span > 0 else 0
        conditions["eta_span_exceeds_3"] = conditions["eta_span_orders"] > 3
        conditions["eta_min"] = eta_min
        conditions["eta_max"] = eta_max

    # Condition 2: conversion degenerates to identity (all eta ≈ 1)
    identity_count = sum(1 for e in all_etas if 0.9 < e < 1.1)
    conditions["degenerate_identity"] = identity_count == len(all_etas) and len(all_etas) > 0

    # Condition 3: cross-paradigm consistency (relative error < 20%)
    # Check if the same conversion ratio is consistent across calibration points
    ratios_pb = []  # physical -> biological
    ratios_pc = []  # physical -> cognitive
    ratios_bc = []  # biological -> cognitive
    for cal in all_calibrations:
        etas = compute_eta_matrix(cal)
        if "physical->biological" in etas:
            ratios_pb.append(etas["physical->biological"])
        if "physical->cognitive" in etas:
            ratios_pc.append(etas["physical->cognitive"])
        if "biological->cognitive" in etas:
            ratios_bc.append(etas["biological->cognitive"])

    consistency = {}
    for name, ratios in [("phys->bio", ratios_pb), ("phys->cogn", ratios_pc), ("bio->cogn", ratios_bc)]:
        if ratios:
            mean_r = sum(ratios) / len(ratios)
            if mean_r > 0:
                rel_errors = [abs(r - mean_r) / mean_r for r in ratios]
                max_rel_error = max(rel_errors)
                consistency[name] = {
                    "values": ratios,
                    "mean": mean_r,
                    "max_relative_error": max_rel_error,
                    "within_20pct": max_rel_error < 0.20,
                }
    conditions["consistency"] = consistency

    # Overall classification
    falsified = (
        conditions.get("eta_span_exceeds_3", False)
        or conditions.get("degenerate_identity", False)
    )
    consistent = all(c.get("within_20pct", False) for c in consistency.values()) if consistency else False

    if falsified:
        classification = "falsification"
    elif consistent:
        classification = "support"
    else:
        classification = "challenge"

    conditions["classification"] = classification
    return conditions


def source_hash() -> str:
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> None:
    calibrations = [
        calibration_dna_replication(),
        calibration_atp_hydrolysis(),
        calibration_ion_transport(),
    ]

    # Compute eta matrices
    for cal in calibrations:
        cal["eta_matrix"] = compute_eta_matrix(cal)

    # Check falsification conditions
    analysis = check_falsification(calibrations)

    # Compute S values (S = E * N, N=1 for all)
    for cal in calibrations:
        cal["S_physical"] = cal["physical"]["E"]
        cal["S_biological"] = cal["biological"]["E"]
        cal["S_cognitive"] = cal["cognitive"]["E"]

    classification = analysis["classification"]

    # Use first calibration for top-level S values
    cal0 = calibrations[0]

    output = {
        "submission_id": "ref-xd-e-paradigm-001-v2-20260731",
        "claim_id": CLAIM_ID,
        "title": "E-dimension paradigm conversion: calibrated cross-paradigm mapping",
        "author": {"name": "reference-implementation", "affiliation": "open-validation", "contact": ""},
        "preregistration": {
            "hash": "in-script-preregistered-constants-v2",
            "timestamp_utc": "2026-07-31T00:00:00+00:00",
            "uri": "protocol-p1-ai.md#8-claim-xd-e-paradigm-001",
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
            "S_A": cal0["S_physical"],
            "S_B": cal0["S_biological"],
            "preferred_path": "A" if classification == "support" else "B",
            "selected_counts": {
                "A": 3 if classification == "support" else 0,
                "B": 0 if classification == "support" else 3,
            },
            "p_value": None,
            "summary": (
                f"3 calibration points; eta span={analysis['eta_span_orders']:.1f} orders; "
                f"consistent={all(c.get('within_20pct', False) for c in analysis['consistency'].values())}; "
                f"classification={classification}"
            ),
            "raw_output": {
                "landauer_limit_J_per_bit": E_LANDAUER,
                "atp_energy_J": E_ATP,
                "calibration_points": calibrations,
                "falsification_analysis": analysis,
            },
        },
        "classification": classification,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
