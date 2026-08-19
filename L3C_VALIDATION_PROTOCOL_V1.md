# L3-C Validation Protocol V1｜Reader Model 五按钮 × 新鲜度 验证协议

Status: DRAFT（尚未 FROZEN，待人工确认后锁定）

## 定位

本协议不是新的分析体系，是 [`READER_MODEL_V1.md`](READER_MODEL_V1.md) 中已经写明但从未执行的 Feedback / Validation 任务的具体操作规则，衔接在已冻结的 Baseline Review 链条（L1 → L2 → Blind Feature Extraction → L3-A → L3-B → Final，全部 FROZEN，见 [`outputs/reports/Baseline_Review_Final_2026-08-08.md`](outputs/reports/Baseline_Review_Final_2026-08-08.md)）之后，编号 L3-C。

不修改、不重跑、不引用旧的 `feature_labels_blind_2026-08-08.csv` 或 `l3_analysis_dataset_2026-08-08.csv` 中的任何判断——那批文件的 Lock Rule 依然有效。L3-C 使用新文件、新数据范围。

## Scope

数据源：`data/metrics/toutiao_metrics_2026-08-19.csv`（截至 2026-08-19 的全量已发布文章表现数据，覆盖 2026-07-16 至 2026-08-19，含原46篇基线区间，是当前口径下最新的完整拉取）。

以该文件的全部行作为 L3-C 样本池。样本量以实际去重后的行数为准，标注开始前先在 `data/baseline_review/l3c_labels_blind_2026-08-19.csv` 的表头写清楚总行数，标注完成后不得再增删行。

## Blinding Rule

标注者（人工或 AI）在填写 `interest_button_primary` 时，只能读取：

- 文章标题
- 文章正文（如可获取；仅有标题时基于标题判断，并在 `evidence_note` 注明"仅标题"）
- 对应的雷达原始素材（`data/radar_pool/`、`data/radar_sources/` 中同名文件），仅用于确认事件基本事实，不得用于判断"这篇表现好不好"

不得读取、使用或参考：

- 展现、阅读、点击率、点赞、评论、收益等任何表现列
- 任何已有的 L1/L2/L3-A/L3-B 报告或排名

`interest_button_primary` 与 `freshness_days` 必须在完全不知道该行表现数据的情况下写入，写完锁定后再与 `toutiao_metrics_2026-08-19.csv` join。

## Fields

### interest_button_primary

Type: single choice（强制单选，不允许多标签）

Allowed values：

1. 钱
2. 工作
3. 规则
4. 公平
5. 家庭
6. 无（不构成明确利益关联，或五个按钮都不占主导）

Decision rule：
依据 [`READER_MODEL_V1.md`](READER_MODEL_V1.md) 的判定链——"事件 → 影响读者哪一类现实利益 → 改变了读者的什么规则/经验/位置判断 → 读者为什么必须重新确认自己的位置"——只选**驱动读者关注的主导按钮**。多个按钮同时命中时，选叙事重心/标题落点所在的那一个，不做联合标签，避免样本被切成过多稀疏格子。选"无"必须在 `evidence_note` 写明为什么五个按钮都不适用，不能因为拿不准就默认选"无"。

### freshness_days

Type: integer（可为0或负值不允许，最小为0）

计算公式：

```
freshness_days = 文章发布日期 − 事件锚点日期
```

**事件锚点日期（event anchor date）判定规则，按优先级取第一个满足的**：

1. `event_date_explicit`：雷达原始素材（`radar_pool` / `radar_sources` 对应文件）中明确写出事件发生日期或首次公开报道日期的，用该日期。
2. `first_report_date`：雷达素材未写明确日期，但正文/标题隐含可判断的首次报道时间窗口（如"昨天""本周""8月X日"）的，用该窗口内可推断的最早日期。
3. `radar_capture_fallback`：以上都无法判断时，用该选题被抓取入池的日期（即 `radar_pool` 文件名中的日期）作为锚点，并在 `evidence_note` 标注 `fallback_used=true`。

**禁止行为**：标注者不得在完成 `interest_button_primary` 或看到任何表现数据之后，重新搜索"这个事件后来有没有二次传播/最近一轮讨论"来选择更晚的锚点日期。锚点日期只能来自选题当天已经存在、已经写入雷达文件的信息。每一行必须在 `evidence_note` 中注明使用的是上述三种规则中的哪一种（`anchor_type` 取值：`event_date_explicit` / `first_report_date` / `radar_capture_fallback`），使锚点可追溯、可复核，不能事后按对理论有利的方向重新选择。

## Output Table

写入：`data/baseline_review/l3c_labels_blind_2026-08-19.csv`

必需列：

- schema_version（固定值 `L3C_V1`）
- label_status（标注中用 `DRAFT`，全部完成后统一改为 `LOCKED_BLIND`）
- toutiao_group_id 或 title（作为与 `toutiao_metrics_2026-08-19.csv` join 的键，标题需与 metrics 文件完全一致）
- interest_button_primary
- freshness_days
- anchor_type
- evidence_note

## Outcome 分离（Join 之后，进入分析层时遵守）

三个结果变量必须分开呈现，不得合并成单一"表现好坏"判断：

- **A. 展现（impressions）**：反映平台愿不愿意继续扩大推荐池，是分发决策的信号。
- **B. CTR / 阅读转换率（reads / impressions）**：反映在已获得的展现里，标题/选题能不能让人点，与展现是两件独立的事——高展现不代表高CTR，见 08-19 数据中已出现"671展现16阅读"这类展现高但转换低的样本，不能笼统称为"表现好"。
- **C. 收益 / RPM（revenue、revenue per 1000 reads）**：反映这批读者的广告价值，与前两者都不同源。

`interest_button_primary` 和 `freshness_days` 分别与 A、B、C 三个结果独立做关联观察，不合并为一个复合分数。

## Small-N 判定标准（沿用 L3-A 口径）

- 任一按钮/锚点类型对应样本 n < 5：标注 `[Small-N]`，不得单独作为方向性结论，只记录数值。
- n = 1：单样本，不构成组间比较，只记录，不纳入方向判断。
- 若 `interest_button_primary` 六个取值中出现某值 n=0 或占比 >90%（零方差或近零方差），比照 L3-A 对 `stakes_has_action_advice` 的处理方式，标记为"无法判断"，不强行制造比较。

## 纪律（沿用 Baseline Review 全链条纪律）

- 全程不使用"因为/导致/所以"等因果表述，只报告关联方向和样本量。
- 标注完成、`label_status` 改为 `LOCKED_BLIND` 之后，不得因为看到 join 后的表现数据而回头修改 `interest_button_primary`、`freshness_days` 或 `anchor_type`。如确需修正标注错误，必须新建版本文件并说明原因，不得覆盖已锁定文件。
- 分析层（L3-C 关联检验）产出的结论只能落在 Confirmed Association / Candidate Association / No Evidence / 无法判断 四类，不得直接写成生产规则或 Prompt 指令。是否升级为规则，按 Baseline Review Final 的先例，需要更大样本和独立复核。

## 待确认事项（本协议冻结前必须回答）

1. `interest_button_primary` 选"无"的比例如果偏高（比如超过30%），是否说明按钮定义本身需要在下一版调整？——本协议不预设答案，留给标注完成后的分布检查。
2. 标注者是本人还是由我（Claude）执行盲标？如果由我执行，需要说明：我在标注时不会主动查询该文章当前的展现/阅读数据，但无法保证对已发布内容完全零记忆污染（比如这次对话里已经提到过"厌学送外卖 671展现"）——这一点需要你决定是否接受，或者指定人工标注更彻底的样本子集做交叉校验。

本协议在你确认以上两点、且字段定义没有异议后，改 Status 为 FROZEN，再开始标注 `toutiao_metrics_2026-08-19.csv` 全部样本。
