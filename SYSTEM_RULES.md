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

硬性规则：筛选前必须先保存文案雷达完整原文到 `data/radar_pool/`。筛选卡、Shared 和生产包都必须引用这份已保存原文，不能只保存摘要或筛选结果。

来源真实性硬性规则：`data/radar_pool/` 只允许进入两类内容：

- 从老师爆款文案网站真实采集/导出的完整原文。
- 用户明确粘贴并确认来自老师爆款文案网站的完整原文。

禁止为了测试流程自行编造选题、评分、来源标签或伪造“今日爆点”来源。若没有真实网站原文，流程状态只能标记为“等待采集”，不能生成筛选卡或发布包。

雷达/文案完整性规则：从 soloapi.cn 采集时，不能只保存列表卡片字段。必须打开目标选题的“雷达/文案”详情，把详情页里的文案雷达、生成文案或可复制正文一并保存到原始采集文件和 `data/radar_pool/`。若详情页无法打开、权限不足或内容为空，状态标记为“等待雷达/文案详情”，不能进入正式发布包。

采集栏目规则：老师网站已取消“官方扶持”生产入口。后续采集只允许使用“今日爆点”，`source_column` 必须为 `今日爆点`。

当日采集规则：生产只能使用当天采集、且 `source_date` 等于当天日期的选题。历史库存选题不得进入新的筛选卡、Shared 参数或生产包。当天没有可用选题时，流程必须回到老师网站爆点文案源重新采集；不得为了继续生产而启用过期库存。

### 最小筛选参数

- 文案ID
- 原标题
- 热点类型
- 账号适配：高 / 中 / 低
- 普通人相关度：高 / 中 / 低
- 冲突强度：高 / 中 / 低
- 利益或风险强度：高 / 中 / 低
- 评论空间：高 / 中 / 低
- 热点剩余时效：长 / 中 / 短
- 今日爆款评分：0-100
- 今日优先级：P1 / P2 / P3 / 不发
- 来源标签
- 入选理由

### 优先级

- P1：优先生产
- P2：可以生产
- P3：有空位再生产
- 不发：暂不进入生产

优先级只决定生产顺序，不决定生成篇数。

### 评分加权

- 同等条件下，优先选择今日爆款评分高的文案。
- 评分高不能覆盖账号不适配、事实风险高、热点过时等硬伤。
- 今日爆款评分高，且账号适配、普通人相关度、冲突强度为高时，优先进入 P1。
- 今日爆款评分高但综合条件不足以占用 P1 时，优先考虑 P2。

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
