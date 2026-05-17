# COMP5339 Quiz 2 复习笔记 — Week 7–11

> 考试题型：**短答题为主，可能有 MCQ**。重点是概念解释 + 系统对比。

---

## Week 7 — Temporal Data Engineering

**叙事链**：普通数据库只存"当前状态" → 现实世界的数据有时间维度 → 需要追踪历史/未来状态 → 引入时态数据库和时间序列存储

---

### 核心概念：时态数据类型

| 类型 | 含义 | 例子 |
|------|------|------|
| **Instant / Point** | 某一时刻发生的事 | 订单下单时间 10:05 AM |
| **Interval** | 一段持续时间（duration） | 员工合同从 2020 年到 2022 年 |
| **Period** | 有起止点的时间段（anchored） | 每个日历年 |

SQL 对应类型：`DATE`, `TIME`, `TIMESTAMP`, `INTERVAL`

---

### 两种时间语义（重点考点）

| 时间类型 | 含义 | 特点 |
|----------|------|------|
| **Valid Time（事实时间）** | 事实在现实世界中成立的时间 | 可以向前或向后修改 |
| **Transaction Time（事务时间）** | 数据被存入数据库的时间 | **只能向前**，不可修改历史 |
| User-defined Time | 无特殊语义，应用层自己解释 | 如生日、发布时间 |

**Bitemporal table** = 同时有 Valid time + Transaction time 两列

---

### 时态查询语句类型

| 类型 | 含义 | 例子 |
|------|------|------|
| **Current** | 查当前时刻成立的事实 | "现在库存多少？" |
| **Sequenced** | 查某时刻/某时段成立的事实 | "2022年的工资是多少？" |
| **Nonsequenced** | 忽略时间，查历史中任意时刻 | "某员工有没有被记录过高薪？" |

---

### 表示"现在"（NOW/UC）的策略

传统数据库没有内置时态支持，常见做法：

- **Max-timestamp（最常用）**：用 `9999-12-31` 表示"至今有效"
- NULL：会导致比较失效（NULL 比较返回 FALSE）
- Min-timestamp：反直觉
- PostgreSQL 用 `'infinity'` 表示无穷大（不要用 `now` 关键字，它表示事务开始时间）

---

### 时序数据的三种存储方案（重点对比）

| 方案 | 结构 | 优点 | 缺点 |
|------|------|------|------|
| **Point-based（点表示）** | 每行一个时刻 | 标准 SQL，简单，容易索引 | 行数多，高频数据存储开销大 |
| **Sequence-based（序列表示）** | 一行存数组 | 紧凑，适合批量分析 | 查询复杂，索引难，不跨 DBMS |
| **Dedicated TSDB（专用时序库）** | TimescaleDB, InfluxDB | 高性能，自动分区，内置 downsampling | 额外维护成本，学习曲线 |

PostgreSQL 的 Range Types：`DATERANGE`, `TSRANGE`，用 GiST 索引
常用谓词：`&&`（重叠），`@>`（包含），`upper_inf()`（无上界）

---

## Week 8 — Unstructured Data

**叙事链**：80-90% 的业务数据是非结构化的（图片/视频/文本） → 无法直接存入关系表 → 需要预处理 + 特征提取 → 转换成数值向量才能用于 ML

---

### 文本数据处理流程

```
原始文本 → Tokenisation → Normalisation（小写/词根化） → Stop-word removal → Feature vector
```

**TF-IDF（Bag of Words 模型）**

- **TF**（词频）：词在文档中出现的次数
- **IDF**（逆文档频率）：`log(总文档数 / 含该词的文档数)`，出现越普遍权重越低
- **TF-IDF = TF × IDF**：既常见又有区分度的词权重高
- Python 工具：`sklearn.feature_extraction.text.CountVectorizer`

**Word Embeddings（语义向量）**

| 方法 | 特点 |
|------|------|
| **TF-IDF** | 稀疏向量，无语义，计算简单 |
| **Word2Vec** | 稠密向量，有语义相似性 |
| **BERT** | 上下文感知（bidirectional），同一词不同语境有不同向量 |

**文档相似度**：Cosine Similarity（向量夹角越小越相似）

---

### 图像数据类型

| 类型 | 特点 |
|------|------|
| **RGB（TrueColor）** | 3 通道，每像素 3×8 bit，约 1600 万色 |
| **Grayscale** | 单通道，只有亮度信息，常用于医学/科学图像 |
| **Binary** | 黑白二值（0/1），用于分割掩码（mask） |

---

### 图像特征提取

两种路径：
- **White box**：手工设计特征（基于图像梯度等），如 skimage
- **Black box**：神经网络自动学习特征（CNN、LLM）

图像相似度搜索流程：提取特征向量 → 建索引 → 查询时转换为相同向量 → 找最近邻

---

### 元数据分析

- 数字图片/视频含有 **EXIF/XMP** 元数据（拍摄时间、GPS、相机参数）
- 工具：**exiftool**（命令行）
  ```bash
  exiftool filename              # 读全部元数据
  exiftool -GPS* filename        # 只读 GPS
  exiftool -common -csv=out.csv *.jpg  # 批量导出为 CSV
  ```
- "一个用户的元数据就是另一个用户的数据"——元数据可用于情报分析

---

## Week 9 — Stream Data Processing

**叙事链**：传统 DBMS 处理"静止的数据" → 很多数据是实时产生的流 → 需要"在运动中"处理 → 引入 Pub/Sub 消息系统 + 流处理引擎

---

### DBMS vs DSMS（重要对比）

| 维度 | DBMS（传统数据库） | DSMS（流数据系统） |
|------|-------------------|-------------------|
| 数据 | Persistent relations | Transient streams |
| 大小 | 有界 | **无界** |
| 更新方式 | Insert/Update/Delete | Append only |
| 查询 | 一次性查询 | **持续查询** |
| 答案 | 精确 | 可能近似 |

---

### Pub/Sub 模式

- **Publisher** 发布消息到 **Broker** 的某个 **Topic**
- **Subscriber** 订阅感兴趣的 Topic，Broker 推送消息
- 同一消息可被多个 Subscriber 同时消费

---

### MQTT vs Kafka（重点对比）

| 维度 | MQTT | Kafka |
|------|------|-------|
| 定位 | 轻量级，适合 IoT/传感器 | 大规模分布式流数据 |
| 消息存储 | 默认不存储（retain flag 存最后一条） | **持久化存储**，可回放 |
| QoS | 0 / 1 / 2（at most / at least / exactly once） | **At least once** |
| 扩展性 | 有限 | 高（分区 + 副本） |
| 默认 QoS | QoS 0 | — |

**MQTT 要点**：
- Topic 区分大小写（`Temp ≠ temp`）
- 通配符：`+`（单级），`#`（多级）
- QoS 0 = at most once；QoS 1 = at least once；QoS 2 = exactly once

**Kafka 要点**：
- Topic 按 Partition 存储，每个 Partition 是有序 append-only 日志
- 不同 Consumer Group 可以独立消费同一 Topic
- 支持容错（Replication Factor N → 最多容忍 N-1 台服务器故障）

---

### 流查询：Stateless vs Stateful

| 类型 | 含义 | 例子 |
|------|------|------|
| **Stateless** | 每条记录独立处理 | `SELECT` + `WHERE`（过滤/投影） |
| **Stateful** | 需要跨多条记录维护状态 | 聚合、Join、窗口 |

---

### 窗口类型（Window）

窗口 = 从无界流中截取有界片段的机制

| 窗口类型 | 含义 | 例子 |
|----------|------|------|
| **Agglomerative** | 从起点累积到当前时刻 | 今日总点赞数 |
| **Sliding** | 固定大小，可重叠滑动 | 最近 5 分钟点赞数，每 30 秒更新 |
| **Tumbling** | 固定大小，**不重叠** | 每 1 分钟的点赞数 |
| **Session** | 由数据中的事件标记（如 auction_start/end）定义 | 一次竞价会话 |

---

### 三种时间概念

| 时间 | 含义 |
|------|------|
| **Event Time** | 事件在现实中发生的时间（最准确，但可能乱序到达） |
| **Ingestion Time** | 数据进入消息系统的时间 |
| **Processing Time** | 流处理引擎处理该事件的时间（最容易获得，但不反映真实顺序） |

**Watermark**：流处理器用来声明"到目前为止，所有早于时间 T 的事件都已到达"，用于触发基于 Event Time 的窗口计算

---

### Spark Streaming vs Apache Flink（重点对比）

| 维度 | Apache Spark Streaming | Apache Flink |
|------|------------------------|--------------|
| 原理 | **Micro-batching**（把流切成小批次） | **Pipelining**（真正的流处理） |
| 数据抽象 | RDD / DStream | DataSet / DataStream |
| 处理阶段 | 分离的 Stages | **重叠的**（低延迟） |
| 优化器 | SparkSQL + Adaptive Exec | 内置于 API |
| 流处理延迟 | 较高（毫秒~秒级） | 更低（毫秒级） |

> **Kafka/MQTT = 消息存储系统；Spark/Flink = 流处理计算引擎**，两者角色不同，不要混淆

---

## Week 10 — Scalable Data Engineering

**叙事链**：单机处理不了大数据 → Scale-up 有上限 → Scale-out 分布式集群 → 数据需要分片和复制 → 需要分布式计算框架

---

### Scale-Up vs Scale-Out

| | Scale-Up（纵向扩展） | Scale-Out（横向扩展） |
|--|---------------------|----------------------|
| 方式 | 换更强的单机硬件 | 增加更多节点组成集群 |
| 上限 | 有硬件天花板 | 理论上无限 |
| 架构 | 单机 | Shared-nothing（各节点独立） |

---

### 存储优化

**Column Store vs Row Store**

| | Row Store | Column Store |
|--|-----------|--------------|
| 数据组织 | 按行存储 | 按列存储 |
| 适合 | OLTP（点查询，更新） | OLAP（聚合，大范围扫描） |
| 压缩 | 一般 | 更好（同类型数据，可用 run-length/dictionary encoding） |
| 例子 | MySQL, PostgreSQL | BigQuery, Apache Parquet |

**Wide Column Store**（如 HBase, BigTable）≠ Column Store：按 column family 分组，按行存储每个 family，适合稀疏数据

---

### 数据分区（Partitioning / Sharding）

| 策略 | 方式 | 适用 |
|------|------|------|
| **Horizontal Partitioning** | 按行切分（每个分区是一组行） | 大表扩展，并行查询 |
| **Vertical Partitioning** | 按列切分 | 分离常用列和冷列 |
| **Round-robin** | 轮询分配到各节点 | 均匀分布 |
| **Hash Partitioning** | 对 key 做哈希决定节点 | 点查询快 |
| **Range Partitioning** | 按值范围分区 | 范围查询快 |

---

### 数据复制（Replication）

**目的**：提高可用性（一个节点故障仍可读）和读性能

| | 同步（Eager） | 异步（Lazy） |
|--|---------------|-------------|
| 一致性 | 强 | 弱（可能读到旧数据） |
| 性能 | 差（需等所有副本确认） | 好 |
| 实践 | 少用 | **大多数系统默认** |

| | Primary Copy（单 Leader） | Multi-Leader |
|--|--------------------------|--------------|
| 写入 | 只能写 Primary | 可写任意 Leader |
| 冲突 | 无 | 需要冲突解决 |
| 实践 | **更常用**（如 MongoDB） | 分布式写场景 |

---

### CAP 定理

分布式系统只能同时满足三个中的**两个**：

- **C**onsistency（一致性）：所有节点看到相同数据
- **A**vailability（可用性）：系统始终响应请求
- **P**artition Tolerance（分区容忍性）：网络分区时仍能工作

| 组合 | 牺牲 | 适用场景 |
|------|------|----------|
| CP | Availability | 金融系统（一致性优先） |
| AP | Consistency | 社交媒体（可用性优先，允许短暂不一致） |

---

### 分布式计算框架

**HDFS（Hadoop Distributed File System）**
- 1 个 NameNode（元数据管理）+ 多个 DataNode（实际存储）
- 文件切成 64 MB 的块，默认复制 3 份

**Apache Spark**
- 核心抽象：**RDD**（Resilient Distributed Dataset）——不可变、分布式、可容错
- **Lazy Evaluation**：只有遇到 Action（如 `collect()`, `show()`）才真正执行
- DataFrame API 更高级，支持 SQL 风格查询
- SparkSQL：注册 DataFrame 为临时视图后可直接用 SQL 查询

**Apache Flink**
- 核心：Pipelined 执行（算子之间立即传递数据，无 Stage 分离）
- DataSet API（批处理）+ DataStream API（流处理）
- 同样是 Lazy Evaluation：调用 `env.execute()` 才开始

---

## Week 11 — DataOps, Data Architectures & ML

**叙事链**：数据管道需要在生产环境长期稳定运行 → 需要监控、编排、质量管控 → DataOps 解决这个问题 → 如何把数据高效地送给 ML 模型 → Feature Store

---

### 数据架构类型

| 架构 | 特点 | 局限 |
|------|------|------|
| **Data Warehouse** | 结构化数据，OLAP，ETL/ELT | 不擅长处理非结构化数据 |
| **Data Lake** | 存一切（结构/非结构化），HDFS + MapReduce | 易变成"数据沼泽"（data swamp） |
| **Lambda Architecture** | Batch（冷路径）+ Stream（热路径）双通道 | 维护两套逻辑复杂 |
| **Kappa Architecture** | 只用流处理一条路径统一处理 | 对历史数据的批处理不如 Lambda 灵活 |

**Lambda vs Kappa**：
- Lambda：批处理给准确结果，流处理给低延迟结果，最终合并 → 两套系统，维护成本高
- Kappa：只用流处理，批处理也通过重放流来实现 → 更简洁

---

### DataOps

DataOps = DevOps 理念应用于数据管道，核心是**自动化 + 协作 + 持续监控**

**四大核心职能**：

1. **Pipeline Orchestration**（编排）：自动协调 ETL 流程（工具：Apache Airflow）
2. **Data Quality Monitoring**（质量监控）：实时检测数据准确性
3. **Governance & Security**（治理与安全）：合规（GDPR/CCPA）、访问控制
4. **Self-Service Data Access**：让业务用户自助访问数据

**数据可观测性五大支柱**（Data Observability）：

| 支柱 | 含义 |
|------|------|
| **Freshness** | 数据是否及时更新 |
| **Distribution** | 数值是否在合理范围内 |
| **Volume** | 数据量是否正常（有无缺失/异常） |
| **Schema** | 数据结构是否发生变化 |
| **Lineage** | 数据如何在系统中流转变换 |

---

### Scaling ML：两种路线

| 路线 | 思路 | 例子 |
|------|------|------|
| **ML to Data**（计算去找数据） | 把 ML 算法嵌入数据库，数据不动 | **MADlib**（PostgreSQL 扩展） |
| **Data to ML**（数据送给模型） | 提取特征向量传给 ML 平台 | **Feature Store** |

**MADlib**：
- 在 PostgreSQL 内运行 ML 算法（KNN、ARIMA、分类、回归等）
- 无需导出数据，减少网络传输
- SQL 调用：`SELECT * FROM madlib.knn(...)`

---

### Feature Store

**解决的问题**：训练和推理时使用的 feature 不一致（training-serving skew）

**核心组件**：

| 组件 | 职责 |
|------|------|
| **Transformation** | 批量 / 流式 / 即时 feature 转换 |
| **Storage（Offline）** | 历史 feature 数据，用于训练（S3/BigQuery/Snowflake） |
| **Storage（Online）** | 低延迟 feature 服务，用于实时推理（Redis/DynamoDB） |
| **Serving** | 训练和推理时一致地提供 feature |
| **Feature Registry** | 元数据 + 版本控制的中央目录 |
| **Monitoring** | 检测 feature drift，监控服务健康 |

**三种 Feature Transform 类型**：

| 类型 | 含义 | 例子 |
|------|------|------|
| **Batch Transform** | 对静止数据批量处理 | 用户历史购买数据中的国家信息 |
| **Streaming Transform** | 对流数据实时计算 | 过去 30 分钟用户点击次数 |
| **On-Demand Transform** | 推理时实时计算 | 当前用户是否在某地理位置 |

---

## 高频考点速查

### 常考对比汇总

| 对比 | 核心区别 |
|------|----------|
| Valid Time vs Transaction Time | 现实事实的时间 vs 数据库记录的时间 |
| Point-based vs Sequence-based | 每行一时刻 vs 一行存数组 |
| TF-IDF vs BERT | 稀疏无语义 vs 稠密有上下文 |
| MQTT vs Kafka | 轻量 IoT vs 大规模持久化流 |
| Sliding vs Tumbling Window | 可重叠 vs 不重叠 |
| Event Time vs Processing Time | 真实发生时间 vs 处理器处理时间 |
| Spark vs Flink（流处理） | Micro-batching vs Pipelining |
| Scale-up vs Scale-out | 换更强单机 vs 加更多节点 |
| Column Store vs Row Store | OLAP 友好 vs OLTP 友好 |
| Sync vs Async Replication | 强一致低性能 vs 弱一致高性能 |
| Lambda vs Kappa | 批+流双路 vs 纯流单路 |
| MADlib vs Feature Store | ML to Data vs Data to ML |

### 系统 → 用途速查

| 系统 | 用途 |
|------|------|
| TimescaleDB / InfluxDB | 时序数据库 |
| MQTT | IoT 轻量 Pub/Sub |
| Apache Kafka | 大规模分布式 Pub/Sub + 持久化 |
| Apache Spark | 分布式批处理 + 流处理（micro-batch） |
| Apache Flink | 分布式批处理 + **低延迟**流处理（pipelining） |
| HDFS | 分布式文件系统（Hadoop 生态） |
| MADlib | PostgreSQL 内置 ML |
| Feast / Delta Lake | Feature Store |
| Apache Airflow | Pipeline Orchestration |
| exiftool | 图片/视频元数据提取 |
