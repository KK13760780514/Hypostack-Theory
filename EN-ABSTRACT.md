# 玄叠论（HypoStack Theory）英文理论摘要 / English Abstract with Chinese Translation

> 协议版本：v16.1.0 · 实证等级：L4_candidate · 许可证：CC BY-SA 4.0（文本）/ MIT（代码）
>
> 本文件基于 [玄叠论.md](玄叠论.md) 第 1.0–1.4 节与第 11 部分撰写，是理论的简明摘要，不是完整规则书。

---

## English

### 1. Abstract

HypoStack Theory (玄叠论) is a falsifiable hypothesis proposing that differences drive the evolution of all systems. Its core presupposition is that only information structures exist, and they persistently eliminate differences. Its signature formula is **S = ∫ E dN**, where S is the information action (cumulative consumption), E is the driving force (difference intensity), and N is the number of evolution steps. This is not the universe's objective function but its selection record—frugal paths persist, costly ones perish. Every prediction is independently testable; before experimental data arrives, the theory is neither confirmed nor refuted. Current empirical standing is **L4_candidate**, with two claims (CHEM-001, ADAM-001) revised from challenge to support after correcting E/S calibration and a third (PHASE-001) verified as support in its first run, awaiting community replication.

### 2. Core Formula

**S = ∫ E dN**

- **S** — the information action: the total consumption accumulated along an evolutionary path. It quantifies how much "effort" a structure expends to eliminate a difference.
- **E** — the driving force: the difference intensity at each step. It is not externally injected fuel but an intrinsic property of information structures—a determinism gradient. A perfectly uniform state has E = 0; any difference makes E > 0.
- **N** — the number of evolution steps: how many discrete operations the structure performs along the path.

This formula is the theory's signature—much as E = mc² is to relativity. It reveals the equivalence of "frugality" and "evolution": all evolution is a process of minimizing effort. Crucially, this is **not the universe's objective function**—the universe has no goal. It is the universe's **selection record**: frugal paths are retained, costly ones perish. What we perceive as "reward" is merely survivorship bias. The principle of least action in physics, natural selection in biology, and market equilibrium in economics are not analogies but special cases of this same formula at different scales.

### 3. Key Predictions

The theory issues six cross-disciplinary predictions (Section 11 of the rulebook), each with a designed falsification path; pre-registered falsification protocols exist for those with reference implementations (11.1 physics, 11.6 AI), while the others remain qualitative case frameworks awaiting operationalization:

1. **Physics — Phase-transition path selection.** When a system transitions between phases, it selects the path minimizing S. In supersaturated-solution crystallization, the path with lower total consumption is preferred. This is a specific application of the least-action principle; if verified, S = ∫ E dN is an equivalent expression of it.

2. **Biology — Cell-differentiation path competition.** A stem cell facing multiple differentiation fates selects the path minimizing S. Lower-concentration, gradual differentiation (lower per-step E) is preferred over high-concentration forced differentiation. This recasts cell-fate choice as a microscopic natural selection where S quantifies the selection criterion.

3. **Neuroscience — High-R cognitive welding: information-energy non-conservation.** When a structure's self-reference depth R exceeds a threshold, cognitive welding produces new information relations without proportional energy increase. The ratio ΔE_phys / ΔS_xuan is predicted to deviate significantly below the Landauer limit (kT ln 2 ≈ 2.97×10⁻²¹ J/bit at body temperature 310 K) for high-R tasks versus low-R tasks. This is a unique incremental prediction not made by systems theory, dissipative-structure theory, or structural realism.

4. **Economics — Market-equilibrium path selection.** When two paths to equilibrium exist, the lower-transaction-cost path is preferred. If policy raises the cost of one path, the market redirects to the lower-S alternative. Market equilibrium can be understood as the process of S = ∫ E dN approaching its minimum.

5. **Social science — Institutional-change path dependence.** Societies undergoing institutional transformation select the path minimizing S. When gradual reform (lower per-step E, more steps) and radical revolution (higher per-step E, fewer steps) lead to the same endpoint, the lower-S path is preferred. Path dependence is the cumulative effect of S = ∫ E dN on a historical scale.

6. **AI — Adaptive optimization dynamics.** The cumulative consumption S of an Adam-style adaptive optimizer eliminating a given difference is systematically lower than that of the best fixed-learning-rate SGD. In a pathological linear-regression setting (12 seeds, per-seed criterion S_adam ≤ 1.1 × S_best_sgd, ≥ 11/12 pass, one-sided binomial p < 0.01), Adam's spontaneous step-size adjustment is predicted to be more frugal.

### 4. Current Evidence

Current empirical level: **L4_candidate** (3 support-level experimental results, awaiting independent replication). Highest argument strength: L2 (post-hoc translation, 3 entries).

Two open-validation claims were revised from **challenge** to **support** after correcting the E/S calibration in validation round V2, and a third claim (PHASE-001) was verified as support in its first run:

- **XD-AI-ADAM-001** — Adaptive optimization dynamics. V1 (2026-07-30): challenge, direction correct but effect below threshold (8/12 seeds, p = 0.194). V2 (2026-08-01): **support**—12/12 seeds passed, p = 2.4e-4 (binomial). Adam mean S = 188.53 vs. best-SGD mean S = 345.97.
- **XD-P1-CHEM-001** — Chemical reaction-path competition. V1 (2026-07-30): challenge. V2 (2026-08-01): **support**—16/16 temperature matches, p = 1.5e-5. Preferred-path S = 31980.96 vs. alternative S = 55000.0.
- **XD-P1-PHASE-001** — Phase-transition path selection. V1 (2026-08-01): **support**—12/12 seeds passed, p = 2.4e-4 (binomial). Slow-cool S ≈ 48,903 vs. quench S ≈ 237,486.
- **XD-E-PARADIGM-001** — E-dimension paradigm transformation. V2 (2026-08-01): challenge (3 calibration points, η span 2.5 orders). V3 (2026-08-01): challenge (5 calibration points, η span 2.3 orders, power-law fits R² < 0.64; no universal conversion function). exploratory.

All results (3 support + 1 challenge) are logged in the public evidence ledger; all are reference-implementation self-validations and await community independent replication before advancing beyond L4_candidate.

### 5. How to Verify

All validation artifacts live in the [`open-validation/`](open-validation/) directory. There are **4 active claims** open for independent verification:

- **XD-P1-CHEM-001** — Chemical reaction-path competition ([TASK-005](open-validation/tasks/TASK-005-chemical-path.md))
- **XD-AI-ADAM-001** — Adaptive optimization dynamics ([TASK-004](open-validation/tasks/TASK-004-adam-dynamics.md))
- **XD-E-PARADIGM-001** — E-dimension paradigm transformation ([TASK-003](open-validation/tasks/TASK-003-e-dimension-paradigm-map.md))
- **XD-P1-PHASE-001** — Phase-transition path selection ([TASK-006](open-validation/tasks/TASK-006-phase-transition.md))

The reference implementations use **only the Python standard library (3.9+)**—no dependencies to install. To run them in five minutes:

```powershell
python .\open-validation\reference-implementation\chemical_path.py
python .\open-validation\reference-implementation\chemical_path_v2.py
python .\open-validation\reference-implementation\adam_dynamics.py
python .\open-validation\reference-implementation\e_paradigm_map.py
python .\open-validation\reference-implementation\e_paradigm_map_v2.py
python .\open-validation\reference-implementation\e_paradigm_map_v3.py
python .\open-validation\reference-implementation\phase_transition.py
```

Submission workflow: claim a task → fill the [preregistration template](open-validation/preregistration-template.yaml) → run the experiment → generate a submission JSON per [submission-schema.json](open-validation/submission-schema.json) → validate with `validate_submission.py` → results are appended to [evidence-ledger.csv](open-validation/evidence-ledger.csv). All submissions pass formal checks, pre-registration compliance, and review (an independent review committee is not yet formed; the proposer currently performs reviews, see the validation protocol).

### 6. Honesty Boundaries

The theory explicitly declares its own limitations (Section 1.4 of the rulebook). Honesty, it states, matters more than the appearance of completeness:

- **Cannot explain "why co-presence."** Presupposition Zero (at least two structures co-exist) is the irreducible logical starting point. Asking why co-presence exists is asking why relations exist rather than not—a question no relational ontology can answer.
- **Cannot prove information is the sole fundamental existence.** Material ontology and process ontology are equally self-consistent. Information is chosen as the basic category because it is the most convenient for cross-disciplinary translation—not because it is proven to be the universe's sole essence.
- **Cannot eliminate dimensional conflicts across the nine dimensions.** The nine dimensions have different units. Mahalanobis distance and cosine similarity only mitigate, not eradicate, the conflict. A full nine-dimensional manifold metric is required for a fundamental solution and is not yet complete.
- **Presuppositions cannot be directly falsified.** Presuppositions One through Four are derivation starting points. They can only be tested indirectly through the predictive accuracy of their corollaries—if all predictions fail, the theory loses scientific value.
- **Not a neutral tool.** The theory is not neutral; it presupposes information ontology. If you do not accept this presupposition, the theory has no meaning for you.
- **Immunity to criticism.** The theory pre-places honest declarations at every potential defect, making it nearly impossible to overturn during the current empirical vacuum—any criticism can be absorbed by "honesty." This is a design side effect, not the intent.
- **Layered protection of presuppositions.** The five presuppositions bear different falsification risks. Presupposition Zero is permanently protected; Presupposition Three's falsification threshold is raised (challengers must construct the function themselves). The theory can only be challenged from Presupposition Four (emergence) or the corollary layer.
- **Governance parasitism.** The theory cannot operate independently of community governance—falsification, presupposition-overturn, benchmark replacement, and version iteration all depend on community voting.
- **Non-independence of translation verification.** Translation accuracy is confirmed by domain experts, but they have already been exposed to the nine-dimensional coordinate system; this is peer review, not fully independent third-party verification.
- **Infinite regression of evolution.** v16.1.0 is not the endpoint. By the theory's own evolutionary logic, the next diagnostic will reveal new defects—this is statistical inevitability, not prediction.

---

## 中文

### 1. 摘要

玄叠论（HypoStack Theory）是一套可证伪的理论假说，主张差异驱动万物演化。其核心预设是：宇宙中只有信息结构在消除差异。标志性公式为 **S = ∫ E dN**，其中 S 是信息作用量（总消耗），E 是驱动力（差异强度），N 是演化步数。这不是宇宙的目标函数，而是宇宙的筛选记录——省力者留，费力者走。每一个推论都在等待独立的实验检验；在实验数据到位之前，理论既未被证实，也未被推翻。当前实证等级为 **L4_candidate**，两个 claim（CHEM-001、ADAM-001）在修正 E/S 口径后从 challenge 修正为 support，第三个 claim（PHASE-001）在首次运行中即验证为 support，等待社区独立复核。

### 2. 核心公式

**S = ∫ E dN**

- **S** —— 信息作用量：沿一条演化路径累积的总消耗。它量化了一个结构消除差异所耗费的"力"。
- **E** —— 驱动力：每一步的差异强度。它不是外部注入的燃料，而是信息结构的内在属性——确定性梯度。完全均匀的状态 E = 0；任何差异出现则 E > 0。
- **N** —— 演化步数：结构沿路径执行的离散操作次数。

这个公式是玄叠论的标志性公式——就像 E = mc² 之于相对论。它揭示的是"省力"和"演化"的等价性：万物演化，就是万物在省力。关键在于，这**不是宇宙的"目标函数"**——宇宙没有目标。它是宇宙的**"筛选记录"**：省力者留，费力者走。我们看到的"奖励"，只是幸存者偏差。物理学的最小作用量原理、生物学的自然选择、经济学的市场均衡——它们不是类比，而是同一个公式在不同尺度上的特例。

### 3. 关键预言

理论发布了六个跨学科预言（规则书第 11 部分），每个预言都设计了证伪路径；其中已有参考实现的预言（11.1 物理学、11.6 AI）附带预注册的证伪协议，其余仍为待操作化的定性案例框架：

1. **物理学——相变路径选择。** 物质系统相变时，会选择总消耗 S 最小的路径。在过饱和溶液结晶实验中，系统优先选择总消耗更低的路径。这是最小作用量原理的具体应用；若被验证，则 S = ∫ E dN 是该原理的等价表达。

2. **生物学——细胞分化路径竞争。** 干细胞面临多种分化方向时，会选择总消耗 S 最小的路径。低浓度逐步分化（每步 E 较低）优于高浓度强制分化。这将细胞命运选择重述为一场微观自然选择，S 量化了筛选标准。

3. **神经科学——高 R 认知焊接的信息-能量非守恒。** 当结构的自视深度 R 超过阈值时，认知焊接可在不消耗等比例物理能量的情况下产生新信息关系。预测高 R 任务的 ΔE_phys / ΔS_xuan 比值显著低于兰道尔极限（kT ln 2 ≈ 2.97×10⁻²¹ J/bit，体温 310K）。这是系统论、耗散结构论、结构实在论均不会做出的独有增量预测。

4. **经济学——市场均衡路径选择。** 当两条达到均衡的路径并存时，交易成本更低的那条被优先选择。若政策提高了某条路径的成本，市场会转向总消耗更小的替代路径。市场均衡可理解为 S = ∫ E dN 趋近最小值的过程。

5. **社会科学——制度变迁的路径依赖。** 社会制度变革时选择总消耗 S 最小的路径。当渐进式改革（每步 E 较低、步数较多）与激进式革命（每步 E 较高、步数较少）终点相同时，社会倾向选择 S 更小的路径。路径依赖是 S = ∫ E dN 在历史尺度上的累积效应。

6. **AI——自适应优化动态。** Adam 式自适应优化器消除同一差异的总消耗 S，系统性低于最优固定学习率 SGD。在病态线性回归设置中（12 个种子，逐种子判据 S_adam ≤ 1.1 × S_best_sgd，≥ 11/12 通过，单侧二项 p < 0.01），预测 Adam 的自发步长调节更省力。

### 4. 当前证据

当前实证等级：**L4_candidate**（已有 3 个 support 级实验证据，等待独立复核）。最高论据强度：L2（事后翻译，共 3 条）。

两个开放验证 claim 在 V2 轮次修正 E/S 口径后，从 **challenge** 修正为 **support**，第三个 claim（PHASE-001）在首次运行中即验证为 support：

- **XD-AI-ADAM-001** —— 自适应优化动态。V1（2026-07-30）：challenge，方向正确但效应未达阈值（8/12 种子，p = 0.194）。V2（2026-08-01）：**support**——12/12 种子通过，p = 2.4e-4（二项检验）。Adam 平均 S = 188.53，最优 SGD 平均 S = 345.97。
- **XD-P1-CHEM-001** —— 化学反应路径竞争。V1（2026-07-30）：challenge。V2（2026-08-01）：**support**——16/16 温度匹配，p = 1.5e-5。优选路径 S = 31980.96，对照路径 S = 55000.0。
- **XD-P1-PHASE-001** —— 相变路径选择。V1（2026-08-01）：**support**——12/12 种子通过，p = 2.4e-4（二项检验）。慢冷 S ≈ 48,903，淬火 S ≈ 237,486。
- **XD-E-PARADIGM-001** —— E 维度范式转换。V2（2026-08-01）：challenge（3 标定点，η 跨度 2.5 个数量级）。V3（2026-08-01）：challenge（5 标定点，η 跨度 2.3 个数量级，幂律拟合 R² < 0.64，无普适转换函数）。exploratory。

所有结果（3 个 support + 1 个 challenge）均已录入公开证据账本；全部为参考实现自验证，等待社区独立复核后方可超越 L4_candidate 等级。

### 5. 如何验证

所有验证产物位于 [`open-validation/`](open-validation/) 目录。当前有 **4 个活跃 claim** 等待独立验证：

- **XD-P1-CHEM-001** —— 化学反应路径竞争（[TASK-005](open-validation/tasks/TASK-005-chemical-path.md)）
- **XD-AI-ADAM-001** —— 自适应优化动态（[TASK-004](open-validation/tasks/TASK-004-adam-dynamics.md)）
- **XD-E-PARADIGM-001** —— E 维度范式转换（[TASK-003](open-validation/tasks/TASK-003-e-dimension-paradigm-map.md)）
- **XD-P1-PHASE-001** —— 相变路径选择（[TASK-006](open-validation/tasks/TASK-006-phase-transition.md)）

参考实现**仅使用 Python 标准库（3.9+）**，无需安装任何依赖。五分钟内即可运行：

```powershell
python .\open-validation\reference-implementation\chemical_path.py
python .\open-validation\reference-implementation\chemical_path_v2.py
python .\open-validation\reference-implementation\adam_dynamics.py
python .\open-validation\reference-implementation\e_paradigm_map.py
python .\open-validation\reference-implementation\e_paradigm_map_v2.py
python .\open-validation\reference-implementation\e_paradigm_map_v3.py
python .\open-validation\reference-implementation\phase_transition.py
```

提交流程：认领任务 → 填写[预注册模板](open-validation/preregistration-template.yaml) → 运行实验 → 按 [submission-schema.json](open-validation/submission-schema.json) 生成提交 JSON → 运行 `validate_submission.py` 校验 → 结果自动追加到 [evidence-ledger.csv](open-validation/evidence-ledger.csv)。所有提交经过形式检查、预注册合规检查和评审（独立评审委员会尚未组建，当前由提出者执行，见开放验证协议）。

### 6. 诚实边界

理论明确宣告自身的局限（规则书第 1.4 节）。它声明：诚实地说出来，比假装能做到更重要：

- **无法解释"为何共在"。** 预设零（至少存在两个结构）是不可还原的逻辑起点。追问"为何共在"等于追问"为何存在关系而非不存在关系"——任何关系本体论都无法回答。
- **无法证明"信息是唯一的基本存在"。** 物质本体论、过程本体论同样自洽。选择信息作为基本范畴，是因为它在跨学科翻译上最便利——不是因为它被证明是宇宙的唯一本质。
- **无法消除多维度量衡的量纲冲突。** 九个维度量纲各不相同。马氏距离和余弦相似度只是缓解，不是根除。唯一根本性的解决方案是建立完整的九维流形度规，目前尚未完成。
- **预设不可被直接实验推翻。** 预设一至预设四是理论推导的起点，只能通过推论的预测准确性间接检验——如果所有预测全部落空，理论即失去科学价值。
- **不是中立的工具。** 这套理论不中立，它预设了信息本体论。如果你不接受这个预设，它对你没有意义。
- **理论对批评的免疫性。** 理论在每一处可能存在缺陷的地方都预先放置了诚实声明，使其在当前实证空白阶段几乎无法被推翻——任何批评都可被"诚实"所吸收。这是设计的实际效果，而非初衷。
- **预设的分层保护。** 五个预设承担不同的证伪风险。预设零被永久保护；预设三的证伪门槛已被抬高（挑战方需自行构造函数）。理论只能从预设四（涌现）或推论层入手推翻。
- **治理对理论的寄生性。** 理论目前无法脱离社区治理独立运作——证伪流程、预设推翻、基准替换、版本迭代全部依赖社群投票。
- **翻译检验的非独立性。** 翻译准确性由原领域专家确认，但专家在确认时已接触九维坐标的概念体系；这是同侪评审，不是完全独立的第三方检验。
- **无限回归的演化宿命。** v16.1.0 不是终点。按理论自身的演化规律，下一次诊断必然发现新的缺陷——这是统计必然，不是预测。
