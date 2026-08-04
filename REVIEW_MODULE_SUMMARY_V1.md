# Review Module Summary V1

## Module

Review

## Version

V1

## Status

FROZEN

## Purpose

确认头条文案是否保持了老师文案的传播能力，并符合今日头条发布标准。

Review decides whether the article can enter the publishing flow.

## Primary Owner

GPT

## Supporting Actor

User

## Input

头条文案 V1

## Output

Review Decision

## Deliverable

Review Decision

## State

```text
Ready for Review
↓
Reviewing
↓
Review Completed
```

## Responsibility

Review is responsible for:

- 检查
- 判断
- 输出审核结论

Review is not responsible for:

- 修改正文
- 优化正文
- 发布正文

## Boundary

Review allows:

- 发现问题
- 指出问题
- 决定处理方式

Review forbids:

- 直接修改正文
- 重新生成正文
- 直接发布

## Decision

- PASS
- REVISION
- REJECT

## Decision Point

```text
Review
    ├── PASS
    │   ↓
    │   Publish
    │
    ├── REVISION
    │   ↓
    │   Revision
    │   ↓
    │   Review
    │
    └── REJECT
        ↓
        End
```

## Standard

Review checks:

- 标题
- 结构
- 核心意思
- 传播能力

## Dependencies

- Collect Module
- Transform Module
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
- REVIEW_STANDARD_V1.md
