# COMP5339 Data Engineering — 期末模拟题

> 题型参考：短答题为主，部分 MCQ，含代码阅读题
> 满分 100 分，建议用时 2 小时
> 闭卷，不可使用 AI 工具

---

## Section A — 选择题 MCQ（每题 2 分，共 20 分）

**1.** 以下哪一项最准确地描述了 **Unbounded data**？

- A. 存储在固定大小文件中的数据集
- B. 持续产生、没有固定终点的数据流
- C. 超过 1TB 的大型数据集
- D. 没有 Schema 定义的数据

---

**2.** 一个电商平台需要实时检测欺诈交易，每秒处理数百万条交易记录。以下哪个系统组合最合适？

- A. PostgreSQL + Pandas
- B. MQTT + TimescaleDB
- C. Apache Kafka + Apache Flink
- D. MongoDB + Scrapy

---

**3.** 关于 **Valid Time** 和 **Transaction Time** 的描述，哪一项是正确的？

- A. Valid Time 只能向前移动，Transaction Time 可以向前和向后
- B. 两种时间都可以向前和向后修改
- C. Valid Time 可以向前和向后修改，Transaction Time 只能向前
- D. 两种时间都只能向前移动

---

**4.** 以下哪种存储格式最适合 OLAP 聚合查询？

- A. Row Store（行存储）
- B. Column Store（列存储）
- C. Wide Column Store
- D. Document Store

---

**5.** Apache Kafka 的消息传递语义是？

- A. At most once（至多一次）
- B. Exactly once（恰好一次）
- C. At least once（至少一次）
- D. Best effort（尽力而为）

---

**6.** 一个 XML 文档满足标签配对规则但不符合 DTD 定义的结构，该文档是？

- A. Well-formed 且 Valid
- B. Well-formed 但不 Valid
- C. 既不 Well-formed 也不 Valid
- D. Valid 但不 Well-formed

---

**7.** 在 CAP 定理中，社交媒体平台选择 AP 组合，意味着它牺牲了？

- A. Availability（可用性）
- B. Partition Tolerance（分区容忍性）
- C. Consistency（一致性）
- D. 不牺牲任何属性

---

**8.** 以下关于 **Sliding Window** 和 **Tumbling Window** 的区别，哪项正确？

- A. Sliding Window 不重叠，Tumbling Window 可以重叠
- B. Sliding Window 可以重叠，Tumbling Window 不重叠
- C. 两者都不重叠
- D. 两者都可以重叠

---

**9.** 数据工程师使用 `exiftool` 工具主要是为了？

- A. 从网页提取 HTML 表格数据
- B. 读取和提取图片/视频的元数据（如 GPS、拍摄时间）
- C. 将 CSV 文件转换为 JSON 格式
- D. 对文本数据进行 TF-IDF 特征提取

---

**10.** 以下哪项最准确地描述了 **Feature Store** 要解决的核心问题？

- A. 数据仓库存储容量不足
- B. 训练和推理时使用的 Feature 不一致（training-serving skew）
- C. 机器学习模型训练速度太慢
- D. 数据湖中数据格式混乱

---

## Section B — 短答题（每题 8 分，共 56 分）

**11. OLTP vs OLAP（W3）**

请从以下四个维度比较 OLTP 和 OLAP 系统的区别：
1. 主要读模式
2. 主要用户
3. 数据量级
4. 举一个具体的应用例子

---

**12. 数据质量（W2）**

以下数据表中存在多种数据质量问题。请识别出至少**四种**不同类型的问题，并说明每种问题属于哪个类别（Missing / Default / Incorrect / Inconsistent）。

| CustomerID | Name | Email | PostalCode | OrderDate | Category |
|------------|------|-------|------------|-----------|----------|
| 101 | Alice | alice@example.com | 2000 | 2023-12-25 | Electronics |
| 102 | Bob | NULL | 99999 | 25th Dec 2023 | electronics |
| 103 | Carol | carol@example.com | 3000 | 2023-01-15 | Electronics |
| 104 | Dana | dana@example.com | 4000 | 2023-12-31 12:00:00 | ELECTRONICS |

---

**13. Web 爬虫（W4）**

以下是一段 HTML 代码：

```html
<div id="results">
  <table class="data">
    <tr><th>City</th><th>Population</th></tr>
    <tr><td>Sydney</td><td>5,312,000</td></tr>
    <tr><td>Melbourne</td><td>5,078,000</td></tr>
  </table>
</div>
```

(a) 用 BeautifulSoup 写出两种不同方式找到这个 `<table>` 元素的代码（每种一行）。

(b) 解释 CSS Selector `div#results table.data` 的含义。

(c) 说明 Web API 和 Web 爬虫各自的优缺点（每点各两项即可）。

---

**14. 时序数据存储（W7）**

某气象局需要存储来自 500 个传感器的温度数据，每个传感器每分钟上报一次，数据需保存 10 年。

(a) 描述**点表示法（Point-based representation）**和**序列表示法（Sequence-based representation）**各自如何存储这类数据，并各给出一个 CREATE TABLE 语句示意。

(b) 对于这个场景，你会推荐哪种存储方案？说明理由（可以推荐专用时序数据库）。

---

**15. 数据分区与复制（W10）**

(a) 解释 **Hash Partitioning** 和 **Range Partitioning** 的区别，各适合什么查询场景？

(b) 解释 **Synchronous（Eager）Replication** 和 **Asynchronous（Lazy）Replication** 的区别，实际系统中更常用哪种？为什么？

(c) MongoDB 使用哪种复制策略？当读请求打到 Secondary 节点时可能出现什么问题？

---

**16. 流处理架构（W9 + W11）**

(a) 解释 **Lambda Architecture** 和 **Kappa Architecture** 各自的设计思路，并说明 Lambda 架构的主要缺点。

(b) 在流处理中，**Event Time** 和 **Processing Time** 有什么区别？什么情况下必须使用 Event Time？

(c) 什么是 **Watermark**？它在流处理中解决什么问题？

---

**17. NoSQL 对比（W5）**

某公司需要构建一个社交网络应用，需要高效查询"用户 A 的朋友的朋友中有哪些人也喜欢某个话题"。

(a) 解释为什么关系型数据库在这类查询上性能差。

(b) 图数据库（如 Neo4j）在这类场景下的优势是什么？

(c) 如果改用 MongoDB 存储社交关系数据，会遇到什么问题？

---

## Section C — 代码阅读题（每题 8 分，共 24 分）

**18. 读以下 Pandas 代码（W2）**

```python
import pandas as pd

df = pd.read_csv('power_stations.csv')

df['generatornumber'] = df['generatornumber'].fillna(0).astype(int)
df['generationmw'] = df['generationmw'].astype(float)

df.dropna(subset=['stationname'], inplace=True)

result = df[df['state'] == 'NSW'].groupby('fueltype')['generationmw'].mean()
print(result)
```

(a) 第 4 行为什么要先 `fillna(0)` 再 `astype(int)`？直接 `astype(int)` 会出什么问题？

(b) 第 7 行 `dropna(subset=['stationname'])` 和 `dropna()` 有什么区别？

(c) 描述最后两行代码的功能（用一句话说明 `result` 包含什么数据）。

---

**19. 读以下 MongoDB 查询（W5）**

```javascript
db.orders.find(
  {
    status: "shipped",
    total: { $gt: 100 },
    $or: [
      { region: "NSW" },
      { region: "VIC" }
    ]
  },
  { customer: 1, total: 1, region: 1 }
).sort({ total: -1 })
```

(a) 这个查询的完整筛选条件是什么？用自然语言描述。

(b) 第二个参数 `{ customer: 1, total: 1, region: 1 }` 的作用是什么？如果去掉它会怎样？

(c) 如果要用 SQL 表达等价查询，写出对应的 SQL 语句。

---

**20. 读以下 Spark 代码（W10）**

```python
from pyspark.sql import SparkSession
import pyspark.sql.functions as f

spark = SparkSession.builder.appName("SalesAnalysis").getOrCreate()

df = spark.read.option("header", True).csv("sales.csv")

result = df.filter(f.col("region") == "NSW") \
           .groupBy("product") \
           .agg(f.sum("amount").alias("total_sales")) \
           .orderBy("total_sales", ascending=False)

result.show(10)
```

(a) 第 7-10 行定义了 `result` 但数据还没有被处理，为什么？这体现了 Spark 的什么特性？

(b) 哪一行代码触发了实际的计算执行？

(c) 如果数据量极大（TB 级别），这段代码相比用 Pandas 直接读取有什么优势？

---

## 参考答案

<details>
<summary>展开查看答案（建议先自己做完再看）</summary>

### Section A 答案

| 题号 | 答案 | 关键理由 |
|------|------|----------|
| 1 | **B** | Unbounded = 持续产生无终点 |
| 2 | **C** | 大规模实时流 → Kafka（消息）+ Flink（处理） |
| 3 | **C** | Valid Time 反映现实可修正；Transaction Time 是数据库历史只能向前 |
| 4 | **B** | Column Store 针对聚合扫描优化，OLAP 场景 |
| 5 | **C** | Kafka 保证消息不丢但可能重复消费 |
| 6 | **B** | 标签配对 = Well-formed；不符合 DTD = 不 Valid |
| 7 | **C** | AP = 可用 + 分区容忍，牺牲一致性 |
| 8 | **B** | Sliding 可重叠；Tumbling 不重叠（固定区间） |
| 9 | **B** | exiftool 专门处理图片/视频的 EXIF/XMP 元数据 |
| 10 | **B** | Feature Store 核心解决 training-serving skew |

---

### Section B 参考答案

**11. OLTP vs OLAP**

| 维度 | OLTP | OLAP |
|------|------|------|
| 主要读模式 | 点查询（按 key 取少量记录） | 聚合扫描（COUNT/SUM 大量记录） |
| 主要用户 | Web/移动应用终端用户 | 内部数据分析师 |
| 数据量级 | GB 到 TB | TB 到 PB |
| 例子 | 银行转账系统 | 销售报表数据仓库 |

---

**12. 数据质量问题**

- Bob 的 Email = NULL → **Missing（缺失）**
- Bob 的 PostalCode = 99999 → **Default（占位符）**，不是真实邮编
- Bob 的 OrderDate = "25th Dec 2023" → **Incorrect（格式错误）**，应为标准日期格式
- Dana 的 OrderDate 含时间戳 → **Inconsistent（格式不一致）**，其他行只有日期
- Category 列大小写混用（Electronics / electronics / ELECTRONICS）→ **Inconsistent（不一致）**

---

**13. Web 爬虫**

(a)
```python
# 方式一：find_all + class
table = content.find_all('table', 'data')[0]

# 方式二：CSS selector
table = content.select('div#results table.data')[0]
```

(b) `div#results table.data`：选择 id 为 `results` 的 `<div>` 元素内部，class 为 `data` 的 `<table>` 元素。

(c)
- **Web API 优点**：返回结构化数据（JSON），稳定，有文档；**缺点**：需要认证，有访问频率限制
- **Web 爬虫优点**：可获取无 API 的网页数据；**缺点**：依赖 HTML 结构，网页改版即失效

---

**14. 时序数据存储**

(a)
```sql
-- 点表示法：每行一个时刻
CREATE TABLE Observations (
    sensor_id INT,
    ts        TIMESTAMP,
    temperature FLOAT
);

-- 序列表示法：一行存数组
CREATE TABLE Observations2 (
    sensor_id   INT,
    temperature FLOAT[],
    obs_start   TIMESTAMP,
    obs_end     TIMESTAMP
);
```

(b) 推荐**专用时序数据库**（如 TimescaleDB）：500 个传感器 × 每分钟 1 条 × 10 年 ≈ 26 亿行，点表示法行数极多但可用；专用 TSDB 提供自动时间分区、快速聚合、内置 retention policy，更适合高频大规模时序场景。序列表示法查询复杂且不可移植，不推荐。

---

**15. 分区与复制**

(a)
- **Hash Partitioning**：对 key 做哈希决定存储节点；适合**点查询**（等值查找），数据均匀分布
- **Range Partitioning**：按值范围划分；适合**范围查询**（如按时间段查询），但可能数据分布不均

(b)
- **Synchronous**：事务需等所有副本确认，一致性强，性能差
- **Asynchronous**：只写 Primary，副本异步更新，性能好，可能读到旧数据
- 实际更常用 **Asynchronous**，因为网络等待代价太高

(c) MongoDB 使用 **Primary Copy + Asynchronous（单 Leader 异步）** 复制。读 Secondary 时可能读到**旧数据**（stale read），即"Read Your Own Write"一致性违反。

---

**16. 流处理架构**

(a)
- **Lambda**：批处理（cold path）提供准确结果 + 流处理（hot path）提供低延迟结果，在 Serving Layer 合并；**缺点**：维护两套逻辑（批和流），代码重复，维护成本高
- **Kappa**：统一用流处理，批处理通过重放历史流实现，更简洁

(b) Event Time = 事件在现实中发生的时间；Processing Time = 处理引擎处理该事件的时间。当事件可能**乱序到达**（如网络延迟、传感器缓冲）时，必须使用 Event Time 才能得到正确的时间窗口结果。

(c) Watermark 是流处理器发出的一个声明："截止时间 T，所有早于 T 的事件已到达"。它解决**乱序事件和晚到数据**的问题——触发 Event Time 窗口计算，晚于 watermark 的事件被视为 late data。

---

**17. NoSQL 对比**

(a) 关系型数据库中，"朋友的朋友"需要做多次自连接（JOIN），每增加一层关系 JOIN 代价呈指数增长，性能极差。

(b) 图数据库将关系本身作为一等公民（Edge），图遍历不需要 JOIN，直接沿边走，性能远优于 RDBMS 的多层 JOIN。

(c) MongoDB 是文档型数据库，不支持原生图遍历。存社交关系需要在文档中嵌入 friend_ids 数组，查询"朋友的朋友"需要多次应用层查询，效率低且逻辑复杂。

---

### Section C 参考答案

**18. Pandas 代码**

(a) `int` 类型不支持 `NaN`，若列中有缺失值直接 `astype(int)` 会抛出 `ValueError`。先用 `fillna(0)` 把 NaN 替换成 0，再安全转换为 int。

(b) `dropna(subset=['stationname'])` 只删除 `stationname` 列为空的行，其他列有缺失值的行保留。`dropna()` 会删除**任意列**有缺失值的行，更激进，可能丢失大量数据。

(c) `result` 是 NSW 州内，按燃料类型（fueltype）分组后，每种燃料类型的**平均发电量（generationmw）**。

---

**19. MongoDB 查询**

(a) 查找 `status` 为 "shipped" **且** `total` 大于 100 **且**（`region` 为 "NSW" **或** `region` 为 "VIC"）的所有订单。

(b) 第二个参数是**投影（Projection）**，表示只返回 `customer`、`total`、`region` 三个字段（相当于 SQL 的 SELECT 指定列）。去掉则返回文档的所有字段。

(c)
```sql
SELECT customer, total, region
FROM orders
WHERE status = 'shipped'
  AND total > 100
  AND region IN ('NSW', 'VIC')
ORDER BY total DESC;
```

---

**20. Spark 代码**

(a) Spark 使用**懒执行（Lazy Evaluation）**：`filter()`、`groupBy()`、`agg()`、`orderBy()` 都是 Transformation，只记录执行计划，不触发实际计算。这让 Spark 能在执行前整体优化执行计划。

(b) 最后一行 `result.show(10)` 是 **Action**，触发实际计算。

(c) Spark 在**分布式集群**上并行处理数据，数据不需要全部载入单机内存；Pandas 需要把所有数据加载到单机内存，TB 级数据会 OOM（内存溢出）。Spark 还能利用 Catalyst 优化器和多核并行，处理速度更快。

</details>
