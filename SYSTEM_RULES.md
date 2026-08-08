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
Radar Source
↓
Shared
↓
Transform
↓
Article Master
↓
Review
↓
Revision / Publish
↓
Feedback
```

`Radar Source` 是 Transform Method，不是独立生命周期。

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

- Public Relevance（大众相关度）：高 / 中 / 低
- Stakes（利益/风险）：高 / 中 / 低
- Conflict Clarity（冲突清晰度）：高 / 中 / 低
- Discussion Tension（讨论张力）：高 / 中 / 低

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
雷达原文
  ↓
Shared 七项
  ↓
Transform 参数
  ↓
Article Master
```

### 第一层：雷达原文与雷达/文案详情

原文永久冻结，不允许修改。从 soloapi.cn 采集时，雷达/文案详情是 Transform 的第一依据，必须与列表卡片一并保存。

### 第二层：Shared 七项

Transform 必须完整继承：

- 原始事实
- 核心冲突
- 核心利益
- 目标人群
- 普通人代入
- 风险或成本
- 评论入口

### 第三层：Transform 参数

Transform 参数用于约束平台化表达：

- 不机械照抄雷达原句。
- 保留雷达已经确认的结构、节奏、核心冲突和表达动作。
- 完整继承 Shared 七项。
- 允许为今日头条重新组织句式和表达，但不得改变事实与核心推进。

## Transform｜Radar Source

输入：

- 雷达/文案详情
- 原始事实
- Shared 七项

要求：

- Transform 生产依据必须是 soloapi.cn 目标选题详情页里的“雷达/文案”内容。
- 列表卡片、筛选卡和 Shared 参数只能作为辅助校验，不能替代“雷达/文案”详情。
- 保留雷达/文案详情里的终审结构、核心冲突、结构顺序、普通人代入和评论入口。
- 不机械照抄原句。
- 允许重新组织句式、标题、篇幅、排版和头条表达。
- 不改变事实与核心推进。
- 输出 Article Master。

## 数据记录

每篇只记录：

- 原始选题ID
- 生产方式：Radar Source
- 标题
- 发布时间
- 阅读量
- 点赞
- 评论
- 收益

## 本轮范围

- 完成唯一 Transform 主链。
- 完成 Selection、Radar Source、Shared、Transform 参数。
- 固定数据字段。
- 固定 Review → Revision / Publish → Feedback 生命周期。

不要修改现有知乎系统，不要新增复杂数据库，不要重新设计大 Prompt。
