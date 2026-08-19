# L3-C Validation Protocol V1｜Reader Model 五按钮 × 新鲜度 验证协议

Status: FROZEN（2026-08-19 修订版，经审计通过后冻结）

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

### first_publication_freshness_days

Type: integer（最小为0）

计算公式：

```
first_publication_freshness_days = 文章发布日期 − 首次公开传播锚点日期
```

**首次公开传播锚点日期，判定的是"信息进入公共传播场的时间"，不是"事情客观发生的时间"**。事件发生日期本身不作为锚点，只能作为辅助事实记录在 `evidence_note` 里——原因：一件事8月10日发生、8月16日才首次被报道、8月19日发布，真正影响头条内容竞争的是"这条信息对公众来说有多新"，即3天，而不是"事情本身有多久远"的9天。用事件发生日期当锚点，测出来的会是"事件年龄"和"新闻新鲜度"的混合变量，不是新鲜度本身。

判定规则，按优先级取第一个满足的：

1. `first_report_confirmed`：雷达原始素材（`radar_pool` / `radar_sources` 对应文件）或正文中明确写出首次公开报道/首次传播日期的，用该日期。
2. `first_report_inferred`：素材未写明确日期，但正文/标题隐含可判断的首次传播时间窗口（如"昨天""本周""8月X日"）的，用该窗口内可推断的最早日期。
3. `radar_capture_fallback`：以上都无法判断时，用该选题被抓取入池的日期（即 `radar_pool` 文件名中的日期）作为锚点，并在 `evidence_note` 标注 `fallback_used=true`。

每一行在 `evidence_note` 中注明 `anchor_type` 取值（`first_report_confirmed` / `first_report_inferred` / `radar_capture_fallback`），使锚点可追溯、可复核。

### active_wave_freshness_days

Type: integer（最小为0），可以等于 `first_publication_freshness_days`（即事件只有一次传播、没有二次传播波次的情况）

计算公式：

```
active_wave_freshness_days = 文章发布日期 − 最近一次可确认公开传播波次日期（latest_prepublication_wave_date）
```

存在意义：昨天"厌学送外卖"这类案例说明，一条8天前的旧闻可能在发布前2天重新形成传播潮——此时头条面对的可能是一条"2天新鲜"的内容，而不是"8天旧闻"。这是与首次传播锚点相互独立、需要同时保留的第二个变量，不是用来替代 `first_publication_freshness_days`，两个变量都要落表，用于分别检验头条更吃"事件首次新鲜度"还是"当前传播波次新鲜度"。

`latest_prepublication_wave_date` 检索规则（防 hindsight bias 的核心机制，全部59篇必须严格执行同一流程，不得挑选执行）：

1. 检索必须在**完全不看该文章任何表现数据**的前提下进行——检索顺序、检索方式与是否已知展现/阅读无关。
2. 检索只能寻找**严格早于该文章发布日期**的公开传播记录（新闻报道、社交媒体讨论量可见的公开二次传播迹象），使用可核验的公开来源，来源需记录在 `evidence_note`（如媒体名+日期，或"未找到独立于首次报道的二次传播波次，等同 first_publication"）。
3. 59篇必须逐篇执行完全相同的检索步骤，不得因为对某篇文章"感觉"表现好/差而单独加检索或跳过检索。
4. 找不到独立于首次报道的二次传播波次时，`active_wave_freshness_days = first_publication_freshness_days`，`evidence_note` 注明 `no_secondary_wave_found`。
5. 全部59篇检索完成、日期写入并锁定（`label_status` 改为 `LOCKED_BLIND`）之后，才允许与 `toutiao_metrics_2026-08-19.csv` join。join 之后不得因为看到表现数据而回头补充或修改任何一行的 `latest_prepublication_wave_date`。

## Output Table

写入：`data/baseline_review/l3c_labels_blind_2026-08-19.csv`

必需列：

- schema_version（固定值 `L3C_V1`）
- label_status（标注中用 `DRAFT`，全部完成后统一改为 `LOCKED_BLIND`）
- toutiao_group_id 或 title（作为与 `toutiao_metrics_2026-08-19.csv` join 的键，标题需与 metrics 文件完全一致）
- interest_button_primary
- first_publication_freshness_days
- anchor_type（first_report_confirmed / first_report_inferred / radar_capture_fallback）
- active_wave_freshness_days
- wave_evidence_note（`latest_prepublication_wave_date` 的来源，或 `no_secondary_wave_found`）
- evidence_note

## Outcome 分离（Join 之后，进入分析层时遵守）

三个结果变量必须分开呈现，不得合并成单一"表现好坏"判断：

- **A. 展现（impressions）**：反映平台愿不愿意继续扩大推荐池，是分发决策的信号。
- **B. CTR / 阅读转换率（reads / impressions）**：反映在已获得的展现里，标题/选题能不能让人点，与展现是两件独立的事——高展现不代表高CTR，见 08-19 数据中已出现"671展现16阅读"这类展现高但转换低的样本，不能笼统称为"表现好"。
- **C1. Revenue（总收益）**：受阅读规模直接影响的总量指标，规模效应会掩盖"变现效率"。
- **C2. RPM（revenue per 1000 reads，每千阅读变现价值）**：剥离规模效应后的变现效率指标，与 C1 不可互相替代——一篇高阅读低RPM和一篇低阅读高RPM在C1上可能相近，但在C2上完全相反，必须分开报告，不得合并成单一"收益表现"。

`interest_button_primary`、`first_publication_freshness_days`、`active_wave_freshness_days` 分别与 A（展现）、B（CTR）、C1（Revenue）、C2（RPM）四个结果独立做关联观察，不合并为一个复合分数。

## Small-N 判定标准（沿用 L3-A 口径）

- 任一按钮/锚点类型对应样本 n < 5：标注 `[Small-N]`，不得单独作为方向性结论，只记录数值。
- n = 1：单样本，不构成组间比较，只记录，不纳入方向判断。
- 若 `interest_button_primary` 六个取值中出现某值 n=0 或占比 >90%（零方差或近零方差），比照 L3-A 对 `stakes_has_action_advice` 的处理方式，标记为"无法判断"，不强行制造比较。

## 纪律（沿用 Baseline Review 全链条纪律）

- 全程不使用"因为/导致/所以"等因果表述，只报告关联方向和样本量。
- 标注完成、`label_status` 改为 `LOCKED_BLIND` 之后，不得因为看到 join 后的表现数据而回头修改 `interest_button_primary`、`freshness_days` 或 `anchor_type`。如确需修正标注错误，必须新建版本文件并说明原因，不得覆盖已锁定文件。
- 分析层（L3-C 关联检验）产出的结论只能落在 Confirmed Association / Candidate Association / No Evidence / 无法判断 四类，不得直接写成生产规则或 Prompt 指令。是否升级为规则，按 Baseline Review Final 的先例，需要更大样本和独立复核。

## 已确认事项

1. **`interest_button_primary` 选"无"的比例即使超过30%，本轮也不据此调整按钮定义**。只在最终报告中如实写"Reader Model 对当前样本覆盖率不足"，是否修改按钮定义留给下一版单独评估，L3-C 本身不因分布结果反向修改标注规则。
2. **标注方式**：由 Claude 完成59篇预注册规则标注（`label_status=DRAFT`），不称为严格 Blind——因为本次对话上下文中已经出现过"厌学送外卖 671展现"等具体数字，存在记忆污染，协议如实记录这一局限，不假装做到了纯盲标。随后从59篇中**随机抽取约15篇**（抽样用与文章内容/表现无关的确定性规则，如按 `toutiao_group_id` 或行号做随机种子抽样，不得挑选671展现那篇或其他高展现/低展现文章）交由人工独立复标，计算两组标注在 `interest_button_primary`、`anchor_type`、`active_wave_freshness_days` 是否找到二次传播波次 三项上的一致率。一致率高则以AI标注为准结案；一致率明显偏低则升级为59篇全量人工复标或双标仲裁。

## Status: FROZEN

三处效度修正（新鲜度锚点改为公开传播时间而非事件发生时间、增加二次传播波次变量、Revenue/RPM拆分）已按审计意见完成，字段范围不再扩展。协议自本次修订起冻结，可以开始对 `toutiao_metrics_2026-08-19.csv` 全部样本执行标注。
