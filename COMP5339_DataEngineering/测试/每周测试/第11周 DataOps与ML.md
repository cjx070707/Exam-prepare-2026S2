# 第11周测试 — DataOps、数据架构与 ML

---

## 选择题

**1.** Lambda Architecture 和 Kappa Architecture 的核心区别是？

- A. Lambda 只用流处理，Kappa 用批处理和流处理双通道
- B. Lambda 用批处理（冷路径）+ 流处理（热路径）双通道；Kappa 统一用流处理单通道
- C. Kappa 性能更差，只适合小规模数据
- D. 两者没有本质区别，叫法不同而已

<details><summary>答案</summary>

**答案：B**

解析：**Lambda Architecture**（Nathan Marz 提出）：双通道——**Batch Layer（冷路径）** 处理全量历史数据（准确但高延迟）+ **Speed Layer（热路径）** 实时处理最新数据（低延迟但近似）+ **Serving Layer** 合并两路结果。**Kappa Architecture**（Jay Krebs 提出）：单通道，全部走流处理，通过重放历史数据来处理批量需求。Kappa 更简单，Lambda 更灵活（适合批流需求差异大的场景）。

</details>

---

**2.** DataOps 是什么？它与 DevOps 的关系是？

- A. DataOps 是 DevOps 的另一个名称，完全相同
- B. DataOps 是借鉴 DevOps 理念（自动化、持续集成）应用于数据管理的实践，专注于数据管道的质量、协作和自动化
- C. DataOps 只适用于机器学习项目，不适用于传统数据仓库
- D. DataOps 取代了 DevOps，是更先进的开发方法

<details><summary>答案</summary>

**答案：B**

解析：**DataOps** 将 DevOps 的核心理念（CI/CD、自动化测试、协作、持续监控）应用于数据工程领域，目标是：加速数据交付、保证数据质量、打通数据生产者（工程师）和消费者（分析师/数据科学家）之间的协作壁垒。关键实践：Pipeline Orchestration、Data Quality Monitoring、Data Governance、Self-Service Access。

</details>

---

**3.** Data Observability（数据可观测性）的五个支柱是？

- A. Freshness、Distribution、Volume、Schema、Lineage
- B. Accuracy、Completeness、Consistency、Timeliness、Uniqueness
- C. Ingestion、Storage、Transformation、Serving、Monitoring
- D. CI、CD、Testing、Deployment、Rollback

<details><summary>答案</summary>

**答案：A**

解析：Data Observability 五支柱：
- **Freshness（时效性）**：数据是否及时更新
- **Distribution（分布）**：数据值是否在预期范围内
- **Volume（数量）**：数据量是否正常（缺失或异常增多）
- **Schema（结构）**：数据结构是否发生变化（新增/删除字段）
- **Lineage（血缘）**：数据在系统中如何流转和变换的完整链路

</details>

---

**4.** Feature Store 中，"Training-Serving Skew"（训练-服务偏差）是指什么问题？

- A. 训练数据量太小，模型欠拟合
- B. 训练时和推理（serving）时使用的 feature 计算逻辑不一致，导致模型在生产中表现下降
- C. 模型训练速度和推理速度差距过大
- D. 训练数据和测试数据来自不同分布

<details><summary>答案</summary>

**答案：B**

解析：Training-Serving Skew 是 ML 生产部署中常见的隐蔽问题：训练时 feature 用 Python/Pandas 计算，推理时用 Java/SQL 重新实现，两者逻辑细节不同（如时间窗口定义、NULL 处理方式），导致模型收到的实际 feature 与训练时不同，性能下降。**Feature Store** 通过统一 feature 定义和服务，从根本上消除这个问题。

</details>

---

**5.** Feature Store 中，Online Storage 和 Offline Storage 的区别是？

- A. Online 用于历史训练；Offline 用于实时推理
- B. Online 优化低延迟实时推理（如 Redis/DynamoDB）；Offline 存储大量历史数据用于模型训练（如 S3/BigQuery）
- C. 两者存储完全相同的数据，只是地理位置不同
- D. Online Storage 只支持 SQL 查询

<details><summary>答案</summary>

**答案：B**

解析：**Online Storage（在线存储）**：Key-Value 存储（如 Redis、DynamoDB），面向低延迟（毫秒级）实时推理，存储最新 feature 值。**Offline Storage（离线存储）**：数据湖/仓库（如 S3、BigQuery、Snowflake），存储历史 feature 数据，用于模型训练和回测（Point-in-time accuracy：可以查询"历史上某时刻的 feature 值是什么"）。

</details>

---

**6.** 现代数据栈（Modern Data Stack）中，dbt 的主要职责是？

- A. 数据摄取（从数据源拉取原始数据）
- B. 数据仓库存储（替代 Snowflake/BigQuery）
- C. 数据转换（在数据仓库内做 SQL 转换，管理模型依赖）
- D. 数据可视化（生成报表和 Dashboard）

<details><summary>答案</summary>

**答案：C**

解析：现代数据栈（Modern Data Stack）的典型工具链：**Fivetran/Airbyte**（数据摄取 Ingestion）→ **Snowflake/BigQuery**（云数据仓库 Storage）→ **dbt**（数据转换 Transformation，在仓库内用 SQL 定义 data models，管理依赖和测试）→ **Tableau/Power BI**（可视化）。dbt 让 SQL 转换也能像代码一样版本控制和测试。

</details>

---

**7.** CI/CD 在 ML 工程中的意义是？

- A. CI/CD 只用于软件开发，与 ML 无关
- B. CI（持续集成）自动测试新代码/模型；CD（持续部署）自动将通过测试的模型部署到生产环境，实现频繁安全的模型更新
- C. CI/CD 是一种数据存储技术
- D. CI/CD 只适用于大型企业，小团队不需要

<details><summary>答案</summary>

**答案：B**

解析：ML 场景下的 CI/CD：**CI（Continuous Integration）**：每次数据更新或代码变更时，自动重新训练模型并运行评估测试（验证精度没有下降）。**CD（Continuous Deployment）**：测试通过后，自动将新模型部署到 Serving 服务。意义：ML 模型需要频繁更新（应对数据 drift、业务变化），CI/CD 让这一过程安全、可靠、自动化。

</details>

---

**8.** MADlib 的核心设计思路是？它解决了什么问题？

- A. 将数据导出到外部 Python 环境做 ML，避免数据库成为瓶颈
- B. 在数据库（PostgreSQL）内部直接执行 ML 算法（ML to Data），数据不需要移出数据库
- C. 将 ML 模型的预测结果存储回数据库
- D. 用 GPU 加速 PostgreSQL 内的查询

<details><summary>答案</summary>

**答案：B**

解析：传统方法：将数据从数据库导出到 Python/R → 在外部做 ML → 结果导回。问题：数据传输开销大，数据量超出内存时困难。**MADlib** 的思路：**将计算带到数据（ML to Data）**，直接在 PostgreSQL 内运行 ML 函数（通过 C++ UDF），数据不离开数据库，支持描述统计、分类、回归、聚类、时序预测（ARIMA）等，在大数据场景下避免了传输开销。

</details>

---

## 简答题

**9.** 解释 Lambda Architecture 的三层结构（Batch Layer、Speed Layer、Serving Layer），以及它的主要缺点。

<details><summary>答案</summary>

**三层结构**：
- **Batch Layer（冷路径）**：接收所有数据，定期（如每小时/每天）对全量历史数据做精确批处理，结果准确但有延迟（Batch Views）
- **Speed Layer（热路径）**：实时处理最新到达的数据，结果低延迟但可能是近似值（Realtime Views）；当 Batch Layer 结果到来后被覆盖
- **Serving Layer**：合并 Batch Views 和 Realtime Views 响应查询

**主要缺点**：
1. **代码重复**：同一业务逻辑需要在 Batch（MapReduce/Spark）和 Speed（Flink/Spark Streaming）两套系统中分别实现，维护成本高
2. **一致性风险**：两套实现细节可能出现不一致
3. **系统复杂度高**：需要维护和运维两套独立的数据处理系统

Kappa Architecture 通过统一用流处理解决了这个问题（代价：大规模历史重算成本较高）。

</details>

---

**10.** 你的公司有以下两个 ML 需求：
- **系统A**：每天批量预测次日商品需求量（基于过去90天历史数据）
- **系统B**：用户浏览商品时实时推荐（需要 50ms 内返回）

说明两个系统在 Feature Store 中应分别使用哪种 Storage 和哪种 Feature Transform，并解释共用同一个 Feature Store 的好处。

<details><summary>答案</summary>

**系统A（批量预测）**：
- Storage：**Offline Storage**（如 BigQuery/S3），存储90天历史 feature 数据，支持大批量读取
- Transform：**Batch Transform**（提前计算好历史特征，如"过去90天每个商品的平均销量"）

**系统B（实时推荐）**：
- Storage：**Online Storage**（如 Redis），低延迟键值查询，50ms 内必须返回
- Transform：**Streaming Transform**（实时计算，如"用户过去10分钟的点击类目"）或 **On-Demand Transform**（推理时动态计算，如"当前时间是否是促销时段"）

**共用 Feature Store 的好处**：
1. **消除 Training-Serving Skew**：System B 的 online serving 使用的 feature 与训练时完全一致（同一 feature 定义）
2. **Feature 复用**：系统A和B可共享基础 feature（如商品历史销量），避免重复开发
3. **统一版本管理**：feature 变更有版本记录，方便回溯和审计
4. **统一监控**：一个地方监控所有 feature 的质量和 drift

</details>

---

**11.** 对比 Kappa Architecture 和 Lambda Architecture，在以下金融风控场景中哪个更合适？

**场景**：需要①实时检测可疑交易（毫秒级）；②每月重新训练风控模型（需回溯5年历史数据做批量特征计算）。

<details><summary>答案</summary>

**Lambda Architecture 更合适**。

原因：

| 需求 | Lambda 处理方式 | 适合性 |
|------|----------------|--------|
| 实时检测（毫秒级） | Speed Layer（流处理）实时处理交易流 | ✅ 低延迟满足 |
| 月度模型重训（5年历史） | Batch Layer（Spark/MapReduce）批量处理5年数据 | ✅ 批处理更适合大规模历史数据 |

若用 **Kappa**：需要将5年历史数据从消息队列重放（Replay），这在时间和存储成本上极其昂贵；且流处理对超大规模历史数据的吞吐和效率不如专用批处理（Spark）。

**另外**：金融场景对准确性要求极高，Lambda 的 Batch Layer 可以定期"修正"流处理的近似结果，确保最终一致性。

</details>
