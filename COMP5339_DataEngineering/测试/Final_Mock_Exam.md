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

<details>
<summary>Answer</summary>

**B** — Unbounded data is a stream that keeps arriving indefinitely (e.g., IoT sensor feeds, live event logs). File size and schema are unrelated to the bounded/unbounded distinction.

</details>

---

**Q2.** An e-commerce platform must detect fraudulent transactions in real time, processing millions of events per second. Which system combination is most appropriate?

- A. PostgreSQL + Pandas
- B. MQTT + TimescaleDB
- C. Apache Kafka + Apache Flink
- D. MongoDB + Scrapy

<details>
<summary>Answer</summary>

**C** — Kafka ingests and durably buffers high-throughput event streams; Flink performs low-latency, stateful stream processing (pipelining, not micro-batching). PostgreSQL/Pandas cannot scale to millions of events/second in real time. MQTT is for lightweight IoT messaging, not high-throughput fraud detection. Scrapy is a web scraping tool.

</details>

---

**Q3.** Which statement correctly describes **Valid Time** and **Transaction Time**?

- A. Valid Time can only move forward; Transaction Time can move forward and backward
- B. Both can be modified freely in either direction
- C. Valid Time can be modified in either direction; Transaction Time can only move forward
- D. Both can only move forward

<details>
<summary>Answer</summary>

**C** — **Valid Time** represents when a fact was true in the real world and can be corrected retroactively (e.g., back-dating a salary change). **Transaction Time** records when data was entered into the database and is append-only — you cannot alter the past audit trail.

</details>

---

**Q4.** Which storage format is best suited for **OLAP aggregation queries**?

- A. Row Store
- B. Column Store
- C. Wide Column Store
- D. Document Store

<details>
<summary>Answer</summary>

**B** — Column Store reads only the columns involved in a query (avoiding unnecessary I/O), enables better compression (homogeneous data per column), and supports parallel reads across columns. Row Store is optimised for OLTP point queries that read entire rows.

</details>

---

**Q5.** What is Apache Kafka's message delivery semantic?

- A. At most once
- B. Exactly once
- C. At least once
- D. Best effort

<details>
<summary>Answer</summary>

**C** — Kafka's default delivery semantic is **at least once** — messages are not lost, but a consumer may process the same message more than once if it crashes before committing its offset. MQTT QoS 0 is "at most once"; MQTT QoS 2 is "exactly once".

</details>

---

**Q6.** In the CAP theorem, a financial system that prioritises **consistency over availability** during a network partition is classified as:

- A. AP
- B. CA
- C. CP
- D. PA

<details>
<summary>Answer</summary>

**C** — **CP** (Consistency + Partition Tolerance): the system stays consistent during a partition but may refuse to respond (sacrificing availability). Financial systems prefer CP because returning stale or conflicting balances is unacceptable.

</details>

---

**Q7.** Which of the following is a **stateful** stream operation?

- A. Filtering records where temperature > 100
- B. Projecting only the `sensor_id` and `value` fields
- C. Computing the average reading over a 5-minute sliding window
- D. Converting timestamps from UTC to local time

<details>
<summary>Answer</summary>

**C** — A windowed aggregation must maintain state (accumulate values) across multiple records. Filtering, projecting, and timestamp conversion are stateless — each record is processed independently with no memory of prior records.

</details>

---

**Q8.** What is the primary role of a **Watermark** in stream processing?

- A. To encrypt messages in transit
- B. To declare that all events with a timestamp earlier than T have arrived, triggering event-time windows
- C. To set the maximum allowed processing latency
- D. To partition the stream across multiple worker nodes

<details>
<summary>Answer</summary>

**B** — A watermark is the stream processor's assertion: "I have seen all events up to time T." It allows the system to close and emit results for event-time windows without waiting forever for late-arriving data. Events arriving after the watermark are treated as "late data".

</details>

---

**Q9.** Which architecture uses **two parallel paths** — a batch layer for accuracy and a speed layer for low latency — that are merged in a serving layer?

- A. Kappa Architecture
- B. Lambda Architecture
- C. Star Schema
- D. Feature Store

<details>
<summary>Answer</summary>

**B** — **Lambda Architecture** has a batch path (reprocesses all historical data for accurate results) and a speed/stream path (provides low-latency approximate results), combined at the serving layer. **Kappa Architecture** simplifies this to a single stream path.

</details>

---

**Q10.** In a Feature Store, what is the purpose of **Online Storage** (e.g., Redis)?

- A. To store raw training datasets for model experimentation
- B. To provide low-latency feature retrieval during real-time model inference
- C. To version-control feature transformation logic
- D. To detect feature drift over time

<details>
<summary>Answer</summary>

**B** — Online Storage holds pre-computed features in a low-latency key-value store so they can be retrieved in milliseconds during real-time inference (prediction serving). Offline Storage (e.g., S3, BigQuery) holds historical features for model training, where latency is less critical.

</details>

---

## Section B — Short Answer (8 marks each, 56 marks total)

**Q11.** Compare **OLTP** and **OLAP** systems across the following four dimensions: read/write pattern, query type, typical users, and data volume. Give one real-world example for each. (8 marks)

<details>
<summary>Answer</summary>

| Dimension | OLTP | OLAP |
|-----------|------|------|
| Read/write pattern | Frequent INSERT/UPDATE/DELETE on single rows; point queries by primary key | Bulk ETL/ELT loads; large aggregation scans (SUM, COUNT, AVG over millions of rows) |
| Query type | Short, predefined, low-latency transactions | Complex, ad-hoc analytical queries that may run for seconds or minutes |
| Typical users | End users via web/mobile applications | Internal data analysts and business intelligence tools |
| Data volume | GB to TB (current operational state) | TB to PB (multi-year historical records) |

*OLTP example*: A bank's core banking system processing account transfers — each transfer is an immediate, atomic transaction.

*OLAP example*: A retail data warehouse where analysts query year-over-year sales growth by product category across all regions.

</details>

---

**Q12.** The following Python snippet is used to clean a dataset. Identify **three distinct data quality problems** present in the data and explain how each line of code addresses them. (8 marks)

```python
df['weight'] = df['weight'].replace(0, pd.NA)
df = df.dropna(subset=['patient_id'])
df['gender'] = df['gender'].str.upper().replace({'MALE': 'M', 'FEMALE': 'F'})
df['age'] = pd.to_numeric(df['age'], errors='coerce')
```

<details>
<summary>Answer</summary>

| Line | Problem Type | Explanation |
|------|-------------|-------------|
| `replace(0, pd.NA)` | **Default value** — 0 is used as a placeholder for missing weight, which is medically impossible | Converts the sentinel 0 to a proper null (pd.NA) so it can be handled as missing |
| `dropna(subset=['patient_id'])` | **Missing value** — some rows have no patient ID, making them unidentifiable | Removes rows where the primary identifier is absent; retains rows with NaN in other columns |
| `.str.upper().replace(...)` | **Inconsistency** — gender is encoded as `M`, `Male`, `MALE`, `F`, `Female`, etc. | Normalises all strings to uppercase first, then maps all variants to a single canonical encoding (`M` / `F`) |
| `pd.to_numeric(..., errors='coerce')` | **Incorrect / non-numeric value** — age column may contain strings like `"N/A"` or `"unknown"` | Converts valid strings to numbers; non-parseable values become NaN (coerce) rather than raising an error |

</details>

---

**Q13.** The following HTML is returned by a web request. Write the BeautifulSoup code (using `find` / `find_all` / `select`) to extract the text `"Sydney"` from it. Then explain what `pd.read_html()` does and when it is appropriate to use. (8 marks)

```html
<div id="results">
  <table class="data">
    <tr><th>City</th><th>Population</th></tr>
    <tr><td>Sydney</td><td>5300000</td></tr>
    <tr><td>Melbourne</td><td>5000000</td></tr>
  </table>
</div>
```

<details>
<summary>Answer</summary>

**Extracting "Sydney"**:

```python
from bs4 import BeautifulSoup

content = BeautifulSoup(html, 'html5lib')

# Option 1 — navigate by tag
table = content.find(id='results').find('table', 'data')
first_data_row = table.find_all('tr')[1]   # skip header row
city = first_data_row.find('td').text      # → "Sydney"

# Option 2 — CSS selector
city = content.select('#results table.data tr:nth-child(2) td')[0].text
```

**`pd.read_html()`**:
- Takes an HTML string and parses all `<table>` elements, returning a list of DataFrames.
- Each table becomes one DataFrame, with the header row used as column names.
- **Appropriate when**: the target data is already in a well-structured `<table>` tag; avoids manual row/cell iteration.
- **Not appropriate when**: the page has no `<table>` (data is in `<div>` or JavaScript), or when fine-grained cleaning of individual cells is required before creating a DataFrame.

</details>

---

**Q14.** A company stores employee contract dates in a **bitemporal table**. Explain the difference between **Valid Time** and **Transaction Time**, why both are needed, and what `9999-12-31` (or `infinity`) represents in this context. (8 marks)

<details>
<summary>Answer</summary>

**Valid Time**: the period during which a fact was true in the real world. It can be set to any past or future date — for example, a salary increase agreed retroactively from three months ago would have a valid_time_start in the past.

**Transaction Time**: the period during which the database record existed in the system. It is set automatically by the database at insert/update time and can never be changed retroactively — it represents the audit trail of when the system "knew" something.

**Why both are needed**:
- Valid Time alone cannot answer "what did we believe at a specific point in time?" (you can't reconstruct a past database state).
- Transaction Time alone cannot answer "when was this fact actually true in the real world?" (only tells you when data was entered).
- Together (**bitemporal**), they support queries like: "What salary did we have on record for this employee as of last Tuesday, for the period January 2024?"

**`9999-12-31` / `infinity`**: represents "currently valid with no known end date". Since SQL date columns cannot store true infinity, this sentinel value means "this record is still open / currently active". It allows range-based queries (`WHERE valid_time_end = 'infinity'`) to retrieve all currently valid records efficiently.

</details>

---

**Q15.** A distributed database must decide between a **CP** and an **AP** configuration. Explain the CAP theorem, describe what each configuration sacrifices, and give a concrete use case for each. (8 marks)

<details>
<summary>Answer</summary>

**CAP Theorem**: A distributed system can guarantee at most **two** of the following three properties simultaneously:
- **C**onsistency: every node returns the most recent, correct data
- **A**vailability: every request receives a response (not necessarily the latest data)
- **P**artition Tolerance: the system continues operating despite network partitions (dropped messages between nodes)

Since network partitions are unavoidable in distributed systems, P is effectively always required. The real trade-off is between C and A:

| | CP | AP |
|--|----|----|
| Sacrifices | Availability — the system may reject requests to avoid returning stale data | Consistency — the system responds even if it might return outdated data |
| Behaviour during partition | Some nodes refuse requests until consistency is restored | All nodes continue responding, potentially with stale values |
| Use case | **Financial systems** (banking, stock trading) — returning an incorrect balance is unacceptable, so it is better to refuse the request | **Social media platforms** (Twitter, Facebook likes) — a slightly stale count is acceptable; it is more important that the service stays up |

</details>

---

**Q16.** Compare **Apache Spark Streaming** and **Apache Flink** for stream processing. What is the fundamental architectural difference between them, and what does that mean for latency? Also explain what "lazy evaluation" means in Spark and what triggers actual execution. (8 marks)

<details>
<summary>Answer</summary>

**Architectural difference**:

| | Spark Streaming | Apache Flink |
|--|-----------------|--------------|
| Processing model | **Micro-batching** — incoming stream is chopped into small time-based batches; each batch is processed as a mini-batch job | **Pipelining** — each record flows directly from one operator to the next as soon as it arrives; no batching boundary |
| Stages | Separate, sequential stages with synchronisation barriers | Overlapping — operators execute concurrently and pass records immediately |
| Latency | Milliseconds to seconds (bounded by batch interval) | Sub-millisecond to milliseconds (true streaming) |

**Latency implication**: Flink achieves lower and more consistent latency because records are never held up waiting for a batch to fill. Spark's micro-batching introduces a minimum latency equal to the batch interval.

**Lazy Evaluation in Spark**:
- Transformations (e.g., `filter()`, `map()`, `select()`) build up a **logical plan** but do not execute immediately.
- Actual computation is only triggered when an **Action** is called — operations that must return a result or write output:
  - `collect()`, `count()`, `show()`, `take(n)`, `write()`, `save()`
- This allows Spark's optimiser (Catalyst) to inspect the full computation graph and apply optimisations (predicate pushdown, column pruning, join reordering) before any data is read.

</details>

---

**Q17.** Explain the **Lambda Architecture** and the **Kappa Architecture**. What problem does each solve, and what is the main limitation of Lambda that Kappa addresses? (8 marks)

<details>
<summary>Answer</summary>

**Lambda Architecture**:
- **Problem it solves**: Combining high accuracy (historical batch reprocessing) with low latency (real-time stream results).
- **Structure**:
  - **Batch layer**: periodically reprocesses all historical data to produce accurate, complete views (high latency, high accuracy)
  - **Speed layer**: processes the live stream in real time to fill the gap since the last batch run (low latency, approximate)
  - **Serving layer**: merges results from both layers for queries
- **Main limitation**: The same business logic must be implemented and maintained **twice** — once in the batch system and once in the stream system. This duplication increases development cost and the risk of divergence between the two implementations.

**Kappa Architecture**:
- **Problem it solves**: The dual-codebase maintenance burden of Lambda.
- **Structure**: A single stream processing pipeline handles both real-time processing and historical reprocessing. Historical reprocessing is done by **replaying the event log** (e.g., re-reading Kafka from offset 0) through the same stream processing code.
- **Trade-off**: Slightly less flexibility for complex batch analytics that are easier to express in a batch paradigm (e.g., large shuffles, iterative algorithms).
- **Key advantage**: One codebase, one processing model — simpler to develop, test, and maintain.

</details>

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

**(a)** What does `errors='coerce'` do in `pd.to_numeric()`? What would happen if `errors='raise'` were used instead? (2 marks)

<details>
<summary>Answer</summary>

`errors='coerce'` silently converts any value that cannot be parsed as a number into `NaN`, allowing the rest of the column to be processed normally.

With `errors='raise'`, `pd.to_numeric()` would raise a `ValueError` and halt execution as soon as it encounters a non-numeric string (e.g., `"unknown"` or `"N/A"`) in the column.

</details>

**(b)** What does `pd.cut()` do here? What would the `age_group` value be for a patient aged 35? (2 marks)

<details>
<summary>Answer</summary>

`pd.cut()` divides a continuous numeric column into discrete bins and assigns a label to each value. The bins `[0, 18, 40, 60, 120]` create four intervals: (0–18], (18–40], (40–60], (60–120].

A patient aged 35 falls in the (18–40] bin, so their `age_group` would be `'young_adult'`.

</details>

**(c)** Describe what the final three lines produce. What does `reset_index()` do here? (2 marks)

<details>
<summary>Answer</summary>

`groupby('age_group')['bmi'].mean()` computes the mean BMI for each age group, producing a Series with `age_group` as the index. `reset_index()` converts that index back into a regular column, turning the result into a proper DataFrame. The columns are then renamed `age_group` and `avg_bmi`. The final output is a table showing the average BMI for each of the four age groups.

</details>

**(d)** Why is `bmi` replaced with `np.nan` before the `groupby` instead of after? (2 marks)

<details>
<summary>Answer</summary>

`groupby().mean()` automatically skips `NaN` values when computing the mean. If the placeholder `0` were left in place, it would be included in the average calculation and artificially lower the mean BMI for that group. Replacing it with `NaN` before aggregation ensures `0` is treated as missing (unknown) rather than as a real BMI measurement.

</details>

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

<details>
<summary>Answer</summary>

Retrieve the top 10 shipped orders with a total over $500, placed in either Sydney or Melbourne, ordered from highest to lowest total — returning only the `customer_id`, `total`, and `region` fields (excluding the default `_id` field).

</details>

**(b)** What does `_id: 0` in the projection do? Why might you want this? (2 marks)

<details>
<summary>Answer</summary>

`_id: 0` **excludes** the MongoDB document identifier field from the results. By default MongoDB includes `_id` in every query result even when you specify a projection. Excluding it is useful when the `_id` is an internal database identifier that has no meaning to the consumer of the data (e.g., the application only needs `customer_id`).

</details>

**(c)** Rewrite the `$or` condition as an equivalent MongoDB query using the `$in` operator. (2 marks)

<details>
<summary>Answer</summary>

```javascript
db.orders.find(
  {
    status: "shipped",
    total: { $gt: 500 },
    region: { $in: ["Sydney", "Melbourne"] }
  },
  { customer_id: 1, total: 1, region: 1, _id: 0 }
).sort({ total: -1 }).limit(10)
```

`$in` tests whether a field's value matches any element in the provided array — semantically equivalent to the `$or` over two equality checks.

</details>

**(d)** How does this query differ from an equivalent SQL query in terms of schema enforcement? (2 marks)

<details>
<summary>Answer</summary>

In SQL, the table schema is enforced at write time (schema-on-write) — every row must conform to defined columns and data types. If a column does not exist, the query fails or returns nothing. In MongoDB (schema-on-read), documents in the `orders` collection may not all have a `region` field; documents missing `region` simply do not match the filter and are excluded from results, without any error. This flexibility allows heterogeneous documents but means data quality depends on application-level enforcement rather than the database itself.

</details>

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

<details>
<summary>Answer</summary>

Spark uses **lazy evaluation**. Calling `.filter()`, `.groupBy()`, `.agg()`, and `.orderBy()` only builds a logical execution plan — no data is read or processed. Computation is only triggered when an **action** is called (`show()`, `collect()`, `count()`, `write()`, etc.). This allows Spark's Catalyst optimiser to inspect the entire query plan and apply optimisations (e.g., predicate pushdown to the Parquet reader, column pruning) before any work begins.

</details>

**(b)** What is the advantage of reading from **Parquet** format compared to CSV for this type of query? (2 marks)

<details>
<summary>Answer</summary>

Parquet is a **columnar storage format**. For this query (which only uses `region`, `product_category`, `revenue`, `order_id`), Parquet allows Spark to read only those four columns from disk — skipping all others. CSV is row-oriented, so reading any column requires reading the entire row. This results in significantly less I/O and faster query execution, especially at scale. Parquet also stores data type metadata and supports efficient compression per column.

</details>

**(c)** The second `.filter()` (`order_count > 1000`) is applied after `.agg()`. Why can't this filter be applied before the `groupBy`? (2 marks)

<details>
<summary>Answer</summary>

`order_count` is a **derived column** produced by the aggregation (`count("order_id").alias("order_count")`). It does not exist in the raw data — it is computed per group. Therefore it cannot be referenced in a filter before the `groupBy`/`agg` step. This pattern is equivalent to SQL's `HAVING` clause (filter on aggregated values) as opposed to `WHERE` (filter on raw rows before aggregation).

</details>

**(d)** This code reads from an S3 path. What type of storage layer does this represent, and what is one limitation of this approach for **real-time** analytics? (2 marks)

<details>
<summary>Answer</summary>

S3 is an object store used as a **Data Lake** layer — it stores raw or semi-processed data cheaply at scale without enforcing schema. The primary limitation for real-time analytics is **high latency**: S3 is optimised for batch reads of large files, not low-latency point queries. It is also **eventually consistent** in some configurations, and new data written to S3 is typically available in minutes (after batch job runs), not milliseconds — making it unsuitable for sub-second real-time use cases that would require a streaming system (Kafka + Flink) instead.

</details>
