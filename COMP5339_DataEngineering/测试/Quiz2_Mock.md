# COMP5339 — Tutorial Quiz 2 (Mock)

**Scope: Week 7 – Week 11**
**Quiz Writing Time: 30 minutes | Total: 10 marks**
**Closed book. No electronic devices permitted.**

---

## Part I — Multiple Choice Questions (1 mark each)

*Tick the box corresponding to the correct answer. Each question carries one mark.*

---

**Question 1A.** A government agency stores property ownership records. A court ruling on 2026-03-01 establishes that ownership transferred on 2025-06-01 (a backdated change). The agency must also be able to answer: *"What did our system record about this property as of 2026-01-15?"* Which data model supports **both** requirements?

- [ ] Valid Time only — records when facts were true in the real world
- [ ] Transaction Time only — records when data was entered into the system
- [ ] A single `updated_at` timestamp column
- [ ] A bitemporal table with both Valid Time and Transaction Time columns

> [!note]- Answer
> **Bitemporal table（双时态表）。**
> 
> - **Valid Time** 记录"事实在现实中成立的时间"——可以追溯修改（如把 ownership 的 valid_time_start 设为 2025-06-01）。
> - **Transaction Time** 记录"系统何时知道这件事"——append-only，不可追溯篡改，支持审计（"2026-01-15 当时系统记录了什么"）。
> - 只有 bitemporal 才能同时回答两类问题。单个 `updated_at` 或单一时间维度均不够。

---

**Question 1B.** A stream processing job computes website click counts using **event-time** windows of 1 minute. Some events arrive up to 45 seconds late due to network delay. Which mechanism allows the system to correctly close windows without waiting indefinitely?

- [ ] Increase the micro-batch interval to 2 minutes
- [ ] Switch from event time to processing time
- [ ] Configure a Watermark with an allowed lateness of 45 seconds
- [ ] Replace tumbling windows with session windows

> [!note]- Answer
> **Watermark with allowed lateness（水印 + 允许迟到时间）。**
> 
> Watermark 是流处理器的声明："截止时间 T，所有早于 T 的事件已到达。"设置 45 秒的 allowed lateness，系统会等待最多 45 秒后触发窗口，既不会无限期等待，也不会丢弃合理的迟到事件。
> 
> 切换到 processing time 会丢失事件的真实发生顺序；增大 batch interval 只影响 Spark 的 micro-batching，不解决 late data 问题。

---

**Question 1C.** An analytics team runs queries that read only 4 columns out of 180, scanning billions of rows. Which storage format minimises I/O for these queries?

- [ ] Row store (e.g., PostgreSQL heap files)
- [ ] Document store (e.g., MongoDB)
- [ ] Column store (e.g., Parquet / BigQuery)
- [ ] Wide Column store (e.g., HBase)

> [!note]- Answer
> **Column store（列式存储）。**
> 
> 列式存储按列组织数据，查询只涉及 4 列时，只需从磁盘读取这 4 列，其余 176 列完全不读。Row store 读任意列都要读整行；Document store 面向嵌套文档；Wide Column store（HBase）按 column family 分组存储，并非纯列式，不适合 OLAP 聚合扫描。

---

## Part II — Short Answer Questions

*Provide answers in the boxes provided below each question.*

---

**Scenario 1:** A ride-sharing company logs every GPS ping from drivers. Each ping is recorded as it arrives. Occasionally, a driver disputes a fare and the company needs to reconstruct *exactly where the system believed the driver was at a specific past time* — not just the corrected location, but what was on record at that moment. The system receives ~50,000 pings per second during peak hours.

**Question 2:** What temporal data model would you use, and why? How would you represent a record that is *currently valid with no known end date*? What storage approach would you recommend for handling 50,000 pings/second, and why? **(3 Marks)**

> [!note]- Answer
> **时态模型：Transaction Time table（或 Bitemporal table）**
> 
> 该场景的核心需求是"系统在某历史时刻记录的是什么"——这是 **Transaction Time** 的用途（记录数据进入系统的时间，append-only，支持审计回溯）。如果还需要追溯修改真实事件时间，则需要 **Bitemporal table**。
> 
> **表示"当前有效、无已知结束日期"：** 用哨兵值 `9999-12-31`（或 PostgreSQL 的 `'infinity'`）作为 `transaction_time_end`，表示该记录仍处于激活状态。查询当前有效记录用 `WHERE transaction_time_end = 'infinity'`。
> 
> **50,000 pings/second 的存储方案：Dedicated Time Series Database（如 TimescaleDB 或 InfluxDB）**
> - 专为高频时序数据设计，内置时间分区（按时间自动 chunk），压缩率高
> - 比通用 RDBMS 在时序写入和范围查询上性能好几个数量级
> - 若需要更高吞吐，可在前面加 Kafka 做缓冲，再批量写入 TSDB

---

**Scenario 2:** Your team's fraud detection model was trained on a feature called `tx_count_last_1h` (number of transactions by a user in the last hour). After deployment, model accuracy degrades. Investigation reveals that during training, this feature was computed from a data warehouse using a daily batch job, but during inference it is recomputed on the fly from a different data source using a slightly different time window definition.

**Question 3:** What is this problem called? What system would you introduce to solve it, and how does that system specifically address the root cause? **(2 Marks)**

> [!note]- Answer
> **问题名称：Training-Serving Skew（训练-推理偏差）**
> 
> 训练和推理阶段使用了不同的数据源和不同的 feature 计算逻辑，导致模型在训练时学到的规律与实际推理时输入的 feature 分布不一致，表现为线上准确率下降。
> 
> **解决方案：引入 Feature Store（特征存储）**
> 
> Feature Store 解决这个问题的方式：
> - **统一 feature 定义**：feature transformation 逻辑只写一次，存入 Feature Registry，训练和推理都调用同一套逻辑
> - **Offline Storage**（如 S3/BigQuery）：存储历史 feature，供模型训练使用
> - **Online Storage**（如 Redis）：存储预计算好的最新 feature，供实时推理低延迟获取
> - 两路都从同一 feature pipeline 产出，消除了 skew 的根本原因

---

**Scenario 3:** A data engineering team is building a real-time clickstream pipeline. The pipeline processes user events as they arrive. Below are four steps in the pipeline:

1. Filter events where `event_type = 'purchase'`
2. For each `user_id`, count the number of events within each non-overlapping 10-minute interval
3. Add a new field `ingest_time` set to the current system clock at the moment of processing
4. Compute the running total of `revenue` accumulated since the stream started (no fixed end point)

**Question 4:**
1. Classify each of the four steps as **stateless** or **stateful**. **(1 Mark)**
2. Identify the **window type** used in step 2 and step 4. **(1 Mark)**

> [!note]- Answer
> **1. Stateless vs Stateful 分类：**
> 
> | Step | 分类 | 原因 |
> |------|------|------|
> | 1. Filter `event_type = 'purchase'` | **Stateless** | 每条记录独立判断，不依赖其他记录的历史 |
> | 2. Count per user per 10-minute interval | **Stateful** | 需要在窗口内跨多条记录累积计数，必须维护状态 |
> | 3. Add `ingest_time` (system clock) | **Stateless** | 每条记录独立添加字段，不依赖任何历史状态 |
> | 4. Running total of revenue since stream start | **Stateful** | 需要从流开始就持续累积，跨越所有历史记录 |
> 
> **2. 窗口类型：**
> 
> - **Step 2**：**Tumbling Window（滚动窗口）** — 固定大小（10 分钟），不重叠，每个事件只属于一个窗口
> - **Step 4**：**Agglomerative Window（累积窗口）** — 从流的起点一直累积到当前时刻，没有固定结束点
