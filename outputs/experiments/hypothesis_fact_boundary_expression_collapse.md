---
record: Hypothesis Record
status: SUPPORTED
result: outputs/experiments/results_2026-08-09_CONCLUDED.md
production_change: templates/transform_radar_source_prompt.md (Fact Boundary → Permission Boundary, 2026-08-09)
date: 2026-08-08
related_failure_samples:
  - outputs/experiments/medium_adapter_test_2026-08-08_搬家报价570元.md
  - outputs/articles/draft/2026-08-08_搬家报价570元_v1.md
related_constraint: templates/transform_radar_source_prompt.md:21-35 (Fact Boundary)
---

# H

`Fact Boundary`（templates/transform_radar_source_prompt.md:21-35）是否是 `Expression Collapse`（表达坍缩：Writer 退化为按 Radar 字段顺序逐条复述）的主要因果变量。

# Failure Evidence（已有，非新增假设）

同一 Radar（`data/radar_pool/2026-08-08_搬家报价570元-要5060元才肯上楼_0117dc09.radar.md`）：

- **Medium Adapter Raw**（无 Fact Boundary，仅媒介适配约束）→ `outputs/experiments/medium_adapter_test_2026-08-08_搬家报价570元.md` 第174-194行：有对比、递进、转折（"一个是用来吸引人下单的入口价，一个是真正要付的账单"），文章感强，但出现二阶事实推演（如"故意分开"）。
- **加入 Fact Boundary 后**（Medium Adapter + Fact Boundary）→ `outputs/articles/draft/2026-08-08_搬家报价570元_v1.md`：越界表达消失，但同时段落退化为"事实→平台解释→师傅解释→律师说法→普通人影响"的顺序复述，无对比/递进/转折结构。

这构成前后可比较的观察差异，但只有一个样本、非受控，不能作为结论，只能作为立项依据。

# 反作用风险（必须同时验证，不能只验证 H 本身）

`Expression Freedom ↑` 可能通过语言机制反向泄漏为 `Content Freedom ↑`：

- 推理连接词（"因为""这意味着"）可能从合法的判断间连接滑向新增因果事实
- 意图归因词（"故意""刻意"）在语义上和单纯的时间/逻辑顺序描述边界模糊
- 类比、场景化可能引入未经 Radar 批准的具体情节

Rhetorical Reasoning（在已批准判断间建立阅读逻辑）与 Content Inference（新增事实/因果/意图）之间的边界，在自然语言指令层面可能无法被模型稳定区分。这是本实验的第二个待验证问题，重要性不低于 H 本身。

# 四种实验结果与对应结论（写死，实验前不可更改）

| 结果 | 判定标准 | 结论 |
|---|---|---|
| A. 表达↑ 越界≈不变 | Expression Collapse Rate 显著下降，Content Violation Rate 与 Control 无显著差异 | H 得到支持：Fact Boundary 是主因，Content/Expression 权限可用自然语言拆分解耦 |
| B. 表达↑ 越界↑ | Expression Collapse Rate 显著下降，Content Violation Rate 显著上升 | H 部分成立：Fact Boundary 确实参与造成坍缩，但当前自然语言权限边界不足以解耦 Content 与 Expression，尚不具备进入 Judgment Permission Graph 的资格判断依据 —— 实际上是资格判断的必要条件被满足 |
| C. 表达≈不变 越界≈不变 | 两个指标都无显著差异 | H 被削弱：问题可能不主要在 Fact Boundary 文本本身，需回头看 Adapter 其他部分或模型行为 |
| D. 表达≈不变 越界↑ | Expression Collapse Rate 无改善，Content Violation Rate 上升 | 新设计失败：Treatment 表述本身有问题，直接废弃该版本表述，不代表 H 被否定 |

判定该进入 Judgment Permission Graph（结构化授权设计）阶段的唯一触发条件：**结果 B**。
结果 A 说明自然语言层面已经够用，不需要更复杂的结构。
结果 C、D 都不满足进入下一层设计的证据条件。

# Secondary Observation（二级观察，先记录，不处理）

Executor Effect 显示：Claude-Control 更容易 Collapse（ECR 高、CVR 低），ChatGPT-Control 更容易 Violate（ECR 低、CVR 高）——同一份模糊的 Fact Boundary 文本，在不同底层模型上导致了不同的失败模式。这提示"权限边界模糊"这件事本身对不同模型的影响机制可能不一样，但这不是本次 H 的研究对象，不据此展开"Claude Prompt / ChatGPT Prompt 两套系统"的设计工作。仅记录，留待后续如果有独立立项需求时再研究。

# 当前状态

SUPPORTED。落在预注册结果 A：ECR 系统性下降（10组配对中9组下降、1组持平，0组反向），CVR 无系统性上升（5正5负，总体 +0.018，方向不一致）。详见 `results_2026-08-09_CONCLUDED.md`。

已执行的最小生产变更：`templates/transform_radar_source_prompt.md` 第2节 Fact Boundary → Permission Boundary（Content Authority CLOSED / Expression Authority OPEN），逐字替换为实验中已验证的 Treatment 文本，其余部分（Target Format Contract、输出边界、输出格式）未改动。不触碰 Narrative Spine、Radar、Writer Role，不建 Judgment Permission Graph，不新增参数，不重写 Adapter，不重新设计 QA——这些均未被本次实验验证，留待真实生产文章的后续观察决定是否需要。
