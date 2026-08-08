#!/usr/bin/env python3
"""Pre-filter list-page radar candidates before fetching detail pages.

Pre-Filter is an acquisition decision inside Collect. It only answers whether a
list item is worth spending one detail fetch. It must not assign P1/P2/P3.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIGNAL_RESULTS = {"YES", "NO", "UNKNOWN"}
DECISIONS = {"FETCH", "SKIP", "REVIEW"}


def require_today_source_date(source_date: str) -> None:
    today = dt.date.today().isoformat()
    if source_date != today:
        raise SystemExit(
            f"--source-date must be today's date ({today}). "
            "Only same-day list items may enter Pre-Filter."
        )


def require_hot_source_column(source_column: str) -> None:
    if source_column != "今日爆点":
        raise SystemExit("--source-column must be 今日爆点. Pre-Filter only scans 今日爆点.")


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.strip()).strip("-")
    return cleaned[:60] or "radar"


def decide(args: argparse.Namespace) -> tuple[str, str]:
    known_no = [
        args.public_relevance_signal == "NO",
        args.conflict_or_stakes_signal == "NO",
        args.freshness_signal == "NO",
    ]
    unknown = [
        args.public_relevance_signal == "UNKNOWN",
        args.conflict_or_stakes_signal == "UNKNOWN",
        args.freshness_signal == "UNKNOWN",
    ]
    if any(known_no):
        return "SKIP", "标题/列表廉价信息已出现明确淘汰信号，不值得抓详情。"
    if any(unknown):
        return "REVIEW", "信息不足，不提前淘汰；人工或脚本可决定是否抓详情。"
    return "FETCH", "三项廉价信号均通过，值得抓取详情页。"


def build_record(args: argparse.Namespace, item_id: str, decision: str, decision_reason: str) -> str:
    return f"""# 今日爆点预筛：{args.title}

Pre-Filter 是 Collect 内部的 Acquisition Decision（采集决策），只回答：这条是否值得花一次详情采集成本？

Pre-Filter 不允许输出 P1/P2/P3，不替代 Selection V2。

## 基本信息

- 预筛ID：{item_id}
- 标题：{args.title}
- 热点类型：{args.hotspot_type}
- 来源日期：{args.source_date}
- 来源栏目：{args.source_column}
- 榜单位置：{args.rank}
- 列表评分：{args.list_score}
- 来源标签：{args.source_label}

## 三项廉价信号

| 信号 | 结果 | 判断问题 |
| --- | --- | --- |
| 大众相关性 | {args.public_relevance_signal} | 标题本身能否看出普通人相关性？ |
| 冲突/利益/风险 | {args.conflict_or_stakes_signal} | 是否存在明确冲突、利益或风险信号？ |
| 新鲜度 | {args.freshness_signal} | 热点是否仍然新鲜？ |

## 预筛结论

- 采集决策：{decision}
- 判断理由：{args.reason or decision_reason}

## 后续纪律

- FETCH / REVIEW 后仍必须抓详情页，保存完整雷达原文，才能进入 Selection V2。
- SKIP 只允许用于明显淘汰；不确定时不能跳过。
- 本文件不得作为正式发布资源决策依据。
"""


def append_log(args: argparse.Namespace, item_id: str, decision: str, decision_reason: str, out_path: Path) -> None:
    log_path = ROOT / "data" / "radar_prefilter" / "prefilter_log.csv"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()
    with log_path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        if not exists:
            writer.writerow([
                "预筛ID",
                "标题",
                "热点类型",
                "来源日期",
                "来源栏目",
                "榜单位置",
                "列表评分",
                "来源标签",
                "大众相关性信号",
                "冲突利益风险信号",
                "新鲜度信号",
                "采集决策",
                "判断理由",
                "保存路径",
                "记录时间",
            ])
        writer.writerow([
            item_id,
            args.title,
            args.hotspot_type,
            args.source_date,
            args.source_column,
            args.rank,
            args.list_score,
            args.source_label,
            args.public_relevance_signal,
            args.conflict_or_stakes_signal,
            args.freshness_signal,
            decision,
            args.reason or decision_reason,
            str(out_path),
            dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-filter 今日爆点 list items before detail fetch.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--hotspot-type", default="")
    parser.add_argument("--source-date", required=True)
    parser.add_argument("--source-column", default="今日爆点")
    parser.add_argument("--rank", default="", help="List rank or pool position, if visible.")
    parser.add_argument("--list-score", default="", help="Cheap list-page score/label, if visible.")
    parser.add_argument("--source-label", default="", help="Cheap list-page source labels, if visible.")
    parser.add_argument("--public-relevance-signal", required=True, choices=sorted(SIGNAL_RESULTS))
    parser.add_argument("--conflict-or-stakes-signal", required=True, choices=sorted(SIGNAL_RESULTS))
    parser.add_argument("--freshness-signal", required=True, choices=sorted(SIGNAL_RESULTS))
    parser.add_argument("--reason", default="")
    args = parser.parse_args()

    require_today_source_date(args.source_date)
    require_hot_source_column(args.source_column)
    decision, decision_reason = decide(args)

    digest_source = "|".join([
        args.source_date,
        args.title,
        args.rank,
        args.list_score,
        args.source_label,
    ])
    digest = hashlib.sha1(digest_source.encode("utf-8")).hexdigest()[:8]
    item_id = f"{args.source_date}_{slugify(args.title)}_{digest}"
    out_path = ROOT / "data" / "radar_prefilter" / f"{slugify(item_id)}.prefilter.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_record(args, item_id, decision, decision_reason).rstrip() + "\n", encoding="utf-8")
    append_log(args, item_id, decision, decision_reason, out_path)
    print(f"{decision}\t{out_path}")


if __name__ == "__main__":
    main()
