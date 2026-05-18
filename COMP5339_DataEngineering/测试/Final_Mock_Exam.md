# COMP5339 Data Engineering — Final Mock Exam

> **Format**: MCQ + Short Answer + Code Reading
> **Total marks**: 100 | **Suggested time**: 2 hours
> **Closed book. No AI tools permitted.**

---

## Section A — Multiple Choice (2 marks each, 20 marks total)

**Q1.** Which of the following best describes **unbounded data**?

- A. A dataset stored in a fixed-size file
- B. A continuously generated stream of data with no defined endpoint
- C. Any dataset larger than 1 TB
- D. Data that has no schema definition

> [!note]- Answer
> **B** — Unbounded data 是没有终点的持续数据流（如 IoT 传感器、实时日志）。数据大小和 schema 与 bounded/unbounded 的划分无关。

---

**Q2.** An e-commerce platform must detect fraudulent transactions in real time, processing millions of events per second. Which system combination is most appropriate?

- A. PostgreSQL + Pandas
- B. MQTT + TimescaleDB
- C. Apache Kafka + Apache Flink
- D. MongoDB + Scrapy

> [!note]- Answer
> **C** — Kafka 负责高吞吐量的事件流持久化缓冲；Flink 做低延迟有状态流处理（pipelining，非 micro-batching）。PostgreSQL/Pandas 无法扩展到每秒百万事件。MQTT 是轻量级 IoT 消息协议，不适合大规模欺诈检测。Scrapy 是爬虫工具。

---

**Q3.** Which statement correctly describes **Valid Time** and **Transaction Time**?

- A. Valid Time can only move forward; Transaction Time can move forward and backward
- B. Both can be modified freely in either direction
- C. Valid Time can be modified in either direction; Transaction Time can only move forward
- D. Both can only move forward

> [!note]- Answer
> **C** — **Valid Time** 表示事实在现实中成立的时间，可以向前或向后修改（如追溯调整工资）。**Transaction Time** 记录数据进入数据库的时间，只能向前（append-only），是不可篡改的审计轨迹。

---

**Q4.** Which storage format is best suited for **OLAP aggregation queries**?

- A. Row Store
- B. Column Store
- C. Wide Column Store
- D. Document Store

> [!note]- Answer
> **B** — Column Store 只读取查询涉及的列，避免无关 I/O；同列数据类型相同，压缩率更高；不同列可并行读取。Row Store 适合 OLTP 点查询（需要读取整行）。

---

**Q5.** What is Apache Kafka's message delivery semantic?

- A. At most once
- B. Exactly once
- C. At least once
- D. Best effort

> [!note]- Answer
> **C** — Kafka 默认语义是 **at least once**：消息不会丢失，但 consumer 崩溃后重启可能重复消费同一条消息。MQTT QoS 0 = at most once；MQTT QoS 2 = exactly once。

---

**Q6.** In the CAP theorem, a financial system that prioritises **consistency over availability** during a network partition is classified as:

- A. AP
- B. CA
- C. CP
- D. PA

> [!note]- Answer
> **C** — **CP**（Consistency + Partition Tolerance）：发生网络分区时，系统保持一致性，宁可拒绝请求也不返回可能过时的数据（牺牲 Availability）。金融系统不能接受错误余额，因此选 CP。

---

**Q7.** Which of the following is a **stateful** stream operation?

- A. Filtering records where temperature > 100
- B. Projecting only the `sensor_id` and `value` fields
- C. Computing the average reading over a 5-minute sliding window
- D. Converting timestamps from UTC to local time

> [!note]- Answer
> **C** — 窗口聚合需要跨多条记录维护状态（累积值）。过滤、投影、时间转换都是 stateless——每条记录独立处理，不依赖历史记录。

---

**Q8.** What is the primary role of a **Watermark** in stream processing?

- A. To encrypt messages in transit
- B. To declare that all events with a timestamp earlier than T have arrived, triggering event-time windows
- C. To set the maximum allowed processing latency
- D. To partition the stream across multiple worker nodes

> [!note]- Answer
> **B** — Watermark 是流处理器的声明："截止时间 T，所有早于 T 的事件已到达。"它用于触发基于 event time 的窗口计算，避免无限等待迟到数据。晚于 watermark 的事件被视为 late data，可丢弃或走 side output。

---

**Q9.** Which architecture uses **two parallel paths** — a batch layer for accuracy and a speed layer for low latency — merged in a serving layer?

- A. Kappa Architecture
- B. Lambda Architecture
- C. Star Schema
- D. Feature Store

> [!note]- Answer
> **B** — **Lambda Architecture** 有 batch path（重处理全量历史，结果精确）和 speed/stream path（实时处理，结果近似），在 serving layer 合并。**Kappa Architecture** 简化为只用一条流处理路径。

---

**Q10.** In a Feature Store, what is the purpose of **Online Storage** (e.g., Redis)?

- A. To store raw training datasets for model experimentation
- B. To provide low-latency feature retrieval during real-time model inference
- C. To version-control feature transformation logic
- D. To detect feature drift over time

> [!note]- Answer
> **B** — Online Storage（如 Redis、DynamoDB）以毫秒级延迟提供预计算好的 feature，用于实时推理（inference）。Offline Storage（如 S3、BigQuery）存储历史 feature，用于模型训练，对延迟要求不高。

---

## Section B — Short Answer (8 marks each, 56 marks total)

**Q11.** Compare **OLTP** and **OLAP** systems across four dimensions: read/write pattern, query type, typical users, and data volume. Give one real-world example for each. (8 marks)

> [!note]- Answer
> | 维度 | OLTP | OLAP |
> |------|------|------|
> | Read/write pattern | 频繁的单行 INSERT/UPDATE/DELETE；按 PK 点查询 | 批量 ETL/ELT 导入；大范围聚合扫描（SUM、COUNT、AVG） |
> | Query type | 短小、预定义、低延迟事务 | 复杂、临时性分析查询，可能运行数秒到数分钟 |
> | Typical users | 通过 Web/移动 App 的终端用户 | 内部数据分析师和 BI 工具 |
> | Data volume | GB 到 TB（当前运营数据） | TB 到 PB（多年历史记录） |
> 
> *OLTP 例*：银行核心系统处理转账——每笔转账是一个立即完成的原子事务。
> 
> *OLAP 例*：零售数仓——分析师查询各地区近三年各品类销售额同比增长。

---

**Q12.** The following Python snippet cleans a dataset. Identify **three distinct data quality problems** and explain how each line addresses them. (8 marks)

```python
df['weight'] = df['weight'].replace(0, pd.NA)
df = df.dropna(subset=['patient_id'])
df['gender'] = df['gender'].str.upper().replace({'MALE': 'M', 'FEMALE': 'F'})
df['age'] = pd.to_numeric(df['age'], errors='coerce')
```

> [!note]- Answer
> | 代码行 | 问题类型 | 说明 |
> |--------|---------|------|
> | `replace(0, pd.NA)` | **Default**（占位符）：0 代替了缺失的体重值 | 将哨兵值 0 转为真正的 null，便于后续按缺失值处理 |
> | `dropna(subset=['patient_id'])` | **Missing**（缺失）：部分行缺少主键标识符 | 删除无法识别身份的行，同时不影响其他列有 NaN 的行 |
> | `.str.upper().replace(...)` | **Inconsistent**（不一致）：`M`、`Male`、`MALE`、`F` 混用 | 先全部转大写，再统一映射为单一编码（`M`/`F`） |
> | `pd.to_numeric(..., errors='coerce')` | **Incorrect / non-numeric**：age 列含 `"N/A"`、`"unknown"` 等字符串 | 可解析的转为数字，无法解析的转为 NaN 而不抛出异常 |

---

**Q13.** The following HTML is returned by a web request. Write BeautifulSoup code to extract `"Sydney"`. Then explain what `pd.read_html()` does and when it is appropriate to use. (8 marks)

```html
<div id="results">
  <table class="data">
    <tr><th>City</th><th>Population</th></tr>
    <tr><td>Sydney</td><td>5300000</td></tr>
    <tr><td>Melbourne</td><td>5000000</td></tr>
  </table>
</div>
```

> [!note]- Answer
> **提取 "Sydney"**：
> ```python
> from bs4 import BeautifulSoup
> content = BeautifulSoup(html, 'html5lib')
> 
> # 方式一：按标签导航
> table = content.find(id='results').find('table', 'data')
> city = table.find_all('tr')[1].find('td').text   # → "Sydney"
> 
> # 方式二：CSS selector
> city = content.select('#results table.data tr:nth-child(2) td')[0].text
> ```
> 
> **`pd.read_html()`**：接收 HTML 字符串，解析其中所有 `<table>` 元素，返回 DataFrame 列表（每张表对应一个 DataFrame），用表头行作为列名。
> 
> **适合用的情况**：目标数据已经在结构良好的 `<table>` 标签里，可以避免手动遍历行和单元格。
> 
> **不适合用的情况**：页面没有 `<table>`（数据在 `<div>` 里或由 JavaScript 渲染），或需要在构建 DataFrame 之前对单元格进行精细清洗。

---

**Q14.** A company stores employee contract dates in a **bitemporal table**. Explain the difference between **Valid Time** and **Transaction Time**, why both are needed, and what `9999-12-31` represents in this context. (8 marks)

> [!note]- Answer
> **Valid Time**：事实在现实世界中成立的时间段。可以追溯修改——例如三个月前谈好的薪资调整，`valid_time_start` 可以设为过去的日期。
> 
> **Transaction Time**：数据库记录存在于系统中的时间段。由数据库自动设置，不可追溯修改——是系统"何时知道某件事"的审计轨迹。
> 
> **为什么两者都需要**：
> - 只有 Valid Time：无法回答"系统在某个历史时刻记录的是什么？"（无法重建过去某时刻的数据库状态）
> - 只有 Transaction Time：无法回答"这个事实在现实中什么时候成立？"
> - **Bitemporal** 结合两者，可以回答："截止上周二，我们系统记录的 2024 年 1 月该员工的薪资是多少？"
> 
> **`9999-12-31` / `infinity`**：表示"当前有效，无已知结束日期"。因为 SQL date 列无法存储真正的无穷大，用这个哨兵值表示记录仍然处于开放/激活状态，便于用 `WHERE valid_time_end = 'infinity'` 查询所有当前有效记录。

---

**Q15.** A distributed database must choose between **CP** and **AP**. Explain the CAP theorem, describe what each configuration sacrifices, and give a concrete use case for each. (8 marks)

> [!note]- Answer
> **CAP 定理**：分布式系统最多同时满足以下三个属性中的**两个**：
> - **C**onsistency：所有节点返回最新、正确的数据
> - **A**vailability：系统始终响应请求（不一定是最新数据）
> - **P**artition Tolerance：网络分区时系统仍能继续运行
> 
> 由于网络分区在分布式系统中不可避免，P 实际上必须保留。真正的取舍在 C 和 A 之间：
> 
> | | CP | AP |
> |--|----|----|
> | 牺牲 | Availability——分区期间宁可拒绝请求也不返回可能过时的数据 | Consistency——系统继续响应，但可能返回旧数据 |
> | 适用场景 | **金融系统**（银行、股票交易）——返回错误余额不可接受 | **社交媒体**（Twitter 点赞数）——短暂的数据不一致可以接受，服务可用性更重要 |

---

**Q16.** Compare **Apache Spark Streaming** and **Apache Flink** for stream processing. What is the fundamental architectural difference and its implication for latency? Also explain Spark's "lazy evaluation" and what triggers actual execution. (8 marks)

> [!note]- Answer
> | | Spark Streaming | Apache Flink |
> |--|-----------------|--------------|
> | 处理模型 | **Micro-batching**：流被切成小时间批次，每批作为 mini-batch 处理 | **Pipelining**：每条记录到达后立即在算子间传递，无批次边界 |
> | Stage 结构 | 分离的 Stage，有同步屏障 | 算子重叠并发执行 |
> | 延迟 | 毫秒到秒级（受 batch interval 限制） | 亚毫秒到毫秒级（真正的流处理） |
> 
> **延迟含义**：Flink 延迟更低且更稳定，因为记录不需要等待一个批次填满。Spark 的 micro-batching 引入了至少等于 batch interval 的最低延迟。
> 
> **Spark Lazy Evaluation**：Transformation（`.filter()`、`.map()`、`.select()`）只是构建逻辑执行计划，不触发计算。只有调用 **Action** 时才真正执行：`collect()`、`count()`、`show()`、`take(n)`、`write()`。这样 Catalyst 优化器可以在执行前看到完整计划，应用 predicate pushdown、列裁剪等优化。

---

**Q17.** Explain the **Lambda Architecture** and the **Kappa Architecture**. What problem does each solve, and what is the main limitation of Lambda that Kappa addresses? (8 marks)

> [!note]- Answer
> **Lambda Architecture**：
> - 解决的问题：同时需要高准确性（历史批处理重算）和低延迟（实时流结果）。
> - 结构：**Batch layer**（重处理全量历史，结果精确）+ **Speed layer**（实时流处理，低延迟近似）+ **Serving layer**（合并两路结果）。
> - 主要局限：同样的业务逻辑需要**实现两遍**——一套批处理代码，一套流处理代码。维护成本高，两套实现容易出现逻辑偏差。
> 
> **Kappa Architecture**：
> - 解决的问题：Lambda 的双重代码库维护负担。
> - 结构：只用一条流处理 pipeline，历史重处理通过**回放事件日志**（从 Kafka offset 0 重读）复用同一套流处理代码实现。
> - 取舍：对某些更适合批处理范式的复杂分析（如大规模 shuffle、迭代算法）灵活性略低。
> - 核心优势：一套代码，一种处理模型——更易开发、测试和维护。

---

## Section C — Code Reading (8 marks each, 24 marks total)

**Q18.** Read the following Pandas code and answer the questions.

```python
import pandas as pd
import numpy as np

df = pd.read_csv('patients.csv')

df['bmi'] = df['bmi'].replace(0, np.nan)
df['age'] = pd.to_numeric(df['age'], errors='coerce')
df = df.dropna(subset=['patient_id', 'age'])

df['age_group'] = pd.cut(df['age'],
                          bins=[0, 18, 40, 60, 120],
                          labels=['child', 'young_adult', 'middle_aged', 'senior'])

result = df.groupby('age_group')['bmi'].mean().reset_index()
result.columns = ['age_group', 'avg_bmi']
print(result)
```

**(a)** What does `errors='coerce'` do? What would happen with `errors='raise'`? (2 marks)

> [!note]- Answer
> `errors='coerce'`：无法解析为数字的值静默转为 `NaN`，其余正常处理。
> 
> `errors='raise'`：一旦遇到不能解析的字符串（如 `"unknown"`、`"N/A"`），立即抛出 `ValueError` 终止执行。

**(b)** What does `pd.cut()` do here? What `age_group` would a patient aged 35 receive? (2 marks)

> [!note]- Answer
> `pd.cut()` 将连续数值列切分为离散区间，并为每个值打上对应的标签。bins `[0, 18, 40, 60, 120]` 产生四个区间：(0–18]、(18–40]、(40–60]、(60–120]。
> 
> 年龄 35 落在 (18–40] 区间，`age_group` 为 `'young_adult'`。

**(c)** What do the final three lines produce? What does `reset_index()` do here? (2 marks)

> [!note]- Answer
> `groupby('age_group')['bmi'].mean()` 计算每个年龄组的平均 BMI，结果是以 `age_group` 为 index 的 Series。`reset_index()` 将 index 转回普通列，变成标准 DataFrame。最终输出是一张包含四个年龄组平均 BMI 的表格。

**(d)** Why is `bmi` replaced with `np.nan` **before** the `groupby` instead of after? (2 marks)

> [!note]- Answer
> `groupby().mean()` 自动跳过 `NaN`。如果占位符 `0` 没有被替换，它会被计入平均值，人为拉低每组的 BMI 均值。在聚合前替换为 `NaN`，确保 `0` 被当作"未知"而非真实体重数据处理。

---

**Q19.** Read the following MongoDB query and answer the questions.

```javascript
db.orders.find(
  {
    status: "shipped",
    total: { $gt: 500 },
    $or: [
      { region: "Sydney" },
      { region: "Melbourne" }
    ]
  },
  { customer_id: 1, total: 1, region: 1, _id: 0 }
).sort({ total: -1 }).limit(10)
```

**(a)** Describe in plain English what this query retrieves. (2 marks)

> [!note]- Answer
> 查找 Sydney 或 Melbourne 地区、状态为 shipped、订单金额超过 500 的订单，按金额从高到低排序，返回前 10 条，只显示 `customer_id`、`total`、`region` 三个字段（不含 `_id`）。

**(b)** What does `_id: 0` in the projection do? Why might you want this? (2 marks)

> [!note]- Answer
> `_id: 0` **排除** MongoDB 文档的内部标识符字段。默认情况下 MongoDB 即使在 projection 中也会返回 `_id`。当 `_id` 只是数据库内部 ID，对数据消费方没有意义时（例如应用层只需要 `customer_id`），排除它可以使结果更整洁。

**(c)** Rewrite the `$or` condition using the `$in` operator. (2 marks)

> [!note]- Answer
> ```javascript
> db.orders.find(
>   {
>     status: "shipped",
>     total: { $gt: 500 },
>     region: { $in: ["Sydney", "Melbourne"] }
>   },
>   { customer_id: 1, total: 1, region: 1, _id: 0 }
> ).sort({ total: -1 }).limit(10)
> ```
> `$in` 检查字段值是否属于数组中的任一元素，语义上等价于对两个等值条件做 `$or`，写法更简洁。

**(d)** How does this query differ from an equivalent SQL query in terms of schema enforcement? (2 marks)

> [!note]- Answer
> SQL 在写入时强制 schema（schema-on-write）——每行必须符合预定义的列和类型，不存在的列会报错。MongoDB 是 schema-on-read——`orders` 集合中的文档不一定都有 `region` 字段，缺少该字段的文档只是不匹配过滤条件，不会报错。灵活性更高，但数据质量依赖应用层保证，而非数据库本身。

---

**Q20.** Read the following PySpark code and answer the questions.

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

spark = SparkSession.builder.appName("SalesAnalysis").getOrCreate()

df = spark.read.parquet("s3://data-lake/sales/2025/")

result = (
    df.filter(col("region") == "Asia")
      .groupBy("product_category")
      .agg(
          avg("revenue").alias("avg_revenue"),
          count("order_id").alias("order_count")
      )
      .filter(col("order_count") > 1000)
      .orderBy(col("avg_revenue").desc())
)

result.show(20)
```

**(a)** Why does Spark not execute any computation until `result.show(20)` is called? What is this behaviour called? (2 marks)

> [!note]- Answer
> Spark 使用 **lazy evaluation（惰性求值）**。`.filter()`、`.groupBy()`、`.agg()`、`.orderBy()` 只构建逻辑执行计划，不读取或处理数据。只有调用 **Action**（如 `show()`、`collect()`、`count()`、`write()`）时才真正触发计算。这样 Catalyst 优化器可以在执行前看到完整计划，应用 predicate pushdown、列裁剪等优化。

**(b)** What is the advantage of reading from **Parquet** format compared to CSV for this query? (2 marks)

> [!note]- Answer
> Parquet 是**列式存储格式**。这个查询只用到 `region`、`product_category`、`revenue`、`order_id` 四列，Parquet 允许 Spark 只读这四列，跳过其余所有列。CSV 是行式存储，读任意列都要读整行。因此 Parquet 大幅减少 I/O，查询速度更快。此外 Parquet 还存储类型元数据，支持高效的按列压缩。

**(c)** The second `.filter()` (`order_count > 1000`) is applied after `.agg()`. Why can't this filter be applied before the `groupBy`? (2 marks)

> [!note]- Answer
> `order_count` 是由聚合（`count("order_id").alias("order_count")`）产生的**派生列**，在原始数据中不存在，必须先执行 `groupBy`/`agg` 才能得到。这等价于 SQL 中的 `HAVING` 子句（对聚合结果过滤），而非 `WHERE`（对原始行过滤）。

**(d)** This code reads from S3. What storage layer does this represent, and what is one limitation for **real-time** analytics? (2 marks)

> [!note]- Answer
> S3 是对象存储，作为 **Data Lake** 层使用——廉价地大规模存储原始或半处理数据，不强制 schema。对实时分析的主要局限是**高延迟**：S3 针对大文件的批量读取优化，不适合低延迟点查询。新写入 S3 的数据通常需要等批处理任务完成后才可用（分钟级），不满足亚秒级实时需求，后者需要 Kafka + Flink 这样的流处理系统。
