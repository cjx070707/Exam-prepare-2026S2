# COMP5339 课堂 Quiz 题目合集
> **来源**：Tutorial Quiz 1-1 ~ 2-4（含 sample answers）  
> **格式**：每份 3 道 MCQ（各 3 小题）+ 简答题，共 10 分  
> **说明**：PDF 提取整理，答案为官方 sample answers

## 目录
- [Quiz 1-1](#quiz-11)
- [Quiz 1-2](#quiz-12)
- [Quiz 1-3](#quiz-13)
- [Quiz 1-4](#quiz-14)
- [Quiz 2-1](#quiz-21)
- [Quiz 2-2](#quiz-22)
- [Quiz 2-3](#quiz-23)
- [Quiz 2-4](#quiz-24)

---

## Quiz 1-1 {#quiz-11}
**Tutorial Quiz 1** · Thursday, 16 April  
*源文件：`COMP5339 - Quiz 1-1 (sample answers).pdf`*
Tutorial Quiz – 1
Thursday, 16 April

### Part I – Multiple Choice Questions

**Question 1:** This question has three parts. Tick the boxes corresponding to each correct answer.
Each question carries one mark.

A. In the “Data Engineering Lifecycle” diagram, why is Storage drawn as a long layer
underneath ingestion → transformation → serving (instead of being a single step)?

- Storage supports all stages (landing raw data, staging transformations, and
serving curated data), and its choice affects performance, cost, and reliability
across the pipeline
- Storage is only used for archiving after analytics are complete
- Storage is mainly for backups and doesn’t affect pipeline design
- Storage is only needed when working with streaming systems


B. When extracting data from a webpage, what is the most important first step?

- Inspecting the webpage structure
- Writing extraction code
- Storing data in a database
- Running the crawler

C. A data engineering team is building a pipeline to ingest data from multiple external APIs
whose structures frequently change (new fields, missing fields, nested variations). Which
design choice is most appropriate?

- Use a strictly normalised relational schema before ingestion
- Use a schema-on-read approach with a document-oriented store
- Use a schema-on-write approach with enforced constraints
- Use a columnar data warehouse with a fixed schema

### Part II – Short Answer Questions
Provide answers in the provided boxes.

**Question 1:** Why is a graph database more suitable than a relational model for this use case?
(2 Marks)
Graph databases efficiently represent relationships such as prerequisites and dependencies
between concepts. They allow fast traversal without complex joins. This makes them ideal
for ontology-driven systems and knowledge graphs where relationships are central.

**Question 2:** Data Acquisition, Cleaning, and Integration

**Scenario 1:** You work at an e-commerce company and ingest order events daily from multiple
source systems. Sometimes an order arrives 2-3 days late, and occasionally the same order
appears twice with identical fields.
Answer the following:
How would you design your ingestion + staging layer to ensure:
1. Non-identical loads (no duplicates), (1 Mark)
2. Correct historical completeness (late arrivals are included), and (1 Mark)
3. Identify a schema change? (1 Mark)

1.
Store the data into the staging area and find any duplicates (i.e., the entire row is
duplicated) before ingesting into a database or storage area
2.
Look for the orders that were completed in the past and include them in their
respective days/dates
3.
Store the base schema in a storage area and compare it with the current schema at
ingestion time


**Scenario 2:** The source team adds a new column (discount) to the orders feed and later
changes the postal_code column type from numeric to string. Your pipeline starts failing.
Answer the following:
What controls and design choices would you put in place to handle schema evolution safely
(both breaking and non-breaking changes) while keeping downstream analytical tables stable?
(2 Marks)


Implement schema validation at ingestion and alert on breaking changes. Use schema
evolution rules: allow additional fields, but fail on incompatible type changes. Store raw
payloads to avoid data loss and map them to a stable schema in staging.

---

## Quiz 1-2 {#quiz-12}
**Tutorial Quiz 1** · Friday, 17 April, at 06 PM  
*源文件：`COMP5339 - Quiz 1-2 (sample answers).pdf`*
Tutorial Quiz – 1
Friday, 17 April, at 06 PM

### Part I – Multiple Choice Questions

**Question 1:** This question has three parts. Tick the boxes corresponding to each correct answer.
Each question carries one mark.

A. Which statement best describes the role of staging in an OLTP → OLAP pipeline?

- Staging tables are the final tables used by BI dashboards; fact/dim tables are just
temporary
- Staging replaces the OLTP system by serving user transactions with high concurrency
- Staging exists only to store aggregated results (e.g., monthly revenue)
- Staging stores a raw or lightly cleaned copy of source data to support reruns,
deduplication, and incremental loading before building fact/dim tables

B. You can either (i) run SQL that filters/aggregates in the DB and return a small result set,
or (ii) bulk-load the whole table into Pandas and process it there. Which is the strongest
technical reason for choosing option (i)?

- Pandas cannot do joins or group-bys
- SQL cannot express aggregations compared to Pandas
- Bulk-loading is always slower, even for small datasets
- DBMS can optimise queries, and bulk-loading requires the full dataset to fit into
memory

C. A data engineering team is ingesting semi-structured data from multiple sources where
fields vary across records. They decide to use a schema-late approach. Which of the
following is the main advantage of this decision?
- Enforces strict consistency across all records
- Reduces storage size compared to relational databases
- Eliminates the need for data validation entirely
- Allows ingestion of heterogeneous data without a predefined schema

### Part II – Short Answer Questions
Provide answers in the provided boxes.

**Scenario 1:** The Table below shows order lines for one customer (note that such orders exist
with several customers). Two dashboards (developed by two different teams) show different
“monthly revenue” numbers. One includes only order status with “Shipped”; the other
includes “Cancelled” and “On Hold”. Both teams claim they are correct.

Answer the following:
How do you enforce consistent metric definitions across the organisation, and what pipeline
components help prevent or detect these inconsistencies (e.g., checks, documentation, semantic
layer, etc.)? (2 Marks)
Define metrics centrally (data catalogue/semantic layer) with agreed filters (e.g., only
status='Shipped'). Publish tables and prevent ad-hoc redefinition by creating views. Add
data tests (for accepted statuses and revenue formula checks) and documentation.
ORDERNUMBER
CUSTOMERNAME
ORDERDATE
STATUS
SALES
20001
Australian Collectors, Co.
1/10/2004
Shipped
3600
20015
Australian Collectors, Co.
1/18/2004
Cancelled
1204
20022
Australian Collectors, Co.
1/25/2004
On Hold
870


**Scenario 2:** A fact table grows to billions of rows. Most queries filter by date and region, but
performance and cost are rising.

**Question 2:** What strategies would you use to improve performance and control cost (e.g.,
partitioning, aggregates), and how do you decide which to implement? (2 Marks)
- If most queries filter by time, then partition by date first.
- If queries also filter heavily by regioof the choicesuct, then cluster/sort on those.
- If the same aggregations power dashboards repeatedly, then materialised views/marts.


**Scenario 3:** Your analysts want near-real-time dashboards. The OLTP database is already
under heavy load. Running large analytical queries against it slows down customer operations.

**Question 3:** What extraction approach would you choose (see options below), and how would
you architect the system so analytical workloads do not impact OLTP performance? Choose
one choice below and justify your selection. (3 Mark)
1. Change Data Capture (CDC), i.e., as soon as the data changes
2. Replication
3. Scheduled extracts
1. I would avoid querying the OLTP database directly for dashboards because
analytical scans and joins can compete with transactional workloads (locks, CPU,
I/O). Instead, I would use CDC (reading the database’s transaction log) to stream
changes into an analytics environment.
2. CDC reads changes from the transaction log rather than running large
joins/aggregations on OLTP tables.
3. OLTP already writes to logs for recovery; CDC just consumes those logs.

---

## Quiz 1-3 {#quiz-13}
**Tutorial Quiz 1** · Friday, 17 April, at 07 PM  
*源文件：`COMP5339 - Quiz 1-3 (sample answers).pdf`*
Tutorial Quiz – 1
Friday, 17 April, at 07 PM

### Part I – Multiple Choice Questions

**Question 1:** This question has three parts. Tick the boxes corresponding to each correct answer.
Each question carries one mark.

A. In a data pipeline, what is the main challenge when extracting data from multiple linked
webpages?

- Data storage
- Network speed
- Maintaining consistent structure across pages
- Visualising the data

B. In a document database (such as MongoDB), relationships between entities can be
represented using embedding or referencing. When is embedding preferred?
- When data is highly normalised
- When related data is frequently accessed together
- When relationships are many-to-many and large
- When strict ACID transactions are required

C. Why are APIs generally preferred over web scraping in data engineering?
- APIs provide structured and stable access to data
- APIs provide unstructured data
- APIs are always free
- APIs require more manual effort

### Part II – Short Answer Questions

**Scenario 1:** You are given a webpage from an online unit allocation, presented in an HTML
structure below. You need to extract this data for a data warehouse.
Answer the following:
1. Identify the attributes and write at least one record (1 Mark)
2. Which elements will you target for extraction? (1 Mark)


Attributes: title, code, lecturer, enrolments
Record: Data Engineering, COMP5339, Imdad, 450
Element to target for extraction: div id = "course"


**Question 2:** Suppose the webpage changes to (compared to the initial outline, above) the
following:

What data quality issues may arise, and how would you handle them in a pipeline? (2 Marks)

Issues:
- The numeric field under the "enrolments" becomes text
- Inconsistent format

How to handle them:
- Apply transformation to extract numeric values
- Standardise format (e.g., remove “students”) and enforce schema validation


**Question 3:** Suppose the webpage structure changes to (compared to the initial structure,
above):

1. What has changed? (1 Mark)
2. What problem does this cause, and how would you make your pipeline more robust?
(1 Mark)
What has changed: class = "course" has now changed to class = "course-item"

Part 2 - Sample answer:
Problem:
- Extraction logic breaks due to dependency on class name
Solutions:
- Add validation checks
- Implement monitoring/alerts
- Design adaptable extraction rules


**Question 4:** The website owner later provides an API that returns structured course data. Will
you switch from scraping to API? Justify your answer. (1 Mark)

---

## Quiz 1-4 {#quiz-14}
**Tutorial Quiz 1** · Friday, 17 April, at 08 PM  
*源文件：`COMP5339 - Quiz 1-4 (sample answers).pdf`*
Tutorial Quiz – 1
Friday, 17 April, at 08 PM

### Part I – Multiple Choice Questions

**Question 1:** This question has three parts. Tick the boxes corresponding to each correct answer.
Each question carries one mark.

A. A data engineering team is building a pipeline to ingest data from multiple external APIs
whose structures frequently change (new fields, missing fields, nested variations). Which
design choice is most appropriate?

- Use a strictly normalised relational schema before ingestion
- Use a schema-on-read approach with a document-oriented store
- Use a schema-on-write approach with enforced constraints
- Use a columnar data warehouse with a fixed schema

B. Which statement best describes the role of staging in an OLTP → OLAP pipeline?

- Staging tables are the final tables used by BI dashboards; fact/dim tables are just
temporary
- Staging replaces the OLTP system by serving user transactions with high concurrency
- Staging exists only to store aggregated results (e.g., monthly revenue)
- Staging stores a raw or lightly cleaned copy of source data to support reruns,
deduplication, and incremental loading before building fact/dim tables

C. You can either (i) run SQL that filters/aggregates in the DB and return a small result set,
or (ii) bulk-load the whole table into Pandas and process it there. Which is the strongest
technical reason for choosing option (i)?

- Pandas cannot do joins or group-bys
- SQL cannot express aggregations compared to Pandas
- Bulk-loading is always slower, even for small datasets
- DBMS can optimise queries, and bulk-loading requires the full dataset to fit into
memory

### Part II – Short Answer Questions
Provide answers in the provided boxes.

**Scenario 1:** A fact table grows to billions of rows. Most queries filter by date and region, but
performance and cost are rising.

**Question 1:** What strategies would you use to improve performance and control cost (e.g.,
partitioning, aggregates), and how do you decide which to implement? (3 Marks)
Define metrics centrally (data catalogue/semantic layer) with agreed filters (e.g., only
status='Shipped'). Publish tables and prevent ad-hoc redefinition by creating views. Add data
tests (for accepted statuses and revenue formula checks) and documentation.

**Scenario 2:** Your analysts want near-real-time dashboards. The OLTP database is already
under heavy load. Running large analytical queries against it slows down customer operations.

**Question 2:** What extraction approach would you choose (see options below), and how would
you architect the system so analytical workloads do not impact OLTP performance? Choose
one choice below and justify your selection. (2 Marks)
1. Change Data Capture (CDC), i.e., as soon as the data changes
2. Replication
3. Scheduled extracts
1. I would avoid querying the OLTP database directly for dashboards because
analytical scans and joins can compete with transactional workloads (locks, CPU,
I/O). Instead, I would use CDC (reading the database’s transaction log) to stream
changes into an analytics environment.
2. - CDC reads changes from the transaction log rather than running large
joins/aggregations on OLTP tables.
3. - OLTP already writes to logs for recovery; CDC just consumes those logs.

**Scenario 3:** You are given a webpage from an online unit allocation, presented in an HTML
structure below. You need to extract this data for a data warehouse.
Answer the following:
1. Identify the attributes and write at least one record (1 Mark)
2. Which elements will you target for extraction? (1 Mark)


Attributes: title, code, lecturer, enrolments
Record: Data Engineering, COMP5339, Imdad, 450

Element to target for extraction: div id = "course"

---

## Quiz 2-1 {#quiz-21}
**Tutorial Quiz 2** · Thursday, 21 May  
*源文件：`COMP5339 - Quiz 2-1 (sample answers).pdf`*
Tutorial Quiz – 2
Thursday, 21 May

### Part I – Multiple Choice Questions

**Question 1:** This question has three parts. Tick the boxes corresponding to each correct answer.
Each question carries one mark.

A. From a data engineering perspective, what is the main extra requirement for a supervised
learning pipeline compared with an unsupervised learning pipeline?

- It must always use image data
- It does not require preprocessing
- It only works on structured data
- It must include ground-truth labels linked correctly to features

B. Why is metadata analysis attractive in image pipelines?

- A. It is always more accurate than image content
- It can provide useful structured information without full image-content analysis
- It avoids all storage requirements
- It replaces feature extraction completely in every case

C. Which of the following is an example of a transactional data stream?

- Credit card purchases by customers
- Temperature readings from sensors
- Road traffic speed measurements
- Weather history reports

### Part II – Short Answer Questions
Provide answers in the provided boxes.

**Question 1:** What is the main purpose of tokenisation in text preprocessing? What are the
storage options for storing the output of tokenisation? (2 Marks)
Tokenisation mainly splits raw text into smaller units such as words, subwords, or terms so
the text can be processed and converted into features for analysis or machine learning.
Storage options include:
- 
As text/JSON documents for flexible storage of token lists
- 
In relational tables with one row per document or one row per token
- 
As sparse matrices / document-term matrices when preparing features for ML

**Question 2:** Why is a traditional DBMS not sufficient for many stream processing
applications? (2 Marks)
A traditional DBMS is mainly designed for data at rest, where queries are executed over
stored data. Stream applications require continuous processing of live data with low delay,
which a DBMS does not handle as naturally as a stream processing system.


**Scenario 2:** Explain the difference between scale-up and scale-out in scalable data
engineering. Why is scale-out generally preferred for big data systems? (3 Marks)
Scale-up means increasing the power of a single machine by adding more CPU, memory,
or storage. Scale-out means adding more machines or nodes to a cluster. Scale-out is
generally preferred for big data systems because a single server has physical and cost
limits, while clusters can grow more easily and support shared-nothing distributed
processing.


EXTRA SHEET

---

## Quiz 2-2 {#quiz-22}
**Tutorial Quiz 2** · Friday, 22 May, at 06 PM  
*源文件：`COMP5339 - Quiz 2-2 (sample answers).pdf`*
Tutorial Quiz – 2
Friday, 22 May, at 06 PM

### Part I – Multiple Choice Questions

**Question 1:** This question has three parts. Tick the boxes corresponding to each correct answer.
Each question carries one mark.

A. In a supervised text-classification pipeline, which sequence is most appropriate?

- Raw text → feature extraction → labels + features → model training
- Raw text → clustering → labels → storage
- Raw text → image similarity → prediction
- Raw text → regression → tokenisation

B. In a publish/subscribe system, publishers send messages to:
- Specific consumers directly
- Window operators only
- Relational tables only
- Topics managed by a broker

C. Why might one-hot encoding become problematic in a production pipeline?

- It may create very high-dimensional data when there are categories
- It cannot represent categories
- It works only on images
- It always causes label leakage

### Part II – Short Answer Questions
Provide answers in the provided boxes.

**Question 1:** Why is unstructured data important in data engineering? (2 Marks)
Unstructured data is important because a very large portion of useful business information
exists in forms such as text, images, video, email, and social media, rather than in structured
tables. From a data engineering perspective, this means pipelines must be designed to
ingest, preprocess, extract features from, and analyse these data types before they can
support machine learning or analytics.

**Question 2:** Discuss the main goals of scalability in distributed data systems, including
speed-up and scale-up. Why are these difficult to achieve perfectly in practice? (2 Marks)
Speed-up means that adding more resources should reduce processing time for the same
amount of data. Scale-up means that if both data size and resources grow together, the
system should maintain similar performance. In practice, perfect scalability is difficult
because coordination, communication, and synchronisation overhead increase as more nodes
are added.


**Question 3:** Why is simply having multiple PostgreSQL servers usually not equivalent to
using a parallel database such as Greenplum for large-scale MADlib workloads? (3
Marks)
Multiple PostgreSQL servers are independent systems, so partitioning, distributed query
planning, cross-node joins, merging results, and fault handling must be managed manually.
Greenplum, in contrast, is designed as a shared-nothing parallel database with coordinated
execution across nodes. Therefore, Greenplum usually provides better scalability and more
integrated support for data-parallel analytics.

EXTRA SHEET

---

## Quiz 2-3 {#quiz-23}
**Tutorial Quiz 2** · Friday, 22 May, at 07 PM  
*源文件：`COMP5339 - Quiz 2-3 (sample answers).pdf`*
Tutorial Quiz – 2
Friday, 22 May, at 07 PM

### Part I – Multiple Choice Questions

**Question 1:** This question has three parts. Tick the boxes corresponding to each correct answer.
Each question carries one mark.

A. Why is TF-IDF often more informative than raw term frequency alone?

- It preserves sentence structure
- It only works for images
- It gives more weight to words common across all documents
- It reduces the weight of terms that are common across documents

B. A data stream is best described as:

- A batch file waiting for ETL
- A fixed-size table stored on disk
- A normalised relational schema
- A potentially unbounded sequence of tuples

C. Why are message processing guarantees difficult to achieve?

- A. Because streams are always small
- Because producers, brokers, and consumers can fail, causing loss or duplication
- Because SQL does not support streaming
- Because topics cannot be partitioned


### Part II – Short Answer Questions

**Question 1:** Why is feature extraction necessary for text and image data in ML
pipelines/workflows? (2 Marks)
Feature extraction is necessary because most machine learning algorithms require numerical
input, while raw text and images are unstructured. In text, methods such as Bag-of-Words,
TF-IDF, and embeddings are used; in images, colour, gradients, texture, shape, or learned
neural features can be extracted. This transformation makes the data usable for classification,
similarity search, and other ML tasks.

**Question 2:** What is a session window? Provide one challenge in a streaming pipeline. (2
Marks)
A session window is a variable-length window that groups related events based on activity
boundaries, such as explicit markers or inactivity gaps. It is useful for modelling sessions
such as auctions or user activity periods.


**Question 3:** Why can in-database machine learning tools such as MADlib be more scalable
than the standard approach of loading all data into Python with Pandas for analysis? (3
Mark)
MADlib keeps computation close to the data inside the DBMS, reducing data movement and
avoiding the need to fit the entire dataset into application memory. It can also exploit
database storage, buffering, and in some systems parallel execution. In contrast, exporting
data to Python can create memory bottlenecks, data transfer overhead, and limited scalability.


EXTRA SHEET

---

## Quiz 2-4 {#quiz-24}
**Tutorial Quiz 2** · Friday, 22 May, at 08 PM  
*源文件：`COMP5339 - Quiz 2-4 (sample answers).pdf`*
Tutorial Quiz – 2
Friday, 22 May, at 08 PM

### Part I – Multiple Choice Questions

**Question 1:** This question has three parts. Tick the boxes corresponding to each correct answer.
Each question carries one mark.

A. Which of the following is an example of advanced feature engineering for time-series
data?

- Stop-word removal
- GPS metadata extraction
- Binary thresholding only
- Lag features and rolling averages

B. In the ML pipelines, what is the strongest reason to keep preprocessing and feature
extraction consistent between training and inference?

- To ensure the model receives inputs in the same feature space it learned from
- To make slides look cleaner
- To avoid using storage systems
- To convert all unstructured data into metadata

C. In a DSMS, queries are typically:

- One-time and transient
- Continuous and persistent
- Only executed at the end of the day
- Limited to batch tables


### Part II – Short Answer Questions
Provide answers in the provided boxes.

**Question 1:** What is a session window? Provide one challenge in a streaming pipeline. (2
Marks)
A session window is a variable-length window that groups related events based on activity
boundaries, such as explicit markers or inactivity gaps. It is useful for modelling sessions
such as auctions or user activity periods.

**Question 2:** What is meant by scale-agnostic data management and scale-agnostic data
processing? Explain how sharding, replication, and parallel processing contribute to these
goals. (2 Marks)
Scale-agnostic data management means storing and organising data so the system can grow
smoothly, using techniques such as sharding for performance and replication for availability.
Scale-agnostic data processing means computation can be parallelised across many CPUs or
nodes. Parallel processing improves performance, while sharding and replication help the
system scale and remain available under failures.

**Scenario 3:** A company currently uses an ETL-based data warehouse and wants to migrate to
an ELT-based cloud warehouse. What major architectural changes would be required, and
why might this migration be difficult from a data engineering perspective? (3 Mark)
The company would need to introduce or expand a staging/raw layer, move transformation
logic closer to the warehouse, redesign schemas and orchestration workflows, and update
governance, validation, and monitoring processes. The migration is difficult because it affects
the core data flow, existing dependencies, reporting logic, team responsibilities, and
infrastructure design.

EXTRA SHEET

---
