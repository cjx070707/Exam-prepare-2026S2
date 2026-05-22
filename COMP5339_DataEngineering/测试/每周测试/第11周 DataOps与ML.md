# 第11周测试 — DataOps & ML Systems

---

**Question 1.** A streaming analytics company processes 10TB of event data daily. Their data science team complains that monthly model retraining (requiring a full 90-day historical replay) takes 3 days when run through the streaming pipeline. A senior engineer proposes switching from **Lambda Architecture** to **Kappa Architecture** to simplify the codebase. A tech lead objects. Who is correct?

- [ ] A. The senior engineer is correct — Kappa is always simpler and should replace Lambda in all cases
- [x] B. The tech lead is correct — when large-scale historical batch reprocessing is a core requirement, Lambda's dedicated Batch Layer is more cost-effective than replaying 90 days through a stream processor
- [ ] C. Lambda Architecture does not support real-time processing, so Kappa is the only viable option
- [ ] D. Both architectures are equivalent in this scenario — the choice only affects operational complexity, not performance

> [!note]- Answer
> **B. Lambda vs Kappa Architecture 的选型权衡。**
>
> - **Kappa Architecture**：统一用流处理，通过从 Kafka **重放（Replay）**历史数据来处理批量需求。优点：单一代码路径，维护简单。缺点：大规模历史重放（90天 × 10TB/天 = 900TB）在流处理引擎中效率极低；Kafka 需存储90天数据，存储成本极高。
>
> - **Lambda Architecture**：**Batch Layer**（Spark / MapReduce）专门处理全量历史数据，效率极高；**Speed Layer**（流处理）处理实时数据；**Serving Layer** 合并两路结果。
>
> 当批量历史重处理是核心需求时，Lambda 的 Batch Layer 远比 Kappa 的流式重放高效。Kappa 适合历史重算需求轻量的场景。

---

**Question 2.** A data team's production dashboard shows customer churn metrics that haven't updated for 36 hours, even though the source database is actively receiving new records. The data observability monitoring system fires an alert. Which of the five Data Observability pillars is this alert detecting?

- [x] A. Freshness — the data has not been updated within the expected time window
- [ ] B. Volume — the number of records in the table has dropped unexpectedly
- [ ] C. Schema — a column has been added or removed from the source table
- [ ] D. Lineage — the upstream data source has changed its transformation logic

> [!note]- Answer
> **A. Data Observability — Freshness（时效性）异常。**
>
> 五个 Data Observability 支柱：
> - **Freshness（时效性）**：数据是否在预期时间窗口内更新 ← **本题触发的告警**
> - **Volume（数量）**：数据量是否在正常范围（缺失或异常增多）
> - **Distribution（分布）**：字段值是否在预期范围内（如 age 出现负数）
> - **Schema（结构）**：字段是否新增、删除或类型变更
> - **Lineage（血缘）**：数据在系统中的流转路径和变换链路
>
> 36小时未更新是典型的 **Freshness** 问题——pipeline 可能卡住、ETL job 失败、或上游数据源停止写入。解决思路：检查 pipeline orchestration（如 Airflow）中是否有 task 失败。

---

**Question 3.** A machine learning team trains a fraud detection model. The feature *"number of transactions by this user in the last 24 hours"* is computed in Python/Pandas during training (using UTC midnight as the 24-hour boundary). Six months later, the model is deployed and the same feature is recomputed in Java (using a rolling 86,400-second window from the current timestamp). Model performance drops 15% in production. What is the root cause?

- [ ] A. Model drift — the distribution of fraud patterns has changed over 6 months
- [ ] B. The Java implementation is less accurate than Python for floating-point computations
- [x] C. Training-Serving Skew — the feature computation logic differs between training (Python) and serving (Java), so the model receives different feature values in production than it was trained on
- [ ] D. The model was overfitted to training data and cannot generalise to production

> [!note]- Answer
> **C. Training-Serving Skew（训练-服务偏差）。**
>
> 这是 ML 生产部署中最隐蔽的问题之一：训练时 feature 用 Python 计算（以 UTC 午夜为24小时边界），推理时用 Java 重实现（以当前时间戳减86400秒为边界）——看似相同的 feature，实际数值在时间边界处可能相差数小时的交易量，导致模型收到的 feature 与训练分布不同，性能下降。
>
> **根本解决方案：Feature Store**
> - 统一 feature 定义（一份代码，一个计算逻辑）
> - 训练时从 **Offline Store** 读取 point-in-time 准确的历史 feature
> - 推理时从 **Online Store** 读取同一 feature 定义计算的最新值
> - 从根本上消除"两套实现导致的偏差"

---

**Question 4.** An e-commerce recommendation system needs a feature: *"total amount spent by this user in the last 7 days."* The feature is used in two contexts:
- **Training**: Offline batch job processes 2 years of historical orders
- **Serving**: Real-time recommendation API must return results within 30ms

Which Feature Store storage strategy is correct?

- [ ] A. Use Online Storage (Redis) for both — it's fast enough for training too
- [ ] B. Use Offline Storage (S3/BigQuery) for both — consistency is more important than latency
- [x] C. Offline Storage for training (historical batch reads, high throughput); Online Storage for serving (millisecond key-value lookup at inference time)
- [ ] D. No Feature Store needed — compute the feature on-the-fly with SQL at serving time

> [!note]- Answer
> **C. Feature Store: Offline vs Online Storage 的职责分工。**
>
> | | Offline Storage | Online Storage |
> |--|--|--|
> | **典型实现** | S3, BigQuery, Snowflake | Redis, DynamoDB, Cassandra |
> | **优化目标** | 高吞吐批量读取 | 低延迟键值查询（毫秒级） |
> | **用途** | 模型训练：扫描2年历史数据生成 training examples | 实时推理：30ms 内查出某 user 的最新 feature 值 |
>
> D 的方案（serving 时实时跑 SQL 计算7天聚合）对复杂特征延迟不可接受（SQL 查询通常 100ms+），且每次推理都重复计算，资源浪费。Feature Store 预计算并存储特征，serving 只需 key-value lookup。

---

> 📌 **新增题目**

**Question 5.** A healthcare analytics team has a 3TB patient records dataset stored in **PostgreSQL**. They need to train a **K-Nearest Neighbours (KNN) classifier** to predict readmission risk. A junior engineer proposes: *"Export the data to a Pandas DataFrame, then use scikit-learn's KNeighborsClassifier."* A senior engineer objects and recommends **Apache MADlib** instead. Who is correct and why?

- [ ] A. The junior engineer is correct — scikit-learn's KNN implementation is always faster than database-based ML
- [ ] B. Neither; the team should migrate to Apache Spark MLlib for scalable machine learning
- [ ] C. The senior engineer is correct — MADlib runs ML algorithms inside PostgreSQL using SQL (`SELECT * FROM madlib.knn(...)`), avoiding data export; it leverages the database's parallelism and keeps the 3TB dataset in-place, which Pandas cannot handle in memory
- [ ] D. The senior engineer is correct — MADlib should be used because it provides a Feature Store with Point-in-Time correctness, which scikit-learn lacks

> [!note]- Answer
> **C. MADlib — "Bring the Algorithm to the Data"。**
>
> - **A 错误**：scikit-learn 需要将数据加载进内存（RAM）；3TB 数据远超普通服务器内存，Pandas 会 OOM（Out of Memory）崩溃，根本无法运行。
> - **B 错误**：Spark MLlib 是可行方案，但需要搭建独立的 Spark 集群——这是重量级基础设施迁移，成本高。当数据已在 PostgreSQL 中时，MADlib 是更轻量的选择。
> - **C 正确**：MADlib 的核心思想是 **"Bring the Algorithm to the Data"**——ML 算法在数据库内部执行，数据不需要导出：
>   ```sql
>   SELECT * FROM madlib.knn(
>       'patients',        -- 训练集表名
>       'features',        -- 特征列
>       'label',           -- 标签列
>       'new_patients',    -- 预测集
>       'result_table',    -- 输出表
>       5                  -- K 值
>   );
>   ```
>   利用 PostgreSQL 的并行查询引擎处理 3TB 数据，无需数据移动。
> - **D 错误**：MADlib 是数据库内 ML 框架，不提供 Feature Store 或 Point-in-Time 功能，这是对 MADlib 的错误描述。

---

**Scenario 1:** A media streaming company runs the following data stack:
- Raw clickstream events → Kafka → **Flink** (real-time processing) → live dashboard
- Raw clickstream events → **Spark** batch job (runs nightly) → content recommendation model training

A new VP of Engineering wants to eliminate the Spark batch job and "just use Flink for everything."

**Question 6:** **(4 Marks)**

**(a)** What architecture does the current system represent, and what would the VP's proposed change result in? **(2 Marks)**

**(b)** The recommendation model requires retraining every week using 1 year of historical clickstream data. Evaluate whether the VP's proposal is technically sound. **(2 Marks)**

> [!note]- Answer
> **(a) 架构识别**
>
> 当前系统是 **Lambda Architecture**：
> - **Speed Layer**：Kafka → Flink（实时流处理，低延迟 live dashboard）
> - **Batch Layer**：Spark 批处理（全量历史数据，模型训练）
> - **Serving Layer**（隐含）：Dashboard + Recommendation Model
>
> VP 的提案是将系统改为 **Kappa Architecture**：单一 Flink 流处理通道，通过 Kafka 消息回放来处理历史数据需求，消除 Batch Layer。
>
> **(b) 技术评估**
>
> VP 的提案**存在重大风险**：
> - 1年历史 clickstream 数据量通常达 TB 级；用 Flink 流式回放处理1年数据的效率远低于 Spark 批处理——Spark 的 DAG 优化器和列式 Parquet 读取专为大规模历史数据设计。
> - Kafka 默认保留7天数据，保存1年数据需额外配置大容量存储（成本高）。
> - 流处理引擎对超大规模历史 backfill 的吞吐量和资源效率不如专用批处理。
>
> 结论：历史批量重训是核心需求时，保留 Lambda（Spark Batch Layer）比迁移到 Kappa 更合理。

---

**Scenario 2:** A bank is building an ML system to approve or reject loan applications in real time. Each decision must be fully auditable — regulators can ask: *"Why was this application rejected on 15 March 2024, based on the data available at that time?"*

**Question 7:** **(4 Marks)**

**(a)** Why does a standard Feature Store (without Point-in-Time correctness) fail to satisfy this regulatory audit requirement? **(2 Marks)**

**(b)** The bank's data team uses **dbt** in their transformation pipeline. Explain dbt's role in the Modern Data Stack and how it supports data quality in this regulated environment. **(2 Marks)**

> [!note]- Answer
> **(a) Point-in-Time Correctness（时间点准确性）的必要性**
>
> 假设 Feature Store 只存储每个申请人的**最新** feature 值（如"当前信用评分 = 780"）。审计人员在2025年查询"2024年3月15日该申请人的信用评分"——如果 Feature Store 已用新值覆盖旧值，系统无法重建历史时刻的特征，无法解释当时的决策依据。
>
> **Point-in-Time Correct Feature Store** 的解决方案：在 Offline Store 中保存每个 feature 值的完整历史（带时间戳），支持查询"某时间点该实体的 feature 值是什么"。同时防止**目标泄露（Label Leakage）**——避免训练时使用了决策时刻之后才产生的数据。
>
> **(b) dbt 在 Modern Data Stack 中的角色**
>
> **dbt（data build tool）** 的职责：在数据仓库（如 BigQuery / Snowflake）**内部**用 SQL 定义数据转换模型，管理模型间的依赖关系（DAG），并对转换结果进行自动化测试。
>
> 在受监管的金融环境中，dbt 提供：
> - **版本控制**：所有 SQL 转换通过 Git 管理，每次变更有记录，支持审计追溯
> - **数据测试**：内置测试（`not_null`、`unique`、`accepted_values`）在每次 pipeline 运行时自动验证数据质量，防止错误数据流入贷款决策模型
> - **Lineage（血缘）**：自动生成数据血缘图，审计人员可追溯"贷款决策 feature 来自哪些原始数据源，经过了哪些转换"
