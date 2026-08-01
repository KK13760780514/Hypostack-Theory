# HypoStack 提交目录说明

把符合 `../submission-schema.json` 的结果 JSON 放在本目录。

建议命名：

```text
YYYY-MM-DD-<author>-<claim-id>.json
```

示例：

```text
2026-07-30-kimi-XD-P1-CHEM-001.json
```

文件名中的日期为实验执行（预注册）日期；`evidence-ledger.csv` 的 `timestamp_utc` 为提交校验日期，两者可能相差一天（如 2026-07-31 执行、2026-08-01 入库），属正常现象。

提交前必须完成：

1. 填写 `../preregistration-template.yaml`，并在实验前固定 `E`、`N`、`S` 和统计阈值。
2. 运行校验器：

```powershell
python ..\validate_submission.py .\your-submission.json
```

3. 如果校验通过，结果会被追加到 `../evidence-ledger.csv`。

负面结果、挑战结果、证伪结果都可以提交。不要只提交支持性结果。
