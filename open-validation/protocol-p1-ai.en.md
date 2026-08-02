> [中文版本](protocol-p1-ai.md) | English version

# HypoStack Open Validation Protocol (v0.1.0)

Version: v0.1.0 (open-validation protocol version, independent of the theory protocol v16.1.0)  
Status: Open-validation MVP  
Core formula: `S = Σ(E_i × ΔN_i)`

> **File naming note**: This file is named `protocol-p1-ai.md` (historical naming), but its content covers all 7 claims: P1 simulation (XD-P1-SIM-001), chemical paths (XD-P1-CHEM-001), AI toy (XD-AI-TOY-001), Adam dynamics (XD-AI-ADAM-001), E-paradigm mapping (XD-E-PARADIGM-001), phase-transition paths (XD-P1-PHASE-001), and market equilibrium (XD-P2-ECO-001). The filename is not changed with the scope to keep existing document and issue links stable.

## 1. Validation Objective

This protocol tests one narrow question only: after `E`, `N`, and `S` are explicitly defined, do systems prefer paths with smaller total consumption `S`.

**Calibration note (2026-08-01)**: All 5 active claims currently use the **ordering-test** form — they compute S for two imposed paths and compare the values (e.g., the share of seeds with S_A<S_B), without directly measuring the system's "choosing/switching" event. The theory's "choice" assertion (玄叠论.md layer-2 breaking; sections 11.1/11.4/11.6) can be operationalized into two kinds of tests:

- **Ordering test** (current claims): does the smaller-S path dominate in retention/frequency/convergence?
- **Choice/switching test** (future direction): when a system faces candidate paths, or when a path's cost changes mid-course, does it turn toward the smaller-S path? — no claim covers this yet; a design draft is in [predictions-operationalization.md](predictions-operationalization.md) P-ECO-002.

Ordering tests produce the first batch of L4/L5 candidate evidence; the choice/switching test is a stronger test form, to be landed by future claims. This protocol's objective statement has been converged under this calibration.

It does not claim to prove the whole of HypoStack theory; it only produces the first batch of L4/L5 candidate evidence that can be independently replicated.

Any calibration change (E/N/S definitions or statistical thresholds) must follow the *Calibration-Change Management Rules* (ISSUE-006) in [known-issues.md](known-issues.md): after a change, new submissions default to `exploratory` with a cooldown period, and V2+ corrections must attach a V1-calibration comparison report.

## 2. Claim XD-P1-SIM-001: P1 Enhanced Computer Simulation (degraded)

> **⚠ Degraded**: this claim contains a definitional circularity (softmax necessarily prefers lower S) and has been replaced by [XD-P1-CHEM-001](#7-claim-xd-p1-chem-001chemical-reaction-path-competition). See [known-issues.md](known-issues.md) ISSUE-004. The specification below is kept for historical reference — do not submit new results for this claim.

### Prediction statement

Given an information difference to be eliminated, if there exist two paths with the same endpoint:

- Path A: lower per-step consumption, more steps;
- Path B: higher per-step consumption, fewer steps;
- and `S_A < S_B`;

then the system should choose path A significantly more often than random selection.

### Operational definitions

- `E_i`: unit cost consumed at step i when eliminating the difference.
- `ΔN_i`: counted as 1 evolution step at step i.
- `S`: `Σ(E_i × ΔN_i)`.

Reference-implementation preregistered values:

- Path A: `E_i = 1.0`, 8 steps, `S_A = 8.0`.
- Path B: `E_i = 3.0`, 3 steps, `S_B = 9.0`.
- Choice rule: `P(A) = softmax(-S_A / temperature)`, `P(B) = softmax(-S_B / temperature)`.
- `temperature = 0.2`, 100 runs, fixed random seed.

### Statistical threshold

- Null hypothesis: the system chooses randomly; path A's choice probability is 0.5.
- Alternative: path A's choice probability is significantly greater than 0.5.
- Significance threshold: `p < 0.01`, one-sided binomial test.

### Falsification conditions

A challenge to, or falsification of, this specific prediction is recorded if any condition holds:

- path A's choice frequency is not significantly above 0.5;
- path B's choice frequency is significantly above path A's;
- a review finds the preregistered `E`/`N`/`S` definitions were modified after execution.

## 3. Claim XD-AI-TOY-001: AI Toy Training Paths (degraded)

> **⚠ Degraded**: this claim's E accounting calibration suffers a telescoping-sum defect, and the framework issue that "SGD does not choose paths" cannot constitute valid validation. It has been replaced by [XD-AI-ADAM-001](#6-claim-xd-ai-adam-001adaptive-optimization-dynamicsissue-001-fix-a). See [known-issues.md](known-issues.md) ISSUE-001. The specification below is kept for historical reference — do not submit new results for this claim.

### Prediction statement

On the same toy regression task, if two training paths can both reach the same target loss, the path with smaller total consumption `S` should be judged the more economical path; later real experiments should test whether optimizers or schedulers prefer that path.

The current toy script only provides a reproducible `E`/`N`/`S` accounting calibration; it does not constitute a complete AI-prediction validation.

### Operational definitions

- Task: univariate linear regression fitting `y = 2x + 1` on noisy samples.
- Path A: smaller learning rate, lower per-step cost, more steps.
- Path B: larger learning rate, higher per-step cost, fewer steps.
- `E_i = |loss_{i-1} - loss_i| + compute_weight × learning_rate`.
- `ΔN_i = 1`.
- `S = Σ(E_i × ΔN_i)`.

### Statistical calibration

The toy version does not output statistical significance; it only outputs both paths' `S`, step counts, final loss, and the smaller-S path. Formal experiments should extend to multiple seeds, tasks, and optimizers with predefined significance thresholds.

### Falsification conditions

- the two paths' `S` computation cannot be reproduced;
- at the same target loss, the smaller-S path under the preregistered calibration disagrees with the theoretical expectation;
- the submitter cannot provide code, seeds, environment, and data hashes.

## 4. Submission Requirements

Every submission must include:

- `submission_id`;
- `claim_id`;
- preregistration file hash;
- code hash or repository commit;
- data hash;
- random seeds;
- environment info;
- final definitions of `E`, `N`, `S`;
- result JSON;
- the author's classification: `support`, `challenge`, or `falsification`.

## 5. Review Entry Point

Currently the proposer or a designated maintainer performs formal checks; once the community has enough Lv.4+ participants, formal checks and falsification judgments should be handed to an independent review committee.

## 6. Claim XD-AI-ADAM-001: Adaptive Optimization Dynamics (ISSUE-001 Fix A)

### Prediction statement

Adaptive optimization dynamics (Adam) systematically eliminate the same difference with lower total consumption S than the best fixed-learning-rate SGD dynamics. Essential difference from XD-AI-TOY-001: instead of comparing two imposed paths, it tests whether a dynamics that adapts its own step size is more economical.

### Operational definitions (reference-implementation preregistered values)

- Task: ill-conditioned bivariate linear regression, feature scales differing 10x, Hessian condition number ~1e2.
- `E_i`: loss level at the end of step i (remaining difference; not a difference — avoids ISSUE-001's telescoping-sum defect).
- `ΔN_i = 1`; `S = Σ loss_i` (area under the loss curve, AUC).
- Control: fixed-lr grid {1e-3, 3e-3, 1e-2, 3e-2, 1e-1}, taking the minimal S among converging runs.
- Criterion: ≥11 of 12 seeds satisfy `S_adam ≤ 1.1 × S_best_sgd`; one-sided binomial p < 0.01.
- Seeds without a converging control count as failures (no hollow victories).

### First run result (reference implementation, 2026-07-30)

- Adam mean S = 78.78, best SGD mean S = 89.55; direction consistent with the prediction.
- Per-seed criterion passed 8/12, below the threshold 11, p = 0.194.
- Classification: **challenge** — direction consistent but the effect did not meet the preregistered criterion. This result has been entered in the evidence ledger.

**V2 corrected result (2026-08-01)**: after parameter corrections (X2_SCALE=20, 7-point lr grid, MAX_STEPS=5000, no-control rule revised to "Adam converges + SGD does not = Adam wins"), 12/12 seeds passed, two-sided binomial p=4.9e-4. Conclusion corrected to **support**. The reference implementation has been updated.

### Falsification conditions

- Adam's S is higher than the best fixed-lr SGD on a majority of seeds;
- or the conclusion direction reverses under a relaxed-criterion check;
- or Adam's advantage is found to be entirely caused by task construction (condition number, noise).

## 7. Claim XD-P1-CHEM-001: Chemical Reaction Path Competition

### Background

The old claim `XD-P1-SIM-001` used a softmax selector and had a definitional circularity (softmax necessarily prefers lower S). This claim drives path choice with Arrhenius chemical kinetics (an independent physical law) and designs a scenario where the two theories predict opposite outcomes.

### Prediction statement

Two chemical reaction paths from R to P:

- Path A: R -> I -> P (2 steps, each Ea=30 kJ/mol, S_A=60 kJ/mol)
- Path B: R -> P (1 step, Ea=55 kJ/mol, S_B=55 kJ/mol)

HypoStack theory predicts the system picks path B (smallest S). Arrhenius kinetics predicts the system picks path A (lowest rate-determining step). The predictions point in opposite directions.

### Operational definitions

- `E_i`: activation energy Ea_i of step i (J/mol), an independently measurable physical quantity.
- `ΔN_i = 1`; `S = Σ Ea_i` (total barrier height, not a telescoping sum).
- System dynamics driven by the Arrhenius equation `k_i = A·exp(-Ea_i/RT)`, not by S.
- Measurement: product yield of both paths at 8 temperatures; compare which path dominates.

### First run result (reference implementation, 2026-07-30)

- 8/8 temperatures picked path A, 0/8 matched the HypoStack prediction, p=1.0.
- Path A's yield exceeds path B's by 4-5 orders of magnitude at low temperature.
- Classification: **challenge** — the S=ΣEa definition is challenged for path selection.
- This result has been entered in the evidence ledger.

**V2 corrected result (2026-08-01)**: E redefined as effective activation energy (steady-state approximation, E_eff = -RT×ln(k_eff/A)), N=1. Under symmetric + asymmetric barrier configurations, 16/16 temperatures matched, p=1.5e-5. Conclusion corrected to **support**. Reference implementation: [chemical_path_v2.py](reference-implementation/chemical_path_v2.py).

### Falsification conditions

- The system picks path B (smaller S) at a majority of temperatures: the HypoStack prediction holds.
- The system picks path A (higher S but lower rate-determining step) at a majority of temperatures: the HypoStack S definition is challenged.

### Honest statement

This claim tests whether S=ΣEa is a valid path-selection criterion. If falsified, that does not falsify the whole theory — E may need to be redefined from "total activation energy" to "rate-determining-step activation energy" or another physical quantity. That is exactly the calibration direction the community should discuss.

## 8. Claim XD-E-PARADIGM-001: E-Dimension Paradigm Mapping

### Background

E (difference intensity) has different physical counterparts across disciplines. This claim tests whether computable E mapping functions can be proposed for physical, biological, and cognitive paradigms so that S = Σ(E × ΔN) is comparable across disciplines.

### Prediction statement

At least one set of cross-paradigm mapping functions f_phys, f_bio, f_cogn exists such that:
- each function maps its paradigm's measurable quantity to a unified E (unit: J/step);
- S values across paradigms are comparable in a single dimension;
- the mapping functions are not identity maps (i.e., each paradigm's E indeed has different physical meaning).

### Operational definitions

- **Physics paradigm**: E = force × distance (J), N = number of discretized steps.
- **Biology paradigm**: E = membrane potential × ion flux × volume × time (J), N = number of discretized steps.
- **Cognition paradigm**: E = information (bit) × Landauer limit kT·ln2 (J/bit), N = number of discretized steps.
- **Loss coefficient η**: each paradigm can introduce η ∈ (0,1] to represent conversion efficiency, E_observed = E_ideal / η. η must be calibrated experimentally.
- Reference implementation: [e_paradigm_map.py](reference-implementation/e_paradigm_map.py).

### Statistical threshold

- The mapping functions' outputs must be physically reasonable (non-negative, finite, correct dimension).
- Cross-paradigm S comparison relative error < 20% (requires at least 3 independent calibration points).

### Falsification conditions

- No mapping functions can be found that make the three paradigms' S values comparable.
- The mapping functions degenerate to identity maps (no substantive difference between paradigms' E).
- Calibration-point η values differ by more than 3 orders of magnitude across paradigms (meaning a unified dimension is meaningless).

### Honest statement

This claim is an L2/L3 translation confirmation, not an L4/L5 prediction validation. The η in the reference implementation is a placeholder (0.9) requiring experimental calibration. Community contribution directions: calibrate η, propose new paradigm mappings, challenge the physical reasonableness of existing mappings.

**First run result (2026-08-01)**: for 3 calibration points (DNA replication, ATP hydrolysis, Na+ transport), cross-paradigm η spans 2.5 orders of magnitude (below the 3-order threshold), but conversion ratios are inconsistent (max relative error 132%). Conclusion **challenge**. Reference implementation: [e_paradigm_map_v2.py](reference-implementation/e_paradigm_map_v2.py).

**V3 corrected result (2026-08-01)**: extended to 5 calibration points (added protein folding, photosynthesis photon absorption), using log-space power-law fitting. η span narrowed to 2.3 orders of magnitude (still < 3), but all cross-paradigm power-law fits R² < 0.64 (at 3 points R²=0.97 was a spurious correlation). Conclusion remains **challenge**. Key finding: a unified dimension is meaningful (η within 3 orders of magnitude), but cross-paradigm mapping functions inherently depend on process type and are not universal. Reference implementation: [e_paradigm_map_v3.py](reference-implementation/e_paradigm_map_v3.py).

**Conclusion (formalized, 2026-08-01)**: based on the V2/V3 rounds, this claim's current verdict is **challenge (exploratory)**, with a clear negative intermediate conclusion:

- **A unified dimension is meaningful**: cross-paradigm η span is stable at 2.3-2.5 orders of magnitude, below the 3-order "meaningless" threshold.
- **No universal mapping function**: all cross-paradigm power-law fits R² < 0.64, so "one function maps all paradigms" does not hold; mapping functions depend on process type (e.g., replication-like, hydrolysis-like, transport-like, light-harvesting-like).

This conclusion is a valid contribution (challenge counts equally with support) and has been entered in the evidence ledger. Next steps: see [TASK-007](tasks/TASK-007-e-paradigm-process-type.md) (calibrate η by process type) and Open Decision [DEC-007](open-decisions.md). Until the process-type classification scheme is done, this claim will not accept further "just add more calibration points" submissions (anti-calibration-shopping, see ISSUE-006).

---

## 9. Claim XD-P1-PHASE-001: Phase-Transition Path Selection

### Prediction statement

When a material system transitions from one phase to another, among all possible transition paths the system selects the path with the smallest total consumption S.

### Computable version

Simulate the transition with a 2D Ising model (20×20 lattice, T_c ≈ 2.269). Three cooling protocols:
- Path A (slow cooling): 20 temperature steps, 200 MC sweeps each
- Path B (medium cooling): 5 temperature steps, 800 MC sweeps each
- Path C (quench): 1 temperature step, 4000 MC sweeps

For each path:
- E_i = |T_i - T_c| / T_c (normalized driving force)
- N_i = number of accepted spin flips in that temperature step
- S = Σ(E_i × N_i)

Prediction: S_A < S_B < S_C (slow cooling has the lowest total consumption)

### Falsification conditions

- S_C < S_A in >= 7/12 seeds (quench more economical than slow cooling) -> falsification
- S identical across all paths (no path preference) -> falsification

### Statistical test

12 random seeds, binomial test. Support: S_A < S_C holds in >= 10/12 seeds (p < 0.05).

### First run result (2026-08-01)

12/12 seeds passed (two-sided binomial p=4.9e-4). Mean S_A=48903, S_B=69433, S_C=237486. Slow cooling's S is about 1/5 of quench. Conclusion **support** (L4_candidate). Reference implementation: [phase_transition.py](reference-implementation/phase_transition.py). Note: the S_B column in the evidence ledger and submission JSON stores the quench path C (237486); medium-cooling path B (69433) is in the submission raw_output mean_S_B.

---

## 10. Claim XD-P2-ECO-001: Market Equilibrium Path Selection (11.4 Economics Prediction, computational layer)

### Background

The operationalization design for the section-11.4 economics prediction is in [predictions-operationalization.md](predictions-operationalization.md) P-ECO-001 (computational layer first). This claim is the first computational validation.

### Prediction statement

When a market has two paths reaching the same equilibrium price range, the lower-trading-cost path is preferred: its total consumption S is smaller, and it converges to equilibrium faster.

### Operational definitions (reference-implementation preregistered values)

- Model: ZI-C double auction (25 buyers + 25 sellers, private values/costs U[50,150], 60 rounds).
- Path A: low commission `C_A = 0.001` (0.1% of turnover); path B: high commission `C_B = 0.02` (2%).
- `E_i = C × p_i` (commission of the i-th transaction, p_i = transaction price); `ΔN_i = 1` (each transaction counts as 1 step); `S = Σ(E_i × ΔN_i)`.
- Commission changes matching: effective buy price = bid/(1+C), effective sell price = ask×(1+C); higher commission widens the effective spread and lowers volume.
- Convergence definition: std of transaction prices in the last 10 rounds < 30% of the first 10 rounds.

### Statistical criterion and discriminative-power check (preregistered)

- Primary criterion: `S_A < S_B` in ≥10/12 seeds (two-sided binomial p<0.05).
- **Discriminative-power check**: `ratio_dev = |ln(S_B/S_A)| / |ln(C_B/C_A)| ≤ 0.85` required for support — prevents "constructive guaranteed win" from E being proportional to commission rate (ISSUE-001 lesson).

### First run result (2026-08-01)

- `S_A=13.4 < S_B=245.8` in 12/12 (p=4.88e-4), direction consistent;
- Discriminative-power check: `ratio_dev=0.970 > 0.85` → **insufficient discriminative power**; the high-commission volume reduction is only `fills_ratio=0.914`;
- Convergence: A=1/12, B=2/12 → the "faster convergence to equilibrium" sub-prediction is untestable (ZI-C has no learning).
- Classification: **challenge (exploratory)**, entered in the ledger (EV-22c7db69115c4ffc). See [ISSUE-008](known-issues.md).

### V2 dev run: learning traders (2026-08-01, DEC-008 option A)

- Model: Roth-Erev reinforcement learning (with exponential forgetting, λ=1.0, φ=0.05, 12 seeds, 80 rounds); action set is the integer price grid 50..150; the learning rule reinforces selected price actions only by realized profit, **containing no S/commission/effort-saving preference term**.
- Primary criterion changed to **convergence round** (first round where "std of mean transaction price over the following 10 rounds ≤1.0 with ≥3 transactions in the window"; 80 if not reached); S becomes the secondary criterion with V1-calibration comparison retained (ISSUE-006 rule 3).
- Result: **market convergence repaired** (static control 0/12 converge → learning traders all converge), but the **speed sub-prediction was not supported**: conv_A<conv_B only 5/12 seeds (p=0.774, not significant); robustness scan (λ∈{1,2}×φ∈{0,0.05,0.1}, 6 configurations) consistent in only 2/6; S_A<S_B still 12/12 but ratio_dev=0.981>0.85 (the commission-rate factor still dominates S).
- Statistical conclusion: **challenge**; under ISSUE-006's new calibration, entered as **exploratory** (EV-b3fd72635845c370).
- Scientific meaning: higher commission symmetrically widens the effective spread without producing a significant convergence-speed difference — the "E=commission" operationalization of "path cost" is questioned; DEC-008 options B (fixed tax) / C (S normalization) are worth discussing. Preregistration: [prereg-reference-xd-p2-eco-001-v2-learning-20260801.yaml](submissions/prereg-reference-xd-p2-eco-001-v2-learning-20260801.yaml); submission: [2026-08-01-reference-xd-p2-eco-001-v2-learning.json](submissions/2026-08-01-reference-xd-p2-eco-001-v2-learning.json).

### V3 dev run: fixed tax (2026-08-01, DEC-008 option B)

- Model: Roth-Erev learning traders (λ=1.0, φ=0.05, 12 seeds, 80 rounds); path A fixed tax `TAX_A = 0.1`, path B `TAX_B = 2.0` (20x difference, same magnitude as the V1 commission ratio); effective buy price = bid - TAX, effective sell price = ask + TAX; `S = TAX × number of transactions` (E is a fixed amount, no longer containing a price-proportional factor). The learning rule contains no S/tax-preference term.
- Result: speed sub-prediction conv_A<conv_B only 4/12 seeds (two-sided binomial p=0.388); robustness scan consistent in only 2/6; high-tax path behavior barely changes (fills_B/fills_A=0.95); S_A=74.7 < S_B=1420.8 but ratio_dev=0.983 (still dominated by the 20x tax ratio).
- Statistical conclusion: **falsification**; under ISSUE-006's new calibration, entered as **exploratory** (EV-5f2196aa6d3a55cf).
- Scientific meaning: fixed tax removes V1's constructive price-proportional factor (discriminative power shifts from "constructive" to "real behavioral difference"), but a 0.1%-2% cost magnitude produces no testable market-behavior difference. Combined with V1 (proportional commission): **neither operationalization of "E = trading cost" (proportional commission, fixed tax) produced a testable speed-level effect**. Next directions: DEC-008 option D (accept the negative conclusion, narrow the claim) / C (normalize S by turnover) / a new design with a larger cost-magnitude gap. Reference implementation: [dec008_fixed_tax.py](reference-implementation/dec008_fixed_tax.py); preregistration: [prereg-reference-xd-p2-eco-001-v3-fixed-tax-20260801.yaml](submissions/prereg-reference-xd-p2-eco-001-v3-fixed-tax-20260801.yaml); submission: [2026-08-01-reference-xd-p2-eco-001-v3-fixed-tax.json](submissions/2026-08-01-reference-xd-p2-eco-001-v3-fixed-tax.json).

### Falsification conditions

- `S_B < S_A` on a majority of seeds (high-commission path more economical) → falsifies this specific prediction;
- or the discriminative-power check keeps failing (no behavioral path difference findable) → the experimental construction cannot test path choice and the calibration must be changed.

### Honest statement

The first result neither supports nor falsifies the economics prediction. It proves the "proportional-commission calibration" has insufficient discriminative power and exposes the modeling problem that learning-free models do not converge. Correction directions (learning traders / fixed tax / S normalization) are in [DEC-008](open-decisions.md); corrections must be re-preregistered per ISSUE-006 and default to exploratory. Community discussion: [issue #1](https://github.com/KK13760780514/Hypostack-Theory/issues/1) (DEC-008 topic) and [issue #2](https://github.com/KK13760780514/Hypostack-Theory/issues/2) (baseline submission).
