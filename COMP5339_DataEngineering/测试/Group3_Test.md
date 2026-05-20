# Group 3 Test — Special Data Types

**Scope: Week 6 (Spatial) + Week 7 (Temporal) + Week 8 (Unstructured)**

**Total: 60 marks | Suggested time: 45 minutes**

---

## Section A — Multiple Choice (2 marks each, 20 marks total)

**Q1.** Two spatial datasets are being joined: one uses SRID 4326 (WGS84) and the other uses SRID 3857 (Web Mercator). What will happen if you run `ST_Intersects(a.geom, b.geom)` without reprojecting?

- A. PostgreSQL will automatically reproject the coordinates before comparing
- B. The query will raise an error and refuse to execute
- C. The query will execute but return geometrically incorrect results
- D. The query will return an empty result set

> [!note]- Answer
> **C** — PostGIS 在 SRID 不一致时不会自动转换坐标，查询会正常执行，但结果在几何上是错误的（两套坐标系的数值直接比较，毫无意义）。不是所有版本都会报错，这就是它危险的地方。进行空间运算前必须用 `ST_Transform()` 统一到相同 SRID。

---

**Q2.** Why can a standard B-Tree index not be used for spatial queries like `ST_Contains`?

- A. B-Tree indexes are too slow for large datasets
- B. B-Tree indexes only support one-dimensional total-order comparisons, not multi-dimensional geometric relationships
- C. PostGIS does not support B-Tree indexes on geometry columns
- D. B-Tree indexes cannot store NULL values, which are common in geometry columns

> [!note]- Answer
> **B** — B-Tree 的本质是支持全序比较（大于/小于/等于），只适合一维数据。空间查询（包含、相交、距离）是多维几何关系，没有单一的大小顺序，B-Tree 无法表达。GiST（Generalised Search Tree）支持可扩展的多维索引结构，因此用 `USING GIST` 来索引 geometry 列。

---

**Q3.** Which PostGIS function would you use to find all restaurants **within** a given neighbourhood polygon?

- A. `ST_Distance(restaurant.geom, neighbourhood.geom) = 0`
- B. `ST_Intersects(neighbourhood.geom, restaurant.geom)`
- C. `ST_Contains(neighbourhood.geom, restaurant.geom)`
- D. `ST_Within(neighbourhood.geom, restaurant.geom)`

> [!note]- Answer
> **C** — `ST_Contains(A, B)` 表示 A 完全包含 B（餐厅在 neighbourhood 内）。`ST_Within(A, B)` 是镜像关系：A 在 B 内，即 `ST_Within(restaurant, neighbourhood)` 也正确，但选项 D 的参数顺序是反的（neighbourhood within restaurant）。`ST_Intersects` 包含边界相交，不严格要求"内部"。

---

**Q4.** A salary record has `valid_time_start = 2024-01-01` and `valid_time_end = 9999-12-31`. What does `valid_time_end = 9999-12-31` represent?

- A. The record was entered into the database on 9999-12-31
- B. The salary is scheduled to change on 9999-12-31
- C. The record is currently valid with no known end date
- D. The record has been archived and is no longer active

> [!note]- Answer
> **C** — `9999-12-31`（或 PostgreSQL 中的 `'infinity'`）是表示"当前有效、无已知结束日期"的哨兵值。SQL date 列无法存储真正的无穷大，用这个最大值代替。查询所有当前有效记录时用 `WHERE valid_time_end = 'infinity'`。这是 temporal 数据库的标准惯例。

---

**Q5.** A company stores employee records with both Valid Time and Transaction Time. An analyst runs the query: *"What salary did we have on record for employee X as of last Tuesday, for the period covering January 2025?"* Which time dimension does each part of the query use?

- A. Both parts use Valid Time
- B. Both parts use Transaction Time
- C. "As of last Tuesday" uses Transaction Time; "covering January 2025" uses Valid Time
- D. "As of last Tuesday" uses Valid Time; "covering January 2025" uses Transaction Time

> [!note]- Answer
> **C** — "as of last Tuesday"（截至上周二系统记录的）= **Transaction Time**（审计轨迹，系统何时知道这件事）。"covering January 2025"（2025 年 1 月成立的事实）= **Valid Time**（事实在现实中成立的时间）。这是 bitemporal 查询的经典结构。

---

**Q6.** Valid Time and Transaction Time differ in a key way. Which statement is correct?

- A. Valid Time is set automatically by the database; Transaction Time is set by the application
- B. Valid Time can be modified retroactively; Transaction Time is append-only
- C. Transaction Time can be set to a future date; Valid Time cannot
- D. Both are automatically managed by the database engine

> [!note]- Answer
> **B** — **Valid Time** 表示事实在现实中成立的时间，可以追溯修改（如法院裁定某事从过去某日期起生效）。**Transaction Time** 是数据库系统自动设置的，记录数据何时进入系统，只能向前（append-only），保证审计轨迹不可篡改。

---

**Q7.** In TF-IDF, why does the word "the" typically receive a very low score even if it appears frequently in a document?

- A. TF-IDF penalises words shorter than four characters
- B. "The" has a high TF but a very low IDF because it appears in almost every document
- C. "The" is excluded from TF-IDF calculation by default
- D. "The" has a low TF because stop words are not counted

> [!note]- Answer
> **B** — TF-IDF = TF × IDF。"the" 在单篇文档中 TF 很高，但因为几乎出现在所有文档中，IDF（log(N/df)）趋近于 0，两者相乘结果极低。这正是 TF-IDF 的设计目的：降低通用词的权重，提升区分性词汇的权重。

---

**Q8.** A sentence contains the word "bank" used in the context of a river. Which text representation correctly captures that this "bank" refers to a riverbank, not a financial institution?

- A. TF-IDF vector, because it counts exact word frequencies
- B. Word2Vec embedding, because it maps similar words to nearby vectors
- C. BERT contextual embedding, because it produces different vectors for the same word in different contexts
- D. A bag-of-words model, because it preserves word position information

> [!note]- Answer
> **C** — **BERT** 是 bidirectional 的上下文嵌入模型，同一个词在不同语境下会产生不同的向量表示。TF-IDF 和 Bag-of-Words 对"bank"只有一种表示，无法区分语义；Word2Vec 也是静态词向量，同词同向量，不感知语境。

---

**Q9.** Which of the following best describes the difference between a **white-box** and **black-box** approach to image feature extraction?

- A. White-box uses more computational resources; black-box uses less
- B. White-box features are hand-designed based on domain knowledge (e.g., gradients); black-box features are learned automatically by a neural network
- C. White-box produces sparse feature vectors; black-box produces dense vectors
- D. White-box is used for colour images; black-box is used for grayscale images

> [!note]- Answer
> **B** — **White-box**（如基于梯度的 skimage 特征）：人工设计，可解释，需要领域知识。**Black-box**（如 CNN、LLM）：神经网络自动学习特征，无需手工设计，但不可解释。两者的核心区别是"特征由人定义"还是"特征由模型学习"。

---

**Q10.** A data engineer needs to extract the GPS coordinates, camera model, and capture timestamp from 50,000 raw image files. Which tool is most appropriate?

- A. OpenCV — reads image pixel data and metadata simultaneously
- B. Pillow (PIL) — the standard Python image processing library
- C. exiftool — reads EXIF/XMP metadata from image files, supports batch processing and scripting
- D. pdfplumber — extracts structured data from files

> [!note]- Answer
> **C** — **exiftool** 专门读取图片（及其他文件）的 EXIF/XMP 元数据，支持批量处理和命令行脚本化，非常适合大规模元数据提取任务。OpenCV 和 Pillow 主要处理像素数据，不是元数据提取的主要工具。pdfplumber 是 PDF 工具。

---

## Section B — Short Answer (8 marks each, 32 marks total)

**Q11.** A city council has a database of park boundaries (polygons) and a separate dataset of public Wi-Fi access points (points). They want to find all Wi-Fi access points located inside any park. Describe how you would implement this query in PostGIS, including: the spatial query type, the index you would create, and why a standard B-Tree index would be insufficient. (8 marks)

> [!note]- Answer
> **查询类型：Spatial Join using `ST_Contains`**
> 
> ```sql
> SELECT wifi.*
> FROM wifi_points wifi, park_polygons park
> WHERE ST_Contains(park.geom, wifi.geom);
> ```
> 
> 或用 `ST_Within`（参数顺序相反，语义等价）：
> ```sql
> WHERE ST_Within(wifi.geom, park.geom)
> ```
> 
> **索引创建：GiST 索引**
> ```sql
> CREATE INDEX park_geom_idx ON park_polygons USING GIST (geom);
> CREATE INDEX wifi_geom_idx ON wifi_points USING GIST (geom);
> ```
> 
> **为什么 B-Tree 不够用：**
> B-Tree 只支持一维全序比较（`<`、`>`、`=`），它的前提是数据可以被线性排序。空间数据是二维的（经纬度），"包含"这个关系无法用大小比较来表达——两个多边形之间不存在"哪个更大"的简单顺序。GiST 支持 R-Tree 风格的多维边界矩形（MBR）索引，可以快速缩小空间搜索范围，再精确验证包含关系。
> 
> **额外注意**：执行前需确认两张表使用相同的 SRID，否则结果错误。

---

**Q12.** A hospital system stores patient diagnosis records. Diagnoses can be backdated (e.g., a diagnosis is officially recorded as effective from a past date after confirmation). The system also needs to support legal audits answering: "What did the system record about this patient on date X?" Design the temporal data model for this requirement. Explain: the two time dimensions needed, how to represent a currently-active record, and what query you would write to find all diagnoses that were valid in January 2025 AND that the system had on record as of 1 March 2025. (8 marks)

> [!note]- Answer
> **需要 Bitemporal Table（双时态表）**，包含两个时间维度：
> 
> | 时间维度 | 列名 | 含义 | 可否修改 |
> |---------|------|------|---------|
> | **Valid Time** | `valid_from`, `valid_to` | 诊断在现实中成立的时间段 | 可追溯修改 |
> | **Transaction Time** | `tx_from`, `tx_to` | 记录在数据库中存在的时间段 | Append-only，不可修改 |
> 
> **表结构示例：**
> ```sql
> CREATE TABLE diagnoses (
>     patient_id   INT,
>     diagnosis    TEXT,
>     valid_from   DATE,
>     valid_to     DATE,    -- 'infinity' 表示当前仍有效
>     tx_from      DATE,
>     tx_to        DATE     -- 'infinity' 表示当前仍在系统中
> );
> ```
> 
> **表示当前有效记录：** 用 `'infinity'`（PostgreSQL）或 `9999-12-31` 作为 `valid_to` 和 `tx_to` 的哨兵值，表示"无已知结束日期"。
> 
> **查询：2025 年 1 月有效，且截至 2025-03-01 系统有记录：**
> ```sql
> SELECT * FROM diagnoses
> WHERE valid_from  <= '2025-01-31'
>   AND valid_to    >= '2025-01-01'   -- valid time 覆盖 Jan 2025
>   AND tx_from     <= '2025-03-01'
>   AND tx_to       >= '2025-03-01';  -- 系统在 2025-03-01 时有该记录
> ```

---

**Q13.** A data science team is building a document search engine for a legal database. They are debating between TF-IDF and BERT for representing document content. Compare the two approaches across three dimensions: representation type, handling of word ambiguity, and computational cost. Then recommend which is more appropriate for legal document search and justify your choice. (8 marks)

> [!note]- Answer
> | 维度 | TF-IDF | BERT |
> |------|--------|------|
> | **表示类型** | Sparse vector（稀疏向量，维度 = 词汇表大小，大多数为 0） | Dense vector（稠密向量，如 768 维，每维都有值） |
> | **词义歧义处理** | 无法处理——同词无论语境向量相同（"bank" 银行 = "bank" 河岸） | 可处理——bidirectional transformer 根据上下文生成不同向量 |
> | **计算成本** | 低——简单统计，可在大规模文档集上快速计算 | 高——需要深度神经网络推理，索引和查询都慢得多 |
> 
> **推荐：BERT（法律文档搜索）**
> 
> 理由：
> 1. 法律文本中同一术语在不同语境下含义差异极大（如"consideration"在合同法和日常语言中含义完全不同）。TF-IDF 无法区分这类歧义，会产生大量不相关结果。
> 2. 法律搜索对精度要求极高，召回相关文档比速度更重要。
> 3. BERT 的高计算成本可通过离线预计算文档向量来缓解（查询时只需计算 query 向量，再做向量相似度搜索）。
> 
> 若文档规模极大且计算资源有限，可考虑以 TF-IDF 作为粗排，再用 BERT 对 top-K 结果重排（两阶段检索）。

---

## Section C — Code Reading (8 marks)

**Q14.** Read the following code and answer the questions below.

```python
import psycopg2
import pandas as pd

conn = psycopg2.connect("dbname=citydb user=analyst")
query = """
    SELECT
        w.wifi_id,
        w.location_name,
        ST_Distance(
            w.geom::geography,
            ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
        ) AS dist_metres
    FROM wifi_points w
    WHERE ST_DWithin(
        w.geom::geography,
        ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
        500
    )
    ORDER BY dist_metres ASC
    LIMIT 10;
"""

lon, lat = 151.2093, -33.8688
df = pd.read_sql_query(query, conn, params=(lon, lat, lon, lat))
print(df)
conn.close()
```

**(a)** What does `ST_MakePoint(%s, %s)` do, and why is the parameter order `(lon, lat)` rather than `(lat, lon)`? (2 marks)

> [!note]- Answer
> `ST_MakePoint(x, y)` 用两个数值构造一个 Point geometry。PostGIS 遵循数学坐标系惯例：`x` = 经度（longitude），`y` = 纬度（latitude）——与日常习惯的"纬度在前"相反。传入 `(lon, lat)` 而非 `(lat, lon)` 是因为 PostGIS 期望 `(x, y)` 顺序，传反了会导致坐标错误（把悉尼放到南极附近）。

**(b)** What does casting to `::geography` do? Why is it used here instead of leaving the geometry as `::geometry`? (2 marks)

> [!note]- Answer
> `::geography` 将 geometry 转换为 geography 类型，使 `ST_Distance` 和 `ST_DWithin` 的计算单位变为**米**（基于地球曲率的测地线距离），而不是坐标单位（度）。`::geometry` 的距离计算是平面欧氏距离，单位是度，在地球表面会产生误差（越靠近极点误差越大）。当需要精确的地理距离（如"500 米内"）时必须用 geography 类型。

**(c)** What does `ST_DWithin(..., 500)` do? How does it relate to the `dist_metres` column? (2 marks)

> [!note]- Answer
> `ST_DWithin(a, b, 500)` 过滤出与目标点距离在 **500 米**以内的所有 Wi-Fi 点，用于 WHERE 子句快速排除远处的点（配合空间索引效率高）。`dist_metres` 是 `ST_Distance` 计算的精确距离，用于 ORDER BY 排序。两者配合：DWithin 先粗筛（利用索引），Distance 再精确计算并排序，是空间查询的标准优化模式。

**(d)** The `params` tuple passes `(lon, lat, lon, lat)` — the same values twice. Why are four parameters needed? (2 marks)

> [!note]- Answer
> SQL 中有两处用到了同一个坐标点：一次在 SELECT 子句的 `ST_Distance`（计算实际距离），一次在 WHERE 子句的 `ST_DWithin`（过滤范围）。每个 `%s` 占位符需要单独绑定一个值，两个函数各需要 `(lon, lat)` 两个参数，合计四个。这也是参数化查询的机制——每个占位符独立绑定，不能复用。
