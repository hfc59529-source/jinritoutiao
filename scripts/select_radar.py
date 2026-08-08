#!/usr/bin/env python3
"""爆点文案筛选卡 V2：Hard Gate → Internal Ranking → External Signal → 当日相对排序。

不再用"7项高/中/低相加"的绝对评分模式。P1/P2/P3 不代表绝对分数，
只代表当天候选素材之间的相对优先顺序；任一 Hard Gate 为 FAIL 时强制"不发"。
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEVELS = {"高", "中", "低"}
GATE_RESULTS = {"PASS", "FAIL"}
PRIORITIES = {"P1", "P2", "P3", "不发"}


def require_today_source_date(source_date: str) -> None:
    today = dt.date.today().isoformat()
    if source_date != today:
        raise SystemExit(
            f"--source-date must be today's date ({today}). "
            "Only same-day collected topics may be selected. "
            "If there is no same-day topic, collect a new one from the teacher site first."
        )


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w一-鿿]+", "-", text.strip()).strip("-")
    return cleaned[:60] or "radar"


def read_source(path_text: str) -> tuple[Path, str]:
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    return path, path.read_text(encoding="utf-8")


def gate_summary(args: argparse.Namespace) -> tuple[bool, list[str]]:
    gates = [
        ("G1｜Source Completeness（完整雷达详情是否存在）", args.gate_source_completeness),
        ("G2｜Fact Boundary（核心事实是否足够明确，能否不自行补事实成文）", args.gate_fact_boundary),
        ("G3｜Risk Boundary（是否存在当前无法处理的事实/法律/安全风险）", args.gate_risk_boundary),
        ("G4｜Freshness（是否仍处于有效发布窗口）", args.gate_freshness),
    ]
    failed = [name for name, result in gates if result == "FAIL"]
    return len(failed) == 0, [name for name, _ in gates]


def build_card(args: argparse.Namespace, source_path: Path, copy_id: str, gate_pass: bool) -> str:
    gate_rows = "\n".join(
        f"| {name} | {result} |"
        for name, result in [
            ("G1｜Source Completeness", args.gate_source_completeness),
            ("G2｜Fact Boundary", args.gate_fact_boundary),
            ("G3｜Risk Boundary", args.gate_risk_boundary),
            ("G4｜Freshness", args.gate_freshness),
        ]
    )
    gate_verdict = "PASS：可进入内部排序" if gate_pass else "FAIL：直接不发，以下排序仅作记录，不影响本次结果"
    effective_priority = args.priority if gate_pass else "不发"

    return f"""# 爆点文案筛选卡：{args.title}

筛选对象：老师网站已经生成完成的爆点文案。
前置要求：雷达文案完整原文必须已保存到 data/radar_pool/。
Selection 只回答"今天已采到的候选里，哪一条最值得占用发布位"，不重新判断"这是不是热点"。

## 基本信息

- 文案ID：{copy_id}
- 原标题：{args.title}
- 热点类型：{args.hotspot_type}
- 来源日期：{args.source_date}
- 雷达内容路径：{source_path}

## ① Hard Gate（任一 FAIL → 不发）

| Gate | 结果 |
| --- | --- |
{gate_rows}

Gate 说明：{args.gate_notes}

**Gate 判定：{gate_verdict}**

## ② Internal Ranking（{'仅记录，Gate未通过不生效' if not gate_pass else '当日候选排序依据'}）

| 变量 | 取值 | 判断问题 |
| --- | --- | --- |
| Public Relevance（大众相关度） | {args.public_relevance} | 有多少普通头条用户会觉得"这和我有关"？ |
| Stakes（利益/风险） | {args.stakes} | 用户不关注这件事，会损失/错过什么？是否具体？ |
| Conflict Clarity（冲突清晰度） | {args.conflict_clarity} | 能否用一句话说清楚矛盾双方和反差？ |
| Discussion Tension（讨论张力） | {args.discussion_tension} | 是否存在普通人能理解的判断分歧，而非单纯情绪站队？ |

## ③ External Signal（外部信号，不与②相加，并列参考）

- 老师网站/平台今日爆款评分：{args.viral_score}
- 来源标签：{args.source_label}

## 筛选结果

- 今日优先级：{effective_priority}（相对当日候选的排序，不是绝对分数）
- 入选理由：{args.reason}

## 推荐执行

```text
{recommendation(effective_priority)}
```
"""


def recommendation(priority: str) -> str:
    if priority == "P1":
        return "当日候选中优先生产"
    if priority == "P2":
        return "可以生产，排在P1之后"
    if priority == "P3":
        return "有空位再生产"
    return "不发（Gate未通过，或当日排序判断不值得占用发布位）"


def append_log(args: argparse.Namespace, copy_id: str, gate_pass: bool, effective_priority: str) -> None:
    log_path = ROOT / "data" / "radar_selection" / "selection_log.csv"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()
    with log_path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        if not exists:
            writer.writerow([
                "文案ID",
                "原标题",
                "热点类型",
                "G1_source_completeness",
                "G2_fact_boundary",
                "G3_risk_boundary",
                "G4_freshness",
                "gate_notes",
                "gate_pass",
                "public_relevance",
                "stakes",
                "conflict_clarity",
                "discussion_tension",
                "viral_score",
                "source_label",
                "今日优先级",
                "入选理由",
            ])
        writer.writerow([
            copy_id,
            args.title,
            args.hotspot_type,
            args.gate_source_completeness,
            args.gate_fact_boundary,
            args.gate_risk_boundary,
            args.gate_freshness,
            args.gate_notes,
            "PASS" if gate_pass else "FAIL",
            args.public_relevance,
            args.stakes,
            args.conflict_clarity,
            args.discussion_tension,
            args.viral_score,
            args.source_label,
            effective_priority,
            args.reason,
        ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a V2 radar selection card: Hard Gate -> Internal Ranking -> External Signal -> relative priority.")
    parser.add_argument("source", help="Finished radar copy from teacher site.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--hotspot-type", required=True)
    parser.add_argument("--source-date", required=True)

    parser.add_argument("--gate-source-completeness", required=True, choices=sorted(GATE_RESULTS))
    parser.add_argument("--gate-fact-boundary", required=True, choices=sorted(GATE_RESULTS))
    parser.add_argument("--gate-risk-boundary", required=True, choices=sorted(GATE_RESULTS))
    parser.add_argument("--gate-freshness", required=True, choices=sorted(GATE_RESULTS))
    parser.add_argument("--gate-notes", required=True, help="任一Gate为FAIL时必须说明具体原因。")

    parser.add_argument("--public-relevance", required=True, choices=sorted(LEVELS))
    parser.add_argument("--stakes", required=True, choices=sorted(LEVELS))
    parser.add_argument("--conflict-clarity", required=True, choices=sorted(LEVELS))
    parser.add_argument("--discussion-tension", required=True, choices=sorted(LEVELS))

    parser.add_argument("--viral-score", type=int, default=0, help="0-100，老师网站/平台给出的今日爆款评分，仅作外部信号参考，不与内部排序相加。")
    parser.add_argument("--source-label", default="", help="原始平台标签，例如 素材质量78·可用 或 S+·92分。")

    parser.add_argument("--priority", required=True, choices=sorted(PRIORITIES), help="当日候选间的相对优先级，Gate未通过时会被强制改写为'不发'。")
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()

    if not 0 <= args.viral_score <= 100:
        raise SystemExit("--viral-score must be between 0 and 100")
    require_today_source_date(args.source_date)

    gate_pass, _ = gate_summary(args)
    if not gate_pass and not args.gate_notes.strip():
        raise SystemExit("Gate 存在 FAIL 时，--gate-notes 必须说明具体原因。")
    effective_priority = args.priority if gate_pass else "不发"

    source_path, content = read_source(args.source)
    digest = hashlib.sha1(content.encode("utf-8")).hexdigest()[:8]
    copy_id = f"{args.source_date}_{slugify(args.title)}_{digest}"

    out_path = ROOT / "data" / "radar_selection" / f"{slugify(copy_id)}.selection.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        build_card(args, source_path, copy_id, gate_pass).rstrip() + "\n", encoding="utf-8"
    )
    append_log(args, copy_id, gate_pass, effective_priority)
    print(out_path)
    if not gate_pass:
        print(f"NOTICE: Hard Gate FAIL -> priority forced to 不发 (requested: {args.priority})")


if __name__ == "__main__":
    main()
