# Observation：Fidelity ≠ Redundant Coverage（观察，非规则）

生效日期：2026-08-19
性质：单次 Production Trial 观察记录，不是新增 Gate 或规则。是否升级为规则待多篇样本验证。

## 背景

首次真实 Production Trial（选题：手机壳 医疗垃圾，`data/radar_selection/2026-08-19_手机壳-医疗垃圾_0384b7a8.selection.md`）验证了 [`SYSTEM_RULES.md`](../../SYSTEM_RULES.md) 里 Shared 七项 Fidelity Check（Presence Check → Fidelity Check 升级）是否真的在 Runtime 生效。

结果：Fidelity Check 真实抓到一次翻译损失——"普通人代入"节点的雷达原句"你每天握着的手机壳，可能是医院废弃针管做的"，初稿被泛化写成"医疗垃圾"，判定 Weakened，退回修复。这证明 Presence → Fidelity 的升级是有效的，不是文档层面的空规则。

## 新发现的问题：Fidelity 修复后出现 Semantic Redundancy

Fidelity Check 修复后，成稿逐项对照雷达七项均为 Preserved，但人工验收判定：**翻译层 PASS，成稿层 REVISION**。

原因：核心利益链（便宜手机壳 → 低价原料从哪里来 → 医疗废料降低成本 → 商家拿走成本差 → 消费者承担无法识别的健康风险）本身已经清楚，但成稿把雷达原文里同一条语义（"消费者健康成本代价"）在不同段落用不同措辞重复兑现了三到四次——不是错译，也不是丢失，是同一信息被反复展开。

## 结论（观察，暂不升级为规则）

Fidelity 的判断标准需要区分两件事：

- **Fidelity（保真）**：核心语义有没有损失——这是当前 Shared 七项 Fidelity Check 已经在做的，本次 Trial 证明有效。
- **Redundancy（冗余）**：核心语义有没有被重复展开——当前 Fidelity Check 不检查这一层，因为"每个节点都逐字对照 Preserved"本身不排斥同一语义被多次表达。

暂不新增 Semantic Redundancy Gate 或规则，避免重犯"没验证业务规律就工程化"的错误（参考 [[project_zhihu_performance_funnel]] 的教训）。先记录为观察，连续跑几篇 Production Trial，如果"Fidelity 保住但成稿仍冗余"稳定复现，再考虑是否把 Semantic Redundancy Check 补进 Quality Review。

## 本次样本处理方式

Quality Review 判定 REVISION（不是 Fact Boundary Review 的"只改标出句子"限制——Quality Review 的 REVISION 允许整体压缩表达，只要不改变 Narrative Spine 和已保真的核心语义）。人工重写压缩版，同一语义只保留一次最强表达，Narrative Spine（事实→冲突→为什么→谁得利/谁承担→普通人处境→回收）未变。最终稿见 `outputs/articles/reviewed/2026-08-19_手机壳-医疗垃圾_0384b7a8.review.md`。
