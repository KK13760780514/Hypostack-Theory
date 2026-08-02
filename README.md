# HypoStack Theory · 玄叠论

> **On the Evolution of Differences** — A falsifiable hypothesis about how differences drive the evolution of all systems.
>
> 关于差异如何驱动万物演化的可证伪理论假说。

**核心公式 / Core Formula:**

```
S = ∫ E dN
```

万物演化，都会选总消耗最小的那条路。`S` 是总消耗（信息作用量），`E` 是每一步的驱动力，`N` 是演化的步数。这不是宇宙的"目标函数"，而是宇宙的"筛选记录"——省力者留，费力者走。

*All systems evolve along paths that minimize the cumulative information action `S`. This is not a "goal function" of the universe, but its "selection record" — the cheap survive, the expensive fade.*

---

## 快速了解 / Quick Overview

| | |
|---|---|
| **协议版本** | v16.1.0 |
| **协议状态** | 开放，欢迎共建 |
| **许可证** | 文本 CC BY-SA 4.0 · 代码 MIT |
| **依赖** | Python 3.9+ 标准库，零依赖 |

## 仓库结构 / Repository Structure

```
Hypostack-Theory/
├── 玄叠论.md                    # 完整理论规则书（v16.1.0）
├── open-validation/             # 开放验证 MVP
│   ├── reference-implementation/  # 参考实现（16 个 Python 脚本，含 V2/V3）
│   ├── submissions/               # 已提交的实验结果
│   ├── tasks/                     # 验证任务清单
│   ├── evidence-ledger.csv        # 公开证据账本
│   ├── validate_submission.py     # 提交校验脚本
│   └── known-issues.md            # 已知问题与开放讨论
├── .github/ISSUE_TEMPLATE/      # GitHub Issue 模板
└── LICENSE                       # MIT
```

## 快速开始 / Quick Start

### 1. 运行参考实现（5 分钟体验）

```powershell
python .\open-validation\reference-implementation\chemical_path.py
python .\open-validation\reference-implementation\chemical_path_v2.py
python .\open-validation\reference-implementation\adam_dynamics.py
python .\open-validation\reference-implementation\e_paradigm_map.py
python .\open-validation\reference-implementation\e_paradigm_map_v2.py
python .\open-validation\reference-implementation\e_paradigm_map_v3.py
python .\open-validation\reference-implementation\phase_transition.py
```

### 2. 查看当前证据

所有实验结果记录在 [evidence-ledger.csv](open-validation/evidence-ledger.csv)。

当前 5 个活跃 claim 均已有实验结果：3 个 **support**（L4_candidate）+ 2 个 challenge：

| Claim | 方向 | 结果历史 | 状态 |
|-------|------|---------|------|
| XD-P1-CHEM-001 | 化学反应路径竞争 | V1 challenge → **V2 support** (16/16, p=1.5e-5) | L4_candidate |
| XD-AI-ADAM-001 | 自适应优化动态 | V1 challenge → **V2 support** (12/12, p=4.9e-4) | L4_candidate |
| XD-E-PARADIGM-001 | E 维度范式转换 | challenge（首次运行 3 标定点 → 扩展至 5 标定点，η 跨度 2.3 级，幂律 R²<0.64） | exploratory |
| XD-P1-PHASE-001 | 相变路径选择 | 首次运行即 **support** (12/12, p=4.9e-4) | L4_candidate |
| XD-P2-ECO-001 | 市场均衡路径选择 | V1 12/12 方向符合但判别力不足（ratio_dev=0.970）；V2 学习型交易者速度子预测 5/12（p=0.774）；V3 固定税速度子预测 4/12（p=0.388，falsification）；两种交易成本操作化均未产出可检验效应 | exploratory |

### 3. 提交你的第一个实验

详见 [开放验证 README](open-validation/README.md) 的「提交你的第一个实验」章节。推荐从 [TASK-005：化学反应路径竞争](open-validation/tasks/TASK-005-chemical-path.md) 开始。

## 当前验证任务 / Active Tasks

| 任务 | 方向 | 说明 |
|------|------|------|
| [TASK-003](open-validation/tasks/TASK-003-e-dimension-paradigm-map.md) | E 维度范式转换 | 提出可计算的转换函数 |
| [TASK-004](open-validation/tasks/TASK-004-adam-dynamics.md) | Adam 自适应动态 | 复现与挑战首次 challenge 结果 |
| [TASK-005](open-validation/tasks/TASK-005-chemical-path.md) | 化学路径竞争 | **推荐入门**，有完整参考实现 |
| [TASK-006](open-validation/tasks/TASK-006-phase-transition.md) | 相变路径选择 | 2D Ising 模型验证，首次结果 support |
| [TASK-007](open-validation/tasks/TASK-007-e-paradigm-process-type.md) | E 范式转换（过程类型） | 按过程类型分类标定 η，检验组内普适性 |

## 关键文档 / Key Documents

- [玄叠论.md](玄叠论.md) - 完整理论规则书
- [EN-ABSTRACT.md](EN-ABSTRACT.md) - 理论英文摘要
- [独立复核召集书](CALL-FOR-REPLICATION.md) — 面向外部研究者的复现邀请（中英双语）
- [传播文案 PROMOTION.md](PROMOTION.md) — 面向社区的分发文案（中英双语，含证据表）
- [贡献指南 CONTRIBUTING.md](CONTRIBUTING.md) — 贡献者须知
- [开放验证 README](open-validation/README.md) - 验证流程与贡献指南
- [已知问题](open-validation/known-issues.md) — ISSUE-001 / ISSUE-004 等开放讨论
- [证据账本](open-validation/evidence-ledger.csv) — 所有实验结果记录
- [评审清单](open-validation/review-checklist.md) — 提交评审标准

## 评审原则 / Review Principles

- 支持性结果、挑战性结果、证伪性结果**均接收**。
- 预注册后禁止修改 `E`、`N`、`S` 和统计阈值。
- 单一预测被证伪 ≠ 玄叠论整体被证伪；只说明该特定条件下的预测失效。
- 当前参考实现是启动版本，不是最终证明。

## 许可证 / License

- **理论文本**（`玄叠论.md` 及文档）：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **代码**（参考实现、校验脚本等）：[MIT](LICENSE)
