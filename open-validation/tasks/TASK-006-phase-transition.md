# TASK-006: 相变路径选择

**Claim ID**: XD-P1-PHASE-001
**学科**: 物理学
**难度**: 中
**状态**: 首次结果 support（L4_candidate），等待独立复现

## 预测

当物质系统从一种相态转变为另一种相态时，系统会选择总消耗 S = ∫ E dN 最小的路径。

## 实验方案

使用 2D Ising 模型模拟相变。三种降温协议（慢冷/中冷/淬火），计算每条路径的 S = Σ(|T_i - T_c|/T_c × N_flips_i)。预测 S_slow < S_quench。

## 参考实现

- 脚本: [phase_transition.py](../reference-implementation/phase_transition.py)
- 协议: [protocol-p1-ai.md 第 9 节](../protocol-p1-ai.md)

## 首次结果

support (12/12, p=4.9e-4)。平均 S_A(慢冷)=48903 vs S_C(淬火)=237486。

## 如何参与（独立复核路径）

> 独立复核同样受预注册规则约束（见 [README 独立复核节](../README.md#独立复核复现现有结果)）。复核召集见 [issue #13](https://github.com/KK13760780514/Hypostack-Theory/issues/13)。

1. Fork 仓库
2. **先预注册**：复制 `../preregistration-template.yaml`，固定 E/N/S 与统计判据（预测 `S_slow < S_quench`，参照原实现口径），生成真实 SHA-256 哈希
3. 独立实现或运行 `phase_transition.py`；若直接运行参考脚本，须使用与原提交不同的种子/参数网格（格点大小、降温步数、温度范围）并显式报告差异
4. 修改参数（格点大小、降温步数、温度范围）测试稳健性
5. 提交你的结果 JSON（经 `../validate_submission.py` 校验）——支持、挑战、证伪结果同等入库

## 验收标准

- 预注册在实验前完成，E/N/S 与判据不得事后修改（含"得到结果后调整判据使其通过"）
- 若直接运行参考脚本，须报告与原提交的参数差异，避免"无差异复跑即视为独立复核"
- 结果 JSON 通过 `validate_submission.py`；`preregistration.hash` 为真实 SHA-256
- 负面结果（未复现 `S_slow < S_quench`）同样提交
