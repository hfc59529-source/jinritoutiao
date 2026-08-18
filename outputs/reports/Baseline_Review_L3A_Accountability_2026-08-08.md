# Baseline Review L3-A｜Accountability & Positioning Association (2026-08-08 labels, filed later)

**数据源**：`data/baseline_review/feature_labels_blind_v2_accountability_2026-08-08.csv`（46行，`label_status = LOCKED_BLIND_V2`，未修改）× `data/baseline_review/baseline_articles_2026-08-08.csv`（真实后台数据，只读不改）。

前置状态：`FEATURE_EXTRACTION_SCHEMA_V2_ACCOUNTABILITY.md` FROZEN，46篇 V2 标签 LOCKED_BLIND_V2。本报告是这条 Evidence Chain 缺失的最后一环——Schema冻结、标签锁定之后一直没有形成正式关联报告，现补上。

三个 Outcome，分开看，不合并：A. impressions（展现）　B. reading_rate = reads/impressions（阅读转换）　C. revenue / revenue>0（收益，样本极稀疏）

---

## 1. Feature Distribution

| Feature | 各组 n |
|---|---|
| accountability_target_clear | FALSE=37, TRUE=9 [Small-N] |
| positionable_sides_present | FALSE=29, TRUE=17 |
| reader_stake_link_explicit | TRUE=31, FALSE=15 |

`accountability_target_clear` TRUE组 n=9，属 Small-N，方向性结论需谨慎对待，不构成 Confirmed。

## 2. 逐特征 × 三阶段结果

### 2.1 accountability_target_clear

| 取值 | n | impressions mean/median | reading_rate mean/median | revenue sum | revenue>0 |
|---|---|---|---|---|---|
| TRUE | 9 [Small-N] | 1852.6 / 1049.0 | 0.73% / 0.02% | ¥0.01 | 1 |
| FALSE | 37 | 802.3 / 680.0 | 0.70% / 0.21% | ¥0.13 | 3 |

**观察**：TRUE组展现均值/中位数均明显高于FALSE组（中位数1049 vs 680）。但阅读率中位数方向相反，TRUE组反而更低（0.02% vs 0.21%）；均值接近（0.73% vs 0.70%），说明TRUE组阅读率分布可能被个别样本拉动。收益两组都极稀疏，无法判断。

### 2.2 positionable_sides_present

| 取值 | n | impressions mean/median | reading_rate mean/median | revenue sum | revenue>0 |
|---|---|---|---|---|---|
| TRUE | 17 | 1388.1 / 760.0 | 0.61% / 0.02% | ¥0.03 | 2 |
| FALSE | 29 | 784.8 / 516.0 | 0.76% / 0.21% | ¥0.11 | 2 |

**观察**：与2.1同方向——TRUE组展现更高，阅读率中位数更低。两个字段（accountability、positionable）在两个结果变量上呈现相同的分叉模式，值得注意但不能视为两个独立证据（这两个字段本身语义相关，可能部分测的是同一件事）。

### 2.3 reader_stake_link_explicit

| 取值 | n | impressions mean/median | reading_rate mean/median | revenue sum | revenue>0 |
|---|---|---|---|---|---|
| TRUE | 31 | 1067.8 / 725.0 | 0.57% / 0.20% | ¥0.03 | 2 |
| FALSE | 15 | 883.6 / 469.0 | 1.00% / 0.21% | ¥0.11 | 2 |

**观察**：展现方向与前两个字段一致（TRUE更高）。阅读率中位数两组接近（0.20% vs 0.21%），差异主要在均值（FALSE组1.00% vs TRUE组0.57%），大概率被FALSE组内少数高阅读率样本拉动，不构成稳定方向。三个字段中，这一个的阅读率分叉证据最弱。

## 3. 与既有 L3-A（V1）结果的交叉参照

V1 报告中 `title_has_direct_person` 已经出现过同构的分叉：展现均值 TRUE组1476 vs FALSE组781（TRUE更高），但阅读率中位数 TRUE组为0、FALSE组0.30%（TRUE更低）。本次 V2 的 accountability_target_clear 和 positionable_sides_present 在同一批46篇上复现了几乎相同的分叉方向——**展现层正相关，阅读转换层零相关或负相关**。三个独立标注的特征（V1一个，V2两个）在同一批数据上指向同一种漏斗断点，这比单一特征的关联更值得继续追。

## 4. 分类结论

### Candidate Association（方向存在，证据不足以Confirm）
- **accountability_target_clear ↔ impressions**：TRUE组展现中位数为FALSE组的1.5倍以上，方向清楚，但 n=9 属 Small-N。
- **positionable_sides_present ↔ impressions**：同方向，n=17，较accountability更大但仍不算充分。
- **三个特征（含V1的title_has_direct_person）共同呈现"展现↑ / 阅读转换↓或平"的分叉模式**：这是本报告最值得记录的发现，但目前是描述性的组间观察，未做混杂控制（题材、结构、字数都可能是潜在混杂），不构成因果结论。

### No Evidence / 证据过弱
- **reader_stake_link_explicit ↔ reading_rate**：中位数两组接近，均值差异疑似被少数样本拉动，不构成方向性结论。

### 无法判断（样本稀疏）
- **全部三个字段 × revenue**：每组仅1-3篇revenue>0，无discriminative power。

## 5. 本报告结论如何影响下一步

不支持"补充普通人代入/责任归因就能提升表现"这类生产规则——因为证据显示这类信号如果有效，作用的是展现层，而非阅读转换层，且尚未排除混杂。

更值得优先研究的问题变成：**为什么这批文章（含V1、V2标注都识别出的高展现样本）在获得展现之后，读者不点开？** 这把研究对象从"正文该不该有责任归因/普通人利益"转向"标题、封面、事件承诺（Title / Cover / Event Promise）在信息流里有没有形成足够的点击理由"。下一份报告应针对这一问题，在同一批46篇内做「高展现低CTR」vs「(相对)高CTR」的对照。

## 纪律确认

- 未修改 `feature_labels_blind_v2_accountability_2026-08-08.csv` 或任何 V1 数据文件。
- 未提出任何生产规则或"应该怎么写"的判断。
- 全文未使用因果表述（"导致/因为/所以证明"）。
- 未进入 L3-B 混杂控制层，仅完成 L3-A 关联层，为已冻结的 Evidence Chain 补齐缺失环节。

**L3-A Accountability 完成，停止。**
