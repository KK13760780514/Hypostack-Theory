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

### Empirical layer (fairly feasible, requires economics community review)

Human-subject laboratory experiments (z-tree/oTree double auction), commission rate as the controlled variable. E/N definitions carry over from the computation layer. Items for review: equilibrium definition (price-band threshold), number of traders, round cap.

### Items for community review

- Whether commission is a reasonable proxy for "per-step consumption" (does it miss search/information costs);
- The operationalization of equilibrium (price-convergence band width).

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
