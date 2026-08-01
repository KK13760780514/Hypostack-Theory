> [中文版本](README.md) | English version

# HypoStack Open Validation MVP

> The minimal open-validation package for HypoStack Theory (玄叠论). HypoStack = Hypothesis + Stack, referring to the theoretical hypothesis of difference-stacked evolution.

**English:** HypoStack is a falsifiable hypothesis about how differences drive the evolution of all systems. The core claim: systems tend to select paths that minimize the cumulative information action `S = Σ(Eᵢ × ΔNᵢ)`, where `E` is the difference intensity and `N` is the discrete step count. This package lets external researchers run, reproduce, challenge, or falsify specific predictions - without reading the full theory.

Goal: Enable external researchers, engineers, and data scientists to directly run, reproduce, challenge, or support the first batch of falsifiable predictions — without first understanding the complete HypoStack Theory.

The current MVP covers six directions (including 2 degraded):

1. XD-P1-SIM-001: P1 softmax simulation (degraded to a calibration demo, see [known-issues.md](known-issues.md) ISSUE-004).
2. XD-P1-CHEM-001: Chemical reaction path competition — uses Arrhenius kinetics instead of the softmax loop; V2 result is support (L4_candidate).
3. XD-AI-TOY-001: AI toy training path (degraded to a calibration demo, see [known-issues.md](known-issues.md) ISSUE-001).
4. XD-AI-ADAM-001: Adaptive optimization dynamics — whether Adam's spontaneous training dynamics yield lower S than optimally tuned fixed-lr SGD (V2 result is support, L4_candidate).
5. XD-E-PARADIGM-001: E-dimension paradigm mapping — propose computable conversion functions for physical, biological, or cognitive paradigms.
6. XD-P1-PHASE-001: Phase-transition path selection — 2D Ising model slow-cool vs. quench path comparison (first result is support, L4_candidate).

## Quick Start

### Run the Reference Implementation (5-minute experience)

```powershell
python .\open-validation\reference-implementation\chemical_path.py
python .\open-validation\reference-implementation\chemical_path_v2.py
python .\open-validation\reference-implementation\adam_dynamics.py
python .\open-validation\reference-implementation\e_paradigm_map.py
python .\open-validation\reference-implementation\e_paradigm_map_v2.py
python .\open-validation\reference-implementation\e_paradigm_map_v3.py
python .\open-validation\reference-implementation\phase_transition.py
```

The reference implementation uses only the Python standard library (3.9+), no dependencies required.

### View Current Evidence

All submitted experimental results are recorded in [evidence-ledger.csv](evidence-ledger.csv). All 4 active claims now have results: 3 classified as **support** at the **L4_candidate** level, and 1 as **challenge** (exploratory):

| claim_id | Classification | Evidence Level | p-value | S (selected) | S (alternative) | Notes |
|---|---|---|---|---|---|---|
| XD-AI-ADAM-001 | support | L4_candidate | 2.4e-4 | 188.5 (Adam) | 346.0 (best SGD) | V2: 12/12 seeds pass; expanded lr grid + no-baseline rule |
| XD-P1-CHEM-001 | support | L4_candidate | 1.5e-5 | 31981.0 (path A) | 55000.0 (path B) | V2: effective activation energy; 16/16 temps consistent |
| XD-E-PARADIGM-001 | challenge | exploratory | null | 1.04e-19 (physical) | 5.06e-20 (biological) | V3: 5 calibration points; eta span 2.3 orders; power-law R²<0.64 |
| XD-P1-PHASE-001 | support | L4_candidate | 2.4e-4 | 48903 (slow cool) | 237486 (quench) | 12/12 seeds pass; 2D Ising model phase transition |

### Submit Your First Experiment (New Contributor Path)

1. **Pick a task**: Recommended starting point is [TASK-005: Chemical Reaction Path Competition](tasks/TASK-005-chemical-path.md), which has a complete reference implementation and a clear prediction conflict.
2. **See an example**: Refer to [example-p1-submission.json](example-p1-submission.json) for the submission JSON format.
3. **Fill in preregistration**: Copy [preregistration-template.yaml](preregistration-template.yaml), fill in your E/N/S definitions and thresholds.
4. **Run the experiment**: Modify the reference implementation parameters, or use your own code.
5. **Generate submission JSON**: Generate a result file in [submission-schema.json](submission-schema.json) format, place it in `submissions/`.
6. **Validate and log**: Run `python .\open-validation\validate_submission.py your-submission.json`; once it passes, it is automatically appended to the evidence ledger.

## Current Tasks

- [TASK-001: Reproduce P1 Enhanced Simulation](tasks/TASK-001-reproduce-p1.md) (historical task, superseded by TASK-005)
- [TASK-002: Stress Test AI Toy Path Accounting Calibration](tasks/TASK-002-stress-test-ai-toy.md) (historical task, superseded by TASK-004)
- [TASK-003: Propose E-Dimension Paradigm Conversion Function](tasks/TASK-003-e-dimension-paradigm-map.md) (reference implementation [e_paradigm_map.py](reference-implementation/e_paradigm_map.py))
- [TASK-004: Reproduce and Challenge Adam Adaptive Dynamics Validation](tasks/TASK-004-adam-dynamics.md) (V2 result: support, L4_candidate; open for independent replication and criterion challenges)
- [TASK-005: Chemical Reaction Path Competition Validation](tasks/TASK-005-chemical-path.md) (V2 result: support, L4_candidate; open for independent replication and calibration challenges)
- [TASK-006: Phase-Transition Path Selection Validation](tasks/TASK-006-phase-transition.md) (V1 result: support, L4_candidate; open for independent replication)

## Contribution Workflow

1. Claim a task from `tasks/` (TASK-005 currently recommended). To claim: open an issue on the Git platform tagging the task number, or submit results directly.
2. Copy and fill in `preregistration-template.yaml`.
3. Before executing the experiment, fix four items: the measurement paradigm for `E`, the computation method for `N`, the computation method for `S`, and the statistical threshold for significant deviation.
4. Run the experiment and save code version, data hash, random seed, and environment info.
5. Generate the result JSON per `submission-schema.json`, place it in `submissions/` (see [example-p1-submission.json](example-p1-submission.json)).
6. Run `validate_submission.py`; once it passes, it is automatically appended to `evidence-ledger.csv`.

## Generate Preregistration Hash

The `preregistration.hash` in your submission is the SHA-256 value of your preregistration YAML file. Generate it with:

```powershell
python -c "import hashlib; print(hashlib.sha256(open('your-preregistration-file.yaml','rb').read()).hexdigest())"
```

Paste the output into the `preregistration.hash` field of your submission JSON. This hash proves that the preregistration content was not modified after the experiment.

## Known Issues

See [known-issues.md](known-issues.md). The most important currently open issues:

- **ISSUE-004**: The P1 softmax selector has a definitional circularity; replaced by XD-P1-CHEM-001 (V2 result: support, L4_candidate).
- **ISSUE-001**: The AI toy path E accounting calibration has a telescoping-sum flaw; replaced by XD-AI-ADAM-001 (V2 result: support, L4_candidate).

Both corrected claims now have V2 results classified as **support** at the **L4_candidate** level, confirming that the calibration fixes are effective. The remaining open questions concern whether the calibration choices (e.g., condition number adjustment, no-control rule revision) introduce bias — community discussion is welcome.

## Review and Issue Templates

- [Review Checklist](review-checklist.md)
- [Submission Result Issue Template](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=submission.md)
- [Challenge or Falsification Issue Template](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=challenge-falsification.md)
- [New Task Proposal Issue Template](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=task-proposal.md)

## Review Principles

- Supportive, challenging, and falsifying results are all accepted.
- After preregistration, modifying `E`, `N`, `S`, and statistical thresholds is prohibited.
- A single prediction being falsified does not mean HypoStack Theory as a whole is falsified; it only means that the prediction fails under that specific condition.
- The current reference implementation is a starting version, not a final proof.

## Current Evidence Level Calibration

- `L4_candidate`: Completed per preregistration; results support the prediction; awaiting independent replication.
- `L5_candidate`: Completed per preregistration; results significantly falsify the specific prediction.
- `exploratory`: Completed per preregistration; results are a challenge or did not reach the statistical threshold; further analysis needed.
- `needs_review`: Format, statistics, or reproducibility not yet checked.
- `degraded`: The claim itself has been degraded (e.g., ISSUE-001/004); records retained for historical reference.
