# 第4周测试 — 网络爬虫与 API

---

## 选择题

**1.** Web Scraping 的五步流程按顺序是？

- A. Extraction → Retrieval → Reconnaissance → Cleaning → Storage
- B. Reconnaissance → Retrieval → Extraction → Cleaning → Storage
- C. Retrieval → Reconnaissance → Extraction → Storage → Cleaning
- D. Reconnaissance → Extraction → Retrieval → Cleaning → Storage

> [!tip]- 答案
> **答案：B**
> 解析：标准五步流程：**Reconnaissance**（侦查：确认目标页面结构、检查 robots.txt 和 ToS）→ **Retrieval**（获取：发送 HTTP 请求下载页面）→ **Extraction**（提取：从 HTML 中解析目标数据）→ **Cleaning**（清洗：处理缺失、格式不一致等）→ **Storage**（存储：写入文件/数据库）。顺序考点常出，Reconnaissance 必须在最前。

---

**2.** 在 Reconnaissance 阶段，为什么必须检查 `robots.txt` 和网站服务条款（Terms of Service）？

- A. 因为 `robots.txt` 会阻止所有爬虫访问，检查后可以绕过它
- B. 违反 `robots.txt` 或 ToS 可能导致 IP 被封或面临法律风险，爬取前必须确认合规
- C. `robots.txt` 记录了网站所有页面的 URL，可用于生成爬取列表
- D. ToS 只对商业用途有效，学术用途可以忽略

> [!tip]- 答案
> **答案：B**
> 解析：`robots.txt` 是网站声明哪些路径允许/禁止爬虫访问的约定文件（如 `Disallow: /private/`）。忽略它不一定在技术上被阻止，但可能违反平台政策，导致 IP 封禁甚至法律追究。ToS 同理，即便是学术用途也不自动豁免。Reconnaissance 阶段的核心任务之一就是合规性确认。

---

**3.** 以下关于静态页面与动态页面的说法，哪项正确？

- A. 静态页面指内容每天不变；动态页面指内容每秒都变
- B. 动态页面由 JavaScript 在浏览器端渲染，`requests.get()` 获取的 HTML 中不含最终数据
- C. `pd.read_html()` 可以解析动态页面中的表格，因为它会自动执行 JavaScript
- D. Selenium 和 `requests` 对动态页面的处理能力相同

> [!tip]- 答案
> **答案：B**
> 解析：动态页面的数据由 JavaScript 在客户端浏览器执行后才被注入 DOM（如 React/Vue 渲染的内容）。`requests.get()` 只下载服务器返回的原始 HTML，JavaScript 尚未执行，因此目标数据缺失。`pd.read_html()` 底层调用 `requests`，同样无法处理动态内容（C 错）。Selenium 控制真实浏览器，JS 执行完毕后再抓取 DOM，是处理动态页面的标准方案（D 错）。

---

**4.** HTTP 状态码 `429` 最可能的含义及其在爬虫场景中的含义是？

- A. 服务器内部错误，与爬虫无关
- B. 资源不存在，目标页面已被删除
- C. 请求过于频繁（Too Many Requests），服务器正在对爬虫进行限速或封锁
- D. 认证失败，需要提供正确的 API Key

> [!tip]- 答案
> **答案：C**
> 解析：常见状态码速记：`200` 成功；`403` Forbidden（权限不足）；`404` Not Found（资源不存在）；`429` Too Many Requests（请求速率超限，反爬机制常用）；`401` Unauthorized（未认证）。爬虫遇到 `429` 应降低请求频率或加入随机延迟。

---

**5.** 比较四种内容提取方式，以下说法哪项最准确？

- A. XPath 和 CSS Selector 功能完全相同，任意场景可互换使用
- B. Text Patterns（正则表达式）是最推荐的提取方式，因为速度最快
- C. XPath 支持向上查找父节点和谓语条件过滤；CSS Selector 不支持向上选择父节点
- D. DOM Navigation（如 `.parent`、`.children`）比 CSS Selector 更适合结构复杂的页面

> [!tip]- 答案
> **答案：C**
> 解析：四种方式对比：**Text Patterns**（正则）灵活但脆弱，HTML 稍变则失效；**DOM Navigation** 逐级遍历，代码繁琐；**CSS Selector** 简洁、广泛支持，但只能向下选择后代，**无法选中父节点**；**XPath** 功能最强，支持 `//div[contains(@class,"row")]` 等谓语过滤，也支持 `..` 逆向查找父节点，适合复杂结构提取。考试高频考点：XPath 能做而 CSS Selector 做不到的事。

---

**6.** 关于 RESTful API 与 SOAP 的区别，以下哪项描述最准确？

- A. REST 使用 XML 消息封装，SOAP 使用 JSON；两者都是无状态的
- B. REST 基于 HTTP 动词（GET/POST 等）、通常返回 JSON，是无状态的；SOAP 使用 XML 消息格式，协议更复杂
- C. SOAP 比 REST 更现代，是当前 Web API 的主流标准
- D. REST 和 SOAP 都必须使用 HTTPS，否则无法正常工作

> [!tip]- 答案
> **答案：B**
> 解析：**REST**（Representational State Transfer）：无状态、利用 HTTP 动词语义（GET=读、POST=创建、PUT=更新、DELETE=删除）、通常返回 JSON，简洁易用，是当前 Web API 主流（课程中 web service = REST）。**SOAP**：基于 XML 的消息协议，有严格的信封（Envelope）结构，功能强大但冗余复杂，多见于早期企业系统。REST ≠ 必须 HTTPS（D 错），SOAP 是更早期的标准（C 错）。

---

**7.** `pd.read_html(url)` 的主要局限是什么？

- A. 只能读取 JSON 格式的数据，无法解析 HTML
- B. 只能提取页面中的 `<table>` 标签内的数据，且对动态渲染的表格无效
- C. 每次调用只能读取第一个表格，无法获取页面上的多个表格
- D. 需要手动传入 BeautifulSoup 对象，不能直接传入 URL

> [!tip]- 答案
> **答案：B**
> 解析：`pd.read_html()` 的两大限制：①只识别 HTML `<table>` 标签，其他结构（`<div>` 模拟的表格）无效；②底层使用 `requests` 获取页面，JavaScript 动态渲染的内容不在其中，动态表格无效。它确实可以返回**多个**表格（返回 DataFrame 列表，用 `[0]`、`[1]` 索引），所以 C 错。

---

**8.** Web API 按访问权限分为三种类型。某公司将库存数据 API 仅开放给其签约零售商，不对公众或注册用户开放，这属于哪种类型？

- A. Public API
- B. Registration-required API
- C. Closed / B2B API
- D. Internal API（内部 API）

> [!tip]- 答案
> **答案：C**
> 解析：三种类型：**Public API** — 完全公开，无需认证（如部分政府开放数据）；**Registration-required API** — 需注册获取 API Key，但对所有人开放注册（如 OpenWeatherMap）；**Closed / B2B API** — 仅对特定合作伙伴/企业开放，不接受公众申请，通常用于 B2B 数据交换。题目场景"仅签约零售商"= Closed B2B API。

---

## 简答/代码阅读题

**9.** 阅读以下 HTML 片段，回答问题：

```html
<div id="content">
  <ul class="menu">
    <li class="item active"><a href="/home">Home</a></li>
    <li class="item"><a href="/about">About</a></li>
    <li class="item"><a href="/data">Data</a></li>
  </ul>
  <table class="results">
    <tr><th>City</th><th>Population</th></tr>
    <tr><td>Sydney</td><td>5312000</td></tr>
    <tr><td>Melbourne</td><td>5078000</td></tr>
  </table>
</div>
```

**(a)** CSS Selector `ul.menu li.item.active a` 会选中哪个元素？写出该元素的完整标签。

**(b)** CSS Selector `#content .results td` 会选中哪些元素？

**(c)** 若要用 XPath 选中 `href` 属性值包含 `"data"` 的 `<a>` 标签，应写什么 XPath 表达式？（CSS Selector 能否完成同样任务？）

> [!tip]- 答案
> **(a)** 选中：`<a href="/home">Home</a>`
> 解析：`ul.menu` 选 class 含 `menu` 的 `<ul>`；`li.item.active` 选同时具有 `item` 和 `active` 两个 class 的 `<li>`（即第一个 `<li>`）；`a` 选其中的 `<a>` 标签。结果为 `<a href="/home">Home</a>`。
>
> **(b)** 选中 `<table class="results">` 内所有 `<td>` 元素，共 4 个：
> - `<td>Sydney</td>`
> - `<td>5312000</td>`
> - `<td>Melbourne</td>`
> - `<td>5078000</td>`
>
> 解析：`#content` 选 `id="content"` 的 `<div>`；`.results` 选其后代中 class 含 `results` 的元素（即 `<table>`）；`td` 选该表格内所有 `<td>`。`<th>` 不被选中。
>
> **(c)** XPath：`//a[contains(@href, 'data')]`
> 选中：`<a href="/data">Data</a>`
>
> CSS Selector **无法**完成同样任务。CSS Selector 没有属性值模糊匹配（`contains`）的语法；虽然 `a[href*="data"]` 在完整 CSS 规范中存在，但 BeautifulSoup 的 `select()` **不支持** `[attr*=value]` 这类属性子串匹配选择器。这正是 XPath 相较于 CSS Selector 的优势之一。

---

**10.** 简述 Web Scraping 五步流程中 Reconnaissance 阶段的主要任务，并解释为何跳过该阶段会带来风险。（3-4 句）

> [!tip]- 答案
> Reconnaissance（侦查）阶段的主要任务：①确认目标网站的页面结构（静态 vs. 动态，数据在哪个标签/路径下）；②检查 `robots.txt` 了解哪些路径被禁止爬取；③阅读网站服务条款（ToS）确认是否允许数据采集。
>
> 跳过该阶段的风险：若直接开始爬取 `robots.txt` 中 `Disallow` 的路径，可能违反平台政策导致 IP 被封；若 ToS 明确禁止数据采集而忽视，可能面临法律追究；若未分析页面结构就写提取代码，动态页面可能导致 `requests` 拿不到目标数据，整个流程白费。

---

**11.** 以下是三种爬取工具的选型场景，请为每种场景选择最合适的工具（`requests+BeautifulSoup` / `Scrapy` / `Selenium`），并给出一句理由。

| 场景 | 最佳工具 | 理由 |
|------|----------|------|
| 抓取一个政府静态 HTML 页面中的数据表格，只需运行一次 | ? | ? |
| 需要登录后点击"加载更多"按钮，内容由 JS 动态注入页面 | ? | ? |
| 每周自动爬取某新闻网站 500 个页面并存入数据库 | ? | ? |

> [!tip]- 答案
> | 场景 | 最佳工具 | 理由 |
> |------|----------|------|
> | 静态页面，一次性 | `requests + BeautifulSoup` | 页面为静态 HTML，轻量工具足够，无需引入框架开销 |
> | 需登录 + JS 动态内容 | `Selenium` | 需要模拟浏览器操作（登录、点击），且内容由 JS 渲染，只有 Selenium 控制真实浏览器才能拿到最终 DOM |
> | 定期大规模多页爬取 | `Scrapy` | Scrapy 内置 Spider 跟链、并发调度、数据 Pipeline，适合持续化、规模化爬取任务 |
