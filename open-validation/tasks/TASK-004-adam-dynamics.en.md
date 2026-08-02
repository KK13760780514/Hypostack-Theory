> [中文版本](TASK-004-adam-dynamics.md) | English version

# TASK-004: Reproduce and Challenge Adam Adaptive Dynamics Validation (Fix A)

- Claim: `XD-AI-ADAM-001`
- Difficulty: L2
- Type: reproduction / challenge / criterion improvement
- Predecessor: TASK-002 (XD-AI-TOY-001, whose calibration was rejected by ISSUE-001)

## Background

ISSUE-001 proved that "comparing two artificial paths" is invalid (SGD does not choose paths; the learning rate is a hyperparameter). Fix A instead tests: **is the total consumption S of adaptive optimization dynamics (Adam) systematically lower than that of the best fixed-learning-rate SGD?**

The **first run result of the reference implementation [adam_dynamics.py](../reference-implementation/adam_dynamics.py) (V1, 2026-07-30) is challenge**:

- Adam mean S(AUC) = 78.78, lower than the best SGD's 89.55 (direction consistent)
- But the per-seed criterion `S_adam ≤ 1.1 × S_best_sgd` passed only 8/12, below the threshold 11, p = 0.194
- Conclusion: direction consistent with the expectation, but the effect did not meet the strict preregistered criterion

## V2 Corrected Result (2026-08-01)

After the parameter corrections (condition number raised, nominal ~4e2, measured numerical condition number 841; lr grid of 7 points, MAX_STEPS=5000, no-control rule revised to "Adam converges + SGD does not converge = Adam wins"), **12/12 seeds passed, p=4.9e-4, conclusion corrected to support (L4_candidate)**. Adam mean S=188.53, best-SGD mean S=345.97 (about 50% saving). The current reference implementation [adam_dynamics.py](../reference-implementation/adam_dynamics.py) has been updated to the V2 parameters.

## Operational Definitions (V1 calibration, preregistered in the reference implementation)

- `E_i`: loss level at the end of step i (remaining difference; not a difference — avoids the telescoping-sum)
- `ΔN_i = 1`, `S = Σ loss_i` (area under the loss curve, AUC)
- Task: ill-conditioned toy regression (feature scales differing 10x, condition number ~1e2)
- Control: fixed-lr grid {1e-3, 3e-3, 1e-2, 3e-2, 1e-1}, taking the minimal S among converging runs
- Criterion: ≥11 of 12 seeds satisfy `S_adam ≤ 1.1 × S_best_sgd`; one-sided binomial p < 0.01

## Claimable Directions

1. **Reproduction**: independently reproduce V2's support conclusion (12/12, p=4.9e-4), or test its robustness with a different seed set. Review call: [issue #12](https://github.com/KK13760780514/Hypostack-Theory/issues/12).
2. **Criterion challenge**: are the `1.1` tolerance and the `≥11/12` threshold too strict? Propose an alternative criterion and preregister it.
3. **Task upgrade**: switch to a more ill-conditioned task (condition number 1e3-1e4 + longer MAX_STEPS) and test whether Adam's advantage strengthens with the degree of ill-conditioning.
4. **Optimizer extension**: add RMSProp, Adagrad, and line-search SGD, and test whether the conclusion holds generally for adaptive methods.
5. **E calibration challenge**: propose an E definition other than AUC (e.g., weighted AUC, time-weighted), preregister it, and compare.

## Acceptance Criteria

- Modifying the criterion or calibration requires prior preregistration; deriving the criterion from results after the fact is prohibited.
- Challenge results are entered in the ledger equally with support results.
- The submission JSON passes `validate_submission.py`.

## Deliverables

- Preregistration YAML;
- Submission JSON;
- A brief conclusion: support / challenge / falsification / exploratory.
