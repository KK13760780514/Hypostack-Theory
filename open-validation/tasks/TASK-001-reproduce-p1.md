# TASK-001：复现 P1 增强版模拟

> **状态：历史任务，已被 TASK-005 取代。** ISSUE-004 证明 softmax 选择器存在定义性循环（softmax 必然偏好低 S）。修正方案已落地为 [TASK-005](TASK-005-chemical-path.md)，用 Arrhenius 化学动力学替代。本文件保留作历史记录。

- Claim: `XD-P1-SIM-001`
- 难度：L1-L2
- 类型：复现 / 稳健性检查

## 目标

复现参考实现 [p1_simulation.py](../reference-implementation/p1_simulation.py)，并检查路径选择是否仍然偏好 `S` 更小的路径。

## 必做项

1. 复制并填写 `../preregistration-template.yaml`。
2. 固定至少 3 组不同随机种子。
3. 在不修改预注册口径的前提下，记录 `S_A`、`S_B`、路径选择次数和 p 值。
4. 输出符合 `../submission-schema.json` 的 JSON，放入 `../submissions/`。

## 可选项

- 改变 `temperature`，观察选择概率是否仍由 `S` 主导。
- 增加 `runs`，检查统计结论是否稳定。
- 尝试让路径 B 的 `S` 更低，检查选择是否反转。

## 验收标准

- 预注册在实验前完成。
- `E`、`N`、`S` 定义没有实验后修改。
- 结果 JSON 通过 `validate_submission.py`。
- 负面结果同样提交。

## 交付物

- 预注册 YAML；
- 提交 JSON；
- 简短结论：支持 / 挑战 / 证伪 / 探索。
