# SYSTEM_AUDIT_V1

审计日期：2026-08-05
审计对象：Architecture、Collect、Transform、A/B 两种生产模式、Shared 参数、六项拆解、Review、Revision、Publish、Feedback、Actor、State、历史脚本/Prompt/模板/数据。
审计方式：直接读取根目录全部 *_V1.md / SYSTEM_RULES.md / README.md，逐一阅读 scripts/*.py 源码，grep 模板与 prompt 实际引用关系，对比 data/ 与 outputs/ 各子目录实际文件，`diff -rq` 对比 jinritoutiao/ 与根目录。本审计只做判断，不修改、不删除任何文件。

**复核记录（2026-08-05，同日）**：用户对首版审计做了工程复核，认可约 90% 的发现，但指出四处定性需要修正——核心原则是区分 **Conflict（规则真实矛盾）** 与 **Missing Mapping / Placement Gap（只是没写归位说明，不等于矛盾）**，以及区分 **No Evidence（没有证据）** 与 **Not Executed（没有执行）**。下方 B/C 部分的严重程度与措辞已按复核意见更新，原始判断保留在括注中以便追溯。

---

## A. Current System Map（当前系统地图）

### A1. 真实生产链路（由 scripts/ 源码证实，非按文档猜测）

```
data/raw/*.md（soloapi 采集原文，人工/Codex粘贴）
   ↓ scripts/save_radar_content.py
data/radar_pool/*.radar.md  +  data/radar_pool/pool_log.csv（追加一行）
   ↓（人工按 templates/radar_selection_card_template.md 思路，实际由 scripts/select_radar.py 生成）
data/radar_selection/*.selection.md  +  data/radar_selection/selection_log.csv
   ↓ scripts/daily_radar_run.py（核心编排脚本，一次性产出下列全部文件）
   ├─ data/radar_sources/{id}.md                         （雷达原文，frozen）
   ├─ data/radar_analysis/{id}.simple_analysis.md         （六项拆解，仅供 B 线）
   ├─ outputs/daily_runs/{id}.shared_params.md            （读取 templates/shared_params_template.md）
   ├─ outputs/daily_runs/{id}.A_params.md                 （读取 templates/line_a_params_template.md）
   ├─ outputs/daily_runs/{id}.B_params.md                 （读取 templates/line_b_params_template.md）
   ├─ prompts/generated/{id}.A_radar_direct.prompt.md     （读取 templates/line_a_radar_direct_prompt.md）
   ├─ prompts/generated/{id}.B_protocol_generate.prompt.md（读取 templates/line_b_protocol_generate_prompt.md）
   ├─ outputs/daily_runs/{id}.publish_schedule.md         （读取 templates/dual_line_publish_schedule.md）
   ├─ outputs/daily_runs/{id}.metadata.json
   └─ outputs/daily_runs/{id}.index.md
   ↓（人工/Claude 依据 prompt 手写正文，未见脚本参与这一步）
outputs/articles/draft/{date}_{title}_{A|B}_....md   （文件名格式与 scripts/save_article.py 的命名规则不一致，见 B 部分）
   ↓（无脚本，无自动流转证据）
outputs/articles/reviewed/ .gitkeep 空目录（无产物）
outputs/articles/published/ .gitkeep 空目录（无产物）
data/metrics/dual_line_metrics.csv （字段已建，阅读量/点赞/评论/收益列全部为空）
notion/sync_logs/*.md （scripts/build_notion_page.py 产出，独立分支，未接入上面主链）
```

### A2. 未接入主链的脚本 / 孤立文件

- `scripts/collect_radar.py`：写入 `data/radar/`，是与 `save_radar_content.py`（写入 `data/radar_pool/`）平行的另一套"采集归档"逻辑，字段结构不同（`status: collected` vs `status: pooled`）。`data/radar/` 目前只有 1 个示例文件 `sample_radar.collected.md`，与 `daily_radar_run.py` 实际链路（读 `data/radar_sources/`）不是同一条路径。
- `scripts/generate_prompt.py`：读取 `prompts/templates/toutiao_article_prompt.md`，写入 `prompts/generated/*.prompt.md`，命名规则（`{date}_{stem}.prompt.md`）与 `daily_radar_run.py` 生成的 `{id}.A_radar_direct.prompt.md` / `{id}.B_protocol_generate.prompt.md` 是两套并存命名，`prompts/generated/2026-07-29_sample_radar.collected.prompt.md` 即由此脚本产出，与双线体系无关。
- `scripts/build_notion_page.py`：独立读取 `--radar` `--prompt` `--article` 三个手动传入路径，写 `notion/sync_logs/`，未见被其它脚本调用，也未见被 daily_radar_run 触发。
- `scripts/save_article.py`：定义了 `outputs/articles/draft/{date}_{stem}.article.md` 的命名与 frontmatter（`source_file` / `prompt_file` / `status` / `saved_at`），但实际 `outputs/articles/draft/` 下现有 7 个文件（如 `2026-07-29_轻资产普通人创业_A_radar_direct.md`）文件名格式和内容开头（`# 2026-07-29 轻资产普通人创业 A稿` 直接开始，无 frontmatter）均与该脚本产出格式不符，说明这些文件不是由 `save_article.py` 生成的，该脚本在当前实际生产中处于未使用/未验证状态。
- `templates/publish_check_template.md`、`radar_analysis_template.md`、`radar_content_template.md`、`radar_rule_template.md`、`radar_selection_card_template.md`、`radar_selection_rules.md`、`radar_simple_analysis_template.md`、`toutiao_convert_template.md`：grep `scripts/*.py` 全部 0 命中，无任何脚本引用，均为孤立模板（可能仅供人工/Claude 在对话中参照，而非程序化调用）。
- `data/radar_candidates/`、`data/radar_rules/`：空目录，无文件、无脚本写入证据。

### A3. 规范层（*_V1.md）与执行层（SYSTEM_RULES.md + scripts/）几乎完全脱节

grep 全部 `ARCHITECTURE_V1.md / DELIVERABLE_DEFINITION_V1.md / STATE_DEFINITION_V1.md / STAGE_DEFINITION_V1.md / COLLECT_*_V1.md / TRANSFORM_*_V1.md / REVIEW_*_V1.md` 未发现任一处提及："A线/B线"、"Shared 参数"、"六项拆解"、"radar_pool"、"radar_selection"、"soloapi"、"daily_radar_run"。这些文件描述的是一条抽象的六阶段流水线（Collect → Transform → Review → Revision → Publish → Feedback），而真正在跑的、README.md 与 SYSTEM_RULES.md 描述、daily_radar_run.py 落地实现的"雷达双生产线"（A/B 模式、Shared 参数、六项拆解）在新规范文件体系里完全不存在对应章节。两套文件目前是并行的、互不引用的两个事实源。

---

## B. Findings（发现）

### B1. jinritoutiao/ 是根目录几乎全部内容的字节级完整复制，且是独立 git 仓库
- 问题：`jinritoutiao/` 子目录内部有自己的 `.git`（独立提交历史：`5848de4 Initial Toutiao operations system` → `e6c1405 同步外层目录改动：新增今日选题数据与流程标准文档`），且用 `diff -rq jinritoutiao/ . --exclude=jinritoutiao --exclude=.git --exclude=.claude --exclude=.gitignore` 对比，输出为空（0 行差异）——即除 `.claude/`（仅根目录有）和 `.gitignore`（仅 jinritoutiao 有）外，全部文件（含全部 *_V1.md、SYSTEM_RULES.md、README.md、scripts/、templates/、prompts/、data/、outputs/、notion/、database/、assets/）逐字节相同。
- 证据文件：`/Users/huangsheng/Documents/今日头条/jinritoutiao/`（整体）；`jinritoutiao/.git`；`jinritoutiao/.gitignore`
- 影响：根目录仓库里存在一份完整的、可独立提交/独立演化的自身镜像。若未来任一侧继续被编辑而未同步，会立刻产生两个事实源；当前 `git status` 显示 `jinritoutiao/` 在根仓库中未被跟踪（`?? jinritoutiao/`），说明这是历史遗留（很可能是旧仓库快照被整体拷入新仓库根目录、且忘记加入 `.gitignore` 或删除），而不是设计意图。
- 严重程度：BLOCKER

### B2. 规范层（*_V1.md）与实际运行层（SYSTEM_RULES.md + scripts/ + data/）之间缺少映射，尚未真正接管
- 问题：`ARCHITECTURE_V1.md`（Stage: Collect/Transform/Review/Revision/Publish/Feedback）、`STATE_DEFINITION_V1.md`、`DELIVERABLE_DEFINITION_V1.md` 中定义的六阶段模型，与 `SYSTEM_RULES.md`（"雷达双生产线 v1"：A线/B线、Shared 参数、六项拆解）之间没有任何交叉引用或映射说明。**新规范目前是悬空的**：不是因为两边内容互相矛盾，而是因为新规范还没有把旧能力挂进去。
- 证据文件：`ARCHITECTURE_V1.md:1-34`（六 Stage 定义，未提及 A/B、Shared、六项拆解）；`SYSTEM_RULES.md:1-30`（雷达双生产线定义）；`TRANSFORM_STANDARD_V1.md` / `TRANSFORM_MODULE_SUMMARY_V1.md`（grep "A线/B线/Shared" 结果为空）。
- 影响：新规范无法直接回答"A/B 生产模式挂在 Transform 下的哪个子节点"，但这不代表二者矛盾——只代表 Placement 尚未写出来。**必须修：**在 `TRANSFORM_STANDARD_V1.md` / `TRANSFORM_MODULE_SUMMARY_V1.md` 中补一段"A/B 是 Transform 内部的生产模式，Shared 参数是两种模式的公共输入"的归位说明即可闭环，不需要改动任何一边的现有定义。
- 严重程度：**BLOCKER**（复核后从 CONFLICT 上调——悬空的规范层本身会阻塞后续任何"按新规范执行生产"的尝试，属于阻断级问题；但根因是 Missing Mapping/Placement Gap，不是规则互相矛盾，处理方式是"补映射"而非"改规则"）

#### B2a（原判断的子项，复核后单独定性）：`data/radar_pool/pool_log.csv` 的 `status` 字段值（如 `确认S+·92分`）、`data/radar_sources/*.md` 的 `status: frozen`，与 `STATE_DEFINITION_V1.md` 定义的 `Collected / Ready for Transform / Transforming / Generated` 等英文状态词不一致
- 复核结论：**不成立为 Conflict，改判为 Mapping Gap**。理由：`STATE_DEFINITION_V1.md` 里的状态描述的是 **Workflow State**（选题在流程中走到哪一步），而 `status: frozen` / `确认S+·92分` 描述的是 **Artifact Status**（某份文件/记录自身的定稿状态或评分），两者是不同的对象（Object），本来就不应该用同一套取值域。证据不足以证明"冲突"，只能证明"两个对象目前没有被显式区分和关联"。
- 证据文件：`STATE_DEFINITION_V1.md`（Workflow State 定义）；`data/radar_sources/*.md` frontmatter（Artifact Status: `status: frozen`）；`data/radar_pool/pool_log.csv`（Artifact Status: 评分文本）
- 严重程度：GAP（Object 未区分 / Missing Mapping，非 CONFLICT）

### B3. 新规范文件内部标题与文件名版本号不一致（V1 文件名，内容标题却是 V2）
- 问题：`ARCHITECTURE_V1.md` 第 1 行标题是 `# Architecture V2`；`DELIVERABLE_DEFINITION_V1.md` 第 1 行是 `# Deliverable Definition V2`；`STATE_DEFINITION_V1.md` 第 1 行是 `# State Definition V2`；`STAGE_DEFINITION_V1.md` 第 1 行是 `# Stage Definition V2`。而 `COLLECT_STANDARD_V1.md`、`TRANSFORM_STANDARD_V1.md`、`REVIEW_STANDARD_V1.md` 等文件标题又正确标注为 V1。
- 证据文件：`ARCHITECTURE_V1.md:1`、`DELIVERABLE_DEFINITION_V1.md:1`、`STATE_DEFINITION_V1.md:1`、`STAGE_DEFINITION_V1.md:1`
- 影响：无法确认这 4 个文件当前生效版本号；如果 V2 是更新版本但文件名未跟着改名，未来新增 `ARCHITECTURE_V2.md` 时会与现有文件名冲突或产生歧义。
- 严重程度：**HIGH**（复核维持问题成立，仅将级别从 CONFLICT 下调标注为 HIGH——命名与标题不一致本身不阻断生产，但会在下次改版时制造混淆，优先级仍高于普通 REDUNDANCY/GAP）

### B4. selection_log.csv 中同一选题被重复登记两条不同 ID 的记录
- 问题：`data/radar_selection/selection_log.csv` 第 2、3 行都是标题"轻资产普通人创业"，但文案ID 分别是 `2026-07-29_轻资产普通人创业_81553c31` 和 `2026-07-29_轻资产普通人创业_d6425301`，其余字段（评分、优先级、入选理由）完全相同。
- 证据文件：`data/radar_selection/selection_log.csv:2-3`；对应的两份文件 `data/radar_selection/2026-07-29_轻资产普通人创业_81553c31.selection.md` 与 `...d6425301...`（未在本次审计中打开逐字对比，但 ID 后缀由 `hashlib.sha1` 内容哈希生成，两条哈希不同意味着两次保存时源文件内容存在细微差异，或被重复执行了一次 select_radar.py）
- 影响：同一选题产生两套下游 A/B 生产文件与两条 pool/selection 记录，破坏"每篇爆点文案只记录一次"的设计前提，也让"今日入选文案"计数失真。
- 严重程度：MEDIUM（复核维持问题成立，级别标注从 REDUNDANCY 调整为 MEDIUM）

### B5. 存在两套并行的"采集归档"脚本与目录，字段结构不同
- 问题：`scripts/collect_radar.py` 写入 `data/radar/`（frontmatter 字段：`source_file/collected_at/content_hash/status: collected/structure_policy`），`scripts/save_radar_content.py` 写入 `data/radar_pool/`（frontmatter 字段：`id/title/hotspot_type/source_date/source_column/source_url/source_label/status: pooled/content_hash/saved_at/policy`）。两者职责重叠（都是"保存雷达原文"），但字段完全不同，且 `daily_radar_run.py` 实际读取的是 `data/radar_sources/`（第三个、又不同的目录），三者互不复用同一份 frontmatter 结构。
- 证据文件：`scripts/collect_radar.py:14-27`；`scripts/save_radar_content.py:28-46`；`scripts/daily_radar_run.py:222-238`（`source_markdown()` 函数，写入 `data/radar_sources/`）
- 影响：一个"雷达原文"概念对应三个物理目录（`data/radar/`、`data/radar_pool/`、`data/radar_sources/`）和三套字段命名，Duplication 未收敛。
- 严重程度：MEDIUM（复核维持问题成立，级别标注从 REDUNDANCY 调整为 MEDIUM）

### B6. outputs/articles/draft/ 实际产物与 save_article.py 定义的产物格式不一致，说明该脚本未被使用
- 问题：`scripts/save_article.py` 规定输出文件名 `{date}_{source.stem}.article.md`，且内容以 YAML frontmatter（`source_file/prompt_file/status/saved_at`）开头。但实际 `outputs/articles/draft/` 下 7 个文件命名为 `{date}_{title}_{A|B}_....md`（如 `2026-07-29_轻资产普通人创业_A_radar_direct.md`），文件内容直接以 `# 2026-07-29 轻资产普通人创业 A稿` 开头，无 frontmatter。
- 证据文件：`scripts/save_article.py:11-38`；`outputs/articles/draft/2026-07-29_轻资产普通人创业_A_radar_direct.md:1-9`
- 影响：Transform 阶段真实产物的保存方式脱离了脚本定义，人工操作代替了脚本，Executability 上出现"交付物在哪、怎么进来的"回答不一致的风险。
- 严重程度：MEDIUM（复核维持问题成立，级别标注从 GAP 调整为 MEDIUM——脚本与真实产物脱节是工程审计里应优先发现的问题，但不阻断当前生产，因为人工路径仍然能出稿）

### B7. Review / Revision / Publish / Feedback 四个阶段在现有目录里找不到产物证据
- 问题：`outputs/articles/reviewed/` 和 `outputs/articles/published/` 目录下只有 `.gitkeep`，无任何文件；`data/metrics/dual_line_metrics.csv` 已建好表头（原始选题ID/生产方式/标题/发布时间/阅读量/点赞/评论/收益）但所有数据行的发布时间及后续四列全部为空；`outputs/reports/` 只有 `.gitkeep`。
- 证据文件：`outputs/articles/reviewed/.gitkeep`；`outputs/articles/published/.gitkeep`；`data/metrics/dual_line_metrics.csv:1-3`；`outputs/reports/.gitkeep`
- 影响：目录为空**只能证明"没有留下文件证据"**，不能直接证明"这四个阶段从未被执行过"——实际发布、审核动作完全可能发生在系统外（例如直接在头条后台操作、或通过聊天记录口头确认），只是没有被落盘记录下来。原判断"Review 没跑"证据链不够严谨，予以收回。可以确认成立的、更保守的表述是：**当前没有任何文件能证明这四个阶段发生过，也没有任何文件能证明没发生过**——无论哪种情况，"交付物应该落在哪里"这件事本身缺失，需要被补上。这与 `ACTOR_DEFINITION_V1.md` 里详细定义的 Review(GPT)/Revision(Claude)/Publish(User)/Feedback(Codex) 职责、以及 README.md 里这四个模块 `DRAFT` 状态标注（Collect/Transform/Review 是 `FROZEN`）是一致的：定义已完成，但"是否执行"和"执行结果存在哪"都无法从系统内部确认。
- 严重程度：**LOW（证据不足）**（复核后从 GAP 下调——原判断把"No Evidence（没有证据）"误推成"Not Executed（没有执行）"，工程审计中这是两回事，证据不足时应保守定级，而不是直接判定流程不存在）

### B8. Executability 缺口：无法从现有文件确认"现在到哪一步、失败后回到哪里"
- 问题：`outputs/daily_runs/{id}.index.md`（由 `daily_radar_run.py` 的 `daily_index()` 生成）只记录了"已生成/已冻结"等静态完成态描述，没有任何字段记录当前处于 Review/Revision/Publish/Feedback 中的哪一步，也没有失败回退指引；`STAGE_DEFINITION_V1.md` 定义了 Stage 边界但没有配套的"当前 Stage 定位"文件或字段与 `daily_runs` 产物关联。
- 证据文件：`scripts/daily_radar_run.py:196-220`（`daily_index()` 函数内容）；`STAGE_DEFINITION_V1.md:1-67`
- 影响：真实生产时，"现在到哪一步"只能靠人工记忆或翻聊天记录判断，找不到一个文件字段可以直接回答；"失败后回到哪里"在 REVISION 分支之外（REJECT 分支）在 `ARCHITECTURE_V1.md` 里被定义为直接 `End`，但 `outputs/` 与 `data/` 中没有任何 REJECT/终止态的实际记录格式或目录。
- 严重程度：GAP

### B9. templates/ 中过半模板文件未被任何脚本引用（孤立文件）
- 问题：14 个模板文件中，`publish_check_template.md`、`radar_analysis_template.md`、`radar_content_template.md`、`radar_rule_template.md`、`radar_selection_card_template.md`、`radar_selection_rules.md`、`radar_simple_analysis_template.md`、`toutiao_convert_template.md` 共 8 个，`grep -rl` scripts/*.py 均为 0 命中。
- 证据文件：`templates/` 目录列表；`grep -rl "<template名>" scripts/*.py` 命令结果（本次审计已执行，均为 0）
- 影响：不确定这 8 个模板当前是被人工/对话流程手动参照使用，还是历史遗留后已废弃；无法仅凭脚本调用链判断其存活状态。
- 严重程度：GAP（证据不足，建议标记 UNPROVEN，见 C 部分）

---

## C. Legacy Capability Decisions（旧能力判定）

- **A/B 生产模式（雷达直转 / 协议复刻）**
  判定：PROVEN
  理由与证据：`scripts/daily_radar_run.py` 完整实现了两条线的 Prompt 生成（`line_a_prompt()` / `line_b_prompt()`），且 `outputs/articles/draft/` 中已有 7 篇分别标注 `A_radar_direct` / `B_protocol_generate` 的真实成稿文件，`data/metrics/dual_line_metrics.csv` 也按"生产方式"字段区分两条线。其在新规范 `TRANSFORM_STANDARD_V1.md` / `TRANSFORM_MODULE_SUMMARY_V1.md` 中未被提及（见 B2），但复核结论是：这不是 A/B 与 Transform 的定义冲突，而是 **Placement Gap（归位缺口）**——A/B 本来就该是 Transform 内部的子节点，只是新规范文档里还没写出这层归属，能力本身已验证运行，缺的只是一句归位说明。

- **Shared 参数**
  判定：PROVEN
  理由与证据：`templates/shared_params_template.md` 被 `scripts/daily_radar_run.py:109` 的 `shared_params()` 函数实际读取并填充，产出 `outputs/daily_runs/{id}.shared_params.md`，且被 A、B 两条线的 Prompt 生成函数（`line_a_prompt`、`line_b_prompt`）共同引用（`{{SHARED_PARAMS}}` 占位符），符合 README.md 与 SYSTEM_RULES.md 描述的"A/B 两种模式的公共输入"定位。Placement 正确（作为 Transform 内部的公共输入层），但同样未被写入新规范 *_V1.md。

- **六项拆解（开头方式/结构顺序/冲突位置/普通人代入方式/情绪推进/评论入口）**
  判定：PROVEN
  理由与证据：`scripts/daily_radar_run.py:66-96`（`simple_analysis_markdown()`）生成六项拆解文件 `data/radar_analysis/{id}.simple_analysis.md`，且仅在 `line_b_prompt()` 中被读取传入（`{{SIMPLE_ANALYSIS}}`），未在 `line_a_prompt()` 中出现，证实"仅服务 B 模式"这一 Placement 判断准确、已正确归位。

- **筛选卡（radar_selection_card）**
  判定：PROVEN（脚本层）+ UNPROVEN（是否使用 templates/radar_selection_card_template.md 这份模板文件本身）
  理由与证据：`scripts/select_radar.py` 内部直接用 f-string 硬编码筛选卡结构（`build_card()` 函数），并未读取 `templates/radar_selection_card_template.md`（grep 0 命中，见 B9）。实际产出的 `data/radar_selection/*.selection.md` 文件确实存在且被 `selection_log.csv` 记录，能力本身在跑，但对应的模板文件是孤立的，两者是"同名不同源"的重复定义。

- **旧 Prompt（prompts/ 目录下各文件）**
  判定：DUPLICATE（两套并存）
  理由与证据：`prompts/templates/toutiao_article_prompt.md` + `scripts/generate_prompt.py` 是一套（产出 `prompts/generated/{date}_{stem}.prompt.md`，如 `2026-07-29_sample_radar.collected.prompt.md`）；`templates/line_a_radar_direct_prompt.md` + `templates/line_b_protocol_generate_prompt.md` + `scripts/daily_radar_run.py` 是另一套（产出 `prompts/generated/{id}.A_radar_direct.prompt.md` 等）。两套都写入同一个目录 `prompts/generated/`，命名规则不同，职责重叠（都是"从雷达原文生成头条 Prompt"）。当前实际在用的是后者（daily_radar_run 一套，8 个真实生成文件），前者只有 1 个示例产物，判断为已被后者取代但未清理。

- **旧脚本（scripts/ 目录下各文件）**
  逐一判定：
  - `daily_radar_run.py`：PROVEN，主链核心，8 组真实产物。
  - `select_radar.py`：PROVEN，筛选卡生成，`selection_log.csv` 有 6 条真实记录（含 1 条重复，见 B4）。
  - `save_radar_content.py`：PROVEN，雷达池写入，`pool_log.csv` 有真实记录。
  - `render_toutiao_cover.py`：UNPROVEN，本次审计未在 outputs/ 或 assets/ 中找到明确由该脚本生成、带时间戳可追溯的封面产物证据，功能独立（PIL 图像处理），与主链无数据依赖，无法判断是否仍在使用。
  - `collect_radar.py`：OBSOLETE 倾向（UNPROVEN 需人工确认）：写入的 `data/radar/` 目录仅有 1 个示例文件，与主链读取的 `data/radar_sources/` 不是同一目录，功能被 `save_radar_content.py` + `daily_radar_run.py` 组合实质替代。
  - `generate_prompt.py`：OBSOLETE 倾向（UNPROVEN）：见上方"旧 Prompt"判断，功能被 `daily_radar_run.py` 的 A/B Prompt 生成实质替代。
  - `save_article.py`：UNPROVEN，见 B6，定义的产物格式与实际 `outputs/articles/draft/` 现有文件不符，无法证明当前仍被使用。
  - `build_notion_page.py`：UNPROVEN，`notion/sync_logs/` 下有 2 个非 `.gitkeep` 产物（`notion_preview.md`、`2026-07-29_soloapi_sync.md`），证明至少运行过一次，但未见与主链自动衔接的证据（无脚本互相调用），是否仍在日常使用无法判断。

- **历史数据（data/ 各子目录、outputs/ 各子目录）**
  - `data/radar_pool/`、`data/radar_selection/`、`data/radar_sources/`、`data/radar_analysis/`：PROVEN，均有对应真实生产记录且与 `daily_radar_run.py` 主链一致。
  - `data/radar/`：OBSOLETE 倾向，仅 1 个示例文件，非主链目录（见上）。
  - `data/radar_candidates/`、`data/radar_rules/`：UNPROVEN（空目录，无文件、无脚本写入证据，可能是预留但未启用的位置）。
  - `data/raw/`：PROVEN，是 `save_radar_content.py`/`select_radar.py` 的实际输入源，5 个真实采集文件。
  - `data/metrics/`：DRAFT/UNPROVEN，表头已建但所有数据行核心字段（阅读量/点赞/评论/收益/发布时间）为空，Feedback 阶段尚无一条完整记录，判定为"结构已就位、内容未验证"。
  - `outputs/daily_runs/`：PROVEN，主链落地目录，36 个文件，与 `daily_radar_run.py` 输出完全对应。
  - `outputs/articles/draft/`：PROVEN（内容存在）但产出方式 UNPROVEN（见 B6，非脚本产出格式）。
  - `outputs/articles/reviewed/`、`outputs/articles/published/`、`outputs/reports/`：UNPROVEN，目录已建，无实际产物，对应 Review/Publish/Feedback 尚未跑通闭环。

- **jinritoutiao/ 嵌套子目录整体**
  判定：DUPLICATE（且判定为高优先级问题，见 B1）
  理由与证据：与根目录逐字节相同的完整镜像，独立 git 历史，未被根仓库跟踪（`git status` 显示 `??`），未被任何脚本、模板、Prompt 引用（`grep -rln jinritoutiao` 除自身外 0 命中）。判定为遗留的旧仓库快照，与当前"正在使用中的能力"无关，属于纯冗余占用，但按审计约束本次不做删除，只标记。

---

## D. Optimization Candidates（优化候选）

仅列候选，不修改任何文件。

### 必须修（建议优先处理，属于 BLOCKER/CONFLICT 级别）
1. 确认 `jinritoutiao/` 子目录的来源与去留：是应当整体移出仓库、还是加入 `.gitignore`、还是确认为一次性归档后从工作区清理。当前它是未跟踪状态但物理占据仓库根目录，且内部有独立 `.git`，存在被误改、误提交、或未来 `git add .` 时被意外纳入根仓库的风险（B1）。
2. 明确新规范体系（*_V1.md）与实际运行体系（SYSTEM_RULES.md + scripts/）的关系：要么在 `TRANSFORM_STANDARD_V1.md` / `TRANSFORM_MODULE_SUMMARY_V1.md` 中补充 A/B 模式、Shared 参数、六项拆解的归属说明，要么在 `SYSTEM_RULES.md` 顶部注明它与 *_V1.md 系列的关系（谁是当前生效标准）（B2）。
3. 统一 `ARCHITECTURE_V1.md`、`DELIVERABLE_DEFINITION_V1.md`、`STATE_DEFINITION_V1.md`、`STAGE_DEFINITION_V1.md` 四个文件内部标题的版本号（当前文件名 V1、标题 V2），确认哪个版本号是权威（B3）。
4. 核实 `selection_log.csv` 中"轻资产普通人创业"重复两条记录（`81553c31` / `d6425301`）是否为误操作，若是则需要在下一次数据维护时处理（本次不改）（B4）。

### 建议修（REDUNDANCY / GAP 级别，可排期处理）
5. 收敛"雷达原文保存"这一职责当前分散在 `data/radar/`（collect_radar.py）、`data/radar_pool/`（save_radar_content.py）、`data/radar_sources/`（daily_radar_run.py）三个目录三套字段的现状，明确唯一事实源（B5）。
6. 明确 `scripts/save_article.py` 是否仍是"保存文章"的标准方式；若实际操作已改为人工/Claude 直接写入 `outputs/articles/draft/`，应在 `TRANSFORM_MODULE_SUMMARY_V1.md` 或相关文档中如实登记当前真实流程，而不是让脚本定义与实际产物长期不一致（B6）。
7. 为 Review/Revision/Publish/Feedback 补充至少一次端到端真实跑通的记录，或在文档中明确当前这四个阶段处于"结构已建、尚未投产"的真实状态（与 README.md 的 DRAFT 标注对齐）（B7）。
8. 为"当前处于哪个 Stage / 失败后回到哪里"设计一个可从文件直接读出的字段或索引（不要求本次实现，只是标记缺口）（B8）。
9. 核实 `prompts/templates/toutiao_article_prompt.md` + `scripts/generate_prompt.py` 这一套是否已被 `daily_radar_run.py` 的 A/B Prompt 生成完全取代，若是则登记为历史遗留候选。
10. 核实 8 个孤立模板文件（`publish_check_template.md` 等，见 B9）当前是否仍在人工/对话流程中被引用，若确认无人使用，登记为退出候选。

### 暂不处理（信息不足或影响范围小，本次只记录）
11. `scripts/render_toutiao_cover.py`（封面图生成）与主链无数据依赖，是否仍在用无法从文件证据判断，需询问实际操作者。
12. `scripts/build_notion_page.py` 与 `notion/sync_logs/` 是否仍在日常同步流程中使用，证据有限（仅 2 个历史产物）。
13. `data/radar_candidates/`、`data/radar_rules/` 两个空目录的设计意图不明，暂不处理。
14. `data/metrics/dual_line_metrics.csv` 所有数据行核心字段为空，属于 Feedback 阶段尚未投产的自然结果，非本次审计范围内的异常。
