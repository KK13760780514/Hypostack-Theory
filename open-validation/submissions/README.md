# 提交目录说明

把符合 `../submission-schema.json` 的结果 JSON 放在本目录。

建议命名：

```text
YYYY-MM-DD-<author>-<claim-id>.json
```

示例：

```text
2026-07-30-kimi-XD-P1-SIM-001.json
```

提交前必须完成：

1. 填写 `../preregistration-template.yaml`，并在实验前固定 `E`、`N`、`S` 和统计阈值。
2. 运行校验器：

```powershell
python ..\validate_submission.py .\your-submission.json
```

3. 如果校验通过，结果会被追加到 `../evidence-ledger.csv`。

负面结果、挑战结果、证伪结果都可以提交。不要只提交支持性结果。
