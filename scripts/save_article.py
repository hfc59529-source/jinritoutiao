#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Save GPT article draft with metadata.")
    parser.add_argument("source_md", help="Markdown file containing generated article.")
    parser.add_argument("--prompt-file", default="")
    parser.add_argument("--status", default="draft")
    parser.add_argument("--out-dir", default=str(ROOT / "outputs" / "articles" / "draft"))
    args = parser.parse_args()

    source = Path(args.source_md)
    if not source.is_absolute():
        source = ROOT / source
    content = source.read_text(encoding="utf-8").rstrip()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date = dt.datetime.now().strftime("%Y-%m-%d")
    out_path = out_dir / f"{date}_{source.stem}.article.md"
    out_path.write_text(
        f"""---
source_file: {source}
prompt_file: {args.prompt_file}
status: {args.status}
saved_at: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

{content}
""",
        encoding="utf-8",
    )
    print(out_path)


if __name__ == "__main__":
    main()

