# Group 4 Test — Scale & Operations

**Scope: Week 9 (Stream Processing) + Week 10 (Scalable Engineering) + Week 11 (DataOps & ML)**

**Total: 60 marks | Suggested time: 45 minutes**

---

## Section A — Multiple Choice (2 marks each, 20 marks total)

**Q1.** A smart factory deploys 10,000 low-power sensors that each send a temperature reading every 30 seconds. The readings only need to be stored for the last 24 hours for alerting. Which messaging system is most appropriate?

- A. Apache Kafka — high-throughput, durable, replayable event log
- B. MQTT — lightweight IoT protocol designed for constrained devices
- C. Apache Flink — stream processing engine with low latency
- D. Apache Spark Streaming — micro-batch processing framework

> [!note]- Answer
> **B** — MQTT 是专为低功耗、低带宽设备设计的轻量级消息协议，非常适合 IoT 传感器场景。Kafka 功能强大但资源消耗大，不适合 10,000 个低功耗设备。Flink 和 Spark 是计算引擎，不是消息传输协议。

---

**Q2.** A stream processing job needs to count purchases **per user per hour**, updating the count every 15 minutes (so the windows overlap). Which window type should be used?

- A. Tumbling window — fixed size, non-overlapping
- B. Session window — defined by data events, variable size
- C. Sliding window — fixed size, overlapping, configurable slide interval
- D. Agglomerative window — accumulates from stream start

> [!note]- Answer
> **C** — **Sliding window**：固定大小（1 小时），但 slide interval（15 分钟）小于 window size（1 小时），所以窗口重叠。Tumbling 是不重叠的，不满足"每 15 分钟更新"的需求。Session 是由事件标记定义边界，大小不固定。Agglomerative 是从流起点累积，没有固定结束点。

---

**Q3.** In a stream processing job using **event time**, events from mobile devices may arrive up to 2 minutes late due to intermittent connectivity. What is the correct mechanism to handle this without dropping valid data?

- A. Switch to processing time to avoid the late data problem entirely
- B. Increase the micro-batch interval in Spark to 2 minutes
- C. Set a watermark with an allowed lateness of 2 minutes
- D. Use a session window instead of a tumbling window

> [!note]- Answer
> **C** — Watermark 声明"截至时间 T，所有早于 T 的事件已到达"。设置 2 分钟的 allowed lateness 后，系统会等待最多 2 分钟再触发窗口，从而容纳迟到的事件。切换到 processing time 会丢失事件的真实发生顺序，得到错误结果。

---

**Q4.** What is the fundamental architectural difference between Apache Spark Streaming and Apache Flink?

- A. Spark processes data in parallel; Flink processes data sequentially
- B. Spark uses micro-batching (processes stream as small batches); Flink uses pipelining (passes records directly between operators)
- C. Spark supports only batch processing; Flink supports only stream processing
- D. Spark requires Kafka as input; Flink can accept any data source

> [!note]- Answer
> **B** — **Spark Streaming** 将流切成小时间批次（micro-batching），每批作为 mini-batch 处理，有 Stage 边界和同步开销。**Flink** 是真正的流处理：每条记录到达后立即在算子间传递（pipelining），无批次边界，延迟更低。

---

**Q5.** An analytics query reads only 5 columns out of 300 and scans 2 billion rows. Which storage format minimises the amount of data read from disk?

- A. Row store (PostgreSQL)
- B. Document store (MongoDB)
- C. Wide Column Store (HBase)
- D. Column store (Parquet)

> [!note]- Answer
> **D** — Column store（如 Parquet）按列存储，查询只涉及 5 列时，只需从磁盘读取这 5 列，其余 295 列完全跳过。Row store 每读一行就必须读全部 300 列。Wide Column Store 按 column family 分组，不是纯列式，不适合这种 OLAP 聚合场景。

---

**Q6.** A distributed database experiences a network partition. The system continues to serve all read and write requests, but some nodes may return slightly stale data. Which CAP configuration does this describe?

- A. CP — Consistency + Partition Tolerance
- B. CA — Consistency + Availability
- C. AP — Availability + Partition Tolerance
- D. PA — Partition Tolerance + Availability (same as AP)

> [!note]- Answer
> **C** — 系统在网络分区时仍然响应请求（Availability ✓），但可能返回过时数据（Consistency ✗），同时能容忍网络分区（Partition Tolerance ✓）= **AP**。CA 在分布式系统中实际上无法实现，因为 P 不可避免。

---

**Q7.** A large e-commerce table is partitioned by `order_date`. A query filters `WHERE order_date BETWEEN '2025-01-01' AND '2025-03-31'`. Which partitioning strategy was used, and what is its advantage for this query?

- A. Hash partitioning — the hash of `order_date` determines the partition, enabling fast range scans
- B. Round-robin partitioning — data is distributed evenly, enabling parallel scans
- C. Range partitioning — data within the date range is co-located in a subset of partitions, minimising partitions scanned
- D. Vertical partitioning — columns are split across partitions, reducing I/O per row

> [!note]- Answer
> **C** — **Range Partitioning** 按值范围划分分区，日期在 Q1 2025 的数据集中在少数几个分区里。这个查询只需扫描那几个分区，而不是全表——这叫 **partition pruning**（分区裁剪）。Hash partitioning 对范围查询没有优势，因为相邻日期可能在不同分区。

---

**Q8.** Which Spark operation triggers actual execution of a lazy evaluation plan?

- A. `.filter(col("region") == "Asia")`
- B. `.groupBy("category").agg(avg("revenue"))`
- C. `.orderBy(col("revenue").desc())`
- D. `.count()`

> [!note]- Answer
> **D** — `count()` 是 **Action**，会触发实际执行。`.filter()`、`.groupBy()`、`.orderBy()` 都是 **Transformation**，只构建逻辑执行计划，不执行。其他 Action 包括：`collect()`、`show()`、`take(n)`、`write()`。

---

**Q9.** A company's Lambda Architecture has a batch layer and a speed layer. The main operational complaint is that the team spends twice as much time on bug fixes because the same logic must be maintained in two separate codebases. Which architecture addresses this specific problem?

- A. Star Schema — separates facts from dimensions
- B. Kappa Architecture — uses a single stream processing pipeline for both real-time and historical reprocessing
- C. Data Lake — stores all raw data in one place
- D. Feature Store — centralises ML feature logic

> [!note]- Answer
> **B** — **Kappa Architecture** 的核心动机就是消除 Lambda 的双重代码库问题。Kappa 用一套流处理代码处理实时数据，历史重处理通过回放 Kafka event log（从 offset 0 重读）复用同一套代码实现，彻底避免了逻辑维护两遍的问题。

---

**Q10.** A fraud detection model's accuracy drops after deployment. Investigation finds that the feature `tx_count_last_1h` was computed from a daily batch snapshot during training, but is recomputed from a live stream at inference time — using a slightly different time window. What is this problem called, and what system is introduced to solve it?

- A. Data drift — solved by retraining the model more frequently
- B. Training-serving skew — solved by introducing a Feature Store
- C. Concept drift — solved by switching from batch to stream training
- D. Model decay — solved by using a larger training dataset

> [!note]- Answer
> **B** — **Training-serving skew**：训练和推理时同一 feature 的计算逻辑不一致，导致模型在生产中表现下降。**Feature Store** 通过统一 feature transformation 定义（训练和推理都从同一 pipeline 取 feature）来消除这个不一致。Data drift 和 concept drift 是数据分布变化问题，与此不同。

---

## Section B — Short Answer (8 marks each, 32 marks total)

**Q11.** A ride-sharing company processes GPS pings from drivers in real time. They need to: (1) count the number of active drivers in each city zone **every 5 minutes** (non-overlapping), and (2) compute a **running total** of trips completed since the start of the day. For each requirement, identify the window type, classify the operation as stateless or stateful, and explain whether event time or processing time is more appropriate. (8 marks)

> [!note]- Answer
> **需求 1：每 5 分钟统计各区活跃司机数**
> 
> - **Window type：Tumbling Window** — 固定大小（5 分钟），不重叠，每个事件只属于一个窗口
> - **Stateful** — 需要在 5 分钟内跨多条记录维护每个 zone 的计数状态
> - **时间选择：Event Time** — GPS ping 可能因网络延迟到达较晚，用 event time 确保司机在正确的 5 分钟窗口里被计入（配合 watermark 处理迟到数据）。用 processing time 会把延迟到达的 ping 放入错误的窗口。
> 
> **需求 2：当日行程累计总数**
> 
> - **Window type：Agglomerative Window** — 从流的起点（当日开始）累积到当前时刻，无固定结束点
> - **Stateful** — 必须持续维护一个累计计数器，依赖所有历史事件
> - **时间选择：Event Time** — 确保行程按其实际完成时间归入当日统计，而不是被处理的时间（司机可能离线后批量上报行程）

---

**Q12.** You are designing the storage architecture for a large-scale analytics platform. The fact table has 500 columns and 10 billion rows. Most queries read 3–8 columns and aggregate across millions of rows. Explain: (1) why column store is preferred over row store for this workload, (2) which partitioning strategy you would choose and why, and (3) what replication configuration you would recommend and why. (8 marks)

> [!note]- Answer
> **1. Column Store vs Row Store**
> 
> 查询只读 3–8 列（共 500 列），column store 只从磁盘读取那几列，跳过其余 492–497 列，I/O 减少超过 98%。Row store 读任意列都要读整行。此外，列式存储同列数据类型相同，压缩率更高（如 run-length encoding 对低基数列效果显著），进一步减少存储和 I/O。代表格式：Parquet（文件格式）、BigQuery（云数仓）。
> 
> **2. 分区策略**
> 
> 推荐 **Range Partitioning（按时间范围）**，例如按月或按季度分区。
> 
> 理由：分析查询通常包含时间过滤（如"过去 3 个月"），range partitioning 使查询只扫描相关分区（partition pruning），大幅减少扫描量。如果还有高频的按 region 等值过滤，可以考虑 **二级 Hash Partitioning**（先 range 后 hash）。
> 
> Round-robin 均匀分布但不支持 pruning；Hash partitioning 对范围查询无效。
> 
> **3. Replication 配置**
> 
> 推荐 **Lazy Propagation + Primary Copy（单 Leader）**。
> 
> - **Lazy（异步）**：写入 primary 后立即返回，不等副本确认，写入延迟低。分析平台对短暂的读旧数据容忍度较高（AP 倾向）。
> - **Primary Copy**：所有写入走一个 leader，无写入冲突，无需冲突解决机制，简单可靠。
> - Replication Factor 建议 3：容忍 2 台节点故障，同时提升读并发（副本可承担读请求）。

---

**Q13.** Your company is deploying a real-time product recommendation system. The ML model uses features like "number of items viewed in the last 30 minutes" and "user's country of residence". Describe: (1) the problem that arises if features are computed separately in training and inference, (2) how a Feature Store solves this, and (3) which type of feature transformation (batch, streaming, or on-demand) is appropriate for each of the two features mentioned. (8 marks)

> [!note]- Answer
> **1. 问题：Training-Serving Skew**
> 
> 如果"过去 30 分钟浏览量"在训练时从数据仓库的每日 batch 快照计算，在推理时从实时流重新计算（时间窗口定义、数据源、边界处理方式可能不同），模型训练时学到的规律和推理时实际输入的 feature 分布会产生偏差，导致模型在生产中表现远低于离线评估结果。
> 
> **2. Feature Store 如何解决**
> 
> - **统一 feature 定义**：feature transformation 逻辑只写一次，存入 Feature Registry（带版本控制）
> - **Offline Storage**（S3/BigQuery）：存储历史 feature，训练时从这里取，保证和推理时用同一套逻辑产出的数据
> - **Online Storage**（Redis/DynamoDB）：存储预计算好的最新 feature，推理时毫秒级获取，低延迟
> - 两路都由同一 feature pipeline 产出，消除计算逻辑不一致
> 
> **3. Feature Transformation 类型**
> 
> | Feature | 类型 | 理由 |
> |---------|------|------|
> | 过去 30 分钟浏览量 | **Streaming**（流式） | 需要实时滑动窗口聚合，数据持续产生，必须用流处理引擎（Kafka + Flink）维护 |
> | 用户所在国家 | **Batch**（批量） | 用户国家信息变化极少，从数据仓库定期批量更新即可，无需实时计算 |

---

## Section C — Code Reading (8 marks)

**Q14.** Read the following PySpark code and answer the questions below.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count, window

spark = SparkSession.builder.appName("RideAnalysis").getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "ride-events") \
    .load()

from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

schema = StructType() \
    .add("ride_id", StringType()) \
    .add("driver_id", StringType()) \
    .add("city", StringType()) \
    .add("fare", DoubleType()) \
    .add("event_time", TimestampType())

rides = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
          .select("data.*") \
          .withWatermark("event_time", "3 minutes")

result = rides \
    .groupBy(window(col("event_time"), "10 minutes"), col("city")) \
    .agg(
        count("ride_id").alias("ride_count"),
        _sum("fare").alias("total_fare")
    )

query = result.writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

query.awaitTermination()
```

**(a)** This code reads from Kafka. What does `.option("subscribe", "ride-events")` specify, and what does the `value` field in the Kafka message contain? (2 marks)

> [!note]- Answer
> `.option("subscribe", "ride-events")` 指定订阅名为 `"ride-events"` 的 Kafka **Topic**，消费者会从该 Topic 的所有 Partition 读取消息。
> 
> Kafka 消息的 `value` 字段是消息的实际内容，默认是 **binary（字节流）**。这里用 `.cast("string")` 将其转为字符串，再用 `from_json()` 按定义的 schema 解析为结构化的列，提取出 `ride_id`、`driver_id` 等字段。

**(b)** What does `.withWatermark("event_time", "3 minutes")` do? What happens to events that arrive more than 3 minutes late? (2 marks)

> [!note]- Answer
> `.withWatermark("event_time", "3 minutes")` 设置一个 3 分钟的 watermark：系统声明"当前最大 event_time - 3 分钟"之前的窗口可以安全关闭并产出结果，同时等待最多 3 分钟的迟到事件。
> 
> 超过 3 分钟迟到的事件被视为 **late data**：Spark Structured Streaming 在 `update` 模式下会**丢弃**这些事件（它们对应的窗口已经被触发并清除状态）。如果需要保留 late data，需要改用 `append` 模式并配置 side output，或增大 watermark 时间。

**(c)** What window type is used in `window(col("event_time"), "10 minutes")`? What would change if it were written as `window(col("event_time"), "10 minutes", "2 minutes")`? (2 marks)

> [!note]- Answer
> `window(col("event_time"), "10 minutes")` 使用 **Tumbling Window**（滚动窗口）：固定 10 分钟，不重叠，每条记录只属于一个窗口。
> 
> 改为 `window(col("event_time"), "10 minutes", "2 minutes")` 则变为 **Sliding Window**（滑动窗口）：窗口大小仍是 10 分钟，但每 2 分钟滑动一次，窗口互相重叠。同一条记录可能同时属于多个窗口（最多 10/2 = 5 个），适合"过去 10 分钟内的实时统计，每 2 分钟更新"的场景。

**(d)** The output mode is `"update"`. What does this mean, and why can't `"complete"` mode be used efficiently with a watermark? (2 marks)

> [!note]- Answer
> **`"update"` 模式**：每次触发计算时，只输出自上次触发以来**发生变化**的行（新增或更新的聚合结果）。适合聚合查询，不会重复输出所有历史结果。
> 
> **`"complete"` 模式**：每次触发都输出**所有**聚合结果的完整快照。问题在于：当使用 watermark 时，Spark 会定期清除过期窗口的状态以控制内存使用。complete 模式要求保留所有历史状态才能输出完整结果，与 watermark 的状态清理机制冲突——要么内存无限增长，要么无法输出正确的 complete 结果。因此 watermark + complete 模式不兼容。
