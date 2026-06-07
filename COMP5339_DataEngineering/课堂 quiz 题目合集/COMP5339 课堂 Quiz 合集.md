# COMP5339 — 课堂 Quiz 题目合集

> **来源**：Tutorial Quiz 1-1 ~ 2-4（官方 sample answers）  
> **格式**：参照 [`测试/Quiz2 模拟题.md`](../测试/Quiz2%20模拟题.md)  
> **说明**：每份 3 道 MCQ（各 3 小题，1 mark each）+ 简答题，共 10 marks

## 目录

- [Quiz 1-1 — Thursday, 16 April](#quiz-11)
- [Quiz 1-2 — Friday, 17 April, 06 PM](#quiz-12)
- [Quiz 1-3 — Friday, 17 April, 07 PM](#quiz-13)
- [Quiz 1-4 — Friday, 17 April, 08 PM](#quiz-14)
- [Quiz 2-1 — Thursday, 21 May](#quiz-21)
- [Quiz 2-2 — Friday, 22 May, 06 PM](#quiz-22)
- [Quiz 2-3 — Friday, 22 May, 07 PM](#quiz-23)
- [Quiz 2-4 — Friday, 22 May, 08 PM](#quiz-24)

---

<a id="quiz-11"></a>

## Quiz 1-1 — Thursday, 16 April

**Tutorial Quiz 1 | Week 1–5**
**Quiz Writing Time: 30 minutes | Total: 10 marks**
**Closed book. No electronic devices permitted.**

---

### Part I — Multiple Choice Questions (1 mark each)

*Tick the box corresponding to the correct answer. Each question carries one mark.*

---

**Question 1A.** In the "Data Engineering Lifecycle" diagram, why is Storage drawn as a long layer underneath ingestion → transformation → serving (instead of being a single step)?

- [ ] Storage supports all stages (landing raw data, staging transformations, and serving curated data), and its choice affects performance, cost, and reliability across the pipeline
- [ ] Storage is only used for archiving after analytics are complete
- [ ] Storage is mainly for backups and doesn't affect pipeline design
- [ ] Storage is only needed when working with streaming systems

> [!note]- Answer
> **Storage 贯穿整个 pipeline 各阶段。**
> 
> Storage 不只是某一步的副产品——raw landing、staging、curated serving 都依赖它。存储选型同时影响性能、成本和可靠性，因此画成贯穿 ingestion → transformation → serving 的底层。

---
**Question 1B.** When extracting data from a webpage, what is the most important first step?

- [ ] Inspecting the webpage structure
- [ ] Writing extraction code
- [ ] Storing data in a database
- [ ] Running the crawler

> [!note]- Answer
> **Inspecting the webpage structure（检查页面结构）。**
> 
> 写代码、跑爬虫、入库之前，必须先理解 HTML 结构（元素、class/id、层级），否则 extraction logic 无法正确定位目标字段。

---
**Question 1C.** A data engineering team is building a pipeline to ingest data from multiple external APIs whose structures frequently change (new fields, missing fields, nested variations). Which design choice is most appropriate?

- [ ] Use a strictly normalised relational schema before ingestion
- [ ] Use a schema-on-read approach with a document-oriented store
- [ ] Use a schema-on-write approach with enforced constraints
- [ ] Use a columnar data warehouse with a fixed schema

> [!note]- Answer
> **Schema-on-read + document-oriented store（如 MongoDB）。**
> 
> 多源 API 结构频繁变化时，schema-on-read 允许先原样 ingest 异构 JSON，再在读取时解析；document store 天然适配嵌套/可变字段。固定 schema 的 relational/warehouse 会在 schema drift 时频繁失败。

---

### Part II — Short Answer Questions

*Provide answers in the boxes provided below each question.*

---

**Question 2.** Why is a graph database more suitable than a relational model for this use case? **(2 Marks)**

> [!note]- Answer
> **Graph database 适合关系/依赖为核心的场景。**
> 
> Graph databases efficiently represent relationships such as prerequisites and dependencies between concepts. They allow fast traversal without complex joins. This makes them ideal for ontology-driven systems and knowledge graphs where relationships are central.

---
**Question 3 — Data Acquisition, Cleaning, and Integration**

**Scenario 1:** You work at an e-commerce company and ingest order events daily from multiple source systems. Sometimes an order arrives 2–3 days late, and occasionally the same order appears twice with identical fields.

How would you design your ingestion + staging layer to ensure:
1. Non-identical loads (no duplicates) **(1 Mark)**
2. Correct historical completeness (late arrivals are included) **(1 Mark)**
3. Identify a schema change? **(1 Mark)**

> [!note]- Answer
> 1. **去重**：数据进入 staging area 后，检测完全重复的行（entire row duplicated），再写入下游 storage/database。
> 2. **迟到数据**：查找过去已完成但迟到的订单，按实际业务日期回填到对应分区/日期。
> 3. **Schema 变更检测**：保存 baseline schema，在 ingestion 时与当前 schema 对比，发现新增/变更字段。

---
**Scenario 2:** The source team adds a new column (`discount`) to the orders feed and later changes the `postal_code` column type from numeric to string. Your pipeline starts failing.

What controls and design choices would you put in place to handle schema evolution safely (both breaking and non-breaking changes) while keeping downstream analytical tables stable? **(2 Marks)**

> [!note]- Answer
> Implement schema validation at ingestion and alert on breaking changes. Use schema evolution rules: allow additional fields, but fail on incompatible type changes. Store raw payloads to avoid data loss and map them to a stable schema in staging.
> 
> **要点**：raw layer 保留原始 payload；non-breaking（新增字段）允许通过；breaking（类型不兼容）fail fast + alert；staging 映射到稳定的下游 analytical schema。

---

<a id="quiz-12"></a>

## Quiz 1-2 — Friday, 17 April, 06 PM

**Tutorial Quiz 1 | Week 1–5**
**Quiz Writing Time: 30 minutes | Total: 10 marks**
**Closed book. No electronic devices permitted.**

---

### Part I — Multiple Choice Questions (1 mark each)

*Tick the box corresponding to the correct answer. Each question carries one mark.*

---

**Question 1A.** Which statement best describes the role of staging in an OLTP → OLAP pipeline?

- [ ] Staging tables are the final tables used by BI dashboards; fact/dim tables are just temporary
- [ ] Staging replaces the OLTP system by serving user transactions with high concurrency
- [ ] Staging exists only to store aggregated results (e.g., monthly revenue)
- [ ] Staging stores a raw or lightly cleaned copy of source data to support reruns, deduplication, and incremental loading before building fact/dim tables

> [!note]- Answer
> **Staging 是 OLTP → OLAP 的中间缓冲层。**
> 
> 存放 raw/lightly cleaned 副本，支持 rerun、deduplication、incremental load，再构建 fact/dim tables。它不是 BI 的最终表，也不替代 OLTP。

---
**Question 1B.** You can either (i) run SQL that filters/aggregates in the DB and return a small result set, or (ii) bulk-load the whole table into Pandas and process it there. Which is the strongest technical reason for choosing option (i)?

- [ ] Pandas cannot do joins or group-bys
- [ ] SQL cannot express aggregations compared to Pandas
- [ ] Bulk-loading is always slower, even for small datasets
- [ ] DBMS can optimise queries, and bulk-loading requires the full dataset to fit into memory

> [!note]- Answer
> **DBMS 可优化查询；bulk-load 需整表进内存。**
> 
> 在数据库端 filter/aggregate 只返回小结果集，利用 query optimizer 和索引；Pandas 方案需把全表 load 进内存，大数据集不可行。Pandas 完全可以做 join/groupby（A 错）。

---
**Question 1C.** A data engineering team is ingesting semi-structured data from multiple sources where fields vary across records. They decide to use a schema-late approach. Which of the following is the main advantage of this decision?

- [ ] Enforces strict consistency across all records
- [ ] Reduces storage size compared to relational databases
- [ ] Eliminates the need for data validation entirely
- [ ] Allows ingestion of heterogeneous data without a predefined schema

> [!note]- Answer
> **Schema-late 允许异构数据无需预定义 schema 即可 ingest。**
> 
> 不同 record 字段不一致时，schema-late（schema-on-read）先存后解析，比 schema-on-write 更灵活。并不消除 validation 需求，也不保证 strict consistency。

---

### Part II — Short Answer Questions

*Provide answers in the boxes provided below each question.*

---

**Scenario 1:** The table below shows order lines for one customer. Two dashboards (developed by two different teams) show different "monthly revenue" numbers. One includes only order status with "Shipped"; the other includes "Cancelled" and "On Hold". Both teams claim they are correct.

| ORDERNUMBER | CUSTOMERNAME | ORDERDATE | STATUS | SALES |
|-------------|--------------|-----------|--------|-------|
| 20001 | Australian Collectors, Co. | 1/10/2004 | Shipped | 3600 |
| 20015 | Australian Collectors, Co. | 1/18/2004 | Cancelled | 1204 |
| 20022 | Australian Collectors, Co. | 1/25/2004 | On Hold | 870 |

How do you enforce consistent metric definitions across the organisation, and what pipeline components help prevent or detect these inconsistencies? **(2 Marks)**

> [!note]- Answer
> Define metrics centrally (data catalogue/semantic layer) with agreed filters (e.g., only status='Shipped'). Publish tables and prevent ad-hoc redefinition by creating views. Add data tests (for accepted statuses and revenue formula checks) and documentation.
> 
> **核心**：semantic layer / data catalogue 统一定义 metric；用 views 防止各团队自行 filter；data tests 检测 status 和 revenue 公式一致性。

---
**Scenario 2:** A fact table grows to billions of rows. Most queries filter by date and region, but performance and cost are rising.

**Question 2:** What strategies would you use to improve performance and control cost (e.g., partitioning, aggregates), and how do you decide which to implement? **(2 Marks)**

> [!note]- Answer
> - If most queries filter by time, then partition by date first.
> - If queries also filter heavily by region/product, then cluster/sort on those.
> - If the same aggregations power dashboards repeatedly, then materialised views/marts.
> 
> **决策逻辑**：先看 query pattern——时间 filter 多 → date partition；region 也常用 → cluster/sort；重复聚合 → materialised views/marts。

---
**Scenario 3:** Your analysts want near-real-time dashboards. The OLTP database is already under heavy load. Running large analytical queries against it slows down customer operations.

**Question 3:** What extraction approach would you choose, and how would you architect the system so analytical workloads do not impact OLTP performance? **(3 Marks)**

1. Change Data Capture (CDC)
2. Replication
3. Scheduled extracts

> [!note]- Answer
> Avoid querying the OLTP database directly for dashboards — analytical scans compete with transactional workloads (locks, CPU, I/O). Use **CDC** (reading the database's transaction log) to stream changes into an analytics environment.
> 
> - CDC reads changes from the transaction log rather than running large joins/aggregations on OLTP tables.
> - OLTP already writes to logs for recovery; CDC just consumes those logs.

---

<a id="quiz-13"></a>

## Quiz 1-3 — Friday, 17 April, 07 PM

**Tutorial Quiz 1 | Week 1–5 (Web Scraping focus)**
**Quiz Writing Time: 30 minutes | Total: 10 marks**
**Closed book. No electronic devices permitted.**

---

### Part I — Multiple Choice Questions (1 mark each)

*Tick the box corresponding to the correct answer. Each question carries one mark.*

---

**Question 1A.** In a data pipeline, what is the main challenge when extracting data from multiple linked webpages?

- [ ] Data storage
- [ ] Network speed
- [ ] Maintaining consistent structure across pages
- [ ] Visualising the data

> [!note]- Answer
> **Maintaining consistent structure across pages（跨页面结构一致性）。**
> 
> 多 linked pages 往往 HTML 结构不完全相同（分页、详情页 vs 列表页），extraction logic 需适配多种 layout，这是 scraping pipeline 的主要工程挑战。

---
**Question 1B.** In a document database (such as MongoDB), relationships between entities can be represented using embedding or referencing. When is embedding preferred?

- [ ] When data is highly normalised
- [ ] When related data is frequently accessed together
- [ ] When relationships are many-to-many and large
- [ ] When strict ACID transactions are required

> [!note]- Answer
> **Embedding 适合 related data 经常一起读取的场景。**
> 
> 一次 read 拿齐 parent + children，避免 join。Highly normalised、many-to-many 大关系、strict ACID 更适合 referencing 或 relational DB。

---
**Question 1C.** Why are APIs generally preferred over web scraping in data engineering?

- [ ] APIs provide structured and stable access to data
- [ ] APIs provide unstructured data
- [ ] APIs are always free
- [ ] APIs require more manual effort

> [!note]- Answer
> **APIs provide structured and stable access to data.**
> 
> API 返回结构化 JSON/XML，schema 相对稳定，有文档和 versioning；scraping 依赖 HTML 结构，易因页面改版而 break，且有 legal/robots.txt 风险。

---

### Part II — Short Answer Questions

*Provide answers in the boxes provided below each question.*

---

**Scenario 1:** You are given a webpage from an online unit allocation, presented in the HTML structure below. You need to extract this data for a data warehouse.

```html
<div id="course">
  <h2 class="title">Data Engineering</h2>
  <span class="code">COMP5339</span>
  <span class="lecturer">Imdad</span>
  <span class="enrolments">450</span>
</div>
```

1. Identify the attributes and write at least one record **(1 Mark)**
2. Which elements will you target for extraction? **(1 Mark)**

> [!note]- Answer
> **Attributes:** title, code, lecturer, enrolments
> **Record:** Data Engineering, COMP5339, Imdad, 450
> **Target element:** `div#course`（或内部 `span`/`h2` 子元素）

---
**Question 2:** Suppose the webpage changes to the following (compared to the initial structure above):

```html
<div id="course">
  <h2 class="title">Data Engineering</h2>
  <span class="code">COMP5339</span>
  <span class="lecturer">Imdad</span>
  <span class="enrolments">450 students</span>
</div>
```

What data quality issues may arise, and how would you handle them in a pipeline? **(2 Marks)**

> [!note]- Answer
> **Issues:**
> - The numeric field under "enrolments" becomes text ("450 students")
> - Inconsistent format
> 
> **How to handle:**
> - Apply transformation to extract numeric values (regex / cast)
> - Standardise format (e.g., remove "students") and enforce schema validation

---
**Question 3:** Suppose the webpage structure changes to the following:

```html
<div class="course-item">
  <h2 class="title">Data Engineering</h2>
  <span class="code">COMP5339</span>
  <span class="lecturer">Imdad</span>
  <span class="enrolments">450</span>
</div>
```

1. What has changed? **(1 Mark)**
2. What problem does this cause, and how would you make your pipeline more robust? **(1 Mark)**

> [!note]- Answer
> **What changed:** `class="course"` → `class="course-item"`（`id="course"` 也可能消失）
> 
> **Problem:** Extraction logic breaks due to dependency on class/id name.
> 
> **Solutions:** Add validation checks; implement monitoring/alerts; design adaptable extraction rules (multiple selectors, semantic locators).

---
**Question 4:** The website owner later provides an API that returns structured course data. Will you switch from scraping to API? Justify your answer. **(1 Mark)**

> [!note]- Answer
> **Yes — switch to API when available.**
> 
> API 提供 structured、stable、documented 的数据访问，减少 HTML 结构变更风险，通常更合法合规，维护成本更低。Scraping 仅作为 API 不可用时的 fallback。

---

<a id="quiz-14"></a>

## Quiz 1-4 — Friday, 17 April, 08 PM

**Tutorial Quiz 1 | Week 1–5**
**Quiz Writing Time: 30 minutes | Total: 10 marks**
**Closed book. No electronic devices permitted.**

---

### Part I — Multiple Choice Questions (1 mark each)

*Tick the box corresponding to the correct answer. Each question carries one mark.*

---

**Question 1A.** A data engineering team is building a pipeline to ingest data from multiple external APIs whose structures frequently change. Which design choice is most appropriate?

- [ ] Use a strictly normalised relational schema before ingestion
- [ ] Use a schema-on-read approach with a document-oriented store
- [ ] Use a schema-on-write approach with enforced constraints
- [ ] Use a columnar data warehouse with a fixed schema

> [!note]- Answer
> **Schema-on-read + document store** — 同 Quiz 1-1C，异构/可变 API 结构需要 schema-late 策略。

---
**Question 1B.** Which statement best describes the role of staging in an OLTP → OLAP pipeline?

- [ ] Staging tables are the final tables used by BI dashboards; fact/dim tables are just temporary
- [ ] Staging replaces the OLTP system by serving user transactions with high concurrency
- [ ] Staging exists only to store aggregated results (e.g., monthly revenue)
- [ ] Staging stores a raw or lightly cleaned copy of source data to support reruns, deduplication, and incremental loading before building fact/dim tables

> [!note]- Answer
> **Staging 存 raw/lightly cleaned 副本** — 同 Quiz 1-2A。

---
**Question 1C.** You can either (i) run SQL that filters/aggregates in the DB, or (ii) bulk-load the whole table into Pandas. Which is the strongest technical reason for choosing option (i)?

- [ ] Pandas cannot do joins or group-bys
- [ ] SQL cannot express aggregations compared to Pandas
- [ ] Bulk-loading is always slower, even for small datasets
- [ ] DBMS can optimise queries, and bulk-loading requires the full dataset to fit into memory

> [!note]- Answer
> **DBMS query optimization + memory constraint** — 同 Quiz 1-2B。

---

### Part II — Short Answer Questions

*Provide answers in the boxes provided below each question.*

---

**Scenario 1:** A fact table grows to billions of rows. Most queries filter by date and region, but performance and cost are rising.

**Question 1:** What strategies would you use to improve performance and control cost? **(3 Marks)**

> [!note]- Answer
> - If most queries filter by time, then **partition by date** first.
> - If queries also filter heavily by region, then **cluster/sort** on those columns.
> - If the same aggregations power dashboards repeatedly, then **materialised views/marts**.
> 
> *(注：官方 sample answer PDF 此处疑似误贴 metric definition 答案；以上为同题 Quiz 1-2 Scenario 2 的正确 sample answer。)*

---
**Scenario 2:** Your analysts want near-real-time dashboards. The OLTP database is already under heavy load.

**Question 2:** What extraction approach would you choose, and how would you architect the system? **(2 Marks)**

1. Change Data Capture (CDC)
2. Replication
3. Scheduled extracts

> [!note]- Answer
> Use **CDC** — stream changes from transaction log into analytics environment without querying OLTP directly.
> 
> - CDC reads from transaction log, not OLTP tables
> - OLTP already writes logs for recovery; CDC consumes them

---
**Scenario 3:** You are given a webpage from an online unit allocation:

```html
<div id="course">
  <h2 class="title">Data Engineering</h2>
  <span class="code">COMP5339</span>
  <span class="lecturer">Imdad</span>
  <span class="enrolments">450</span>
</div>
```

1. Identify the attributes and write at least one record **(1 Mark)**
2. Which elements will you target for extraction? **(1 Mark)**

> [!note]- Answer
> **Attributes:** title, code, lecturer, enrolments
> **Record:** Data Engineering, COMP5339, Imdad, 450
> **Target element:** `div#course`

---

<a id="quiz-21"></a>

## Quiz 2-1 — Thursday, 21 May

**Tutorial Quiz 2 | Week 7–11**
**Quiz Writing Time: 30 minutes | Total: 10 marks**
**Closed book. No electronic devices permitted.**

---

### Part I — Multiple Choice Questions (1 mark each)

*Tick the box corresponding to the correct answer. Each question carries one mark.*

---

**Question 1A.** From a data engineering perspective, what is the main extra requirement for a supervised learning pipeline compared with an unsupervised learning pipeline?

- [ ] It must always use image data
- [ ] It does not require preprocessing
- [ ] It only works on structured data
- [ ] It must include ground-truth labels linked correctly to features

> [!note]- Answer
> **Ground-truth labels linked correctly to features.**
> 
> Supervised learning 需要 labeled training data；labels 必须与 features 正确对应，否则模型学不到有效 pattern。Unsupervised 无此要求。

---
**Question 1B.** Why is metadata analysis attractive in image pipelines?

- [ ] It is always more accurate than image content
- [ ] It can provide useful structured information without full image-content analysis
- [ ] It avoids all storage requirements
- [ ] It replaces feature extraction completely in every case

> [!note]- Answer
> **Metadata 提供 structured info，无需完整 image-content analysis。**
> 
> EXIF（GPS、timestamp、camera model）等 metadata 可直接用于分类/过滤，比 pixel-level analysis 成本低得多。

---
**Question 1C.** Which of the following is an example of a transactional data stream?

- [ ] Credit card purchases by customers
- [ ] Temperature readings from sensors
- [ ] Road traffic speed measurements
- [ ] Weather history reports

> [!note]- Answer
> **Credit card purchases — transactional stream.**
> 
> Transactional stream 指离散业务事件（购买、支付）；sensor temperature / traffic speed 是 measurement stream；weather history 是 bounded batch 数据。

---

### Part II — Short Answer Questions

*Provide answers in the boxes provided below each question.*

---

**Question 2:** What is the main purpose of tokenisation in text preprocessing? What are the storage options for storing the output of tokenisation? **(2 Marks)**

> [!note]- Answer
> **Purpose:** Tokenisation splits raw text into smaller units (words, subwords, terms) for feature extraction and ML.
> 
> **Storage options:**
> - Text/JSON documents
> - Relational tables (one row per document or per token)
> - Sparse matrices / document-term matrices for ML

---
**Question 3:** Why is a traditional DBMS not sufficient for many stream processing applications? **(2 Marks)**

> [!note]- Answer
> A traditional DBMS is designed for **data at rest** — queries run over stored data. Stream applications require **continuous processing of live data with low latency**, which DSMS (Flink, Kafka Streams) handle natively.

---
**Scenario 2:** Explain the difference between scale-up and scale-out in scalable data engineering. Why is scale-out generally preferred for big data systems? **(3 Marks)**

> [!note]- Answer
> **Scale-up:** increase power of a single machine (more CPU, memory, storage).
> **Scale-out:** add more machines/nodes to a cluster.
> 
> Scale-out preferred because single server has physical/cost limits; clusters grow more easily and support shared-nothing distributed processing.

---

<a id="quiz-22"></a>

## Quiz 2-2 — Friday, 22 May, 06 PM

**Tutorial Quiz 2 | Week 7–11**
**Quiz Writing Time: 30 minutes | Total: 10 marks**
**Closed book. No electronic devices permitted.**

---

### Part I — Multiple Choice Questions (1 mark each)

*Tick the box corresponding to the correct answer. Each question carries one mark.*

---

**Question 1A.** In a supervised text-classification pipeline, which sequence is most appropriate?

- [ ] Raw text → feature extraction → labels + features → model training
- [ ] Raw text → clustering → labels → storage
- [ ] Raw text → image similarity → prediction
- [ ] Raw text → regression → tokenisation

> [!note]- Answer
> **Raw text → feature extraction → labels + features → model training.**
> 
> Supervised text classification 先提取 features（BoW/TF-IDF/embeddings），再与 labels 配对训练模型。Clustering 是 unsupervised；tokenisation 是 preprocessing 子步骤，不是 pipeline 末尾。

---
**Question 1B.** In a publish/subscribe system, publishers send messages to:

- [ ] Specific consumers directly
- [ ] Window operators only
- [ ] Relational tables only
- [ ] Topics managed by a broker

> [!note]- Answer
> **Topics managed by a broker.**
> 
> Pub/sub 模式中 publisher 发到 topic，broker 管理 topic，consumer 订阅 topic。Publisher 不直接寻址 consumer。

---
**Question 1C.** Why might one-hot encoding become problematic in a production pipeline?

- [ ] It may create very high-dimensional data when there are many categories
- [ ] It cannot represent categories
- [ ] It works only on images
- [ ] It always causes label leakage

> [!note]- Answer
> **High dimensionality with many categories.**
> 
> One-hot 为每个 category 创建一列；category 数量大时（如 city、product ID）feature space 爆炸，存储和计算成本剧增。

---

### Part II — Short Answer Questions

*Provide answers in the boxes provided below each question.*

---

**Question 2:** Why is unstructured data important in data engineering? **(2 Marks)**

> [!note]- Answer
> A large portion of useful business information exists as text, images, video, email, and social media — not structured tables. Pipelines must ingest, preprocess, extract features, and analyse these data types before they support ML or analytics.

---
**Question 3:** Discuss the main goals of scalability in distributed data systems, including speed-up and scale-up. Why are these difficult to achieve perfectly in practice? **(2 Marks)**

> [!note]- Answer
> **Speed-up:** adding resources reduces processing time for same data volume.
> **Scale-up:** data size and resources grow together while maintaining performance.
> 
> Perfect scalability is hard because coordination, communication, and synchronisation overhead increase with more nodes.

---
**Question 4:** Why is simply having multiple PostgreSQL servers usually not equivalent to using a parallel database such as Greenplum for large-scale MADlib workloads? **(3 Marks)**

> [!note]- Answer
> Multiple independent PostgreSQL servers require manual partitioning, distributed query planning, cross-node joins, result merging, and fault handling. Greenplum is a shared-nothing parallel DB with coordinated execution — better scalability and integrated data-parallel analytics.

---

<a id="quiz-23"></a>

## Quiz 2-3 — Friday, 22 May, 07 PM

**Tutorial Quiz 2 | Week 7–11**
**Quiz Writing Time: 30 minutes | Total: 10 marks**
**Closed book. No electronic devices permitted.**

---

### Part I — Multiple Choice Questions (1 mark each)

*Tick the box corresponding to the correct answer. Each question carries one mark.*

---

**Question 1A.** Why is TF-IDF often more informative than raw term frequency alone?

- [ ] It preserves sentence structure
- [ ] It only works for images
- [ ] It gives more weight to words common across all documents
- [ ] It reduces the weight of terms that are common across documents

> [!note]- Answer
> **TF-IDF down-weights terms common across all documents.**
> 
> 高频但无区分度的词（如 the, data）IDF 低，权重被降低；有区分度的词权重更高。C 选项说反了。

---
**Question 1B.** A data stream is best described as:

- [ ] A batch file waiting for ETL
- [ ] A fixed-size table stored on disk
- [ ] A normalised relational schema
- [ ] A potentially unbounded sequence of tuples

> [!note]- Answer
> **A potentially unbounded sequence of tuples.**
> 
> Data stream 是持续产生、无固定终点的事件序列（unbounded）。Batch file / fixed table 是 bounded data at rest。

---
**Question 1C.** Why are message processing guarantees difficult to achieve?

- [ ] Because streams are always small
- [ ] Because producers, brokers, and consumers can fail, causing loss or duplication
- [ ] Because SQL does not support streaming
- [ ] Because topics cannot be partitioned

> [!note]- Answer
> **Producers, brokers, and consumers can fail — causing loss or duplication.**
> 
> Exactly-once / at-least-once 保证在分布式 failure 场景下很难实现；需要 idempotency、checkpointing、transactional writes 等机制。

---

### Part II — Short Answer Questions

*Provide answers in the boxes provided below each question.*

---

**Question 2:** Why is feature extraction necessary for text and image data in ML pipelines? **(2 Marks)**

> [!note]- Answer
> ML algorithms require numerical input; raw text and images are unstructured. Text: BoW, TF-IDF, embeddings. Images: colour, gradients, texture, shape, or neural features. This transformation enables classification, similarity search, and other ML tasks.

---
**Question 3:** What is a session window? Provide one challenge in a streaming pipeline. **(2 Marks)**

> [!note]- Answer
> A **session window** groups related events based on activity boundaries (explicit markers or inactivity gaps) — variable-length, useful for user sessions or auctions.
> 
> **Challenge:** Session boundaries depend on event timing; late-arriving events can split or merge sessions incorrectly; requires watermark/lateness handling.

---
**Question 4:** Why can in-database ML tools such as MADlib be more scalable than loading all data into Python with Pandas? **(3 Marks)**

> [!note]- Answer
> MADlib keeps computation close to data inside the DBMS — reduces data movement and avoids fitting entire dataset into application memory. Can exploit DB storage, buffering, and parallel execution. Exporting to Python creates memory bottlenecks and transfer overhead.

---

<a id="quiz-24"></a>

## Quiz 2-4 — Friday, 22 May, 08 PM

**Tutorial Quiz 2 | Week 7–11**
**Quiz Writing Time: 30 minutes | Total: 10 marks**
**Closed book. No electronic devices permitted.**

---

### Part I — Multiple Choice Questions (1 mark each)

*Tick the box corresponding to the correct answer. Each question carries one mark.*

---

**Question 1A.** Which of the following is an example of advanced feature engineering for time-series data?

- [ ] Stop-word removal
- [ ] GPS metadata extraction
- [ ] Binary thresholding only
- [ ] Lag features and rolling averages

> [!note]- Answer
> **Lag features and rolling averages.**
> 
> Time-series feature engineering 包括 lag、rolling mean/std、seasonal decomposition 等。Stop-word removal 是 NLP preprocessing；GPS metadata 是 image/spatial 场景。

---
**Question 1B.** In ML pipelines, what is the strongest reason to keep preprocessing and feature extraction consistent between training and inference?

- [ ] To ensure the model receives inputs in the same feature space it learned from
- [ ] To make slides look cleaner
- [ ] To avoid using storage systems
- [ ] To convert all unstructured data into metadata

> [!note]- Answer
> **Same feature space for training and inference — prevents Training-Serving Skew.**
> 
> 训练和推理使用不同 preprocessing 逻辑会导致 feature distribution 不一致，线上模型 accuracy 下降。

---
**Question 1C.** In a DSMS, queries are typically:

- [ ] One-time and transient
- [ ] Continuous and persistent
- [ ] Only executed at the end of the day
- [ ] Limited to batch tables

> [!note]- Answer
> **Continuous and persistent.**
> 
> DSMS（Data Stream Management System）的 queries 持续运行，实时处理 incoming tuples；不同于 batch 的一次性 query。

---

### Part II — Short Answer Questions

*Provide answers in the boxes provided below each question.*

---

**Question 2:** What is a session window? Provide one challenge in a streaming pipeline. **(2 Marks)**

> [!note]- Answer
> A **session window** is a variable-length window grouping events by activity boundaries (inactivity gaps or explicit markers), useful for modelling user sessions or auctions.
> 
> **Challenge:** Late events can affect session assignment; requires careful watermark and state management.

---
**Question 3:** What is meant by scale-agnostic data management and scale-agnostic data processing? Explain how sharding, replication, and parallel processing contribute. **(2 Marks)**

> [!note]- Answer
> **Scale-agnostic data management:** store/organise data so the system grows smoothly — sharding for performance, replication for availability.
> **Scale-agnostic data processing:** computation parallelised across CPUs/nodes — parallel processing improves performance; sharding and replication support scale and fault tolerance.

---
**Scenario 3:** A company uses an ETL-based data warehouse and wants to migrate to an ELT-based cloud warehouse. What major architectural changes would be required, and why might this migration be difficult? **(3 Marks)**

> [!note]- Answer
> Introduce/expand staging/raw layer; move transformation logic closer to warehouse; redesign schemas and orchestration; update governance, validation, and monitoring.
> 
> Difficult because it affects core data flow, existing dependencies, reporting logic, team responsibilities, and infrastructure design.

---

