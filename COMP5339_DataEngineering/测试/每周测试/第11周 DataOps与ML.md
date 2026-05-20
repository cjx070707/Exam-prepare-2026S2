# 第11周测试 — DataOps、数据架构与 ML

---

## 一、选择题

**1.** Lambda Architecture 和 Kappa Architecture 的核心区别是？

- A. Lambda 只用流处理，Kappa 用批处理和流处理双通道
- B. Lambda 用批处理（冷路径）+ 流处理（热路径）双通道，Kappa 统一用流处理
- C. Kappa 性能更差，只适合小规模数据
- D. 两者没有本质区别

**2.** DataOps 可观测性五支柱中，"Lineage" 指的是？

- A. 数据是否及时更新
- B. 数据量是否正常
- C. 数据如何在系统中流转和变换的完整链路
- D. 数据结构是否发生变化

**3.** Feature Store 中，Online Storage 和 Offline Storage 的区别是？

- A. Online 用于历史训练，Offline 用于实时推理
- B. Online 用于低延迟实时推理，Offline 用于历史数据训练
- C. 两者存储相同的数据，只是位置不同
- D. Online Storage 只支持 SQL 查询

**4.** MADlib 的核心思路是？

- A. 将数据导出到外部 ML 平台训练
- B. 在 PostgreSQL 内部直接运行 ML 算法，数据不需要移动
- C. 将 ML 模型嵌入到 Feature Store
- D. 使用 GPU 加速 ML 训练

**5.** "Training-Serving Skew" 是指什么问题？

- A. 训练数据量太小
- B. 训练时和推理时使用的 feature 计算逻辑不一致，导致模型表现下降
- C. 模型训练速度和推理速度差距过大
- D. 训练数据和测试数据分布不同

---

## 二、简答题

**6.** 解释 Lambda Architecture 的三层结构（Batch Layer、Speed Layer、Serving Layer），以及它的主要缺点是什么。

**7.** DataOps 的四大核心职能是什么？Apache Airflow 在其中承担什么角色？

**8.** 解释 Feature Store 的三种 Feature Transform 类型（Batch、Streaming、On-Demand），各举一个例子。

---

## 三、应用题

**9.** 你的公司有以下两个 ML 需求：
- 系统A：每天批量预测第二天的商品需求量（基于过去 90 天的销售历史）
- 系统B：用户浏览商品时实时推荐（需要在 50ms 内返回结果）

请分别说明：
1. 系统A 和 系统B 应该使用 Feature Store 的哪种 Storage？
2. Feature Transform 应该用哪种类型？
3. 两个系统共用同一个 Feature Store 的好处是什么？

**10.** 对比 Kappa Architecture 和 Lambda Architecture，在以下场景中哪个更合适？说明理由。

场景：一个金融风控系统，需要：
- 实时检测可疑交易（毫秒级响应）
- 每月重新训练风控模型（需要回溯 5 年历史数据）

---

## 参考答案

1. **B**
2. **C**
3. **B**
4. **B**
5. **B**
6. **Lambda Architecture 三层**：
   - **Batch Layer（冷路径）**：定期（如每小时）处理全量历史数据，给出准确结果
   - **Speed Layer（热路径）**：实时处理最新数据，给出低延迟的近似结果
   - **Serving Layer**：合并批处理和流处理的结果，响应查询
   
   **主要缺点**：需要维护两套独立的处理逻辑（批和流），代码重复，维护成本高；两套逻辑容易产生不一致。
7. **四大核心职能**：
   - **Pipeline Orchestration**：自动协调 ETL 流程，管理依赖关系
   - **Data Quality Monitoring**：实时检测数据准确性和一致性
   - **Governance & Security**：合规（GDPR/CCPA）和访问控制
   - **Self-Service Data Access**：让业务用户自助访问数据
   
   **Airflow 的角色**：Pipeline Orchestration 工具，以 DAG 定义任务依赖，自动调度和重试 ETL 任务。
8.
   | 类型 | 含义 | 例子 |
   |------|------|------|
   | Batch Transform | 从历史数据仓库批量计算 feature | 用户过去 30 天的购买总金额 |
   | Streaming Transform | 实时从数据流中计算 feature | 用户过去 10 分钟的点击次数 |
   | On-Demand Transform | 推理时实时计算，无法提前预计算 | 当前用户所在城市的实时天气 |
9.
   1. 系统A（批量预测）→ **Offline Storage**（如 BigQuery/S3，存历史数据）；系统B（实时推荐）→ **Online Storage**（如 Redis，低延迟）
   2. 系统A → **Batch Transform**；系统B → **Streaming Transform** 或 **On-Demand Transform**
   3. 共用 Feature Store 的好处：保证训练和推理时使用完全相同的 feature 计算逻辑，消除 Training-Serving Skew；feature 可复用，避免重复开发；统一版本管理和监控。
10. **Lambda Architecture 更合适**。理由：
    - 实时风控（毫秒级）→ Speed Layer 处理，满足低延迟需求
    - 月度模型重训（5年历史）→ Batch Layer 处理，批处理更适合大规模历史数据的精确计算
    - 金融场景对准确性要求高，Lambda 的双路设计允许批处理结果修正流处理的近似误差
    - 若用 Kappa，5年历史数据重放成本极高，且流处理对超大规模批量历史数据不如 MapReduce/Spark 高效
