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

> [!note]- Answer
> **C** — OLAP is designed for large-scale, historical, aggregation-heavy queries by analysts. Options A, B, and D are short, transactional operations on current data — typical OLTP workloads.

---

**Q2.** In a Star Schema, the table `Sales(Market_Id, Product_Id, Time_Id, Sales_Amt)` is a:

- A. Dimension Table
- B. Fact Table
- C. Bridge Table
- D. Lookup Table

> [!note]- Answer
> **B** — A **Fact Table** stores measurable business events (`Sales_Amt`) and holds foreign keys to each Dimension Table. Dimension Tables store descriptive attributes about those dimensions.

---

**Q3.** What is the key difference between **ETL** and **ELT**?

- A. ETL is used in cloud environments; ELT is used on-premises
- B. ETL transforms data before loading; ELT loads raw data first, then transforms inside the warehouse
- C. ETL supports unstructured data; ELT only handles structured data
- D. ELT requires an external transformation tool; ETL does not

> [!note]- Answer
> **B** — ETL = Extract → Transform → Load (transformation happens outside the destination). ELT = Extract → Load → Transform (raw data is loaded first, transformation happens inside the data warehouse using its own compute). ELT is common in modern cloud warehouses like BigQuery and Snowflake.

---

**Q4.** What is the most important distinction between a **Data Lake** and a **Data Warehouse**?

- A. A Data Lake can only store structured data
- B. A Data Lake uses schema-on-read; a Data Warehouse uses schema-on-write
- C. A Data Warehouse stores raw data; a Data Lake stores refined data
- D. A Data Lake does not support SQL queries

> [!note]- Answer
> **B** — **Schema-on-read** means structure is defined when data is queried (flexible, but may be messy). **Schema-on-write** means structure is enforced when data is loaded (rigid but clean). Data Lakes (HDFS, S3) use schema-on-read; Data Warehouses (Snowflake, BigQuery) enforce schema-on-write.

---

**Q5.** In an XML DTD, what does `(name, age?)` mean?

- A. Both `name` and `age` must appear, in that order
- B. `name` must appear exactly once; `age` is optional (zero or one occurrence)
- C. Either `name` or `age` must appear (mutually exclusive)
- D. `name` appears zero or more times; `age` appears exactly once

> [!note]- Answer
> **B** — In DTD syntax: `?` = zero or one (optional); `*` = zero or more; `+` = one or more; no symbol = exactly once. The comma means the elements must appear in that sequence.

---

**Q6.** What does the following MongoDB query do?

```javascript
db.students.find({ age: { $gt: 20 } }, { name: 1, address: 1 })
```

- A. Finds students older than 20 and returns all fields
- B. Finds students older than 20 and returns only `name` and `address`
- C. Inserts a record with `age > 20` including `name` and `address`
- D. Updates `name` and `address` for students older than 20

> [!note]- Answer
> **B** — The first argument is the **filter** (`{ age: { $gt: 20 } }`); the second is the **projection** (`{ name: 1, address: 1 }`), which specifies which fields to return. Setting a field to `1` includes it.

---

**Q7.** Compared to a relational database, a graph database (e.g., Neo4j) excels at:

- A. Large-scale numerical aggregations (SUM / AVG)
- B. Complex multi-table JOIN operations
- C. Multi-hop relationship traversals (e.g., "friends of friends")
- D. High-volume bulk INSERT operations

> [!note]- Answer
> **C** — Graph databases store relationships as first-class citizens (edges), making multi-hop traversals O(1) per hop. Relational databases must perform repeated, expensive JOIN operations for the same task, which degrades rapidly as hops increase.

---

**Q8.** Which NoSQL type is best suited for storing **social network relationships**?

- A. Document Store
- B. Wide Column Store
- C. Graph Database
- D. Time Series Database

> [!note]- Answer
> **C** — Social networks are fundamentally about relationships between entities. Graph databases model nodes and edges natively, making friend recommendations and shortest-path queries highly efficient.

---

**Q9.** A "Valid" XML document means it is:

- A. Syntactically well-formed only (all tags match and are properly closed)
- B. Well-formed AND conforms to a DTD or XML Schema definition
- C. Correctly rendered by any modern browser
- D. Semantically meaningful in its business context

> [!note]- Answer
> **B** — **Well-formed** = satisfies XML syntax rules (proper nesting, closed tags, quoted attributes). **Valid** = well-formed **plus** the structure and content conform to a declared DTD or XML Schema. A document can be well-formed but not valid.

---

**Q10.** Which of the following statements about MongoDB is correct?

- A. MongoDB requires a fixed schema to be defined before inserting data
- B. All documents in a collection must have the same structure
- C. MongoDB stores documents in JSON format and supports nested structures
- D. MongoDB uses SQL as its query language

> [!note]- Answer
> **C** — MongoDB is schema-late (no upfront schema required). Documents within the same collection can have different structures. Data is stored as BSON (binary JSON). The query language is JavaScript-based, not SQL.

---

## Section B — Short Answer (8 marks each, 32 marks total)

**Q11.** Compare OLTP and OLAP systems across three dimensions: **read/write patterns**, **query characteristics**, and **data volume**. Give one typical example of each. (8 marks)

> [!note]- Answer
> | Dimension | OLTP | OLAP |
> |-----------|------|------|
> | Read/write pattern | Frequent INSERT/UPDATE/DELETE on individual rows; point queries by primary key | Bulk ETL/ELT loads; large aggregation scans (SUM, COUNT, AVG over millions of rows) |
> | Query characteristics | Short, predefined, low-latency transactions | Complex, ad-hoc analytical queries; may run for seconds or minutes |
> | Data volume | GB to TB (current operational data) | TB to PB (multi-year historical records) |
> 
> *OLTP example*: A bank's transaction processing system — each ATM withdrawal is a discrete, immediate transaction.
> 
> *OLAP example*: A retail data warehouse — analysts query year-on-year sales growth by product category across all regions.

---

**Q12.** Describe the structure of a **Star Schema**. Explain what a Fact Table and Dimension Tables store and how they relate. Use a hypothetical e-commerce data warehouse as an example. (8 marks)

> [!note]- Answer
> **Structure**:
> - A **Fact Table** sits at the centre. It stores measurable business events (facts) and holds foreign keys pointing to each Dimension Table. Facts are typically numeric and additive (e.g., revenue, quantity).
> - **Dimension Tables** surround the fact table, each describing one aspect of a fact — who, what, when, where.
> - The Fact Table links to Dimension Tables via foreign keys, forming a star-like shape.
> 
> **E-commerce example**:
> ```
> Fact:    Orders(order_id, customer_id, product_id, time_id, region_id, order_amount)
> Dims:    Customer(customer_id, name, age, email)
>          Product(product_id, name, category, unit_price)
>          Time(time_id, date, month, quarter, year)
>          Region(region_id, city, state, country)
> ```
> To answer "total revenue by product category in Q1 2025", JOIN `Orders` with `Product` and `Time`, then SUM `order_amount`.

---

**Q13.** Explain why a Data Lake can easily become a **"data swamp"**. How do organisations typically combine a Data Lake and a Data Warehouse in practice? (8 marks)

> [!note]- Answer
> **Why Data Lakes become swamps**:
> - Data is loaded with no enforced schema (schema-on-read), so raw files accumulate with inconsistent formats and no documentation.
> - Without a metadata catalogue, users cannot discover what data exists or whether it is trustworthy.
> - No data quality checks at ingestion mean corrupted or duplicated records mix with valid data.
> - Over time, the lake fills with data nobody maintains or understands — effectively inaccessible.
> 
> **Practical combination**:
> 1. **Data Lake (HDFS/S3)**: All raw data lands here first, in its original format. Nothing is discarded.
> 2. **ETL/ELT pipeline**: Data is cleaned, standardised, and modelled.
> 3. **Data Warehouse (Snowflake/BigQuery)**: Refined, business-ready tables are stored here for BI and analysts.
> 
> This gives the flexibility of a lake (store everything cheaply) with the reliability of a warehouse (query clean, structured data efficiently).

---

**Q14.** Compare a **relational database (RDBMS)** and a **graph database** across three dimensions: data model, query language, and performance advantage. When should you prefer a graph database? (8 marks)

> [!note]- Answer
> | Dimension | RDBMS (e.g., PostgreSQL) | Graph DB (e.g., Neo4j) |
> |-----------|--------------------------|------------------------|
> | Data model | Tables with rows and columns; relationships via foreign keys | Nodes + Edges + Properties; relationships are stored explicitly |
> | Query language | SQL | Cypher (Neo4j), SPARQL, Gremlin |
> | Performance advantage | ACID transactions; efficient bulk aggregations | Multi-hop graph traversal in O(1) per hop; avoids costly repeated JOINs |
> 
> **Prefer a graph database when**: the core problem involves traversing **relationships** rather than aggregating values — e.g., social network friend recommendations, fraud detection (transaction chains), knowledge graphs, or network topology analysis.

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

**(a)** What is the role of `%s`? Why is parameterised querying preferred over string concatenation? (2 marks)

> [!note]- Answer
> `%s` is a **parameter placeholder**. psycopg2 safely binds the value `'Sydney'` to the placeholder before sending the query to the database.
> 
> Parameterised queries prevent **SQL injection attacks** — if the value came from user input and was concatenated directly (e.g., `f"WHERE region = '{user_input}'"`) an attacker could inject malicious SQL. Parameterisation escapes the value properly, treating it as data, not executable SQL.

**(b)** What type does `cursor.fetchall()` return? (1 mark)

> [!note]- Answer
> A **list of tuples** — each tuple represents one row of the result set, with column values as elements.

**(c)** Describe the full flow of this script from connection to final output. (3 marks)

> [!note]- Answer
> 1. Opens a connection to the PostgreSQL database `sales`
> 2. Executes SQL that filters to Sydney, groups by `product_id`, and computes total sales per product
> 3. Retrieves all result rows with `fetchall()`
> 4. Wraps rows in a DataFrame with columns `product_id` and `total`
> 5. Sorts by `total` descending, keeps the top 5, prints them, then closes the connection

**(d)** Does this code demonstrate "push compute into the DBMS" or "pull all data into Python"? Explain. (2 marks)

> [!note]- Answer
> **Push compute into the DBMS.** The SQL performs both filtering (`WHERE region = 'Sydney'`) and aggregation (`GROUP BY`, `SUM`) inside the database. Python receives only the aggregated result — one row per product — not the entire `sales` table. This is efficient: the database uses its indexes and query optimiser, and minimal data crosses the network boundary.
