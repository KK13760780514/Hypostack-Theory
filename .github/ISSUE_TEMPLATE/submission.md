---
name: "Validation submission"
about: "Submit a support, challenge, falsification, or exploratory validation result."
title: "[Submission] <claim-id> - <short title>"
labels: ["submission", "needs-form-check"]
---

## Claim / 声明

- claim_id:
- 相关任务 / Related task: TASK-003 / TASK-004 / TASK-005 / TASK-006 / 其他 / Other

## 预注册 / Preregistration

- 预注册文件 / Preregistration file:
- 预注册哈希 / Preregistration hash:
- 预注册时间 / Preregistration timestamp:
- 是否早于实验执行 / Before experiment execution: 是 / Yes · 否 / No

## 固定口径 / Fixed Calibration

- E 的测量范式 / E measurement paradigm:
- N 的计算方式 / N calculation method:
- S 的计算方式 / S calculation method:
- 统计阈值 / Statistical threshold:

## 实现 / Implementation

- 代码仓库/提交号 / Repository / commit:
- 代码哈希 / Code hash:
- 数据哈希 / Data hash:
- 随机种子 / Random seed:
- 环境 / Environment:

## 结果 / Results

- S_A:
- S_B:
- preferred_path:
- p_value:
- classification: support / challenge / falsification / exploratory

## 摘要 / Summary

用 5 句话以内说明结果。
Describe the result in 5 sentences or fewer.

## 自查 / Self-check

- [ ] 已通过 `validate_submission.py` / Passed `validate_submission.py`
- [ ] 已放入 `submissions/` / Placed in `submissions/`
- [ ] 已接受负面结果也可入库 / Negative results are accepted for the ledger
