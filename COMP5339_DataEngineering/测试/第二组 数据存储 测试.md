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
> **C** — OLAP 面向大规模历史数据的聚合分析查询，由分析师使用。选项 A、B、D 都是对当前数据的短暂事务操作，属于 OLTP 场景。

---

**Q2.** In a Star Schema, the table `Sales(Market_Id, Product_Id, Time_Id, Sales_Amt)` is a:

- A. Dimension Table
- B. Fact Table
- C. Bridge Table
- D. Lookup Table

> [!note]- Answer
> **B** — **Fact Table** 存储可度量的业务事件（`Sales_Amt`），并持有指向各 Dimension Table 的外键（`Market_Id`、`Product_Id`、`Time_Id`）。Dimension Table 存储描述性属性。

---

**Q3.** What is the key difference between **ETL** and **ELT**?

- A. ETL is used in cloud environments; ELT is used on-premises
- B. ETL transforms data before loading; ELT loads raw data first, then transforms inside the warehouse
- C. ETL supports unstructured data; ELT only handles structured data
- D. ELT requires an external transformation tool; ETL does not

> [!note]- Answer
> **B** — ETL = Extract → Transform → Load（先在外部转换，再载入目标）；ELT = Extract → Load → Transform（先把原始数据载入数仓，再利用仓库内部算力转换）。ELT 在 BigQuery、Snowflake 等现代云数仓中更常见。

---

**Q4.** What is the most important distinction between a **Data Lake** and a **Data Warehouse**?

- A. A Data Lake can only store structured data
- B. A Data Lake uses schema-on-read; a Data Warehouse uses schema-on-write
- C. A Data Warehouse stores raw data; a Data Lake stores refined data
- D. A Data Lake does not support SQL queries

> [!note]- Answer
> **B** — **Schema-on-read**：读取时才定义结构，灵活但可能混乱（Data Lake）。**Schema-on-write**：写入时强制结构，严格但整洁（Data Warehouse）。

---

**Q5.** In an XML DTD, what does `(name, age?)` mean?

- A. Both `name` and `age` must appear, in that order
- B. `name` must appear exactly once; `age` is optional (zero or one occurrence)
- C. Either `name` or `age` must appear (mutually exclusive)
- D. `name` appears zero or more times; `age` appears exactly once

> [!note]- Answer
> **B** — DTD 符号速记：`?` = 零或一次（可选）；`*` = 零或多次；`+` = 一或多次；不加符号 = 恰好一次。逗号表示元素必须按顺序出现。

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
> **B** — `find()` 的第一个参数是 **filter**（`{ age: { $gt: 20 } }`），第二个参数是 **projection**（`{ name: 1, address: 1 }`），指定返回哪些字段。字段设为 `1` = 包含，`0` = 排除。

---

**Q7.** Compared to a relational database, a graph database (e.g., Neo4j) excels at:

- A. Large-scale numerical aggregations (SUM / AVG)
- B. Complex multi-table JOIN operations
- C. Multi-hop relationship traversals (e.g., "friends of friends")
- D. High-volume bulk INSERT operations

> [!note]- Answer
> **C** — 图数据库将关系作为一等公民（edge）直接存储，多跳遍历每跳 O(1)。关系型数据库做同样的多跳查询需要反复执行昂贵的 JOIN，随跳数增加性能急剧下降。

---

**Q8.** Which NoSQL type is best suited for storing **social network relationships**?

- A. Document Store
- B. Wide Column Store
- C. Graph Database
- D. Time Series Database

> [!note]- Answer
> **C** — 社交网络的核心是实体之间的关系（用户-用户、用户-内容），天然对应图结构。Graph Database 对好友推荐、最短路径等查询有原生支持。

---

**Q9.** A "Valid" XML document means it is:

- A. Syntactically well-formed only (all tags match and are properly closed)
- B. Well-formed AND conforms to a DTD or XML Schema definition
- C. Correctly rendered by any modern browser
- D. Semantically meaningful in its business context

> [!note]- Answer
> **B** — **Well-formed** = 满足 XML 语法规则（标签正确嵌套、闭合、属性带引号）。**Valid** = Well-formed **加上**符合 DTD 或 XML Schema 定义的结构约束。一个文档可以 well-formed 但不 valid。

---

**Q10.** Which of the following statements about MongoDB is correct?

- A. MongoDB requires a fixed schema to be defined before inserting data
- B. All documents in a collection must have the same structure
- C. MongoDB stores documents in JSON format and supports nested structures
- D. MongoDB uses SQL as its query language

> [!note]- Answer
> **C** — MongoDB 是 schema-late（无需提前定义结构），同一 Collection 中不同 Document 结构可以不同，数据以 BSON（binary JSON）存储，支持嵌套，查询语言是 JavaScript 风格，不是 SQL。

---

## Section B — Short Answer (8 marks each, 32 marks total)

**Q11.** Compare OLTP and OLAP systems across three dimensions: **read/write patterns**, **query characteristics**, and **data volume**. Give one typical example of each. (8 marks)

> [!note]- Answer
> | 维度 | OLTP | OLAP |
> |------|------|------|
> | Read/write pattern | 频繁的单行 INSERT/UPDATE/DELETE；按主键点查询 | 批量 ETL/ELT 导入；大范围聚合扫描（SUM、COUNT、AVG） |
> | Query characteristics | 短小、预定义、低延迟事务 | 复杂、临时性分析查询，可能运行数秒到数分钟 |
> | Data volume | GB 到 TB（当前运营数据） | TB 到 PB（多年历史记录） |
> 
> *OLTP 例*：银行转账系统——每笔转账是一个立即完成的原子事务。
> 
> *OLAP 例*：零售数仓——分析师查询各地区近三年各品类销售额同比增长。

---

**Q12.** Describe the structure of a **Star Schema**. Explain what a Fact Table and Dimension Tables store and how they relate. Use a hypothetical e-commerce data warehouse as an example. (8 marks)

> [!note]- Answer
> **结构**：
> - **Fact Table** 位于中心，存储可度量的业务事件（facts）及指向各 Dimension Table 的外键。facts 通常是数值型且可加（如 revenue、quantity）。
> - **Dimension Tables** 围绕 Fact Table，每张表描述一个维度（谁、什么、何时、何地）。
> - Fact Table 通过外键关联各 Dimension Table，形成星形结构。
> 
> **电商例子**：
> ```
> Fact:   Orders(order_id, customer_id, product_id, time_id, region_id, order_amount)
> Dims:   Customer(customer_id, name, age, email)
>         Product(product_id, name, category, unit_price)
>         Time(time_id, date, month, quarter, year)
>         Region(region_id, city, state, country)
> ```
> 查询"2025 Q1 各品类总销售额"：JOIN `Orders` + `Product`（取 category）+ `Time`（筛 Q1），再 SUM `order_amount`。

---

**Q13.** Explain why a Data Lake can easily become a **"data swamp"**. How do organisations typically combine a Data Lake and a Data Warehouse in practice? (8 marks)

> [!note]- Answer
> **为什么变成 data swamp**：
> - Schema-on-read 意味着数据写入时无结构约束，格式参差不齐且缺乏文档。
> - 没有 metadata catalogue，用户不知道有什么数据、格式是什么、是否可信。
> - 入库时没有数据质量检查，损坏或重复的记录与有效数据混在一起。
> - 久而久之，数据堆积但无人维护，实际上无法使用。
> 
> **实践中的结合方式**：
> 1. **Data Lake（HDFS/S3）**：所有原始数据先落地，原格式保留，不丢弃历史。
> 2. **ETL/ELT pipeline**：对数据清洗、标准化、建模（如构建 Star Schema）。
> 3. **Data Warehouse（Snowflake/BigQuery）**：存储精炼后的业务数据，供 BI 工具和分析师使用。
> 
> 这种组合兼顾了 Lake 的灵活性（廉价存储全量数据）和 Warehouse 的可靠性（查询干净、结构化的数据）。

---

**Q14.** Compare a **relational database (RDBMS)** and a **graph database** across three dimensions: data model, query language, and performance advantage. When should you prefer a graph database? (8 marks)

> [!note]- Answer
> | 维度 | RDBMS（如 PostgreSQL） | Graph DB（如 Neo4j） |
> |------|------------------------|----------------------|
> | Data model | 表（行和列）；关系通过 foreign key 表达 | Node（实体）+ Edge（关系）+ Properties；关系是一等公民 |
> | Query language | SQL | Cypher（Neo4j）、SPARQL、Gremlin |
> | Performance advantage | ACID 事务；批量数值聚合效率高 | 多跳图遍历每跳 O(1)；避免昂贵的反复 JOIN |
> 
> **优先选 Graph DB 的场景**：核心问题是**关系的遍历**而非数据聚合——社交网络好友推荐、欺诈检测（交易关系链）、知识图谱、网络拓扑分析。

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
> `%s` 是**参数占位符**，psycopg2 会把 `('Sydney',)` 中的值安全地绑定到 SQL 中。
> 
> 用参数化查询可以防止 **SQL injection（SQL 注入）攻击**——如果用字符串拼接（如 `f"WHERE region = '{user_input}'"` ），攻击者可以在输入中注入恶意 SQL 语句。参数化方式会对值进行转义，将其作为数据而非可执行 SQL 处理。

**(b)** What type does `cursor.fetchall()` return? (1 mark)

> [!note]- Answer
> 返回一个 **list of tuples**（元组列表）——每个元组对应结果集的一行，元素对应各列的值。

**(c)** Describe the full flow of this script from connection to final output. (3 marks)

> [!note]- Answer
> 1. 连接到 PostgreSQL 数据库 `sales`
> 2. 执行 SQL：筛选 Sydney 地区的销售记录，按 `product_id` 分组，计算每个产品的总销售额
> 3. `fetchall()` 获取所有结果行
> 4. 将结果包装成 DataFrame，列名为 `product_id` 和 `total`
> 5. 按 `total` 降序排列，取前 5 行，打印后关闭连接

**(d)** Does this code demonstrate "push compute into the DBMS" or "pull all data into Python"? Explain. (2 marks)

> [!note]- Answer
> **Push compute into the DBMS。** SQL 在数据库内部完成了过滤（`WHERE region = 'Sydney'`）和聚合（`GROUP BY` + `SUM`）。Python 只接收聚合后的少量结果（每个产品一行），而不是把整张 `sales` 表拉过来再处理。这样充分利用了数据库的索引和查询优化器，网络传输量也最小。
