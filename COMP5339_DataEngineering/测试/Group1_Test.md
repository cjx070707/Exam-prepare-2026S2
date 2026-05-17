# Group 1 测试题 — 数据获取与清洗

**覆盖范围：Week 1 (Intro + Unix) + Week 2 (Acquisition & Cleaning) + Week 4 (Web Scraping & APIs)**

**总分：60 分 | 建议用时：45 分钟**

---

## Section A — MCQ（每题 2 分，共 20 分）

**Q1.** 下列哪种数据源属于 Unbounded（无界）数据？

- A. 从 data.gov.au 下载的 CSV 文件
- B. 数据库中的一次 SQL 查询结果
- C. IoT 传感器持续上报的温度读数
- D. Web API 返回的 JSON 响应

---

**Q2.** 以下 Unix 命令中，哪个命令用于**统计文件行数**？

- A. `cut -l data.csv`
- B. `wc -l data.csv`
- C. `grep -c data.csv`
- D. `sort -n data.csv`

---

**Q3.** 某数据集中，气温字段出现了大量 `99999` 的值，但实际不可能达到这个温度。这属于哪类数据质量问题？

- A. Missing（缺失）
- B. Incorrect（错误值）
- C. Default（占位符）
- D. Inconsistent（不一致）

---

**Q4.** 以下 Pandas 代码的作用是什么？

```python
df['age'].fillna(0).astype(int)
```

- A. 删除 `age` 列中所有 NaN 行，然后转为整数
- B. 将 `age` 列的 NaN 替换为 0，然后将整列转为整数类型
- C. 将 `age` 列的 0 替换为 NaN，然后转为整数
- D. 将 `age` 列转为整数，遇到 NaN 时报错

---

**Q5.** 以下 BeautifulSoup 调用中，哪个可以找到**所有** class 为 `data` 的 `table` 元素？

- A. `content.find('table', 'data')`
- B. `content.find_all('table', 'data')`
- C. `content.select('table#data')`
- D. `content.find(class_='data')`

---

**Q6.** CSS Selector `table.results` 的含义是：

- A. id 为 `results` 的 `table`
- B. class 为 `results` 的任意元素
- C. class 为 `results` 的 `table`
- D. 包含子元素 `results` 的 `table`

---

**Q7.** 使用 `requests.get()` 后，`response.status_code` 返回 `404` 表示：

- A. 服务器内部错误
- B. 请求成功
- C. 资源未找到
- D. 需要身份验证

---

**Q8.** Web API 与直接爬取 HTML 网页相比，主要优势是：

- A. 不需要网络连接
- B. 返回结构化数据（JSON/XML），更稳定，不受页面改版影响
- C. 速度更快，因为不经过 HTTP 协议
- D. 不需要解析任何格式

---

**Q9.** 以下哪个工具最适合爬取**需要 JavaScript 渲染**的动态网页？

- A. `requests` + `BeautifulSoup`
- B. `Scrapy`
- C. `Selenium`
- D. `pd.read_html()`

---

**Q10.** URL `https://api.example.com/data?format=json&limit=100` 中，查询参数有几个？

- A. 1
- B. 2
- C. 3
- D. 无法判断

---

## Section B — 短答题（每题 8 分，共 32 分）

**Q11.** 请解释 Bounded 和 Unbounded 数据的区别，并各举一个例子。说明 Unbounded 数据在处理前需要做什么转换，以及为什么。（8分）

---

**Q12.** 某数据工程师从某市卫生局获得了一份医院就诊记录 CSV，发现以下问题：
- 部分行的"年龄"列为空
- 性别列出现了 `M`、`Male`、`男` 三种写法
- 有几行的体重值为 `0`，但医疗记录不可能为 0

请说明每个问题分别属于哪类数据质量问题，并说明处理方法。（8分）

---

**Q13.** 解释 `requests` + `BeautifulSoup` 与 `Scrapy` 的适用场景差异。什么情况下应该选择 `Scrapy`？（8分）

---

**Q14.** 数据工程师有两种处理数据库查询结果的方式："Push compute into DBMS" 和 "Pull all data into Python"。分别解释这两种方式的思路，并说明各自的适用场景和局限。（8分）

---

## Section C — 代码阅读（共 8 分）

**Q15.** 阅读以下代码，回答问题：

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://example.com/rankings"
response = requests.get(url)

content = BeautifulSoup(response.text, 'html5lib')
table = content.find_all('table')[1]
df = pd.read_html(str(table))[0]

df = df.dropna(subset=['Score'])
df['Score'] = df['Score'].astype(float)
df_top = df[df['Score'] > 80].sort_values('Score', ascending=False)

print(df_top.head(10))
```

(a) `find_all('table')[1]` 取的是页面上哪一个 table？（1分）

(b) `pd.read_html(str(table))[0]` 的作用是什么？为什么要加 `[0]`？（2分）

(c) `dropna(subset=['Score'])` 和直接 `dropna()` 有什么区别？（2分）

(d) 最后三行代码做了什么？用一句话描述整个数据处理流程的目标。（3分）

---

<details>
<summary>📋 参考答案（点击展开）</summary>

### Section A 答案

| 题号 | 答案 | 解析 |
|------|------|------|
| Q1 | **C** | IoT 传感器持续上报，没有终点 → Unbounded；其余都是有固定大小的批次 |
| Q2 | **B** | `wc -l` 统计行数；`-c` 统计字节数，`-w` 统计词数 |
| Q3 | **C** | 用极端数值（99999）代替缺失值 → Default（占位符）；Incorrect 指真正的传感器故障数据 |
| Q4 | **B** | `fillna(0)` 先将 NaN 替换为 0，再用 `astype(int)` 转为整数 |
| Q5 | **B** | `find_all('table', 'data')` 返回所有匹配的元素列表；`find` 只返回第一个 |
| Q6 | **C** | `tag.class` → class 为 `results` 的 `table` 标签；`#` 才是 id 选择器 |
| Q7 | **C** | HTTP 404 = Not Found（资源未找到）；200 = 成功；500 = 服务器内部错误 |
| Q8 | **B** | API 返回结构化数据，接口稳定；HTML 可能因页面改版而失效 |
| Q9 | **C** | Selenium 可以驱动真实浏览器，执行 JavaScript；其他工具不能处理动态渲染 |
| Q10 | **B** | `format=json` 和 `limit=100` 共 2 个查询参数 |

### Section B 参考答案

**Q11.**
- **Bounded**：有固定大小、有终点的数据集。例：下载的 CSV 文件、API 返回的 JSON 响应。
- **Unbounded**：持续产生、没有终点的数据流。例：IoT 传感器实时上报的温度数据、社交媒体的实时评论流。
- **转换**：处理 Unbounded 数据前必须划定窗口（Window）或批次（Batch），将其截断为 Bounded。原因：计算引擎无法对无穷序列执行聚合操作，必须定义一个时间或数量边界才能产出结果。

**Q12.**
- "年龄"列为空 → **Missing（缺失）**：处理方式：用 `fillna()` 填充均值/中位数，或 `dropna()` 删除该行（视下游分析需求）。
- 性别列写法不统一 → **Inconsistent（不一致）**：处理方式：标准化映射，如 `replace({'Male': 'M', '男': 'M'})`，统一为单一编码。
- 体重值为 0 → **Default（占位符）**：0 是系统默认填入值，并非真实体重。处理方式：将 0 替换为 `NaN`，再按缺失值处理。

**Q13.**
- `requests` + `BeautifulSoup`：适合**单页或少量页面**爬取，代码简单直接，适合快速原型和一次性任务。
- `Scrapy`：适合**多页面自动跟链**（spider）的大规模爬取，内置请求队列、去重、并发管理、管道处理，适合系统化、长期运行的爬虫项目。
- 选择 `Scrapy` 的场景：需要跟踪分页链接、需要爬取整个站点结构、需要处理反爬（速率限制）、需要将数据导出到多个目标（数据库、文件）。

**Q14.**
- **Push compute into DBMS**：在数据库内执行 SQL（聚合、过滤、JOIN），只把最终结果传回 Python。优势：利用数据库索引和查询优化器，传输量小，可扩展。局限：复杂的统计分析或 ML 在 SQL 中难以表达。
- **Pull all data into Python**：将全表或大批数据拉入 Pandas DataFrame，在 Python 中处理。优势：灵活，可用任意 Python 库。局限：数据必须能放进内存，大数据集会 OOM；网络传输开销大。

**Q15.**

(a) 页面上**第二个** table（索引从 0 开始，`[1]` = 第二个）。

(b) `pd.read_html()` 将 HTML 字符串中所有 table 解析为 DataFrame 列表；`[0]` 取列表中第一个（也是唯一一个，因为 `str(table)` 只含一张表）。

(c) `dropna(subset=['Score'])` 只删除 `Score` 列为空的行，其他列有 NaN 的行保留；`dropna()` 会删除**任意列**含有 NaN 的行，影响范围更大，可能丢失过多数据。

(d) 最后三行：筛选出 Score > 80 的行，按 Score 降序排列，打印前 10 条。整体目标：从网页排行榜中提取表格，清洗数据后，找出得分最高的前 10 名记录。

</details>
