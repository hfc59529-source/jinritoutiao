# Review Standard V1

## Purpose

确认头条文案是否保持了老师文案的传播能力，并符合今日头条发布标准。

Review is not responsible for modifying the article.

Review decides whether the article can enter the publishing flow.

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

## Primary Owner

GPT

## Assist

User

The final publishing decision is confirmed by User.

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

## Review Decision

### PASS

Allows the article to enter Publish.

PASS means no Revision is required.

### REVISION

Returns the article to Claude for modification.

After modification, the article returns to Ready for Review.

### REJECT

Ends the current production.

## Review Standard

Review checks:

- 标题
- 结构
- 核心意思
- 传播能力

## Decision Point

Review is the first decision point in the production flow.

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
