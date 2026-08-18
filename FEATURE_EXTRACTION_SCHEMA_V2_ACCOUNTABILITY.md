# Feature Extraction Schema V2｜Accountability & Positioning Add-on

Status: FROZEN (before labeling begins)

Purpose:
Extend FEATURE_EXTRACTION_SCHEMA_V1 with 3 new blind fields to retroactively test the Reader Model v0.2 hypothesis (Self-positioning + Accountability) against the same 46 already-published baseline articles, without producing new content.

Scope:
Applies only to the 46 articles in `data/baseline_review/blind_feature_input_2026-08-08.csv` (title + body only, no performance columns).

## Blinding Rule (inherited from V1)

Same as V1: annotator reads only toutiao_group_id, title, body. No impressions/reads/likes/comments/shares/revenue/rankings may be read or inferred before labeling. Labels are written once and locked (`label_status = LOCKED_BLIND_V2`) before joining with performance data.

## Fields

### accountability_target_clear

Type: boolean (TRUE / FALSE)

Definition:
TRUE only if the text establishes an identifiable responsibility relationship between a specific named or clearly identifiable subject (a person, company, institution, or role) and a negative outcome in the story — i.e. the text lets the reader answer "谁该为这个结果负责" with a specific subject.

Explicitly NOT sufficient for TRUE:
- Merely naming a company/platform/institution as the subject of a neutral event ("某平台发生……", "TikTok正在测试……") without attaching a negative outcome and responsibility to it.
- A policy or system being described in the abstract ("新规规定……") with no specific actor blamed.
- An outcome with no clear cause attributed to any actor (e.g. accident with disputed cause, "原因尚不明确").

Decision rule: ask "if I finished reading, could I name who should be blamed or held responsible for what went wrong?" If yes and the answer is a specific actor (not "the system" in the abstract, not "society"), TRUE.

### positionable_sides_present

Type: boolean (TRUE / FALSE)

Definition:
TRUE only if ALL three hold:
1. At least two subjects/sides exist with different interests or responsibility positions.
2. An ordinary reader can understand what each side gains or loses.
3. The text provides enough concrete information (not just naming two roles) for a reader to form a leaning/preference toward one side.

Explicitly NOT sufficient for TRUE:
- Two roles merely appear in the same story without their respective gains/losses being made legible (e.g. "大学生" and "平台" both mentioned, but no comparison of what each gets or loses).
- One-sided narration where only one party's experience is described and the other party is an unelaborated abstraction.

### reader_stake_link_explicit

Type: boolean (TRUE / FALSE)

Definition:
TRUE only if the text explicitly and concretely connects the event to what it means for an ordinary reader's own money, job, safety, family, or expectations — not just a generic closing remark. The connection must let a reader answer "this matters to me because ___" with a specific mechanism, not a vague appeal.

Explicitly NOT sufficient for TRUE:
- Generic stock phrases implying universal relevance without a concrete mechanism ("这值得每个人关注", "这提醒我们要小心").
- A takeaway aimed at a narrow professional audience with no bridge to ordinary readers.

TRUE requires a concrete bridge, e.g. "如果你也...(具体情境)，你可能会...(具体后果)".

## Output

Write to: `data/baseline_review/feature_labels_blind_v2_accountability_2026-08-08.csv`

Columns: schema_version, label_status, toutiao_group_id, title, accountability_target_clear, positionable_sides_present, reader_stake_link_explicit, evidence_note

## Analysis Plan (locked before joining)

Do NOT collapse to a single "performance" number. Join against three separate funnel stages from `baseline_articles_2026-08-08.csv`:

1. **Impressions**（展现，分发层）
2. **Reading rate** = reads/impressions（点击转化层）
3. **Revenue / revenue>0**（收益层，样本极稀疏，46篇仅4篇>0，谨慎解读）

Report each of the 3 new fields × each of the 3 funnel stages separately (mean/median, group n). Do not average across funnel stages. Flag any group with n<5 as Small-N. No causal language. No production rule may be written directly from this pass — this stays at Candidate/Confirmed Association level per the existing Evidence Boundary discipline in `Baseline_Review_Final_2026-08-08.md`.
