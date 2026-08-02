> [中文版本](TASK-002-stress-test-ai-toy.md) | English version

# TASK-002: Stress Test the AI Toy Path Accounting Calibration

> **Status: historical task, superseded by TASK-004.** ISSUE-001's root-cause analysis proved that this task's "artificial two-path comparison" framework is invalid (SGD does not choose paths); Fix A has been landed as [TASK-004](TASK-004-adam-dynamics.md). This file is kept as a historical record and a negative-example calibration.

- Claim: `XD-AI-TOY-001`
- Difficulty: L2-L3
- Type: calibration challenge / multi-seed robustness

## Goal

Stress test the accounting calibration `E = |Δloss| + compute_weight × learning_rate` in [ai_toy_path.py](../reference-implementation/ai_toy_path.py), and judge whether it really distinguishes "more economical" training paths.

## Required Work

1. Fix at least 10 random seeds.
2. Sweep at least 5 learning rates, covering both the "low per-step cost, high step count" and "high per-step cost, low step count" regimes.
3. Keep the target loss, maximum step count, and `compute_weight` uniform.
4. Report each path's `S`, step count, final loss, and whether the target loss is reached.
5. Answer explicitly: under the current calibration, which learning-rate regime has lower `S`? Does this result match the HypoStack Theory expectation?

## Optional Work

- Add a second `E` definition as a control, e.g., counting only `|Δloss|` or only the fixed per-step cost.
- Extend the task from univariate regression to a small classification problem.
- Check whether there is a stable regime where "fewer steps but higher per-step cost" nonetheless yields lower `S`.

## Acceptance Criteria

- Reporting only results that support HypoStack Theory is not allowed.
- If the calibration produces counterintuitive results, they must be stated explicitly.
- The submission JSON passes `validate_submission.py`; the classification should use `challenge` or `exploratory`.

## Deliverables

- Preregistration YAML;
- Multi-seed result table;
- Submission JSON;
- Improvement suggestions for the current `E` calibration.
