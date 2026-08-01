# TASK-005：化学反应路径竞争验证

- Claim: `XD-P1-CHEM-001`
- 难度：L2-L3
- 类型：独立验证 / 口径挑战 / 证伪尝试

## 背景

旧 claim `XD-P1-SIM-001` 使用 softmax 选择器，存在定义性循环（softmax 必然偏好低 S）。本任务用独立物理定律（Arrhenius 化学动力学）驱动的自然系统替代，设计了一个**两个理论预测相反**的场景。

## 预测冲突

两条化学反应路径从反应物 R 到产物 P：

- 路径 A：R -> I -> P（2步，每步 Ea=30 kJ/mol，S_A=60 kJ/mol）
- 路径 B：R -> P（1步，Ea=55 kJ/mol，S_B=55 kJ/mol）

- **玄叠论预测**：系统选 S 最小的路径 B（S_B=55 < S_A=60）
- **Arrhenius 预测**：系统选决速步最低的路径 A（决速步 Ea=30 < 路径 B Ea=55）

两个预测**方向相反**，有真正的区分度。

## 参考实现首次结果（V1，2026-07-30）

[chemical_path.py](../reference-implementation/chemical_path.py) 在 8 个温度点（280K-500K）模拟：

- **8/8 温度全部选路径 A，0/8 匹配玄叠论预测，p=1.0**
- 路径 A 的产物量在低温下比路径 B 高 4-5 个数量级
- 结论分类：**challenge**--玄叠论的 S=ΣEa 定义在路径选择上被挑战

## V2 修正结果（2026-08-01）

E 重定义为有效活化能（稳态近似，E_eff = -RT×ln(k_eff/A)），N=1。对称+非对称两组势垒配置下 **16/16 温度全部匹配，p=1.5e-5，结论修正为 support（L4_candidate）**。参考实现见 [chemical_path_v2.py](../reference-implementation/chemical_path_v2.py)。

## 可认领方向

1. **复现**：独立复现 V2 的 support 结论（16/16, p=1.5e-5），或在不同温度范围/Ea 组合下检验稳健性。复核召集见 [issue #11](https://github.com/KK13760780514/Hypostack-Theory/issues/11)。
2. **口径挑战**：V2 采用有效活化能口径（稳态近似）；提出替代 E 定义（如决速步 Ea、自由能垒 ΔG‡）预注册后对比，检验是否仍与 Arrhenius 一致。
3. **证伪扩展**：找到更多"S 低但系统不选"的案例，或找到"S 低且系统选"的案例。
4. **理论分析**：分析 S=ΣEa / S=E_eff 与 Arrhenius 动力学在什么条件下一致、什么条件下冲突。
5. **真实实验**：用真实化学反应数据（文献中的竞争反应路径）替代模拟。

## 验收标准

- 修改 E 定义必须先预注册。
- challenge 结果与 support 结果同等入库。
- 提交 JSON 通过 `validate_submission.py`。

## 交付物

- 预注册 YAML；
- 提交 JSON；
- 简短结论：支持 / 挑战 / 证伪 / 探索。
