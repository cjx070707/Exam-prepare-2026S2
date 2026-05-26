# Week 4 Quiz — Web Scraping & APIs

---

## Multiple Choice Questions

**1.** What is the correct order of the five-step Web Scraping pipeline?

- A. Extraction → Retrieval → Reconnaissance → Cleaning → Storage
- B. Reconnaissance → Retrieval → Extraction → Cleaning → Storage
- C. Retrieval → Reconnaissance → Extraction → Storage → Cleaning
- D. Reconnaissance → Extraction → Retrieval → Cleaning → Storage

> [!tip]- Answer
> **答案：B**
> 解析：标准五步流程：**Reconnaissance**（侦查：确认目标页面结构、检查 robots.txt 和 ToS）→ **Retrieval**（获取：发送 HTTP 请求下载页面）→ **Extraction**（提取：从 HTML 中解析目标数据）→ **Cleaning**（清洗：处理缺失、格式不一致等）→ **Storage**（存储：写入文件/数据库）。顺序考点常出，Reconnaissance 必须在最前。

---

**2.** During the Reconnaissance stage, why is it essential to check `robots.txt` and the website's Terms of Service (ToS)?

- A. Because `robots.txt` blocks all scrapers, so checking it lets you bypass the restriction
- B. Violating `robots.txt` or ToS may result in IP bans or legal consequences, so compliance must be confirmed before scraping
- C. `robots.txt` lists all page URLs on the site, which can be used to build a scraping target list
- D. ToS only applies to commercial use, so academic use can safely ignore it

> [!tip]- Answer
> **答案：B**
> 解析：`robots.txt` 是网站声明哪些路径允许/禁止爬虫访问的约定文件（如 `Disallow: /private/`）。忽略它不一定在技术上被阻止，但可能违反平台政策，导致 IP 封禁甚至法律追究。ToS 同理，即便是学术用途也不自动豁免。Reconnaissance 阶段的核心任务之一就是合规性确认。

---

**3.** Which of the following statements about static vs. dynamic pages is most accurate?

- A. Static pages have content that never changes day-to-day; dynamic pages change every second
- B. Dynamic pages are rendered by JavaScript in the browser; the HTML returned by `requests.get()` does not contain the final data
- C. `pd.read_html()` can parse tables in dynamic pages because it automatically executes JavaScript
- D. Selenium and `requests` have the same capability for handling dynamic pages

> [!tip]- Answer
> **答案：B**
> 解析：动态页面的数据由 JavaScript 在客户端浏览器执行后才被注入 DOM（如 React/Vue 渲染的内容）。`requests.get()` 只下载服务器返回的原始 HTML，JavaScript 尚未执行，因此目标数据缺失。`pd.read_html()` 底层调用 `requests`，同样无法处理动态内容（C 错）。Selenium 控制真实浏览器，JS 执行完毕后再抓取 DOM，是处理动态页面的标准方案（D 错）。

---

**4.** What does HTTP status code `429` most likely mean, and what does it imply in a web scraping context?

- A. Internal server error, unrelated to scraping activity
- B. Resource not found; the target page has been deleted
- C. Too Many Requests — the server is rate-limiting or blocking the scraper
- D. Authentication failure; a valid API Key must be provided

> [!tip]- Answer
> **答案：C**
> 解析：常见状态码速记：`200` 成功；`403` Forbidden（权限不足）；`404` Not Found（资源不存在）；`429` Too Many Requests（请求速率超限，反爬机制常用）；`401` Unauthorized（未认证）。爬虫遇到 `429` 应降低请求频率或加入随机延迟。

---

**5.** Comparing four content extraction methods, which statement is most accurate?

- A. XPath and CSS Selector are functionally identical and fully interchangeable in all scenarios
- B. Text Patterns (regular expressions) are the most recommended extraction method due to their speed
- C. XPath supports upward parent-node traversal and predicate-based filtering; CSS Selector cannot select parent nodes
- D. DOM Navigation (e.g. `.parent`, `.children`) is better suited for complex page structures than CSS Selector

> [!tip]- Answer
> **答案：C**
> 解析：四种方式对比：**Text Patterns**（正则）灵活但脆弱，HTML 稍变则失效；**DOM Navigation** 逐级遍历，代码繁琐；**CSS Selector** 简洁、广泛支持，但只能向下选择后代，**无法选中父节点**；**XPath** 功能最强，支持 `//div[contains(@class,"row")]` 等谓语过滤，也支持 `..` 逆向查找父节点，适合复杂结构提取。考试高频考点：XPath 能做而 CSS Selector 做不到的事。

---

**6.** Which of the following best describes the difference between RESTful APIs and SOAP?

- A. REST uses XML message envelopes and SOAP uses JSON; both are stateless
- B. REST uses HTTP verbs (GET/POST/etc.) and typically returns JSON; it is stateless. SOAP uses an XML message format and has a more complex protocol structure
- C. SOAP is more modern than REST and is the current mainstream standard for Web APIs
- D. Both REST and SOAP require HTTPS to function correctly

> [!tip]- Answer
> **答案：B**
> 解析：**REST**（Representational State Transfer）：无状态、利用 HTTP 动词语义（GET=读、POST=创建、PUT=更新、DELETE=删除）、通常返回 JSON，简洁易用，是当前 Web API 主流（课程中 web service = REST）。**SOAP**：基于 XML 的消息协议，有严格的信封（Envelope）结构，功能强大但冗余复杂，多见于早期企业系统。REST ≠ 必须 HTTPS（D 错），SOAP 是更早期的标准（C 错）。

---

**7.** What is the main limitation of `pd.read_html(url)`?

- A. It can only read JSON-formatted data and cannot parse HTML
- B. It can only extract data within `<table>` tags, and it does not work on dynamically rendered tables
- C. Each call retrieves only the first table on the page; multiple tables cannot be accessed
- D. It requires a BeautifulSoup object as input and cannot accept a URL directly

> [!tip]- Answer
> **答案：B**
> 解析：`pd.read_html()` 的两大限制：①只识别 HTML `<table>` 标签，其他结构（`<div>` 模拟的表格）无效；②底层使用 `requests` 获取页面，JavaScript 动态渲染的内容不在其中，动态表格无效。它确实可以返回**多个**表格（返回 DataFrame 列表，用 `[0]`、`[1]` 索引），所以 C 错。

---

**8.** Web APIs can be classified into three access types. A company exposes its inventory data API exclusively to its contracted retailers, with no access for the general public or registered users. Which type does this belong to?

- A. Public API
- B. Registration-required API
- C. Closed / B2B API
- D. Internal API

> [!tip]- Answer
> **答案：C**
> 解析：三种类型：**Public API** — 完全公开，无需认证（如部分政府开放数据）；**Registration-required API** — 需注册获取 API Key，但对所有人开放注册（如 OpenWeatherMap）；**Closed / B2B API** — 仅对特定合作伙伴/企业开放，不接受公众申请，通常用于 B2B 数据交换。题目场景"仅签约零售商"= Closed B2B API。

---

## Short Answer / Code Reading Questions

**9.** Read the following HTML fragment and answer the questions:

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

**(a)** What element does the CSS Selector `ul.menu li.item.active a` select? Write out the full tag.

**(b)** What elements does the CSS Selector `#content .results td` select?

**(c)** Write an XPath expression to select the `<a>` tag whose `href` attribute contains the string `"data"`. Can a CSS Selector accomplish the same task?

> [!tip]- Answer
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

**10.** Briefly describe the main tasks of the Reconnaissance stage in the five-step Web Scraping pipeline, and explain the risks of skipping it. (3–4 sentences)

> [!tip]- Answer
> Reconnaissance（侦查）阶段的主要任务：①确认目标网站的页面结构（静态 vs. 动态，数据在哪个标签/路径下）；②检查 `robots.txt` 了解哪些路径被禁止爬取；③阅读网站服务条款（ToS）确认是否允许数据采集。
>
> 跳过该阶段的风险：若直接开始爬取 `robots.txt` 中 `Disallow` 的路径，可能违反平台政策导致 IP 被封；若 ToS 明确禁止数据采集而忽视，可能面临法律追究；若未分析页面结构就写提取代码，动态页面可能导致 `requests` 拿不到目标数据，整个流程白费。

---

**11.** For each of the three scraping scenarios below, choose the most appropriate tool (`requests + BeautifulSoup` / `Scrapy` / `Selenium`) and give a one-sentence reason.

| Scenario | Best Tool | Reason |
|----------|-----------|--------|
| Scrape a government static HTML page for a data table — one-time run only | ? | ? |
| Must log in, then click a "Load More" button; content is dynamically injected by JS | ? | ? |
| Automatically scrape 500 pages from a news site every week and store results in a database | ? | ? |

> [!tip]- Answer
> | Scenario | Best Tool | Reason |
> |----------|-----------|--------|
> | Static page, one-time | `requests + BeautifulSoup` | 页面为静态 HTML，轻量工具足够，无需引入框架开销 |
> | Login required + JS dynamic content | `Selenium` | 需要模拟浏览器操作（登录、点击），且内容由 JS 渲染，只有 Selenium 控制真实浏览器才能拿到最终 DOM |
> | Scheduled large-scale multi-page scraping | `Scrapy` | Scrapy 内置 Spider 跟链、并发调度、数据 Pipeline，适合持续化、规模化爬取任务 |
