---
status: BLIND_SET_FROZEN
source_runs:
  - outputs/experiments/run_2026-08-08 (Claude executor)
  - outputs/experiments/run_2026-08-08_chatgpt (ChatGPT executor)
mapping_file: outputs/experiments/_sealed/blind_set_mapping_2026-08-09_SEALED.json
frozen_at: 2026-08-09
---

# 盲标集说明

20篇（Claude 10篇 + ChatGPT 10篇，各5样本 × Control/Treatment）已匿名化、去标签、随机打乱，命名为 A01–A20。

## 脱敏方式

- 每篇只保留"标题候选 + 正文"，去掉 frontmatter（sample/condition/executor/status/source_radar）、去掉"生产方式：Radar Source"这类模板痕迹行。
- 文件名替换为随机 ID（A01–A20），与真实样本/条件/执行器的映射关系单独存放在 `outputs/experiments/_sealed/blind_set_mapping_2026-08-09_SEALED.json`，权限设为仅所有者可读（600），不在本目录内，不随本目录一起浏览。
- 已对本目录做过全文 grep 检查，未检出 "Claude / ChatGPT / control / treatment / GPT-5 / executor / radar_pool / S1_–S5_" 等任何来源或条件标签的残留。

## 已知污染风险（如实披露，不隐瞒）

- 打乱与脱敏脚本由本次执行者（Claude）编写和运行，因此在生成阶段，Claude 对 20 篇的真实来源是可见的（脚本运行时打印过映射关系）。这构成 Sentence-level Annotation 阶段的潜在污染源：如果标注也由同一个 Claude 会话执行，标注结果不能被认定为真正意义上的双盲。
- 如果 Annotation 要求严格的标注者盲态（不知道来源），建议：由用户本人、另一个不知情的评审者，或一个未参与本次打乱脚本执行的独立会话来做逐句标注；本会话此后不应再读取 `_sealed/` 目录内容，直到标注完成、指标计算完毕。

## 下一步

不在本轮开始 Annotation。等待明确指令后，再进入 `BLIND_SET_FROZEN → ANNOTATED`。
