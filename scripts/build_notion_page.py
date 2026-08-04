#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_optional(path_text: str) -> str:
    if not path_text:
        return "未生成"
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    return path.read_text(encoding="utf-8").rstrip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Notion-ready markdown preview page.")
    parser.add_argument("--radar", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--article", default="")
    parser.add_argument("--out", default=str(ROOT / "notion" / "sync_logs" / "notion_preview.md"))
    args = parser.parse_args()

    radar = read_optional(args.radar)
    prompt = read_optional(args.prompt)
    article = read_optional(args.article)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"""# 头条内容自动化第一版预览

同步时间：{dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 状态

- 雷达文案：已采集
- Prompt：已生成
- 文章：{ "已保存" if args.article else "待生成" }
- 发布：待人工发布
- 数据采集：待发布后采集
- 复盘：待数据回收后复盘

## 文案雷达

{radar}

---

## 自动生成 Prompt

{prompt}

---

## GPT 文章

{article}

---

## 下一步

- 确认雷达文案采集格式
- 确认 Prompt 输出是否符合头条文章需求
- 确认 Notion 页面字段和数据库拆分方式
""",
        encoding="utf-8",
    )
    print(out)


if __name__ == "__main__":
    main()

