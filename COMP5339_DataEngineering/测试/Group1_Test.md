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
> **C** — IoT sensor readings are continuously generated with no fixed endpoint, making them unbounded. All other options produce a finite, fixed-size dataset at the time of retrieval.

---

**Q2.** Which Unix command counts the **number of lines** in a file?

- A. `cut -l data.csv`
- B. `wc -l data.csv`
- C. `grep -c data.csv`
- D. `sort -n data.csv`

> [!note]- Answer
> **B** — `wc -l` counts lines. `-c` counts bytes, `-w` counts words. `grep -c` counts matching lines but requires a pattern argument.

---

**Q3.** A dataset contains temperature records where the value is `99999`, which is physically impossible. What type of data quality issue is this?

- A. Missing
- B. Incorrect
- C. Default
- D. Inconsistent

> [!note]- Answer
> **C** — A **Default** value is a placeholder (like `99999`, `0`, or `-1`) substituted when the real value is unavailable, rather than leaving the field null. **Incorrect** refers to genuinely wrong values caused by sensor faults or input errors. **Missing** means the field is null/blank.

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
> **B** — `fillna(0)` replaces NaN with 0 first (necessary because Python's `int` type cannot represent NaN), then `astype(int)` converts the whole column to integer. Without `fillna` first, `astype(int)` would raise a `ValueError`.

---

**Q5.** Which BeautifulSoup call returns **all** `<table>` elements with class `data`?

- A. `content.find('table', 'data')`
- B. `content.find_all('table', 'data')`
- C. `content.select('table#data')`
- D. `content.find(class_='data')`

> [!note]- Answer
> **B** — `find_all` returns a list of all matching elements. `find` returns only the first match. Option C uses `#` which selects by **id**, not class. Option D finds any element with that class, not specifically `<table>`.

---

**Q6.** What does the CSS selector `table.results` match?

- A. A `<table>` with id `results`
- B. Any element with class `results`
- C. A `<table>` with class `results`
- D. A `<table>` containing a child element named `results`

> [!note]- Answer
> **C** — `tag.class` syntax selects elements of that tag type with that class. `#results` would select by id. `.results` alone (without the tag) would match any element with that class.

---

**Q7.** After calling `requests.get()`, a `response.status_code` of `404` means:

- A. Internal server error
- B. Request succeeded
- C. Resource not found
- D. Authentication required

> [!note]- Answer
> **C** — HTTP 404 = Not Found. 200 = OK (success). 500 = Internal Server Error. 401 = Unauthorized.

---

**Q8.** Compared to scraping HTML pages directly, what is the primary advantage of using a Web API?

- A. APIs do not require a network connection
- B. APIs return structured data (JSON/XML) that is stable and not affected by page redesigns
- C. APIs are faster because they bypass the HTTP protocol
- D. APIs require no parsing whatsoever

> [!note]- Answer
> **B** — APIs expose a stable, structured interface (usually JSON). HTML scraping breaks whenever the website's layout changes. APIs still use HTTP and still require parsing, but the structure is far more predictable.

---

**Q9.** Which tool is best suited for scraping a website that **requires JavaScript to render** its content?

- A. `requests` + `BeautifulSoup`
- B. `Scrapy`
- C. `Selenium`
- D. `pd.read_html()`

> [!note]- Answer
> **C** — Selenium drives a real browser that executes JavaScript. `requests` fetches only the raw HTML. `BeautifulSoup` and `Scrapy` also do not execute JavaScript. `pd.read_html()` only parses static HTML tables.

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
> **B** — `format=json` and `limit=100` are two separate query parameters, separated by `&`. The `?` marks the start of the query string.

---

## Section B — Short Answer (8 marks each, 32 marks total)

**Q11.** Explain the difference between **Bounded** and **Unbounded** data. Give one example of each. What transformation must be applied to unbounded data before it can be processed, and why? (8 marks)

> [!note]- Answer
> - **Bounded data**: A dataset with a fixed, finite size. The full dataset is available at the time of processing. *Example*: a CSV file downloaded from a government portal; the result of a SQL query.
> - **Unbounded data**: A continuous, never-ending stream of data with no defined endpoint. *Example*: real-time IoT sensor readings; a live social media event stream.
> - **Required transformation**: Unbounded data must be divided into **windows** or **batches** before processing. This is necessary because any aggregation (sum, count, average) requires a defined boundary — you cannot compute an average over an infinite sequence. A window imposes a finite scope (e.g., "last 5 minutes") so the computation can complete and produce a result.

---

**Q12.** A data engineer receives a hospital patient record CSV and finds the following issues:
- Several rows have a blank `age` field
- The `gender` column contains `M`, `Male`, and `男` entries
- Some rows have a `weight` value of `0`, which is medically impossible

Identify the data quality problem type for each issue and describe how to handle it. (8 marks)

> [!note]- Answer
> | Issue | Problem Type | Handling |
> |-------|-------------|---------|
> | Blank `age` field | **Missing** — value never recorded or lost | `fillna()` with median age, or `dropna()` if the field is critical |
> | `M` / `Male` / `男` in gender | **Inconsistent** — same concept in multiple formats | Standardise with `.replace({'Male': 'M', '男': 'M'})` |
> | `weight` = 0 | **Default** — 0 is a placeholder, not a real measurement | Replace 0 with `NaN` via `.replace(0, np.nan)`, then treat as missing |

---

**Q13.** Compare `requests` + `BeautifulSoup` with `Scrapy` as web scraping tools. When should you choose `Scrapy`? (8 marks)

> [!note]- Answer
> | Dimension | `requests` + `BeautifulSoup` | `Scrapy` |
> |-----------|------------------------------|----------|
> | Setup | Low — minimal boilerplate | Higher — requires Spider class and project structure |
> | Best for | Single pages or a small, known list of URLs | Multi-page crawls that follow links automatically |
> | Concurrency | Single-threaded by default | Built-in async request engine |
> | Features | Manual everything | Built-in: deduplication, rate limiting, pipelines |
> 
> **Choose Scrapy when**: you need to follow pagination links, crawl an entire site structure, handle retries and rate limiting automatically, or run the crawl on a recurring schedule.

---

**Q14.** A data engineer has two choices: **"push compute into the DBMS"** or **"pull all data into Python"**. Explain the approach, use case, and limitation of each. (8 marks)

> [!note]- Answer
> **Push compute into the DBMS**
> - *Approach*: Write SQL that performs filtering, aggregation, and joining inside the database. Python only receives the final, small result set.
> - *Use case*: Large tables where only a fraction of data is needed; aggregations that benefit from indexes.
> - *Limitation*: Complex statistical analysis or ML workflows are difficult to express in SQL alone.
> 
> **Pull all data into Python**
> - *Approach*: Fetch the entire table into a Pandas DataFrame and perform all processing in Python.
> - *Use case*: Exploratory analysis needing flexible transformations; small-to-medium datasets that fit in memory.
> - *Limitation*: The full dataset must fit in memory (OOM risk); high network transfer cost; loses database query optimisation.

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
> The **second** table on the page. Python list indexing starts at 0, so index `[1]` is the second element.

**(b)** What does `pd.read_html(str(table))[0]` do? Why is `[0]` needed? (2 marks)

> [!note]- Answer
> `pd.read_html()` parses all HTML `<table>` elements in the given string and returns a **list** of DataFrames. Since `str(table)` contains exactly one table, the list has one element. `[0]` retrieves that single DataFrame from the list.

**(c)** What is the difference between `dropna(subset=['Score'])` and `dropna()`? (2 marks)

> [!note]- Answer
> - `dropna(subset=['Score'])` drops only rows where the **`Score` column specifically** is NaN. Rows with NaN in other columns are kept.
> - `dropna()` drops any row that has **at least one NaN in any column**, which can remove far more rows than intended.

**(d)** Describe what the last three lines do and summarise the overall goal of this script in one sentence. (3 marks)

> [!note]- Answer
> The last three lines: filter to rows where Score > 80, sort by Score descending, then print the top 10.
> 
> **Overall goal**: Scrape a rankings table from a webpage, clean the data, and display the top 10 highest-scoring entries.
