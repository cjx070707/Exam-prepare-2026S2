# 第5周测试 — NoSQL 与半结构化数据

---

## 一、选择题

**1.** 以下哪项是半结构化数据的特征？

- A. 有严格固定的 schema，每条记录字段完全一致
- B. 无任何结构，完全随机
- C. 没有固定 schema，可有嵌套结构，不同对象字段可不同
- D. 只能用 JSON 格式存储

**2.** XML 中，DTD 符号 `(name+)` 表示什么？

- A. name 元素可选（零或一个）
- B. name 元素出现一次或多次
- C. name 元素出现零次或多次
- D. name 元素必须恰好出现一次

**3.** MongoDB 中以下查询等价于 SQL 中的哪条语句？

```javascript
db.students.find({ age: { $gt: 20 } }, { name: 1 })
```

- A. `SELECT * FROM students WHERE age > 20`
- B. `SELECT name FROM students WHERE age > 20`
- C. `SELECT name FROM students WHERE age >= 20`
- D. `SELECT name FROM students WHERE age = 20`

**4.** 关系型数据库与图数据库相比，图数据库的核心优势是？

- A. 强 ACID 事务支持
- B. 更高的写入性能
- C. 高效处理节点之间的关系遍历查询
- D. 更低的存储成本

**5.** 一个 XML 文档是 "Well-formed" 但不是 "Valid" 意味着？

- A. XML 语法正确，但不符合 DTD/Schema 定义的结构
- B. XML 结构正确，但有语法错误
- C. 既没有语法错误，也符合 DTD
- D. 文档无法被任何解析器读取

---

## 二、简答题

**6.** 解释 MongoDB 中 `insertOne` 时，在 MongoDB Shell 中 key 不需要引号，但在 JSON 文件中 key 必须用双引号的原因。

**7.** 对比 XML 和 JSON，从标签语法、属性支持、常见用途三个角度说明差异。

**8.** 以下 DTD 片段描述的是什么结构？

```
<!ELEMENT person (name, (email | phone)?, address*)>
```

---

## 三、应用题

**9.** 写出 MongoDB 查询，完成以下需求（基于 `courses` 集合）：

1. 查找所有 `credits` 大于等于 6 的课程，只返回 `name` 和 `credits` 字段
2. 查找 `department` 为 "CS" 或 "IT" 的所有课程，按 `name` 升序排列
3. 插入一条新课程记录：name="Data Engineering", credits=6, department="IT"

**10.** 你需要为一个社交网络（用户之间有关注、好友、点赞关系）选择数据库。关系型数据库和图数据库哪个更合适？请说明理由。

---

## 参考答案

1. **C**
2. **B**
3. **B**
4. **C**
5. **A**
6. MongoDB Shell 是 JavaScript 接口，JavaScript 允许对象 key 不加引号；而 JSON 是独立标准，要求 key 必须用双引号（标准 JSON 规范）。在 `mongoimport` 或 JSON 文件导入时必须遵循标准 JSON 格式。
7.
   | 角度 | XML | JSON |
   |------|-----|------|
   | 标签语法 | 用户自定义开合标签 `<name>Alice</name>` | key-value 对 `"name": "Alice"` |
   | 属性支持 | 有（`<person id="1">`） | 无属性概念，全部作为 key |
   | 常见用途 | 企业数据交换、SOAP Web Service | Web API、现代数据存储 |
8. `person` 元素由以下部分组成（按顺序）：
   - `name`：必须出现一次
   - `email` 或 `phone`：二选一，且可选（出现 0 或 1 次）
   - `address`：可出现零次或多次
9.
```javascript
// 1. credits >= 6，只返回 name 和 credits
db.courses.find({ credits: { $gte: 6 } }, { name: 1, credits: 1, _id: 0 })

// 2. department 为 CS 或 IT，按 name 升序
db.courses.find({ $or: [{ department: "CS" }, { department: "IT" }] }).sort({ name: 1 })

// 3. 插入新课程
db.courses.insertOne({ name: "Data Engineering", credits: 6, department: "IT" })
```
10. **图数据库（如 Neo4j）更合适**。社交网络的核心查询是关系遍历（"A 的好友的好友有谁？"），关系型数据库需要多层 JOIN，性能随关系深度急剧下降；图数据库原生存储节点和边，关系遍历是 O(1) 操作，天然适合这类场景。
