# Reader Model V1（五按钮框架）

## 层级归属

本文件不是独立 Stage，是 [`templates/radar_selection_rules.md`](templates/radar_selection_rules.md) 中 Internal Ranking（R1 Public Relevance / R2 Stakes）的判定模型，同时供 Quality Review 做 Reader Promise 检查、供 Feedback/Validation 做假设验证使用。

Reader Model 不进入 Transform 生产层。Transform 仍然只执行 Original Radar Production Prompt，不接受本模型作为生成规则（见 `SYSTEM_RULES.md` Transform 章节）。

## 背景

头条评论区高赞内容不是在讨论事件本身，而是在用事件确认自己在系统里的位置——"这跟我的钱/工作/安全有关吗"。头条定位是"普通人的现实利益解释器"，不是新闻搬运，也不是知乎式机制解释。

## 五按钮

| 按钮 | 用户潜意识问题 | 对应内容 |
| --- | --- | --- |
| 钱 | 我会多花/少赚多少钱？ | 工资、物价、养老金、消费 |
| 工作 | 我的饭碗会不会变？ | AI、裁员、就业、35岁 |
| 规则 | 以前那套还管用吗？ | 政策、行业变化、平台规则 |
| 公平 | 凭什么他可以，我不行？ | 企业、员工、阶层、资源 |
| 家庭 | 这会不会落到我家？ | 教育、养老、孩子、婚姻 |

## 判定问题

事件本身不是判断依据，判断依据是：

```text
事件
  ↓
影响读者哪一类现实利益（钱/工作/规则/公平/家庭）
  ↓
改变了读者的什么规则/经验/位置判断
  ↓
读者为什么必须重新确认自己的位置
```

## 用途边界

- **Selection**：命中的按钮数量和清晰度，作为 R1 Public Relevance、R2 Stakes 的判断依据，替代凭感觉打高/中/低。
- **Quality Review**：检查成品是否真的完成了"读者利益关联"（Reader Promise 检查），而不只是叙述完整。
- **Feedback / Validation**：验证按钮命中与展现、CTR、互动之间是否存在可重复的相关性，避免退化成"我感觉这个有效"。
- **不进入 Transform**：核心冲突、普通人代入、情绪推进等具体写法仍然全部交给 Original Radar Production Prompt，Reader Model 不在生成阶段重新解释这些内容。

## 状态

v0.1，尚未固化为强制 Gate。12 篇分组实验（钱/工作/规则/社会利益冲突各 3 篇）用于验证哪个按钮真正带来阅读和互动，验证前不得直接工程化为评分公式。
