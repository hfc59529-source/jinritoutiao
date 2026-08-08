# Confirmed Quality Finding：Coverage PASS ≠ Article Coherence PASS

生效日期：2026-08-09
性质：Review 方法升级(执行顺序变更)，不是新增参数系统，不改 Fact Boundary / Intent Authority / Permission Boundary

## Finding

Coverage Completeness（字段完整性）不能证明文章成立。Quality Review 必须检查 Approved Judgments 之间是否形成可解释的 Reasoning Chain；当字段间不存在自然的因果、对立、递进或问题—回应关系，却仍被按字段顺序逐项输出时，应识别为 Field Stitching，而不是把"字段全部覆盖"判为结构完整。

## 证据链

```text
1888元 Draft（人工判断"不对"）
  ↓ 全文级 Judgment Review（Central Proposition / Reasoning Chain / Semantic Integration）
  ↓ 定位出：多中心命题、Reasoning Gap（"暂无结果"→"没有尽头"）、局部自相矛盾（"维权没有着落"vs"已报警准备起诉"）、Field Stitching（转场词精确对应 Radar 字段分界线）
  ↓ 反查历史真实样本（Independent Verification，非同一篇的循环论证）
  ↓ 搬家报价570元_v1（已被本仓库记录为 Failure Evidence）：同一方法论下，Field Stitching + Reasoning Gap 复现，且强度更高（连转场词都没有）
  ↓ 独子去世87个游戏账号 A稿（对照样本）：同样多字段，但未被误判 FAIL——因为字段之间存在真实的因果/对立关系（游戏公司主张 vs 法院认定），不是并排堆叠
  ↓ 出现正负对照，方法具备判别力，不是逢文必判 FAIL
  ↓ Quality Failure Class 候选成立
```

## Minimal Review Change

Quality Review 的执行顺序从 `Coverage-first` 改为 `Judgment-first → Coverage-second`：

```text
1. Central Proposition：全文到底在说一件什么事？能不能压缩成一句话？
2. Reasoning Chain：每一个主要判断为什么接在上一个判断后面？（事实→判断→下一判断，逐箭头检查"凭什么能过去"）
3. Contradiction Check：有没有前后自相矛盾？（局部矛盾优先于整体审美判断，不需要高级"文感"，应直接标出）
4. Semantic Integration：Radar 的多个字段有没有被整合成同一条推进链，还是"一字段一段"拼接？
5. Reader Experience：读者代入是体验出来的（Stakes Experience），还是作者宣布出来的（Stakes Statement）？
6. 以上成立后，再检查字段覆盖、标题、语言合规等（原 Coverage-first 检查项，降级为第二优先级，不再是唯一判据）
```

### Diagnostic（便宜的诊断手段，非新增参数）

**转场词删除测试**：删除"更重要的是／另一边／这件事戳中的不只是……"等连接词后，如果前后命题本身无法回答"为什么下一句接在这里"，这个连接词很可能只是在遮盖 Semantic Seam（字段拼接留下的接缝），而不是真实的论证过渡。

## 范围声明

本次只变更 Quality Review 的检查顺序和判断标准，不新增参数系统，不修改 Permission Boundary / Approved Intent Authority（已在 [2026-08-09_intent_authority_v1.md](2026-08-09_intent_authority_v1.md) 中生效并封存），不修改 Fact Boundary，不修改 Selection V2。
