> [中文版本](p3-dimension-reduction.md) | English version

# Nine-Dimensional Coordinate Dimensionality-Reduction — Proposal Framework (Presupposition 3)

> Status: **proposal framework** (awaiting community claims; computation to run once data is ready)
> Related: [玄叠论.md](../玄叠论.md) §1.1 Presupposition 3 (nine-dimensional completeness / F·Φ·N strong coupling), §1.4 "cannot eliminate dimensional conflicts", §2.3 distance metrics, Appendix E (metric & geodesics), [math-foundations.en.md](math-foundations.en.md) Q5.
> This framework does not complete a dimensionality-reduction proof; it formalizes the test path, lists required data and acceptance criteria, for the community to execute once data is ready.

## 1. Current State of the Problem

Presupposition 3 asserts that all observable properties of a structure can be fully described by the nine coordinates `(F, S, E, N, R, Φ, K, Ξ, λ)`, and that no tenth irreducible property exists. The theory honestly states:

- `F / Φ / N` are strongly coupled; if they can be mutually derived, the nine coordinates can be reduced to seven or fewer;
- the reduction test path is already written into Presupposition 3: "compute variance contribution via PCA; if two dimensions' cumulative contribution exceeds a threshold, they can be merged";
- the nine dimensions have different units, currently mitigated with Mahalanobis distance / cosine similarity, but **the full manifold metric is not done** (Appendix E bounty).

**Current gap**: the above reduction test has no empirical data yet — nine-dimensional coordinates are currently annotated case-by-case by hand, lacking a sufficiently large, cross-type coordinate dataset to run PCA / manifold learning.

## 2. Goal

Once data is ready, test whether the reduction branch of Presupposition 3 holds, answering two sub-questions:

1. **Mergeability**: do any of the nine coordinates admit reconstruction (linear or nonlinear) from the rest? (i.e., is there reducible redundancy?)
2. **Completeness boundary**: do the current nine dimensions cover the observed variance of structural properties, or is there a significant "residual direction" suggesting a tenth irreducible property?

## 3. Test Paths (candidate routes)

### Route R1: PCA variance contribution (linear, specified by Presupposition 3)

- **Method**: run PCA on the standardized nine-dimensional coordinate matrix; compute per-component variance contribution.
- **Criterion (candidate threshold, adjustable)**: if two original dimensions can be reconstructed from the first k principal components with cumulative contribution ≥ 95%, judge them mergeable.
- **Limitation**: captures only linear correlation; if the `F/Φ/N` coupling is nonlinear it may be underestimated.

### Route R2: Correlation / redundancy analysis (pairwise dimensions)

- **Method**: compute the correlation matrix across the nine dimensions (Pearson / Spearman); identify pairs with high |ρ|.
- **Criterion (candidate)**: pairs with |ρ| ≥ 0.9 are "merge candidates", sent to Route R3 for nonlinear review.
- **Limitation**: linear-correlation threshold, and high correlation does not equal mutual derivability.

### Route R3: Nonlinear reconstruction / manifold learning

- **Method**: estimate intrinsic dimension with autoencoders / UMAP / kernel PCA; test whether the intrinsic dimension is well below 9.
- **Criterion (candidate)**: intrinsic dimension estimate ≤ 7 with reconstruction error < 5% supports "reducible".
- **Limitation**: depends on sample size and model choice; results must be cross-validated against R1/R2.

### Route R4 (counterexample-driven): the tenth-dimension challenge

- **Method**: a community member proposes a candidate "tenth irreducible property" and attempts to reconstruct it as a function `f(F,S,E,N,R,Φ,K,Ξ,λ)` of the nine.
- **Criterion**: if a feasible reconstruction exists, the property is not irreducible; if repeated attempts fail, Presupposition 3 needs revision.
- **Status**: this operationalizes the built-in falsification condition of Presupposition 3, complementing R1–R3.

## 4. Data Requirements

| Requirement | Description | Status |
|-------------|-------------|--------|
| Sample size | PCA / manifold learning suggest ≥ 100 structures (all nine dims); ideally ≥ 500 | **insufficient** (currently case-by-case manual annotation) |
| Coverage | cross structure types (physical / biological / cognitive / social / artificial), to avoid spurious reduction from a single type | insufficient |
| Annotation spec | each sample carries measurement paradigm, measurer ID, XRS mapping (see §2.5) | partially in place |
| Dimensionality handling | standardize / nondimensionalize first (linked to Appendix E metric and math-foundations Q5) | scheme to be unified |

**Conclusion**: reduction computation (R1–R3) is **currently blocked by insufficient data**. In the short term, the executable work is: refine the annotation spec and accumulate the dataset; R4 (tenth-dimension challenge) does not depend on big data and **can open now**.

## 5. Acceptance Criteria

- [ ] Dataset meets requirements (sample size, coverage, annotation spec per §4)
- [ ] At least R1 (PCA) and R2 (correlation) executed, results public
- [ ] If R1/R2 suggest reducibility, review with R3 nonlinear methods
- [ ] Conclusion is one of: ① report mergeable dimensions and reconstruction error; ② report no reducible redundancy found (nine dimensions retained)
- [ ] Any reduction conclusion must jointly assess impact on distance metrics (§2.3) and replication fidelity Δ_coord (§2.4)
- [ ] Negative results (cannot reduce / insufficient data to decide) are recorded as well

## 6. Relation to Existing Framework

- **Presupposition 3**: this framework operationalizes its reduction test path;
- **Appendix E metric**: a successful reduction changes the manifold dimension and must be coordinated with the metric derivation (see [math-foundations.en.md](math-foundations.en.md) §4);
- **Q5 dimensionality**: the pre-reduction standardization scheme is shared with Q5;
- **Evidence logging**: numerical results are logged per [submission-schema.json](submission-schema.json) as exploratory; conclusory proposals are reviewed via the DEC process.

## 7. Priorities and Contribution Routes

| Route | Difficulty | Data dependency | Priority |
|-------|-----------|-----------------|----------|
| R4 tenth-dimension challenge | low–medium | none (logical/constructive) | **high (do now)** |
| Annotation-spec refinement | low | none | high |
| R2 correlation analysis | low | medium (≥100 samples) | medium |
| R1 PCA | medium | medium–high | medium |
| R3 nonlinear reconstruction | high | high (≥500 samples) | low |

**How to contribute**: proposals, counterexamples, datasets, or numerical experiments on any route can open an issue (the [task-proposal template](../.github/ISSUE_TEMPLATE/task-proposal.md) works); numerical outcomes are logged via the open-validation flow, proposals reviewed via DEC. **Counterexamples are equally welcome** — constructing a "tenth dimension" that cannot be reconstructed from the nine is a direct challenge to Presupposition 3 and an important contribution.
