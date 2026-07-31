# HypoStack 已知问题与开放讨论点

本文件记录开放验证 MVP 中已发现但尚未解决的问题。这些问题不是需要被隐藏的缺陷，而是等待社区讨论和解决的开放议题。

## ISSUE-001：AI 玩具路径记账口径下 S_B < S_A

**状态**：修正 A 已采纳并落地（`XD-AI-ADAM-001`），首次验证结果为 challenge  
**影响 claim**：`XD-AI-TOY-001`（已降级）→ `XD-AI-ADAM-001`（新）  
**发现时间**：2026-07-30  
**分析时间**：2026-07-30  
**落地时间**：2026-07-30

### 问题描述

在 [ai_toy_path.py](reference-implementation/ai_toy_path.py) 当前记账口径下，路径 B（高学习率）的 S 略小于路径 A，与"低消耗路径被偏好"的预期表述方向不一致。

### 根因分析（参数扫描结论）

使用 [issue001_sweep.py](reference-implementation/issue001_sweep.py) 对 5 个学习率 × 6 个 compute_weight 做网格扫描，比较三种候选 E 定义，结论：

1. **当前口径 V0（`E_i = |Δloss| + cw·lr`）存在结构性缺陷，不是参数问题。**  
   `Σ|Δloss|` 是望远镜求和：对任何收敛路径，它都约等于 `loss_0 - loss_final`，与路径无关。扫描证实所有学习率下 S ≈ 3.04（初始 loss）。V0 的区分信号只来自 `cw·lr·steps` 这个任意项，区分能力极弱且不稳定。

2. **V1（固定步成本 `E_i = 1 + cw·lr`）区分能力强但单调。**  
   S ≈ 步数，总是偏好最大学习率。该口径下"最小作用量"退化为"最快收敛"，无法检验有意义的区分。

3. **V2（进展归一化 `E_i = cw·lr/|Δloss|`）同样单调偏好大学习率。**

4. **更深层的概念问题：玩具设置中"系统选择路径"不成立。**  
   SGD 不选择路径，学习率是人选的超参数。比较两条人为路径的 S，不能构成对"系统自发选择 S 最小路径"的验证。

### 候选修正方向（待社区决策）

- **修正 A（推荐先做）**：把 claim 从"比较人为路径"改为"自适应优化动态是否趋向低 S"——用自适应学习率方法（如 Adam、line search）观察自发训练动态，检验其 S 是否低于对照动态。
- **修正 B**：将 E 重定义为可测量的真实资源（FLOPs、wall-clock、能耗），使 S 成为可独立测量的总消耗，再检验收敛路径是否资源最优。
- **修正 C**：废弃 `XD-AI-TOY-001` 玩具版，直接按 [玄叠论.md](../玄叠论.md) 11.6 节设计正式多种子实验。

### 当前处理

- `ai_toy_path.py` 保留为 `exploratory` 标记的口径演示，不作为验证证据。
- [issue001_sweep.py](reference-implementation/issue001_sweep.py) 作为分析工具保留，供复核扫描结论。
- **修正 A 已落地**：[adam_dynamics.py](reference-implementation/adam_dynamics.py)，E_i 改用 loss 水平（AUC），比较 Adam 自适应动态与最优固定 lr SGD。
- 落地过程中发现并修复一个空洞胜利 bug：初版任务条件数过高（1e4）导致所有固定 lr 在 MAX_STEPS 内不收敛，对照缺失时阈值退化为无穷大而"自动成功"。修复：条件数降至 1e2、发散记有限惩罚值、无有效对照的种子计为失败。
- 首次正式运行结果：**challenge**（8/12 通过逐种子判据，阈值 11，p=0.194；Adam 平均 S=78.78 低于 SGD 的 89.55，方向一致但效应未达判据）。已入证据账本。
- 后续认领见 [TASK-004](tasks/TASK-004-adam-dynamics.md)。

## ISSUE-004：P1 softmax 选择器存在定义性循环

**状态**：已修正（XD-P1-CHEM-001 替代），旧 claim 降级  
**影响 claim**：`XD-P1-SIM-001`（已降级）-> `XD-P1-CHEM-001`（新）  
**发现时间**：2026-07-30

### 问题描述

[P1 模拟](reference-implementation/p1_simulation.py) 的选择规则是 `P(A) = softmax(-S_A / temperature)`。只要 S_A < S_B，softmax 就必然偏好 A。这不是"验证系统偏好低 S"，而是"定义了一个偏好低 S 的函数，然后发现它偏好低 S"。p ≈ 7.9e-31 的极端显著性正是这个循环的证明。

### 修正方案

创建 [chemical_path.py](reference-implementation/chemical_path.py)，用 Arrhenius 化学动力学（独立物理定律）驱动路径选择，并设计两个理论预测相反的场景：

- 玄叠论预测路径 B（S_B=55 < S_A=60）
- Arrhenius 预测路径 A（决速步 Ea=30 < 55）

### 首次结果

8/8 温度全部选路径 A，0/8 匹配玄叠论预测，p=1.0。结论：**challenge**。

这意味着 S=ΣEa 作为路径选择判据被挑战。可能的口径修正方向：E 应为决速步 Ea 而非总 Ea。后续认领见 [TASK-005](tasks/TASK-005-chemical-path.md)。

### 当前处理

- `p1_simulation.py` 降级为口径演示，不作为 L4 候选证据。
- `XD-P1-SIM-001` 的账本记录保留但标记为历史。
- 新 claim `XD-P1-CHEM-001` 的 challenge 结果已入账。

## ISSUE-002：预注册哈希生成门槛

**状态**：已解决  
**影响 claim**：所有

### 问题描述

外部贡献者可能不知道如何为预注册文件生成哈希值。

### 解决方案

已在 [README.md](README.md)「生成预注册哈希」一节补充命令与说明：

```powershell
python -c "import hashlib; print(hashlib.sha256(open('你的预注册文件.yaml','rb').read()).hexdigest())"
```

## ISSUE-003：多种子提交的格式支持

**状态**：已解决  
**影响 claim**：所有

### 问题描述

原始 schema 只支持 `seed` 为单个整数，但多种子实验需要传入种子列表。

### 解决方案

已更新 [submission-schema.json](submission-schema.json)，`seed` 字段现在支持 `integer` 或 `array of integers`。

## ISSUE-005：外部贡献者友好性不足

**状态**：已改善（持续）  
**影响 claim**：所有

### 问题描述

冷启动测试发现 README 和预注册模板对外部研究者不够友好：
1. 快速开始还列着已降级的 `p1_simulation.py`，而非 `chemical_path.py`。
2. 缺少"从零提交第一个实验"的逐步引导。
3. 没有指向示例提交和证据账本的链接。
4. 预注册模板缺字段说明和示例值。
5. 已知问题只提了 ISSUE-001，未提更重要的 ISSUE-004。

### 解决方案

- README 新增"提交你的第一个实验（新贡献者路径）"和"查看当前证据"两节。
- 预注册模板为每个字段加了中文注释和示例值。
- 贡献流程加入认领方式和示例提交链接。
- 已知问题更新为同时列出 ISSUE-001 和 ISSUE-004。

### 仍需解决

- 没有真正的 Git 远程仓库，外部人无法 fork 和 PR。
- 没有 CONTRIBUTING.md（贡献指南独立文件）。
- 没有中文/英文双语支持（当前全部中文）。
