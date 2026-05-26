# Week 5 Quiz — NoSQL & Semi-structured Data

---

## Multiple Choice Questions

**1.** Which of the following best describes the characteristics of semi-structured data?

- A. It has a strictly fixed schema where every record contains exactly the same fields
- B. It has no parseable structure at all and can only be stored as raw binary
- C. It has a self-describing structure (e.g., tags or key-value pairs) but does not enforce a fixed schema, allowing different records to have different fields
- D. It must be stored in a relational database to guarantee data consistency

> [!tip]- Answer
> **答案：C**
> 解析：Semi-structured 数据的核心特征是有内在结构（XML 标签、JSON 键值对）但不强制 schema，不同对象的字段可以缺失或额外增加，支持嵌套。JSON 和 XML 都是典型代表。A 描述的是结构化数据（关系表）；B 描述的是非结构化数据（如图片、音频）；D 错误，NoSQL（如 MongoDB）正是为了避免强制关系型存储而设计的。

---

**2.** An XML document is judged to be "Well-formed" but not "Valid". What does this mean?

- A. The document conforms to the associated DTD structural rules but contains syntax errors (e.g., unclosed tags)
- B. The document satisfies basic XML syntax rules but does not conform to the structural constraints defined by a DTD or XML Schema
- C. The document has neither syntax errors nor DTD violations, but its character encoding declaration is incorrect
- D. The document can be rendered by a browser but cannot be processed by an XML parser

> [!tip]- Answer
> **答案：B**
> 解析：**Well-formed** 是 XML 的基础要求：根元素唯一、所有标签正确闭合、属性值有引号、元素正确嵌套。**Valid** 是更严格的约束：在 well-formed 基础上，还需符合 DTD 或 XML Schema 所定义的元素顺序、必选元素、数据类型等业务规则。Well-formed 是 Valid 的必要条件，但 well-formed 不保证 valid。

---

**3.** What element structure does the following DTD fragment describe?

```xml
<!ELEMENT book (title, (author | editor)+, chapter*)>
```

- A. book contains: title (exactly once), both author and editor (each must appear at least once), chapter (zero or more times)
- B. book contains: title (exactly once), author or editor (at least once, possibly multiple times), chapter (zero or more times)
- C. book contains: title (optional), author or editor (exactly once), chapter (one or more times)
- D. book contains: title (exactly once), author or editor (zero or one time), chapter (zero or more times)

> [!tip]- Answer
> **答案：B**
> 解析：按 DTD 符号规则解析：`title` 无符号 = 必须恰好出现1次；`(author | editor)+` 中 `|` 表示二选一，`+` 表示整体出现1次或多次（至少1次）；`chapter*` 中 `*` 表示出现0次或多次。注意 `+` 作用于整个 `(author | editor)` 组，而非要求两者同时出现。

---

**4.** Regarding the origin and design goals of NoSQL databases, which statement is most accurate?

- A. NoSQL has completely replaced SQL, and modern systems no longer use relational databases
- B. NoSQL means "No SQL", meaning it does not support any query language at all
- C. NoSQL ("Not only SQL") was designed to overcome the Scale-Up bottleneck of traditional RDBMS by handling large-scale data through Scale-Out
- D. NoSQL databases provide stronger consistency guarantees than relational databases, making them more suitable for financial transactions

> [!tip]- Answer
> **答案：C**
> 解析：NoSQL 全称是 "Not only SQL"，并非排除 SQL 而是补充它。传统 RDBMS 通过 Scale-Up（更强的单机硬件）扩展，存在硬件上限且成本高；NoSQL 通过 Scale-Out（增加更多普通节点）横向扩展，适合互联网规模的海量数据。多数 NoSQL 系统牺牲了强一致性换取高可用性（BASE 模型），因此 D 错误。

---

**5.** Which of the following correctly matches NoSQL systems to their types?

- A. Redis → Document Store；Neo4j → Key-Value Store
- B. MongoDB → Document Store；Neo4j → Graph DB；InfluxDB → Time-Series DB
- C. HBase → Graph DB；Cassandra → Document Store；MongoDB → Wide Column Store
- D. DynamoDB → Graph DB；InfluxDB → Key-Value Store；Neo4j → Document Store

> [!tip]- Answer
> **答案：B**
> 解析：五类 NoSQL 及代表系统：Document Store = MongoDB（JSON 文档）；Key-Value Store = Redis、DynamoDB、Cassandra；Graph DB = Neo4j；Time-Series DB = InfluxDB；Wide Column Store = HBase、BigTable。选项 B 完全正确。A、C、D 均存在分类错误。

---

**6.** MongoDB adopts a "schema-late (schema-on-read)" design. Which statement best reflects this characteristic?

- A. MongoDB automatically generates and locks the schema when data is written; subsequent writes must strictly follow it
- B. Different documents in the same collection can have different fields; schema interpretation is handled by the application layer at read time
- C. MongoDB does not support nested documents; all data must be stored in a flat structure
- D. MongoDB requires every collection to declare all field types at creation time

> [!tip]- Answer
> **答案：B**
> 解析：Schema-on-read（schema-late）意味着数据库本身不在写入时验证结构，同一个 Collection 中的不同 Document 可以有完全不同的字段。Schema 的解读由应用程序在读取数据时负责。这与关系型数据库的 schema-on-write 相反。MongoDB 实际上支持嵌套文档，D 错误。

---

**7.** In MongoDB's relationship modeling, what is the primary consideration for choosing "Embedded" over "Reference"?

- A. Embedded is suitable for scenarios where two entities need to be updated frequently and independently
- B. Embedded stores related data in the same document, which is ideal for data that is always read together and offers better read performance
- C. Reference modeling causes data redundancy, so Embedded is always the superior choice
- D. Embedded modeling requires nesting to be no more than two levels deep; beyond that, Reference must be used

> [!tip]- Answer
> **答案：B**
> 解析：Embedded（嵌入）将子文档直接放入父文档，单次查询即可获取所有相关数据，读取性能好，适合"总是一起使用"的数据（如订单与订单明细）。Reference（引用）类似关系型外键，将关联数据存在独立集合，适合需要独立更新或被多处引用的数据（如用户与文章）。A 描述的恰恰是引用更适合的场景；C 的"始终最优"是绝对化表述，错误；D 是虚构限制。

---

**8.** Regarding the comparison between Neo4j graph databases and relational databases, which statement is correct?

- A. Neo4j does not support ACID transactions and is therefore unsuitable for scenarios requiring data consistency
- B. Relational databases experience significant performance degradation on multi-hop relationship queries (e.g., "friends of friends") as depth increases, while graph databases maintain stable performance through native relationship storage
- C. Neo4j uses standard SQL for queries, the same as relational databases
- D. Relational databases scale via Scale-Out, while graph databases scale via Scale-Up

> [!tip]- Answer
> **答案：B**
> 解析：这是一道常见 MCQ 陷阱题。Neo4j **支持 ACID 事务**，这与很多人对 NoSQL 的刻板印象相反（A 错误）。Neo4j 使用 Cypher（或 Gremlin/SPARQL）查询，而非 SQL（C 错误）。扩展方向恰恰相反：关系型数据库倾向 Scale-Up，图数据库倾向 Scale-Out（D 错误）。B 正确描述了图数据库在关系遍历上的核心优势：每次遍历是 O(1) 的"指针跟随"操作。

---

## Short Answer Questions

**9.** Both JSON and XML are semi-structured data formats. Compare the two from three perspectives: syntactic conciseness, attribute support, and typical use cases.

> [!tip]- Answer
> | Perspective | XML | JSON |
> |-------------|-----|------|
> | **Syntactic Conciseness** | Opening and closing tags are verbose (e.g., `<name>Alice</name>`), resulting in larger file sizes | Key-value pairs are concise (e.g., `"name": "Alice"`), smaller in size and faster to parse |
> | **Attribute Support** | Supports element attributes; metadata can be attached directly to tags (e.g., `<book id="1">`) | No concept of attributes; all information is expressed as key-value pairs |
> | **Typical Use Cases** | Enterprise data exchange (SOAP/EDI), configuration files (Maven/Spring), Office document formats | Web REST API responses, MongoDB document storage, modern front-end/back-end data exchange |
>
> **考试要点**：JSON 更轻量，是现代 Web API 主流格式；XML 历史更悠久，有成熟的 DTD/Schema 验证机制，在企业遗留系统中仍广泛使用。两者都是半结构化数据的代表格式。

---

**10.** What mechanisms does MongoDB's distributed architecture use to achieve high scalability and high availability? Briefly explain from three dimensions: Sharding, Replication, and consistency.

> [!tip]- Answer
> **Sharding（分片/Auto Sharding）**：MongoDB 自动将数据按 shard key 分布到多个节点（水平分割），每个 shard 只存储部分数据。这实现了 Scale-Out，随数据量增长只需添加节点，突破单机存储和吞吐量上限。
>
> **Replication（复制/Single-Leader Replication）**：每个 shard 维护一个 Replica Set，包含一个 Primary（主节点）和多个 Secondary（从节点）。写操作只发往 Primary，再异步同步到 Secondary。Primary 宕机时，从节点自动选举新主，保证高可用。
>
> **一致性（Eventual Consistency from Follower）**：默认情况下从 Secondary 读取可能返回稍旧的数据，这是最终一致性（Eventual Consistency）。若业务需要强一致，可配置从 Primary 读取，但会降低读吞吐量。

---

**11.** An e-commerce platform needs to analyze user behavior paths (e.g., multi-step conversion funnels like "browse → add to cart → purchase") and also needs to recommend "what other users who bought the same product also bought". Explain why a graph database is more suitable than a relational database for this scenario, and identify one key difference between a graph database query language (using Cypher as an example) and SQL.

> [!tip]- Answer
> **图数据库更适合的原因**：上述场景的核心是**多跳关系遍历**——从一个用户出发，沿着"行为"边跨越多个节点（用户→商品→用户）找到关联节点。关系型数据库实现此类查询需要多层 JOIN，随着遍历深度增加，JOIN 的笛卡尔积膨胀导致性能指数级下降。图数据库（如 Neo4j）将节点和边作为一等公民原生存储，每次遍历是 O(1) 的"指针跟随"，无论图的深度如何性能都保持稳定。
>
> **Cypher 与 SQL 的关键区别**：SQL 通过 JOIN 表达关系，依赖外键和中间表；Cypher 通过图模式（pattern matching）直接描述节点和边的结构，如 `(u:User)-[:PURCHASED]->(p:Product)` 直观表达"用户购买了商品"这一关系，无需额外连接表。Cypher 更擅长描述"路径"和"网络结构"，SQL 更擅长描述"集合"和"聚合"。
