# 第5周测试 — NoSQL 与半结构化数据

---

## 选择题

**1.** 以下哪项最准确地描述了半结构化数据（Semi-structured data）的特征？

- A. 有严格固定的 schema，每条记录的字段完全一致
- B. 没有任何可解析的结构，只能作为原始二进制存储
- C. 有自描述结构（如标签或键值对），但不强制固定 schema，不同记录的字段可以不同
- D. 必须存储在关系型数据库中才能保证数据一致性

> [!tip]- 答案
> **答案：C**
> 解析：Semi-structured 数据的核心特征：有内在结构（XML 标签、JSON 键值对）但不强制 schema，不同对象的字段可以缺失或额外增加，支持嵌套。JSON 和 XML 都是典型代表。A 描述的是结构化数据（关系表）；B 描述的是非结构化数据（如图片、音频）；D 错误，NoSQL（如 MongoDB）正是为了避免强制关系型存储而设计的。

---

**2.** 一个 XML 文档被判定为 "Well-formed" 但不是 "Valid"，这意味着什么？

- A. 文档符合关联的 DTD 结构规则，但存在语法错误（如标签未闭合）
- B. 文档满足 XML 基本语法规则，但不符合 DTD 或 XML Schema 定义的结构约束
- C. 文档既无语法错误也符合 DTD，但字符编码声明有误
- D. 文档可以被浏览器渲染，但无法被 XML 解析器处理

> [!tip]- 答案
> **答案：B**
> 解析：**Well-formed** 是 XML 的基础要求：根元素唯一、所有标签正确闭合、属性值有引号、元素正确嵌套。**Valid** 是更严格的约束：在 well-formed 基础上，还需符合 DTD 或 XML Schema 所定义的元素顺序、必选元素、数据类型等业务规则。Well-formed 是 Valid 的必要条件，但 well-formed 不保证 valid。

---

**3.** 以下 DTD 片段描述的元素结构是什么？

```xml
<!ELEMENT book (title, (author | editor)+, chapter*)>
```

- A. book 包含：title（必须1次）、author 和 editor（两者都必须至少出现1次）、chapter（0或多次）
- B. book 包含：title（必须1次）、author 或 editor（至少出现1次，可多次）、chapter（0或多次）
- C. book 包含：title（可选）、author 或 editor（恰好1次）、chapter（1或多次）
- D. book 包含：title（必须1次）、author 或 editor（0或1次）、chapter（0或多次）

> [!tip]- 答案
> **答案：B**
> 解析：按 DTD 符号规则解析：`title` 无符号 = 必须恰好出现1次；`(author | editor)+` 中 `|` 表示二选一，`+` 表示整体出现1次或多次（至少1次）；`chapter*` 中 `*` 表示出现0次或多次。注意 `+` 作用于整个 `(author | editor)` 组，而非要求两者同时出现。

---

**4.** 关于 NoSQL 数据库的起源与设计目标，以下说法最准确的是？

- A. NoSQL 完全取代了 SQL，现代系统已不再使用关系型数据库
- B. NoSQL 的含义是"No SQL"，即完全不支持任何查询语言
- C. NoSQL（"Not only SQL"）是为了应对传统 RDBMS Scale-Up 的瓶颈，通过 Scale-Out 的方式处理大规模数据
- D. NoSQL 数据库的一致性保证比关系型数据库更强，因此更适合金融交易

> [!tip]- 答案
> **答案：C**
> 解析：NoSQL 全称是 "Not only SQL"，并非排除 SQL 而是补充它。传统 RDBMS 通过 Scale-Up（更强的单机硬件）扩展，存在硬件上限且成本高；NoSQL 通过 Scale-Out（增加更多普通节点）横向扩展，适合互联网规模的海量数据。多数 NoSQL 系统牺牲了强一致性换取高可用性（BASE 模型），因此 D 错误。

---

**5.** 以下 NoSQL 系统与其类型的对应关系，哪项是正确的？

- A. Redis → Document Store；Neo4j → Key-Value Store
- B. MongoDB → Document Store；Neo4j → Graph DB；InfluxDB → Time-Series DB
- C. HBase → Graph DB；Cassandra → Document Store；MongoDB → Wide Column Store
- D. DynamoDB → Graph DB；InfluxDB → Key-Value Store；Neo4j → Document Store

> [!tip]- 答案
> **答案：B**
> 解析：五类 NoSQL 及代表系统：Document Store = MongoDB（JSON 文档）；Key-Value Store = Redis、DynamoDB、Cassandra；Graph DB = Neo4j；Time-Series DB = InfluxDB；Wide Column Store = HBase、BigTable。选项 B 完全正确。A、C、D 均存在分类错误。

---

**6.** MongoDB 采用"schema-late（schema-on-read）"设计，以下哪项说法最能体现这一特性？

- A. MongoDB 在写入数据时自动生成并锁定 schema，后续写入必须严格遵循
- B. 集合中不同文档可以拥有不同字段，schema 的解释由应用层在读取时处理
- C. MongoDB 不支持嵌套文档，所有数据必须扁平化存储
- D. MongoDB 强制要求每个集合在创建时声明所有字段类型

> [!tip]- 答案
> **答案：B**
> 解析：Schema-on-read（schema-late）意味着数据库本身不在写入时验证结构，同一个 Collection 中的不同 Document 可以有完全不同的字段。Schema 的解读由应用程序在读取数据时负责。这与关系型数据库的 schema-on-write 相反。MongoDB 实际上支持嵌套文档，D 错误。

---

**7.** 在 MongoDB 的关系建模中，选择"Embedded（嵌入式）"而非"Reference（引用）"的主要考量是什么？

- A. 嵌入式适合两个实体需要频繁独立更新的场景
- B. 嵌入式将相关数据存储在同一文档中，适合总是一起读取的数据，读取性能更好
- C. 引用建模会导致数据冗余，因此嵌入式始终是更优的选择
- D. 嵌入式建模要求嵌套层级不超过两层，否则必须使用引用

> [!tip]- 答案
> **答案：B**
> 解析：Embedded（嵌入）将子文档直接放入父文档，单次查询即可获取所有相关数据，读取性能好，适合"总是一起使用"的数据（如订单与订单明细）。Reference（引用）类似关系型外键，将关联数据存在独立集合，适合需要独立更新或被多处引用的数据（如用户与文章）。A 描述的恰恰是引用更适合的场景；C 的"始终最优"是绝对化表述，错误；D 是虚构限制。

---

**8.** 关于 Neo4j 图数据库与关系型数据库的比较，以下说法正确的是？

- A. Neo4j 不支持 ACID 事务，因此不适合需要数据一致性的场景
- B. 关系型数据库在处理多跳关系查询（如"朋友的朋友"）时，随着深度增加性能显著下降，而图数据库通过原生关系存储保持稳定性能
- C. Neo4j 使用标准 SQL 语言查询，与关系型数据库查询方式相同
- D. 关系型数据库通过 Scale-Out 扩展，图数据库通过 Scale-Up 扩展

> [!tip]- 答案
> **答案：B**
> 解析：这是一道常见 MCQ 陷阱题。Neo4j **支持 ACID 事务**，这与很多人对 NoSQL 的刻板印象相反（A 错误）。Neo4j 使用 Cypher（或 Gremlin/SPARQL）查询，而非 SQL（C 错误）。扩展方向恰恰相反：关系型数据库倾向 Scale-Up，图数据库倾向 Scale-Out（D 错误）。B 正确描述了图数据库在关系遍历上的核心优势：每次遍历是 O(1) 的"指针跟随"操作。

---

## 简答题

**9.** JSON 和 XML 都是半结构化数据格式。请从语法简洁性、属性支持和典型应用场景三个角度比较两者的差异。

> [!tip]- 答案
> | 角度 | XML | JSON |
> |------|-----|------|
> | **语法简洁性** | 开合标签冗余（如 `<name>Alice</name>`），体积较大 | 键值对简洁（如 `"name": "Alice"`），体积小，解析速度快 |
> | **属性支持** | 支持元素属性，可在标签中附加元数据（如 `<book id="1">`） | 无属性概念，所有信息均作为键值对表达 |
> | **典型应用场景** | 企业数据交换（SOAP/EDI）、配置文件（Maven/Spring）、Office 文档格式 | Web REST API 响应、MongoDB 文档存储、现代前后端数据交换 |
>
> **考试要点**：JSON 更轻量，是现代 Web API 主流格式；XML 历史更悠久，有成熟的 DTD/Schema 验证机制，在企业遗留系统中仍广泛使用。两者都是半结构化数据的代表格式。

---

**10.** MongoDB 的分布式架构采用了哪些机制来实现高可扩展性和高可用性？从 Sharding、Replication 和一致性三个维度简要说明。

> [!tip]- 答案
> **Sharding（分片/Auto Sharding）**：MongoDB 自动将数据按 shard key 分布到多个节点（水平分割），每个 shard 只存储部分数据。这实现了 Scale-Out，随数据量增长只需添加节点，突破单机存储和吞吐量上限。
>
> **Replication（复制/Single-Leader Replication）**：每个 shard 维护一个 Replica Set，包含一个 Primary（主节点）和多个 Secondary（从节点）。写操作只发往 Primary，再异步同步到 Secondary。Primary 宕机时，从节点自动选举新主，保证高可用。
>
> **一致性（Eventual Consistency from Follower）**：默认情况下从 Secondary 读取可能返回稍旧的数据，这是最终一致性（Eventual Consistency）。若业务需要强一致，可配置从 Primary 读取，但会降低读吞吐量。

---

**11.** 某电商平台需要分析用户行为路径（如"浏览→加购→购买"的多步转化链路），同时还需要推荐"购买了同款商品的用户还买了什么"。请说明为什么图数据库比关系型数据库更适合这类场景，并指出图数据库查询语言（以 Cypher 为例）与 SQL 的一个关键区别。

> [!tip]- 答案
> **图数据库更适合的原因**：上述场景的核心是**多跳关系遍历**——从一个用户出发，沿着"行为"边跨越多个节点（用户→商品→用户）找到关联节点。关系型数据库实现此类查询需要多层 JOIN，随着遍历深度增加，JOIN 的笛卡尔积膨胀导致性能指数级下降。图数据库（如 Neo4j）将节点和边作为一等公民原生存储，每次遍历是 O(1) 的"指针跟随"，无论图的深度如何性能都保持稳定。
>
> **Cypher 与 SQL 的关键区别**：SQL 通过 JOIN 表达关系，依赖外键和中间表；Cypher 通过图模式（pattern matching）直接描述节点和边的结构，如 `(u:User)-[:PURCHASED]->(p:Product)` 直观表达"用户购买了商品"这一关系，无需额外连接表。Cypher 更擅长描述"路径"和"网络结构"，SQL 更擅长描述"集合"和"聚合"。
