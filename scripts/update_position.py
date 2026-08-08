#!/usr/bin/env python3
"""更新 outputs/daily_runs/{id}.position.md 中生产位置台账。

只负责改写已有字段，不新建选题、不新建 Stage/State 名词。
Stage/State 取值必须来自 STAGE_DEFINITION_V1.md / STATE_DEFINITION_V1.md，
Current Actor 取该 Stage 在 ACTOR_DEFINITION_V1.md 中的 Primary Owner。

新台账使用单一 `## Production` 区块；历史 A/B 台账仍可通过 --line A/B 更新。
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FIELD_ORDER = [
    "Enabled",
    "Current Stage",
    "Current State",
    "Current Deliverable",
    "Current Actor",
    "Next Action",
    "On Failure",
    "Last Updated",
]

# 合法的 Stage 迁移表，按 ARCHITECTURE_V1.md 的 Workflow 推导：
# Collect → Transform → Review → {Publish(PASS) | Revision(REVISION) | End(REJECT)}
# Revision → Review；Publish → Feedback；Feedback/End 为终态。
# 允许原地停留在同一 Stage（同 Stage 内的 State 推进）。
LEGAL_NEXT_STAGE: dict[str, set[str]] = {
    "Transform": {"Transform", "Review"},
    "Review": {"Review", "Publish", "Revision", "End"},
    "Revision": {"Revision", "Review"},
    "Publish": {"Publish", "Feedback"},
    "Feedback": {"Feedback"},
    "End": {"End"},
}


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^\w一-鿿]+", "-", text.strip())
    cleaned = cleaned.strip("-")
    return cleaned[:60] or "radar"


def position_path(source_id: str) -> Path:
    base_name = slugify(source_id)
    return ROOT / "outputs" / "daily_runs" / f"{base_name}.position.md"


def parse_sections(text: str) -> dict[str, str]:
    """按新 `## Production` 或历史 `## A/B Line` 标题切出区块。"""
    parts = re.split(r"(?=^## (?:Production|[AB] Line)$)", text, flags=re.MULTILINE)
    sections: dict[str, str] = {}
    for part in parts:
        if not part.strip():
            continue
        first = part.strip().splitlines()[0]
        if first == "## Production":
            sections["Production"] = part
            continue
        m = re.match(r"^## ([AB]) Line$", first)
        if m:
            sections[m.group(1)] = part
    first_part = parts[0].strip().splitlines()[0] if parts and parts[0].strip() else ""
    prefix = "" if re.match(r"^## (?:Production|[AB] Line)$", first_part) else parts[0]
    return {"__prefix__": prefix, **sections}


def parse_fields(section: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in section.splitlines():
        m = re.match(r"^- ([^:]+): (.*)$", line.strip())
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    return fields


def render_section(line: str, fields: dict[str, str]) -> str:
    heading = "## Production" if line == "Production" else f"## {line} Line"
    lines = [heading, ""]
    for key in FIELD_ORDER:
        if key in fields:
            lines.append(f"- {key}: {fields[key]}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="更新 {id}.position.md 中的当前位置。")
    parser.add_argument("--id", required=True, help="选题 ID（与 daily_radar_run.py 的 source_id 一致）。")
    parser.add_argument("--line", default="Production", choices=["Production", "A", "B"])
    parser.add_argument("--enabled", choices=["YES", "NO"], help="仅在需要切换生产区块开关时传入。")
    parser.add_argument("--stage", help="Stage 取值需与 STAGE_DEFINITION_V1.md 一致，如 Review。")
    parser.add_argument("--state", help="State 取值需与 STATE_DEFINITION_V1.md 一致，如 Reviewing。")
    parser.add_argument("--deliverable", help="当前交付物路径。")
    parser.add_argument("--actor", help="当前 Stage 的 Primary Owner（见 ACTOR_DEFINITION_V1.md）。")
    parser.add_argument("--next-action", dest="next_action", help="下一步动作。")
    parser.add_argument("--on-failure", dest="on_failure", help="失败/REJECT/REVISION 时回到哪里。")
    parser.add_argument("--updated-by", dest="updated_by", required=True, help="谁执行了这次更新（Actor 名）。")
    parser.add_argument(
        "--force",
        action="store_true",
        help="跳过 Stage 迁移合法性校验（仅用于修正历史记录，不用于正常生产流程）。",
    )
    args = parser.parse_args()

    path = position_path(args.id)
    if not path.exists():
        raise SystemExit(
            f"未找到位置台账：{path}\n"
            "位置台账必须由 daily_radar_run.py 在 Transform 阶段先创建初始版本，"
            "update_position.py 只负责更新，不负责创建。"
        )

    text = path.read_text(encoding="utf-8")
    sections = parse_sections(text)
    if args.line not in sections:
        heading = "## Production" if args.line == "Production" else f"## {args.line} Line"
        raise SystemExit(f"{path} 中没有找到 '{heading}' 区块。")

    fields = parse_fields(sections[args.line])

    if args.stage and not args.force:
        current_stage = fields.get("Current Stage")
        if current_stage is None:
            raise SystemExit(
                f"{args.line} Line 当前没有 Current Stage 字段（可能已 Enabled: NO），"
                "无法判断迁移是否合法。如确认要强制写入，加 --force。"
            )
        allowed = LEGAL_NEXT_STAGE.get(current_stage)
        if allowed is None:
            raise SystemExit(f"未知的 Current Stage：{current_stage}，无法校验迁移合法性。")
        if args.stage not in allowed:
            raise SystemExit(
                f"非法迁移：{args.line} Line 当前 Stage 是 {current_stage}，"
                f"不能直接跳到 {args.stage}。\n"
                f"{current_stage} 允许迁移到：{sorted(allowed)}。\n"
                "如确认这是历史修正而非正常生产流程，加 --force 跳过校验。"
            )

    if args.enabled:
        fields["Enabled"] = args.enabled
        if args.enabled == "NO":
            # 关闭该生产线时只保留 Enabled 字段，避免残留一个不再更新的假状态。
            fields = {"Enabled": "NO"}

    if fields.get("Enabled") != "NO":
        if args.stage:
            fields["Current Stage"] = args.stage
        if args.state:
            fields["Current State"] = args.state
        if args.deliverable:
            fields["Current Deliverable"] = args.deliverable
        if args.actor:
            fields["Current Actor"] = args.actor
        if args.next_action:
            fields["Next Action"] = args.next_action
        if args.on_failure:
            fields["On Failure"] = args.on_failure
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fields["Last Updated"] = f"{now} by {args.updated_by}"

    prefix = sections.get("__prefix__", "")
    sections[args.line] = render_section(args.line, fields)

    if "Production" in sections:
        new_text = prefix.rstrip() + "\n\n" + sections["Production"].rstrip() + "\n"
    else:
        ordered = []
        for line in ("A", "B"):
            if line in sections:
                ordered.append(sections[line].rstrip())
        new_text = prefix.rstrip() + "\n\n" + "\n\n".join(ordered) + "\n"

    path.write_text(new_text, encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
