#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEVELS = {"高", "中", "低"}
TIME_WINDOWS = {"长", "中", "短"}
DUAL_VALUES = {"YES", "NO"}
PRIORITIES = {"P1", "P2", "P3", "不发"}


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text.strip()).strip("-")
    return cleaned[:60] or "radar"


def read_source(path_text: str) -> tuple[Path, str]:
    path = Path(path_text)
    if not path.is_absolute():
        path = ROOT / path
    return path, path.read_text(encoding="utf-8")


def validate(name: str, value: str, allowed: set[str]) -> None:
    if value not in allowed:
        allowed_text = " / ".join(sorted(allowed))
        raise SystemExit(f"{name} must be one of: {allowed_text}")


def build_card(args: argparse.Namespace, source_path: Path, copy_id: str) -> str:
    return f"""# 爆点文案筛选卡：{args.title}

筛选对象：老师网站已经生成完成的爆点文案。
前置要求：雷达文案完整原文必须已保存到 data/radar_pool/。

## 基本信息

- 文案ID：{copy_id}
- 原标题：{args.title}
- 热点类型：{args.hotspot_type}
- 来源日期：{args.source_date}
- 雷达内容路径：{source_path}

## 最小筛选参数

| 参数 | 取值 | 备注 |
| --- | --- | --- |
| 头条账号适配 | {args.account_fit} | 是否属于账号当前内容范围，是否接近历史高表现题型 |
| 普通人相关度 | {args.public_relevance} | 是否适合普通大众阅读，是否过度垂直 |
| 冲突强度 | {args.conflict_strength} | 冲突是否集中、清楚、有讨论性 |
| 利益或风险强度 | {args.benefit_risk_strength} | 是否有明确利益、损失、风险或成本 |
| 评论空间 | {args.comment_space} | 是否容易引发评论和站队 |
| 热点剩余时效 | {args.time_window} | 是否仍在发酵，是否能支撑 4-6 小时后的 B 稿 |
| 今日爆款评分 | {args.viral_score} | 老师网站/平台给出的今日爆款、确认S+、素材质量等分数 |
| 平台扶持评分 | {args.support_score} | 平台扶持、流量倾斜、活动匹配等分数 |
| 双线生产适配 | {args.dual_line_fit} | 是否能生成 A/B 两篇明显不同文案 |

## 筛选结果

- 今日优先级：{args.priority}
- 来源标签：{args.source_label}
- 入选理由：{args.reason}

## 推荐执行

```text
{recommendation(args.priority)}
```
"""


def recommendation(priority: str) -> str:
    if priority == "P1":
        return "进入 A稿 -> 其他题 -> B稿"
    if priority == "P2":
        return "只走 A线"
    if priority == "P3":
        return "有空位再发"
    return "暂不进入生产"


def append_log(args: argparse.Namespace, copy_id: str) -> None:
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
                "账号适配",
                "普通人相关度",
                "冲突强度",
                "利益或风险强度",
                "评论空间",
                "热点剩余时效",
                "今日爆款评分",
                "平台扶持评分",
                "双线生产适配",
                "今日优先级",
                "来源标签",
                "入选理由",
            ])
        writer.writerow([
            copy_id,
            args.title,
            args.hotspot_type,
            args.account_fit,
            args.public_relevance,
            args.conflict_strength,
            args.benefit_risk_strength,
            args.comment_space,
            args.time_window,
            args.viral_score,
            args.support_score,
            args.dual_line_fit,
            args.priority,
            args.source_label,
            args.reason,
        ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a radar selection card before dual-line production.")
    parser.add_argument("source", help="Finished radar copy from teacher site.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--hotspot-type", required=True)
    parser.add_argument("--source-date", required=True)
    parser.add_argument("--account-fit", required=True, choices=sorted(LEVELS))
    parser.add_argument("--public-relevance", required=True, choices=sorted(LEVELS))
    parser.add_argument("--conflict-strength", required=True, choices=sorted(LEVELS))
    parser.add_argument("--benefit-risk-strength", required=True, choices=sorted(LEVELS))
    parser.add_argument("--comment-space", required=True, choices=sorted(LEVELS))
    parser.add_argument("--time-window", required=True, choices=sorted(TIME_WINDOWS))
    parser.add_argument("--viral-score", type=int, default=0, help="0-100 score for today's viral potential.")
    parser.add_argument("--support-score", type=int, default=0, help="0-100 score for platform support.")
    parser.add_argument("--source-label", default="", help="Original platform label, e.g. 素材质量78·可用 or S+·92分.")
    parser.add_argument("--dual-line-fit", required=True, choices=sorted(DUAL_VALUES))
    parser.add_argument("--priority", required=True, choices=sorted(PRIORITIES))
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    if not 0 <= args.viral_score <= 100:
        raise SystemExit("--viral-score must be between 0 and 100")
    if not 0 <= args.support_score <= 100:
        raise SystemExit("--support-score must be between 0 and 100")

    source_path, content = read_source(args.source)
    digest = hashlib.sha1(content.encode("utf-8")).hexdigest()[:8]
    copy_id = f"{args.source_date}_{slugify(args.title)}_{digest}"

    out_path = ROOT / "data" / "radar_selection" / f"{slugify(copy_id)}.selection.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_card(args, source_path, copy_id).rstrip() + "\n", encoding="utf-8")
    append_log(args, copy_id)
    print(out_path)


if __name__ == "__main__":
    main()
