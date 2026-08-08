# Intent Authority V1 = EFFECTIVE

生效日期：2026-08-09
变更文件：templates/transform_radar_source_prompt.md（Minimal Patch，仅在 Permission Boundary 区域新增 "Approved Intent Authority" 一节，未改动 Narrative Spine、Fact Authority、Expression Authority 措辞）
未改动：Selection V2 规则/代码、Radar 采集流程、Fact Boundary Review / Quality Review 流程

## 证据链

```text
Production Failure（2026-08-09 司机捡手机1888元 V1 Draft，Fact Boundary Review FAIL）
  ↓
Intent Mapping（Radar → Transform Prompt → Draft 对照，定位核心冲突/普通人代入判断丢失）
  ↓
Failure Observation：Intent Drift after Expression Unlock
  ↓
Candidate Definition：Intent Authority（Fact Authority / Intent Authority / Expression Authority 三分）
  ↓
Boundary Cases（10项，含原句搬运/同义改写/展开/压缩/弱化/强化/替换/新增判断）
  ↓
H2：Approved Intent Authority Constraint 可提升 IPR、降低 IVR，且不引发 ECR 回升
  ↓
Controlled A/B（同一 Radar，Control V1 ×5、Treatment V2 ×5，共10篇独立生成）
  ↓
Independent Blind Annotation（隔离 Agent，不接触 KEY / Prompt / H2 / 历史 Failure Draft）
  ↓
揭盲：ΔIPR +50pp／ΔIVR −75pp／ΔECR 0／ΔCVR −2条，Unauthorized Addition Treatment 0 vs Control 1
  ↓
H2 = SUPPORTED
  ↓
Production Change = APPLIED（本次）
```

## 结论

Control 组（V1，无 Approved Intent Authority）5 篇独立生成，全部在"主切口""核心冲突"两项 Approved Judgment 上发生同方向 Weakening（涉嫌敲诈→模糊情绪化表述；平台监管责任缺失→流程性弱化），证明 V1 权限模型下的 Intent Drift 是可复现的系统性失效，不是单篇偶然。Treatment 组（V1 + Approved Intent Authority）5 篇 IPR 全部 4/4，ECR 未回升，CVR 未恶化，H2 全部四条判据命中。

## 后续

- 旧的 2026-08-09 司机捡手机1888元 V1 Draft（`outputs/articles/draft/2026-08-09_2026-08-09_司机捡手机索1888元还威胁拔卡.draft.article.md`）保留原状，作为 Failure Evidence，不再修订。
- 该选题重新走一次正式生产（新 Transform Prompt → 新 Production Draft），走完整 Fact Boundary Review → Quality Review。
- 本次不研究 Narrative Authority（节点顺序权限），维持 Out of Scope。
