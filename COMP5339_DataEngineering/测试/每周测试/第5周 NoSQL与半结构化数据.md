# 第5周测试 — NoSQL 与半结构化数据

---

## 选择题

**1.** 以下哪项是半结构化数据（Semi-structured）的特征？

- A. 有严格固定的 schema，每条记录字段完全一致
- B. 完全没有任何结构，不可解析
- C. 没有固定 schema，但有自描述结构（如标签、键值对），不同对象字段可不同
- D. 只能用 JSON 格式存储

> [!tip]- 答案
>
> **答案：C**
>
> 解析：Semi-structured 数据的关键特征：有内在结构（标签/键值对）但不强制固定 schema，字段可嵌套、可缺失、可变化。JSON 和 XML 都是典型代表，MongoDB 文档也属于半结构化。A 是 Structured（关系表）；B 是 Unstructured。
>

---

**2.** XML DTD 符号中，`(name+)` 表示什么？

- A. name 元素可选（零或一次）
- B. name 元素出现一次或多次（至少一次）
- C. name 元素出现零次或多次
- D. name 元素必须恰好出现一次

> [!tip]- 答案
>
> **答案：B**
>
> 解析：DTD 数量符号：`?` = 0或1次；`*` = 0或多次；`+` = 1或多次（至少出现一次）；无符号 = 恰好1次。`(name+)` 意味着 `name` 元素必须至少出现一次，但可以多次。
>

---

**3.** MongoDB 中以下查询等价于 SQL 中的哪条语句？

```javascript
db.students.find({ age: { $gt: 20 } }, { name: 1, _id: 0 })
```

- A. `SELECT * FROM students WHERE age > 20`
- B. `SELECT name FROM students WHERE age > 20`
- C. `SELECT name FROM students WHERE age >= 20`
- D. `SELECT name FROM students WHERE age = 20`

> [!tip]- 答案
>
> **答案：B**
>
> 解析：MongoDB `find(query, projection)` 的第一个参数是过滤条件，第二个是投影（字段选择）。`{ age: { $gt: 20 } }` 等价于 `WHERE age > 20`；`{ name: 1, _id: 0 }` 表示只返回 `name` 字段，排除 `_id`。`$gt` 是 "greater than"，对应 SQL 的 `>`（不包含等于，所以不是 `>=`）。
>

---

**4.** CAP 定理指出，分布式系统不能同时保证哪三个属性？

- A. Consistency（一致性）、Availability（可用性）、Performance（性能）
- B. Consistency（一致性）、Availability（可用性）、Partition Tolerance（分区容错）
- C. Concurrency（并发）、Atomicity（原子性）、Performance（性能）
- D. Consistency（一致性）、Atomicity（原子性）、Partition Tolerance（分区容错）

> [!tip]- 答案
>
> **答案：B**
>
> 解析：CAP 定理：分布式系统在网络分区（Partition）发生时，必须在 **Consistency**（所有节点看到相同数据）和 **Availability**（每个请求都得到响应）之间二选一。CA 系统（如传统 RDBMS）牺牲 P；CP 系统（如 HBase、MongoDB 强一致模式）牺牲 A；AP 系统（如 Cassandra、CouchDB）牺牲 C。
>

---

**5.** ACID 与 BASE 的对比中，BASE 的含义是？

- A. Basic Availability, Soft state, Eventually consistent
- B. Batch processing, Atomicity, Scalability, Efficiency
- C. Backup, Atomic, Secure, Efficient
- D. Basic Atomicity, Strong consistency, Eventually available

> [!tip]- 答案
>
> **答案：A**
>
> 解析：BASE 是 NoSQL 系统的一致性模型，与 ACID 相对：**BA**sically Available（基本可用，允许部分失败）、**S**oft state（状态可能不断变化）、**E**ventually consistent（最终一致，不保证强一致）。典型系统：Cassandra、DynamoDB。ACID 适合金融等高一致性需求；BASE 适合大规模分布式、高可用场景。
>

---

**6.** 一个 XML 文档是 "Well-formed" 但不是 "Valid"，意味着？

- A. XML 语法结构正确（标签配对、嵌套合法），但不符合 DTD/Schema 定义的业务规则
- B. XML 符合 DTD 定义，但有语法错误（如标签未闭合）
- C. 既无语法错误也符合 DTD，但文件编码有问题
- D. 文档无法被任何解析器读取

> [!tip]- 答案
>
> **答案：A**
>
> 解析：**Well-formed**：满足 XML 基本语法规则（根元素唯一、标签配对闭合、属性值有引号等）。**Valid**：除 well-formed 外，还要符合关联的 DTD 或 XML Schema 所定义的结构（如必须包含哪些元素、元素顺序、数据类型）。Well-formed 是必要条件，Valid 是更严格的约束。
>

---

**7.** 关系型数据库与图数据库相比，图数据库的核心优势是？

- A. 更强的 ACID 事务支持
- B. 更低的存储成本
- C. 高效处理深层节点关系遍历查询（如社交网络中"朋友的朋友"）
- D. 比关系型数据库更好的 SQL 兼容性

> [!tip]- 答案
>
> **答案：C**
>
> 解析：图数据库（如 Neo4j）原生存储节点（Nodes）和边（Edges/Relationships），关系遍历是 O(1) 的"指针跟随"操作。关系型数据库做多层 JOIN 时，性能随深度指数级下降。典型场景：社交网络、推荐系统、欺诈检测路径分析。
>

---

**8.** 以下 DTD 片段描述的是什么结构？

```xml
<!ELEMENT person (name, (email | phone)?, address*)>
```

- A. person 包含：name（必须）、email（必须）、address（可多个）
- B. person 包含：name（必须1次）、email 或 phone（可选，0或1次）、address（0或多次）
- C. person 包含：name（可选）、email 和 phone（两者都必须）、address（1或多次）
- D. person 的所有子元素都是可选的

> [!tip]- 答案
>
> **答案：B**
>
> 解析：按 DTD 规则解析：
> - `name`：无符号 = 必须出现恰好1次
> - `(email | phone)?`：`|` 表示二选一，`?` 表示整体出现0或1次（可选）
> - `address*`：`*` 表示出现0或多次
>
> 所以：person 必须有一个 name，可选地有 email 或 phone（两者不能同时出现），以及零个或多个 address。
>

---

## 简答题

**9.** 写出 MongoDB 查询，完成以下需求（基于 `courses` 集合）：
1. 查找所有 `credits` 大于等于 6 的课程，只返回 `name` 和 `credits` 字段（不含 `_id`）
2. 查找 `department` 为 "CS" 或 "IT" 的课程，按 `name` 升序排列
3. 插入新课程：`name="Data Engineering", credits=6, department="IT"`

> [!tip]- 答案
>
> ```javascript
> // 1. credits >= 6，只返回 name 和 credits
> db.courses.find(
>   { credits: { $gte: 6 } },
>   { name: 1, credits: 1, _id: 0 }
> )
>
> // 2. department 为 CS 或 IT，按 name 升序
> db.courses.find(
>   { department: { $in: ["CS", "IT"] } }
>   // 或: { $or: [{ department: "CS" }, { department: "IT" }] }
> ).sort({ name: 1 })
>
> // 3. 插入新课程
> db.courses.insertOne({
>   name: "Data Engineering",
>   credits: 6,
>   department: "IT"
> })
> ```
>

---

**10.** 对比 XML 和 JSON，从三个角度说明差异和各自典型用途。

> [!tip]- 答案
>
> | 角度 | XML | JSON |
> |------|-----|------|
> | **语法** | 开合标签 `<name>Alice</name>`，冗余但可读 | 键值对 `"name": "Alice"`，简洁轻量 |
> | **属性** | 支持元素属性 `<person id="1">` | 无属性概念，全部作为键值对 |
> | **元数据/Schema** | 有 DTD 和 XML Schema 用于验证结构 | 有 JSON Schema，但验证较少强制使用 |
> | **典型用途** | 企业数据交换（SOAP）、配置文件、Office 文档 | Web REST API、MongoDB 文档、现代数据交换 |
>
> **考试要点**：JSON 更轻量适合 Web API；XML 更成熟有完整的 Schema 验证机制。
>

---

**11.** 你需要为一个社交网络（用户之间有关注、好友、点赞关系，需要频繁查询"某用户好友的好友列表"）选择数据库。图数据库（Neo4j）和关系型数据库哪个更合适？写出 Neo4j Cypher 查询："查找 Alice 的所有直接好友"。

> [!tip]- 答案
>
> **图数据库（Neo4j）更合适**。
>
> 原因：社交网络的核心是关系遍历（"朋友的朋友"，多跳查询）。关系型数据库需要多层 JOIN，性能随深度指数级下降。图数据库原生存储节点和边，每次遍历是 O(1) 的"指针跟随"，无论深度如何性能都稳定。
>
> **Cypher 查询**：
> ```cypher
> MATCH (alice:Person {name: 'Alice'})-[:FRIEND]->(friend:Person)
> RETURN friend.name
> ```
>
> 解析：`MATCH` 是图模式匹配；`(alice:Person {name:'Alice'})` 找到 Alice 节点；`-[:FRIEND]->` 沿 FRIEND 关系出边遍历；`(friend:Person)` 是目标节点。
>
