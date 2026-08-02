> [中文版本](README.md) | English version

# HypoStack Submission Directory Guide

Place result JSON files that conform to `../submission-schema.json` in this directory.

Suggested naming:

```text
YYYY-MM-DD-<author>-<claim-id>.json
```

Example:

```text
2026-07-30-kimi-XD-P1-CHEM-001.json
```

The date in the filename is the experiment execution (preregistration) date; the `timestamp_utc` in `evidence-ledger.csv` is taken from the `timestamp_utc` field in the submission JSON (the time filled in by the submitter in the submission JSON). The two may differ by one day (e.g., executed on 2026-07-31, entered into the ledger on 2026-08-01), which is normal.

The following must be completed before submitting:

1. Fill in `../preregistration-template.yaml`, and fix `E`, `N`, `S`, and the statistical threshold before the experiment.
2. Run the validator:

```powershell
python ..\validate_submission.py .\your-submission.json
```

3. If validation passes, the result is appended to `../evidence-ledger.csv`.

Negative results, challenge results, and falsification results can all be submitted. Do not submit only supportive results.
