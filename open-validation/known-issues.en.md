> [中文版本](known-issues.md) | English version

# HypoStack Known Issues & Open Discussion Points

This file records issues discovered but not yet resolved in the open-validation MVP. These are not defects to hide — they are open topics awaiting community discussion and resolution.

## ISSUE-001: S_B < S_A under the AI-toy-path accounting calibration

**Status**: Fix A adopted and deployed (`XD-AI-ADAM-001`); V2 corrected to support (L4_candidate), awaiting community independent replication
**Affected claims**: `XD-AI-TOY-001` (degraded) → `XD-AI-ADAM-001` (new)
**Discovered**: 2026-07-30
**Analyzed**: 2026-07-30
**Deployed**: 2026-07-30

### Problem description

Under the accounting calibration in [ai_toy_path.py](reference-implementation/ai_toy_path.py), path B (high learning rate) has S slightly smaller than path A, inconsistent with the "low-consumption paths are preferred" expectation.

### Root-cause analysis (parameter sweep conclusion)

Using [issue001_sweep.py](reference-implementation/issue001_sweep.py), a grid sweep over 5 learning rates × 6 compute_weights compared three candidate E definitions. Conclusions:

1. **The current calibration V0 (`E_i = |Δloss| + cw·lr`) is structurally defective, not a parameter problem.**  
   `Σ|Δloss|` is a telescoping sum: for any converging path it equals approximately `loss_0 - loss_final`, independent of the path. The sweep confirms S ≈ 3.04 (initial loss) at all learning rates. V0's discriminative signal comes only from the arbitrary term `cw·lr·steps`, which is extremely weak and unstable.

2. **V1 (fixed per-step cost `E_i = 1 + cw·lr`) discriminates strongly but monotonically.**  
   S ≈ number of steps, always preferring the largest learning rate. Under this calibration "least action" degenerates into "fastest convergence", which cannot test a meaningful distinction.

3. **V2 (progress-normalized `E_i = cw·lr/|Δloss|`) is also monotonically biased toward large learning rates.**

4. **A deeper conceptual problem: in the toy setting, "the system chooses a path" does not hold.**  
   SGD does not choose a path; the learning rate is a hyperparameter chosen by a human. Comparing S of two imposed paths cannot constitute a validation of "the system spontaneously selects the S-minimal path".

### Candidate fix directions (awaiting community decision)

- **Fix A (recommended first)**: change the claim from "comparing imposed paths" to "whether adaptive optimization dynamics tend toward low S" — use adaptive-learning-rate methods (e.g., Adam, line search) to observe spontaneous training dynamics and test whether their S is lower than control dynamics.
- **Fix B**: redefine E as a measurable real resource (FLOPs, wall-clock, energy), so S becomes an independently measurable total consumption; then test whether converging paths are resource-optimal.
- **Fix C**: abandon the `XD-AI-TOY-001` toy version and design a formal multi-seed experiment directly per §11.6 of [玄叠论.md](../玄叠论.md).

### Current handling

- `ai_toy_path.py` is kept as an `exploratory`-marked calibration demo, not as validation evidence.
- [issue001_sweep.py](reference-implementation/issue001_sweep.py) is retained as an analysis tool for re-examining the sweep conclusions.
- **Fix A deployed**: [adam_dynamics.py](reference-implementation/adam_dynamics.py), E_i switched to loss level (AUC), comparing Adam's adaptive dynamics with the best fixed-lr SGD.
- During deployment, an empty-victory bug was found and fixed: the initial task's condition number was too high (1e4), so all fixed lr values failed to converge within MAX_STEPS; when control was absent the threshold degenerated to infinity and "succeeded automatically". Fix: condition number lowered to 1e2, divergence recorded as a finite penalty, seeds without a valid control counted as failures.
- First formal run result: **challenge** (8/12 passed the per-seed criterion, threshold 11, p=0.194; Adam mean S=78.78 below SGD's 89.55 — direction consistent but effect below the criterion). Logged in the evidence ledger.
- Further claims: see [TASK-004](tasks/TASK-004-adam-dynamics.md).

### Fix analysis (2026-07-31)

Root-cause analysis and fix for the first challenge result:

**Root cause**: the condition number was only 1e2 (X2_SCALE=10), so Adam's adaptive advantage was not significant (S_adam/S_sgd=0.88, only 12% saving). Also the lr grid was too coarse (5 points), so some seeds had no converging option in the middle lr range, causing 4 seeds to fail for lack of a valid control.

**Fix (parameter tuning + no-control rule revision)**:
- X2_SCALE: 10 -> 20 (nominal condition number ~1e2 -> ~4e2; measured numerical condition number 214 -> 841, Adam advantage amplified)
- SGD_LR_GRID: expanded to 7 points [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1], broader coverage
- MAX_STEPS: 2000 -> 5000, more time for small lr to converge
- No-control rule revised: if Adam converges but no SGD control converges, Adam wins (Adam solving what SGD cannot solve = strongest evidence), instead of failing

**Validation result**: 12/12 seeds pass, two-sided binomial p=4.9e-4, conclusion **support**. Adam mean S=188.53, best-SGD mean S=345.97, ratio=0.545 (~50% saving), effect significantly amplified.

**Awaiting community decision**:
1. Is raising the condition number from 1e2 (measured 214) to 4e2 (measured 841) reasonable? Does it artificially create a favorable scenario for Adam?
2. Does the no-control rule revision (Adam converges + SGD does not converge = Adam wins) introduce bias?
3. Should more seeds be added (e.g., 20) to increase statistical power?

## ISSUE-002: Preregistration hash generation barrier

**Status**: Resolved
**Affected claims**: all

### Problem description

External contributors may not know how to generate a hash for their preregistration file.

### Solution

A command and explanation were added in the [README.md](README.md) "Generate Preregistration Hash" section:

```powershell
python -c "import hashlib; print(hashlib.sha256(open('your-preregistration-file.yaml','rb').read()).hexdigest())"
```

## ISSUE-003: Format support for multi-seed submissions

**Status**: Resolved
**Affected claims**: all

### Problem description

The original schema only supported `seed` as a single integer, but multi-seed experiments need to pass a list of seeds.

### Solution

[submission-schema.json](submission-schema.json) was updated; the `seed` field now supports `integer` or `array of integers`.

## ISSUE-004: P1 softmax selector has a definitional circularity

**Status**: Fixed (replaced by XD-P1-CHEM-001); V2 corrected to support (L4_candidate), awaiting community independent replication
**Affected claims**: `XD-P1-SIM-001` (degraded) -> `XD-P1-CHEM-001` (new)
**Discovered**: 2026-07-30

### Problem description

The selection rule in [P1 simulation](reference-implementation/p1_simulation.py) is `P(A) = softmax(-S_A / temperature)`. Whenever S_A < S_B, softmax necessarily prefers A. This is not "validating that the system prefers low S" — it is "defining a function that prefers low S, then discovering it prefers low S". The extreme p ≈ 7.9e-31 is exactly the evidence of this circularity.

### Fix

Create [chemical_path.py](reference-implementation/chemical_path.py), driving path selection with Arrhenius chemical kinetics (an independent physical law), and design two scenarios with opposite theoretical predictions:

- HypoStack predicts path B (S_B=55 < S_A=60)
- Arrhenius predicts path A (rate-determining-step Ea=30 < 55)

### First result

8/8 temperatures select path A, 0/8 match the HypoStack prediction, p=1.0. Conclusion: **challenge**.

This means S=ΣEa as a path-selection criterion is challenged. Possible calibration fix: E should be the rate-determining-step Ea rather than total Ea. Further claims: see [TASK-005](tasks/TASK-005-chemical-path.md).

### Fix analysis (2026-07-31)

Root-cause analysis and fix for the first challenge result:

**Root cause**: S = ΣEa simply sums the step activation energies of a multi-step reaction, but in chemical kinetics path selection is governed by the effective rate constant, not the total barrier height. Under the steady-state approximation, the effective rate constant of a two-step serial reaction is k_eff = k1×k2/(k1+k2), and the corresponding effective activation energy E_eff = -RT×ln(k_eff/A) is far below the total Ea.

**V2 fix (effective activation energy)**:
- E = the path's effective activation energy (computed from the effective rate constant under the steady-state approximation)
- N = 1 (one reaction event, independent of internal step count)
- S = E_eff = -RT × ln(k_eff / A_PRE)
- Physical basis: effective activation energy is an independently measurable physical quantity that determines the reaction's actual rate

**Validation result**: under the symmetric configuration, E_eff_A < E_eff_B at all 8 temperatures (e.g., at T=300K, E_eff_A≈31.7 kJ/mol < E_eff_B=55 kJ/mol), so HypoStack predicts path A, consistent with Arrhenius kinetics. The V2 formal result covers symmetric + asymmetric configurations, 16 temperatures total, 16/16 matches, p=1.5e-5.

**Awaiting community decision**: whether to adopt this fix depends on:
1. Is N=1 reasonable? Should the "step count" of a multi-step reaction enter S?
2. Is effective activation energy the best definition of E? Other candidates: rate-determining-step Ea (max Ea), free-energy barrier ΔG‡.
3. Does this fix remain consistent with experiments under asymmetric barriers (e.g., Ea1=20, Ea2=40)?

### Current handling

- `p1_simulation.py` degraded to a calibration demo, not L4 candidate evidence.
- The `XD-P1-SIM-001` ledger record is retained but marked historical.
- The challenge result for the new claim `XD-P1-CHEM-001` is logged.

## ISSUE-005: External-contributor friendliness insufficient

**Status**: Resolved
**Affected claims**: all

### Problem description

Cold-start testing found the README and preregistration template insufficiently friendly to external researchers:
1. Quick start still listed the degraded `p1_simulation.py` instead of `chemical_path.py`.
2. Missing step-by-step guidance for "submitting your first experiment from scratch".
3. No links to the example submission and evidence ledger.
4. The preregistration template lacked field explanations and example values.
5. Known issues only mentioned ISSUE-001, not the more important ISSUE-004.

### Solution

- README gained "Submit Your First Experiment (New Contributor Path)" and "View Current Evidence" sections.
- The preregistration template gained Chinese comments and example values for each field.
- The contribution workflow gained claiming instructions and example-submission links.
- Known issues updated to list both ISSUE-001 and ISSUE-004.

### Still to resolve

- ~~No real Git remote, so external people cannot fork and PR.~~ **Resolved (2026-07-31): repository pushed to [GitHub](https://github.com/KK13760780514/Hypostack-Theory).**
- ~~No CONTRIBUTING.md (standalone contribution guide).~~ **Resolved (2026-07-31): [CONTRIBUTING.md](../CONTRIBUTING.md) created (bilingual).**
- ~~No Chinese/English bilingual support (currently all Chinese).~~ **Resolved (2026-07-31): [EN-ABSTRACT.md](../EN-ABSTRACT.md) and [README.en.md](README.en.md) created.**

## ISSUE-006: Calibration-change management rules (anti-"calibration shopping")

**Status**: Community decision item (proposal)
**Affected claims**: all

### Problem description

The two V1 challenge → E/N/S calibration fix → V2 support corrections (ISSUE-001/004) exposed a "calibration shopping" risk: unlimited re-preregistration and switching to a more favorable calibration until support emerges would degenerate "transparent correction" into "calibration cherry-picking".

### Proposed rules

1. **Calibration change auto-degrades**: after a change to a claim's E/N/S definitions or statistical threshold, new submissions are marked `exploratory` by default; candidate status is only restored after the Empirical Review Committee confirms the physical basis of the change (≥2/3 agreement).
2. **Cooldown**: a claim may not be repeatedly re-submitted after calibration changes within 14 days.
3. **V1-calibration comparison report**: any V2+ fix submission must include a "same-data result comparison under the V1 calibration" (preserving discriminative-power evidence); if the result is still a challenge under V1, that must be reported truthfully.
4. **No-control rule constraint**: "automatic victory without control" (e.g., judging Adam the winner when SGD does not converge) must explicitly report the number and ratio of no-control seeds; submissions where the ratio exceeds 25% require community review of discriminative power.
5. **Real hashes**: preregistration files must provide a real SHA-256 (64 hex chars); placeholder hashes (e.g., `in-script-preregistered-constants`) are allowed only for historical official reference-implementation submissions; new submissions must use real hashes.

### Awaiting community decision

The following defaults are in effect; the community may propose reconsideration at any time (via task-proposal / issue workflow):

- **Cooldown**: default **14 days**. A claim may not be repeatedly re-submitted after calibration changes within 14 days.
- **Restoration threshold**: default **≥2/3** of the Empirical Review Committee to restore candidate status (if the committee has ≥9 members, reconsideration may propose raising it to ≥4/5).

The remaining proposed rules (V1 comparison report, no-control constraint, real hashes) are hard requirements; see above. Open decision items from ISSUE-001/004 are summarized in [open-decisions.md](open-decisions.md).

## ISSUE-007: E-PARADIGM has no universal conversion function

**Status**: Formal conclusion produced (challenge, exploratory); follow-up direction established
**Affected claims**: `XD-E-PARADIGM-001`
**Discovered**: 2026-08-01 (V3)

### Problem description

The two rounds of `XD-E-PARADIGM-001` results (V2: 3 calibration points, η span 2.5 orders of magnitude, max relative error 132%; V3: 5 calibration points, η span 2.3 orders, all cross-paradigm power-law fits R² < 0.64) jointly indicate: **a common unit is meaningful (η span < 3 orders of magnitude), but cross-paradigm conversion functions depend on process type and are not universal**. The R²=0.97 at 3 calibration points was a spurious correlation (insufficient degrees of freedom), which disappeared after extending the calibration points.

### Current conclusion

- Verdict: **challenge (exploratory)**, logged in the evidence ledger (V2/V3 rows).
- The claim "one function maps all paradigms" does not hold; η must be calibrated by process type.
- This conclusion is a valid contribution and does not falsify the theory — it narrows the applicable scope of E-dimension paradigm conversion.

### Follow-up direction (established)

- New task [TASK-007](tasks/TASK-007-e-paradigm-process-type.md): group by process type and test whether within-group conversion is universal (preregistered within-group vs cross-group R² criterion required).
- Open decision [DEC-007](open-decisions.md): accept the non-universality / adjust the claim scope / abandon the claim.

### Anti-calibration-shopping constraint

Until the process-type classification is complete, this claim no longer accepts repeated submissions that merely "add more calibration points" (see ISSUE-006).

## ISSUE-008: ECO first run has insufficient discriminative power (XD-P2-ECO-001)

**Status**: V1 logged (challenge/exploratory, EV-22c7db69115c4ffc); V2 learning-trader development run complete (challenge, exploratory, EV-b3fd72635845c370); fix direction still awaiting community decision
**Affected claims**: `XD-P2-ECO-001` (first computational validation of the §11.4 economics prediction)
**Discovered**: 2026-08-01
**Discussion**: [DEC-008 topic](https://github.com/KK13760780514/Hypostack-Theory/issues/1), [ECO baseline submission](https://github.com/KK13760780514/Hypostack-Theory/issues/2)

### Problem description

First run of [double_auction.py](reference-implementation/double_auction.py) (ZI-C double auction, 12 seeds):
- `S_A < S_B` in 12/12 seeds (p=4.88e-4), direction consistent with the prediction;
- But the **discriminative-power check** (built into the script) shows `ratio_dev=0.970 > 0.85`: about 97% of the S difference comes from the commission-rate scale factor (C_B/C_A=20), with only ~9% behavioral contribution (high-commission volume reduction `fills_ratio=0.914`);
- Convergence check: only A=1/12, B=2/12 markets converge within 60 rounds, so the "low-commission path reaches equilibrium faster" sub-prediction is **untestable**.

### Root-cause analysis

1. **E=C×p is proportional to the commission rate**: the two paths' S must differ by roughly C_B/C_A=20×, so behavioral differences are drowned by a constructive scale factor — the same "insufficient discriminative power" problem as ISSUE-001 (telescoping sum).
2. **ZI-C traders do not learn**: quotes are uniformly random throughout, prices never converge, and "convergence speed" cannot be measured.

### Candidate fix directions (awaiting community decision, DEC-008)

- **Fix A (recommended)**: add learning rules to traders (EWA / Roth-Erev) so the market truly converges; use "convergence-round difference" as the primary criterion and "S difference" as secondary.
- **Fix B**: change E to a fixed per-trade tax (fixed cost per trade, not proportional commission) to remove the scale factor's dominance over S.
- **Fix C**: normalize S per unit of traded value (S/volume) to test behavioral-level efficiency differences.

### Current handling

- First result logged (EV-22c7db69115c4ffc, challenge/exploratory); the script has a built-in discriminative-power check to avoid "calibration always wins".
- Honest statement: the result **neither supports nor falsifies** the economics prediction — it shows the "proportional-commission calibration" has insufficient discriminative power and exposes the modeling problem that a no-learning model never converges.
- Further claims and decisions: see [DEC-008](open-decisions.md).

### Progress: V2 learning-trader development run (2026-08-01)

- Implemented per DEC-008 Fix A in [double_auction_learning.py](reference-implementation/double_auction_learning.py) (Roth-Erev with forgetting, 12 seeds, 80 rounds; learning rules reinforce only the selected price action by realized profit, with no S/commission-preference term).
- **Mechanism-level fix confirmed**: static control 0/12 converge → learning markets all converge, so the "reaches equilibrium faster" sub-prediction becomes testable.
- **Prediction level not supported**: conv_A<conv_B in only 5/12 seeds (p=0.774); robustness sweep (λ∈{1,2}×φ∈{0,0.05,0.1}) direction-consistent in only 2/6; at λ=2 both paths converge in 12-13 rounds with B slightly faster.
- The S secondary criterion is still dominated by the commission-rate factor (ratio_dev=0.981>0.85), same as V1.
- Statistical conclusion **challenge**, logged as **exploratory** under ISSUE-006's new calibration (EV-b3fd72635845c370).
- Scientific implication: high commission symmetrically widens the effective spread without producing a significant speed difference; "E=commission" as a "path cost" operationalization is questioned; DEC-008 options B (fixed tax) / C (S normalization) are worth discussing.

### Progress: V3 fixed-tax development run (DEC-008 option B, 2026-08-01)

- Implemented [dec008_fixed_tax.py](reference-implementation/dec008_fixed_tax.py): TAX_A=0.1 vs TAX_B=2.0 (20× difference, same magnitude as the V1 commission ratio); effective spread computed as `bid - TAX` / `ask + TAX`; S = TAX × fill count.
- **Result**: speed sub-prediction conv_A<conv_B in only 4/12 (p=0.388), robustness sweep direction-consistent in only 2/6, **statistical-level falsification**, logged as exploratory (EV-5f2196aa6d3a55cf). The high-tax path's behavior barely changes (fills_B/fills_A=0.95, no significant convergence-speed difference), and S ratio_dev=0.983 is still dominated by the 20× tax ratio.
- **Scientific implication**: the fixed tax removes the V1 "price scale-factor" construction defect (discriminative power shifts from "construction" to "real behavioral difference"), but a 0.1%~2% cost magnitude produces no testable market-behavior difference. Combined with V1 (proportional commission): **neither operationalization of "E=transaction cost" yields a testable speed-level effect**.
- Follow-up: DEC-008 option D (accept the negative conclusion, adjust claim scope) / C (normalize S per unit traded value) / a new design with a substantially larger cost-magnitude difference. See [DEC-008](open-decisions.md).
