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
> **B** — Unbounded data is a stream that keeps arriving indefinitely (e.g., IoT sensor feeds, live event logs). File size and schema are unrelated to the bounded/unbounded distinction.

---

**Q2.** An e-commerce platform must detect fraudulent transactions in real time, processing millions of events per second. Which system combination is most appropriate?

- A. PostgreSQL + Pandas
- B. MQTT + TimescaleDB
- C. Apache Kafka + Apache Flink
- D. MongoDB + Scrapy

> [!note]- Answer
> **C** — Kafka ingests and durably buffers high-throughput event streams; Flink performs low-latency stateful stream processing (pipelining, not micro-batching). PostgreSQL/Pandas cannot scale to millions of events/second in real time. MQTT is for lightweight IoT messaging. Scrapy is a web scraping tool.

---

**Q3.** Which statement correctly describes **Valid Time** and **Transaction Time**?

- A. Valid Time can only move forward; Transaction Time can move forward and backward
- B. Both can be modified freely in either direction
- C. Valid Time can be modified in either direction; Transaction Time can only move forward
- D. Both can only move forward

> [!note]- Answer
> **C** — **Valid Time** represents when a fact was true in the real world and can be corrected retroactively. **Transaction Time** records when data was entered into the database and is append-only — you cannot alter the past audit trail.

---

**Q4.** Which storage format is best suited for **OLAP aggregation queries**?

- A. Row Store
- B. Column Store
- C. Wide Column Store
- D. Document Store

> [!note]- Answer
> **B** — Column Store reads only the columns involved in a query (avoiding unnecessary I/O), enables better compression (homogeneous data per column), and supports parallel reads. Row Store is optimised for OLTP point queries that read entire rows.

---

**Q5.** What is Apache Kafka's message delivery semantic?

- A. At most once
- B. Exactly once
- C. At least once
- D. Best effort

> [!note]- Answer
> **C** — Kafka's default is **at least once** — messages are not lost, but a consumer may process the same message more than once if it crashes before committing its offset. MQTT QoS 0 is "at most once"; MQTT QoS 2 is "exactly once".

---

**Q6.** In the CAP theorem, a financial system that prioritises **consistency over availability** during a network partition is classified as:

- A. AP
- B. CA
- C. CP
- D. PA

> [!note]- Answer
> **C** — **CP** (Consistency + Partition Tolerance): the system stays consistent during a partition but may refuse to respond (sacrificing availability). Financial systems prefer CP because returning stale or conflicting data is unacceptable.

---

**Q7.** Which of the following is a **stateful** stream operation?

- A. Filtering records where temperature > 100
- B. Projecting only the `sensor_id` and `value` fields
- C. Computing the average reading over a 5-minute sliding window
- D. Converting timestamps from UTC to local time

> [!note]- Answer
> **C** — A windowed aggregation must maintain state (accumulate values) across multiple records. Filtering, projecting, and timestamp conversion are stateless — each record is processed independently with no memory of prior records.

---

**Q8.** What is the primary role of a **Watermark** in stream processing?

- A. To encrypt messages in transit
- B. To declare that all events with a timestamp earlier than T have arrived, triggering event-time windows
- C. To set the maximum allowed processing latency
- D. To partition the stream across multiple worker nodes

> [!note]- Answer
> **B** — A watermark is the stream processor's assertion: "I have seen all events up to time T." It allows the system to close and emit results for event-time windows without waiting forever for late-arriving data. Events arriving after the watermark are treated as "late data".

---

**Q9.** Which architecture uses **two parallel paths** — a batch layer for accuracy and a speed layer for low latency — merged in a serving layer?

- A. Kappa Architecture
- B. Lambda Architecture
- C. Star Schema
- D. Feature Store

> [!note]- Answer
> **B** — **Lambda Architecture** has a batch path (reprocesses all historical data for accurate results) and a speed/stream path (provides low-latency approximate results), combined at the serving layer. **Kappa Architecture** simplifies this to a single stream path.

---

**Q10.** In a Feature Store, what is the purpose of **Online Storage** (e.g., Redis)?

- A. To store raw training datasets for model experimentation
- B. To provide low-latency feature retrieval during real-time model inference
- C. To version-control feature transformation logic
- D. To detect feature drift over time

> [!note]- Answer
> **B** — Online Storage holds pre-computed features in a low-latency key-value store so they can be retrieved in milliseconds during real-time inference. Offline Storage (e.g., S3, BigQuery) holds historical features for model training, where latency is less critical.

---

## Section B — Short Answer (8 marks each, 56 marks total)

**Q11.** Compare **OLTP** and **OLAP** systems across four dimensions: read/write pattern, query type, typical users, and data volume. Give one real-world example for each. (8 marks)

> [!note]- Answer
> | Dimension | OLTP | OLAP |
> |-----------|------|------|
> | Read/write pattern | Frequent INSERT/UPDATE/DELETE on single rows; point queries by PK | Bulk ETL/ELT loads; large aggregation scans (SUM, COUNT, AVG) |
> | Query type | Short, predefined, low-latency transactions | Complex, ad-hoc analytical queries; may run for seconds or minutes |
> | Typical users | End users via web/mobile apps | Internal data analysts and BI tools |
> | Data volume | GB to TB (current operational state) | TB to PB (multi-year historical records) |
> 
> *OLTP example*: A bank's core system processing account transfers — each transfer is an immediate, atomic transaction.
> 
> *OLAP example*: A retail data warehouse where analysts query year-over-year sales growth by product category across all regions.

---

**Q12.** The following Python snippet cleans a dataset. Identify **three distinct data quality problems** present in the data and explain how each line addresses them. (8 marks)

```python
df['weight'] = df['weight'].replace(0, pd.NA)
df = df.dropna(subset=['patient_id'])
df['gender'] = df['gender'].str.upper().replace({'MALE': 'M', 'FEMALE': 'F'})
df['age'] = pd.to_numeric(df['age'], errors='coerce')
```

> [!note]- Answer
> | Line | Problem Type | Explanation |
> |------|-------------|-------------|
> | `replace(0, pd.NA)` | **Default** — 0 is a placeholder for missing weight, not a real value | Converts the sentinel 0 to a proper null so it is treated as missing |
> | `dropna(subset=['patient_id'])` | **Missing** — some rows have no patient ID, making them unidentifiable | Removes rows where the primary identifier is absent |
> | `.str.upper().replace(...)` | **Inconsistent** — gender encoded as `M`, `Male`, `MALE`, `F`, `Female`, etc. | Normalises all strings to uppercase, then maps variants to a single encoding |
> | `pd.to_numeric(..., errors='coerce')` | **Incorrect / non-numeric** — age column contains strings like `"N/A"` or `"unknown"` | Converts valid strings to numbers; non-parseable values become NaN |

---

**Q13.** The following HTML is returned by a web request. Write BeautifulSoup code to extract the text `"Sydney"` from it. Then explain what `pd.read_html()` does and when it is appropriate to use. (8 marks)

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
> **Extracting "Sydney"**:
> ```python
> from bs4 import BeautifulSoup
> content = BeautifulSoup(html, 'html5lib')
> 
> # Option 1 — navigate by tag
> table = content.find(id='results').find('table', 'data')
> city = table.find_all('tr')[1].find('td').text   # → "Sydney"
> 
> # Option 2 — CSS selector
> city = content.select('#results table.data tr:nth-child(2) td')[0].text
> ```
> 
> **`pd.read_html()`**: Takes an HTML string, parses all `<table>` elements, and returns a list of DataFrames (one per table), using the header row as column names.
> 
> **Appropriate when**: the target data is already in a well-structured `<table>` tag — avoids manual row/cell iteration.
> 
> **Not appropriate when**: the page has no `<table>` (data is in `<div>` or rendered by JavaScript), or when fine-grained cell-level cleaning is required before creating a DataFrame.

---

**Q14.** A company stores employee contract dates in a **bitemporal table**. Explain the difference between **Valid Time** and **Transaction Time**, why both are needed, and what `9999-12-31` represents in this context. (8 marks)

> [!note]- Answer
> **Valid Time**: the period during which a fact was true in the real world. It can be set to any past or future date — e.g., a salary increase agreed retroactively from three months ago would have a `valid_time_start` in the past.
> 
> **Transaction Time**: the period during which the database record existed in the system. Set automatically at insert/update time; can never be changed retroactively — it is the audit trail of when the system "knew" something.
> 
> **Why both are needed**:
> - Valid Time alone cannot answer "what did we believe at a specific point in time?" (you can't reconstruct a past database state).
> - Transaction Time alone cannot answer "when was this fact actually true in the real world?"
> - Together (**bitemporal**) they support queries like: "What salary did we have on record for this employee as of last Tuesday, for the period January 2024?"
> 
> **`9999-12-31` / `infinity`**: Represents "currently valid with no known end date." Since SQL date columns cannot store true infinity, this sentinel means "this record is still open / currently active."

---

**Q15.** A distributed database must choose between **CP** and **AP**. Explain the CAP theorem, describe what each configuration sacrifices, and give a concrete use case for each. (8 marks)

> [!note]- Answer
> **CAP Theorem**: A distributed system can guarantee at most **two** of the following three properties simultaneously:
> - **C**onsistency: every node returns the most recent, correct data
> - **A**vailability: every request receives a response (not necessarily the latest data)
> - **P**artition Tolerance: the system continues operating despite network partitions
> 
> Since network partitions are unavoidable in distributed systems, P is effectively always required. The real trade-off is between C and A:
> 
> | | CP | AP |
> |--|----|----|
> | Sacrifices | Availability — system may reject requests to avoid returning stale data | Consistency — system responds even if it might return outdated data |
> | Use case | **Financial systems** (banking) — returning an incorrect balance is unacceptable | **Social media** (Twitter likes) — a slightly stale count is acceptable; uptime is critical |

---

**Q16.** Compare **Apache Spark Streaming** and **Apache Flink** for stream processing. What is the fundamental architectural difference and its implication for latency? Also explain Spark's "lazy evaluation" and what triggers actual execution. (8 marks)

> [!note]- Answer
> | | Spark Streaming | Apache Flink |
> |--|-----------------|--------------|
> | Processing model | **Micro-batching** — stream is chopped into small time-based batches | **Pipelining** — records flow directly operator-to-operator as they arrive |
> | Stages | Separate sequential stages with synchronisation barriers | Overlapping — operators execute concurrently |
> | Latency | Milliseconds to seconds (bounded by batch interval) | Sub-millisecond to milliseconds (true streaming) |
> 
> **Latency implication**: Flink achieves lower, more consistent latency because records are never held up waiting for a batch to fill. Spark's micro-batching introduces a minimum latency equal to the batch interval.
> 
> **Lazy Evaluation in Spark**: Transformations (`.filter()`, `.map()`, `.select()`) build up a logical plan but do not execute immediately. Computation is only triggered when an **Action** is called — operations that must return a result or write output: `collect()`, `count()`, `show()`, `take(n)`, `write()`. This allows Spark's Catalyst optimiser to inspect the full plan and apply optimisations before any data is read.

---

**Q17.** Explain the **Lambda Architecture** and the **Kappa Architecture**. What problem does each solve, and what is the main limitation of Lambda that Kappa addresses? (8 marks)

> [!note]- Answer
> **Lambda Architecture**:
> - *Problem*: Combining high accuracy (historical batch reprocessing) with low latency (real-time stream results).
> - *Structure*: **Batch layer** (reprocesses all history for accurate results) + **Speed layer** (processes live stream for low-latency approximate results) + **Serving layer** (merges both).
> - *Main limitation*: The same business logic must be implemented **twice** — once in batch and once in stream. This duplication increases cost and risk of divergence between the two implementations.
> 
> **Kappa Architecture**:
> - *Problem*: The dual-codebase maintenance burden of Lambda.
> - *Structure*: A single stream processing pipeline handles both real-time and historical reprocessing. Historical reprocessing is done by **replaying the event log** (re-reading Kafka from offset 0) through the same stream code.
> - *Trade-off*: Slightly less flexibility for complex batch analytics that are easier to express in a batch paradigm.
> - *Key advantage*: One codebase, one processing model — simpler to develop, test, and maintain.

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
> `errors='coerce'` silently converts any value that cannot be parsed as a number into `NaN`, allowing the rest of the column to be processed normally.
> 
> With `errors='raise'`, `pd.to_numeric()` would raise a `ValueError` and halt execution as soon as it encounters a non-numeric string (e.g., `"unknown"` or `"N/A"`) in the column.

**(b)** What does `pd.cut()` do here? What `age_group` would a patient aged 35 receive? (2 marks)

> [!note]- Answer
> `pd.cut()` divides a continuous numeric column into discrete bins and assigns a label to each value. The bins `[0, 18, 40, 60, 120]` create four intervals: (0–18], (18–40], (40–60], (60–120].
> 
> A patient aged 35 falls in the (18–40] bin, so their `age_group` would be `'young_adult'`.

**(c)** What do the final three lines produce? What does `reset_index()` do here? (2 marks)

> [!note]- Answer
> `groupby('age_group')['bmi'].mean()` computes mean BMI per age group, producing a Series with `age_group` as the index. `reset_index()` converts that index back into a regular column, turning the result into a proper DataFrame. The columns are renamed `age_group` and `avg_bmi`. The output is a table showing average BMI for each of the four age groups.

**(d)** Why is `bmi` replaced with `np.nan` **before** the `groupby` instead of after? (2 marks)

> [!note]- Answer
> `groupby().mean()` automatically skips `NaN` values. If the placeholder `0` were left in place, it would be included in the average and artificially lower the mean BMI. Replacing it with `NaN` before aggregation ensures `0` is treated as missing (unknown) rather than a real BMI measurement.

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
> Retrieve the top 10 shipped orders with a total over $500, placed in either Sydney or Melbourne, ordered from highest to lowest total — returning only `customer_id`, `total`, and `region` (excluding the default `_id` field).

**(b)** What does `_id: 0` in the projection do? Why might you want this? (2 marks)

> [!note]- Answer
> `_id: 0` **excludes** the MongoDB document identifier from the results. By default MongoDB includes `_id` in every query result even when you specify a projection. Excluding it is useful when `_id` is an internal identifier with no meaning to the data consumer (e.g., the application only needs `customer_id`).

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
> `$in` tests whether a field's value matches any element in the array — semantically equivalent to the `$or` over two equality checks.

**(d)** How does this query differ from an equivalent SQL query in terms of schema enforcement? (2 marks)

> [!note]- Answer
> In SQL, the schema is enforced at write time (schema-on-write) — every row must conform to defined columns and types. In MongoDB (schema-on-read), documents in the collection may not all have a `region` field; documents missing `region` simply do not match the filter and are excluded without any error. This flexibility allows heterogeneous documents but means data quality depends on application-level enforcement, not the database itself.

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
> Spark uses **lazy evaluation**. Calling `.filter()`, `.groupBy()`, `.agg()`, and `.orderBy()` only builds a logical execution plan — no data is read or processed. Computation is only triggered when an **action** is called (`show()`, `collect()`, `count()`, `write()`, etc.). This allows Spark's Catalyst optimiser to inspect the entire plan and apply optimisations (e.g., predicate pushdown to the Parquet reader, column pruning) before any work begins.

**(b)** What is the advantage of reading from **Parquet** format compared to CSV for this query? (2 marks)

> [!note]- Answer
> Parquet is a **columnar storage format**. This query only uses four columns (`region`, `product_category`, `revenue`, `order_id`). Parquet allows Spark to read only those columns from disk, skipping all others. CSV is row-oriented — reading any column requires reading the entire row. This results in significantly less I/O and faster execution. Parquet also stores type metadata and supports efficient per-column compression.

**(c)** The second `.filter()` (`order_count > 1000`) is applied after `.agg()`. Why can't this filter be applied before the `groupBy`? (2 marks)

> [!note]- Answer
> `order_count` is a **derived column** produced by the aggregation (`count("order_id").alias("order_count")`). It does not exist in the raw data — it is computed per group. It cannot be referenced before the `groupBy`/`agg` step. This is equivalent to SQL's `HAVING` clause (filter on aggregated values) versus `WHERE` (filter on raw rows before aggregation).

**(d)** This code reads from S3. What storage layer does this represent, and what is one limitation for **real-time** analytics? (2 marks)

> [!note]- Answer
> S3 is an object store used as a **Data Lake** layer — storing raw or semi-processed data cheaply at scale without enforcing schema. The primary limitation for real-time analytics is **high latency**: S3 is optimised for batch reads of large files, not low-latency point queries. New data written to S3 is typically available only after a batch job completes (minutes, not milliseconds), making it unsuitable for sub-second real-time use cases that require a streaming system (Kafka + Flink) instead.
