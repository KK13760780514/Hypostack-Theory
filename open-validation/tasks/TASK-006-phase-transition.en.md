> [中文版本](TASK-006-phase-transition.md) | English version

# TASK-006: Phase-Transition Path Selection

**Claim ID**: XD-P1-PHASE-001
**Discipline**: Physics
**Difficulty**: Medium
**Status**: First result support (L4_candidate), awaiting independent replication

## Prediction

When a material system transitions from one phase to another, the system selects the path with the smallest total consumption S = ∫ E dN.

## Experimental Plan

Simulate the phase transition with a 2D Ising model. Three cooling protocols (slow cooling / medium cooling / quench), computing each path's S = Σ(|T_i - T_c|/T_c × N_flips_i). Prediction: S_slow < S_quench.

## Reference Implementation

- Script: [phase_transition.py](../reference-implementation/phase_transition.py)
- Protocol: [protocol-p1-ai.md section 9](../protocol-p1-ai.md)

## First Result

support (12/12, p=4.9e-4). Mean S_A(slow cooling)=48903 vs S_C(quench)=237486.

## How to Participate (Independent Replication Path)

> Independent replication is equally subject to the preregistration rules (see [README Independent Replication section](../README.md#独立复核复现现有结果)). Review call: [issue #13](https://github.com/KK13760780514/Hypostack-Theory/issues/13).

1. Fork the repository
2. **Preregister first**: copy `../preregistration-template.yaml`, fix E/N/S and the statistical criterion (prediction `S_slow < S_quench`, following the original implementation's calibration), and generate a real SHA-256 hash
3. Independently implement or run `phase_transition.py`; if running the reference script directly, you must use seeds/parameter grids (lattice size, cooling steps, temperature range) different from the original submission and explicitly report the differences
4. Modify parameters (lattice size, cooling steps, temperature range) to test robustness
5. Submit your result JSON (validated by `../validate_submission.py`) — support, challenge, and falsification results are entered equally

## Acceptance Criteria

- Preregistration is completed before the experiment; E/N/S and the criterion must not be modified after the fact (including "adjusting the criterion to pass after obtaining results")
- If running the reference script directly, you must report parameter differences from the original submission, to avoid "re-running without differences being counted as independent replication"
- The result JSON passes `validate_submission.py`; `preregistration.hash` is a real SHA-256
- Negative results (failure to reproduce `S_slow < S_quench`) are submitted as well
