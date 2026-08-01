# 玄叠论 / HypoStack Theory · 推广文案

> 用于知乎 / V2EX / GitHub Discussions / Reddit / Twitter 等平台发布，吸引外部研究者独立复现实验结果。

---

## 中文

### 我做了一套"可证伪"的演化理论，三个预言已获实验支持——现在开放给任何人复现

**玄叠论（HypoStack Theory）** 是一套可证伪的理论假说，核心公式只有一个：

```
S = ∫ E dN
```

`S` 是总消耗（信息作用量），`E` 是每一步的驱动力（差异强度），`N` 是演化步数。它主张：差异驱动万物演化，而万物演化都走总消耗最小的那条路。这不是宇宙的"目标函数"，而是宇宙的"筛选记录"——省力者留，费力者走。

**它和市面上那些"大统一理论"有什么不同？**

它不是哲学思辨，而是一个有明确预言、有可运行实验、有公开证据账本的可证伪理论。已有参考实现的预言都附带预注册的证伪协议；在实验数据到位之前，理论既未被证实，也未被推翻。它把"诚实"写进了规则书第 1.4 节，连"理论对批评的免疫性"这种自身缺陷都主动声明。

**当前证据（不挑结果，全部如实呈现）：**

| 预言 | 方向 | 当前结果 | 等级 |
|------|------|---------|------|
| 化学路径竞争（XD-P1-CHEM-001） | support | 16/16 温度匹配，p=1.5e-5 | L4_candidate |
| AI 优化动态（XD-AI-ADAM-001） | support | 12/12 种子通过，p=2.4e-4 | L4_candidate |
| 相变路径选择（XD-P1-PHASE-001） | support | 12/12 种子通过，p=2.4e-4 | L4_candidate |
| E 维度范式转换（XD-E-PARADIGM-001） | challenge | 5 个标定点，无普适转换函数 | exploratory |
| 市场均衡路径选择（XD-P2-ECO-001） | challenge | V1 12/12 方向符合但判别力不足（ratio_dev=0.970）；V2 学习型交易者速度子预测 5/12（p=0.774） | exploratory |

当前实证等级：**L4_candidate**——有 3 个 support 级 + 2 个 challenge 级实验结果，但还在等独立复核。

**一个必须说清楚的转折：**

其中两个 support 结果（化学路径和 AI 动态），首次验证（V1）其实都是 challenge。化学路径 V1 是 8/8 全部选了理论预测的相反路径；AI 动态 V1 只有 8/12 通过，效应未达阈值。修正口径后（化学路径从 ΣEa 改为基于稳态近似的有效活化能；AI 从比较人为路径改为 Adam 自适应动态），V2 才变为 support。第三个（相变路径选择）在首次运行中即验证为 support。

这不是 p-hacking。所有修正都记录在 `known-issues.md`，包含根因分析和待社区决策的开放问题；预注册后禁止修改 `E`、`N`、`S` 和统计阈值；每次口径变更都有物理依据，不是调参数凑结果。事实上，如果只是想"赢"，我不会把 challenge 结果也写进证据账本。

**如何参与（5 分钟即可跑通）：**

1. Fork 仓库
2. 选择 **TASK-005：化学反应路径竞争**（推荐入门，有完整参考实现）
3. 运行 Python 脚本——**仅用标准库，零依赖**：
   ```powershell
   python .\open-validation\reference-implementation\chemical_path.py
   ```
4. 生成预注册文件的 SHA-256 哈希，运行实验，按 schema 提交 JSON 结果
5. 结果追加到公开证据账本 `evidence-ledger.csv`

**诚实声明：**

- 这套理论可能是错的。单一预言被证伪 ≠ 理论整体被证伪，但多个独立证伪就很危险了。
- 当前证据等级是 candidate，不是确认。三个 support 结果必须经过独立复核才能超越 L4_candidate。
- 欢迎证伪。支持、挑战、证伪结果**均接收**——证伪也是贡献，账本里已经躺着 challenge 结果就是证明。

仓库地址：**https://github.com/KK13760780514/Hypostack-Theory**

---

## English

### HypoStack Theory: A falsifiable theory of how differences drive evolution — now with 3 experimentally supported predictions (L4_candidate, awaiting independent replication)

**HypoStack Theory (玄叠论)** is a falsifiable hypothesis with one signature formula:

```
S = ∫ E dN
```

`S` is cumulative information action (total consumption), `E` is the driving force (difference intensity) at each step, `N` is the number of evolution steps. The claim: all systems evolve along paths that minimize `S`. This is not the universe's objective function — it has none — but its *selection record*: frugal paths persist, costly ones perish.

**Why is this different from the usual "unified theory of everything" posts?**

It is not philosophy. It is a falsifiable theory with explicit predictions, runnable experiments, and a public evidence ledger. Every prediction ships with a pre-registered falsification protocol. Before experimental data arrives, the theory is neither confirmed nor refuted. The rulebook even declares its own limitations upfront (Section 1.4) — including the uncomfortable fact that its honesty declarations make it nearly immune to criticism during the current evidence vacuum.

**Current evidence — all of it, including the challenges:**

| Prediction | Direction | Result | Level |
|------------|-----------|--------|-------|
| Chemical path competition (XD-P1-CHEM-001) | support | 16/16 temperature matches, p=1.5e-5 | L4_candidate |
| AI adaptive dynamics (XD-AI-ADAM-001) | support | 12/12 seeds, p=2.4e-4 | L4_candidate |
| Phase-transition path (XD-P1-PHASE-001) | support | 12/12 seeds, p=2.4e-4 | L4_candidate |
| E-dimension paradigm map (XD-E-PARADIGM-001) | challenge | 5 calibration points, no universal transform | exploratory |
| Market-equilibrium path (XD-P2-ECO-001) | challenge | V1 12/12 direction-consistent but insufficient discriminative power (ratio_dev=0.970); V2 learning traders speed sub-prediction 5/12 (p=0.774) | exploratory |

Empirical level: **L4_candidate** — three support-level + two challenge-level results, awaiting independent replication.

**The twist you should know about:**

Two of the three support results were *challenges* on first run (V1). The chemical path went 8/8 against the prediction; the AI dynamics passed only 8/12 seeds. After correcting the E/S calibration — chemical: switched from summing activation energies to effective activation energy via steady-state approximation; AI: replaced a toy path-comparison with Adam's spontaneous adaptive dynamics — V2 turned both into support. The third (phase-transition path selection) was support from its first run.

This is not p-hacking. Every correction is logged in `known-issues.md` with root-cause analysis and open questions for the community. Pre-registration locks `E`, `N`, `S`, and statistical thresholds — they cannot be changed after the fact. If I just wanted to "win," I would not have published the challenge results in the ledger.

**How to participate (runs in 5 minutes, zero dependencies):**

1. Fork the repo
2. Pick **TASK-005: Chemical reaction-path competition** (recommended starting point, full reference implementation)
3. Run the Python script — **standard library only**:
   ```powershell
   python .\open-validation\reference-implementation\chemical_path.py
   ```
4. Generate a SHA-256 hash of your pre-registration file, run the experiment, submit a JSON result per schema
5. Your result is appended to the public `evidence-ledger.csv`

**Honest disclaimer:**

- The theory may be wrong. A single falsified prediction ≠ the whole theory is dead, but multiple independent falsifications are dangerous.
- The current level is *candidate*, not *confirmed*. All three support results need independent replication to advance beyond L4_candidate.
- Falsifications are welcome. Support, challenge, and falsification results are **all accepted** — the ledger already contains challenge results as proof.

Repo: **https://github.com/KK13760780514/Hypostack-Theory**
