# 贡献指南 / Contributing Guidelines

> HypoStack Theory（玄叠论）是一个关于差异如何驱动万物演化的可证伪理论假说。核心公式：`S = ∫ E dN`，其中 `E` 是每一步的差异强度，`N` 是离散步数，`S` 是累计信息作用量。本仓库提供开放验证 MVP，包含 5 个活跃 claim，欢迎外部研究者参与运行、复现、挑战或证伪。
>
> *HypoStack Theory is a falsifiable hypothesis about how differences drive the evolution of all systems. Core formula: `S = ∫ E dN`, where `E` is the difference intensity per step, `N` is the discrete step count, and `S` is the cumulative information action. This repository provides an open-validation MVP with 5 active claims. External researchers are welcome to run, reproduce, challenge, or falsify them.*

当前活跃 claim / Active claims:

| Claim ID | 方向 / Direction |
|----------|------------------|
| `XD-P1-CHEM-001` | 化学反应路径竞争 / Chemical path competition |
| `XD-AI-ADAM-001` | Adam 自适应动态 / Adam adaptive dynamics |
| `XD-E-PARADIGM-001` | E 维度范式转换 / E-dimension paradigm shift |
| `XD-P1-PHASE-001` | 相变路径选择 / Phase transition path selection |
| `XD-P2-ECO-001` | 市场均衡路径选择 / Market equilibrium path selection |

---

## 1. 如何参与 / How to Contribute

### 中文

欢迎任何背景的贡献者。你可以通过以下四种方式参与，所有方式均通过 GitHub Issue 发起：

1. **提交验证结果**：对某个活跃 claim 运行实验，提交支持（support）、挑战（challenge）、证伪（falsification）或探索（exploratory）结果。使用[提交结果 Issue 模板](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=submission.md)。
2. **挑战或证伪**：提交最小反例、复现失败报告或证伪尝试。使用[挑战或证伪 Issue 模板](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=challenge-falsification.md)。挑战对象可以是 claim、预设、推论、口径或实现。
3. **提出新任务**：提出新的验证方向、悬赏任务或基础设施改进。使用[新任务提案 Issue 模板](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=task-proposal.md)。
4. **改进文档**：修正错别字、补充说明、改善示例或翻译。直接提交 Pull Request 即可，无需预注册。

无论你提交的是支持性还是负面结果，只要通过形式校验和评审，都会进入[证据账本](open-validation/evidence-ledger.csv)。我们**不会只保留支持性结果**。

---

### English

Contributors of any background are welcome. You can participate in four ways, all initiated via GitHub Issues:

1. **Submit validation results**: Run an experiment on an active claim and submit a support, challenge, falsification, or exploratory result. Use the [submission Issue template](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=submission.md).
2. **Challenge or falsify**: Submit a minimal counterexample, failed replication, or falsification attempt. Use the [challenge/falsification Issue template](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=challenge-falsification.md). The target can be a claim, preset, inference, measurement caliber, or implementation.
3. **Propose new tasks**: Suggest new validation directions, bounties, or infrastructure improvements. Use the [task proposal Issue template](https://github.com/KK13760780514/Hypostack-Theory/issues/new?template=task-proposal.md).
4. **Improve documentation**: Fix typos, clarify explanations, improve examples, or translate. Submit a Pull Request directly—no preregistration needed.

Whether your result is supportive or negative, as long as it passes form validation and review, it enters the [evidence ledger](open-validation/evidence-ledger.csv). We **do not keep only supportive results**.

---

## 2. 认领任务 / Claim a Task

### 中文

所有验证任务列在 [open-validation/tasks/](open-validation/tasks/) 目录中：

| 任务 | 方向 | 说明 |
|------|------|------|
| [TASK-001](open-validation/tasks/TASK-001-reproduce-p1.md) | 复现 P1 增强 | 历史任务，已被 TASK-005 取代 |
| [TASK-002](open-validation/tasks/TASK-002-stress-test-ai-toy.md) | 压力测试 AI 玩具 | 历史任务，已被 TASK-004 取代 |
| [TASK-003](open-validation/tasks/TASK-003-e-dimension-paradigm-map.md) | E 维度范式转换 | 提出可计算的转换函数 |
| [TASK-004](open-validation/tasks/TASK-004-adam-dynamics.md) | Adam 自适应动态 | 复现与挑战首次 challenge 结果 |
| [TASK-005](open-validation/tasks/TASK-005-chemical-path.md) | 化学路径竞争 | **推荐入门**，有完整参考实现 |
| [TASK-006](open-validation/tasks/TASK-006-phase-transition.md) | 相变路径选择 | 2D Ising 模型验证，首次结果 support |
| [TASK-007](open-validation/tasks/TASK-007-e-paradigm-process-type.md) | E 范式转换（过程类型） | 按过程类型分类标定 η，检验组内普适性（由 ISSUE-007 立项，需预注册判据） |

**新贡献者推荐从 [TASK-005](open-validation/tasks/TASK-005-chemical-path.md) 开始**：它有完整的参考实现（[chemical_path.py](open-validation/reference-implementation/chemical_path.py)）、明确的预测冲突（玄叠论预测路径 B，Arrhenius 预测路径 A），V1 结果为 challenge 而 V2 已修正为 support（L4_candidate），欢迎独立复现。

认领方式：

1. 阅读任务文件，了解背景、预测冲突和验收标准。
2. 在 GitHub 上开一个 Issue，注明你要认领的任务编号（如 `Claiming TASK-005`），简要说明你的计划。
3. 如果多人认领同一任务，鼓励独立并行验证——多份独立结果比单份更有价值。
4. 也可以不开 Issue 直接提交结果，但建议先认领以避免重复工作。

---

### English

All validation tasks are listed in the [open-validation/tasks/](open-validation/tasks/) directory:

| Task | Direction | Notes |
|------|-----------|-------|
| [TASK-001](open-validation/tasks/TASK-001-reproduce-p1.md) | Reproduce P1 enhanced | Historical, superseded by TASK-005 |
| [TASK-002](open-validation/tasks/TASK-002-stress-test-ai-toy.md) | Stress-test AI toy | Historical, superseded by TASK-004 |
| [TASK-003](open-validation/tasks/TASK-003-e-dimension-paradigm-map.md) | E-dimension paradigm shift | Propose a computable conversion function |
| [TASK-004](open-validation/tasks/TASK-004-adam-dynamics.md) | Adam adaptive dynamics | Reproduce and challenge the first challenge result |
| [TASK-005](open-validation/tasks/TASK-005-chemical-path.md) | Chemical path competition | **Recommended starter**, full reference implementation |
| [TASK-006](open-validation/tasks/TASK-006-phase-transition.md) | Phase-transition path selection | 2D Ising model validation, first result support |
| [TASK-007](open-validation/tasks/TASK-007-e-paradigm-process-type.en.md) | E-paradigm conversion (process type) | Calibrate η by process type, test within-type universality (spawned from ISSUE-007, preregistration required) |

**New contributors should start with [TASK-005](open-validation/tasks/TASK-005-chemical-path.md)**: it has a complete reference implementation ([chemical_path.py](open-validation/reference-implementation/chemical_path.py)), a clear prediction conflict (XuanDie predicts path B, Arrhenius predicts path A), and its V1 was a challenge with V2 revised to support (L4_candidate), welcoming independent replication.

How to claim:

1. Read the task file to understand the background, prediction conflict, and acceptance criteria.
2. Open a GitHub Issue stating the task number you are claiming (e.g., `Claiming TASK-005`) with a brief plan.
3. If multiple people claim the same task, independent parallel verification is encouraged—multiple independent results are more valuable than one.
4. You may also submit results directly without opening an Issue, but claiming first helps avoid duplicate work.

---

## 3. 提交实验结果 / Submit Results

### 中文

完整提交流程共四步。详细说明见 [open-validation/README.md](open-validation/README.md) 的「提交你的第一个实验」章节。

**第 1 步：填写预注册**

复制 [open-validation/preregistration-template.yaml](open-validation/preregistration-template.yaml) 到 `open-validation/submissions/` 目录，重命名为 `prereg-<你的名字>-<claim编号>.yaml`。在**运行实验之前**填写完毕，并固定四项内容：`E` 的测量范式、`N` 的计算方式、`S` 的计算方式、统计阈值。

生成预注册哈希（SHA-256），填入提交 JSON 的 `preregistration.hash` 字段：

```powershell
python -c "import hashlib; print(hashlib.sha256(open('你的预注册文件.yaml','rb').read()).hexdigest())"
```

**第 2 步：运行实验**

修改参考实现的参数，或使用你自己的代码。运行时保存：代码版本（git commit）、代码哈希、数据哈希、随机种子、环境信息（OS、Python 版本、依赖）。

**第 3 步：生成提交 JSON**

按 [open-validation/submission-schema.json](open-validation/submission-schema.json) 格式生成结果文件。参考 [example-p1-submission.json](open-validation/example-p1-submission.json) 了解字段格式。文件放入 `open-validation/submissions/`，建议命名：

```text
YYYY-MM-DD-<author>-<claim-id>.json
```

提交 JSON 的必填字段包括：`submission_id`、`claim_id`、`title`、`author`、`preregistration`（含 `hash` 和 `timestamp_utc`）、`implementation`（含 `code_hash`、`seed`、`environment`）、`result`（含 `S_A`、`S_B`、`preferred_path`、`summary`）、`classification`、`timestamp_utc`。

**第 4 步：校验入账**

运行校验脚本：

```powershell
python .\open-validation\validate_submission.py .\open-validation\submissions\你的提交.json
```

- 校验通过：结果自动追加到 [open-validation/evidence-ledger.csv](open-validation/evidence-ledger.csv)，并按分类赋予证据等级。
- 校验失败：脚本会输出错误信息，修正后重新运行。历史失败记录会被新通过的结果标记为 `superseded_by`，不会被删除。

你可以使用 `--no-ledger` 参数只校验不入账，方便本地调试。

---

### English

The full submission process has four steps. See the "Submit your first experiment" section of [open-validation/README.md](open-validation/README.md) for details.

**Step 1: Fill in the preregistration**

Copy [open-validation/preregistration-template.yaml](open-validation/preregistration-template.yaml) into the `open-validation/submissions/` directory, renaming it `prereg-<your-name>-<claim-id>.yaml`. Complete it **before running the experiment**, fixing four items: the `E` measurement paradigm, the `N` calculation method, the `S` calculation method, and the statistical threshold.

Generate the preregistration hash (SHA-256) and put it in the `preregistration.hash` field of your submission JSON:

```powershell
python -c "import hashlib; print(hashlib.sha256(open('your-preregistration.yaml','rb').read()).hexdigest())"
```

**Step 2: Run the experiment**

Modify the reference implementation parameters, or use your own code. While running, save: code version (git commit), code hash, data hash, random seed, and environment info (OS, Python version, dependencies).

**Step 3: Generate the submission JSON**

Generate the result file following the [open-validation/submission-schema.json](open-validation/submission-schema.json) format. See [example-p1-submission.json](open-validation/example-p1-submission.json) for the field layout. Place the file in `open-validation/submissions/` with the suggested naming:

```text
YYYY-MM-DD-<author>-<claim-id>.json
```

Required fields in the submission JSON: `submission_id`, `claim_id`, `title`, `author`, `preregistration` (with `hash` and `timestamp_utc`), `implementation` (with `code_hash`, `seed`, `environment`), `result` (with `S_A`, `S_B`, `preferred_path`, `summary`), `classification`, `timestamp_utc`.

**Step 4: Validate and ledger**

Run the validation script:

```powershell
python .\open-validation\validate_submission.py .\open-validation\submissions\your-submission.json
```

- On success: the result is automatically appended to [open-validation/evidence-ledger.csv](open-validation/evidence-ledger.csv) and assigned an evidence level based on its classification.
- On failure: the script prints error messages; fix them and re-run. Historical failed records are marked `superseded_by` when a new passing result arrives—they are never deleted.

You can use the `--no-ledger` flag to validate without appending to the ledger, useful for local debugging.

---

## 4. 预注册制度 / Preregistration

### 中文

**为什么必须预注册？**

玄叠论的核心公式 `S = ∫ E dN` 中，`E`、`N`、`S` 的具体测量方式有多种合法定义。如果不预先固定，研究者可以在看到结果后选择对自己有利的口径，导致确认偏误。预注册的作用是：在实验执行前公开声明「我将如何测量、如何判断」，使结果无论支持还是反对预测，都具有可比性和可信度。

预注册通过 [open-validation/preregistration-template.yaml](open-validation/preregistration-template.yaml) 完成。提交 JSON 中的 `preregistration.hash` 字段记录预注册文件的 SHA-256 哈希，供评审时与预注册文件对照核验。`validate_submission.py` 仅做格式与时间顺序检查（非 64 位 hex 或占位符会输出 warnings）；哈希与预注册文件的一致性属于评审环节的人工核查项，请妥善保存预注册文件。

**四项不可更改声明**

预注册后，以下四项内容**禁止修改**。如果实验过程中发现需要调整，必须重新预注册并重新提交，原结果保留作历史记录：

1. **`E` 的测量范式**：`E_i` 是什么、单位是什么、如何测量（如「第 i 步的活化能 Ea_i，单位 J/mol，由 Arrhenius 方程参数确定」）。
2. **`N` 的计算方式**：`N` 是什么、如何界定一步（如「反应步数，一个 ODE 积分步为一步」）。
3. **`S` 的计算方式**：`S` 的公式与实现说明（如 `S = Σ(E_i × ΔN_i)`，对每步的 `E_i` 求和）。
4. **统计阈值**：检验方法、显著性水平 `alpha`、单侧/双侧（如「binomial test，alpha=0.01，单侧」）。

预注册模板中的 `result_policy.post_registration_changes_allowed` 字段必须设为 `false`。

---

### English

**Why is preregistration mandatory?**

In the core formula `S = ∫ E dN`, the concrete measurement of `E`, `N`, and `S` has multiple legitimate definitions. Without fixing them in advance, a researcher could choose a favorable caliber after seeing the results, leading to confirmation bias. Preregistration serves to publicly declare "how I will measure and how I will judge" before the experiment runs, so that results—whether supportive or opposing—are comparable and credible.

Preregistration is done via [open-validation/preregistration-template.yaml](open-validation/preregistration-template.yaml). The `preregistration.hash` field in the submission JSON records the SHA-256 hash of the preregistration file so reviewers can cross-check it. `validate_submission.py` only performs a format and timestamp check (non-64-hex hashes or placeholders produce warnings); verifying the hash actually matches the preregistration file is a manual review step, so keep the preregistration file for verification.

**The four immovable declarations**

After preregistration, the following four items **must not be modified**. If you discover a need to adjust during the experiment, you must re-preregister and resubmit; the original result is retained as a historical record:

1. **`E` measurement paradigm**: what `E_i` is, its unit, and how it is measured (e.g., "activation energy Ea_i of step i, in J/mol, determined by Arrhenius equation parameters").
2. **`N` calculation method**: what `N` is and how a step is defined (e.g., "number of reaction steps, one ODE integration step per step").
3. **`S` calculation method**: the formula and implementation note (e.g., `S = Σ(E_i × ΔN_i)`, summing `E_i` over each step).
4. **Statistical threshold**: the test method, significance level `alpha`, and one-sided/two-sided choice (e.g., "binomial test, alpha=0.01, one-sided").

The `result_policy.post_registration_changes_allowed` field in the preregistration template must be set to `false`.

---

## 5. 代码规范 / Code Standards

### 中文

为保证可复现性和零依赖运行，所有验证代码须遵守以下规范：

1. **Python 3.9+**：参考实现和校验脚本均使用 Python 3.9+ 语法。提交时请在 `environment.python_version` 中记录实际版本。
2. **仅用标准库**：不得依赖 numpy、scipy、torch 等第三方库。参考实现只使用 Python 标准库（`math`、`hashlib`、`json`、`csv` 等），确保任何人无需 `pip install` 即可运行。在 `environment.dependencies` 中填写 `python-stdlib-only`。
3. **代码必须有 SHA-256 哈希**：提交 JSON 的 `implementation.code_hash` 字段必须填写主脚本的 SHA-256 哈希值。生成方式：

   ```powershell
   python -c "import hashlib; print(hashlib.sha256(open('你的主脚本.py','rb').read()).hexdigest())"
   ```

   如果代码托管在 Git 仓库，请在 `implementation.repository` 填写仓库 URL，在 `implementation.commit` 填写 commit hash。
4. **随机种子固定**：所有涉及随机性的实验必须在运行前固定种子，并在 `implementation.seed` 中记录。多个种子以数组形式提供（如 `[42, 123, 456]`）。
5. **可复现**：另一位评审者应能仅凭提交信息（代码哈希、种子、环境）独立重跑核心结果。

---

### English

To ensure reproducibility and zero-dependency execution, all validation code must follow these standards:

1. **Python 3.9+**: The reference implementations and validation script use Python 3.9+ syntax. Record the actual version in `environment.python_version` when submitting.
2. **Standard library only**: Do not depend on third-party libraries such as numpy, scipy, or torch. The reference implementations use only the Python standard library (`math`, `hashlib`, `json`, `csv`, etc.), so anyone can run them without `pip install`. Fill `python-stdlib-only` in `environment.dependencies`.
3. **Code must have a SHA-256 hash**: The `implementation.code_hash` field of the submission JSON must contain the SHA-256 hash of the main script. Generate it with:

   ```powershell
   python -c "import hashlib; print(hashlib.sha256(open('your-main-script.py','rb').read()).hexdigest())"
   ```

   If the code is hosted in a Git repository, fill in the repository URL in `implementation.repository` and the commit hash in `implementation.commit`.
4. **Fixed random seed**: Any experiment involving randomness must fix its seed before running and record it in `implementation.seed`. Multiple seeds are provided as an array (e.g., `[42, 123, 456]`).
5. **Reproducible**: Another reviewer should be able to independently re-run the core result using only the submission info (code hash, seed, environment).

---

## 6. 评审流程 / Review Process

### 中文

所有提交经过五个阶段的评审。完整清单见 [open-validation/review-checklist.md](open-validation/review-checklist.md)。评审目标是判断结果是否可进入证据账本，**而不是判断评审者是否喜欢玄叠论**。

1. **形式检查**：JSON 是否通过 `validate_submission.py`；`claim_id` 是否属于当前开放 claim；`submission_id` 是否唯一；作者、时间戳、代码哈希、环境信息是否完整；提交文件是否位于 `submissions/` 并符合命名规范。
2. **预注册合规**：预注册时间是否早于实验执行时间；`E`、`N`、`S` 和统计阈值是否已固定；实验后是否被修改；如有偏离，作者是否明确声明并解释影响。
3. **可复现性**：代码是否可运行；随机种子是否固定；数据哈希或数据来源是否完整；原始输出是否可追溯；依赖版本是否明确；另一位评审者能否独立重跑核心结果。
4. **统计检查**：统计检验是否与预注册一致；单侧/双侧选择是否一致；p 值计算是否正确；是否报告效应量；多重比较是否已处理；是否只挑选支持性结果。
5. **证据解释**：`support`/`challenge`/`falsification`/`exploratory` 分类是否与结果一致；是否把一个具体预测的成败夸大为整套理论的成败；负面结果是否已记录；如果结果挑战当前口径，是否明确说明是口径问题、实现问题还是理论问题。

涉及证伪核心预设的结论，应升级给独立委员会评审。评审者与提交者不得有未声明的利益关系，评审者不得修改提交数据。

---

### English

All submissions go through five review stages. The full checklist is in [open-validation/review-checklist.md](open-validation/review-checklist.md). The review goal is to judge whether a result can enter the evidence ledger—**not whether the reviewer likes XuanDie Theory**.

1. **Form check**: Does the JSON pass `validate_submission.py`; is `claim_id` among the currently open claims; is `submission_id` unique; are author, timestamp, code hash, and environment info complete; is the file in `submissions/` with correct naming.
2. **Preregistration compliance**: Was the preregistration timestamp earlier than the experiment execution; were `E`, `N`, `S`, and the statistical threshold fixed; were they modified after the experiment; if there is deviation, did the author clearly declare and explain the impact.
3. **Reproducibility**: Is the code runnable; is the random seed fixed; are the data hash or source complete; is the raw output traceable; are dependency versions explicit; can another reviewer independently re-run the core result.
4. **Statistical check**: Is the statistical test consistent with the preregistration; is the one-sided/two-sided choice consistent; is the p-value calculated correctly; is the effect size reported; are multiple comparisons handled; are only supportive results cherry-picked.
5. **Evidence interpretation**: Is the `support`/`challenge`/`falsification`/`exploratory` classification consistent with the result; is the success or failure of a single prediction overclaimed as that of the whole theory; are negative results recorded; if the result challenges the current caliber, is it clearly stated whether it is a caliber issue, an implementation issue, or a theoretical issue.

Conclusions involving falsification of core presets should be escalated to an independent committee. Reviewers must have no undisclosed conflicts of interest with submitters and must not modify submission data.

---

## 7. 证据等级 / Evidence Levels

### 中文

提交通过校验后，由 `validate_submission.py` 根据分类自动赋予证据等级，记录在 [open-validation/evidence-ledger.csv](open-validation/evidence-ledger.csv) 的 `evidence_level` 列：

| 证据等级 | 对应分类 | 含义 |
|----------|----------|------|
| `L4_candidate` | `support` | 按预注册完成，结果支持该具体预测，等待独立复核。 |
| `L5_candidate` | `falsification` | 按预注册完成，结果显著证伪该具体预测。 |
| `exploratory` | `challenge` 或其他非 support/falsification 分类 | 校验器对非 support/falsification 分类一律赋予 exploratory（含 challenge 及提交者自标 exploratory 的结果）；统计阈值评估属评审环节。 |
| `needs_review` | 任意（校验未通过） | 格式（schema）检查未通过，需修正后重新提交；统计与可复现性评估属评审环节，见 review-checklist.md。 |

另有历史等级与升级路径：

- `degraded`：claim 本身已被降级（如 ISSUE-001/004），记录保留作历史参考，不再接受新提交。
- `confirmed`：由 `L4_candidate` 经**外部独立复核确认**后升级（对应分类 support + 独立复核），不由校验脚本自动生成。

说明：

- `L4_candidate` 和 `L5_candidate` 都是「候选」等级，需经过独立复核后才能升级。
- `exploratory` 不是失败，而是验证包正在暴露口径问题，这类结果对理论改进同样有价值。
- 证据账本中的记录永不删除。失败记录在新提交通过后会被标记为 `superseded_by`，保留完整历史。

---

### English

After a submission passes validation, `validate_submission.py` automatically assigns an evidence level based on its classification, recorded in the `evidence_level` column of [open-validation/evidence-ledger.csv](open-validation/evidence-ledger.csv):

| Evidence level | Corresponding classification | Meaning |
|----------------|------------------------------|---------|
| `L4_candidate` | `support` | Completed per preregistration; the result supports the specific prediction; awaiting independent review. |
| `L5_candidate` | `falsification` | Completed per preregistration; the result significantly falsifies the specific prediction. |
| `exploratory` | `challenge` or any non-support/falsification classification | The validator assigns exploratory to any non-support/falsification classification (including challenge and self-labeled exploratory); statistical-threshold evaluation is part of review. |
| `needs_review` | Any (validation failed) | Format (schema) checks failed; resubmit after correction. Statistical and reproducibility evaluation are part of review, see review-checklist.md. |

There are also a historical level and an upgrade path:

- `degraded`: The claim itself has been downgraded (e.g., ISSUE-001/004); the record is retained for historical reference and no longer accepts new submissions.
- `confirmed`: Upgraded from `L4_candidate` only after **external independent review confirmation** (classification: support + independent review); not auto-generated by the validator.

Notes:

- Both `L4_candidate` and `L5_candidate` are "candidate" levels requiring independent review before upgrading.
- `exploratory` is not a failure—it means the validation package is exposing caliber issues, and such results are equally valuable for theory improvement.
- Records in the evidence ledger are never deleted. Failed records are marked `superseded_by` when a new submission passes, preserving full history.

---

## 8. 行为准则 / Code of Conduct

### 中文

参与 HypoStack 开放验证社区，请遵守以下准则：

1. **支持性、挑战性、证伪性结果均接收**。我们追求的是可证伪性，而不是证明理论正确。一份严谨的 challenge 或 falsification 与一份严谨的 support 同样有价值，都会进入证据账本。不要只提交支持性结果。
2. **预注册后禁止修改**。`E`、`N`、`S` 和统计阈值一旦预注册，不得在实验后修改。如需调整口径，必须重新预注册并重新提交，原结果保留作历史记录。这是保证结果可信度的基石。
3. **单一预测证伪 ≠ 理论证伪**。玄叠论包含多个 claim 和多层推论。某个具体预测在特定条件下被证伪，只说明该条件下的预测失效，不等于整套玄叠论被证伪。不要把单个 claim 的成败夸大为整体理论的成败。
4. **诚实声明**。提交者须声明「我不是只提交支持玄叠论的结果」，并允许结果被公开引用。评审者须声明与提交者无未声明的利益关系。
5. **尊重不同口径**。`S` 的定义有多种合法定义，关于口径的讨论是科学推进的一部分。对口径的挑战应聚焦于逻辑和证据，而非人身。

---

### English

When participating in the HypoStack open-validation community, please follow these guidelines:

1. **Supportive, challenge, and falsification results are all accepted.** We pursue falsifiability, not proof that the theory is correct. A rigorous challenge or falsification is as valuable as a rigorous support and both enter the evidence ledger. Do not submit only supportive results.
2. **No modification after preregistration.** Once `E`, `N`, `S`, and the statistical threshold are preregistered, they must not be modified after the experiment. To adjust a caliber, you must re-preregister and resubmit; the original result is retained as a historical record. This is the cornerstone of result credibility.
3. **Single-prediction falsification ≠ theory falsification.** XuanDie Theory contains multiple claims and layers of inference. A specific prediction being falsified under certain conditions only means that prediction fails under those conditions—it does not equal falsification of the entire theory. Do not overclaim the success or failure of a single claim as that of the whole theory.
4. **Honest declaration.** Submitters must declare "I am not submitting only results that support XuanDie Theory" and allow the result to be publicly cited. Reviewers must declare no undisclosed conflicts of interest with submitters.
5. **Respect different calibers.** There are multiple legitimate definitions of `S`; discussion about caliber is part of scientific progress. Challenges to a caliber should focus on logic and evidence, not on persons.

---

## 9. 许可证 / License

### 中文

- **理论文本**（`玄叠论.md` 及所有文档，包括本文件）：[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)。你可以自由分享和改编，但必须署名并以相同许可发布衍生作品。
- **代码**（参考实现、校验脚本等）：[MIT](LICENSE)。

提交内容（预注册 YAML、提交 JSON、实验代码）的许可证默认与仓库一致：文本部分按 CC BY-SA 4.0，代码部分按 MIT。提交即表示你同意按此许可发布你的贡献。

---

### English

- **Theory text** (`玄叠论.md` and all documentation, including this file): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You may freely share and adapt, but you must attribute and distribute derivatives under the same license.
- **Code** (reference implementations, validation scripts, etc.): [MIT](LICENSE).

The license of submitted content (preregistration YAML, submission JSON, experiment code) defaults to that of the repository: text under CC BY-SA 4.0, code under MIT. By submitting, you agree to release your contribution under these licenses.
