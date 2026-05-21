# 第4周测试 — 网络爬虫与 API

---

## 选择题

**1.** HTTP 状态码 404 和 403 分别表示？

- A. 服务器内部错误；请求超时
- B. 资源未找到；权限不足（禁止访问）
- C. 请求成功；重定向
- D. 权限不足；资源未找到

<details><summary>答案</summary>

**答案：B**

解析：常见 HTTP 状态码：`200` 成功；`301/302` 重定向；`400` 请求格式错误；`403` Forbidden（有服务器但无权限）；`404` Not Found（资源不存在）；`500` 服务器内部错误；`429` 请求过于频繁（反爬常见）。

</details>

---

**2.** BeautifulSoup 中，`content.find_all('table', 'data')` 的含义是？

- A. 找所有 id 为 "data" 的 table 元素
- B. 找所有 class 为 "data" 的 table 元素
- C. 找所有包含文字 "data" 的 table 元素
- D. 找第一个 table，然后在其中再找 "data"

<details><summary>答案</summary>

**答案：B**

解析：`find_all(tag, string)` 中第二个位置参数传字符串时，BeautifulSoup 将其解释为 class 名称，等价于 `find_all('table', class_='data')`。若要按 id 查找，需显式写 `find_all('table', id='data')`。

</details>

---

**3.** CSS Selector 中，`#results` 和 `.results` 分别选中的是？

- A. class="results" 的元素；id="results" 的元素
- B. id="results" 的元素；class="results" 的元素
- C. 标签名为 "results" 的元素；包含文字 "results" 的元素
- D. 两者都选中 class="results" 的元素

<details><summary>答案</summary>

**答案：B**

解析：CSS 选择器规则：`#id名` 选中对应 id 的元素；`.class名` 选中对应 class 的元素；`标签名` 直接选标签（如 `table`、`div`）。在 BeautifulSoup 中用 `select('#results')` 或 `select('.results')`。

</details>

---

**4.** 以下哪种工具最适合抓取含 JavaScript 动态渲染内容的网页？

- A. `requests` + `BeautifulSoup`
- B. `pd.read_html()`
- C. `Selenium`
- D. `urllib`

<details><summary>答案</summary>

**答案：C**

解析：`requests` 只能获取服务器返回的静态 HTML，JavaScript 动态渲染的内容（如 React/Vue 生成的 DOM）不包含在其中。`Selenium` 控制真实浏览器执行 JS 后再抓取 DOM，适合动态页面。`pd.read_html()` 适合静态 HTML 中的 `<table>` 标签。

</details>

---

**5.** Web API 相比直接爬取 HTML 网页的主要优势是？

- A. 速度更快，可以绕过所有访问限制
- B. 返回结构化数据（JSON/XML），更稳定，不受页面改版影响
- C. 不需要任何认证就可以使用
- D. 可以获取页面上显示的所有内容（包括图片、视频）

<details><summary>答案</summary>

**答案：B**

解析：API 返回结构化数据（通常为 JSON），字段明确，解析简单；即使前端页面重新设计，API 接口通常保持兼容。HTML 爬虫依赖页面结构，页面一改版就可能失效。大多数公开 API 仍需 API Key 认证（C 错）。

</details>

---

**6.** 以下 URL 中，各部分分别代表什么？

```
https://api.data.gov.au/v1/resources?format=json&limit=100
```

- A. `https` = 路径；`api.data.gov.au` = 参数；`v1/resources` = 域名
- B. `https` = 协议；`api.data.gov.au` = 域名；`/v1/resources` = 路径；`format=json&limit=100` = 查询参数
- C. `https` = 协议；`v1/resources` = 域名；`format=json` = 路径
- D. 整个 URL 是查询参数

<details><summary>答案</summary>

**答案：B**

解析：URL 结构：`协议://域名/路径?查询参数`。此例：`https`（协议）+ `api.data.gov.au`（域名）+ `/v1/resources`（路径，表示 API 版本和端点）+ `?format=json&limit=100`（查询参数，`&` 分隔多个参数）。

</details>

---

**7.** `requests.get()` 和 `requests.post()` 的核心区别是？

- A. `GET` 比 `POST` 更安全，应该始终使用 `GET`
- B. `GET` 用于获取数据（参数在 URL 中）；`POST` 用于提交数据（参数在请求体中）
- C. `GET` 只能用于 HTML 页面，`POST` 只能用于 API
- D. `POST` 返回的状态码总是 201

<details><summary>答案</summary>

**答案：B**

解析：`GET` 是幂等操作（多次调用结果相同），参数附在 URL query string 中，适合查询操作。`POST` 参数放在请求体（body）中，适合创建/修改数据（如登录、表单提交、上传）。REST API 规范中：GET=读；POST=创建；PUT/PATCH=更新；DELETE=删除。

</details>

---

**8.** 以下 BeautifulSoup 代码能正确提取所有学生姓名吗？

```html
<ul id="student-list">
  <li class="student">Alice</li>
  <li class="student">Bob</li>
</ul>
```

```python
content = BeautifulSoup(html, 'html5lib')
names = [s.text for s in content.find_all('li', 'student')]
```

- A. 不能，应该用 `find_all('ul', 'student-list')`
- B. 能，`find_all('li', 'student')` 找所有 class="student" 的 li 元素
- C. 不能，`text` 应该替换为 `string`，两者不同
- D. 不能，需要先用 `select('#student-list')` 定位父元素

<details><summary>答案</summary>

**答案：B**

解析：`find_all('li', 'student')` 等价于 `find_all('li', class_='student')`，找所有 class 为 `student` 的 `<li>` 元素。`.text` 获取元素的文本内容（包含子元素文本），这里每个 `<li>` 直接包含文字，`.text` 正确。`.string` 在有多个子元素时会返回 None，`.text` 更通用。

</details>

---

## 简答题

**9.** 写出完整的 Python 代码，将以下 HTML 表格数据读入 Pandas DataFrame：

```html
<div id="main">
  <table class="results-table">
    <tr><th>Name</th><th>Score</th></tr>
    <tr><td>Alice</td><td>95</td></tr>
    <tr><td>Bob</td><td>87</td></tr>
  </table>
</div>
```

<details><summary>答案</summary>

```python
import requests
import pandas as pd
from bs4 import BeautifulSoup

response = requests.get('https://example.com')
content = BeautifulSoup(response.text, 'html5lib')

# 方法1：BeautifulSoup + pd.read_html
table = content.find('table', 'results-table')
df = pd.read_html(str(table))[0]

# 方法2：直接用 pd.read_html（适合静态页面中有 <table> 时）
# dfs = pd.read_html(response.text)
# df = dfs[0]
```

`pd.read_html()` 返回页面中所有 `<table>` 的列表，取 `[0]` 是第一个表格。

</details>

---

**10.** 比较 `requests + BeautifulSoup`、`Scrapy`、`Selenium` 三种工具，说明各自适用场景和主要限制。

<details><summary>答案</summary>

| 工具 | 适用场景 | 主要限制 |
|------|----------|----------|
| `requests + BeautifulSoup` | 静态 HTML 页面，少量页面抓取，快速原型 | 无法处理 JS 动态渲染；无内置并发/爬虫管理 |
| `Scrapy` | 多页面自动跟链，大规模爬取，需要 pipeline 管理 | 学习曲线较陡；仍不能直接处理 JS 渲染（需配合 Splash） |
| `Selenium` | JS 动态渲染页面，需要模拟浏览器操作（点击、登录、滚动） | 速度慢，资源消耗大；不适合大规模抓取 |

**考试要点**：Selenium 是处理动态页面的唯一选项；Scrapy 是大规模爬取的框架首选。

</details>

---

**11.** 以下代码调用了一个需要 API Key 的 REST API，但运行后返回状态码 401。问题在哪里？应如何修改？

```python
import requests
response = requests.get('https://api.example.com/data?city=Sydney')
print(response.json())
```

<details><summary>答案</summary>

**问题**：HTTP 401 Unauthorized 表示缺少有效的认证信息。该 API 需要 API Key，但代码中没有传递。

**修改方式（常见两种）**：

```python
# 方式1：API Key 作为查询参数
response = requests.get(
    'https://api.example.com/data',
    params={'city': 'Sydney', 'api_key': 'YOUR_KEY'}
)

# 方式2：API Key 放在请求头（更安全）
response = requests.get(
    'https://api.example.com/data',
    params={'city': 'Sydney'},
    headers={'Authorization': 'Bearer YOUR_KEY'}
)
```

始终检查 API 文档确认认证方式（Query param vs Header vs OAuth）。

</details>
