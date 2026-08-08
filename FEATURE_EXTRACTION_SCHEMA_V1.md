# Feature Extraction Schema V1

Status: FROZEN

Purpose:
Define the allowed blind feature labels for the first Baseline Review before joining with performance data.

Scope:
Applies only to the 46 already-published Today Toutiao articles in `data/baseline_review/`.

## Blinding Rule

The annotator may read only:

- Today Toutiao backend article ID
- title
- article body

The annotator must not read, use, or infer from:

- impressions
- reads
- likes
- comments
- shares
- favorites
- revenue
- L1/L2/L3 reports
- rankings or performance summaries

Labels must be written once and locked before joining with performance data.

## Fields

### topic_category

Type: single choice

Allowed values:

1. 宏观经济/行业数据
2. 企业/商业动态
3. 社会民生/案件
4. 消费/维权
5. 职场/收入
6. 科技/国际

Decision rule:
Choose the primary subject that drives the article's reader relevance. Do not create new categories.

### structural_form

Type: single choice

Allowed values:

1. 事件通报/新闻转述
2. 解读/分析
3. 案例叙事

Decision rule:
Choose one Primary Form only. If an article contains both story and explanation, label according to the dominant structure:

- Use `事件通报/新闻转述` when the article mainly reports what happened.
- Use `解读/分析` when the article mainly explains meaning, causes, risks, or implications.
- Use `案例叙事` when the article mainly follows a concrete person, company, dispute, or case as a narrative.

### title_has_number

Type: boolean

Allowed values: TRUE, FALSE

Decision rule:
TRUE if the title contains Arabic numerals or Chinese numerals used as concrete quantities, dates, percentages, rankings, money, ages, counts, or durations.

### title_is_question

Type: boolean

Allowed values: TRUE, FALSE

Decision rule:
TRUE if the title contains `?`, `？`, or is phrased as a direct question.

### title_has_direct_person

Type: boolean

Allowed values: TRUE, FALSE

Decision rule:
TRUE if the title directly addresses or names reader-side people using words such as `你`, `普通人`, `打工人`, `消费者`, `车主`, `用户`, `家长`, `年轻人`, or equivalent direct audience markers.

### stakes_has_specific_amount_or_quantity

Type: boolean

Allowed values: TRUE, FALSE

Decision rule:
TRUE if the title or body contains concrete money, quantity, percentage, duration, scale, count, or measurable consequence that materially raises the stakes.

### stakes_has_action_advice

Type: boolean

Allowed values: TRUE, FALSE

Decision rule:
TRUE if the title or body contains explicit reader action guidance, warnings, checks, decisions, or "what to do" language.

## Output Table

Write blind labels to:

`data/baseline_review/feature_labels_blind_2026-08-08.csv`

Required columns:

- schema_version
- label_status
- toutiao_group_id
- title
- topic_category
- structural_form
- title_has_number
- title_is_question
- title_has_direct_person
- stakes_has_specific_amount_or_quantity
- stakes_has_action_advice
- evidence_note

`evidence_note` may cite short non-performance evidence from the title/body only.

## Lock Rule

After all 46 rows are labeled, do not revise `feature_labels_blind_2026-08-08.csv` based on performance data. Any later change must create a new versioned file and explain why the blind label was invalid under this schema.
