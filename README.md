# Today Toutiao System

## Module Status

| Module | Version | Status |
| --- | --- | --- |
| Collect | V1 | FROZEN |
| Transform | V1 | FROZEN |
| Review | V1 | FROZEN |
| Revision | V1 | DRAFT |
| Publish | V1 | DRAFT |
| Feedback | V1 | DRAFT |

Status lifecycle:

```text
DRAFT
↓
REVIEW
↓
FROZEN
↓
ACTIVE
```

# 采集老师爆点文案系统

正式方向：唯一 Production Line。

```text
老师网站爆点文案池
        ↓
List Scan
        ↓
Pre-Filter
        ↓
Detail Fetch
        ↓
爆点文案筛选卡
        ↓
今日入选文案
        ↓
冻结完整雷达原文（含 Original Radar Production Prompt）
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

所有规则仅用于今日头条，不调用知乎或其他平台规则。

## 生产结构

```text
老师网站爆点文案池
  ↓
爆点文案筛选卡
  ↓
今日入选文案
  ↓
雷达原文（含 Original Radar Production Prompt）
  ↓
Transform：Target Format Contract + Fact Boundary
  ↓
Article Draft
  ↓
Fact Boundary Review（独立一轮，只判断事实边界）
  ↓
Quality Review（独立一轮，参照 Shared 七项判断覆盖与阅读质量）
  ↓
Article Master
```

Transform 不再用自己的一套规则重新指导"核心冲突怎么写、怎么推进、普通人怎么代入"——这些交给雷达详情里的 Original Radar Production Prompt 本身逐字执行。Transform 只负责两件事：Target Format Contract（输出成什么载体）、Fact Boundary（什么不能编）。Shared 七项不再是生成参数，降级为 Quality Review 阶段的参照清单，用来检查 Article Draft 有没有丢核心事实/核心冲突/核心利益/目标人群/普通人代入/风险成本/评论入口。

## 爆点文案筛选层

筛选对象是老师网站已经生成完成的爆点文案，不是原始热点。

Collect 内部先做轻筛：

```text
List Scan
  ↓
Pre-Filter
  ↓
Detail Fetch
```

Pre-Filter = Acquisition Decision（采集决策），只回答“这条是否值得花一次详情采集成本”。它只看标题、榜单位置、列表评分/标签、来源日期等廉价信息，只输出 FETCH / SKIP / REVIEW，不输出 P1 / P2 / P3。

Pre-Filter 只做明显淘汰：标题本身看不出大众相关性、没有明确冲突/利益/风险信号、或热点明显不新鲜时才 SKIP；不确定时不能淘汰。

Detail Fetch 后，必须先把文案雷达完整原文保存到 `data/radar_pool/`，才能进入 Selection V2。

`data/radar_pool/` 必须只保存真实来源内容：从老师爆款文案网站采集/导出的完整原文，或用户明确粘贴并确认来自该网站的完整原文。禁止为了测试流程自行编造选题、评分、来源标签或伪造“今日爆点”来源；没有真实原文时，只能停在“等待采集”状态。

从 soloapi.cn 采集时，必须打开目标选题的“雷达/文案”详情，把详情页里的文案雷达、生成文案或可复制正文同步保存。只采列表卡片不算完整采集；如果详情页无法打开或内容为空，只能标记为“等待雷达/文案详情”，不能进入正式发布包。

采集栏目规则：网站已取消“官方扶持”生产入口，后续只采“今日爆点”；`source_column` 必须为 `今日爆点`。

生产当日规则：只生产当天采集的选题，`source_date` 必须等于当天日期。当天没有可用选题时，必须回到老师网站爆点文案源重新找；不能拿历史库存硬生产。

默认老师网站产出的文案已经合格，所以这里不判断“文案写得好不好”，只判断它值不值得占用今天的头条发布位。这是一个 Ranking（当日候选相对排序）问题，不是 Absolute Scoring（绝对评分）问题。详细规则见 `templates/radar_selection_rules.md`。

**① Hard Gate（任一 FAIL → 不发，直接停止排序）**：

- G1｜Source Completeness：完整雷达详情是否存在
- G2｜Fact Boundary：核心事实是否足够明确，能否不自行补事实成文
- G3｜Risk Boundary：是否存在当前无法处理的事实/法律/安全风险
- G4｜Freshness：是否仍处于有效发布窗口

**② Internal Ranking（Gate 通过后，用于当日候选排序）**：

- Public Relevance（大众相关度）：高 / 中 / 低
- Stakes（利益/风险）：高 / 中 / 低
- Conflict Clarity（冲突清晰度）：高 / 中 / 低
- Discussion Tension（讨论张力）：高 / 中 / 低

四项不相加、不折算分数，只用于比较当日候选谁更值得优先占位。

**③ External Signal（外部信号，不与②相加，并列参考）**：

- 老师网站/平台今日爆款评分：0-100
- 来源标签（如 S+/素材质量等）

外部评分很可能已经包含了冲突、热度、传播性等因素，与内部排序变量相加属于 Double Counting（重复计权），禁止相加。

每篇爆点文案只记录：

- 文案ID
- 原标题
- 热点类型
- G1-G4 Gate 结果与说明
- Public Relevance / Stakes / Conflict Clarity / Discussion Tension：高 / 中 / 低
- 今日爆款评分：0-100
- 来源标签
- 今日优先级：P1 / P2 / P3 / 不发
- 入选理由

**④ 相对排序**：

- P1：当天最值得优先占用发布位
- P2：次优先
- P3：有空位再生产
- 不发：Gate 未通过，或综合判断不值得占用当天发布位

P1/P2/P3 不代表达到某个绝对分数线，只代表当天候选之间的相对顺序；当天候选都弱时可以全部“不发”，都强时仍按相对顺序排出 P1/P2/P3。

独立性纪律：Selection 不根据未经验证的历史“爆文规律”（如标题是否疑问句、字数长短等内容表现层面的候选发现）挑题，与 Baseline Review 保持独立。

## 每日标准流程

1. 老师网站爆点文案进入 `data/radar_pool/`。
2. 保存文案雷达完整原文，原文不改写。
3. 生成爆点文案筛选卡，筛选卡必须引用已保存的雷达内容文件，判断 P1 / P2 / P3 / 不发。
4. 今日入选文案进入原文库，原文永久冻结。
5. Transform：直接执行雷达详情里的 Original Radar Production Prompt，套用 Target Format Contract 和 Fact Boundary，生成 Article Draft。
6. Fact Boundary Review：独立一轮，逐句核对 Article Draft 与雷达详情，只判断事实边界，不判断好不好看。
7. Quality Review：Fact Boundary Review PASS 后进行，参照 Shared 七项检查覆盖是否完整，判断结构、传播能力、阅读体验。
8. Review 后进入 Revision 或 Publish。
9. 发布后进入 Feedback，并与 Baseline 对照。

## Transform｜Radar Source

输入：

- Original Radar Production Prompt（雷达/文案详情原文，含创作任务单）
- Target Format Contract
- Fact Boundary

要求：

- Transform 生产依据必须是 soloapi.cn 目标选题详情页里的"雷达/文案"内容，逐字执行创作任务单，不用自己的规则重新指导怎么写
- 篇幅受 Frozen Output Constraints 约束：Source Format 与 Target Format 一致时原样继承终审字数/段数；不一致（如雷达给的是短视频规格）时只继承内容层的 Narrative Spine（叙事节点顺序），按 Target Format Contract 展开成完整头条图文
- 受 Fact Boundary 约束：不得新增源材料未确认的具体人物行为、事件过程、时间地点、主观认知、因果关系、收费披露状态、具体运作机制、舆情/效果数据、确定性评价
- 输出 Article Draft（未经审核，不是最终稿）

## 数据字段

每篇只记录：

- 原始选题ID
- 生产方式：Radar Source
- 标题
- 发布时间
- 阅读量
- 点赞
- 评论
- 收益

## 直转约束

允许修改：

- 平台格式
- 篇幅（受 Frozen Output Constraints 约束）
- 表达方式（不改变事实与核心推进）

禁止修改：

- 雷达/文案详情里的开头核心冲突
- 雷达/文案详情里的段落推进顺序
- 雷达/文案详情里的普通人代入逻辑
- 雷达/文案详情里的利益与风险表达
- 雷达/文案详情里的评论入口

禁止新增（Fact Boundary）：

- 源材料未确认的具体人物行为、事件过程、时间地点
- 源材料未确认的主观认知、因果关系
- 源材料未确认的收费/信息披露状态、具体运作机制
- 源材料未确认的舆情/效果数据、确定性评价

优先级：

```text
雷达/文案详情优先
头条适配其次
自由创作最后
```

## 发布前检查

每篇必须输出：

- 首句是否保留原冲突：是 / 否
- 核心利益是否一致：是 / 否
- 推进顺序是否一致：是 / 否
- 是否被改成说明文：是 / 否
- 评论入口是否保留：是 / 否

当“是否被改成说明文”为“是”时，禁止进入发布。

## 目录

```text
data/
  raw/            临时原始输入
  radar/          兼容第一版的采集归档
  radar_pool/     老师网站爆点文案池，保存文案雷达完整原文
  radar_selection/爆点文案筛选卡
  radar_sources/  雷达原文库，永久冻结
  radar_rules/    预留，现阶段不扩展复杂规律库
  metrics/        发布后数据
prompts/
  templates/      Prompt 模板
  generated/      自动生成 Prompt
outputs/
  articles/
    draft/        GPT 初稿
    reviewed/     人工审核稿
    published/    已发布稿
  reports/        复盘报告
  daily_runs/     每日生产运行包
                 其中包含 Shared、Transform 参数、metadata、index、position
database/         后续 SQLite 数据库
notion/
  sync_logs/      Notion 同步记录
scripts/          自动化脚本
templates/        研究轨与生产轨固定模板
```

## 第一版命令兼容

```bash
python3 scripts/collect_radar.py data/raw/sample_radar.md
python3 scripts/generate_prompt.py data/radar/sample_radar.collected.md
```

## 雷达生产命令

先保存雷达文案原文：

```bash
python3 scripts/save_radar_content.py data/raw/sample_radar.md \
  --title "轻资产普通人创业" \
  --hotspot-type "副业创业" \
  --source-date "2026-07-29" \
  --source-column "今日爆点" \
  --source-label "确认S+·92分；素材质量78·可用"
```

再生成筛选卡：

```bash
python3 scripts/select_radar.py data/radar_pool/保存后的雷达文件.radar.md \
  --title "轻资产普通人创业" \
  --hotspot-type "副业创业" \
  --source-date "2026-07-29" \
  --gate-source-completeness PASS \
  --gate-fact-boundary PASS \
  --gate-risk-boundary PASS \
  --gate-freshness PASS \
  --gate-notes "详情页完整，事实清楚，无事实/法律风险，仍在发布窗口内" \
  --public-relevance 高 \
  --stakes 高 \
  --conflict-clarity 高 \
  --discussion-tension 中 \
  --viral-score 92 \
  --source-label "确认S+·92分；素材质量78·可用" \
  --priority P1 \
  --reason "大众相关度高，利益点具体，冲突清晰，适合优先生产"
```

入选后进入生产主链：

```bash
python3 scripts/daily_radar_run.py data/raw/sample_radar.md \
  --title "轻资产普通人创业" \
  --hotspot-type "副业创业" \
  --source-date "2026-07-29" \
  --original-type "雷达文案" \
  --selection-card "data/radar_selection/筛选卡文件名.selection.md"
```
