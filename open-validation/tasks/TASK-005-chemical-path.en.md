> [中文版本](TASK-005-chemical-path.md) | English version

# TASK-005: Chemical Reaction Path Competition Validation

- Claim: `XD-P1-CHEM-001`
- Difficulty: L2-L3
- Type: independent validation / calibration challenge / falsification attempt

## Background

The old claim `XD-P1-SIM-001` used a softmax selector and had a definitional circularity (softmax necessarily prefers lower S). This task replaces it with a natural system driven by an independent physical law (Arrhenius chemical kinetics), and designs a scenario in which **the two theoretical predictions point in opposite directions**.

## Prediction Conflict

Two chemical reaction paths from reactant R to product P:

- Path A: R -> I -> P (2 steps, each Ea=30 kJ/mol, S_A=60 kJ/mol)
- Path B: R -> P (1 step, Ea=55 kJ/mol, S_B=55 kJ/mol)

- **HypoStack Theory prediction**: the system picks the path with the smallest S, path B (S_B=55 < S_A=60)
- **Arrhenius prediction**: the system picks the path with the lowest rate-determining step, path A (rate-determining-step Ea=30 < path B's Ea=55)

The two predictions **point in opposite directions**, providing real discriminative power.

## First Run Result of the Reference Implementation (V1, 2026-07-30)

[chemical_path.py](../reference-implementation/chemical_path.py) simulates 8 temperature points (280K-500K):

- **8/8 temperatures all picked path A, 0/8 matched the HypoStack Theory prediction, p=1.0**
- Path A's product yield exceeds path B's by 4-5 orders of magnitude at low temperature
- Classification: **challenge** — the S=ΣEa definition is challenged for path selection

## V2 Corrected Result (2026-08-01)

E redefined as effective activation energy (steady-state approximation, E_eff = -RT×ln(k_eff/A)), N=1. Under symmetric + asymmetric barrier configurations, **16/16 temperatures all matched, p=1.5e-5, conclusion corrected to support (L4_candidate)**. Reference implementation: [chemical_path_v2.py](../reference-implementation/chemical_path_v2.py).

## Claimable Directions

1. **Reproduction**: independently reproduce V2's support conclusion (16/16, p=1.5e-5), or test robustness under different temperature ranges/Ea combinations. Review call: [issue #11](https://github.com/KK13760780514/Hypostack-Theory/issues/11).
2. **Calibration challenge**: V2 adopts the effective-activation-energy calibration (steady-state approximation); propose an alternative E definition (e.g., rate-determining-step Ea, free-energy barrier ΔG‡), preregister it, and compare — test whether it still agrees with Arrhenius.
3. **Falsification extension**: find more cases where "S is low but the system does not choose it", or cases where "S is low and the system chooses it".
4. **Theoretical analysis**: analyze under what conditions S=ΣEa / S=E_eff agree with Arrhenius kinetics and under what conditions they conflict.
5. **Real experiment**: replace the simulation with real chemical reaction data (competing reaction paths from the literature).

## Acceptance Criteria

- Modifying the E definition requires prior preregistration.
- Challenge results are entered in the ledger equally with support results.
- The submission JSON passes `validate_submission.py`.

## Deliverables

- Preregistration YAML;
- Submission JSON;
- A brief conclusion: support / challenge / falsification / exploratory.
