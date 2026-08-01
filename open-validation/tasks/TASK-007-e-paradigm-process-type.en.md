> [中文版本](TASK-007-e-paradigm-process-type.md) | English version

# TASK-007: Calibrate η by Process Type (E-Dimension Paradigm Conversion)

- Claim: `XD-E-PARADIGM-001`
- Difficulty: L3
- Type: paradigm conversion / data analysis
- Prerequisite conclusion: V2/V3 showed "no universal cross-paradigm conversion function", see [protocol-p1-ai.md](../protocol-p1-ai.md) section 8 and [ISSUE-007](../known-issues.md).

## Background

`XD-E-PARADIGM-001` produced power-law fits R² < 0.64 across all cross-paradigm pairs at 5 calibration points, showing that conversion functions depend on process type (replication, hydrolysis, transport, light harvesting, etc.) and are not universal. A common unit is still meaningful (η span 2.3 orders < 3).

## Goal

Test the new hypothesis "after grouping calibration points by process type, conversion is universal within a group":

- Group existing calibration points by process type;
- Re-run cross-paradigm mapping and power-law fitting within each group;
- If within-group R² is significantly higher than cross-group R² (e.g., > 0.8), the hypothesis gains support.

## Required Work

1. Provide a process-type classification criterion (operational, not subjective).
2. Run cross-paradigm mapping within each group and report within-group R².
3. Compare with cross-group R² and state whether the difference is significant (the statistical criterion must be preregistered).
4. Propose an extendable calibration-point expansion plan (at least 3 calibration points per group).

## Preregistration Requirements

Conclusions of this task enter the evidence ledger, so preregistration is **mandatory**:

- `E`, `N`, `S` definitions follow [protocol-p1-ai.md](../protocol-p1-ai.md) section 8;
- Preregister the statistical criterion: the difference threshold between mean within-group R² and cross-group R²;
- Fix the classification criterion and the calibration-point set before submitting.

## Acceptance Criteria

- Whether the within-group R² improvement is significant (per the preregistered criterion);
- The classification criterion must be reproducible and not adjusted after the fact (calibration-shopping protection, see ISSUE-006);
- Failure conditions must be reported (if within-group R² remains < 0.64, this supports the stricter conclusion that conversion functions are universal neither across paradigms nor within process-type groups).

## Deliverables

- Process-type classification criterion;
- Within-group vs. cross-group R² comparison table;
- Preregistered statistical criterion;
- Result JSON (per [submission-schema.json](../submission-schema.json), classification per the preregistered criterion).
