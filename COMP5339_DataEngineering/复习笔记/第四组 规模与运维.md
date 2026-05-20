# Group 4 — 规模化与运维

**Week 9 (Stream Processing) + Week 10 (Scalable Engineering) + Week 11 (DataOps & ML)**

> 叙事链：单机批处理撑不住大数据量 → 分布式集群横向扩展 → 数据实时流入 → 流处理应对低延迟需求 → 生产环境的管道需要监控编排（DataOps）→ ML 消费数据需要 Feature Store

> 本文件是 W9-W11 的完整归档版，与 `Quiz2_Revision_W7-W11.md` 内容一致，可交叉参考

---

## Part 1 — 流数据处理（W9）

### DBMS vs DSMS

| 维度 | DBMS（传统数据库） | DSMS（流数据系统） |
|------|-------------------|-------------------|
| 数据形态 | Persistent relations | Transient streams |
| 数据大小 | 有界 | **无界** |
| 更新方式 | Insert / Update / Delete | Append only |
| 查询类型 | 一次性 | **持续查询** |
| 查询答案 | 精确 | 可能近似 |

### Pub/Sub 模式

- **Publisher** 把消息发到 **Broker** 的 **Topic**
- **Subscriber** 订阅 Topic，Broker 推送消息
- 同一消息可被多个独立 Subscriber 同时消费，互不干扰

### MQTT vs Kafka

| 维度 | MQTT | Apache Kafka |
|------|------|--------------|
| **定位** | 轻量级，IoT/传感器 | 大规模分布式流数据 |
| **消息存储** | 默认不持久化（retain 只存最后一条） | **持久化到磁盘**，可回放 |
| **QoS 级别** | 0 / 1 / 2 | At least once |
| **默认 QoS** | QoS 0（at most once） | — |
| **扩展性** | 有限 | 高（Partition + Replication） |

**MQTT 关键细节**：
- Topic 区分大小写（`Temp ≠ temp`）
- 通配符：`+`（单级），`#`（多级，只能用于末尾）
- QoS 0 = at most once；QoS 1 = at least once；QoS 2 = exactly once

**Kafka 关键细节**：
- 每个 Topic 分为多个 **Partition**，每个 Partition 是有序 append-only 日志
- 不同 **Consumer Group** 独立消费同一 Topic（各自维护 offset）
- Replication Factor N → 最多容忍 N-1 台服务器故障
- 语义：**At least once**（消息不丢，但可能重复消费）

### 流查询：Stateless vs Stateful

| 类型 | 含义 | 例子 |
|------|------|------|
| **Stateless** | 每条记录独立处理，无需记忆历史 | 过滤（WHERE）、投影（SELECT） |
| **Stateful** | 需要跨多条记录维护状态 | 聚合、Join、窗口操作 |

### 窗口类型

| 窗口 | 含义 | 例子 |
|------|------|------|
| **Agglomerative** | 从起点累积到当前时刻 | 今日总点赞数 |
| **Sliding** | 固定大小，可重叠滑动 | 最近 5 分钟点赞数，每 30 秒更新 |
| **Tumbling** | 固定大小，**不重叠** | 每 1 分钟统计一次 |
| **Session** | 由数据中的事件标记定义 | auction_start 到 auction_end 之间的所有竞价 |

### 三种时间概念

| 时间 | 含义 | 特点 |
|------|------|------|
| **Event Time** | 事件在现实中发生的时间 | 最准确，但事件可能乱序到达 |
| **Ingestion Time** | 数据进入消息系统的时间 | 中间层 |
| **Processing Time** | 流处理引擎处理该条记录的时间 | 最容易获取，不反映真实顺序 |

**Watermark**：流处理器声明"截止时间 T，所有早于 T 的事件已到达"，用于触发基于 Event Time 的窗口。晚于 watermark 的事件视为"late data"，可丢弃或走 side output。

### Spark Streaming vs Flink

| 维度 | Apache Spark Streaming | Apache Flink |
|------|------------------------|--------------|
| **处理原理** | **Micro-batching**（流切成小批次） | **Pipelining**（真正的流，算子间立即传递） |
| **数据抽象** | RDD / DStream | DataSet / DataStream |
| **处理阶段** | 分离的 Stages | 重叠（低延迟） |
| **流处理延迟** | 毫秒~秒级 | 毫秒级（更低） |
| **批处理** | RDD | DataSet |
| **优化器** | SparkSQL + Adaptive Exec | 内置于 API |

> **Kafka/MQTT = 消息存储系统；Spark/Flink = 计算引擎**，两者角色不同

---

## Part 2 — 可扩展数据工程（W10）

### Scale-Up vs Scale-Out

| | Scale-Up（纵向） | Scale-Out（横向） |
|-|-----------------|------------------|
| 方式 | 换更强的单机硬件 | 增加更多节点 |
| 上限 | 有硬件天花板 | 理论上无限 |
| 架构 | 单机 | **Shared-nothing**（各节点独立） |
| 现状 | 受限 | 主流大数据方案 |

### Column Store vs Row Store

| | Row Store | Column Store |
|-|-----------|--------------|
| **数据组织** | 按行存储 | 按列存储 |
| **适合查询** | OLTP（点查询、更新） | OLAP（聚合、大范围扫描） |
| **压缩率** | 一般 | 更高（同类型数据，可用 run-length / dictionary encoding） |
| **并行处理** | 一般 | 更好（不同列可在不同磁盘并行读） |
| **代表系统** | PostgreSQL, MySQL | BigQuery, Apache Parquet |

**Wide Column Store**（如 HBase, BigTable）≠ Column Store：按 column family 分组，按行存储每个 family，适合稀疏大数据，通过多维 key（row + family + column）访问数据。

### 数据分区（Sharding）

| 策略 | 方式 | 适用 |
|------|------|------|
| **Horizontal Partitioning** | 按行切分，每个分区是一组行 | 大表扩展，并行查询 |
| **Vertical Partitioning** | 按列切分 | 分离冷热列 |
| **Round-robin** | 轮询分配到各节点 | 均匀分布 |
| **Hash Partitioning** | 对 key 哈希决定节点 | 点查询快 |
| **Range Partitioning** | 按值范围划分节点 | 范围查询快 |

**分区优势**：更小的数据集查询更快，支持 Inter-Query Parallelism（不同查询在不同分区并行）和 Intra-Query Parallelism（同一查询访问多个分区并行）

### 数据复制（Replication）

**目的**：高可用性（一个节点宕机仍可读），同时提升读性能

| | 同步（Eager） | 异步（Lazy） |
|-|---------------|-------------|
| **一致性** | 强 | 弱（可能读到旧数据） |
| **性能** | 差（需等所有副本确认） | 好 |
| **实践** | 少用 | **大多数系统默认** |

| | Primary Copy（单 Leader） | Multi-Leader |
|-|--------------------------|--------------|
| **写入** | 只能写 Primary | 可写任意 Leader |
| **冲突** | 无 | 需要冲突解决机制 |
| **实践** | **更常用**（如 MongoDB） | 分布式写场景 |

**最佳实践**：Lazy Propagation + Primary Copy（性能和简洁性最优）

### CAP 定理

分布式系统只能同时满足三个中的**两个**：

| 属性 | 含义 |
|------|------|
| **C**onsistency | 所有节点看到相同的最新数据 |
| **A**vailability | 系统始终响应请求 |
| **P**artition Tolerance | 网络分区时仍能继续运行 |

| 组合 | 牺牲 | 典型场景 |
|------|------|----------|
| **CP** | Availability | 金融系统（一致性优先） |
| **AP** | Consistency | 社交媒体（可用性优先，允许短暂不一致） |

### HDFS 架构

- 1 个 **NameNode**：管理命名空间，记录文件分块位置和副本信息
- 多个 **DataNode**：实际存储数据块
- 文件切成 **64MB 块**，每块默认复制 **3 份**
- 读取流程：Client → NameNode（获取块位置）→ 就近 DataNode 读取

### 分布式计算框架

**MapReduce（Hadoop）**：
- Map：过滤和排序（如按首字母分组）
- Reduce：汇总操作（如计数）

**Apache Spark**：
- 核心：**RDD**（Resilient Distributed Dataset）——不可变、分布式、容错
- **Lazy Evaluation**：只有 Action（`collect()`, `show()`, `count()`）才触发实际计算
- DataFrame API → 自动优化为 RDD 执行
- PySpark SQL：注册临时视图后可直接用 SQL

**Apache Flink**：
- Pipelined 执行：算子之间立即传递数据，无 Stage 分离
- DataSet API（批）+ DataStream API（流）
- 同样 Lazy Evaluation：调用 `env.execute()` 才启动

---

## Part 3 — DataOps、数据架构与 ML（W11）

### 数据架构类型

| 架构 | 特点 | 局限 |
|------|------|------|
| **Data Warehouse** | 结构化，OLAP，ETL/ELT | 不擅长非结构化数据 |
| **Data Lake** | 存一切（HDFS + S3），schema-on-read | 易变成"数据沼泽" |
| **Lambda Architecture** | Batch（冷路径）+ Stream（热路径）双通道 | 两套逻辑，维护成本高 |
| **Kappa Architecture** | 只用流处理，批处理通过重放流实现 | 对历史批处理灵活性稍弱 |

**Lambda vs Kappa**：
- Lambda：批处理给准确结果，流处理给低延迟结果，结果在 Serving Layer 合并
- Kappa：统一用流处理，更简洁，减少重复维护

### DataOps

DataOps = DevOps 思想应用于数据管道，核心是**自动化 + 协作 + 持续监控**

**四大核心职能**：

| 职能 | 说明 | 工具示例 |
|------|------|----------|
| **Pipeline Orchestration** | 自动协调 ETL 流程，管理依赖 | Apache Airflow |
| **Data Quality Monitoring** | 实时检测数据准确性和一致性 | — |
| **Governance & Security** | 合规（GDPR/CCPA），访问控制 | Apache Atlas |
| **Self-Service Data Access** | 让业务用户自助访问数据 | — |

**数据可观测性五大支柱**：

| 支柱 | 含义 |
|------|------|
| **Freshness** | 数据是否及时更新 |
| **Distribution** | 数值是否在合理范围内 |
| **Volume** | 数据量是否正常（有无缺失） |
| **Schema** | 数据结构是否变化 |
| **Lineage** | 数据如何在系统中流转变换 |

### Scaling ML：两种路线

| 路线 | 思路 | 代表 |
|------|------|------|
| **ML to Data** | 把 ML 算法嵌入数据库，数据不动 | **MADlib**（PostgreSQL 扩展） |
| **Data to ML** | 提取 feature 向量，送给 ML 平台 | **Feature Store** |

**MADlib**：
- 在 PostgreSQL 内运行 ML 算法（KNN、回归、分类、ARIMA 等）
- 无需导出数据，避免网络传输
- 调用方式：`SELECT * FROM madlib.knn(...)`

### Feature Store

**解决的核心问题**：训练和推理时 feature 不一致（training-serving skew）

**组件**：

| 组件 | 职责 |
|------|------|
| **Transformation** | 批量/流式/即时 feature 转换 |
| **Offline Storage** | 历史 feature，用于训练（S3/BigQuery/Snowflake） |
| **Online Storage** | 低延迟 feature，用于实时推理（Redis/DynamoDB） |
| **Serving** | 训练和推理时一致地提供 feature |
| **Feature Registry** | 元数据 + 版本控制的中央目录 |
| **Monitoring** | 检测 feature drift，监控服务健康 |

**三种 Feature Transform**：

| 类型 | 例子 |
|------|------|
| **Batch** | 用户历史购买数据中的国家信息（从数据仓库） |
| **Streaming** | 过去 30 分钟用户点击次数 |
| **On-Demand** | 当前用户是否在某地理位置（推理时实时计算） |

---

## 高频考点

**流处理（W9）**：
- DBMS vs DSMS 六个维度
- MQTT vs Kafka：存储、QoS、规模的差异
- 四种窗口类型：Agglomerative / Sliding / Tumbling / Session
- Event Time vs Processing Time，Watermark 的作用
- Spark Streaming vs Flink：micro-batching vs pipelining

**规模化（W10）**：
- CAP 定理：三选二，CP vs AP 的场景
- Column Store vs Row Store：适合 OLAP vs OLTP
- 三种分区策略：Round-robin / Hash / Range
- Lazy/Eager Replication + Primary/Multi-Leader 四种组合，实践中最常用的是哪个
- HDFS：NameNode 和 DataNode 的分工
- Spark Lazy Evaluation：什么触发执行（Action）

**DataOps & ML（W11）**：
- Lambda vs Kappa：两路 vs 单路
- DataOps 可观测性五支柱
- MADlib vs Feature Store：ML to Data vs Data to ML
- Feature Store 的 Offline vs Online Storage 用途
- Training-serving skew 是什么问题
