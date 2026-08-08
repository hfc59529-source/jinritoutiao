#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_METHOD = "Radar Source"


def require_today_source_date(source_date: str) -> None:
    today = dt.date.today().isoformat()
    if source_date != today:
        raise SystemExit(
            f"--source-date must be today's date ({today}). "
            "Only same-day collected topics may enter the daily production run. "
            "If there is no same-day topic, collect a new one from the teacher site first."
        )


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.strip())
    cleaned = cleaned.strip("-")
    return cleaned[:60] or "radar"


def ensure(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_text(path_text: str) -> tuple[Path, str]:
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    return path, path.read_text(encoding="utf-8")


def write(path: Path, content: str) -> None:
    ensure(path.parent)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def source_markdown(args: argparse.Namespace, source_path: Path, content: str, source_id: str) -> str:
    return f"""---
id: {source_id}
title: {args.title}
hotspot_type: {args.hotspot_type}
source_date: {args.source_date}
original_link: {args.original_link}
original_type: {args.original_type}
selection_card: {args.selection_card}
status: frozen
source_file: {source_path}
content_hash: {hashlib.sha1(content.encode("utf-8")).hexdigest()[:12]}
created_at: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
policy: original_text_is_frozen
---

# {args.title}

## 雷达原文

{content.rstrip()}
"""


def shared_params(args: argparse.Namespace, source_id: str, original_facts: str) -> str:
    template = (ROOT / "templates" / "shared_params_template.md").read_text(encoding="utf-8")
    return (
        template.replace("- 原始选题ID：", f"- 原始选题ID：{source_id}")
        .replace("- 标题：", f"- 标题：{args.title}")
        .replace("- 热点类型：", f"- 热点类型：{args.hotspot_type}")
        .replace("- 来源日期：", f"- 来源日期：{args.source_date}")
        .replace("### 1. 原始事实\n\n", f"### 1. 原始事实\n\n{original_facts.rstrip() or '同雷达原文'}\n\n")
    )


def transform_params() -> str:
    return (ROOT / "templates" / "transform_params_template.md").read_text(encoding="utf-8")


def transform_prompt(source_content: str, original_facts: str) -> str:
    """拼装 Transform Prompt（Execution Adapter）。

    Shared 七项、Transform 参数不再拼入生成 Prompt——Shared 七项降级为 Quality
    Review 参照清单，Transform 参数文件只作执行记录，两者都不参与生成指令。
    """
    template = (ROOT / "templates" / "transform_radar_source_prompt.md").read_text(encoding="utf-8")
    return (
        template.replace("{{RADAR_ORIGINAL}}", source_content.rstrip())
        .replace("{{ORIGINAL_FACTS}}", original_facts.rstrip() or "同雷达原文")
    )


def metadata(args: argparse.Namespace, source_id: str, paths: dict[str, Path]) -> str:
    data = {
        "id": source_id,
        "title": args.title,
        "hotspot_type": args.hotspot_type,
        "source_date": args.source_date,
        "original_link": args.original_link,
        "original_type": args.original_type,
        "selection_card": args.selection_card,
        "status": "frozen",
        "production_method": PRODUCTION_METHOD,
        "paths": {key: str(value) for key, value in paths.items()},
        "parameter_layers": {
            "radar_selection": "爆点文案筛选卡",
            "radar_source": "冻结完整雷达原文（含 Original Radar Production Prompt）",
            "transform": "Execution Adapter：Target Format Contract + Fact Boundary",
            "output": "Article Draft",
            "shared": "Shared 七项（Quality Review 参照清单，不参与生成）",
        },
        "metrics_fields": [
            "原始选题ID",
            "生产方式",
            "标题",
            "发布时间",
            "阅读量",
            "点赞",
            "评论",
            "收益",
        ],
        "production_rule": {
            "priority": "P1/P2/P3 只决定生产优先级，不决定生成篇数。",
            "transform": "直接执行 Original Radar Production Prompt，Transform 只提供 Target Format Contract 和 Fact Boundary 两个执行适配约束，不重新指导怎么写。",
            "review": "Fact Boundary Review 与 Quality Review 两轮独立审核，不能合并。",
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def position_markdown(args: argparse.Namespace, source_id: str, paths: dict[str, Path]) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""# Current Position：{args.title}

关联 ID：{source_id}

本文件是该选题唯一的位置台账（Single Source of Truth）。
Stage/State 取值只使用 STAGE_DEFINITION_V1.md / STATE_DEFINITION_V1.md 已定义的名词，
Current Actor 取该 Stage 在 ACTOR_DEFINITION_V1.md 中的 Primary Owner。
后续状态迁移由 scripts/update_position.py 更新，不手工编辑本文件的字段值。

## Production

- Enabled: YES
- Current Stage: Transform
- Current State: Ready for Transform
- Current Deliverable: {paths["transform_prompt"]}
- Current Actor: Claude
- Next Action: 直接执行 Transform Prompt 里的 Original Radar Production Prompt，生成 Article Draft，保存到 outputs/articles/draft/，随后进入 Fact Boundary Review
- On Failure: 留在 Transform，修复输入（雷达原文/Prompt）后重新执行
- Last Updated: {now} by daily_radar_run.py
"""


def daily_index(args: argparse.Namespace, source_id: str, paths: dict[str, Path]) -> str:
    return f"""# 每日雷达生产运行包：{args.title}

运行日期：{dt.date.today().isoformat()}

## 状态

- 雷达原文：已冻结（含 Original Radar Production Prompt）
- 爆点文案筛选卡：{args.selection_card or "未关联"}
- Shared 七项：已生成（Quality Review 参照，不参与生成）
- Transform 执行记录：已生成
- Transform Prompt：已生成（Execution Adapter：Target Format Contract + Fact Boundary）
- 数据记录字段：已固定

## 文件

- 爆点文案筛选卡：{args.selection_card or "未关联"}
- 雷达原文库：{paths["source"]}
- Shared 七项（Quality Review 参照）：{paths["shared_params"]}
- Transform 执行记录：{paths["transform_params"]}
- Transform Prompt：{paths["transform_prompt"]}
- 元数据：{paths["metadata"]}
- 当前位置台账：{paths["position"]}

## 今日执行顺序

1. 从爆点文案筛选卡确认今日优先级。
2. P1 优先生产，P2 可以生产，P3 有空位再生产，不发则停止。
3. 冻结完整雷达原文（含 Original Radar Production Prompt）。
4. Transform：直接执行 Original Radar Production Prompt，套用 Target Format Contract 和 Fact Boundary，生成 Article Draft。
5. Fact Boundary Review：独立一轮，逐句核对事实边界。
6. Quality Review：Fact Boundary Review PASS 后进行，参照 Shared 七项检查覆盖与阅读质量，产出 Article Master。
7. Review 后进入 Revision 或 Publish。
8. 发布后进入 Feedback，并与 Baseline 对照。

## 主链

```text
Collect
  ↓
Selection
  ↓
Radar Source（含 Original Radar Production Prompt）
  ↓
Transform（Execution Adapter）
  ↓
Article Draft
  ↓
Fact Boundary Review
  ↓
Quality Review（参照 Shared 七项）
  ↓
Article Master
  ↓
Revision / Publish
  ↓
Feedback
```

## 关联 ID

```text
{source_id}
```
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a daily radar production run package.")
    parser.add_argument("source", help="Raw radar markdown file.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--hotspot-type", required=True)
    parser.add_argument("--source-date", required=True)
    parser.add_argument("--original-link", default="")
    parser.add_argument("--original-type", default="雷达文案")
    parser.add_argument("--facts-file", default="", help="Optional markdown file with original facts.")
    parser.add_argument("--selection-card", default="", help="Optional radar selection card path.")
    args = parser.parse_args()
    require_today_source_date(args.source_date)

    source_path, raw_content = read_text(args.source)
    _, facts_content = read_text(args.facts_file) if args.facts_file else (Path(), "")
    source_id = f"{args.source_date}_{slugify(args.title)}"
    base_name = slugify(source_id)

    paths = {
        "source": ROOT / "data" / "radar_sources" / f"{base_name}.md",
        "shared_params": ROOT / "outputs" / "daily_runs" / f"{base_name}.shared_params.md",
        "transform_params": ROOT / "outputs" / "daily_runs" / f"{base_name}.transform_params.md",
        "transform_prompt": ROOT / "prompts" / "generated" / f"{base_name}.transform.prompt.md",
        "metadata": ROOT / "outputs" / "daily_runs" / f"{base_name}.metadata.json",
        "index": ROOT / "outputs" / "daily_runs" / f"{base_name}.index.md",
        "position": ROOT / "outputs" / "daily_runs" / f"{base_name}.position.md",
    }

    write(paths["source"], source_markdown(args, source_path, raw_content, source_id))
    write(paths["shared_params"], shared_params(args, source_id, facts_content))
    write(paths["transform_params"], transform_params())
    write(paths["transform_prompt"], transform_prompt(raw_content, facts_content))
    write(paths["metadata"], metadata(args, source_id, paths))
    write(paths["index"], daily_index(args, source_id, paths))
    write(paths["position"], position_markdown(args, source_id, paths))

    print(paths["index"])
    print(paths["position"])


if __name__ == "__main__":
    main()
