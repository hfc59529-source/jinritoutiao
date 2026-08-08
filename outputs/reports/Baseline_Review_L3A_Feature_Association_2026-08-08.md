# Baseline Review L3-A｜Feature Association（特征关联层）(2026-08-08)

**唯一数据源**：`data/baseline_review/l3_analysis_dataset_2026-08-08.csv`（46行，`label_status = LOCKED_BLIND`，未修改）

前置状态：L1 FROZEN / L2 FROZEN / FEATURE_EXTRACTION_SCHEMA_V1 FROZEN / feature_labels_blind LOCKED_BLIND / Join 已完成。

本层只检验**预注册的盲标特征**与三个结果变量之间是否存在可观察关联，不做因果解释、不做混杂控制（留给 L3-B）。`read_duration`、`read_complete_rate`、`reads_per_1000_impressions`、`revenue_per_1000_reads` 仅作为辅助描述出现，不作为独立核心 Outcome（避免与 reading_rate / revenue 重复计算同一现象）。

三个 Outcome：A. impressions（展现）　B. reading_rate = reads/impressions（阅读转换）　C. revenue / revenue>0（收益）

---

## 1. Feature Distribution（特征分布，先看样本量）

| Feature | 各组 n |
|---|---|
| topic_category | 消费/维权=11, 企业/商业动态=10, 宏观经济/行业数据=8, 科技/国际=8, 职场/收入=5, 社会民生/案件=4 |
| structural_form | 解读/分析=27, 案例叙事=10, 事件通报/新闻转述=9 |
| title_has_number | TRUE=27, FALSE=19 |
| title_is_question | FALSE=35, TRUE=11 |
| title_has_direct_person | FALSE=31, TRUE=15 |
| stakes_has_specific_amount_or_quantity | TRUE=45, **FALSE=1 [SMALL-N]** |
| stakes_has_action_advice | TRUE=46, FALSE=0 **[零方差]** |

`stakes_has_action_advice` 46篇全为TRUE，无对照组，无法参与任何比较。`stakes_has_specific_amount_or_quantity` 的FALSE组仅1篇，属Small-N，其对应数值（展现418、阅读率0.96%、收益0）不构成任何组间结论，仅供记录。`topic_category`中"社会民生/案件"(n=4)、"职场/收入"(n=5)样本量也偏小，相关结论需谨慎对待。

---

## 2. 逐特征 × 三阶段结果

### 2.1 topic_category（题材类别）

| 题材 | n | impressions mean/median | reading_rate mean/median | revenue sum | revenue>0 count |
|---|---|---|---|---|---|
| 企业/商业动态 | 10 | 1,285.3 / 858.5 | 1.36% / 0.53% | ¥0.11 | 2 |
| 消费/维权 | 11 | 1,693.3 / 1,003.0 | 0.58% / 0.26% | ¥0.01 | 1 |
| 宏观经济/行业数据 | 8 | 742.1 / 584.5 | 0.27% / 0.07% | ¥0.02 | 1 |
| 科技/国际 | 8 | 584.4 / 683.0 | 0.82% / 0.15% | ¥0.00 | 0 |
| 职场/收入 | 5 | 642.6 / 516.0 | 0.41% / 0.00% | ¥0.00 | 0 |
| 社会民生/案件 [Small-N] | 4 | 263.2 / 314.0 | 0.41% / 0.35% | ¥0.00 | 0 |

**观察**：企业/商业动态、消费/维权在展现均值上明显高于其余题材；企业/商业动态在阅读率均值上也最高（1.36%）。4篇有收益文章分散在3个题材（企业/商业动态×2、消费/维权×1、宏观经济/行业数据×1），未集中于单一题材。科技/国际、职场/收入、社会民生/案件三个题材revenue>0均为0篇。

### 2.2 structural_form（内容结构）

| 结构 | n | impressions mean/median | reading_rate mean/median | revenue sum | revenue>0 count |
|---|---|---|---|---|---|
| 案例叙事 | 10 | 1,565.5 / 643.0 | 0.61% / 0.14% | ¥0.01 | 1 |
| 解读/分析 | 27 | 964.9 / 745.0 | 0.71% / 0.14% | ¥0.13 | 3 |
| 事件通报/新闻转述 | 9 | 516.6 / 453.0 | 0.81% / 0.30% | ¥0.00 | 0 |

**观察**：三种结构在展现、阅读率的中位数彼此接近（643/745/453展现中位数；0.14%/0.14%/0.30%阅读率中位数），差异主要体现在均值（案例叙事均值1,565.5远高于中位数643.0，组内离散度大，受个别高展现样本拉动）。收益4篇中3篇属于"解读/分析"，但该组样本量也最大（n=27，占59%），**不能排除只是基数效应**。

### 2.3 title_has_number（标题含数字）

| 取值 | n | impressions mean/median | reading_rate mean/median | revenue sum | revenue>0 count |
|---|---|---|---|---|---|
| FALSE | 19 | 928.9 / 725.0 | 0.93% / 0.12% | ¥0.11 | 2 |
| TRUE | 27 | 1,063.2 / 641.0 | 0.55% / 0.26% | ¥0.03 | 2 |

**观察**：展现均值 TRUE 更高，但展现中位数 FALSE 更高；阅读率均值 FALSE 更高，但阅读率中位数 TRUE 更高。均值与中位数方向在两个结果变量上都相反，**方向不稳定**。revenue>0篇数两组相同（各2篇）。

### 2.4 title_is_question（标题为疑问句）

| 取值 | n | impressions mean/median | reading_rate mean/median | revenue sum | revenue>0 count |
|---|---|---|---|---|---|
| FALSE | 35 | 994.7 / 700.0 | 0.60% / 0.14% | ¥0.05 | 3 |
| TRUE | 11 | 1,049.5 / 760.0 | 1.03% / 0.32% | ¥0.09 | 1 |

**观察**：TRUE组（疑问句）在展现和阅读率上均值、中位数均高于FALSE组，方向一致。但 revenue sum 上TRUE组（¥0.09，主要由赣锋锂业单篇贡献）高于FALSE组均值贡献，而revenue>0篇数TRUE组反而更少（1 vs 3）——收益篇数与收益金额方向不一致。n=11，样本量偏小。

### 2.5 title_has_direct_person（标题含直接人称）

| 取值 | n | impressions mean/median | reading_rate mean/median | revenue sum | revenue>0 count |
|---|---|---|---|---|---|
| FALSE | 31 | 781.0 / 641.0 | 0.72% / 0.30% | ¥0.04 | 2 |
| TRUE | 15 | 1,476.4 / 718.0 | 0.67% / 0.00% | ¥0.10 | 2 |

**观察**：展现均值 TRUE 组明显更高（1,476 vs 781），但阅读率中位数 TRUE 组为 0（该组过半文章零阅读），FALSE 组中位数 0.30% 更高。**展现和阅读转换方向相反**，revenue>0篇数两组相同。

### 2.6 stakes_has_specific_amount_or_quantity（含具体金额/数量后果）

TRUE=45, FALSE=1（[Small-N]，仅1篇）。TRUE组承载了全部4篇收益文章。因FALSE组仅1个样本，**无法形成组间比较**，本特征标记为"无法判断"。

### 2.7 stakes_has_action_advice（含行动建议）

46篇全部TRUE，**零方差，无对照组，无法判断**。

---

## 3. word_count 与 topic_category / structural_form 的关系

目的：检验 L2 中"高表现组字数更长"是否可能只是题材/结构的 Proxy。

| topic_category | n | word_count mean/median | word_count min–max |
|---|---|---|---|
| 宏观经济/行业数据 | 8 | 1,222.6 / 1,296.5 | 539–1,815 |
| 科技/国际 | 8 | 1,164.1 / 844.5 | 563–2,139 |
| 企业/商业动态 | 10 | 1,103.8 / 1,074.0 | 543–2,003 |
| 消费/维权 | 11 | 1,017.5 / 977.0 | 562–1,766 |
| 职场/收入 | 5 | 762.2 / 744.0 | 327–1,288 |
| 社会民生/案件 | 4 | 704.8 / 716.0 | 524–863 |

| structural_form | n | word_count mean/median | word_count min–max |
|---|---|---|---|
| 解读/分析 | 27 | 1,123.4 / 1,022.0 | 327–2,139 |
| 案例叙事 | 10 | 958.6 / 874.0 | 567–1,766 |
| 事件通报/新闻转述 | 9 | 893.1 / 619.0 | 524–2,036 |

全体46篇 word_count：均值1,042.5，中位数942.0，P25=619.0，P75=1,380.0（参照值）。

**观察**：题材之间字数均值最高与最低相差约518字（宏观经济/行业数据1,222.6 vs 社会民生/案件704.8）；结构类型之间相差约230字（解读/分析1,123.4 vs 事件通报/新闻转述893.1）。两个维度都显示字数存在系统性差异，且与L2中"高展现/高阅读率/有收益组字数更长"的方向部分重合（企业/商业动态、宏观经济/行业数据、解读/分析——这几个在2.1、2.2中表现相对靠前的组，字数也相对靠前）。**这为"word_count可能是topic_category/structural_form的代理变量"提供了初步支持，但本层不做混杂控制回归，仅记录关联存在，正式检验交给L3-B**。

---

## 4. 分类结论

### Confirmed Association（数据中明确存在的关联，非因果）
- **word_count 与 topic_category 存在关联**：不同题材之间字数均值差异达518字，且分布区间不同（如"社会民生/案件"字数普遍偏短、"宏观经济/行业数据"普遍偏长）。
- **word_count 与 structural_form 存在关联**：不同结构类型之间字数均值差异达230字，"解读/分析"类系统性长于"事件通报/新闻转述"类。
- **stakes_has_action_advice 在当前样本内零方差**：46篇全TRUE，这是数据集本身的确认事实（不是关联，是无法比较的确认状态）。

### Candidate Association（方向存在但证据不足）
- **title_is_question 与展现、阅读率**：TRUE组（疑问句）均值和中位数均高于FALSE组，方向一致，但 n=11 偏小，且revenue篇数与revenue金额方向不统一，需更大样本验证。
- **topic_category（企业/商业动态、消费/维权）与展现**：两个题材展现均值明显高于其他题材，但各组n均在4-11之间，样本量不足以确认稳定关联。
- **structural_form（解读/分析）与收益篇数**：4篇收益中3篇属于该结构，但该结构本身样本占比59%，无法排除基数效应。

### No Evidence（当前46篇未显示稳定关联）
- **title_has_number**：展现、阅读率的均值与中位数方向均相反，无稳定方向。
- **title_has_direct_person**：展现方向与阅读转换方向相反（TRUE组展现更高但阅读率中位数为0），不构成单一方向的关联。
- **stakes_has_specific_amount_or_quantity**：FALSE组仅1篇，Small-N，无法判断。

---

## 纪律确认

- 全文未使用"因为/导致/所以"等因果表述。
- 未提出任何生产建议或"应该怎么写"的判断。
- 未修改 `feature_labels_blind_2026-08-08.csv` 或 `l3_analysis_dataset_2026-08-08.csv` 中的任何盲标值，未创建新标签。
- `reads_per_1000_impressions`、`revenue_per_1000_reads`、`read_duration`、`read_complete_rate` 仅作辅助描述引用，未被当作独立结果变量参与分类判断。
- 未进入机制解释，未做混杂控制。
- 所有结论均可回指 `l3_analysis_dataset_2026-08-08.csv` 中的具体46条记录。

**L3-A 完成，停止，等待 GPT 审核，不进入 L3-B。**
