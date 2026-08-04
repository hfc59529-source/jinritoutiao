# Transform Module Summary V1

## Module

Transform

## Version

V1

## Status

FROZEN

## Purpose

将老师网站已经验证的爆点文案，在保持传播能力的前提下，转换为符合今日头条平台的可发布文案。

Transform means conversion, not creation.

## Primary Owner

Claude

## Supporting Actor

None

## Input

老师原文

## Output

头条文案 V1

## Deliverable

头条文案

## State

```text
Ready for Transform
↓
Transforming
↓
Generated
↓
Ready for Review
```

## Boundary

Transform allows:

- 平台表达
- 平台敏感词处理
- 段落格式
- 排版
- 标点
- 语气微调
- 篇幅控制

Transform forbids:

- 修改标题方向
- 修改核心冲突
- 修改结构顺序
- 修改核心意思
- 增加新观点
- 删除关键论证
- 改变情绪推进
- 重新创作

## Transform Target

Today Toutiao

## Standard

保持传播能力，只做平台适配。

## Zero Optimization Principle

Transform forbids active optimization.

Claude is not responsible for making the article better.

Claude is responsible for preserving the original distribution potential and completing platform adaptation.

## Action Model

```text
Transform = Preserve + Adapt
```

Transform is not Rewrite.

## Dependencies

- Collect Module
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
- TRANSFORM_STANDARD_V1.md
- SYSTEM_RULES.md（Production Modes 执行层规范，见 TRANSFORM_STANDARD_V1.md 的 Production Modes 一节）
