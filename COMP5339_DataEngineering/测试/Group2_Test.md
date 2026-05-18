# Group 2 Test — Storage Systems

**Scope: Week 3 (Databases, Warehouses, Lakes) + Week 5 (NoSQL & Semi-structured)**

**Total: 60 marks | Suggested time: 45 minutes**

---

## Section A — Multiple Choice (2 marks each, 20 marks total)

**Q1.** Which of the following scenarios best fits an **OLAP** system?

- A. A customer completes a purchase on an e-commerce site
- B. An ATM processes a cash withdrawal
- C. An analyst queries three years of regional sales trends
- D. An employee updates their personal profile in an HR system

<details>
<summary>Answer</summary>

**C** — OLAP (Online Analytical Processing) is designed for large-scale, historical, aggregation-heavy queries by analysts. Options A, B, and D are short, transactional operations on current data — typical OLTP workloads.

</details>

---

**Q2.** In a Star Schema, the table `Sales(Market_Id, Product_Id, Time_Id, Sales_Amt)` is a:

- A. Dimension Table
- B. Fact Table
- C. Bridge Table
- D. Lookup Table

<details>
<summary>Answer</summary>

**B** — A **Fact Table** stores measurable business events (`Sales_Amt`) and holds foreign keys to each Dimension Table (`Market_Id`, `Product_Id`, `Time_Id`). Dimension Tables store descriptive attributes about those dimensions.

</details>

---

**Q3.** What is the key difference between **ETL** and **ELT**?

- A. ETL is used in cloud environments; ELT is used on-premises
- B. ETL transforms data before loading; ELT loads raw data first, then transforms inside the warehouse
- C. ETL supports unstructured data; ELT only handles structured data
- D. ELT requires an external transformation tool; ETL does not

<details>
<summary>Answer</summary>

**B** — ETL = Extract → Transform → Load (transformation happens outside the destination). ELT = Extract → Load → Transform (raw data is loaded first, transformation happens inside the data warehouse or lake using its own compute power). ELT is common in modern cloud data warehouses like BigQuery and Snowflake.

</details>

---

**Q4.** What is the most important distinction between a **Data Lake** and a **Data Warehouse**?

- A. A Data Lake can only store structured data
- B. A Data Lake uses schema-on-read; a Data Warehouse uses schema-on-write
- C. A Data Warehouse stores raw data; a Data Lake stores refined data
- D. A Data Lake does not support SQL queries

<details>
<summary>Answer</summary>

**B** — **Schema-on-read** means structure is defined when data is queried (flexible, but may be messy). **Schema-on-write** means structure is enforced when data is loaded (rigid but clean). Data Lakes (HDFS, S3) use schema-on-read; Data Warehouses (Snowflake, BigQuery) enforce schema-on-write.

</details>

---

**Q5.** In an XML DTD, what does `(name, age?)` mean?

- A. Both `name` and `age` must appear, in that order
- B. `name` must appear exactly once; `age` is optional (zero or one occurrence)
- C. Either `name` or `age` must appear (mutually exclusive)
- D. `name` appears zero or more times; `age` appears exactly once

<details>
<summary>Answer</summary>

**B** — In DTD syntax: `?` = zero or one (optional); `*` = zero or more; `+` = one or more; no symbol = exactly once. The comma means the elements must appear in sequence.

</details>

---

**Q6.** What does the following MongoDB query do?

```javascript
db.students.find({ age: { $gt: 20 } }, { name: 1, address: 1 })
```

- A. Finds students older than 20 and returns all fields
- B. Finds students older than 20 and returns only `name` and `address`
- C. Inserts a record with `age > 20` including `name` and `address`
- D. Updates `name` and `address` for students older than 20

<details>
<summary>Answer</summary>

**B** — In MongoDB's `find()`, the first argument is the **filter** (`{ age: { $gt: 20 } }`) and the second is the **projection** (`{ name: 1, address: 1 }`), which specifies which fields to return. Setting a field to `1` includes it; `0` excludes it.

</details>

---

**Q7.** Compared to a relational database, a graph database (e.g., Neo4j) excels at:

- A. Large-scale numerical aggregations (SUM / AVG)
- B. Complex multi-table JOIN operations
- C. Multi-hop relationship traversals (e.g., "friends of friends")
- D. High-volume bulk INSERT operations

<details>
<summary>Answer</summary>

**C** — Graph databases store relationships as first-class citizens (edges), making multi-hop traversals O(1) per hop regardless of dataset size. Relational databases must perform repeated, expensive JOIN operations for the same task, which degrades rapidly as hops increase.

</details>

---

**Q8.** Which NoSQL database type is best suited for storing **social network relationships**?

- A. Document Store
- B. Wide Column Store
- C. Graph Database
- D. Time Series Database

<details>
<summary>Answer</summary>

**C** — Social networks are fundamentally about relationships between entities (users, posts, likes). Graph databases model nodes and edges natively, making friend recommendations, shortest-path queries, and influence analysis highly efficient.

</details>

---

**Q9.** A "Valid" XML document means it is:

- A. Syntactically well-formed only (all tags match and are properly closed)
- B. Well-formed AND conforms to a DTD or XML Schema definition
- C. Correctly rendered by any modern browser
- D. Semantically meaningful in its business context

<details>
<summary>Answer</summary>

**B** — **Well-formed** = satisfies XML syntax rules (proper nesting, closed tags, quoted attributes). **Valid** = well-formed **plus** the structure and content conform to a declared DTD or XML Schema. A document can be well-formed but not valid.

</details>

---

**Q10.** Which of the following statements about MongoDB is correct?

- A. MongoDB requires a fixed schema to be defined before inserting data
- B. All documents in a collection must have the same structure
- C. MongoDB stores documents in JSON format and supports nested structures
- D. MongoDB uses SQL as its query language

<details>
<summary>Answer</summary>

**C** — MongoDB is schema-late (no upfront schema required), documents within the same collection can have different structures, data is stored as BSON (binary JSON), and the query language is JavaScript-based — not SQL.

</details>

---

## Section B — Short Answer (8 marks each, 32 marks total)

**Q11.** Compare OLTP and OLAP systems across three dimensions: **read/write patterns**, **query characteristics**, and **data volume**. Give one typical example of each. (8 marks)

<details>
<summary>Answer</summary>

| Dimension | OLTP | OLAP |
|-----------|------|------|
| Read/write pattern | Frequent INSERT / UPDATE / DELETE on individual rows; point queries by primary key | Bulk ETL/ELT loads; large aggregation scans (COUNT, SUM, AVG across millions of rows) |
| Query characteristics | Short, predefined, low-latency transactions | Complex, ad-hoc analytical queries by data analysts; may run for seconds or minutes |
| Data volume | GB to TB (current operational data) | TB to PB (historical records spanning years) |

*OLTP example*: A bank's transaction processing system — each ATM withdrawal is a discrete, immediate transaction.

*OLAP example*: A retail data warehouse — analysts query year-on-year sales growth by product category across all regions.

</details>

---

**Q12.** Describe the structure of a **Star Schema**. Explain what a Fact Table and a Dimension Table each store and how they relate to each other. Use a hypothetical e-commerce data warehouse as an example. (8 marks)

<details>
<summary>Answer</summary>

**Structure**:
- A **Fact Table** sits at the centre. It stores measurable business events (facts) and holds foreign keys pointing to each surrounding Dimension Table. Facts are typically numeric and additive (e.g., revenue, quantity).
- **Dimension Tables** surround the fact table. Each describes one aspect (dimension) of a fact — who, what, when, where. They contain descriptive, textual attributes.
- The Fact Table links to Dimension Tables via foreign keys, forming a star-like shape.

**E-commerce example**:

```
Fact Table:
  Orders(order_id, customer_id, product_id, time_id, region_id, order_amount, quantity)

Dimension Tables:
  Customer(customer_id, name, age, membership_tier, email)
  Product(product_id, name, category, brand, unit_price)
  Time(time_id, date, week, month, quarter, year)
  Region(region_id, city, state, country)
```

To answer "total revenue by product category in Q1 2025", you JOIN `Orders` with `Product` (for category) and `Time` (for Q1 2025), then SUM `order_amount`.

</details>

---

**Q13.** Explain why a Data Lake can easily become a **"data swamp"**. How do organisations typically combine a Data Lake and a Data Warehouse in practice? (8 marks)

<details>
<summary>Answer</summary>

**Why Data Lakes become swamps**:
- Data is loaded with no enforced schema (schema-on-read), so raw files accumulate with inconsistent formats and no documentation
- Without a metadata catalogue, users cannot discover what data exists, what it means, or whether it is trustworthy
- No data quality checks at ingestion mean corrupted or duplicated records mix with valid data
- Over time, the lake fills with data nobody maintains, understands, or uses — becoming effectively inaccessible

**Practical combination**:
1. **Raw ingestion layer (Data Lake — HDFS/S3)**: All raw data lands here first, in its original format. Nothing is discarded. This preserves full history and supports future re-processing.
2. **ETL/ELT pipeline**: Data is cleaned, standardised, and modelled (e.g., into a Star Schema).
3. **Curated layer (Data Warehouse — Snowflake/BigQuery)**: Refined, business-ready tables are stored here for BI tools and analysts.

This split gives the flexibility of a lake (store everything cheaply) with the reliability and performance of a warehouse (query clean, structured data efficiently).

</details>

---

**Q14.** Compare a **relational database (RDBMS)** and a **graph database** across three dimensions: data model, query language, and performance advantage. When should you prefer a graph database? (8 marks)

<details>
<summary>Answer</summary>

| Dimension | RDBMS (e.g., PostgreSQL) | Graph DB (e.g., Neo4j) |
|-----------|--------------------------|------------------------|
| Data model | Tables with rows and columns; relationships expressed via foreign keys | Nodes (entities) + Edges (relationships) + Properties; relationships are stored explicitly |
| Query language | SQL | Cypher (Neo4j), SPARQL, Gremlin |
| Performance advantage | ACID transactions; efficient bulk aggregations; well-optimised for structured, tabular data | Multi-hop graph traversal in O(1) per hop; avoids costly repeated JOINs |

**When to prefer a graph database**:
- The core problem involves traversing **relationships** rather than aggregating values
- Typical use cases: social network friend recommendations, fraud detection (transaction chains), knowledge graphs, network topology analysis, recommendation engines
- Query pattern example: "Find all users who purchased the same product as users who follow User X" — trivial in a graph, exponentially expensive in SQL JOINs

</details>

---

## Section C — Code Reading (8 marks)

**Q15.** Read the following code and answer the questions below.

```python
import psycopg2
import pandas as pd

conn = psycopg2.connect("dbname=sales user=analyst password=secret")
cursor = conn.cursor()

cursor.execute(
    "SELECT product_id, SUM(sales_amt) AS total FROM sales WHERE region = %s GROUP BY product_id",
    ('Sydney',)
)

rows = cursor.fetchall()
df = pd.DataFrame(rows, columns=['product_id', 'total'])
df_sorted = df.sort_values('total', ascending=False).head(5)
print(df_sorted)
conn.close()
```

**(a)** What is the role of `%s` in the SQL string? Why is parameterised querying preferred over string concatenation? (2 marks)

<details>
<summary>Answer</summary>

`%s` is a **parameter placeholder**. psycopg2 safely binds the value `'Sydney'` from the tuple `('Sydney',)` to the placeholder before sending the query to the database.

Parameterised queries prevent **SQL injection attacks** — if the value came from user input and was concatenated directly into the string (e.g., `f"... WHERE region = '{user_input}'"`) an attacker could inject malicious SQL (e.g., `'; DROP TABLE sales; --`). Parameterisation escapes the value properly, treating it as data rather than executable SQL.

</details>

**(b)** What type does `cursor.fetchall()` return? (1 mark)

<details>
<summary>Answer</summary>

A **list of tuples** — each tuple represents one row of the result set, with column values as elements.

</details>

**(c)** Describe the full flow of this script from database connection to final output. (3 marks)

<details>
<summary>Answer</summary>

1. Opens a connection to the PostgreSQL database `sales`
2. Executes a SQL query that filters records to the Sydney region, groups by `product_id`, and computes the total sales amount per product
3. Retrieves all result rows with `fetchall()`
4. Wraps the rows in a Pandas DataFrame with column names `product_id` and `total`
5. Sorts the DataFrame by `total` in descending order and keeps the top 5 rows
6. Prints those 5 rows, then closes the database connection

</details>

**(d)** Does this code demonstrate "push compute into the DBMS" or "pull all data into Python"? Explain. (2 marks)

<details>
<summary>Answer</summary>

**Push compute into the DBMS.** The SQL performs both filtering (`WHERE region = 'Sydney'`) and aggregation (`GROUP BY product_id`, `SUM(sales_amt)`) inside the database. Python receives only the aggregated result (one row per product), not the entire `sales` table. This is efficient: the database uses its indexes and query optimiser, and minimal data crosses the network boundary.

</details>
