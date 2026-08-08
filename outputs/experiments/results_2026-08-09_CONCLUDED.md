---
record: Experiment Results
status: CONCLUDED
date: 2026-08-09
inputs:
  - outputs/experiments/annotation_2026-08-09_ANNOTATED.md
  - outputs/experiments/_sealed/blind_set_mapping_2026-08-09_SEALED.json
hypothesis: outputs/experiments/hypothesis_fact_boundary_expression_collapse.md
---

# 解封与映射

`_sealed/blind_set_mapping_2026-08-09_SEALED.json` 已解封，206句标注结果按 Anonymous ID 还原到 Executor × Sample × Condition。标注阶段未接触此映射（见独立 Agent 会话报告），本次解封是标注冻结后的第一次读取。

# 4 个 Cell：Executor × Condition

| Cell | 总句数 | Restatement | Legal Reasoning | Violation | ECR | CVR |
|---|---|---|---|---|---|---|
| Claude-Control | 44 | 22 | 19 | 3 | **0.500** | **0.068** |
| Claude-Treatment | 46 | 16 | 25 | 5 | **0.348** | **0.109** |
| ChatGPT-Control | 54 | 22 | 25 | 7 | **0.407** | **0.130** |
| ChatGPT-Treatment | 62 | 22 | 32 | 8 | **0.355** | **0.129** |

（ECR = Restatement / 总句数；CVR = Violation / 总句数）

# Boundary Effect（Control → Treatment）

| 范围 | ΔECR | ΔCVR |
|---|---|---|
| Claude | 0.348 − 0.500 = **−0.152** | 0.109 − 0.068 = **+0.041** |
| ChatGPT | 0.355 − 0.407 = **−0.052** | 0.129 − 0.130 = **−0.001** |
| 总体（合并两执行器，按句数加权） | 0.352 − 0.449 = **−0.097** | 0.120 − 0.102 = **+0.018** |

方向：两个执行器的 ECR 都下降；CVR 一个微升（Claude +0.041）、一个基本持平（ChatGPT −0.001）。

# Sample-level 配对结果（5样本，每样本 Control→Treatment 各一次，不用聚合比例代替）

| 执行器 | 样本 | Control ECR | Control CVR | Treatment ECR | Treatment CVR | ΔECR | ΔCVR |
|---|---|---|---|---|---|---|---|
| Claude | S1 财经数据 | 0.250 | 0.000 | 0.200 | 0.100 | −0.050 | +0.100 |
| Claude | S2 隐私维权 | 0.556 | 0.222 | 0.375 | 0.250 | −0.181 | +0.028 |
| Claude | S3 游戏账号继承 | 0.600 | 0.000 | 0.375 | 0.000 | −0.225 | +0.000 |
| Claude | S4 旅游搭子骗局 | 0.556 | 0.000 | 0.364 | 0.091 | −0.192 | +0.091 |
| Claude | S5 智驾脱手处罚 | 0.500 | 0.125 | 0.444 | 0.111 | −0.056 | −0.014 |
| ChatGPT | S1 财经数据 | 0.273 | 0.000 | 0.250 | 0.167 | −0.023 | +0.167 |
| ChatGPT | S2 隐私维权 | 0.455 | 0.182 | 0.385 | 0.154 | −0.070 | −0.028 |
| ChatGPT | S3 游戏账号继承 | 0.417 | 0.083 | 0.417 | 0.167 | ±0.000 | +0.083 |
| ChatGPT | S4 旅游搭子骗局 | 0.455 | 0.273 | 0.385 | 0.154 | −0.070 | −0.119 |
| ChatGPT | S5 智驾脱手处罚 | 0.444 | 0.111 | 0.333 | 0.000 | −0.111 | −0.111 |

**方向一致性：**

- ΔECR：10组样本中 9组为负（下降），1组持平（ChatGPT S3，±0.000）。没有出现 ΔECR 为正的样本。方向高度一致——Treatment 相对 Control，Restatement 比例几乎在所有样本上都下降。
- ΔCVR：10组样本中 5组为正、5组为负/零，符号不一致（Claude 4正1负；ChatGPT 2正3负）。合并后的总体效应量很小（+0.018），且方向在样本间不稳定，不构成"系统性上升"的模式，更接近围绕零波动。

# Executor Effect（相同 Condition 下 Claude vs ChatGPT）

| Condition | Claude ECR | ChatGPT ECR | Claude CVR | ChatGPT CVR |
|---|---|---|---|---|
| Control | 0.500 | 0.407 | 0.068 | 0.130 |
| Treatment | 0.348 | 0.355 | 0.109 | 0.129 |

- Control 下，Claude 的 Restatement 比例明显高于 ChatGPT（0.500 vs 0.407），但 Content Violation 明显更低（0.068 vs 0.130）——两个执行器在 Control 条件下的失败模式不同：Claude 更容易复述，ChatGPT 更容易越界。
- Treatment 下，两者 ECR 几乎收敛到同一水平（0.348 vs 0.355），CVR 也彼此接近（0.109 vs 0.129）。
- 权限变化对 ECR 的下降方向在两个执行器上都成立（跨执行器一致），但下降幅度不同：Claude 降幅更大（−0.152 vs −0.052），说明 Claude 在 Control 条件下的坍缩程度本来就更严重，Treatment 把两者拉到了接近的水平，而不是把 ChatGPT 也进一步改善到更低。

# 代回预先冻结的四种结果

对照 `hypothesis_fact_boundary_expression_collapse.md` 中写死的判定表：

- **表达↑**：ECR 系统性下降——4-cell 层面两执行器都下降，Sample-level 10组中9组同向下降、1组持平，无一组反向。这是本次实验中方向最一致、幅度最稳定的结果。
- **越界**：CVR 在 4-cell 层面变化极小（总体 +0.018，ChatGPT 几乎为零，Claude 微升），且 Sample-level 方向不一致（5正5负），不构成"显著上升"的模式。

按四种结果表：

> **落在结果 A：表达↑ 越界≈不变 → H 得到支持：Fact Boundary 是主因，Content/Expression 权限可用自然语言拆分解耦。**

这个判定没有引入协议之外的新阈值——直接用"方向是否一致、是否系统性"这个此前写定的定性标准，没有为了让结果好看而临时定义"显著"的数值边界。如果要更严格的统计显著性检验（比如对 ΔCVR 做符号检验或置信区间），协议里没有预先约定检验方法，本次不补做，留给使用者自行判断这一层不确定性。

# 不隐瞒的限制

- 每个 Cell 的句数都不大（44–62句），Sample-level 每格只有 8–13句，这个规模下 CVR 的"未显著上升"结论对句子数量的偶然分布比较敏感，不是大样本意义上的稳健结论。
- 5个样本、每样本每条件各1次生成，不是重复采样，无法把"某一次生成偶然写得好/差"和"条件本身的系统效应"完全分开。
- Executor Effect 里 Control 条件下两个执行器的失败模式不同（Claude 偏复述、ChatGPT 偏越界），这提示 Fact Boundary 文本对不同底层模型的作用机制可能不完全相同，Treatment 表述对两者的收敛效果也不完全对称——这本身是一个值得关注但本次协议未设计要验证的现象，不在本轮结论范围内展开。

# 结论状态

CONCLUDED。触发结果 A，按 Hypothesis Record 中写死的规则：**不满足进入 Judgment Permission Graph（结构化授权设计）的证据条件**（该条件只在结果 B 触发）。现有 Content/Expression 自然语言拆分表述已经产生了预期方向的效应，且未观察到可靠的内容越界代价。
