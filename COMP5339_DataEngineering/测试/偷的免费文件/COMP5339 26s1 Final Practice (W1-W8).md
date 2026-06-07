# COMP5339 — 26s1 Final Practice (W1–W8)

> **来源**：外部练习资料（截至 26S1）  
> **格式**：参照 [`Quiz2 模拟题.md`](../Quiz2%20模拟题.md)  
> **说明**：题目无官方答案；含图片的题已附原图或重绘 diagram

**原始扫描页：**

| 页 | 内容 |
|----|------|
| [Page 1 — W1](images/page-01-w1.png) | Week 1 Introduction + Q1–Q9 |
| [Page 2 — W2/W3](images/page-02-w2-w3.png) | Q9 续 + W2 全题 + W3 Q1 |
| [Page 3 — W3/W4](images/page-03-w3-w4.png) | W3 Q2–Q10 + W4 Web Scraping & APIs |
| [Page 4 — W5/W6](images/page-04-w5-w6.png) | W5 NoSQL + W6 Temporal（Q1–Q4） |
| [Page 5 — W6/W7/W8](images/page-05-w6-w8.png) | W6 Q5–Q10 + W7 Spatial + W8 Q1 |

![Page 1 原图](images/page-01-w1.png)

![Page 2 原图](images/page-02-w2-w3.png)

![Page 3 原图](images/page-03-w3-w4.png)

![Page 4 原图](images/page-04-w5-w6.png)

![Page 5 原图](images/page-05-w6-w8.png)

---

## W1 — Introduction to Data Engineering and Data Pipelines

> **本周重点**：数据工程是端到端服务，不是"搬文件"。核心动作：ingest（获取）→ validate（验证）→ transform（转换）→ deliver（交付）。常考指标：throughput、latency、freshness、lineage、observability。

---

### Q1 · 选择题

A dashboard is updated by a script that downloads a CSV manually, edits column names in a spreadsheet, and uploads the result to a shared folder. Which change most directly turns this into a data-engineering pipeline rather than a manual reporting task?

- [ ] (A) Move the spreadsheet to a shared drive but keep the same manual edits.
- [ ] (B) Automate ingestion, validation, transformation, and repeatable delivery with logging.
- [ ] (C) Add a dashboard refresh button without validating source changes.
- [ ] (D) Keep only the final edited spreadsheet and no run logs or validation results.

---

### Q2

Explain the difference between **data generation**, **data acquisition**, **data transformation**, and **serving** in a typical data pipeline. Use one concrete example.

---

### Q3 · 概念题

A manager says: *"If our model is wrong, that is a data-science problem, not a data-engineering problem."* Give two ways poor data engineering can create a wrong model conclusion.

---

### Q4 · 选择题

Which pair best matches the terms?

- [ ] (A) Throughput: delay until data is usable; latency: records processed per second.
- [ ] (B) Throughput: records processed per unit time; latency: time from source event to usable output.
- [ ] (C) Throughput: number of tables; latency: number of columns.
- [ ] (D) Throughput: storage cost; latency: cloud region.

---

### Q5

A pipeline has perfect average throughput but fails during hourly traffic spikes. Explain why average throughput alone is not enough and name two controls.

---

### Q6 · 策略题

You inherit the following unmanaged reporting flow. Redesign it as a production ETL DAG and state three failure checks that should block publication.

**Given flow（原题配图）：**

![Q6 — Unmanaged reporting flow](images/q6-unmanaged-flow.png)

**Diagram（Mermaid 重绘）：**

```mermaid
flowchart LR
    A["CSV download"] --> B["Manual spreadsheet edit"]
    B --> C["Dashboard upload"]
```

1. **(A)** Replace the boxes with an orchestrated raw → trusted → serving DAG.
2. **(B)** Name three data-quality or lineage checks and where each check runs.
3. **(C)** Explain how the design supports replay after a transformation bug.

---

### Q7 · 选择题

A pipeline reads transaction files nightly. One night the source silently changes the date format and half the rows are rejected. Which quality dimension is most directly threatened?

- [ ] (A) Completeness and validity/accuracy.
- [ ] (B) Freshness only, because the source file still arrived on time.
- [ ] (C) Lineage only, because row rejection cannot affect data values.
- [ ] (D) Security only, because any date parsing issue is an access-control problem.

---

### Q8 · 概念题

Why is a pipeline usually evaluated by **correctness**, **efficiency**, and **ease-of-use** rather than speed alone?

---

### Q9 · 真题改编（Semester 2, 2023 modified）

A city council wants a dashboard comparing live car-park occupancy with suburb-level public-transport accessibility. Occupancy arrives from a web API every minute, while accessibility scores are published monthly as CSV files.

Propose a high-level data architecture and justify which parts should be **streaming**, **batch**, **raw-staged**, and **served** to the dashboard.

---

### Q10

Name the four common data-engineering challenge categories **volume**, **variety**, **velocity**, and **veracity**. For each, give one example risk.

---

## W2 — Data Acquisition and Data Cleaning

> **本周重点**：ingestion 与 cleaning 的边界——源系统怎样把数据交给 pipeline，pipeline 又如何在不破坏语义的前提下修复数据。高频考点：push/pull/polling、CDC、schema drift、missing/default/incorrect/inconsistent values、raw staging 的审计价值。考试常要求设计 validation matrix、quarantine 策略和恢复流程；警惕把所有异常值直接填零、丢弃严重病例、或让清洗逻辑只藏在代码里。

---

### Q1 · 选择题

A source database can emit commit-log changes with operation type and timestamp. Which ingestion strategy is usually preferable for a large table that changes frequently?

- [ ] (A) Download the whole table every minute.
- [ ] (B) Change data capture with idempotent target writes.
- [ ] (C) Run a full extract every hour and overwrite the target without operation metadata.
- [ ] (D) Append all changed rows without deduplication or delete handling.

---

### Q2

Compare **push**, **pull**, and **polling** ingestion. Give one situation where each is natural.

---

### Q3 · 概念题

A dataset uses blank values, `'NA'`, `-1`, and `99999` to represent different kinds of missing values. Why can replacing all of them with zero be dangerous?

---

### Q4 · 公式题

A batch pipeline receives **1,200,000 records in 20 minutes**. The downstream service can validate **800 records per second** on one worker. Ignoring overhead, how many workers are required to keep up with the average arrival rate? Explain the limitation of this calculation.

---

### Q5 · 真题改编（Semester 1, 2024 modified）

A hospital vitals feed has 30% missing blood-pressure values, and missingness is more common for severe cases because measurements are postponed during emergency treatment.

Classify the missingness mechanism and explain an appropriate cleaning strategy.

---

### Q6 · 选择题

Which check is most suitable for detecting **schema drift** before it silently breaks a dashboard?

- [ ] (A) Compare incoming field names, types, and required columns against a versioned schema.
- [ ] (B) Sort the rows alphabetically.
- [ ] (C) Only check whether the final dashboard still has the same number of charts.
- [ ] (D) Accept all new fields but never alert on missing required fields.

---

### Q7

The following ingestion profile is observed for a public-transport feed. Complete a **data-quality matrix** with one validation rule and one action for each row.

| Signal | Example symptom |
|--------|-----------------|
| Completeness | 18% of vehicles omit route id |
| Validity | speed field contains `fast` |
| Timeliness | events arrive 25 minutes late |
| Consistency | stop id exists in one file but not in the reference table |

---

### Q8 · 策略题

A team cleans customer addresses by lowercasing text and removing punctuation, then joins to postcode boundaries. The join success improves, but some apartment and unit information disappears.

Diagnose the bug and propose a safer cleaning workflow.

---

### Q9 · 选择题

Which statement about **raw staging data** is best?

- [ ] (A) It is useless once curated tables exist.
- [ ] (B) It can support replay, auditing, and changed transformation logic if access is controlled.
- [ ] (C) It should always be editable by analysts.
- [ ] (D) It removes the need for metadata.

---

### Q10

Explain why data cleaning assumptions should be recorded as **metadata or documentation**, not just embedded in code.

---

## W3 — Databases, SQL, Warehouses, and OLAP

> **本周重点**：DBMS、warehouse 与 OLAP。区分 OLTP 事务型点查 vs OLAP 历史聚合扫描；理解 star schema、fact/dimension、SCD、metadata、source-to-target reconciliation。考试常要求画 fact table 与 dimensions、解释列式存储/分区/materialised aggregate，并说明 ETL 元数据如何支撑审计。

![W3/W4 原页](images/page-03-w3-w4.png)

---

### Q1 · 选择题

Why can pushing a filter and aggregation into a DBMS be better than exporting the whole table to Python?

- [ ] (A) It always changes the answer.
- [ ] (B) It can reduce data transfer and use indexes/optimisation.
- [ ] (C) It prevents all data-quality issues.
- [ ] (D) It removes the need for SQL permissions.

---

### Q2

Distinguish **OLTP** and **OLAP** access patterns using an online store example.

---

### Q3 · 真题改编（Semester 1, 2024 modified）

A CSV has store, product, sale date, and amount. Design a **star schema** and explain why it helps analytical queries.

---

### Q4

A finance report changes after an analyst edits a transformation rule. What **lineage metadata** should be available to audit the change?

---

### Q5 · 选择题

Which operation best describes aggregating daily sales to monthly sales in an OLAP cube?

- [ ] (A) Roll-up.
- [ ] (B) Drill-through to raw logs.
- [ ] (C) Packet routing.
- [ ] (D) Hash partitioning.

---

### Q6 · 公式题 / 计算题

A warehouse table stores **200 million** sales rows. A query needs only **4 columns out of 40** and records from **one month out of 24** equally sized months. Roughly what **fraction of cell values** is needed if column pruning and partition pruning both work ideally?

---

### Q7 · 真题改编（Semester 2, 2023 modified）

An analytics team wants to build a **data lake** for raw CSV, JSON API responses, images, and curated warehouse extracts. Explain what makes this a data lake rather than just a folder of files, and evaluate one **governance risk** if raw data is stored without cataloguing or lifecycle rules.

---

### Q8 · 概念题

What is a **slowly changing dimension**? Give an example where preserving old dimension values matters.

---

### Q9 · 选择题

A dashboard query joins large fact rows to dimensions but one dimension key is missing for many records. Which issue is most likely?

- [ ] (A) Referential-integrity or late-arriving dimension problem.
- [ ] (B) Successful compression.
- [ ] (C) Correct pivoting.
- [ ] (D) A late-arriving dimension or inconsistent key mapping.

---

### Q10

Explain why indexes that help **OLTP** transactions are not automatically enough for **OLAP** workloads.

---

## W4 — Web Scraping and Web APIs

> **本周重点**：web scraping 与 API ingestion。核心不是"能不能抓到数据"，而是怎样**稳定、合规、可恢复**地抓取。常考 rate limit、pagination、retry/backoff、HTML 结构变化、API schema change、secret 管理和采集元数据。考试可能给 429、timeout、DOM selector 失效或 JSON 类型漂移场景，要求设计 crawler/API client 控制流；区分可重试错误与永久错误，说明日志、样本快照和 canary URL 如何让失败在进入 warehouse 前暴露。

---

### Q1 · 真题改编（Semester 2, 2024 modified）

Design a **politeness policy** for a small crawler that collects public product pages. Include a simple state flow and how the crawler should handle **4xx errors**, **5xx errors**, **redirects**, and **timeouts**.

---

### Q2 · 选择题

Which response should usually cause a crawler to **slow down or back off**?

- [ ] (A) HTTP 429 Too Many Requests.
- [ ] (B) HTTP 200 OK.
- [ ] (C) A smaller HTML heading.
- [ ] (D) A CSV delimiter.

---

### Q3 · 概念题

Compare scraping an HTML page with using an official **JSON API** for the same data. Give one advantage and one risk of each.

---

### Q4 · 真题改编（Semester 2, 2023 modified）

A scraper is failing because it treats visible article text, navigation menus, and page metadata as one flat string. Sketch the **high-level structure of an HTML page** and explain why distinguishing the head, body, tags, and nested elements matters for extraction.

---

### Q5

Why is a **timeout** not the same as a negative result from a web API?

---

### Q6 · 策略题

A scraper starts returning **empty prices** after a website redesign. The HTTP status is **200** and pages still contain price text visible in a browser. Diagnose likely causes and propose **monitoring** that would catch this earlier.

---

### Q7 · 公式题

An API allows an effective steady rate of **600 requests per 10 minutes** per token, with no initial burst. You need to fetch **18,000 product records**, one request per product, using one token. What is the **minimum time** ignoring network latency? What **design concern** remains?

---

### Q8 · 概念题

Give three pieces of **metadata** a pipeline should store for each API extraction run.

---

### Q9 · 选择题

A web API changes one field from **integer to string** without notice. Which downstream failure is most plausible?

- [ ] (A) Type validation or numeric aggregation fails.
- [ ] (B) Rate limiting becomes stricter because the field is now textual.
- [ ] (C) A spatial CRS mismatch appears in unrelated distance queries.
- [ ] (D) The API authentication token gains broader privileges automatically.

---

### Q10

Explain why **authentication secrets** for APIs should not be hard-coded in notebooks or committed to version control.

---

## W5 — Semistructured Data and NoSQL

> **本周重点**：半结构化数据与 NoSQL 建模。理解 XML/JSON/HTML 结构差异、schema-late 的灵活性与风险、document DB 的 embedding vs referencing 取舍、shard key 与 access pattern 的匹配。高分答案要说明约束在哪里 enforced、如何控制文档膨胀、如何避免 hot shard。

![W5/W6 原页](images/page-04-w5-w6.png)

---

### Q1 · 选择题

Which property best describes **semi-structured data**?

- [ ] (A) It may have nested, optional, or heterogeneous fields while still carrying structure.
- [ ] (B) It cannot be parsed by any program.
- [ ] (C) It must be stored only in CSV files.
- [ ] (D) It has no labels or tags of any kind.

---

### Q2

Compare **XML** and **JSON** for data exchange. Mention one advantage and one disadvantage of each.

---

### Q3 · 真题改编（Semester 2, 2024 modified）

A bookstore platform receives XML inventory, JSON user reviews, and scraped HTML book pages. Explain why the data is semi-structured and design a **MongoDB collection** for books and reviews.

---

### Q4 · 选择题

Which MongoDB aggregation approach is most flexible for multi-stage transformations such as match, unwind, group, and project?

- [ ] (A) Aggregation pipeline.
- [ ] (B) Screenshot aggregation.
- [ ] (C) Manual copy-paste.
- [ ] (D) HTML heading levels.

---

### Q5

Explain the design trade-off between **embedding** and **referencing** in a document database.

---

### Q6 · 策略题

A MongoDB collection stores user documents with an **unbounded array of click events**. Over time some documents exceed practical size and updates slow down. Diagnose the design problem and propose a redesign.

---

### Q7 · 真题改编（Semester 1, 2024 modified）

Briefly compare **relational databases** and **NoSQL databases** in terms of data structure and scalability.

---

### Q8 · 公式题 / 计算题

A sharded collection stores **90 million events** across **9 shards** by region. One region accounts for **45 million events**. What **imbalance risk** appears, and what **shard-key improvement** could reduce it?

---

### Q9

Model a **recommendation graph** with users, books, and authors. Specify node labels, relationship types, and one **Cypher-style query** to find authors liked by users who follow Alice.

---

### Q10 · 选择题

Which statement about NoSQL schema design is best?

- [ ] (A) NoSQL removes all need to think about schema.
- [ ] (B) The access pattern should strongly influence the document/key/graph structure.
- [ ] (C) All relationships should always be embedded.
- [ ] (D) Sharding always improves every query.

---

## W6 — Temporal Data Engineering

> **本周重点**：时间语义——event time、ingestion/processing time、valid time、transaction time；interval 表示、late data 与 correction、watermark、bitemporal 设计、as-of 查询。考试常给医疗/能源/零售场景，要求说明为何单个 `updated_at` 不够、如何用 half-open interval 表达 validity、late event 怎样进入 window。

![W6/W7/W8 原页](images/page-05-w6-w8.png)

---

### Q1 · 选择题

Which pair of time dimensions is needed for **bitemporal audit queries**?

- [ ] (A) Valid time and transaction time.
- [ ] (B) CPU time and screen time.
- [ ] (C) Latitude time and longitude time.
- [ ] (D) HTML time and XML time.

---

### Q2

A hospital guideline table has condition, treatment, start date, replacement date, and database load time. Explain why a single **last-updated timestamp** cannot answer: *what was valid on 15 March 2024 according to the database on 30 April 2024?*

---

### Q3 · 概念题

Give two reasons **time zones** can break a data pipeline even when all timestamps look valid.

---

### Q4 · 公式题 / 计算题

A sensor emits one reading every **5 seconds** per device. There are **240 devices**. How many readings arrive per **hour**? What **storage design concern** follows?

---

### Q5 · 选择题

A stream window includes events by their **event timestamp**, not arrival timestamp. What problem must the system handle?

- [ ] (A) Late and out-of-order events.
- [ ] (B) XML declarations.
- [ ] (C) Polygon holes.
- [ ] (D) Choosing a CRS suitable for measurement rather than only web display.

---

### Q6

Compare **point-based** and **interval-based** temporal representation with examples.

---

### Q7

An energy provider corrects yesterday's hourly meter readings after a calibration issue. Dashboards already consumed the old values. Design a **temporal ingestion strategy** that supports correction, replay, and audit.

---

### Q8 · 选择题

Which SQL predicate is safest for a **half-open validity interval**?

- [ ] (A) `valid_start <= t AND t < valid_end`
- [ ] (B) `valid_start < t AND valid_end < t`
- [ ] (C) `t < valid_start AND valid_end < t`
- [ ] (D) `valid_start = valid_end`

---

### Q9

What is a **watermark** in stream processing, and why is it useful for temporal aggregation?

---

### Q10

A retailer joins clickstream events to a product catalogue that changes over time. Explain how a **temporal join** should decide which product category to attach to each click.

---

## W7 — Spatial-Temporal Data Engineering

> **本周重点**：空间与时间结合——point/line/polygon、CRS、spatial index、point-in-polygon、trajectory、geospatial join。常见陷阱：CRS 不一致、把 polygon 当 centroid、未做 bounding-box 预过滤就全量精确计算。答题要把 geometry 类型、索引策略和查询 workflow 连起来。

---

### Q1 · 选择题

Which geometry type is most natural for a **bus GPS observation** at one timestamp?

- [ ] (A) Point.
- [ ] (B) Polygon.
- [ ] (C) MultiPolygon boundary.
- [ ] (D) XML body.

---

### Q2

Name suitable **geometry types** for rainfall gauges, road segments, suburb boundaries, and flood extents.

---

### Q3 · 真题改编（Semester 1, 2024 modified）

A spatial pipeline combines Airbnb points in **WGS84** with incident polygons in **GDA94**. Explain the **CRS problem** and design a query workflow for finding listings within **5 km** of incidents.

---

### Q4 · 公式题

A GPS feed sends one point every **5 seconds** for each of **1,500 buses**. Estimate **points per day**. State one **indexing or partitioning** strategy.

---

### Q5

Why is computing **Euclidean distance directly on latitude and longitude degrees** usually wrong?

---

### Q6 · 选择题

Which predicate is most appropriate to test whether a point lies **inside a suburb polygon**?

- [ ] (A) `ST_Contains` or `ST_Within`.
- [ ] (B) `ST_Uppercase`.
- [ ] (C) SQL `COUNT` only.
- [ ] (D) XML standalone.

---

### Q7

A prototype stores flood extents as only **centroid points**. Explain one analysis that becomes impossible or misleading and propose a corrected representation.

---

### Q8 · 概念题

Compare **point-based** and **sequence-based** representation for bus movement data.

---

### Q9 · 选择题

A spatial index primarily helps by:

- [ ] (A) Reducing candidate geometries before expensive exact spatial predicates.
- [ ] (B) Converting JSON to XML.
- [ ] (C) Proving every polygon is valid.
- [ ] (D) Replacing all CRS transformations.

---

### Q10

Design a **spatial-temporal table** for ride-share pickups and drop-offs that supports queries by time window, pickup suburb, and trip distance. Include key fields and two indexes.

---

## W8 — Processing Unstructured Data

> **本周重点**：非结构化数据处理——text/PDF/image、OCR、embedding、metadata。强调保留 raw artifact、版本化、metadata、quality check 和 manual review queue；注意 privacy 与 access control。

> ⚠️ **资料截断**：原扫描页仅收录 W8 Q1 部分选项，后续题目待补充。

---

### Q1 · 选择题

Which is the best first engineering step before running sentiment analysis over millions of support emails?

- [ ] (A) Define ingestion, parsing, metadata, access control, and privacy controls before model training.
- [ ] (B) *(其余选项在扫描页中截断，待补全)*

---
