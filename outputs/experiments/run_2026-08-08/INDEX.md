---
run: Controlled Experiment — Fact Boundary vs Content/Expression Split
experiment_design: outputs/experiments/experiment_design_content_expression_decoupling.md
hypothesis: outputs/experiments/hypothesis_fact_boundary_expression_collapse.md
status: OUTPUTS_FROZEN
frozen_at: 2026-08-08
---

# 产出清单（10篇，5样本 × 2条件）

| 样本 | Control | Treatment |
|---|---|---|
| S1 科技省份增长消费滞后 | S1_科技省份增长消费滞后_control.md | S1_科技省份增长消费滞后_treatment.md |
| S2 女子修手机私密照 | S2_女子修手机私密照_control.md | S2_女子修手机私密照_treatment.md |
| S3 游戏账号继承 | S3_游戏账号继承_control.md | S3_游戏账号继承_treatment.md |
| S4 旅游搭子骗局 | S4_旅游搭子骗局_control.md | S4_旅游搭子骗局_treatment.md |
| S5 智驾脱手处罚 | S5_智驾脱手处罚_control.md | S5_智驾脱手处罚_treatment.md |

# 生成方式

每个样本按 `experiment_design_content_expression_decoupling.md` 中冻结的 Control / Treatment 文本，代入 `templates/transform_radar_source_prompt.md` 第1节（Target Format Contract，两条件一致）+ 第2节（本次实验唯一变量），对应雷达原文的"给GPT的创作任务单"部分执行生成。每个样本先生成 Control，再生成 Treatment，各生成一次，不重跑、不因某篇质量差而重生成。

# 冻结声明

10篇产出已冻结，生成过程中未对照修改 Prompt、未根据中间结果调整任何一版文本。下一步：Sentence-level Annotation（逐句三分类标注），标注前不再修改本次产出。
