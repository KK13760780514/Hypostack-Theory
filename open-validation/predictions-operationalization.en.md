> [中文版本](predictions-operationalization.md) | English version

# Predictions Operationalization

> Related: [玄叠论.md](../玄叠论.md) §11.2/11.4/11.5 (currently labeled "testability status: to be operationalized").
> Purpose: upgrade qualitative case frameworks into **preregistrable** experimental designs (E/N/S definitions + statistical criteria), and clarify which parts are executable now vs. which require review by the respective disciplinary community.
> Status: **design document, not yet preregistered**. Any execution must preregister first (E/N/S and statistical thresholds locked before running).

## Principles

1. **Computational first**: build a fully reproducible simulation ("computation layer") as the first validation; real experiments are the long-term "empirical layer".
2. **E/N/S must have measurable or countable operational definitions**, otherwise no falsifiability is claimed.
3. **Each design lists the items requiring disciplinary community review** — we do not prescribe measurement conventions for biologists/economists.
4. Counterexamples and challenges are equally welcome.

---

## P-BIO-001: Cell differentiation path competition (§11.2)

### Current state

§11.2 "testability status": E (concentration gradient) has no unit and N (differentiation steps) has no counting scheme. The design resolves this in two layers.

### Computation layer (preregistrable now)

**Model**: gene regulatory network (GRN) driven bistable differentiation simulation (random Boolean network or simple ODE system) with two terminal states (e.g., neural vs. muscle lineage).

**Two paths**:
- Path A (stepwise): transitions through k intermediate regulatory states, low barrier per step;
- Path B (direct jump): reaches the terminal state in 1–2 steps, high barrier per step.

**Operational definitions**:
- `E_i` = transition barrier from regulatory state x_i to x_{i+1} (Boolean network: minimal number of flipped nodes to trigger the transition; ODE: minimal driving strength between two steady states);
- `ΔN_i = 1` (each regulatory state transition counts as one step);
- `S = Σ(E_i × ΔN_i)`.

**Prediction**: across multiple seeds, the progeny fraction entering each lineage favors the lower-S path; no preference when S is equal.

**Statistical criterion (example preregistration)**: ≥10/12 random initial-state seeds satisfy "progeny share of the lower-S path significantly > 0.5" (binomial, p < 0.05); counterexample: ≥4/12 seeds favor the higher-S path.

### Empirical layer (long-term, requires biology community review)

In vitro pluripotent stem cells + directed differentiation factors (low/high concentration). Items needing biologist confirmation: ① quantitative mapping from concentration gradient to transition barrier E; ② identification standard for intermediate-state count N (single-cell transcriptomic intermediate-state counting); ③ lineage-tracing experimental design.

### Items for community review

- Whether the choice of GRN model (Boolean vs. ODE) biases the conclusion;
- Whether E (minimal flip count vs. barrier height) is the most reasonable measure of differentiation cost.

---

## P-ECO-001: Market equilibrium path selection (§11.4)

### Current state

§11.4 "testability status": E (transaction cost) and N (equilibrium steps) lack measurement schemes. Economics is the **most operationalizable** of the three predictions — transaction cost has an explicit measure (commission), and steps are countable (trading rounds).

### Computation layer (preregistrable now)

**Model**: computational economics simulation — double auction market with adaptive traders (zero-intelligence + learning rules mix), fixed order flow.

**Two paths**: same initial non-equilibrium price distribution, two commission rates: path A low (e.g., 0.1%), path B high (e.g., 2%).

**Operational definitions**:
- `E_i` = commission cost of round i (precisely measurable, as a fraction of traded value);
- `ΔN_i` = number of matched trades in round i;
- `S = Σ(E_i × ΔN_i)`.

**Prediction**: both paths converge to the same equilibrium price band, but the low-commission path has smaller S and converges faster.

**Statistical criterion (example preregistration)**: ≥10/12 seeds satisfy "S_A < S_B and path A reaches the equilibrium neighborhood first" (binomial, p < 0.05).

### Computation-layer first run (2026-08-01, challenge/exploratory)

[double_auction.py](reference-implementation/double_auction.py) (ZI-C double auction) first run: S_A<S_B in 12/12 seeds (p=4.88e-4) matches the direction, but the discriminative-power check failed (`ratio_dev=0.970`; 97% of the S difference comes from the commission-rate factor), and the learning-free ZI-C market barely converges (the "converges faster" sub-prediction is untestable). See [ISSUE-008](known-issues.md) and [DEC-008](open-decisions.md). Fix directions: learning traders / fixed per-trade tax / S normalization. **This computation-layer design stays exploratory until a fix lands.**

### Empirical layer (fairly feasible, requires economics community review)

Human-subject laboratory experiments (z-tree/oTree double auction), commission rate as the controlled variable. E/N definitions carry over from the computation layer. Items for review: equilibrium definition (price-band threshold), number of traders, round cap.

### Items for community review

- Whether commission is a reasonable proxy for "per-step consumption" (does it miss search/information costs);
- The operationalization of equilibrium (price-convergence band width).

---

## P-ECO-002: Market "automatic switching" experiment (§11.4 second sub-prediction, choice/switching test)

### Motivation

The §11.4 prediction has two sub-predictions: ① the low-transaction-cost path is preferred (ranking test; P-ECO-001 has run V1~V3); ② **"if a policy intervention raises the transaction cost of one path, the market automatically switches to another path with lower total consumption"** (switching/choice test). Sub-prediction ② is the most direct operationalization of the theory's "choice" assertion (the "choice/switching test" form in the operational-definition note of 玄叠论.md's general experimental template); no claim covers it yet.

### Design (preregistration draft, pending community review)

**Model**: Roth-Erev learning traders in a double auction (based on [double_auction_learning.py](reference-implementation/double_auction_learning.py); the learning rule contains no S/cost preference term — switching must emerge from trading behavior itself, not from construction).

**Procedure**:

1. Phase 1 (t=1..T1): market runs on low-tax path A (TAX_A); learning traders converge to equilibrium;
2. Phase 2 (t=T1+1..T2): policy intervention — path A's tax rises to TAX_B (the former high-tax rate), path B's tax drops to TAX_A; traders keep learning;
3. Observation: does the market switch to the new low-tax path (measured by share of fills, prices, and profit-retention direction)?

**Operational definitions**:

- `E_i` = transaction cost of the path actually traded in round i (TAX_A or TAX_B);
- `ΔN_i` = number of fills in round i;
- `S = Σ(E_i × ΔN_i)`;
- **Switching indicator**: share of fills on the low-tax path in the last K rounds of phase 2, `p_low`, compared to the phase-1 baseline `p_low_base`.

**Prediction**: if "the market automatically switches to the lower-S path" holds, `p_low` after the intervention should exceed the pre-intervention baseline (agents aggregate toward the new low-tax path).

**Statistical criterion (example preregistration)**: ≥10/12 seeds satisfy `p_low(phase 2) > p_low_base + 0.15` (two-sided binomial p<0.05).

**Falsification condition**: ≤4/12 seeds satisfy the criterion — the "automatic switching" prediction is unsupported/falsified in this framework.

**Items for review**: intervention magnitude (TAX_A/TAX_B gap), phase lengths, switching-threshold choice, need for calibration on real data.

### Relationship to DEC-008

DEC-008 options D (accept the negative conclusion, narrow the claim) and C (normalize S per unit traded value) have been discussed. P-ECO-002 offers **option E (switching experiment)**: if ranking tests are untestable under both operationalizations (V1~V3), a switching test may provide direct evidence of "path choice at the behavior level", or falsify the prediction more thoroughly. This direction requires confirmation via the [DEC-008](open-decisions.md) community discussion before it is set up as a task.

---

## P-SOC-001: Institutional-change path dependence (§11.5)

### Current state

§11.5 honestly states: E (social mobilization/coordination cost) is not directly measurable, N (reform steps) is not countable, cross-country historical cases cannot be randomized, and there is no statistical design — **a qualitative case study, not claiming falsifiable testing**.

### Design conclusion

**This prediction does not enter the preregistration pipeline for the foreseeable future**, because:
1. E has no independent measurement proxy (fiscal expenditure ≠ mobilization cost, and cost structures are incomparable across regimes);
2. N has no unified counting standard ("reform steps" depend on the observer's institutional-granularity choice);
3. No control can be constructed (history is not repeatable).

**Future candidates** (re-evaluate only if):
- an E proxy comparable across regimes appears (e.g., a reform-legislation cost index);
- or a natural experiment (quasi-experimental design) provides comparable paths;
- only then design a preregistration.

**Current treatment**: retained as a theory-translation case (same class as Appendix M); excluded from the open-validation task list to avoid manufacturing a "non-falsifiable fake test".

---

## Priorities

| Design | Computation-layer difficulty | Empirical-layer feasibility | Suggestion |
|--------|-----------------------------|-----------------------------|------------|
| P-ECO-001 | medium (market simulation code needed) | higher (commission measurable) | **preferred first**, start at computation layer |
| P-BIO-001 | low–medium (GRN simulation) | medium (needs biology review) | second |
| P-SOC-001 | — | low | keep qualitative; do not launch |

**How to contribute**: open an issue to claim a computation-layer task ([task-proposal](../.github/ISSUE_TEMPLATE/task-proposal.md)); submit computation-layer results per [submission-schema.json](submission-schema.json) (classification per the preregistered criterion); challenges to the designs themselves (inappropriate E/N definitions) are equally welcome.
