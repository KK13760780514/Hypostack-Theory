> [中文版本](review-checklist.md) | English version

# HypoStack Open Validation Review Checklist

Used to review validation submissions in `submissions/`. The review goal is to determine whether a result can enter the evidence ledger — not whether the reviewer likes the theory.

## 0. Review Conclusion Levels

- `form_check_passed`: formally compliant; may proceed to manual scientific review.
- `form_check_failed`: missing critical fields, not reproducible, or violates preregistration constraints.
- `L4_candidate`: completed per preregistration and results support the specific prediction; awaiting independent replication.
- `L5_candidate`: completed per preregistration and results significantly falsify the specific prediction.
- `exploratory`: calibration exploration, task draft, or non-decisive result.
- `needs_review`: failed validation; requires manual review before re-grading (often triggered by re-validation after a schema update).
- `degraded`: the claim has been degraded due to a calibration defect; its historical results are kept but no new submissions are accepted.
- `confirmed`: result confirmed by external independent replication (upgraded from L4_candidate).

## 1. Formal Check

- [ ] JSON passes `validate_submission.py`.
- [ ] `claim_id` belongs to a currently open claim.
- [ ] `submission_id` is unique.
- [ ] Author, timestamp, code hash, and environment info are complete.
- [ ] Submission file is in `submissions/` and follows the naming convention.

## 2. Preregistration Compliance

- [ ] Preregistration time precedes experiment execution time.
- [ ] Measurement paradigm for `E` is fixed.
- [ ] Computation method for `N` is fixed.
- [ ] Computation method for `S` is fixed.
- [ ] Statistical threshold is fixed.
- [ ] `E`, `N`, `S`, or threshold were not modified after the experiment.
- [ ] If deviation occurred, the author explicitly states and explains the impact.

## 3. Reproducibility

- [ ] Code runs.
- [ ] Random seeds are fixed.
- [ ] Data hash or data source is complete.
- [ ] Raw output is traceable.
- [ ] Dependency versions are explicit.
- [ ] Another reviewer can independently re-run the core result.

## 4. Statistical Check

- [ ] Statistical test matches preregistration.
- [ ] One-sided/two-sided choice matches preregistration.
- [ ] p-value computation is correct.
- [ ] Effect size or equivalent metric is reported.
- [ ] Multiple comparisons are handled.
- [ ] No cherry-picking of supportive results.

## 5. Evidence Interpretation

- [ ] `support`, `challenge`, `falsification`, `exploratory` classifications are consistent with the result.
- [ ] Success/failure of one specific prediction is not inflated into success/failure of the whole theory.
- [ ] Negative results are recorded.
- [ ] If the result challenges the current calibration, it is clear whether the issue is calibration, implementation, or theory.

## 6. Conflict of Interest

- [ ] Reviewer has no undeclared interest relationship with the submitter.
- [ ] Reviewer did not modify submission data.
- [ ] Conclusions involving falsification of core presuppositions should be escalated to the independent committee.

## 7. Review Conclusion Template

```text
Conclusion: form_check_passed / form_check_failed
Suggested evidence level: L4_candidate / L5_candidate / exploratory / needs_review
Reasoning:
Needed additions:
Recommend entering the evidence ledger: yes / no
Reviewer:
Date:
```
