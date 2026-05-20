# Group 3 — 特殊数据类型

**Week 6 (Spatial) + Week 7 (Temporal) + Week 8 (Unstructured)**

> 叙事链：通用存储和查询对空间、时序、非结构化数据都不够用 → 每种类型有自己的数据模型、索引方式和查询语义

> W7 和 W8 的详细内容已在 `Quiz2_Revision_W7-W11.md` 中，本文件作为完整归档版

---

## Part 1 — 空间数据（W6）

### 为什么需要专门处理

普通数据库支持点查询和范围查询，但空间查询（"找出距我 10km 内的餐厅"）需要：
- 理解地理坐标的几何含义
- 高效的空间索引
- 专用的空间操作符

### 空间数据类型

| 类型 | 含义 | 例子 |
|------|------|------|
| **Point** | 单个位置坐标 (x, y) | GPS 坐标，地址 |
| **LineString** | 有序点的连线 | 道路，河流 |
| **Polygon** | 封闭区域 | 行政区划，建筑轮廓 |
| **Geometry** | 以上类型的统称 | — |

### 坐标系（SRID）

- **SRID（Spatial Reference ID）**：定义坐标的参考系
- **WGS84（SRID 4326）**：GPS 使用的标准经纬度坐标系
- 进行空间运算时，所有数据必须使用**相同的 SRID**，否则结果错误

### 空间查询类型

| 查询类型 | 含义 | SQL 函数（PostGIS） |
|----------|------|---------------------|
| **Distance** | 两点间距离 | `ST_Distance(a, b)` |
| **Contains** | A 是否包含 B | `ST_Contains(a, b)` |
| **Intersects** | A 和 B 是否相交 | `ST_Intersects(a, b)` |
| **Within** | A 是否在 B 内 | `ST_Within(a, b)` |
| **Spatial Join** | 按空间关系连接两张表 | `WHERE ST_Contains(region, point)` |

### 空间索引

- 普通 B-Tree 索引无法处理空间查询（不支持多维比较）
- **GiST（Generalised Search Tree）**：PostgreSQL 的通用索引，支持空间数据
- **R-Tree**：另一种常用空间索引，按边界矩形分层组织空间对象

```sql
CREATE INDEX spatial_idx ON Locations USING GIST (geom);
```

### 空间数据格式

| 格式 | 特点 | 用途 |
|------|------|------|
| **GeoJSON** | JSON 格式的空间数据，易与 Web API 配合 | Web 地图，API 数据交换 |
| **KML** | XML 格式，Google Earth 使用 | 地理数据可视化 |
| **WKT** | Well-Known Text，如 `POINT(151.2 -33.8)` | 数据库存储 |

### 工作流程

```
获取含空间属性的数据（CSV with lat/lon，GeoJSON API）
→ 存入数据库（PostGIS 扩展）
→ 确保坐标系（SRID）一致
→ 建空间索引（GiST）
→ 执行空间查询（距离、包含、空间 Join）
→ 导出为 GeoJSON/KML 可视化
```

---

## Part 2 — 时序数据（W7）

> 详细内容见 `Quiz2_Revision_W7-W11.md` — Week 7 部分

### 核心概念速查

**两种时间语义**：

| 时间 | 含义 | 特点 |
|------|------|------|
| **Valid Time** | 事实在现实中成立的时间 | 可向前/向后修改 |
| **Transaction Time** | 数据存入数据库的时间 | 只能向前，支持审计回溯 |

**Bitemporal table** = 同时包含两种时间列的表

**表示"现在"**：用 `9999-12-31`（max-timestamp），PostgreSQL 用 `'infinity'`

**时态查询三类**：Current（当前）/ Sequenced（某时刻）/ Nonsequenced（任意时刻）

### 时序存储三方案对比

| 方案 | 结构 | 优点 | 缺点 |
|------|------|------|------|
| **Point-based** | 每行一个时刻 | 标准 SQL，容易索引 | 高频数据行数多 |
| **Sequence-based** | 一行存数组 | 紧凑，适合批量分析 | 查询复杂，不可移植 |
| **Dedicated TSDB** | TimescaleDB / InfluxDB | 高性能，内置时间特性 | 额外维护成本 |

---

## Part 3 — 非结构化数据（W8）

> 详细内容见 `Quiz2_Revision_W7-W11.md` — Week 8 部分

### 核心概念速查

**处理流程**：
```
原始数据（文本/图片）→ 预处理 → 特征提取 → 数值向量 → ML / 相似度搜索
```

**文本特征提取**：

| 方法 | 类型 | 特点 |
|------|------|------|
| **TF-IDF** | Bag of Words | 稀疏，无语义，计算简单 |
| **Word2Vec** | 词向量 | 稠密，有语义相似性 |
| **BERT** | 上下文嵌入 | 同词不同语境有不同向量（bidirectional） |

**图像类型**：RGB（3通道 24bit）/ Grayscale（单通道）/ Binary（黑白 mask）

**特征提取两种路径**：
- White box：手工设计（基于图像梯度，如 skimage）
- Black box：神经网络自动学习（CNN、LLM）

**元数据工具**：`exiftool`（读取 EXIF/XMP 元数据，支持批量、脚本化）

---

## 高频考点

**空间（W6）**：
- GeoJSON vs KML：格式和用途
- SRID 的作用：坐标系必须一致
- 空间索引：GiST（PostgreSQL），为什么普通 B-Tree 不够用
- 四类空间查询：Distance / Contains / Intersects / Spatial Join

**时序（W7）**：
- Valid Time vs Transaction Time：哪个能修改，哪个只能向前
- Bitemporal table 的定义
- 三种时序存储方案的优缺点对比
- MAX-timestamp 方法（`9999-12-31`）

**非结构化（W8）**：
- 为什么非结构化数据需要特征提取才能用于 ML
- TF-IDF 的计算逻辑（TF × IDF）
- BERT 和 TF-IDF 的核心区别（有无上下文语义）
- exiftool 能做什么
