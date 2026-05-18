# Group 1 Test — Data Acquisition & Cleaning

**Scope: Week 1 (Intro + Unix) + Week 2 (Acquisition & Cleaning) + Week 4 (Web Scraping & APIs)**

**Total: 60 marks | Suggested time: 45 minutes**

---

## Section A — Multiple Choice (2 marks each, 20 marks total)

**Q1.** Which of the following is an example of **unbounded** data?

- A. A CSV file downloaded from data.gov.au
- B. The result set of a SQL query
- C. Continuous temperature readings from an IoT sensor
- D. A JSON response from a Web API

> [!note]- Answer
> **C** — IoT 传感器持续产生数据，没有固定终点，属于 unbounded。其余选项在获取时都是有限大小的数据集，属于 bounded。

---

**Q2.** Which Unix command counts the **number of lines** in a file?

- A. `cut -l data.csv`
- B. `wc -l data.csv`
- C. `grep -c data.csv`
- D. `sort -n data.csv`

> [!note]- Answer
> **B** — `wc -l` 统计行数。`-c` 统计字节数，`-w` 统计词数。`grep -c` 需要提供匹配模式，不是统计总行数。

---

**Q3.** A dataset contains temperature records where the value is `99999`, which is physically impossible. What type of data quality issue is this?

- A. Missing
- B. Incorrect
- C. Default
- D. Inconsistent

> [!note]- Answer
> **C** — 这是 **Default（占位符）**问题：用一个极端数值（`99999`）来代替真正的缺失值，而不是留空。**Incorrect** 指传感器故障或输入错误导致的真实错误值；**Missing** 指字段为空。

---

**Q4.** What does the following Pandas code do?

```python
df['age'].fillna(0).astype(int)
```

- A. Drops all rows where `age` is NaN, then converts to integer
- B. Replaces NaN in `age` with 0, then converts the column to integer type
- C. Replaces 0s in `age` with NaN, then converts to integer
- D. Converts `age` to integer; raises an error if NaN is present

> [!note]- Answer
> **B** — `fillna(0)` 先把 NaN 替换为 0（必须这一步，因为 Python 的 `int` 类型无法表示 NaN），然后 `astype(int)` 将整列转为整数类型。如果不先 `fillna`，直接 `astype(int)` 会抛出 `ValueError`。

---

**Q5.** Which BeautifulSoup call returns **all** `<table>` elements with class `data`?

- A. `content.find('table', 'data')`
- B. `content.find_all('table', 'data')`
- C. `content.select('table#data')`
- D. `content.find(class_='data')`

> [!note]- Answer
> **B** — `find_all` 返回所有匹配元素的列表；`find` 只返回第一个。选项 C 用了 `#`，是按 **id** 选择而非 class。选项 D 匹配任意 class 为 `data` 的元素，不限于 `<table>`。

---

**Q6.** What does the CSS selector `table.results` match?

- A. A `<table>` with id `results`
- B. Any element with class `results`
- C. A `<table>` with class `results`
- D. A `<table>` containing a child element named `results`

> [!note]- Answer
> **C** — `tag.class` 格式匹配指定标签类型 + 指定 class 的元素。`#results` 才是按 id 选择；`.results`（不带标签名）匹配任意 class 为 `results` 的元素。

---

**Q7.** After calling `requests.get()`, a `response.status_code` of `404` means:

- A. Internal server error
- B. Request succeeded
- C. Resource not found
- D. Authentication required

> [!note]- Answer
> **C** — HTTP 404 = Not Found（资源不存在）。200 = 成功；500 = 服务器内部错误；401 = 未授权。

---

**Q8.** Compared to scraping HTML pages directly, what is the primary advantage of using a Web API?

- A. APIs do not require a network connection
- B. APIs return structured data (JSON/XML) that is stable and not affected by page redesigns
- C. APIs are faster because they bypass the HTTP protocol
- D. APIs require no parsing whatsoever

> [!note]- Answer
> **B** — API 返回结构化数据（通常是 JSON），接口稳定，不会因为网页改版而失效。直接爬 HTML 的缺点是：一旦页面布局改变，爬虫就会失效。API 仍然使用 HTTP 协议，也需要解析数据，但结构更可预期。

---

**Q9.** Which tool is best suited for scraping a website that **requires JavaScript to render** its content?

- A. `requests` + `BeautifulSoup`
- B. `Scrapy`
- C. `Selenium`
- D. `pd.read_html()`

> [!note]- Answer
> **C** — `Selenium` 驱动真实浏览器，可以执行 JavaScript。`requests` 只获取原始 HTML，不执行 JS；`BeautifulSoup` 和 `Scrapy` 同理。`pd.read_html()` 只解析静态 HTML 表格。

---

**Q10.** How many query parameters does the following URL contain?

```
https://api.example.com/data?format=json&limit=100
```

- A. 1
- B. 2
- C. 3
- D. Cannot be determined

> [!note]- Answer
> **B** — `format=json` 和 `limit=100` 是两个独立的查询参数，以 `&` 分隔。`?` 标识查询字符串的起始位置。

---

## Section B — Short Answer (8 marks each, 32 marks total)

**Q11.** Explain the difference between **Bounded** and **Unbounded** data. Give one example of each. What transformation must be applied to unbounded data before it can be processed, and why? (8 marks)

> [!note]- Answer
> - **Bounded data**：有固定大小、有终点的数据集，获取时全量可用。例：从政府网站下载的 CSV 文件、一次 SQL 查询的结果集。
> - **Unbounded data**：持续产生、没有终点的数据流。例：IoT 传感器实时上报的温度数据、社交媒体的实时评论流。
> - **必要转换**：处理 unbounded 数据前，必须划定 **window（窗口）** 或 **batch（批次）**，将其截断为有限范围。原因：任何聚合操作（SUM、COUNT、AVG）都需要一个明确的边界——不可能对无穷序列求平均值。窗口为计算提供了有限的范围（如"过去 5 分钟"），使结果能够被产出。

---

**Q12.** A data engineer receives a hospital patient record CSV and finds the following issues:
- Several rows have a blank `age` field
- The `gender` column contains `M`, `Male`, and `男` entries
- Some rows have a `weight` value of `0`, which is medically impossible

Identify the data quality problem type for each issue and describe how to handle it. (8 marks)

> [!note]- Answer
> | 问题 | 类型 | 处理方式 |
> |------|------|----------|
> | `age` 字段为空 | **Missing**（缺失）：值从未被记录或在传输中丢失 | `fillna()` 用中位数填充，或若该字段关键则 `dropna()` 删除该行 |
> | `gender` 写法不统一 | **Inconsistent**（不一致）：同一概念用多种格式表达 | `.replace({'Male': 'M', '男': 'M'})` 统一为单一编码 |
> | `weight` = 0 | **Default**（占位符）：用 0 代替缺失值，并非真实体重 | `.replace(0, np.nan)` 转为真正的缺失值，再按 Missing 处理 |

---

**Q13.** Compare `requests` + `BeautifulSoup` with `Scrapy` as web scraping tools. When should you choose `Scrapy`? (8 marks)

> [!note]- Answer
> | 维度 | `requests` + `BeautifulSoup` | `Scrapy` |
> |------|------------------------------|----------|
> | 上手难度 | 低，代码简单直接 | 较高，需要 Spider 类和项目结构 |
> | 适合场景 | 单页或少量已知 URL 的抓取 | 需要自动跟链的多页大规模爬取 |
> | 并发 | 默认单线程 | 内置异步请求引擎 |
> | 内置功能 | 无，需手动处理 | 去重、速率限制、pipeline、重试 |
> 
> **选 `Scrapy` 的时机**：需要跟踪分页链接或爬取整站结构；需要自动处理 retry 和 rate limiting；需要将数据写入多个目标（数据库、JSON、CSV）；爬虫需要定期重复运行。

---

**Q14.** A data engineer has two choices: **"push compute into the DBMS"** or **"pull all data into Python"**. Explain the approach, use case, and limitation of each. (8 marks)

> [!note]- Answer
> **Push compute into the DBMS**
> - 思路：在数据库内用 SQL 完成过滤、聚合、JOIN，Python 只接收最终的少量结果集。
> - 适用场景：大表中只需要少量数据；聚合查询能利用数据库索引和查询优化器。
> - 局限：复杂的统计分析或 ML 工作流难以用 SQL 表达。
> 
> **Pull all data into Python**
> - 思路：把整张表或大批数据拉入 Pandas DataFrame，在 Python 中处理。
> - 适用场景：探索性分析，需要灵活变换；数据集较小，能放进内存。
> - 局限：数据必须能放进内存（大数据集有 OOM 风险）；网络传输开销大；失去数据库查询优化的优势。

---

## Section C — Code Reading (8 marks)

**Q15.** Read the following code and answer the questions below.

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

**(a)** Which table on the page does `find_all('table')[1]` select? (1 mark)

> [!note]- Answer
> 页面上的**第二张表**。Python 列表索引从 0 开始，`[1]` 是第二个元素。

**(b)** What does `pd.read_html(str(table))[0]` do? Why is `[0]` needed? (2 marks)

> [!note]- Answer
> `pd.read_html()` 解析 HTML 字符串中所有的 `<table>` 元素，返回一个 **DataFrame 列表**。因为 `str(table)` 只含一张表，列表里只有一个元素，`[0]` 取出这唯一的 DataFrame。

**(c)** What is the difference between `dropna(subset=['Score'])` and `dropna()`? (2 marks)

> [!note]- Answer
> - `dropna(subset=['Score'])`：只删除 `Score` 列为 NaN 的行，其他列有 NaN 的行保留。
> - `dropna()`：删除**任意列**含有 NaN 的行，影响范围大得多，容易误删有效数据。

**(d)** Describe what the last three lines do and summarise the overall goal of this script in one sentence. (3 marks)

> [!note]- Answer
> 最后三行：筛选出 Score > 80 的行 → 按 Score 降序排列 → 打印前 10 条。
> 
> **整体目标**：从网页排行榜抓取表格，清洗数据后，输出得分最高的前 10 名记录。
