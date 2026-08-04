# Transform Standard V1

## Purpose

将老师网站已经验证的爆点文案，在保持传播能力的前提下，转换为符合今日头条平台的可发布文案。

Transform means conversion, not creation.

## Responsibility

Transform is responsible for:

- 平台适配
- 输出头条文案

Transform is not responsible for:

- 重新选题
- 修改标题方向
- 重写结构
- 审核
- 发布

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

## Primary Owner

Claude

## Assist

None

## Deliverable

头条文案

This is the first transformed draft, not the final publishable draft.

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

## Input

老师原文

Transform does not accept:

- AI 总结
- 半截文案
- 摘要
- 二次整理

## Output

头条文案 V1

Later changes belong to Revision, not Transform.

## Transform Target

Today Toutiao

## Transform Standard

Keep:

- 标题
- 结构
- 核心意思
- 情绪推进

Adapt:

- 平台表达
- 平台格式
- 平台排版
- 平台敏感词

Summary:

保持传播能力，只做平台适配。

## Zero Optimization Principle

Transform forbids active optimization.

Claude is not responsible for making the article better.

Claude is responsible for preserving the original distribution potential and completing platform adaptation.

Unless the system explicitly authorizes it, Claude must not actively:

- 优化
- 改写
- 增强
- 精简逻辑
- 增加观点
- 删除观点
- 调整结构

## Transform Action Model

Transform has only two actions:

- Preserve
- Adapt

Preserve means keeping:

- 标题
- 结构
- 意思
- 情绪推进

Adapt means adapting:

- 平台表达
- 平台格式
- 平台排版
- 敏感词

Transform is not Rewrite.

Transform equals Preserve plus Adapt.
