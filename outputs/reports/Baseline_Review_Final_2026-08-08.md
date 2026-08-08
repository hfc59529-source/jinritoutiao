# Baseline Review Final｜46篇基线复盘最终结论 (2026-08-08)

依据：`Baseline_Review_L1_2026-08-08.md`、`Baseline_Review_L2_2026-08-08.md`、`Baseline_Review_L3A_Feature_Association_2026-08-08.md`、`Baseline_Review_L3B_Confounder_Test_2026-08-08.md`（均已 FROZEN）。

本文件不产生任何新分析、新变量、新假设，只把已冻结的结论归类为 ACTION / TEST / HOLD 三类。这是第一次46篇 Baseline Review 的收尾文件，完成后本轮复盘结束，回到生产。

---

## ACTION｜已有足够证据，下一轮必须据此行动

### 1. 46篇整体表现极低，确立为下一轮实验基线
- 展现46,357 / 阅读513（中位数1）/ 收益¥0.14，19篇零阅读（41.3%），42篇零收益（91.3%），Top4篇贡献100%收益。
- 这是 **Confirmed Result**（L1）。下一轮生产完成后，必须用同一套字段和同样的复盘流程与本次基线对比，才能判断是否发生实质变化。不与基线对比的"感觉变好了"不构成证据。

### 2. 继续采集 read_duration / read_complete_rate，作为阅读环节的诊断指标
- 高阅读率组的停留时长（43.3秒 vs 14.5秒）和完读率（28.8% vs 8.6%）明显高于低阅读率组（L2 Confirmed Association，L3层未推翻）。
- 这是阅读发生后的行为伴随指标，**不能**作为写作前置依据（Outcome Leakage），但应继续采集，用于诊断"有没有人真的在读"，区别于单纯看 impressions/reads 数字。

---

## TEST｜证据不足，值得设计下一轮实验验证，禁止直接改规则

### 3. 疑问句标题（title_is_question）
- Candidate Association：疑问句标题组在展现、阅读率的均值和中位数上方向一致地更高，但 n=11，且收益贡献主要由单篇（赣锋锂业）拉动。
- 下一轮可以继续正常生产、正常观察，但不得写成"标题要用疑问句"这类规则。样本扩大后需重新走一次同样的关联检验。

### 4. Topic Category 对 word_count–performance 关系的混杂（H-L3-001a: Partially Supported）
- 控制题材后，6个题材中3个方向保持一致、2个完全反转、1个部分反转——说明"字数"这个信号本身可能和题材纠缠在一起，值得在样本扩大后专门设计跨题材的对照观察。
- 这不是一条可执行的写作规则，而是"下一轮复盘该往哪个方向细挖"的候选方向。

---

## HOLD｜当前没有证据，禁止进入任何生产规则

- **周三发布效应**：归一化后周三（n=17）展现和阅读率均值处于7天中间水平，No Evidence。
- **标题含数字（title_has_number）**：展现、阅读率的均值与中位数方向相反，No Evidence。
- **标题含直接人称（title_has_direct_person）**：展现和阅读转换方向相反，No Evidence。
- **字数越长表现越好**：L3-B 已证明当前46篇证据不支持"历史长文表现好 → 下一批写长一点"这条规则。控制题材后方向明显分化，控制结构后证据也弱，联合控制因样本稀疏 INCONCLUSIVE。**这是本轮复盘最重要的一条 HOLD**——防止把一个描述性的组间差异直接升级成生产指令。
- **Structural Form 对 word_count–performance 关系的混杂（H-L3-001b: Weak/Inconclusive）**：证据强度不足以确认，暂不作为研究方向或生产依据。
- **stakes_has_action_advice / stakes_has_specific_amount_or_quantity**：当前46篇内近乎零方差，缺乏区分能力，无法判断是否有效，也不构成"应该/不应该用"的依据。

---

## 本轮复盘的核心产出

不是发现了一个"爆文公式"，而是建立了第一批 **Evidence Boundary（证据边界）**：哪些观察到的差异现在有资格改动生产方式（ACTION），哪些需要更多数据才能判断（TEST），哪些看起来像规律但目前没有资格进入任何 Prompt 或规则（HOLD）。

**Baseline Review（46篇）到此结束。**

| 层级 | 状态 |
|---|---|
| L1 Result | FROZEN |
| L2 Difference | FROZEN |
| Blind Feature Extraction | FROZEN / LOCKED |
| L3-A Feature Association | FROZEN |
| L3-B Confounder Test | FROZEN |
| Final（本文件） | FROZEN |
