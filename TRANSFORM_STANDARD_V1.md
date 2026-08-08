# Transform Standard V1

## Purpose

将老师网站已经验证的爆点文案，在保持传播能力的前提下，转换为符合今日头条平台的可发布文案。

Transform means conversion, not creation.

## Responsibility

Transform is responsible for:

- 平台适配
- 输出头条文案

Transform is not responsible for:

- 重新选题
- 修改标题方向
- 重写结构
- 审核
- 发布

## Boundary

Transform allows:

- 平台表达
- 平台敏感词处理
- 段落格式
- 排版
- 标点
- 语气微调
- 篇幅控制（受 [Frozen Output Constraints](#frozen-output-constraints) 约束，见下）

Transform forbids:

- 修改标题方向
- 修改核心冲突
- 修改结构顺序
- 修改核心意思
- 增加新观点
- 删除关键论证
- 改变情绪推进
- 重新创作

## Frozen Output Constraints

雷达详情里的成品规格分两层，Transform 必须先分清楚再决定继承什么：

- **内容层（Content Layer）**：核心事实、核心冲突、普通人代入、情绪推进、评论入口，以及各内容节点之间的推进顺序——这是一条 **Narrative Spine（叙事主轴）**，例如 Hook → Fact → Conflict → Ordinary-person Stakes → Comment，它规定的是"哪个内容节点在前、哪个在后"，不规定"正文必须是几个自然段"。这一层始终 Preserve，与目标平台无关。
- **源平台成品层（Source Format Layer）**：雷达详情给出的具体成品规格，例如时长、段数、字数区间、口播/图文等载体形式、拍法要求。这一层是否继承取决于 Source Format 与 Target Format 是否一致。

判断规则：

- **同格式转换**（Source Format 与 Target Format 相同，例如雷达给的就是头条图文规格）：源平台成品层的具体规格（如字数区间）构成 Frozen Output Constraints，必须原样继承，不得放大或缩小体量。
- **跨格式转换**（Source Format 与 Target Format 不同，例如雷达给的是短视频口播 45秒/五段/150-220字，Target 是今日头条图文文章）：源平台成品层的具体规格（时长、字数区间、口播节奏、拍法）**不继承**；只继承内容层的 Narrative Spine（叙事节点顺序、核心冲突、事实、普通人代入、评论入口）。Transform 需要把 Narrative Spine 上的每个节点，按目标格式的成品标准（见下方 Target Format Contract）展开成完整表达——**一个叙事节点可以展开成目标格式里的多个自然段，节点数量不等于目标格式的段落数量**，不能把"源格式有几个节点"直接理解成"目标格式写几段"。

跨格式转换时，字数不预设固定区间，标准是"足够完整地展开内容层骨架，不为了凑字数扩写、也不因为要贴合源格式字数而机械压缩"。

## Target Format Contract：今日头条图文

跨格式转换的目标格式如果是今日头条图文文章，成品必须满足：

- 是完整图文文章，不是口播稿的文字版——不能保留"3秒开头""45秒结构"这类口播节奏留下的痕迹。
- Hook（开头）保留，但正文需要把 Fact（事实经过）交代完整，不能因为要贴合源格式的简短节奏而把事实压缩成一句话。
- Narrative Spine 上的每个节点，允许展开成一个或多个自然段；不要求正文段落数与源格式的节点数一一对应，也不强制固定为某个段落数。
- 不能为了拉长篇幅而新增源材料没有的事实、观点或推断；字数由内容本身需要的展开程度决定，不设固定区间。
- 成品标准是"读者不需要额外上下文，独立阅读即可看懂事情经过、核心冲突和为什么与自己有关"。
- 结尾保留 Narrative Spine 里的 Comment（评论入口），不额外新增评论问题。

Transform 在动笔前必须先确认 Source Format 与 Target Format 是否一致，这个判断结果决定了后续走同格式路径还是跨格式路径，不能省略。

## Primary Owner

Claude

## Assist

None

## Deliverable

头条文案

This is the first transformed draft, not the final publishable draft.

## State

```text
Ready for Transform
↓
Transforming
↓
Generated
↓
Ready for Review
```

## Input

老师原文

Transform does not accept:

- AI 总结
- 半截文案
- 摘要
- 二次整理

## Output

头条文案 V1

Later changes belong to Revision, not Transform.

## Transform Target

Today Toutiao

## Transform Standard

Keep:

- 标题
- 结构
- 核心意思
- 情绪推进

Adapt:

- 平台表达
- 平台格式
- 平台排版
- 平台敏感词

Summary:

保持传播能力，只做平台适配。

## Zero Optimization Principle

Transform forbids active optimization.

Claude is not responsible for making the article better.

Claude is responsible for preserving the original distribution potential and completing platform adaptation.

Unless the system explicitly authorizes it, Claude must not actively:

- 优化
- 改写
- 增强
- 精简逻辑
- 增加观点
- 删除观点
- 调整结构

## Production Method（生产方法）

Transform 内部使用唯一生产方法：**Radar Source**。

Radar Source 以 soloapi.cn 目标选题详情页里的“雷达/文案”内容为事实和结构第一依据，完整继承 **Shared 七项**：

- 原始事实
- 核心冲突
- 核心利益
- 目标人群
- 普通人代入
- 风险或成本
- 评论入口

Transform 保留雷达已经确认的结构、节奏、核心冲突和表达动作；不机械照抄雷达原句；允许为今日头条重新组织句式和表达，但不得改变事实与核心推进。

Radar Source、Shared 七项和 Transform 参数的完整规则定义在 [`SYSTEM_RULES.md`](SYSTEM_RULES.md)（雷达生产主链 v1），该文件是 Transform Stage 的执行层规范，与本文件（Transform 的边界与零优化原则）是同一 Stage 内的两份互补文档，不是并行或竞争的规范。

## Transform Action Model

Transform has only two actions:

- Preserve
- Adapt

Preserve means keeping:

- 标题
- 结构
- 意思
- 情绪推进

Adapt means adapting:

- 平台表达
- 平台格式
- 平台排版
- 敏感词

Transform is not Rewrite.

Transform equals Preserve plus Adapt.
