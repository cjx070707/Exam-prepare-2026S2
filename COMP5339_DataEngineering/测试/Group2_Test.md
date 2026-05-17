# Group 2 测试题 — 存储系统

**覆盖范围：Week 3 (Databases, Warehouses, Lakes) + Week 5 (NoSQL & Semi-structured)**

**总分：60 分 | 建议用时：45 分钟**

---

## Section A — MCQ（每题 2 分，共 20 分）

**Q1.** 以下哪种场景最适合使用 OLAP 系统？

- A. 用户在网上商城完成一笔订单
- B. 银行 ATM 完成取款操作
- C. 数据分析师统计过去三年各地区销售额趋势
- D. 员工登录系统更新个人信息

---

**Q2.** 在 Star Schema 中，`Sales(Market_Id, Product_Id, Time_Id, Sales_Amt)` 是哪类表？

- A. Dimension Table
- B. Fact Table
- C. Bridge Table
- D. Lookup Table

---

**Q3.** ETL 和 ELT 的核心区别是：

- A. ETL 用于云环境，ELT 用于本地环境
- B. ETL 先转换后载入，ELT 先载入后转换
- C. ETL 支持非结构化数据，ELT 只支持结构化数据
- D. ELT 需要额外的外部转换工具，ETL 不需要

---

**Q4.** Data Lake 与 Data Warehouse 的最主要区别是：

- A. Data Lake 只能存储结构化数据
- B. Data Lake 使用 schema-on-read，Data Warehouse 使用 schema-on-write
- C. Data Warehouse 存储原始数据，Data Lake 存储精炼数据
- D. Data Lake 不支持 SQL 查询

---

**Q5.** 以下 XML DTD 中，`(name, age?)` 表示什么？

- A. `name` 和 `age` 都必须出现，且顺序固定
- B. `name` 必须出现，`age` 可选（零或一个）
- C. `name` 或 `age` 二选一
- D. `name` 出现零或多次，`age` 出现一次

---

**Q6.** 以下 MongoDB 查询的含义是什么？

```javascript
db.students.find({ age: { $gt: 20 } }, { name: 1, address: 1 })
```

- A. 查找年龄大于 20 的学生，返回所有字段
- B. 查找年龄大于 20 的学生，只返回 name 和 address 字段
- C. 插入年龄大于 20 的记录，包含 name 和 address
- D. 更新年龄大于 20 的学生的 name 和 address

---

**Q7.** 与关系型数据库相比，图数据库（如 Neo4j）最适合哪类查询？

- A. 大量数值聚合（SUM / AVG）
- B. 复杂的多表 JOIN 操作
- C. 多跳关系遍历（如"朋友的朋友"查询）
- D. 大批量数据的 INSERT 操作

---

**Q8.** 以下哪种 NoSQL 类型最适合存储**社交网络中的用户关系**？

- A. Document Store（文档型）
- B. Wide Column Store（宽列型）
- C. Graph Database（图数据库）
- D. Time Series Database（时序数据库）

---

**Q9.** 关于 XML 的合规性，"Valid XML" 意味着：

- A. 仅满足 XML 基本语法（标签匹配、属性引号）
- B. Well-formed 且符合 DTD 或 XML Schema 定义的结构
- C. 能被任意浏览器正确渲染
- D. 数据内容在业务上合理

---

**Q10.** 以下关于 MongoDB 的说法，哪个是正确的？

- A. MongoDB 需要在插入数据前定义固定的表结构
- B. MongoDB 中一个 Collection 只能存储相同结构的 Document
- C. MongoDB 的 Document 以 JSON 格式存储，支持嵌套结构
- D. MongoDB 使用 SQL 作为查询语言

---

## Section B — 短答题（每题 8 分，共 32 分）

**Q11.** 从读写模式、查询特点、数据量三个维度，比较 OLTP 和 OLAP 系统的差异，并各举一个典型的使用场景。（8分）

---

**Q12.** 请描述 Star Schema 的结构，说明 Fact Table 和 Dimension Table 分别存储什么内容，两者如何关联。以一个电商平台的销售数据仓库为例画出结构（用文字描述即可）。（8分）

---

**Q13.** 解释 Data Lake 为什么容易变成"数据沼泽（Data Swamp）"，以及实践中如何将 Data Lake 与 Data Warehouse 结合使用。（8分）

---

**Q14.** 比较关系型数据库（RDBMS）和图数据库（Graph DB）在数据模型、查询语言和性能优势三个维度上的差异。说明在什么业务场景下应优先选择图数据库。（8分）

---

## Section C — 代码阅读（共 8 分）

**Q15.** 阅读以下代码，回答问题：

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

(a) `%s` 在 SQL 语句中起什么作用？为什么要使用参数化查询而不是直接字符串拼接？（2分）

(b) `cursor.fetchall()` 返回的是什么类型的数据？（1分）

(c) 这段代码整体做了什么？描述从连接数据库到最终输出的完整流程。（3分）

(d) 这段代码体现了 "Push compute into DBMS" 还是 "Pull all data into Python"？请解释。（2分）

---

<details>
<summary>📋 参考答案（点击展开）</summary>

### Section A 答案

| 题号 | 答案 | 解析 |
|------|------|------|
| Q1 | **C** | 分析历史趋势 = OLAP；订单、取款、更新信息都是实时单条事务 = OLTP |
| Q2 | **B** | Fact Table 存储可度量的业务事件（Sales_Amt）并持有各维度外键；Dimension Table 存描述信息 |
| Q3 | **B** | ETL = Extract → Transform → Load（先转换再入库）；ELT = Extract → Load → Transform（先入库再转换） |
| Q4 | **B** | Data Lake 读取时才定义结构（schema-on-read），灵活但可能混乱；Data Warehouse 写入时定义结构（schema-on-write） |
| Q5 | **B** | `?` = 零或一个（可选）；`*` = 零或多个；`+` = 一或多个；`,` = 顺序必须 |
| Q6 | **B** | 第一个参数 `{ age: { $gt: 20 } }` 是过滤条件；第二个参数 `{ name: 1, address: 1 }` 是投影（projection），只返回指定字段 |
| Q7 | **C** | 图数据库的优势在于多跳关系遍历（图遍历），关系型数据库做多跳 JOIN 性能极差 |
| Q8 | **C** | 社交网络 = 用户之间的关系 = 图结构 → Graph Database |
| Q9 | **B** | Valid = Well-formed + 符合 DTD/Schema；Well-formed 只要求语法正确 |
| Q10 | **C** | MongoDB 是 schema-late（灵活结构），同一 Collection 中 Document 结构可以不同，使用 JSON 嵌套文档 |

### Section B 参考答案

**Q11.**

| 维度 | OLTP | OLAP |
|------|------|------|
| 读写模式 | Insert/Update/Delete 单条记录，点查询 | 批量 ETL 导入，大范围聚合扫描（COUNT/SUM） |
| 查询特点 | 固定预定义查询，低延迟 | 分析师自由查询，复杂聚合 |
| 数据量 | GB 到 TB | TB 到 PB |

场景举例：OLTP = 银行转账系统（每笔转账是一条事务）；OLAP = 企业数据仓库（统计各地区季度销售额）。

**Q12.**

Star Schema 结构：
- **Fact Table**：存储可度量的业务事件，包含各维度的外键 + 度量值。
- **Dimension Table**：描述事实各维度的属性，通过主键与 Fact Table 关联。

电商示例：
```
Fact Table: Orders(order_id, customer_id, product_id, time_id, region_id, order_amount)

Dimension Tables:
- Customer(customer_id, name, age, email)
- Product(product_id, name, category, brand, price)
- Time(time_id, date, week, month, quarter, year)
- Region(region_id, city, state, country)
```
Orders 通过外键（customer_id, product_id, time_id, region_id）指向各维度表，分析时 JOIN 得到完整描述信息。

**Q13.**

Data Lake 容易变成"数据沼泽"的原因：
- schema-on-read 意味着数据存入时无需结构定义，导致数据质量参差不齐
- 缺乏元数据管理，存入的数据无人知道格式、含义、来源
- 随着数据量增大，找不到需要的数据，或读取时才发现数据不可用

实践结合方式：
- **Data Lake** 存储原始、未处理的数据（HDFS/S3），作为数据中间站，保留全量历史
- **Data Warehouse**（如 BigQuery、Snowflake）存储经过清洗、建模、精炼的数据，供分析使用
- 流程：原始数据 → Data Lake → ETL/ELT 清洗转换 → Data Warehouse → BI 报表

**Q14.**

| 维度 | RDBMS | Graph DB（如 Neo4j） |
|------|-------|----------------------|
| 数据模型 | 表（行和列），外键表示关系 | 节点（Node）+ 边（Edge）+ 属性，关系是一等公民 |
| 查询语言 | SQL | Cypher（Neo4j）、SPARQL、Gremlin |
| 性能优势 | ACID 事务、大批量数据聚合 | 多跳图遍历（O(1) per hop），避免昂贵 JOIN |

优先选图数据库的场景：社交网络（好友推荐）、推荐系统（用户-商品关系）、欺诈检测（交易关系链）、知识图谱、网络拓扑分析。共同特征：核心问题是**关系的遍历**而非数据的聚合。

**Q15.**

(a) `%s` 是参数占位符，psycopg2 会安全地将 `('Sydney',)` 中的值绑定到 SQL 中。使用参数化查询可以防止 **SQL 注入攻击**——如果用字符串拼接，攻击者可以在输入中注入恶意 SQL 语句。

(b) `cursor.fetchall()` 返回一个**列表（list）**，其中每个元素是一个**元组（tuple）**，对应查询结果的一行。

(c) 完整流程：
1. 连接到 PostgreSQL 数据库 `sales`
2. 执行 SQL：筛选 Sydney 地区的销售记录，按 product_id 分组求销售总额
3. 获取全部结果，构建 DataFrame
4. 按总销售额降序排序，取前 5 名
5. 打印结果后关闭连接

(d) **Push compute into DBMS**。SQL 中的 `WHERE region = 'Sydney'` 和 `GROUP BY product_id / SUM(sales_amt)` 都在数据库内部执行，Python 只接收聚合后的少量结果（5行），而不是拉取全表数据再在 Python 中过滤聚合。

</details>
