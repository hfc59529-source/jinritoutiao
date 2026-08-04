#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def build_collected_markdown(source: Path, content: str) -> str:
    collected_at = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    digest = hashlib.sha1(content.encode("utf-8")).hexdigest()[:12]
    return f"""---
source_file: {source}
collected_at: {collected_at}
content_hash: {digest}
status: collected
structure_policy: keep_original
---

# 采集归档

> 本文件由脚本采集生成。下方“原始雷达文案”保持原结构，不做改写。

## 原始雷达文案

{content.rstrip()}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect radar copy without rewriting its structure.")
    parser.add_argument("source", help="Path to raw radar markdown.")
    parser.add_argument("--out-dir", default=str(ROOT / "data" / "radar"))
    args = parser.parse_args()

    source = Path(args.source)
    if not source.is_absolute():
        source = ROOT / source
    content = source.read_text(encoding="utf-8")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{source.stem}.collected.md"
    out_path.write_text(build_collected_markdown(source, content), encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()

