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
爆点文案筛选卡
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
        ↓
Review
        ↓
Revision / Publish
        ↓
Feedback
```

所有规则仅用于今日头条，不调用知乎或其他平台规则。

## 三层参数结构

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

Shared 七项用于保证 Article Master 继承同题、同事实、同核心冲突、同普通人代入、同风险成本和同评论入口。Transform 参数用于约束平台化表达：不机械照抄雷达原句，但不得改变事实与核心推进。

## 爆点文案筛选层

筛选对象是老师网站已经生成完成的爆点文案，不是原始热点。
筛选前必须先把文案雷达完整原文保存到 `data/radar_pool/`。

`data/radar_pool/` 必须只保存真实来源内容：从老师爆款文案网站采集/导出的完整原文，或用户明确粘贴并确认来自该网站的完整原文。禁止为了测试流程自行编造选题、评分、来源标签或伪造“今日爆点”来源；没有真实原文时，只能停在“等待采集”状态。

从 soloapi.cn 采集时，必须打开目标选题的“雷达/文案”详情，把详情页里的文案雷达、生成文案或可复制正文同步保存。只采列表卡片不算完整采集；如果详情页无法打开或内容为空，只能标记为“等待雷达/文案详情”，不能进入正式发布包。

采集栏目规则：网站已取消“官方扶持”生产入口，后续只采“今日爆点”；`source_column` 必须为 `今日爆点`。

生产当日规则：只生产当天采集的选题，`source_date` 必须等于当天日期。当天没有可用选题时，必须回到老师网站爆点文案源重新找；不能拿历史库存硬生产。

默认老师网站产出的文案已经合格，所以这里不判断“文案写得好不好”，只判断它值不值得占用今天的头条发布位。

每篇爆点文案只记录：

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

优先级规则：

- P1：优先生产
- P2：可以生产
- P3：有空位再生产
- 不发：暂不进入生产

评分处理：

- 同等条件下，优先选择今日爆款评分高的文案。
- 评分高不能覆盖账号不适配、事实风险高、热点过时等硬伤。
- 今日爆款评分高，且账号适配、普通人相关度、冲突强度为高时，优先进入 P1。

## 每日标准流程

1. 老师网站爆点文案进入 `data/radar_pool/`。
2. 保存文案雷达完整原文，原文不改写。
3. 生成爆点文案筛选卡，筛选卡必须引用已保存的雷达内容文件，判断 P1 / P2 / P3 / 不发。
4. 今日入选文案进入原文库，原文永久冻结。
5. 提取 Shared 七项：原始事实、核心冲突、核心利益、目标人群、普通人代入、风险或成本、评论入口。
6. Transform：使用“雷达原文 + Shared 七项 + Transform 参数”生成 Article Master。
7. Review 后进入 Revision 或 Publish。
8. 发布后进入 Feedback，并与 Baseline 对照。

## Transform｜Radar Source

输入：

- 雷达/文案详情
- 原始事实
- Shared 七项

要求：

- Transform 生产依据必须是 soloapi.cn 目标选题详情页里的“雷达/文案”内容
- 列表卡片、筛选卡和 Shared 参数只能作为辅助校验，不能替代“雷达/文案”详情
- 保留雷达/文案详情里的终审结构、核心冲突、结构顺序、普通人代入和评论入口
- 不照抄原句
- 允许重新组织句式、标题、篇幅、排版和头条表达
- 输出 Article Master

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
- 篇幅
- 事实补充

禁止修改：

- 雷达/文案详情里的开头核心冲突
- 雷达/文案详情里的段落推进顺序
- 雷达/文案详情里的普通人代入逻辑
- 雷达/文案详情里的利益与风险表达
- 雷达/文案详情里的评论入口

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
  --account-fit 高 \
  --public-relevance 高 \
  --conflict-strength 高 \
  --benefit-risk-strength 高 \
  --comment-space 中 \
  --time-window 长 \
  --viral-score 92 \
  --source-label "确认S+·92分；素材质量78·可用" \
  --priority P1 \
  --reason "账号适配高，普通人相关度高，适合优先生产"
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
