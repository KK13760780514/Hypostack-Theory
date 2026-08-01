> [中文版本](open-decisions.md) | English version

# Open Decisions

This file summarizes all decisions awaiting community input in the open-validation MVP. Every item is part of the contribution loop: **post decision → community discussion (issue) → vote/consensus → finalize**. Researchers, engineers, and anyone who disagrees with HypoStack Theory are welcome to participate.

- Propose a decision: record background in [known-issues.md](known-issues.md) or a new issue
- Discuss: open an issue in this repository (the [task-proposal template](../.github/ISSUE_TEMPLATE/task-proposal.md) works), referencing the decision ID
- Finalize: maintainers update [known-issues.md](known-issues.md), and the protocol and reference implementations are updated accordingly

---

## DEC-001: Does the ADAM task construction bias toward Adam? (source: ISSUE-001)

**Background**: `XD-AI-ADAM-001` V2 raised the Hessian condition number from 1e2 to ~4e2, amplifying Adam's advantage from 12% to 50% energy savings (ratio=0.545).

**Options**:
- A. Keep condition number 4e2 (current default)
- B. Revert to 1e2 (more conservative but weaker effect; needs a larger sample)
- C. Sweep between 1e2/4e2 and report how the effect varies with the condition number

**Default recommendation**: C (do not change the criterion immediately, but add a sensitivity analysis so the community can weigh discriminative power vs. fairness).

**Affected claim**: XD-AI-ADAM-001. **Status**: open.

## DEC-002: Does the "no-control seed counts as a win" rule introduce bias? (source: ISSUE-001)

**Background**: V2 revised the rule to "Adam converges + best-SGD has no converging control → Adam wins".

**Options**:
- A. Keep it (Adam solving what SGD cannot solve = strongest evidence)
- B. No-control seeds count as failures (revert to V1 rule, but V1 then had 4/12 failures)
- C. Report no-control seeds separately, excluding them from the binomial denominator

**Default recommendation**: A, but per ISSUE-006 rule 4, the number and share of no-control seeds must be reported explicitly (>25% requires community review).

**Affected claim**: XD-AI-ADAM-001. **Status**: open.

## DEC-003: Should the number of seeds be increased? (source: ISSUE-001)

**Background**: Currently 12 seeds, p=2.4e-4 (the binomial test can only resolve p at this level for 12 seeds when all pass).

**Options**:
- A. Keep 12 (current default; sufficient statistical power)
- B. Increase to 20 or more (more power, but more compute; limited gain in binomial p resolution)

**Default recommendation**: A; independent replicators are encouraged to use more seeds as additional evidence if they reproduce success.

**Affected claims**: XD-AI-ADAM-001, XD-P1-PHASE-001. **Status**: open.

## DEC-004: Is N=1 reasonable for CHEM? (source: ISSUE-004)

**Background**: V2 fixes N to 1 (one reaction event), so S = E_eff. The "number of steps" of a multi-step reaction no longer enters S.

**Options**:
- A. Keep N=1 (current default; effective activation energy governs rate)
- B. Let N be the number of reaction steps (back to ΣEa, already challenged in V1)
- C. Define N as reaction events × a temperature-dependent factor

**Default recommendation**: A, with additional validation under asymmetric barrier configurations (see DEC-005).

**Affected claim**: XD-P1-CHEM-001. **Status**: open.

## DEC-005: Is effective activation energy the best definition of E? (source: ISSUE-004)

**Background**: Candidates: total barrier ΣEa (V1, challenged), effective activation energy E_eff (V2, support), rate-determining-step Ea (max Ea), free-energy barrier ΔG‡.

**Options**:
- A. Keep E_eff (current default)
- B. Recompute with rate-determining-step Ea and compare with V2 results
- C. Design a new experiment using ΔG‡ (including entropic contributions)

**Default recommendation**: A; the community may submit "same experiment, different E definition" comparisons as challenges.

**Affected claim**: XD-P1-CHEM-001. **Status**: open.

## DEC-006: Calibration-change cooldown and reinstatement threshold (source: ISSUE-006)

**Background**: Governance parameters against "calibration shopping".

**Finalized defaults** (can be reopened for review):
- Cooldown: **14 days**
- Threshold to restore candidate status: **≥2/3** agreement of the empirical review committee

**Reopening path**: open an issue with rationale and impact.

**Affected claims**: all. **Status**: defaults active; open for review.

## DEC-007: How to handle the "no universal conversion function" conclusion of E-PARADIGM (source: V3 result)

**Background**: V3 found all cross-paradigm power-law fits R² < 0.64 across 5 calibration points, concluding "a common unit is meaningful (η span 2.3 orders < 3) but conversion functions depend on process type; not universal". See [protocol-p1-ai.md](protocol-p1-ai.md) section 8.

**Options**:
- A. Accept the non-universality: keep E-PARADIGM-001 as challenge (exploratory), restrict paradigm conversion to "calibrate η by process type"
- B. Reframe the claim as "within-process-type universality" (requires a new preregistration)
- C. Abandon the claim (evidence suggests cross-paradigm E conversion is not feasible)

**Default recommendation**: A, and open TASK-007 (calibrate η by process type) as the follow-up direction.

**Affected claim**: XD-E-PARADIGM-001. **Status**: open.

---

## Decision Status Table

| ID | Topic | Status | Default recommendation |
|----|-------|--------|------------------------|
| DEC-001 | Condition number bias toward Adam | open | C (sensitivity analysis) |
| DEC-002 | No-control win rule | open | A + mandatory share reporting |
| DEC-003 | Number of seeds | open | keep 12 |
| DEC-004 | CHEM N=1 reasonableness | open | A |
| DEC-005 | Best definition of E | open | A |
| DEC-006 | Cooldown / reinstatement threshold | defaults active | 14 days / ≥2/3 |
| DEC-007 | E-PARADIGM non-universality | open | A + TASK-007 |
