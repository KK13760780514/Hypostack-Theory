> [中文版本](TASK-001-reproduce-p1.md) | English version

# TASK-001: Reproduce the P1 Enhanced Simulation

> **Status: historical task, superseded by TASK-005.** ISSUE-004 proved that the softmax selector has a definitional circularity (softmax necessarily prefers lower S). The correction has been landed as [TASK-005](TASK-005-chemical-path.md), which replaces it with Arrhenius chemical kinetics. This file is kept for historical record.

- Claim: `XD-P1-SIM-001`
- Difficulty: L1-L2
- Type: reproduction / robustness check

## Goal

Reproduce the reference implementation [p1_simulation.py](../reference-implementation/p1_simulation.py), and check whether path selection still prefers paths with smaller `S`.

## Required Work

1. Copy and fill in `../preregistration-template.yaml`.
2. Fix at least 3 groups of different random seeds.
3. Without modifying the preregistered calibration, record `S_A`, `S_B`, path-selection counts, and p value.
4. Output a JSON conforming to `../submission-schema.json` and place it in `../submissions/`.

## Optional Work

- Change `temperature` and observe whether the selection probability is still dominated by `S`.
- Increase `runs` and check whether the statistical conclusion is stable.
- Try making path B's `S` lower, and check whether selection reverses.

## Acceptance Criteria

- Preregistration is completed before the experiment.
- The `E`, `N`, `S` definitions are not modified after the experiment.
- The result JSON passes `validate_submission.py`.
- Negative results are submitted as well.

## Deliverables

- Preregistration YAML;
- Submission JSON;
- A brief conclusion: support / challenge / falsification / exploratory.
