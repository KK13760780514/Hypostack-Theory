# Call for Independent Replication · 独立复核召集书

> **HypoStack Theory（玄叠论）** — a falsifiable hypothesis about how differences drive the evolution of all systems.
> 一套关于差异如何驱动万物演化的可证伪理论假说。
> **这是开放科学验证邀请，不是理论推广。** 我们不邀请你相信，只邀请你检验。

## Why now · 为什么需要你

The theory's core claim is: systems preferentially follow paths that minimize the information action `S = ∫ E dN`.

核心断言：系统会偏好总消耗 `S = ∫ E dN` 最小的演化路径。

Currently, **all** existing results were produced by the proposer's reference implementation. No external researcher has independently replicated any of them. Evidence stays at `L4_candidate` until an independent replication confirms it — this is where you come in.

目前**全部**实验结果均由提出者的参考实现产出，尚无任何外部独立复核。证据等级停留在 `L4_candidate`，直到独立复核确认——这就是你入场的位置。

## What exists · 现有证据

| Claim | Result | p-value | Status |
|-------|--------|---------|--------|
| XD-P1-CHEM-001 | Reaction-path competition, 16/16 temps match | 1.5e-5 | support, L4_candidate |
| XD-AI-ADAM-001 | Adam vs best fixed-lr SGD, 12/12 seeds | 2.4e-4 | support, L4_candidate |
| XD-P1-PHASE-001 | 2D Ising phase transition, 12/12 seeds | 2.4e-4 | support, L4_candidate |
| XD-E-PARADIGM-001 | Cross-paradigm E conversion | — | challenge, exploratory |
| XD-P2-ECO-001 | ZI-C 12/12 direction-consistent (V1); learning traders speed 5/12 (V2); fixed-tax speed 4/12 (V3) | 4.9e-4 (V1) | challenge/exploratory (V1 ratio_dev=0.970; V2 EV-b3fd72635845c370; V3 EV-5f2196aa6d3a55cf) |

（全部记录见 [evidence-ledger.csv](open-validation/evidence-ledger.csv)）

## What we need · 我们需要什么

1. **Independent replication（独立复核）**：re-implement or independently run the three support experiments (`chemical_path_v2.py`, `adam_dynamics.py`, `phase_transition.py`), and report whether the result reproduces. Full workflow: [Independent Replication section](open-validation/README.en.md) / [独立复核章节](open-validation/README.md).
2. **Open decisions（开放决策）**：8 unresolved governance/calibration decisions (e.g., whether the Adam task is unfairly constructed, whether CHEM's N=1 is sound, how to handle ECO's insufficient discriminative power). Pick one: [open-decisions.md](open-validation/open-decisions.en.md) / [open-decisions.md](open-validation/open-decisions.md).
3. **Tasks（任务认领）**：[TASK-001..007](open-validation/tasks/) — new experiments, refutations, and engineering infrastructure.
4. **Math foundations（数学基础）**：the integral `S = ∫ E dN` lacks a measure-theoretic definition. Lowest-cost entry: numerical convergence checks ([math-foundations.md](open-validation/math-foundations.en.md) Q3).

## How · 如何参与

- **提交实验**：`validate_submission.py` + [submission-schema.json](open-validation/submission-schema.json)，支持与证伪结果同等入账。
- **提决策/任务**：用 [decision.md](.github/ISSUE_TEMPLATE/decision.md) 或 [task-proposal.md](.github/ISSUE_TEMPLATE/task-proposal.md) 模板开 issue。
- **预注册**：实验前固定 E/N/S 与统计阈值（[preregistration-template.yaml](open-validation/preregistration-template.yaml)），哈希 SHA-256。
- **防口径购物**：修改口径后新提交默认降级 exploratory（[ISSUE-006](open-validation/known-issues.md)）。

## Ground rules · 底线

- 支持、挑战、证伪结果**同等欢迎**——证伪单一预测只说明该预测失效，不等于整体理论被推翻。
- 不接受"证明整套理论"式任务；所有任务都要求有明确失败条件。
- 参考实现是启动版本，不是最终证明。

## Links · 入口

| 文档 | EN |
|------|----|
| [开放验证 README](open-validation/README.md) | [README.en](open-validation/README.en.md) |
| [开放决策清单](open-validation/open-decisions.md) | [Open Decisions](open-validation/open-decisions.en.md) |
| [已知问题](open-validation/known-issues.md) | — |
| [数学基础备忘录](open-validation/math-foundations.md) | [Math Foundations](open-validation/math-foundations.en.md) |
| [任务清单](open-validation/tasks/) | — |
| [证据账本](open-validation/evidence-ledger.csv) | — |
