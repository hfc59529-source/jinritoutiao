# Collect Module Summary V1

## Module

Collect

## Version

V1

## Status

FROZEN

## Purpose

Bring valid source material into the Today Toutiao system.

## Primary Owner

Codex

## Supporting Actor

User

## Input

Teacher website source material from the V1 collection scope.

## Output

老师原文

## State

```text
Collected
↓
Ready for Transform
```

## Boundary

Collect defines what can enter the system.

Collect uses two internal actions, not new stages:

- List Scan + Pre-Filter：Acquisition Decision（是否值得抓详情）
- Detail Fetch：抓取并保存完整雷达详情

Pre-Filter only uses cheap list-page information and must not output P1 / P2 / P3. Formal publication priority belongs to Selection V2 after Detail Fetch.

## Collection Priority

1. 今日爆点 S+ 爆点池
2. 今日爆点 S 级内容

V1 does not collect other sections. The teacher site no longer provides 官方扶持 as a production source.

## Collection Intake

- Source ID（来源唯一编号）
- Source Section（来源板块）
- Source URL（来源链接）
- Collected At（采集时间）
- Title（标题）
- Level（级别）
- Collection Reason（采集理由）
- Radar Full Text（文案雷达全文）
- Source Article Full Text（来源成品文案全文）
- Source Article Status（来源成品文案状态）

Source Article Status:

- AVAILABLE
- MISSING

MISSING source material cannot enter Ready for Transform.

## Collection Boundary

Black List:

- 金融投资
- 政治时政
- 法律判案解读
- 医疗诊断
- 灾难事故
- 色情、赌博、毒品、违法

White List:

- 职场
- 创业
- 商业
- 教育
- 家庭
- 婚姻
- 亲子
- 消费
- 社会现象
- 普通人故事
- 企业管理
- 餐饮
- 美业
- 母婴

## Dependencies

- System Goal
- Architecture
- Workflow
- Stage
- Deliverable
- State
- Actor
- Governance Principles

## Files

- ARCHITECTURE_V1.md
- STAGE_DEFINITION_V1.md
- DELIVERABLE_DEFINITION_V1.md
- STATE_DEFINITION_V1.md
- ACTOR_DEFINITION_V1.md
- GOVERNANCE_PRINCIPLES_V1.md
- COLLECT_STANDARD_V1.md
