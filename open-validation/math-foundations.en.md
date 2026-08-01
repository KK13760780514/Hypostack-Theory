> [中文版本](math-foundations.md) | English version

# Math Foundations — Open Problem Memo

> Status: **open problem** — contributions from mathematicians / mathematical physicists are welcome.
> Related: [玄叠论.md](../玄叠论.md) §1.4 "math foundations debt", Appendix E (metric and geodesic derivation, bounty for a full derivation), open decisions [open-decisions.md](open-decisions.md).
> This memo does not claim to complete a proof; it formalizes the problem, lists candidate routes and acceptance criteria, so the community can claim pieces of it.

## 1. Current State of the Problem

The core formula `S = ∫ E dN` is currently shorthand for the discrete sum `S = Σ(E_i × ΔN_i)`. The rulebook (§1.4) honestly states that its measure-theoretic definition and the integrability/existence of its continuum limit have **not been established**. All current validation experiments use the discrete computable version, so existing evidence does **not** depend on a strict continuum version — but the theory's mathematical standing remains unresolved.

## 2. Formal Statement of the Problem

Given:

- an evolution path: a finite or countable sequence of steps `{N_i}` (increasing stack count);
- a driving intensity per step `E_i` (a measurable quantity, e.g., activation energy, loss level, normalized temperature difference);
- step size `ΔN_i = N_{i+1} - N_i`.

Discrete definition: `S_path = Σ_i E_i × ΔN_i`.

To establish a continuum definition `S = ∫ E dN`, one must answer:

1. **Integrand object**: What spaces do `E` and `N` live in? (Is `E` a function of `N`, `E(N)`? Or a functional of the path `N(τ)`, `E[N(·)]`?)
2. **Measure**: What measure does `dN` correspond to? (A continuum analogue of the counting measure, a Lebesgue–Stieltjes measure, or a measure on path space?)
3. **Convergence**: Does the discrete sum `Σ(E_i ΔN_i)` converge under mesh refinement? Is it path-parameterization independent (Riemann property)?
4. **Minimization**: Is minimizing `∫ E dN` well-posed (solution exists, unique or at least nonempty)?

## 3. Core Open Sub-Problems

### Q1: Dependency structure of `E`

- **Problem**: In the physical analogy `E` corresponds to a Lagrangian density, depending on the configuration (positions/velocities) rather than the independent variable itself. What does `E_i` depend on in existing experiments? (CHEM: constant activation energy; ADAM: loss level `loss_i`; PHASE: normalized temperature difference `|T_i − T_c|/T_c`.)
- **Candidate route**: Formalize `E` as a functional on paths `N(t)` (`t` an external parameter), `E = E(N(t), dN/dt, t)`, so `S` becomes an action functional `∫₀ᵀ E(...) dN`, then study whether its Euler–Lagrange equations correspond to "layer-2 symmetry breaking".
- **Community entry**: Build the simplest computable model from ADAM (where `E = loss` has a known analytic form).

### Q2: Measure and integral type

- **Problem**: If `dN` corresponds to a counting measure (discrete steps), what is the measure in the continuum limit?
- **Candidate routes**:
  - Lebesgue–Stieltjes integral `S = ∫ E dN` (`N` as a monotone non-decreasing function, `dN` its Stieltjes measure) — reduces to `∫ E N'(t) dt` when `N` is absolutely continuous;
  - Path integrals (Wiener measure / Brownian-bridge analogy) — but the dependency structure of Q1 must be answered first;
  - Lattice limit: take the fine-graining limit of the discrete sum and test convergence (can be verified numerically first).
- **Community entry**: Run "step-size refinement convergence" numerical checks on the CHEM/PHASE reference data as the first minimal reproducible step.

### Q3: Discrete–continuum consistency

- **Problem**: Reference implementations all use the discrete definition. When does the continuum definition agree with the discrete one?
- **Candidate acceptance criterion**: For a given family of paths, there exists a sequence of mesh refinements under which `Σ(E_i ΔN_i)` converges; the limit is stable w.r.t. the path's "natural parameterization" (at least reproducible).
- **Numerical check**: Refine the temperature steps of phase_transition.py from 20 to 200/2000 and observe whether `S_A` converges — this is the **lowest-cost validation currently executable**, needing no theory derivation.

**Preliminary numerical evidence (2026-08-01, [phase_convergence.py](reference-implementation/phase_convergence.py))**: fixed total MC sweeps=4000, refined temperature steps n∈{2,5,10,20,50,100,200,400}, 12-seed means (seeds 0–11, strengthened run 2026-08-01):

| n_steps | mean S | std | ratio vs n=20 |
|---|---|---|---|
| 2 | 126741 | 585 | 2.59 |
| 5 | 69433 | 485 | 1.42 |
| 10 | 55447 | 493 | 1.13 |
| 20 | 48903 | 281 | 1.00 |
| 50 | 45254 | 433 | 0.925 |
| 100 | 43670 | 332 | 0.893 |
| 200 | 43293 | 344 | 0.885 |
| 400 | 43132 | 312 | 0.882 |

- Under mesh refinement S decreases monotonically and stabilizes: the 200→400 relative change is only **-0.37%** (<1%), and the step shrinks as the grid refines (100→200: -0.86%, 200→400: -0.37%), suggesting a continuum limit may exist.
- Cross-seed std is <1.3% at every grid point (e.g. n=400: 43132±312), indicating good seed stability.
- The n=20 reproduction (48903) matches the ledger mean (48903, <0.1%), confirming script reliability.
- **Honest reading**: S is still grid-dependent (n=20 vs n=400 differ by ~12%); "a continuum limit exists" is a numerical indication, not a proof. Whether the grid dependence affects the stability of path ordering (S_A<S_B<S_C), and the theoretical formalization of Q1/Q2, remain open. **External replicators with independent implementations and more seeds are welcome.**

### Q4: Well-posedness of the minimization

- **Problem**: Does `min_path ∫ E dN` have a solution? Is it unique? What is the mathematical statement of "the system selects the minimum-S path"?
- **Candidate route**: If `E` is path-history independent (CHEM case), `S = E_eff` (constant), and minimization degenerates to `min E_eff` — trivial; the interesting case is when `E` depends on path history (ADAM, PHASE), where the variational problem must be studied.
- **Caution**: A past lesson (ISSUE-001) — "the system chooses a path" cannot be validated by artificially constructed paths; the mathematical formalization must likewise not presuppose the existence of a minimizer.

### Q5: Dimensionality

- **Problem**: The nine dimensions have different units; what is the meaning of summing `E × N` products across dimensions?
- **Candidate route**: Solve jointly with Appendix E's nine-dimensional manifold metric (below). Until the metric exists, `∫ E dN` is strictly meaningful only within a single paradigm with unified units (e.g., J in the physical paradigm) — consistent with E-PARADIGM-001's finding (a common unit is meaningful, but cross-paradigm conversion functions are not universal).
- **Dimensionality reduction**: the operationalized test plan for Presupposition 3 (F/Φ/N strong coupling, reducible) is in [p3-dimension-reduction.en.md](p3-dimension-reduction.en.md).

## 4. Appendix E: Nine-Dimensional Manifold Metric — Starter Framework (Bounty, Community)

The full metric derivation is a separate bounty item ("Appendix E | metric and geodesic derivation (starter framework, bounty for a full derivation)"). Starter framework:

- **Goal**: Construct a metric tensor `g_ij` on the nine-dimensional manifold `M` (coordinates `(F,S,E,N,R,Φ,K,Ξ,λ)`) so that structure distances (e.g., Mahalanobis distance, cosine similarity) approximate geodesic distances on `M`.
- **Constraints**: The dimensions have different units → the metric must include physical unit conversion coefficients (or standardize to dimensionless coordinates first); `F/Φ/N` are strongly coupled (§1.1, Presupposition 3) — if they can be mutually derived, the manifold can be reduced in dimension.
- **Candidate routes**: Information geometry — treat each structure's nine coordinates as distribution parameters of some parametric family and use the Fisher information metric as `g_ij`; or data-driven — estimate the intrinsic metric via PCA / manifold learning on a large set of structure coordinates.
- **Acceptance criteria**: Consistency of geodesic distances under the metric with the replication fidelity `Δ_coord` in §2.4; consistency with the dimension-reduction check (PCA variance contribution).

## 5. Priorities and Contribution Routes

| Sub-problem | Difficulty | Lowest-cost entry | Priority |
|-------------|-----------|-------------------|----------|
| Q3 discrete–continuum consistency (numerical) | low | run refinement-convergence experiment, submit numerical report | **high (do first)** |
| Q2 measure type | medium | literature review + formalization proposal | medium |
| Q1 dependency structure of E | medium–high | build a minimal functional model from ADAM | medium |
| Q4 well-posedness | high | depends on Q1/Q2 | low |
| Q5 dimensionality / Appendix E metric | high | information-geometry review | low |

**How to contribute**: Proposals, counterexamples, or numerical experiments on any sub-problem can open an issue (the [task-proposal template](../.github/ISSUE_TEMPLATE/task-proposal.md) works) or follow the open-validation flow; numerical outcomes are logged per [submission-schema.json](submission-schema.json), theoretical outcomes are reviewed as proposal documents. **Counterexamples and falsifications are equally welcome** — if one proves "the discrete definition fails to converge under any natural continuum limit", that directly challenges the notational status of the core formula, which is an important contribution.
