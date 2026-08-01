> [中文版本](open-decisions.md) | English version

# Open Decisions

This file summarizes all decisions awaiting community input in the open-validation MVP. Every item is part of the contribution loop: **post decision → community discussion (issue) → vote/consensus → finalize**. Researchers, engineers, and anyone who disagrees with HypoStack Theory are welcome to participate.

- Propose a decision: record background in [known-issues.md](known-issues.md) or a new issue
- Discuss: open an issue in this repository (the [task-proposal template](../.github/ISSUE_TEMPLATE/task-proposal.md) works), referencing the decision ID
- Finalize: maintainers update [known-issues.md](known-issues.md), and the protocol and reference implementations are updated accordingly
- Manual publishing guide (with DEC-001–008 issue drafts): see [publishing-guide.md](publishing-guide.md)

---

## DEC-001: Does the ADAM task construction bias toward Adam? (source: ISSUE-001)

**Background**: `XD-AI-ADAM-001` V2 raised the Hessian condition number from 1e2 to ~4e2, amplifying Adam's advantage from 12% to 50% energy savings (ratio=0.545).

**Options**:
- A. Keep condition number 4e2 (current default)
- B. Revert to 1e2 (more conservative but weaker effect; needs a larger sample)
- C. Sweep between 1e2/4e2 and report how the effect varies with the condition number

**Default recommendation**: C (do not change the criterion immediately, but add a sensitivity analysis so the community can weigh discriminative power vs. fairness).

**Decision-support evidence (2026-08-01, proposer-developed, [dec001_cond_scan.py](reference-implementation/dec001_cond_scan.py))**: an 8-point condition-number sweep over X2_SCALE ∈ {5..40} (exact numerical Hessian condition numbers 58→3349; note the nominal "~1e2/~4e2" in the script comments differs slightly — scale=10 is actually 214, scale=20 is 841):

| Numerical cond | ratio S_adam/S_sgd | savings | seeds pass | p | verdict |
|---|---|---|---|---|---|
| 58 | 2.59 | -159% | 0/12 | 1.00 | challenge |
| 123 | 1.55 | -55% | 3/12 | 0.98 | challenge |
| 214 | 0.88 | 12% | 8/12 | 0.19 | challenge (V1) |
| 332 | 0.87 | 13% | 9/12 | 0.07 | challenge |
| 476 | 0.77 | 23% | 10/12 | 0.02 | challenge |
| 841 | 0.54 | 45% | 12/12 | 2.4e-4 | **support** (V2) |
| 1886 | 0.65 | 35% | 12/12 | 2.4e-4 | support |
| 3349 | 0.50 | 50% | 12/12 | 2.4e-4 | support |

**Reading**: the effect grows **smoothly and monotonically** with the condition number (ratio 0.88→0.50), not as a step — supporting option C's sensitivity-curve approach; but the support threshold (≥11/12) is only reached at condition number ≥841, so the V1 challenge at 214 is real and the V2 support genuinely depends on the higher condition number. Also: higher condition numbers mean more no-control seeds (3-4/12 at scale=30/40), raising the weight of the DEC-002 no-control rule.

**Affected claim**: XD-AI-ADAM-001. **Status**: reference evidence produced, awaiting community confirmation. **Discussion**: [issue #4](https://github.com/KK13760780514/Hypostack-Theory/issues/4).

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

**Decision-support evidence (2026-08-01, proposer-developed, [dec005_ea_definitions.py](reference-implementation/dec005_ea_definitions.py))**: recomputed predictions under three E definitions against actual Arrhenius kinetics across 3 configs (symmetric, asymmetric, plus a new "comparable-rates" config Ea1=25/Ea2=35/Ea3=55) × 8 temperatures = 24 cases:

- **E_eff (steady-state approximation)**: 24/24 matches (V2 as-is)
- **E_maxstep (rate-determining-step Ea = max(Ea1,Ea2))**: 24/24 matches
- **E_sum (total barrier ΣEa)**: 0/24 matches (V1 challenge reaffirmed)

**Reading**: E_eff and E_maxstep predict identically on all configs (including the purpose-built "comparable-rates" config) — under the steady-state approximation, E_eff ≈ max(Ea_i) for a two-step series (slow step dominates, difference <0.2%). Thus **the current experimental framework cannot distinguish E_eff from rate-determining-step Ea**; the V2 16/16 evidence supports both equally. Distinguishing them requires a ΔG‡ (free-energy barrier, with entropic contributions) experiment. Recommend confirming option A (keep E_eff, physically more rigorous) while noting that "E_eff vs rate-determining-step Ea is underdetermined by current evidence".

**Affected claim**: XD-P1-CHEM-001. **Status**: reference evidence produced, awaiting community confirmation.

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

**Affected claim**: XD-E-PARADIGM-001. **Status**: open. **Discussion**: [issue #3](https://github.com/KK13760780514/Hypostack-Theory/issues/3).

## DEC-008: How to handle the ECO first run's weak discriminative power (source: ISSUE-008)

**Background**: `XD-P2-ECO-001`'s first run had S_A<S_B in 12/12 seeds (p=4.88e-4), but `ratio_dev=0.970>0.85`: ~97% of the S difference comes from the commission-rate factor (construction), with only ~9% behavioural contribution; and the learning-free ZI-C market barely converges, making the "converges faster" sub-prediction untestable. See [protocol-p1-ai.md](protocol-p1-ai.md) section 10 and [ISSUE-008](known-issues.md).

**Options**:
- A. Add learning traders (EWA/Roth-Erev) so the market actually converges; make "convergence-speed difference" the primary criterion and "S difference" secondary (V2 executed, unsupported)
- B. Change E to a fixed per-trade tax (not proportional commission), removing the rate-factor dominance (V3 executed, falsification)
- C. Normalize S per unit of traded value (S/volume) to test behavioural efficiency differences
- D. Keep the first result, accept the negative conclusion "proportional-commission calibration is untestable", and abandon the claim
- E. **Switching experiment**: a policy intervention raises one path's cost mid-run; test whether the market "automatically switches" to the new lower-tax path (direct test of the theory's "choice/switching" assertion; preregistration draft in [predictions-operationalization.md](predictions-operationalization.md) P-ECO-002)

**Default recommendation**: lean toward D or C (options A/B reference evidence both failed); if the community judges the "automatic switching" prediction worth testing, evaluate option E first. Per ISSUE-006, any calibration change must be re-preregistered and defaults to exploratory.

**Development progress (2026-08-01)**: a V2 learning-trader run (Roth-Erev, 12 seeds, 80 rounds) per option A is complete: market convergence is fixed (static 0/12 → learning converges in all seeds), but the speed sub-prediction is NOT supported (conv_A<conv_B in only 5/12 seeds, p=0.774; direction consistent in only 2/6 robustness combos). Statistical outcome: challenge; entered as exploratory (EV-b3fd72635845c370). This questions the "E=commission" operationalization and suggests options B/C for discussion. See [ISSUE-008](known-issues.md).

**Option B development run (2026-08-01, V3 fixed-tax, [dec008_fixed_tax.py](reference-implementation/dec008_fixed_tax.py))**: TAX_A=0.1 vs TAX_B=2.0 (20× difference, same magnitude as the V1 commission ratio), learning market 12 seeds 80 rounds. Result: speed sub-prediction conv_A<conv_B in only 4/12 seeds (two-sided binomial p=0.388), direction consistent in only 2/6 robustness combos, **statistical-level falsification**, entered as exploratory (EV-5f2196aa6d3a55cf). Key finding: under a fixed tax the high-tax path's behavior barely changes (fills_B/fills_A=0.95, no significant convergence-speed difference, S ratio_dev=0.983 still dominated by the 20× tax factor) — a 0.1%~2% cost magnitude produces no testable market-behavior difference. Combined with V1 (proportional commission): **neither proportional-commission nor fixed-tax operationalization of "E=transaction cost" yields a testable speed-level effect** in this model framework; the discriminative-power problem shifts from a "constructive scale factor" (V1) to "the effect itself is too weak" (V2/V3). Options D (accept the negative conclusion and narrow the claim) and C (normalize S per unit traded value) are now favored, or a new design with a substantially larger cost-magnitude difference.

**Affected claim**: XD-P2-ECO-001. **Status**: option A/B reference evidence produced, awaiting community confirmation. **Discussion**: [issue #1](https://github.com/KK13760780514/Hypostack-Theory/issues/1) (ECO baseline submission in [issue #2](https://github.com/KK13760780514/Hypostack-Theory/issues/2)).

---

## Decision Status Table

| ID | Topic | Status | Default recommendation |
|----|-------|--------|------------------------|
| DEC-001 | Condition number bias toward Adam | reference evidence produced (sensitivity curve) | C (keep 4e2, publish curve; note numerical cond is 841) |
| DEC-002 | No-control win rule | open | A + mandatory share reporting |
| DEC-003 | Number of seeds | open | keep 12 |
| DEC-004 | CHEM N=1 reasonableness | open (asymmetric config already covered in V2) | A |
| DEC-005 | Best definition of E | reference evidence produced (E_eff and rate-determining-step Ea indistinguishable) | A (keep E_eff, note underdetermination) |
| DEC-006 | Cooldown / reinstatement threshold | defaults active | 14 days / ≥2/3 |
| DEC-007 | E-PARADIGM non-universality | open | A + TASK-007 |
| DEC-008 | ECO first-run weak discriminative power | option A/B reference evidence produced (V2/V3 both unsupported) | lean D/C; or option E switching experiment (P-ECO-002) |
