# Feature Extraction Schema V3｜Title Resolution (Packaging Gap)

Status: FROZEN (before labeling begins)

Purpose:
Test a single hypothesis against the same 46 baseline articles: does a title that already answers the reader's core information need (title_resolves_outcome=TRUE) correlate with lower CTR than a title that withholds a substantive piece of information (FALSE)? This targets the Impression→Read conversion layer specifically, not impressions or revenue.

Scope:
Applies only to the 46 articles' **titles** in `data/baseline_review/blind_feature_input_2026-08-08.csv`. Body text is NOT used for this label — title only, per the field's own definition.

## Blinding Rule

The annotator reads only: toutiao_group_id, title. Not body, not impressions/reads/CTR/revenue/rankings. Labels written once and locked (`label_status = LOCKED_BLIND_V3`) before joining with performance data.

## Field

### title_resolves_outcome

Type: boolean (TRUE / FALSE)

Definition:
The judgment question is NOT "does the title contain a result?" It is: **"Reading only the title, is the reader's core information need already satisfied?"**

TRUE if the title already delivers the event's main result, causal closure, or core answer — an ordinary reader knows "what happened + how it turned out" from the title alone, and the body would mainly add supporting detail, not resolve anything new.

FALSE if the title still withholds one substantive piece of information that the body is needed to resolve, including but not limited to:
- Reason unanswered ("到底怎么算", "为什么...")
- Meaning/implication unanswered ("普通人该看懂什么信号")
- Outcome not yet happened / anticipatory framing ("将启动", "将至", "拟限制", "首秀")
- Action gap ("该查了")
- Explanation gap (a claim stated without its mechanism)

## Output

Write to: `data/baseline_review/feature_labels_blind_v3_title_resolution_2026-08-08.csv`
Columns: schema_version, label_status, toutiao_group_id, title, title_resolves_outcome, evidence_note

## Analysis Plan (locked before joining)

Core Outcome = **CTR = reads/impressions only**. Not impressions, not revenue — those are reported afterward only as a secondary/side-effect check, explicitly separated from the core test.

Report mean AND median CTR for each group, group n, and explicitly check whether the direction survives removal of the single outlier article "赣锋锂业等成立能源科技公司" (which independently surfaced as a revenue-driving outlier in L3-A V1 and as the top-CTR outlier in the exploratory extremes read). If the TRUE/FALSE CTR gap disappears or reverses after excluding that one article, the finding must be reported as outlier-driven, not as a stable group difference.

No causal language. This may only be described as reaching "Candidate Production Rule" status if: (a) TRUE group CTR is lower than FALSE group on both mean and median, (b) the direction holds after excluding the 赣锋锂业 outlier, (c) n in both groups is not Small-N by the same threshold used in prior reports (rough guide: <10 flagged). Otherwise it stays at Candidate Association or weaker.
