# 第4周测试 — 网络爬虫与 API

---

## 一、选择题

**1.** HTTP 状态码 404 表示什么？

- A. 服务器内部错误
- B. 请求成功
- C. 资源未找到
- D. 权限不足

**2.** BeautifulSoup 中，`content.find_all('table', 'data')` 的含义是？

- A. 找所有 id 为 "data" 的 table 元素
- B. 找所有 class 为 "data" 的 table 元素
- C. 找所有包含 "data" 文本的 table 元素
- D. 找第一个 table 元素，然后在其中找 "data"

**3.** CSS Selector `#results` 选中的是？

- A. class 为 "results" 的元素
- B. id 为 "results" 的元素
- C. 标签名为 "results" 的元素
- D. 包含文字 "results" 的元素

**4.** 以下哪种工具最适合抓取含 JavaScript 动态渲染内容的网页？

- A. `requests` + `BeautifulSoup`
- B. `pd.read_html()`
- C. `Selenium`
- D. `Scrapy`

**5.** Web API 相比直接爬取 HTML 网页的优势是？

- A. 速度更快，可以获取更多数据
- B. 返回结构化数据，更稳定，不受页面改版影响
- C. 不需要任何认证就可以使用
- D. 可以获取网页上显示的所有内容

---

## 二、简答题

**6.** 解释 `requests.get()` 和 `requests.post()` 的区别，分别适用于什么场景？

**7.** 以下 URL 中，各部分分别代表什么？

```
https://api.data.gov.au/v1/resources?format=json&limit=100
```

**8.** 写出 BeautifulSoup 代码，从以下 HTML 中提取所有学生的姓名：

```html
<ul id="student-list">
  <li class="student">Alice</li>
  <li class="student">Bob</li>
  <li class="student">Carol</li>
</ul>
```

---

## 三、应用题

**9.** 你需要从一个网站抓取表格数据，网站的 HTML 结构如下：

```html
<div id="main">
  <table class="results-table">
    <tr><th>Name</th><th>Score</th></tr>
    <tr><td>Alice</td><td>95</td></tr>
    <tr><td>Bob</td><td>87</td></tr>
  </table>
</div>
```

写出完整的 Python 代码，将这张表格的数据读入 Pandas DataFrame。

**10.** 比较 `requests + BeautifulSoup`、`Scrapy`、`Selenium` 三种工具，说明各自适用场景。

---

## 参考答案

1. **C**
2. **B**
3. **B**
4. **C**
5. **B**
6. `GET` 用于获取数据，参数附在 URL 中，适合查询操作；`POST` 用于提交数据，参数在请求体中，适合登录、表单提交等写操作。
7.
   - `https`：协议
   - `api.data.gov.au`：域名
   - `/v1/resources`：路径
   - `format=json&limit=100`：查询参数（format 和 limit 两个参数）
8.
```python
from bs4 import BeautifulSoup
content = BeautifulSoup(html, 'html5lib')
students = content.find_all('li', 'student')
names = [s.text for s in students]
```
9.
```python
import requests, pandas as pd
from bs4 import BeautifulSoup

response = requests.get('https://example.com')
content = BeautifulSoup(response.text, 'html5lib')
table = content.find('table', 'results-table')
df = pd.read_html(str(table))[0]
```
10.
| 工具 | 适用场景 |
|------|----------|
| `requests + BeautifulSoup` | 静态页面，少量页面抓取，快速原型 |
| `Scrapy` | 多页面自动跟链，大规模爬取，需要爬虫框架管理 |
| `Selenium` | 含 JavaScript 动态渲染的页面，需要模拟浏览器操作 |
