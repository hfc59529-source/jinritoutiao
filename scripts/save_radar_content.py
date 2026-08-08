#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require_today_source_date(source_date: str) -> None:
    today = dt.date.today().isoformat()
    if source_date != today:
        raise SystemExit(
            f"--source-date must be today's date ({today}). "
            "Only same-day collected topics may enter production. "
            "If there is no same-day topic, collect a new one from the teacher site first."
        )


def require_hot_source_column(source_column: str) -> None:
    if source_column != "今日爆点":
        raise SystemExit(
            "--source-column must be 今日爆点. "
            "The teacher site no longer provides 官方扶持 as a production source."
        )


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.strip()).strip("-")
    return cleaned[:60] or "radar"


def read_source(path_text: str) -> tuple[Path, str]:
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    return path, path.read_text(encoding="utf-8")


def build_content(args: argparse.Namespace, copy_id: str, content_hash: str, content: str) -> str:
    saved_at = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""---
id: {copy_id}
title: {args.title}
hotspot_type: {args.hotspot_type}
source_date: {args.source_date}
source_column: {args.source_column}
source_url: {args.source_url}
source_label: {args.source_label}
status: pooled
content_hash: {content_hash}
saved_at: {saved_at}
policy: radar_original_content_saved_without_rewrite
---

# {args.title}

## 基本信息

- 文案ID：{copy_id}
- 标题：{args.title}
- 热点类型：{args.hotspot_type}
- 来源日期：{args.source_date}
- 来源栏目：{args.source_column}
- 来源链接：{args.source_url}
- 来源标签：{args.source_label}
- 保存时间：{saved_at}
- 内容哈希：{content_hash}

## 雷达文案原文

{content.rstrip()}
"""


def append_log(args: argparse.Namespace, copy_id: str, out_path: Path, content_hash: str) -> None:
    log_path = ROOT / "data" / "radar_pool" / "pool_log.csv"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()
    with log_path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        if not exists:
            writer.writerow([
                "文案ID",
                "标题",
                "热点类型",
                "来源日期",
                "来源栏目",
                "来源链接",
                "来源标签",
                "保存路径",
                "内容哈希",
                "保存时间",
            ])
        writer.writerow([
            copy_id,
            args.title,
            args.hotspot_type,
            args.source_date,
            args.source_column,
            args.source_url,
            args.source_label,
            str(out_path),
            content_hash,
            dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Save full radar copy content into the radar pool before selection.")
    parser.add_argument("source", help="Markdown/text file containing full radar copy content.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--hotspot-type", required=True)
    parser.add_argument("--source-date", required=True)
    parser.add_argument("--source-column", default="今日爆点")
    parser.add_argument("--source-url", default="")
    parser.add_argument("--source-label", default="")
    args = parser.parse_args()
    require_today_source_date(args.source_date)
    require_hot_source_column(args.source_column)

    _, content = read_source(args.source)
    content_hash = hashlib.sha1(content.encode("utf-8")).hexdigest()[:12]
    copy_id = f"{args.source_date}_{slugify(args.title)}_{content_hash[:8]}"
    out_path = ROOT / "data" / "radar_pool" / f"{slugify(copy_id)}.radar.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_content(args, copy_id, content_hash, content).rstrip() + "\n", encoding="utf-8")
    append_log(args, copy_id, out_path, content_hash)
    print(out_path)


if __name__ == "__main__":
    main()
