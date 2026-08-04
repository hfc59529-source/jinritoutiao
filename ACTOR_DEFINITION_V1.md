# Actor Definition V1

## Actor Responsibility Boundary

| Actor | Core Responsibility | Not Responsible For |
| --- | --- | --- |
| Codex | System | 不写正文、不审核 |
| Claude | Production | 不做最终审核、不维护系统 |
| GPT | Quality | 不写最终正文、不维护数据库 |
| User | Decision | 不做重复性工作 |

## Primary Owner

Each Stage has one Primary Owner.

Other Actors may assist, but they cannot replace the Primary Owner.

| Stage | Primary Owner |
| --- | --- |
| Collect | Codex |
| Transform | Claude |
| Review | GPT |
| Revision | Claude |
| Publish | User |
| Feedback | Codex |

## Stage 1: Collect

### Actor: Codex

Responsible for:

- 自动采集老师网站文案
- 保存完整原文
- 保存来源
- 检查完整性
- 更新 State

### Actor: User

Responsible for:

- 制定采集标准

## Stage 2: Transform

### Actor: Claude

Responsible for:

- 文案转换
- 平台适配
- 保持标题、结构、核心意思、情绪推进不变

Assist:

- None

## Stage 3: Review

### Actor: gpt

Responsible for:

- 审核转换结果
- 输出 Review Decision

### Actor: User

Responsible for:

- 最终发布决定确认

## Stage 4: Revision

### Actor: Claude

Responsible for:

- 根据审核意见修改
- 保存最终发布稿
- 更新 State
- 输出最终可复制版本

## Stage 5: Publish

### Actor: User

Responsible for:

- 手动发布今日头条

### Actor: Claude

Responsible for:

- 不参与实际发布

### Actor: Codex

Responsible for:

- 不参与发布

## Stage 6: Feedback

### Actor: Codex

Responsible for:

- 自动采集文章表现
- 保存阅读量
- 保存点赞
- 保存评论
- 保存收益
- 更新 State
- 建立历史记录
- 维护数据库

### Actor: gpt

Responsible for:

- 读取 Feedback 数据
- 分析表现
- 优化下一轮 Transform 策略

### Actor: User

Responsible for:

- 提供必要权限
- 处理异常情况
