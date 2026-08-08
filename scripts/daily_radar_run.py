#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_LINES = {
    "A": "Radar Direct",
    "B": "Protocol Generate",
}


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


def simple_analysis_markdown(args: argparse.Namespace, source_id: str) -> str:
    return f"""# 雷达简单拆解：{args.title}

## 基本信息

- 原始选题ID：{source_id}
- 标题：{args.title}
- 热点类型：{args.hotspot_type}
- 拆解日期：{dt.date.today().isoformat()}

## 六项拆解

### 1. 开头方式


### 2. 结构顺序


### 3. 冲突位置


### 4. 普通人代入方式


### 5. 情绪推进


### 6. 评论入口


## 给 B 线调用的协议摘要

```text
开头方式：
结构顺序：
冲突位置：
普通人代入方式：
情绪推进：
评论入口：
```
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


def line_params(template_name: str) -> str:
    return (ROOT / "templates" / template_name).read_text(encoding="utf-8")


def line_a_prompt(source_content: str, original_facts: str, shared_path: Path, line_a_path: Path) -> str:
    template = (ROOT / "templates" / "line_a_radar_direct_prompt.md").read_text(encoding="utf-8")
    return (
        template.replace("{{RADAR_ORIGINAL}}", source_content.rstrip())
        .replace("{{ORIGINAL_FACTS}}", original_facts.rstrip() or "同雷达原文")
        .replace("{{SHARED_PARAMS}}", shared_path.read_text(encoding="utf-8").rstrip())
        .replace("{{LINE_A_PARAMS}}", line_a_path.read_text(encoding="utf-8").rstrip())
    )


def line_b_prompt(
    args: argparse.Namespace,
    original_facts: str,
    analysis_path: Path,
    shared_path: Path,
    line_b_path: Path,
) -> str:
    template = (ROOT / "templates" / "line_b_protocol_generate_prompt.md").read_text(encoding="utf-8")
    analysis = analysis_path.read_text(encoding="utf-8")
    return (
        template.replace("{{TOPIC}}", args.title)
        .replace("{{ORIGINAL_FACTS}}", original_facts.rstrip() or "同雷达原文")
        .replace("{{SHARED_PARAMS}}", shared_path.read_text(encoding="utf-8").rstrip())
        .replace("{{LINE_B_PARAMS}}", line_b_path.read_text(encoding="utf-8").rstrip())
        .replace("{{SIMPLE_ANALYSIS}}", analysis.rstrip())
    )


def publish_schedule(source_id: str) -> str:
    template = (ROOT / "templates" / "dual_line_publish_schedule.md").read_text(encoding="utf-8")
    return template.replace("| 1 |  | Radar Direct", f"| 1 | {source_id} | Radar Direct").replace(
        "| 3 |  | Protocol Generate", f"| 3 | {source_id} | Protocol Generate"
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
        "paths": {key: str(value) for key, value in paths.items()},
        "parameter_layers": {
            "radar_selection": "爆点文案筛选卡",
            "plain_text": "雷达原文",
            "shared": "公共参数",
            "line_a": "A线专属参数",
            "line_b": "B线专属参数",
            "output": "生成文案",
        },
        "production_lines": PRODUCTION_LINES,
        "simple_analysis_fields": [
            "开头方式",
            "结构顺序",
            "冲突位置",
            "普通人代入方式",
            "情绪推进",
            "评论入口",
        ],
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
        "publish_rule": {
            "sequence": "A稿 -> 插入一个其他选题 -> B稿",
            "interval": "每篇间隔约2小时",
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def position_line_block(
    line: str,
    enabled: bool,
    deliverable: Path,
    now: str,
) -> str:
    if not enabled:
        return f"""## {line} Line

- Enabled: NO
"""
    return f"""## {line} Line

- Enabled: YES
- Current Stage: Transform
- Current State: Ready for Transform
- Current Deliverable: {deliverable}
- Current Actor: Claude
- Next Action: 根据 Prompt 生成头条文案 V1，保存到 outputs/articles/draft/
- On Failure: 留在 Transform，修复输入（雷达原文/参数/Prompt）后重新执行
- Last Updated: {now} by daily_radar_run.py
"""


def position_markdown(args: argparse.Namespace, source_id: str, paths: dict[str, Path], b_enabled: bool) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""# Current Position：{args.title}

关联 ID：{source_id}

本文件是该选题唯一的位置台账（Single Source of Truth）。A/B 两条生产线分区独立记录，
Stage/State 取值只使用 STAGE_DEFINITION_V1.md / STATE_DEFINITION_V1.md 已定义的名词，
Current Actor 取该 Stage 在 ACTOR_DEFINITION_V1.md 中的 Primary Owner。
后续状态迁移由 scripts/update_position.py 更新，不手工编辑本文件的字段值。

{position_line_block("A", True, paths["line_a_prompt"], now)}
{position_line_block("B", b_enabled, paths["line_b_prompt"], now)}"""


def daily_index(args: argparse.Namespace, source_id: str, paths: dict[str, Path]) -> str:
    return f"""# 每日雷达双生产线运行包：{args.title}

运行日期：{dt.date.today().isoformat()}

## 状态

- 雷达原文：已冻结
- 爆点文案筛选卡：{args.selection_card or "未关联"}
- A线 Radar Direct Prompt：已生成
- B线 Protocol Generate Prompt：已生成
- 公共参数 Shared：已生成
- A线专属参数：已生成
- B线专属参数：已生成
- 六项拆解模板：已生成
- 发布顺序表：已生成
- 数据记录字段：已固定

## 文件

- 爆点文案筛选卡：{args.selection_card or "未关联"}
- 雷达原文库：{paths["source"]}
- 公共参数：{paths["shared_params"]}
- A线专属参数：{paths["line_a_params"]}
- B线专属参数：{paths["line_b_params"]}
- A线直转 Prompt：{paths["line_a_prompt"]}
- B线复刻 Prompt：{paths["line_b_prompt"]}
- 六项拆解：{paths["simple_analysis"]}
- 发布顺序：{paths["publish_schedule"]}
- 元数据：{paths["metadata"]}
- 当前位置台账：{paths["position"]}

## 今日执行顺序

1. 从爆点文案筛选卡确认今日优先级。
2. P1 进入 A/B 双线，P2 只走 A线，P3 有空位再发，不发则停止生产。
3. 从雷达原文提取公共参数 Shared。
4. 用“公共参数 + A线专属参数”生成 Radar Direct 稿。
5. 填写六项拆解。
6. 用“公共参数 + B线专属参数 + 六项拆解”生成 Protocol Generate 稿。
7. 发布时按“A稿 -> 其他选题 -> B稿”，每篇间隔约2小时。
8. 发布后只记录最小数据字段。

## 三层参数结构

```text
老师网站爆点文案池
  ↓
爆点文案筛选卡
  ↓
今日入选文案
  ↓
雷达原文
  ↓
公共参数 Shared
  ├─ A线专属参数
  └─ B线专属参数
      ↓
生成文案
```

## 关联 ID

```text
{source_id}
```
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a daily radar dual-track run package.")
    parser.add_argument("source", help="Raw radar markdown file.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--hotspot-type", required=True)
    parser.add_argument("--source-date", required=True)
    parser.add_argument("--original-link", default="")
    parser.add_argument("--original-type", default="雷达文案")
    parser.add_argument("--facts-file", default="", help="Optional markdown file with original facts.")
    parser.add_argument("--selection-card", default="", help="Optional radar selection card path.")
    parser.add_argument(
        "--single-line",
        action="store_true",
        help="P2/P3：只走 A 线，B 线在位置台账中标记 Enabled: NO。默认双线（P1）。",
    )
    args = parser.parse_args()
    require_today_source_date(args.source_date)

    source_path, raw_content = read_text(args.source)
    _, facts_content = read_text(args.facts_file) if args.facts_file else (Path(), "")
    source_id = f"{args.source_date}_{slugify(args.title)}"
    base_name = slugify(source_id)

    paths = {
        "source": ROOT / "data" / "radar_sources" / f"{base_name}.md",
        "shared_params": ROOT / "outputs" / "daily_runs" / f"{base_name}.shared_params.md",
        "line_a_params": ROOT / "outputs" / "daily_runs" / f"{base_name}.A_params.md",
        "line_b_params": ROOT / "outputs" / "daily_runs" / f"{base_name}.B_params.md",
        "simple_analysis": ROOT / "data" / "radar_analysis" / f"{base_name}.simple_analysis.md",
        "line_a_prompt": ROOT / "prompts" / "generated" / f"{base_name}.A_radar_direct.prompt.md",
        "line_b_prompt": ROOT / "prompts" / "generated" / f"{base_name}.B_protocol_generate.prompt.md",
        "publish_schedule": ROOT / "outputs" / "daily_runs" / f"{base_name}.publish_schedule.md",
        "metadata": ROOT / "outputs" / "daily_runs" / f"{base_name}.metadata.json",
        "index": ROOT / "outputs" / "daily_runs" / f"{base_name}.index.md",
        "position": ROOT / "outputs" / "daily_runs" / f"{base_name}.position.md",
    }

    write(paths["source"], source_markdown(args, source_path, raw_content, source_id))
    write(paths["shared_params"], shared_params(args, source_id, facts_content))
    write(paths["line_a_params"], line_params("line_a_params_template.md"))
    write(paths["line_b_params"], line_params("line_b_params_template.md"))
    write(paths["simple_analysis"], simple_analysis_markdown(args, source_id))
    write(paths["line_a_prompt"], line_a_prompt(raw_content, facts_content, paths["shared_params"], paths["line_a_params"]))
    write(
        paths["line_b_prompt"],
        line_b_prompt(args, facts_content, paths["simple_analysis"], paths["shared_params"], paths["line_b_params"]),
    )
    write(paths["publish_schedule"], publish_schedule(source_id))
    write(paths["metadata"], metadata(args, source_id, paths))
    write(paths["index"], daily_index(args, source_id, paths))
    write(paths["position"], position_markdown(args, source_id, paths, b_enabled=not args.single_line))

    print(paths["index"])
    print(paths["position"])


if __name__ == "__main__":
    main()
