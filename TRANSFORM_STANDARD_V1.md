# Transform Standard V1

## Purpose

将老师网站已经验证的爆点文案，转换为符合今日头条平台的可发布文案。

## History（为什么这版比上一版规则更少）

V1-V6 的生产实验（见 `outputs/articles/draft/2026-08-08_搬家报价570元-要5060元才肯上楼_native_invocation_test.md`）证明：让 Transform 自己重新指导"怎么写"（Preserve 哪些、Adapt 哪些、结构该有几段）会压缩生成能力，产出僵硬的扩写稿；而直接执行雷达详情里的 Original Radar Production Prompt，生成质量明显更好，但会产生未经 Source 支持的事实外推。

结论：Transform 不应该再承担"重新解释怎么写"的角色，只应该是一个 **Execution Adapter（执行适配器）**。

## Execution Adapter Model

Transform 的生成指令来自三个部分，且只有三个部分：

1. **Original Radar Production Prompt**：雷达详情里"给GPT的创作任务单"原文，逐字执行，不二次解释、不额外补充写作规则。这是 Primary Generation Instruction。
2. **Target Format Contract**：只回答"输出成什么载体"（见下）。
3. **Fact Boundary**：只回答"什么不能编"（见下）。

冲突/普通人代入/情绪推进/评论入口该怎么展开、怎么推进——全部交给 Original Radar Production Prompt 本身，Transform 不再用一套独立的 Preserve/Adapt 规则去二次指导。

Shared 七项不再是生成参数，降级为 Review 阶段的参照清单（见 `SYSTEM_RULES.md` 的 Review 章节），不进入生成指令。

## Fact Boundary

不得新增源材料未确认的：

- 具体人物行为
- 具体事件过程
- 时间地点
- 主观认知（如"她觉得""这让她意识到"）
- 因果关系（如"因为……所以……"式的机制推演）
- 收费/信息披露状态（如"没有提前说清楚""等到……才告知"）
- 具体运作机制（如强制手段的具体方式）
- 舆情或效果数据（如热度、传播反馈）
- 确定性评价（如带定性色彩的判断词）

一般性分析允许展开（例如"搬家是低频消费，普通人较难提前摸清收费结构"这类不针对本案具体过程的常识性陈述），但必须与本案已确认事实明确区分，不得把合理推演写成本案已经发生的事实。

Fact Boundary 不能只靠生成模型自己写完之后自我审计——见 History 里链接的实验记录，生成模型很容易把自己的推断标记为"合理分析"然后放行。必须由独立的 Fact Boundary Review（见 `SYSTEM_RULES.md`）在生成之后单独检查，不得省略。

## Frozen Output Constraints

雷达详情里的成品规格分两层，Transform 必须先分清楚再决定继承什么：

- **内容层（Content Layer）**：核心事实、核心冲突、普通人代入、情绪推进、评论入口，以及各内容节点之间的推进顺序——这是一条 **Narrative Spine（叙事主轴）**，例如 Hook → Fact → Conflict → Ordinary-person Stakes → Comment，它规定的是"哪个内容节点在前、哪个在后"，不规定"正文必须是几个自然段"。这一层始终 Preserve，与目标平台无关。
- **源平台成品层（Source Format Layer）**：雷达详情给出的具体成品规格，例如时长、段数、字数区间、口播/图文等载体形式、拍法要求。这一层是否继承取决于 Source Format 与 Target Format 是否一致。

判断规则：

- **同格式转换**（Source Format 与 Target Format 相同，例如雷达给的就是头条图文规格）：源平台成品层的具体规格（如字数区间）构成 Frozen Output Constraints，必须原样继承，不得放大或缩小体量。
- **跨格式转换**（Source Format 与 Target Format 不同，例如雷达给的是短视频口播 45秒/五段/150-220字，Target 是今日头条图文文章）：源平台成品层的具体规格（时长、字数区间、口播节奏、拍法）**不继承**；只继承内容层的 Narrative Spine。Transform 需要让 Original Radar Production Prompt 在目标格式下自然展开，**一个叙事节点可以展开成目标格式里的多个自然段，节点数量不等于目标格式的段落数量**。

跨格式转换时，字数不预设固定区间，标准是"足够完整地展开内容层骨架，不为了凑字数扩写、也不因为要贴合源格式字数而机械压缩"。

## Target Format Contract：今日头条图文

跨格式转换的目标格式如果是今日头条图文文章，成品必须满足：

- 是完整图文文章，不是口播稿的文字版——不能保留"3秒开头""45秒结构"这类口播节奏留下的痕迹。
- Hook（开头）保留，但正文需要把 Fact（事实经过）交代完整，不能因为要贴合源格式的简短节奏而把事实压缩成一句话。
- Narrative Spine 上的每个节点，允许展开成一个或多个自然段；不要求正文段落数与源格式的节点数一一对应，也不强制固定为某个段落数。
- 不能为了拉长篇幅而新增源材料没有的事实、观点或推断——受 Fact Boundary 约束。
- 成品标准是"读者不需要额外上下文，独立阅读即可看懂事情经过、核心冲突和为什么与自己有关"。
- 结尾保留 Narrative Spine 里的 Comment（评论入口），不额外新增评论问题。

Transform 在动笔前必须先确认 Source Format 与 Target Format 是否一致，这个判断结果决定了后续走同格式路径还是跨格式路径，不能省略。

## Primary Owner

Claude

## Assist

None

## Deliverable

Article Draft（未经 Fact Boundary Review 的头条文案初稿，不是最终可发布稿）

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

- Original Radar Production Prompt（雷达详情原文，含"给GPT的创作任务单"）
- Target Format Contract
- Fact Boundary

Transform does not accept:

- AI 总结
- 半截文案
- 摘要
- 二次整理

## Output

Article Draft

进入 Review 后才分 Fact Boundary Review 和 Quality Review 两轮，详见 `SYSTEM_RULES.md`。Article Draft 修改后才升级为 Article Master，属于 Revision 职责，不属于 Transform。

## Production Method（生产方法）

Transform 内部使用唯一生产方法：**Radar Source**。Radar Source 直接执行 soloapi.cn 目标选题详情页里的"雷达/文案"原始创作指令（Original Radar Production Prompt），套用 Target Format Contract 和 Fact Boundary 两个执行适配约束，不再由 Transform 自己重新解释核心冲突、结构顺序、普通人代入该怎么写。

Radar Source 的完整规则定义在 [`SYSTEM_RULES.md`](SYSTEM_RULES.md)（雷达生产主链 v1），该文件是 Transform Stage 的执行层规范，与本文件是同一 Stage 内的两份互补文档，不是并行或竞争的规范。
