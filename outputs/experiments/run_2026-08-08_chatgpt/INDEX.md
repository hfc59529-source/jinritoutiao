# ChatGPT Executor Run — 2026-08-08

status: OUTPUTS_FROZEN
executor: ChatGPT / GPT-5.6 Sol
design_source: outputs/experiments/experiment_design_content_expression_decoupling.md
samples: 5
conditions_per_sample: 2
total_outputs: 10

## Contamination control

- 未读取另一执行器已经冻结的10篇正文。
- 仅依据冻结的 Experiment Design、Adapter 模板与5个 Radar 原始输入生成。
- 每个样本各生成一次 Control、一次 Treatment。
- 生成后未根据质量重跑或修改。
- 本目录内容现冻结，供后续 Blind Annotation 使用。

## Files

| Sample | Topic | Control | Treatment |
|---|---|---|---|
| 01 | 财经数据 | 01_finance_control.md | 01_finance_treatment.md |
| 02 | 隐私/维权 | 02_privacy_control.md | 02_privacy_treatment.md |
| 03 | 家庭伦理/财产 | 03_inheritance_control.md | 03_inheritance_treatment.md |
| 04 | 诈骗 | 04_scam_control.md | 04_scam_treatment.md |
| 05 | 政策法规/科技 | 05_driving_control.md | 05_driving_treatment.md |

## Next state

OUTPUTS_FROZEN → BLIND_ANNOTATION
