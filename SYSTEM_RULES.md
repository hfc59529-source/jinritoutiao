# 雷达生产主链 v1

## 层级归属

本文件是 [`ARCHITECTURE_V1.md`](ARCHITECTURE_V1.md) 中 **Stage 2: Transform** 的执行层规范，归属关系：

```text
Architecture（ARCHITECTURE_V1.md）
        ↓
Stage: Transform（STAGE_DEFINITION_V1.md / TRANSFORM_STANDARD_V1.md）
        ↓
本文件：SYSTEM_RULES.md（雷达生产主链 v1 —— Selection、Radar Source、Shared、Transform 的具体规则）
        ↓
Scripts（scripts/daily_radar_run.py 等）
        ↓
Runtime（data/、outputs/、prompts/generated/ 下的真实产物）
```

本文件不是与 `*_V1.md` 系列并行的另一套系统。Selection、Radar Source、Shared、Transform 都归位于现有生产链路内部，不作为独立 Stage 或独立系统存在。

## 定义

同一个雷达选题只生成一个 Article Master：

```text
Collect
↓
Selection
↓
Radar Source（含 Original Radar Production Prompt）
↓
Transform（Execution Adapter）
↓
Article Draft
↓
Fact Boundary Review
↓
Quality Review（参照 Shared 七项）
↓
Article Master
↓
Revision / Publish
↓
Feedback
```

`Radar Source` 是 Transform Method，不是独立生命周期。Fact Boundary Review 和 Quality Review 都属于 Review Stage 内部的两轮独立审核，不是新增 Stage。

## 爆点文案筛选层

生产之前必须先筛选老师网站已经生成完成的爆点文案。

```text
老师网站爆点文案池
        ↓
List Scan
        ↓
Pre-Filter
        ↓
Detail Fetch
        ↓
爆点文案筛选卡 radar_selection
        ↓
今日入选文案
        ↓
冻结完整雷达原文
        ↓
Shared 七项
        ↓
Transform
        ↓
Article Master
```

筛选对象不是原始热点，而是成品爆点文案。默认老师网站产出的文案已经合格，这里只判断它是否值得占用当天头条发布位。

### Collect 内部动作

Collect 内部允许拆成两个动作，但不新增 Stage：

- List Scan + Pre-Filter：Acquisition Decision（是否值得花一次详情采集成本）
- Detail Fetch：抓取并保存完整雷达详情

Pre-Filter 只读取标题、榜单位置、列表评分/标签、来源日期等廉价信息，只问三个问题：

1. 标题本身能否看出大众相关性？
2. 是否存在明确冲突 / 利益 / 风险信号？
3. 热点是否仍然新鲜？

Pre-Filter 只输出 FETCH / SKIP / REVIEW，不允许输出 P1 / P2 / P3。SKIP 只用于明显淘汰；不确定时必须保留为 REVIEW 或 FETCH，不能提前杀掉潜在素材。

Detail Fetch Rate = 抓取详情数 / 扫描标题数。该指标只衡量 Collect Efficiency（采集效率），不参与 Selection 排名。

硬性规则：筛选前必须先保存文案雷达完整原文到 `data/radar_pool/`。筛选卡、Shared 和生产包都必须引用这份已保存原文，不能只保存摘要或筛选结果。

来源真实性硬性规则：`data/radar_pool/` 只允许进入两类内容：

- 从老师爆款文案网站真实采集/导出的完整原文。
- 用户明确粘贴并确认来自老师爆款文案网站的完整原文。

禁止为了测试流程自行编造选题、评分、来源标签或伪造“今日爆点”来源。若没有真实网站原文，流程状态只能标记为“等待采集”，不能生成筛选卡或发布包。

雷达/文案完整性规则：从 soloapi.cn 采集时，不能只保存列表卡片字段。必须打开目标选题的“雷达/文案”详情，把详情页里的文案雷达、生成文案或可复制正文一并保存到原始采集文件和 `data/radar_pool/`。若详情页无法打开、权限不足或内容为空，状态标记为“等待雷达/文案详情”，不能进入正式发布包。

采集栏目规则：老师网站已取消“官方扶持”生产入口。后续采集只允许使用“今日爆点”，`source_column` 必须为 `今日爆点`。

当日采集规则：生产只能使用当天采集、且 `source_date` 等于当天日期的选题。历史库存选题不得进入新的筛选卡、Shared 参数或生产包。当天没有可用选题时，流程必须回到老师网站爆点文案源重新采集；不得为了继续生产而启用过期库存。

### 筛选结构 V2：Hard Gate → Internal Ranking → External Signal → 相对排序

Selection 不判断"这是不是热点"，只判断"今天已采到的候选里，哪一条最值得占用发布位"。这是 Ranking（相对排序）问题，不是 Absolute Scoring（绝对评分）问题。详细定义见 `templates/radar_selection_rules.md`。

**① Hard Gate（任一 FAIL → 不发，直接停止排序）**

- G1｜Source Completeness：完整雷达详情是否存在
- G2｜Fact Boundary：核心事实是否足够明确，能否不自行补事实成文
- G3｜Risk Boundary：是否存在当前无法处理的事实/法律/安全风险
- G4｜Freshness：是否仍处于有效发布窗口

**② Internal Ranking（Gate 通过后，用于当日候选排序，不相加不折算分数）**

- Public Relevance（大众相关度）：命中 [Reader Model](READER_MODEL_V1.md) 五按钮（钱/工作/规则/公平/家庭）中哪几个，高 / 中 / 低
- Stakes（利益/风险）：命中按钮上的具体损失/错过，高 / 中 / 低
- Conflict Clarity（冲突清晰度）：高 / 中 / 低
- Discussion Tension（讨论张力）：高 / 中 / 低

Reader Model 只用于 Selection 判断和 Quality Review 的 Reader Promise 检查，不进入 Transform 生成层——Transform 仍然只执行 Original Radar Production Prompt。

**③ External Signal（外部信号，与②并列参考，禁止相加）**

- 老师网站/平台今日爆款评分：0-100
- 来源标签

外部评分可能已包含冲突、热度、传播性等因素，与内部排序变量相加属于 Double Counting（重复计权）。

### 最小筛选参数

- 文案ID
- 原标题
- 热点类型
- G1-G4 Gate 结果与说明
- Public Relevance / Stakes / Conflict Clarity / Discussion Tension：高 / 中 / 低
- 命中 Reader Model 按钮：钱 / 工作 / 规则 / 公平 / 家庭（可多选，写明命中理由）
- 今日爆款评分：0-100
- 来源标签
- 今日优先级：P1 / P2 / P3 / 不发
- 入选理由

### 优先级

- P1：当天最值得优先占用发布位
- P2：次优先
- P3：有空位再生产
- 不发：Gate 未通过，或综合判断不值得占用当天发布位

优先级代表当日候选之间的相对排序，不代表绝对分数线，只决定生产顺序，不决定生成篇数。

### 独立性纪律

Selection 不根据未经验证的历史"爆文规律"（如标题是否疑问句、字数长短等内容表现层面的候选/待验证发现）挑题。这类结论研究的是文章写法层面的表现特征，与素材选择层面的可靠规则性质不同，Selection 与 Baseline Review 保持独立判断路径。

## 参数结构

```text
老师网站爆点文案池
  ↓
爆点文案筛选卡
  ↓
今日入选文案
  ↓
雷达原文（含 Original Radar Production Prompt）
  ↓
Transform（Execution Adapter）
  ↓
Article Draft
  ↓
Fact Boundary Review
  ↓
Revision（如有）
  ↓
Quality Review（参照 Shared 七项）
  ↓
Article Master
```

Shared 七项不再位于生成路径上，只在 Quality Review 阶段作参照，见下方"Review｜Radar Source"。

### 第一层：雷达原文与雷达/文案详情

原文永久冻结，不允许修改。从 soloapi.cn 采集时，雷达/文案详情是 Transform 的第一依据，必须与列表卡片一并保存。详情页里"给GPT的创作任务单"是 Original Radar Production Prompt，逐字执行，不二次解释。

## Transform｜Radar Source

输入：

- Original Radar Production Prompt（雷达/文案详情原文，含创作任务单）
- Target Format Contract（今日头条图文，见 `TRANSFORM_STANDARD_V1.md`）
- Fact Boundary（见 `TRANSFORM_STANDARD_V1.md`）

要求：

- Transform 生产依据必须是 soloapi.cn 目标选题详情页里的"雷达/文案"内容，逐字执行创作任务单，不用自己的一套规则重新指导"核心冲突怎么写、怎么推进、普通人怎么代入"——这些交给 Original Radar Production Prompt 本身。
- 篇幅受 [Frozen Output Constraints](TRANSFORM_STANDARD_V1.md#frozen-output-constraints) 约束：先判断雷达给出的 Source Format 与目标今日头条图文的 Target Format 是否一致——一致时，雷达标注的终审字数/段数原样继承；不一致（例如雷达给的是短视频口播规格）时，只继承内容层的 Narrative Spine（叙事节点顺序），不继承源格式的时长、字数区间和拍法要求，按 Target Format Contract 展开成完整头条图文——一个叙事节点可以展开成多个自然段，正文段落数不等于源格式的节点数。
- 受 Fact Boundary 约束：不得新增源材料未确认的具体人物行为、事件过程、时间地点、主观认知、因果关系、收费披露状态、具体运作机制、舆情/效果数据、确定性评价；一般性分析必须与本案已确认事实区分。
- 输出 Article Draft（未经审核，不是最终稿）。

## Review｜Radar Source

Article Draft 生成后，进入两轮独立审核，不能合并成一轮：

### 第一轮：Fact Boundary Review

只回答一个问题：**每一条陈述，本案 Source 能不能支持？** 不管好不好看，不判断结构和展开是否充分。

逐句核对 Article Draft 与雷达详情原文，标出：

- 未经确认的具体人物行为、事件过程、时间地点
- 未经确认的主观认知、因果关系
- 未经确认的收费/信息披露状态
- 未经确认的具体运作机制
- 未经确认的舆情/效果数据
- 未加区分、读起来像本案已证实的一般性推演

Fact Boundary Review 不能由生成 Article Draft 的同一次生成过程"自我审计"替代，必须是独立的一轮检查——生成模型很容易把自己的推断当成"合理分析"放过。

输出：PASS（进入 Quality Review）/ REVISION（列出具体句子，退回 Claude 做最小修改，只改被标出的句子，不改结构和展开方式）。

### 第二轮：Quality Review

只有 Fact Boundary Review PASS 之后才进行。检查：

- Shared 七项覆盖：原始事实、核心冲突、核心利益、目标人群、普通人代入、风险或成本、评论入口，逐项确认有没有丢、有没有写偏。Shared 七项在这里的角色是审核参照，不是生成参数。
- Reader Promise 检查：成品是否真的完成了 [Reader Model](READER_MODEL_V1.md) 在 Selection 阶段标注的按钮承诺，而不只是叙述完整。
- 标题选择（从候选标题中选定，不新造标题），并核对 Title Candidate Rule（见下）
- 结构顺序、核心意思、传播能力、阅读体验是否符合 [Target Format Contract](TRANSFORM_STANDARD_V1.md#target-format-contract今日头条图文)

输出：PASS（进入 Publish）/ REVISION（退回 Claude 修改）/ REJECT（结束本次生产）。

### Title Candidate Rule（标题候选规则，前瞻验证中）

依据：[`FEATURE_EXTRACTION_SCHEMA_V3_TITLE_RESOLUTION.md`](FEATURE_EXTRACTION_SCHEMA_V3_TITLE_RESOLUTION.md)。46 篇盲标复盘发现：`title_resolves_outcome=TRUE`（标题已经把核心结果/原因/怎么办讲完）的 CTR 中位数（0.143%）明显低于 `FALSE`（留有信息缺口，0.321%），剔除单点异常值后方向不变，已达到该报告定义的 Candidate Production Rule 门槛，但**尚未经过下一批真实发布的前瞻验证**。

Quality Review 阶段执行方式：

- 对候选标题标注 `title_resolves_outcome`（TRUE/FALSE），记录在案，不作为 PASS/REVISION/REJECT 的判断依据（**不是 Hard Gate**）。
- 倾向选择 FALSE（留有信息缺口）的候选标题，但不得为了留缺口而扭曲标题与事实的对应关系。
- 该标注进入 Feedback，用于前瞻验证；前瞻验证通过之前，不得把它固化为强制 Gate 或独立 Packaging Module。

Fact Review 和 Quality Review 不能混着做——用"文章终于好看了"降低事实审查标准，或者因为发现事实问题就把文章压得僵硬，都是把两件事混在一起导致的。

## 数据记录

每篇记录：

- 原始选题ID
- 生产方式：Radar Source
- 标题
- 命中 Reader Model 按钮（Selection 阶段标注）
- `title_resolves_outcome`（Quality Review 阶段标注，TRUE/FALSE）
- 发布时间
- 展现量
- 阅读量
- 点击率（CTR = 阅读量 / 展现量）
- 阅读时长
- 点赞
- 评论
- 收益

字段来自真实后台导出（见 `data/metrics/`），Feedback 记录字段不得少于后台实际可采集的字段——字段缺口本身就是需要修的 Bug，不是"以后再说"的扩展项。

## Validation（Feedback 闭环）

Feedback 收集的数据用于验证三类假设，缺 Validation，Reader Model / Title Candidate Rule / 正文规律最终都会退化成"我感觉这个有效"：

| 假设 | 输入信号（来自 Feedback） | 验证的环节 |
| --- | --- | --- |
| Selection 假设 | 命中 Reader Model 按钮 → 展现量、阅读量 | Selection 判断是否真的挑出了值得占用发布位的素材 |
| Title 假设 | `title_resolves_outcome` → CTR（阅读量/展现量） | Title Candidate Rule 是否在前瞻批次里成立 |
| 正文假设 | Shared 七项覆盖、Reader Promise 完成度 → 阅读时长、评论、互动 | 正文是否真正完成了利益关联，而不只是叙述完整 |

Validation 不是新增 Stage，是 Feedback 之后的最小闭环动作：每次复盘先按这三类分别定位（展现问题 / CTR问题 / 阅读时长与互动问题），再决定改 Selection、改标题候选还是改 Transform 依据的雷达原文，不允许跳过定位直接下"选题不行"这类笼统结论。

## 本轮范围

- 完成唯一 Transform 主链，Transform 收缩为 Execution Adapter（Original Radar Production Prompt + Target Format Contract + Fact Boundary）。
- Review 拆分为 Fact Boundary Review 与 Quality Review 两轮独立审核。
- Shared 七项角色从生成参数改为 Quality Review 参照清单。
- 固定数据字段。
- 固定 Review → Revision / Publish → Feedback 生命周期。

不要修改现有知乎系统，不要新增复杂数据库，不要重新设计大 Prompt。

## 本轮范围（Reader Model / Title Candidate Rule / Validation 接口）

- 新增 [`READER_MODEL_V1.md`](READER_MODEL_V1.md)，作为 Selection R1/R2 判断模型，同时供 Quality Review Reader Promise 检查、Feedback/Validation 使用。不新增 Stage，不进入 Transform。
- Title Candidate Rule（`FEATURE_EXTRACTION_SCHEMA_V3_TITLE_RESOLUTION.md`）接入 Quality Review，作为标题选择时的软倾向，不作为 Hard Gate，前瞻验证通过前不固化为独立 Packaging Module。
- Feedback 数据记录字段从 8 项扩展为对齐真实后台可采集字段（展现量、点击率、阅读时长等），并新增 Validation 小节，把 Feedback 数据显式对应到 Selection / Title / 正文三类假设的验证。
