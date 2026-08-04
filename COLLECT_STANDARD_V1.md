# Collect Standard V1

## Collection Boundary

V1 defines what the system should not collect first.

The purpose is to build a stable production system by excluding high-risk, high-timeliness, and high-dispute content.

## Black List

### 金融投资

Exclude:

- 股票
- 基金
- 期货
- 外汇
- 数字货币
- 个股分析
- 荐股
- 投资策略

Reason:

- 合规风险高
- 时效极短
- 容易涉及投资建议
- 生命周期短，不适合作为稳定内容资产

### 政治时政

Exclude:

- 国际政治
- 国内政治评论
- 意识形态争议
- 外交事件评论
- 领导人评论

Reason:

- 平台审核严格
- 争议性高
- 收益和风险不成比例

### 法律判案解读

Exclude:

- 案件评论
- 法律分析
- 量刑预测
- 司法评价

Reason:

- 容易涉及专业判断
- 容易产生事实争议

### 医疗诊断

Exclude:

- 治疗建议
- 药品推荐
- 疾病诊断
- 偏方

Keep:

- 健康科普
- 生活方式
- 新闻事件

### 灾难事故

Exclude in V1:

- 空难
- 重大交通事故
- 死亡事故
- 自然灾害现场

Reason:

- 情绪波动大
- 审核尺度变化快
- 不利于建立稳定系统

### 色情、赌博、毒品、违法

Exclude permanently.

## White List

Prioritize:

- 今日爆点 S+ 爆点池
- 官方扶持中素材质量可用的内容
- 今日爆点 S 级内容
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

## Collection Priority

Collect in this order:

1. 今日爆点 S+ 爆点池
2. 官方扶持中明确标记为“素材质量可用”的内容
3. 今日爆点 S 级内容

Do not collect other sections in V1.

## Collection Intake

When source material is entered into the system, include:

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

## Source Full Content Standard

The system must save the complete source content used for transformation.

If the detail page contains separate areas for Radar Full Text and Generated Article or Copyable Article, both must be saved.

The system cannot save only radar analysis, task sheets, or list summaries.

## V1 Principle

V1 does not mean excluded categories can never be used.

V1 excludes high-risk, high-timeliness, and high-dispute content first to establish a stable production system.

After the system becomes stable, the collection scope can be expanded gradually.
