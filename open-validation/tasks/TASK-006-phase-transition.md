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

support (12/12, p=0.0002)。平均 S_A(慢冷)=48903 vs S_C(淬火)=237486。

## 如何参与

1. Fork 仓库
2. 运行 `python open-validation/reference-implementation/phase_transition.py`
3. 修改参数（格点大小、降温步数、温度范围）测试稳健性
4. 提交你的结果 JSON
