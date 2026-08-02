> [中文版本](publishing-guide.md) | English version

# HypoStack Open Validation · Publishing Guide (GitHub Issues)

> Goal: publish the open decisions (DEC-001–008) as GitHub Issues to start the contribution loop "task release → preregistration → submission → validation → review → evidence ledger".
> Prerequisite: `gh` CLI and `GH_TOKEN` are unavailable in the current environment; this guide is a **purely manual publishing flow** (browser operations).

## 0. Pre-publish self-check

1. All changes are committed locally: evidence ledger (`evidence-ledger.csv`), submission JSONs, protocol (`protocol-p1-ai.md`), open decisions (`open-decisions.md`), known issues (`known-issues.md`), etc.
2. Every new submission has passed `python .\open-validation\validate_submission.py <submission.json>` and has been entered in the ledger.
3. CI (`.github/workflows/ci.yml`) passes.
4. After pushing, the repository documentation stays consistent: **5 active claims (3 support + 2 challenge)**.

## 1. Publishing a DEC issue manually

1. Open <https://github.com/KK13760780514/Hypostack-Theory/issues/new>.
2. Select the **Open decision** template (`.github/ISSUE_TEMPLATE/decision.md`).
3. Paste the corresponding DEC draft from section 3.
4. Title format: `[Decision] DEC-00X: <short title>`.
5. After publishing: backfill the issue link into the "Discussion" column of the corresponding entry in `open-decisions.md` (optional, helps tracking).

## 2. Recommended publishing order

Sorted by direct relevance to current evidence; publish 1 item at a time to avoid spamming:

| Order | ID | Topic | Reason |
|------|------|------|------|
| 1 | DEC-008 | ECO insufficient discriminative power | Newest; blocks the next design round of XD-P2-ECO-001 |
| 2 | DEC-007 | E-PARADIGM not universal | TASK-007 already launched; needs community direction |
| 3 | DEC-001 | ADAM condition number | Directly relates to the fairness of a support result |
| 4 | DEC-002 | No-control counts as win | Related to the ADAM criterion |
| 5 | DEC-003 | Number of seeds | Statistical power |
| 6 | DEC-004 | CHEM N=1 | Calibration reasonableness |
| 7 | DEC-005 | Best definition of E | Linked with DEC-004 |
| 8 | DEC-006 | Cooldown parameters | Governance parameter review; can be published last |

## 3. DEC issue drafts (paste-ready)

### DEC-008: How to handle ECO's insufficient discriminative power

**Decision ID and topic**

DEC-008: How to handle ECO's insufficient discriminative power

**Background**

`XD-P2-ECO-001` (market equilibrium path selection): V1 (proportional commission, first run) had S_A<S_B in 12/12 seeds (p=4.88e-4), but `ratio_dev = 0.970 > 0.85` — about 97% of the S difference comes from the commission-rate proportional factor (constructive), behavior contributes only ~9%, and ZI-C zero-intelligence constrained traders do not learn and the market does not converge, so the speed sub-prediction is untestable (ledger row EV-22c7db69115c4ffc). V2 (learning traders, option A): the convergence problem was fixed, but the speed sub-prediction was 5/12 (p=0.774), not supported (ledger row EV-b3fd72635845c370). V3 (fixed tax, option B): speed sub-prediction 4/12 (p=0.388, falsification); the high-tax path's behavior barely changed (ledger row EV-5f2196aa6d3a55cf). Conclusion: neither proportional commission nor fixed tax produced a testable effect. See [protocol-p1-ai.md](protocol-p1-ai.md) section 10 and [known-issues.md](known-issues.md) ISSUE-008.

**Candidate options**

- A. Add learning rules to traders (EWA/Roth-Erev) so the market truly converges; "convergence-round difference" as the primary criterion, "S difference" as secondary (already executed in V2, not supported)
- B. Switch E to a fixed transaction tax (not proportional commission) to remove the proportional factor's dominance (already executed in V3, falsification)
- C. Normalize S by turnover (S/volume) to test behavioral-level efficiency differences
- D. Accept the negative conclusion that "the trading-cost calibration is untestable in this model framework", narrow or retire the claim
- E. **Switch experiment**: change path costs mid-course via policy intervention and test whether the market "automatically turns" toward the new low-tax path (directly tests the theory's "choice/switching" assertion; preregistration draft in [predictions-operationalization.md](predictions-operationalization.md) P-ECO-002)

**My position and reasoning**

Both A and B have produced reference evidence that did not pass (V2 p=0.774, V3 p=0.388): the problem has shifted from V1's "constructive proportional factor" to "the effect itself is too weak" — trading costs at the 0.1%-2% level do not produce testable market-behavior differences. Current lean: D (narrow the claim to "behavioral efficiency under cost normalization", or accept the negative conclusion) or C (S/volume normalization); option E provides a direct test of "behavioral-level path choice" and is the only direction aligned with the theory's core assertion, usable as a low-cost control. Per ISSUE-006, any calibration change must be re-preregistered and defaults to exploratory (14-day cooldown).

**Suggested default**

D or C; if the community still considers the "automatic switching" prediction (11.4 second sub-prediction) worth testing, prioritize evaluating option E (switch experiment; P-ECO-002 draft ready); otherwise propose a new design with a cost-magnitude gap ≥10x as a control.

**Impact on existing evidence**

- [x] Changes calibration → must go through the degradation and cooldown flow per [ISSUE-006](open-validation/known-issues.md)
- [ ] No calibration change; governance/process only
- [ ] Other:

**Expected consensus method**

- [ ] Simple majority
- [x] ≥2/3 empirical review committee (committee not yet formed; community discussion primary)
- [ ] Other

---

### DEC-007: How to handle the "no universal mapping function" conclusion for E-PARADIGM

**Decision ID and topic**

DEC-007: How to handle the "no universal mapping function" conclusion for E-PARADIGM

**Background**

`XD-E-PARADIGM-001` V3 at 5 calibration points has all cross-paradigm power-law fits R² < 0.64, concluding "a unified dimension is meaningful (η spans 2.3 orders of magnitude) but the mapping function depends on process type and is not universal". See [protocol-p1-ai.md](protocol-p1-ai.md) section 8.

**Candidate options**

- A. Accept the non-universal conclusion: keep E-PARADIGM-001 as challenge (exploratory), restrict paradigm mapping to "calibrate η by process type" (recommended)
- B. Adjust the claim to "within-group universality grouped by process type" (requires a new preregistration)
- C. Retire the claim

**Suggested default**

A, and open TASK-007 (calibrate η by process type) as the follow-up direction.

**Impact on existing evidence**

- [ ] Changes calibration
- [x] No calibration change; governance/process only (narrow the claim scope)

**Expected consensus method**

- [x] ≥2/3 empirical review committee (community discussion primary for now)

---

### DEC-001: Does the ADAM task construction bias toward Adam?

**Decision ID and topic**

DEC-001: Does the ADAM task construction bias toward Adam (should the condition number be adjusted)?

**Background**

`XD-AI-ADAM-001` V2 raised the Hessian condition number from 1e2 to ~4e2 (nominal; measured numerical condition number 841), amplifying Adam's advantage from 12% to 50% energy savings (ratio=0.545).

**Candidate options**

- A. Keep the condition number at 4e2 (current default)
- B. Revert to 1e2 (more conservative but weaker effect; needs a larger sample)
- C. Add a gradient sweep between 1e2/4e2 and report the effect-vs-condition-number curve (recommended)

**Suggested default**

C: do not change the criterion immediately; add a sensitivity analysis so the community can weigh discriminative power vs. fairness.

**Decision-support evidence (2026-08-01, proposer-developed, [dec001_cond_scan.py](reference-implementation/dec001_cond_scan.py))**: 8-point condition-number sweep (X2_SCALE∈{5..40}, numerical condition numbers 58->3349). The effect grows smoothly and monotonically with the condition number (ratio 0.88->0.50), not a step; but the support threshold is reached only at numerical condition number ≥841, and the V1 challenge at 214 is real. See [open-decisions.md](open-decisions.md) DEC-001.

**Impact on existing evidence**

- [ ] Changes calibration
- [x] No calibration change; governance/process only (sensitivity analysis is additional evidence)

**Expected consensus method**

- [x] Simple majority / community discussion

---

### DEC-002: Does the "no-control seed counts as a win" rule introduce bias?

**Decision ID and topic**

DEC-002: Does the "no-control seed counts as a win" rule introduce bias?

**Background**

`XD-AI-ADAM-001` V2 revised the rule to "Adam converges + best-SGD has no converging control → Adam wins".

**Candidate options**

- A. Keep it (Adam solving what SGD cannot solve = strongest evidence) (recommended)
- B. No-control seeds count as failures (revert to the V1 rule)
- C. Report no-control seeds separately, excluding them from the binomial denominator

**Suggested default**

A, but per ISSUE-006 rule 4, the number and share of no-control seeds must be reported explicitly (>25% requires community review).

**Impact on existing evidence**

- [ ] Changes calibration
- [x] No calibration change; governance/process only (mandatory reporting)

**Expected consensus method**

- [x] Simple majority / community discussion

---

### DEC-003: Should the number of seeds be increased?

**Decision ID and topic**

DEC-003: Should the number of seeds be increased?

**Background**

Currently 12 seeds, p=4.9e-4 (two-sided binomial; the smallest resolvable p when all 12 seeds pass).

**Candidate options**

- A. Keep 12 (current default; sufficient statistical power) (recommended)
- B. Increase to 20 or more (more power, but more compute; limited gain in binomial p resolution)

**Suggested default**

A; independent replicators who reproduce success are encouraged to use more seeds as additional evidence.

**Impact on existing evidence**

- [ ] Changes calibration
- [x] No calibration change; governance/process only

**Expected consensus method**

- [x] Simple majority / community discussion

---

### DEC-004: Is N=1 reasonable for CHEM?

**Decision ID and topic**

DEC-004: Is N=1 reasonable for CHEM?

**Background**

`XD-P1-CHEM-001` V2 fixes N to 1 (one reaction event), so S = E_eff. The "number of steps" of a multi-step reaction no longer enters S.

**Candidate options**

- A. Keep N=1 (current default; effective activation energy governs rate) (recommended)
- B. Let N be the number of reaction steps (back to ΣEa, already challenged in V1)
- C. Define N as reaction events × a temperature-dependent factor

**Suggested default**

A, with additional validation under asymmetric barrier configurations (see DEC-005).

**Impact on existing evidence**

- [ ] Changes calibration
- [x] No calibration change; governance/process only

**Expected consensus method**

- [x] Simple majority / community discussion

---

### DEC-005: Is effective activation energy the best definition of E?

**Decision ID and topic**

DEC-005: Is effective activation energy the best definition of E?

**Background**

Candidate definitions: total barrier ΣEa (V1, already challenged), effective activation energy E_eff (V2, support), rate-determining-step Ea (max Ea), free-energy barrier ΔG‡.

**Candidate options**

- A. Keep E_eff (current default) (recommended)
- B. Recompute with rate-determining-step Ea and compare with the V2 result
- C. Design a new experiment with ΔG‡ (including entropy contributions)

**Suggested default**

A; the community may submit "same experiment, different E definition" comparison results as a challenge.

**Decision-support evidence (2026-08-01, proposer-developed, [dec005_ea_definitions.py](reference-implementation/dec005_ea_definitions.py))**: 3 configurations × 8 temperatures = 24 items. E_eff 24/24, rate-determining-step Ea 24/24, ΣEa 0/24. Under the steady-state approximation E_eff ≈ max(Ea_i) (difference <0.2%); the current framework cannot distinguish the two; distinguishing them requires a ΔG‡ experiment. See [open-decisions.md](open-decisions.md) DEC-005.

**Impact on existing evidence**

- [ ] Changes calibration
- [x] No calibration change; governance/process only

**Expected consensus method**

- [x] Simple majority / community discussion

---

### DEC-006: Calibration-change cooldown and recovery threshold (review)

**Decision ID and topic**

DEC-006: Calibration-change cooldown and recovery threshold (review)

**Background**

Governance parameters against "calibration shopping"; the current defaults are in effect: cooldown **14 days**, recovery-to-candidate threshold **≥2/3** empirical review committee approval.

**Candidate options (review)**

- A. Keep 14 days / ≥2/3 (current default) (recommended)
- B. Lengthen the cooldown (e.g., 30 days) or raise the threshold
- C. Shorten the cooldown (e.g., 7 days) or lower the threshold

**Suggested default**

A; if adjustment is desired, attach actual cases from the ISSUE-006 discussion as justification.

**Impact on existing evidence**

- [ ] Changes calibration
- [x] No calibration change; governance/process only

**Expected consensus method**

- [x] ≥2/3 empirical review committee (community discussion primary for now)

---

## 4. Other publishable content (optional)

- **New evidence announcement**: use the submission template to publish the latest `XD-P2-ECO-001` round (V3 fixed tax) result (falsification), citing ledger row EV-5f2196aa6d3a55cf; historical V1/V2 rows: EV-22c7db69115c4ffc, EV-b3fd72635845c370.
- **Independent replication call**: `CALL-FOR-REPLICATION.md` already contains a bilingual call-to-action; can be forwarded periodically to GitHub Discussions / Zhihu / V2EX.
