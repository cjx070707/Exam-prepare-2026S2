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

> 📌 **新增**

### 逻辑删除 vs 物理删除

时态数据库**不做物理删除（DELETE）**，而是"关闭"区间：

```sql
-- ❌ 错误：物理删除，历史永久丢失
DELETE FROM policies WHERE policy_id = 42;

-- ✅ 正确：逻辑删除，关闭 valid_end
UPDATE policies
SET valid_end = CURRENT_DATE
WHERE policy_id = 42;
```

关闭后该记录不再出现在当前查询中，但完整历史保留。

> 📌 **新增**

### 时态 SQL 查询模板

```sql
-- (a) Current Query：查当前有效记录
SELECT emp_id, salary
FROM emp_salary
WHERE valid_end = '9999-12-31';        -- 或 valid_end > CURRENT_DATE

-- (b) Sequenced Query：查某时间点（左闭右开区间）
SELECT salary
FROM emp_salary
WHERE emp_id = 101
  AND valid_start <= '2024-01-01'
  AND valid_end   >  '2024-01-01';     -- 右端用 >，避免边界重复计数

-- (c) Nonsequenced Query：全历史查询（当普通表用）
SELECT DISTINCT emp_id
FROM emp_salary
WHERE salary > 85000;
```

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

> 📌 **新增**

### Inverted Index（倒排索引）

**结构**：`词 → [文档列表（含位置/频率）]`

```
"data"       → [(Doc1, pos:0), (Doc2, pos:0)]
"pipeline"   → [(Doc1, pos:1), (Doc3, pos:0)]
```

**查询加速**：查 "data pipeline" 时 → 分别查索引取集合 → 求交集，无需扫描文档内容。O(1) 索引查找 + O(k) 集合运算（Elasticsearch、PostgreSQL `tsvector` 均基于此）。

> 📌 **新增**

### Subword Tokenization（BPE / WordPiece）

**词级分词的问题**：词汇表固定，未见过的词（OOV）只能替换为 `[UNK]`，信息全丢。

**Subword 方案**：将词分割为高频子词单元，未见过的词也能通过组合子词理解部分含义。

| 算法 | 使用者 | 标记方式 |
|------|--------|---------|
| **BPE** | GPT 系列 | 合并最高频字节对 |
| **WordPiece** | BERT | `##` 前缀 = 非词首部分 |

**NLP 管道顺序**：`文本 → Tokens → Token IDs → Embeddings → Model`

> 📌 **新增**

### Sparse Vector vs Dense Vector

| | Sparse（TF-IDF） | Dense（BERT） |
|-|-----------------|--------------|
| **维度** | 词汇表大小（数万维） | 固定低维（如 768） |
| **非零值** | 极少 | 全部非零 |
| **语义** | 无（词袋） | 有（上下文） |
| **大规模搜索** | Inverted Index | 向量数据库 ANN（Faiss、pgvector） |

关键词精确匹配 → Sparse；语义相似搜索 → Dense。

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

> 📌 **新增**

**Partition 分配规则与 Rebalance**：
- 组内每个 Partition 只能分配给**一个消费者**；当**消费者数 > Partition 数**时，多余消费者 **idle（空闲）**
  - 例：6 Partitions，8 消费者 → 6 个消费者各负责 1 个，2 个空闲
- **Rebalance**：消费者宕机或加入时，Kafka 自动重分配 Partition，从上次提交的 offset 续，不丢数据
- **总副本数 = Partition 数 × Replication Factor**（例：4 Partitions × RF 3 = 12 个副本）

> 📌 **新增**

**三种交付语义（Delivery Semantics）**：

| 语义 | 含义 | 难度 |
|------|------|------|
| **At-most-once** | 最多处理一次，可能丢失 | 最简单 |
| **At-least-once** | 至少处理一次，可能重复 | 中等 |
| **Exactly-once** | 恰好处理一次 | **最难** |

**Exactly-once 实现需同时满足**：
1. **Idempotent Producer**：重试不产生重复消息
2. **原子性提交**：offset 更新与业务写出原子完成（2PC）

Flink / Kafka Streams 通过两阶段提交（2PC）支持 Exactly-once，但引入额外延迟。

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

> [!info] 问题链
> 单机撑不住大数据 → 加机器（**Scale-Out**）→ 多机器怎么存得快？（**Column Store + 分区**）→ 机器挂了怎么办？（**Replication**）→ 复制后网络断了数据不一致？（**CAP**）→ 数据分散了怎么算？（**HDFS + MapReduce → Spark**）

---

### Scale-Up vs Scale-Out

> [!tip] 单机撑不住了，换更强的机器，还是加更多机器？

| | Scale-Up（纵向扩展） | Scale-Out（横向扩展） |
|--|---------------------|----------------------|
| 方式 | 换更强的单机硬件 | 增加更多节点组成集群 |
| 上限 | 有硬件天花板 | 理论上无限 |
| 架构 | 单机 | Shared-nothing（各节点独立） |

*选了 Scale-Out，数据分散到多台机器——但分析查询只用少数几列，每次读整行太浪费 I/O。*

---

### 存储优化

> [!tip] 多机存储后，怎么让分析查询少读点数据？

**Column Store vs Row Store**

| | Row Store | Column Store |
|--|-----------|--------------|
| 数据组织 | 按行存储 | 按列存储 |
| 适合 | OLTP（点查询，更新） | OLAP（聚合，大范围扫描） |
| 压缩 | 一般 | 更好（同类型数据，可用 run-length/dictionary encoding） |
| 例子 | MySQL, PostgreSQL | BigQuery, Apache Parquet |

**Wide Column Store**（如 HBase, BigTable）≠ Column Store：按 column family 分组，按行存储每个 family，适合稀疏数据

*存储结构优化了，但数据具体切到哪台机器？需要一套分区规则。*

---

### 数据分区（Partitioning / Sharding）

> [!tip] 大表放不进一台机器，按什么规则切分到不同节点？

| 策略 | 方式 | 适用 | 代价 |
|------|------|------|------|
| **Horizontal Partitioning** | 按行切分 | 大表扩展，并行查询 | — |
| **Vertical Partitioning** | 按列切分 | 分离常用列和冷列 | — |
| **Round-robin** | 轮询分配到各节点 | 均匀分布 | 无法利用数据局部性 |
| **Hash Partitioning** | `hash(key) % N` 决定节点 | 点查（=）快，均匀分布 | 范围查询必须扫全部节点 |
| **Range Partitioning** | 按值区间划分 | 范围查询只扫对应分区 | 可能数据倾斜（热点） |

**核心矛盾**：Hash 破坏数据顺序性 → 范围查询必须扫全表；Range 保留顺序 → 点查也要扫全表。两者不可兼得，根据查询模式选择。

*数据分散到多台机器了，如果某台宕机，那台机器上的数据就丢了——需要多副本备份。*

---

### 数据复制（Replication）

> [!tip] 机器宕机数据就丢，怎么保证数据安全和读性能？

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

*有了多副本，但网络一断，各副本的数据可能已经不一致。这时系统要怎么应对？*

---

### CAP 定理

> [!tip] 多副本网络断了，保数据一致还是保系统可用？

分布式系统只能同时满足三个中的**两个**：

- **C**onsistency（一致性）：所有节点看到相同数据
- **A**vailability（可用性）：系统始终响应请求
- **P**artition Tolerance（分区容忍性）：网络分区时仍能工作

| 组合 | 牺牲 | 适用场景 |
|------|------|----------|
| CP | Availability | 金融系统（一致性优先） |
| AP | Consistency | 社交媒体（可用性优先，允许短暂不一致） |

*存储、分区、复制都解决了。接下来：数据分散在多台机器上，计算怎么做？把数据都传到一台机器上太慢——让计算去找数据。*

---

### 分布式计算框架

> [!tip] 数据在 HDFS 上分散存好了，计算怎么也跟着分散到各台机器？

**HDFS（Hadoop Distributed File System）**
- 1 个 NameNode（元数据管理）+ 多个 DataNode（实际存储）
- 文件切成 **64 MB** 的块（PPT 默认值），每块默认复制 3 份

> 📌 **新增**

**HDFS 读取详细流程（5 步）**：
1. Client → NameNode：发送读取请求（文件路径）
2. NameNode → Client：返回块列表 + 各块的 DataNode 副本位置
3. Client 缓存：客户端缓存块位置信息
4. Client → DataNode（就近副本）：建立 TCP 连接按块读取
5. DataNode → Client：传输数据块（多块可并行，NameNode 不参与数据传输）

> 📌 **新增**

**NameNode SPOF 与 HA 方案**：
- **为什么 NameNode 宕机 = 集群不可用**：NameNode 是唯一保存文件系统命名空间和块位置映射的节点，没有它客户端无法定位任何数据
- **HA 方案**：Active NameNode + Standby NameNode，通过 **JournalNode 集群**同步 edit log，**ZooKeeper** 监控心跳，宕机后秒级自动 Failover

**Apache Spark**
- 核心抽象：**RDD**（Resilient Distributed Dataset）——不可变、分布式、可容错
- **Lazy Evaluation**：只有遇到 Action（如 `collect()`, `show()`）才真正执行
- DataFrame API 更高级，支持 SQL 风格查询
- SparkSQL：注册 DataFrame 为临时视图后可直接用 SQL 查询

> 📌 **新增**

**Spark RDD Caching**：
```python
rdd.cache()   # 将计算结果存入内存
```
第一次 Action 触发计算并缓存到内存，后续运行直接读取，跳过重算。MapReduce 每次都从 HDFS 读原始数据——**内存缓存是 Spark 比 MapReduce 快的核心原因之一**。

> 📌 **新增**

**MapReduce 三阶段（Shuffle & Sort）**：

| 阶段 | 说明 |
|------|------|
| **Map** | 输入一行，输出 `(key, value)` 键值对（如 `("data", 1)`） |
| **Shuffle & Sort** | 按 key 哈希路由到对应 Reducer，并排序；相同 key 的所有值汇集到同一 Reducer |
| **Reduce** | 对每个 key 的 value 列表汇总（如求和），输出最终结果 |

没有 Shuffle & Sort，各 Mapper 的 `("data", 1)` 就无法汇集到一起求和。

*Spark 用微批（Micro-batching）模拟流处理，延迟在秒级。如果需要毫秒级实时处理、算子间零延迟传递呢？这就是 Flink 的场景——它是真正的流处理引擎。*

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

> 📌 **新增**

**Modern Data Stack（现代数据栈）**：
```
数据源 → Fivetran / Airbyte（采集）→ dbt（转换）→ Snowflake / BigQuery（存储）→ Power BI / Tableau（可视化）
```

**dbt（data build tool）** — transformation 层的核心工具：
- 在数据仓库**内部**用 SQL 定义转换模型，管理模型间依赖（DAG）
- **版本控制**：所有 SQL 通过 Git 管理，变更可追溯，支持审计
- **内置数据测试**：`not_null`、`unique`、`accepted_values`，每次 pipeline 运行自动验证
- **自动生成 Lineage 图**：可追溯数据从哪些原始表经过哪些转换得到

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

> 📌 **新增**

**Point-in-Time Correctness（时间点准确性）**：

**问题**：标准 Feature Store 只存最新 feature 值。若事后审计"某申请人在 2024-03-15 的信用评分"，而值已被覆盖，则无法重建历史决策依据。

**解决方案**：Offline Store 保存 feature 值的**完整历史（带时间戳）**，支持"某时间点该实体的 feature 是什么"的查询。

**两个作用**：
1. **监管审计**：重建历史特征，解释当时的决策
2. **防止 Label Leakage**：训练时只使用决策时刻之前已存在的数据，避免未来信息泄漏

---

## 高频考点速查

### 常考对比汇总

| 对比 | 核心区别 |
|------|----------|
| Valid Time vs Transaction Time | 现实事实的时间 vs 数据库记录的时间 |
| 逻辑删除 vs 物理删除 | `UPDATE valid_end = CURRENT_DATE` vs `DELETE` |
| Point-based vs Sequence-based | 每行一时刻 vs 一行存数组 |
| TF-IDF vs BERT | 稀疏无语义 vs 稠密有上下文 |
| Sparse vs Dense Vector | 高维稀疏无语义（倒排索引搜索）vs 低维稠密有语义（ANN 搜索） |
| BPE vs WordPiece | GPT 系列 vs BERT；都是解决 OOV 的 Subword 分词 |
| MQTT vs Kafka | 轻量 IoT vs 大规模持久化流 |
| At-most vs At-least vs Exactly-once | 可丢 vs 可重复 vs 最难（需 Idempotent + 2PC） |
| Sliding vs Tumbling Window | 可重叠 vs 不重叠 |
| Event Time vs Processing Time | 真实发生时间 vs 处理器处理时间 |
| Spark vs Flink（流处理） | Micro-batching vs Pipelining |
| MapReduce vs Spark | 每次读磁盘 vs 内存缓存（cache()），Spark 快 10-15× |
| Scale-up vs Scale-out | 换更强单机 vs 加更多节点 |
| Column Store vs Row Store | OLAP 友好 vs OLTP 友好 |
| Sync vs Async Replication | 强一致低性能 vs 弱一致高性能 |
| Hash vs Range Partitioning | 点查询快 vs 范围查询快 |
| Lambda vs Kappa | 批+流双路 vs 纯流单路 |
| MADlib vs Feature Store | ML to Data vs Data to ML |
| dbt | Modern Data Stack 的 transformation 层：SQL 版本控制 + 测试 + 血缘 |
| Point-in-Time Correctness | Offline Store 保存历史 feature，支持审计 + 防 label leakage |

### 系统 → 用途速查

| 系统 | 用途 |
|------|------|
| TimescaleDB / InfluxDB | 时序数据库 |
| MQTT | IoT 轻量 Pub/Sub |
| Apache Kafka | 大规模分布式 Pub/Sub + 持久化 |
| Apache Spark | 分布式批处理 + 流处理（micro-batch） |
| Apache Flink | 分布式批处理 + **低延迟**流处理（pipelining） |
| HDFS | 分布式文件系统（Hadoop 生态，64MB 块，NameNode 存元数据） |
| MADlib | PostgreSQL 内置 ML |
| Feast / Delta Lake | Feature Store |
| Apache Airflow | Pipeline Orchestration |
| dbt | 数据仓库内 SQL 转换 + 测试 + 血缘（Modern Data Stack） |
| exiftool | 图片/视频元数据提取 |
| Faiss / pgvector | 大规模 Dense Vector ANN 相似度搜索 |
| Elasticsearch | 倒排索引全文搜索 |
