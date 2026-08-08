---
record: Experiment Design
status: CONCLUDED
result: outputs/experiments/results_2026-08-09_CONCLUDED.md
run_outputs: outputs/experiments/run_2026-08-08/INDEX.md
run_outputs_chatgpt: outputs/experiments/run_2026-08-08_chatgpt/INDEX.md
blind_set: outputs/experiments/blind_set_2026-08-09/INDEX.md
annotation_output: outputs/experiments/annotation_2026-08-09_ANNOTATED.md
date: 2026-08-08
hypothesis: outputs/experiments/hypothesis_fact_boundary_expression_collapse.md
---

# 实验目的

隔离变量，验证 `Fact Boundary`（templates/transform_radar_source_prompt.md:21-35）是否是 `Expression Collapse` 的主要因果变量。不是为了证明新 Prompt 更好看。

# 固定变量

- 同一批 Radar 样本（见下）
- 同一 Adapter 框架（templates/transform_radar_source_prompt.md 的第 1 节 Target Format Contract 不变）
- 同一模型、同一生成参数
- 每个样本只生成一次 Control、一次 Treatment，不做多次采样取优

# 唯一变量：第 2 节的权限表述

## Control（现状原文，逐字照抄 transform_radar_source_prompt.md:21-35）

```text
### 2. Fact Boundary：什么不能编

不得新增源材料未确认的：

- 具体人物行为、具体事件过程、时间地点
- 主观认知（如"她觉得""这让她意识到"）
- 因果关系（如具体的机制推演）
- 收费/信息披露状态（如"没有提前说清楚""等到……才告知"）
- 具体运作机制（如强制手段的具体方式）
- 舆情或效果数据（如热度、传播反馈）
- 确定性评价（带定性色彩的判断词）

一般性分析允许展开（不针对本案具体过程的常识性陈述），但必须与本案已确认事实明确区分，不得把合理推演写成本案已经发生的事实。

生成之后会有独立的 Fact Boundary Review 逐句核对，不要依赖自己"读起来合理"的判断替代这道检查——写的时候就应该对每一句话反问一次"雷达详情里有没有这一句的依据"。
```

## Treatment（Content Freedom = LOW / Expression Freedom = HIGH）

```text
### 2. Permission Boundary：内容权限有限，表达权限充分开放

**Content Authority（内容权限）：CLOSED —— 以下内容只能来自源材料，不能新增**

- 具体人物行为、具体事件过程、时间地点
- 主观认知（如"她觉得""这让她意识到"）
- 因果关系事实（如具体的机制推演、"故意""刻意"等主体意图归因）
- 收费/信息披露状态（如"没有提前说清楚""等到……才告知"）
- 具体运作机制（如强制手段的具体方式）
- 舆情或效果数据（如热度、传播反馈）
- 确定性评价（带定性色彩的判断词）

**Expression Authority（表达权限）：OPEN —— 你可以自由使用以下手段组织已批准的事实与编辑判断**

- 对比、递进、转折、反问
- 在 Radar 已批准的判断之间建立阅读逻辑（例如把"入口价"和"实付价"并置成一组对比，而不新增"为什么会有差距"的具体机制）
- 长短句、节奏控制、信息前后呼应
- 把一个 Editorial Judgment 充分讲透，而不是逐字段罗列

区分标准：如果去掉某句话，某个"已批准判断"就读不懂或读不完整——这是合法的 Expression。如果去掉某句话，读者会少知道一个"事实、过程、动机或结论"——这是违规的 Content。写的时候对每一句话反问一次："这句话是在解释已批准的判断，还是在补充新的事情？"

一般性分析允许展开（不针对本案具体过程的常识性陈述），但必须与本案已确认事实明确区分，不得把合理推演写成本案已经发生的事实。

生成之后会有独立的 Fact Boundary Review 逐句核对，不要依赖自己"读起来合理"的判断替代这道检查。
```

差异只在权限描述的框架（黑名单 vs Content/Expression 两栏 + 区分标准），末两段闭合语保持一致，避免长度/格式差异成为混淆变量。

# 样本（现成 Radar，不重新采集，跨题材，不挑好写的）

| # | 文件 | 题材 |
|---|---|---|
| 1 | `data/radar_pool/2026-07-29_中国科技省份增长更快但消费没有同步跟上_aa3c9759.radar.md` | 财经数据 |
| 2 | `data/radar_pool/2026-07-29_女子修手机被店主导出40多张私密照_cec09919.radar.md` | 隐私/维权 |
| 3 | `data/radar_pool/2026-08-05_独子去世母亲要求继承87个游戏账号_59b32704.radar.md` | 家庭伦理/财产 |
| 4 | `data/radar_pool/2026-08-05_1人操控100个账号把旅游搭子骗去新疆_06d49e38.radar.md` | 诈骗 |
| 5 | `data/radar_pool/2026-08-08_辅助驾驶-自动驾驶-高速上方向盘脱手用智驾男子被处罚_8571fcc5.radar.md` | 政策法规/科技 |

（搬家报价570元样本已用于 Failure Evidence，不计入本次受控实验，避免用同一样本既定义假设又验证假设。）

每个样本各跑一次 Control、一次 Treatment，共 10 篇产出。

# 逐句三分类标注

对每篇产出的正文，按句拆分，每句标注一个类别：

- **Restatement（复述）**：直接对应 Radar 中某个字段，无新增连接、无推进，句子可与 Radar 原句一一对应
- **Legal Rhetorical Reasoning（合法表达推理）**：在两个或多个已批准判断/事实之间建立阅读逻辑（对比、递进、转折、因果顺序陈述），但没有新增 Radar 未提供的具体事实、过程、机制、主体意图或确定性结论
- **Content Violation（内容越界）**：包含 Radar 未提供的具体人物行为/事件过程/时间地点/主观认知/因果机制/主体意图/舆情数据/确定性评价

标注人：不预先知道该句来自 Control 还是 Treatment（盲标，标注时隐去版本标签）。

# 指标计算

- `Expression Collapse Rate` = Restatement 句数 / 总句数（越高越坍缩）
- `Content Violation Rate` = Content Violation 句数 / 总句数（越高越越界）

每个样本分别算 Control 和 Treatment 的两个指标，5 个样本汇总后看整体方向和方差，不用单样本下结论。

# 判定

对照 `hypothesis_fact_boundary_expression_collapse.md` 中写死的四种结果表，判定落在 A / B / C / D 哪一种，据此决定是否有资格进入 Judgment Permission Graph 设计阶段。

# 当前状态

ANNOTATION_FROZEN。20篇（Claude 10篇 + ChatGPT 10篇）已匿名打乱（`blind_set_2026-08-09/`）并完成独立会话的逐句三分类标注（`annotation_2026-08-09_ANNOTATED.md`），标注者未接触 `_sealed/` 映射、未接触本设计文档与 Hypothesis Record。映射尚未解封，Executor × Condition 的指标计算尚未进行，等待明确指令后执行。
