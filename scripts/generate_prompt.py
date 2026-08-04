#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "prompts" / "templates" / "toutiao_article_prompt.md"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a Toutiao article prompt from collected radar copy.")
    parser.add_argument("radar_file", help="Path to collected radar markdown.")
    parser.add_argument("--template", default=str(TEMPLATE))
    parser.add_argument("--out-dir", default=str(ROOT / "prompts" / "generated"))
    args = parser.parse_args()

    radar_file = Path(args.radar_file)
    if not radar_file.is_absolute():
        radar_file = ROOT / radar_file

    template = Path(args.template).read_text(encoding="utf-8")
    radar_content = radar_file.read_text(encoding="utf-8")
    prompt = template.replace("{{RADAR_CONTENT}}", radar_content.rstrip())

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    date = dt.datetime.now().strftime("%Y-%m-%d")
    out_path = out_dir / f"{date}_{radar_file.stem}.prompt.md"
    out_path.write_text(prompt + "\n", encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()

