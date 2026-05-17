# Group 2 — 存储系统

**Week 3 (Databases, Warehouses, Lakes) + Week 5 (NoSQL & Semi-structured)**

> 叙事链：结构化数据放关系型数据库（OLTP）→ 分析需要不同形状（OLAP + 数仓）→ 不是所有数据都有固定结构 → NoSQL 处理半结构化 → 海量原始数据放数据湖

---

## Part 1 — 关系型数据库（W3）

### 核心概念

- **Relation（关系）**：一张表，是一组 tuple 的集合
- **Schema**：描述表的列名和类型
- **Primary Key**：唯一标识每一行（可以是单列或多列组成的 Composite PK）
- **Foreign Key**：引用另一张表的主键，建立"逻辑指针"

```sql
CREATE TABLE Enrolment (
    student_id INT NOT NULL,
    course_id  INT NOT NULL,
    enrolled_at DATE NOT NULL,
    marks INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (course_id)  REFERENCES Course(course_id),
    CHECK (marks IS NULL OR marks BETWEEN 0 AND 100)
);
```

### 从 Python 访问数据库

```python
import psycopg2
import pandas as pd

# 连接 PostgreSQL
conn = psycopg2.connect("dbname=mydb user=me password=...")

# 点查询（Point query）
cursor = conn.cursor()
cursor.execute("SELECT * FROM Stations WHERE stationid = %s", (409001,))

# 批量读取到 DataFrame
df = pd.read_sql_table('measurements', conn)
df = pd.read_sql_query('SELECT * FROM Measurements WHERE obsdate > %s', conn, params=['2020-01-01'])
```

**Push compute into DBMS**（把计算推给数据库）vs **Pull all data**（拉到 Python 处理）：
- 推给 DBMS：利用索引和 join 优化，扩展性强
- 拉到 Python：简单，但数据必须能放进内存

---

## Part 2 — OLTP vs OLAP（W3）

| 维度 | OLTP（在线事务处理） | OLAP（在线分析处理） |
|------|---------------------|---------------------|
| **主要读模式** | 点查询（按 key 取少量记录） | 聚合扫描（COUNT/SUM/AVG 大量记录） |
| **主要写模式** | Insert / Update / Delete 单条记录 | 批量导入（ETL/ELT）或事件流 |
| **用户** | Web/移动应用的终端用户 | 内部数据分析师 |
| **查询特点** | 固定预定义查询 | 分析师可以任意查询 |
| **数据时态** | 当前状态快照 | 历史事件记录 |
| **数据量** | GB 到 TB | TB 到 PB |
| **例子** | 银行转账、订单录入 | 数据仓库、商业报表 |

---

## Part 3 — 数据仓库（W3）

### Star Schema（星型模式）

数据仓库的核心设计模式：

- **Fact Table（事实表）**：存储可度量的业务事件，包含各维度的外键
  - 例：`Sales(Market_Id, Product_Id, Time_Id, Sales_Amt)`
- **Dimension Tables（维度表）**：描述事实的各个维度
  - 例：`Market(Market_Id, City, State, Region)`
  - 例：`Product(Product_Id, Name, Category, Price)`
  - 例：`Time(Time_Id, Week, Month, Quarter)`

维度可以有层级结构，例如：
```
Product: category → pname
Location: country → state → city
Time: year → quarter → month → week → date
```

### ETL vs ELT

| | ETL（Extract-Transform-Load） | ELT（Extract-Load-Transform） |
|-|-------------------------------|-------------------------------|
| **顺序** | 先转换再载入 | 先载入再转换 |
| **转换位置** | 数据仓库外部 | 数据仓库/数据湖内部 |
| **适合** | 传统数仓，数据已知结构 | 现代云数仓，原始数据先存再按需转换 |

---

## Part 4 — 数据仓库 vs 数据湖（W3）

| 维度 | Database（OLTP） | Data Warehouse（OLAP） | Data Lake |
|------|-----------------|----------------------|-----------|
| **数据类型** | 结构化 | 结构化 | 结构化 + 半结构化 + 非结构化 |
| **Schema** | 写入时定义（schema-on-write） | 写入时定义 | 读取时定义（schema-on-read） |
| **用途** | 生产系统事务 | 历史分析、报表 | 灵活存储，未来用途不确定 |
| **技术** | PostgreSQL、MySQL | Snowflake、BigQuery | HDFS、S3 |
| **风险** | — | — | 容易变成"数据沼泽"（data swamp） |

**何时用 Data Warehouse**：数据结构固定，需要快速复杂查询，BI 分析
**何时用 Data Lake**：混合数据类型，需要弹性存储，未来数据用途不确定
**实践中**：两者结合使用——原始数据进 Lake，精炼后移到 Warehouse

---

## Part 5 — 半结构化数据与 NoSQL（W5）

### 半结构化数据特点

- 没有固定 schema（missing/额外属性均可）
- 嵌套结构（树形，如 JSON/XML）
- 同一集合中不同对象可有不同类型
- 自描述（Self-describing）

### XML vs JSON

| | XML | JSON |
|-|-----|------|
| **标签** | 用户自定义标签 | key-value 对 |
| **结构** | 树形，有属性 | 树形，无属性概念 |
| **校验** | DTD / XML Schema | JSON Schema |
| **用途** | 企业数据交换，Web Service | Web API，现代数据存储 |

**XML 合规性**：
- **Well-formed**：满足 XML 语法约束（标签匹配）
- **Valid**：Well-formed + 符合 DTD/Schema 定义的结构

DTD 语法速记：
```
(name, age)   → 严格顺序
(name | age)  → 二选一
(name*)       → 零或多个
(name+)       → 一或多个
(name?)       → 可选（零或一个）
```

### MongoDB（文档型 NoSQL）

- 数据模型：Collection（集合）中存 Document（文档），即嵌套 key-value（JSON 格式）
- Schema-late：不需要提前定义结构

**基本操作**：

```javascript
// 插入
db.users.insertOne({ name: "sue", age: 26, status: "pending" })

// 查询（类似 SELECT ... WHERE ...）
db.students.find()                              // SELECT *
db.students.find({ name: 'Jane' })              // WHERE name='Jane'
db.students.find({ age: { $gt: 20 } })          // WHERE age > 20
db.students.find({ $or: [{ name: 'Jane' }, { name: 'Joe' }] })

// 投影（选择返回哪些字段）
db.users.find({ age: { $gt: 26 } }, { name: 1, address: 1 })

// 排序
db.courses.find().sort({ name: -1 })            // ORDER BY name DESC
```

**引号规则**：
- MongoDB Shell（JavaScript 接口）：key 不需要引号
- mongoimport / JSON 文件：key **必须**用双引号（标准 JSON）

### 关系型 vs 图数据库

| 维度 | RDBMS | Graph DB（如 Neo4j） |
|------|-------|----------------------|
| **数据模型** | 表（行和列） | 节点（Node）、边（Edge）、属性 |
| **Schema** | 固定 | 灵活或无 Schema |
| **查询语言** | SQL | Cypher（Neo4j）、Gremlin、SPARQL |
| **性能优势** | ACID 事务，复杂 join | **图遍历**（关系查询） |
| **扩展方式** | 垂直扩展 | 水平扩展 |
| **适用场景** | 传统业务系统，事务处理 | 社交网络，推荐系统，欺诈检测 |

---

## Part 6 — NoSQL 选型总结

| NoSQL 类型 | 代表系统 | 适合数据 |
|-----------|----------|----------|
| Document Store | MongoDB, Couchbase | 半结构化 JSON |
| Graph DB | Neo4j | 关系密集型数据 |
| Time Series DB | InfluxDB, TimescaleDB | 时序数据 |
| Wide Column Store | HBase, BigTable | 稀疏大数据 |

---

## 高频考点

- **OLTP vs OLAP**：读写模式、用户、数据量、查询特点四个维度
- **Star Schema**：Fact Table + Dimension Tables，能画出结构
- **ETL vs ELT**：转换位置和顺序的差异
- **Data Warehouse vs Data Lake**：schema-on-write vs schema-on-read
- **Well-formed vs Valid XML**：语法合规 vs 符合 DTD 结构
- **MongoDB 查询语法**：`find()`，`$gt`，`$or`，`.sort()`
- **RDBMS vs Graph DB**：数据模型、查询语言、性能特点
