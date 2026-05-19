# Group 1 — 数据获取与清洗

**Week 1 (Intro + Unix) + Week 2 (Acquisition & Cleaning) + Week 4 (Web Scraping & APIs)**

> 叙事链：数据来自各种地方 → 拉进来 → 它到手时是脏的 → 清洗后才能用

---

## Part 1 — 数据从哪来（W1 + W2）

### 数据源分类

| 来源 | 例子 | 常见格式 |
|------|------|----------|
| **File Access** | 企业已有数据集，data.gov.au 下载 | CSV, Excel, XML, JSON, 图片 |
| **Database Access** | 生产系统数据库 | SQL 查询结果 |
| **Web / APIs** | 网页爬取，Web Service API | HTML, JSON, XML |
| **CDC / Logs** | 数据库变更日志，消息队列 | 流数据 |
| **Messages / Streams** | IoT 传感器，Pub/Sub 系统 | 实时流 |

### Bounded vs Unbounded Data

| 类型 | 含义 | 例子 |
|------|------|------|
| **Bounded（有界）** | 有固定大小的数据集或批次 | 下载的文件，API 一次返回的结果 |
| **Unbounded（无界）** | 持续产生、没有终点的数据 | 传感器读数流，日志流 |

> 所有 Unbounded 数据在处理前必须转换成 Bounded（划定窗口或批次）

---

## Part 2 — Unix 命令行工具（W1）

数据工程师经常在命令行处理数据，以下是核心工具：

| 命令 | 用途 | 例子 |
|------|------|------|
| `cat` | 输出文件内容 | `cat data.csv` |
| `head` / `tail` | 看前/后 N 行 | `head -5 data.csv` |
| `sort` | 排序 | `sort data.csv` |
| `grep` | 过滤匹配行 | `grep "Sydney" data.csv` |
| `wc` | 统计行/词/字符数 | `wc -l data.csv` |
| `cut` | 按列切分 | `cut -d',' -f1,3 data.csv` |
| `sed` | 流式文本替换 | `sed -e 's/hello/world/g' file` |

**Piping（管道）**：把一个命令的输出直接作为下一个命令的输入

```bash
cat data.csv | sort | head -3
```

> Unix 中"一切皆文件"——命令输出是流，可以直接通过 `|` 传递，无需中间存储

---

## Part 3 — 数据质量（W2）

### 数据质量六维度

| 维度 | 含义 | 例子 |
|------|------|------|
| **Believable** | 数据是否可信 | 非高峰期销售数据突然暴增 |
| **Value-Added** | 数据是否有用 | 与转化率无关的流量数据 |
| **Relevant** | 数据是否相关 | 把已停产品数据混入当前分析 |
| **Accurate** | 数据是否准确 | 姓名地址不匹配 |
| **Interpretable** | 数据是否可理解 | 报告中充满未定义的缩写 |

### 常见数据问题类型

| 问题 | 原因 | 处理方式 |
|------|------|----------|
| **Missing（缺失）** | 未填写、传输丢失 | `dropna()` 删除，或 `fillna()` 填充 |
| **Default（占位符）** | 用 0 / 99999 代替缺失 | 识别后替换为 NaN |
| **Incorrect（错误值）** | 传感器故障，输入错误 | 用领域知识检测，删除或修正 |
| **Inconsistent（不一致）** | 格式不统一，大小写混用 | 标准化，如统一小写 |

---

## Part 4 — Pandas 数据处理（W2）

### 读取数据

```python
import pandas as pd

# 从 CSV 读取
df = pd.read_csv('data.csv')

# 直接从 URL 读取
df = pd.read_csv('https://data.gov.au/.../file.csv')
```

### 处理缺失值

```python
df.dropna()                        # 删除含缺失值的行
df.fillna(0)                       # 用 0 填充缺失值
df['col'].fillna(0).astype(int)    # 填充后转类型
df['col'].replace('old', 'new')    # 替换特定值
```

### 类型转换

```python
df['col'] = df['col'].astype(float)
# 注意：int 不支持 NaN，转 int 前必须先处理缺失值
```

### 数据可视化（快速检验数据质量）

- **Bar Chart**：分类/名义数据
- **Histogram**：数值分布
- **Scatter Plot**：两个连续变量的关系

```python
import matplotlib.pyplot as plt
df['col'].hist()
plt.show()
```

---

## Part 5 — Web 爬虫与 API（W4）

### HTML 基础

- HTML 是树形结构（DOM 树）
- 标签有类型（`<div>`, `<table>`, `<h1>`）、class 属性、id 属性
- Web 爬虫的核心：找到正确的 HTML 元素提取数据

### HTTP 请求

```python
import requests

# GET 请求
response = requests.get("http://example.com")
print(response.status_code)   # 200 = 成功，404 = 找不到

# 带参数的 GET
response = requests.get(url, params={'key': 'value'})

# POST 请求
response = requests.post(url, params={'key': 'value'})
```

### BeautifulSoup 解析 HTML

```python
from bs4 import BeautifulSoup

content = BeautifulSoup(response.text, 'html5lib')

# 常用方法
content.find('h3')                    # 找第一个 h3
content.find_all('table')             # 找所有 table
content.find(id='results')            # 按 id 找
content.find_all('table', 'data')     # 按 class 找
content.select('#ship.data')          # 用 CSS selector
```

### CSS Selector 规则

| 选择器 | 含义 | 例子 |
|--------|------|------|
| `tag` | 按标签类型 | `table` |
| `tag.class` | 按标签 + class | `table.data` |
| `#id` | 按 id | `#results` |
| `tag:nth-child(n)` | 第 n 个子元素 | `li:first-child` |

### 提取数据到 DataFrame

```python
table = content.find_all('table')[0]
df = pd.read_html(str(table))[0]    # 只对 HTML table 有效
```

### URL 结构

```
https://www.example.com/path/resource?name=fred&address=sydney
│       │               │             └── 查询参数
│       └── 域名         └── 路径
└── 协议（http/https/ftp）
```

### Web API

- API 返回结构化数据（JSON 或 XML），不含 HTML 展示信息
- 更稳定，更适合自动化数据获取
- 很多 API 需要 API Key 认证

```python
import requests, json

response = requests.get('https://api.example.com/data',
                        params={'format': 'json'})
data = response.json()             # 直接解析 JSON
```

### 工具对比

| 工具 | 适用场景 |
|------|----------|
| `requests` + `BeautifulSoup` | 单页面/少量页面爬取 |
| `Scrapy` | 多页面自动跟链爬取（spider） |
| `Selenium` | 含 JavaScript 的动态网页 |
| `pd.read_html()` | 直接提取 HTML 表格 |
| Google Sheets `ImportHTML()` | 快速一次性导入网页表格 |

---

## 高频考点

- **Bounded vs Unbounded** 的区别和转换
- **数据质量四类问题**：Missing / Default / Incorrect / Inconsistent
- **Pandas 缺失值处理**：`dropna` / `fillna` / `replace` / `astype`
- **HTML DOM 结构**：树形，标签 + class + id
- **BeautifulSoup 方法**：`find` / `find_all` / `select`
- **CSS Selector 语法**
- **HTTP 状态码**：200 成功，404 找不到
- **API vs 爬虫**：API 返回结构化数据，更稳定
