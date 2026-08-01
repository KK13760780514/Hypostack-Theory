# HypoStack 开放验证 MVP

> [English version](README.en.md) | 中文版本

> 玄叠论（HypoStack Theory）的开放验证最小包。HypoStack = Hypothesis + Stack，意指差异叠加演化的理论假说。

**English:** HypoStack is a falsifiable hypothesis about how differences drive the evolution of all systems. The core claim: systems tend to select paths that minimize the cumulative information action `S = Σ(Eᵢ × ΔNᵢ)`, where `E` is the difference intensity and `N` is the discrete step count. This package lets external researchers run, reproduce, challenge, or falsify specific predictions — without reading the full theory.

目标：让外部研究者、工程师和数据科学家不需要先理解完整《玄叠论》，也能直接运行、复现、挑战或支持第一批可证伪预测。
当前 MVP 覆盖七个方向（含 2 个已降级）：

1. XD-P1-SIM-001：P1 softmax 模拟（已降级为口径演示，见 [known-issues.md](known-issues.md) ISSUE-004）。
2. XD-P1-CHEM-001：化学反应路径竞争--用 Arrhenius 动力学替代 softmax 循环，V2 结果为 support（L4_candidate）。
3. XD-AI-TOY-001：AI 玩具版训练路径（已降级为口径演示，见 [known-issues.md](known-issues.md) ISSUE-001）。
4. XD-AI-ADAM-001：自适应优化动态--Adam 自发训练动态的 S 是否低于最优固定学习率 SGD（V2 结果为 support，L4_candidate）。
5. XD-E-PARADIGM-001：E 维度范式转换--为物理、生物或认知范式提出可计算的转换函数。
6. XD-P1-PHASE-001：相变路径选择--2D Ising 模型慢冷 vs 淬火路径比较（首次结果为 support，L4_candidate）。
7. XD-P2-ECO-001：市场均衡路径选择--ZI-C 零智能约束交易者双向拍卖，佣金率 vs 固定税对比（V1/V2/V3 均为 challenge/exploratory——V3 falsification，见 [known-issues.md](known-issues.md) ISSUE-008）。

## 快速开始

### 运行参考实现（5 分钟体验）

```powershell
python .\open-validation\reference-implementation\chemical_path.py
python .\open-validation\reference-implementation\chemical_path_v2.py
python .\open-validation\reference-implementation\adam_dynamics.py
python .\open-validation\reference-implementation\e_paradigm_map.py
python .\open-validation\reference-implementation\e_paradigm_map_v2.py
python .\open-validation\reference-implementation\e_paradigm_map_v3.py
python .\open-validation\reference-implementation\phase_transition.py
python .\open-validation\reference-implementation\double_auction.py
python .\open-validation\reference-implementation\double_auction_learning.py
```

参考实现只使用 Python 标准库（3.9+），无需安装依赖。

### 查看当前证据

所有已提交的实验结果记录在 [evidence-ledger.csv](evidence-ledger.csv)。当前 5 个活跃 claim 均已有实验结果：3 个产出 support 结果（L4_candidate），2 个为 challenge（exploratory）--这不是失败，而是验证包正在暴露口径问题。

| claim_id | 分类 | 证据等级 | p 值 | S（选中路径） | S（对照路径） | 备注 |
|---|---|---|---|---|---|---|
| XD-AI-ADAM-001 | support | L4_candidate | 2.4e-4 | 188.5 (Adam) | 346.0 (最优 SGD) | V2: 12/12 种子通过；扩 lr 网格 + 无对照规则修订 |
| XD-P1-CHEM-001 | support | L4_candidate | 1.5e-5 | 31981.0 (路径 A) | 55000.0 (路径 B) | V2: 有效活化能；16/16 温度一致 |
| XD-E-PARADIGM-001 | challenge | exploratory | 无 | 1.04e-19 (物理) | 5.06e-20 (生物) | V3: 5 标定点；η 跨度 2.3 级；幂律 R²<0.64 |
| XD-P1-PHASE-001 | support | L4_candidate | 2.4e-4 | 48903 (慢冷) | 237486 (淬火) | 12/12 种子通过；2D Ising 相变 |
| XD-P2-ECO-001 | challenge | exploratory | 4.9e-4 (V1) | 13.4 (低佣金) | 245.8 (高佣金) | V1 12/12 方向符合但判别力不足（ratio_dev=0.970）；V2 学习型交易者速度子预测 5/12（p=0.774）；V3 固定税速度子预测 4/12（p=0.388，falsification）；两种交易成本操作化均未产出可检验效应，见 [ISSUE-008](known-issues.md)，讨论见 [issue #1](https://github.com/KK13760780514/Hypostack-Theory/issues/1) |

注意：以上结果全部由提出者的参考实现（reference-implementation）产出，尚无外部独立复核结果。

### 提交你的第一个实验（新贡献者路径）

1. **选任务**：推荐从 [TASK-005：化学反应路径竞争](tasks/TASK-005-chemical-path.md) 开始，它有完整的参考实现和明确的预测冲突。
2. **看示例**：参考 [example-p1-submission.json](example-p1-submission.json) 了解提交 JSON 的格式。
3. **填预注册**：复制 [preregistration-template.yaml](preregistration-template.yaml)，填入你的 E/N/S 定义和阈值。
4. **运行实验**：修改参考实现的参数，或用你自己的代码。
5. **生成提交 JSON**：按 [submission-schema.json](submission-schema.json) 格式生成结果文件，放入 `submissions/`。
6. **校验入账**：运行 `python .\open-validation\validate_submission.py 你的提交.json`，通过后自动追加到证据账本。

## 当前任务

- [TASK-001：复现 P1 增强版模拟](tasks/TASK-001-reproduce-p1.md)（历史任务，已被 TASK-005 取代）
- [TASK-002：压力测试 AI 玩具路径记账口径](tasks/TASK-002-stress-test-ai-toy.md)（历史任务，已被 TASK-004 取代）
- [TASK-003：提出 E 维度范式转换函数](tasks/TASK-003-e-dimension-paradigm-map.md)（参考实现 [e_paradigm_map.py](reference-implementation/e_paradigm_map.py)）
- [TASK-004：复现与挑战 Adam 自适应动态验证](tasks/TASK-004-adam-dynamics.md)
- [TASK-005：化学反应路径竞争验证](tasks/TASK-005-chemical-path.md)
- [TASK-006：相变路径选择验证](tasks/TASK-006-phase-transition.md)
- [TASK-007：按过程类型分类标定 η（E 维度范式转换）](tasks/TASK-007-e-paradigm-process-type.md)（由 ISSUE-007 结论立项）

## 贡献流程

1. 从 `tasks/` 中认领一个任务（当前推荐 TASK-005）。认领方式：在 Git 平台开 issue 标注任务编号，或直接提交结果。
2. 复制并填写 `preregistration-template.yaml`。
3. 在实验执行前固定四项内容：`E` 的测量范式、`N` 的计算方式、`S` 的计算方式、显著偏离的统计阈值。
4. 运行实验并保存代码版本、数据哈希、随机种子、环境信息。
5. 按 `submission-schema.json` 生成结果 JSON，放入 `submissions/`（参考 [example-p1-submission.json](example-p1-submission.json)）。
6. 运行 `validate_submission.py`，通过后自动追加到 `evidence-ledger.csv`。

## 生成预注册哈希

提交中的 `preregistration.hash` 是你预注册 YAML 文件的 SHA-256 值。生成命令：

```powershell
python -c "import hashlib; print(hashlib.sha256(open('你的预注册文件.yaml','rb').read()).hexdigest())"
```

把输出粘贴到提交 JSON 的 `preregistration.hash` 字段。`validate_submission.py` 会对该字段做格式与时间顺序检查（非 64 位 hex 或占位符会输出 warnings），但哈希是否与预注册文件一致属于评审环节的人工核查项——请妥善保存预注册 YAML 文件以便复核。

## 独立复核（复现现有结果）

当前 3 个 support 结果（XD-P1-CHEM-001、XD-AI-ADAM-001、XD-P1-PHASE-001）均由提出者的参考实现产出，**尚未有任何外部独立复核**。独立复核是证据从 `L4_candidate` 升级为 `confirmed` 的必要条件。复核流程：

1. 认领要复现的证据：在 [evidence-ledger.csv](evidence-ledger.csv) 中找到目标行，记录其 `evidence_id`（如 `EV-fadf8b4aca7d3ffd`）。
2. 自行实现或运行参考实现脚本（`reference-implementation/` 下的 `chemical_path_v2.py`、`adam_dynamics.py`、`phase_transition.py`），尽量使用你自己的实现或独立环境，不要直接信任参考脚本的输出。
3. 按 `submission-schema.json` 生成结果 JSON，与普通提交的区别：
   - 顶层加 `"replication_of": "<目标 evidence_id>"`（可选但强烈建议，用于在账本中追踪复核链）；
   - `author` 填写你自己的身份（不要用 `reference-implementation`）；
   - `classification` 按你的复现结果填写（复现成功 = `support`，与原文不符 = `challenge` 或 `falsification`）。
4. 运行 `validate_submission.py` 通过后入账。评审确认复核者与提出者非同一主体后，该行可升级为 `confirmed`。

**重要**：独立复核同样受预注册规则约束（提交前固定 E/N/S 与统计阈值，见 [preregistration-template.yaml](preregistration-template.yaml)）。复核者与原提交使用同一 claim 的预注册口径，不得临时修改口径以影响结果。

## 已知问题

见 [known-issues.md](known-issues.md)。当前最重要的开放问题：

- **ISSUE-004**：P1 softmax 选择器存在定义性循环，已用 XD-P1-CHEM-001 替代（V2 结果 support，L4_candidate）。
- **ISSUE-001**：AI 玩具路径 E 记账口径存在望远镜求和，已用 XD-AI-ADAM-001 替代（V2 结果 support，L4_candidate）。

两个修正后的 claim 已在 V2 产出 support 结果（L4_candidate），确认口径修正有效。剩余开放问题：口径选择（如条件数调整、无对照规则修订）是否引入偏差——欢迎社区讨论。

**最新进展**：XD-P1-CHEM-001 与 XD-AI-ADAM-001 的 V2 已修正为 support（L4_candidate），XD-P1-PHASE-001 首次运行即 support（L4_candidate），三者等待独立复核。同日新增经济学首个 claim XD-P2-ECO-001（V1 challenge/exploratory，EV-22c7db69115c4ffc）；V2 学习型交易者开发运行完成（challenge，EV-b3fd72635845c370）：市场可收敛性修复，但速度子预测未获支持（5/12，p=0.774）；V3 固定额税开发运行完成（falsification，EV-5f2196aa6d3a55cf）：速度子预测 4/12（p=0.388），两种交易成本操作化均未产出可检验效应，见 ISSUE-008。

## 评审与 issue 模板

- [评审清单](review-checklist.md)
- [提交结果 issue 模板](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=submission.md)
- [挑战或证伪 issue 模板](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=challenge-falsification.md)
- [新任务提案 issue 模板](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=task-proposal.md)

## 评审原则

- 支持性结果、挑战性结果、证伪性结果都接收。
- 预注册后禁止修改 `E`、`N`、`S` 和统计阈值。
- 单一预测被证伪不等于玄叠论整体被证伪；它只说明该特定条件下的预测失效。
- 当前参考实现只是启动版本，不是最终证明。

## 当前证据等级口径

- `L4_candidate`：按预注册完成，结果支持预测，等待独立复核。
- `L5_candidate`：按预注册完成，结果显著证伪该具体预测。
- `exploratory`：按预注册完成，结果为 challenge 或未达统计阈值，需进一步分析。
- `needs_review`：格式、统计或可复现性尚未通过检查。
- `degraded`：claim 本身已被降级（如 ISSUE-001/004），记录保留作历史参考。
