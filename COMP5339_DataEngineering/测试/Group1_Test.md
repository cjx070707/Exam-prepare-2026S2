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

<details>
<summary>Answer</summary>

**C** — IoT sensor readings are continuously generated with no fixed endpoint, making them unbounded. All other options produce a finite, fixed-size dataset at the time of retrieval.

</details>

---

**Q2.** Which Unix command counts the **number of lines** in a file?

- A. `cut -l data.csv`
- B. `wc -l data.csv`
- C. `grep -c data.csv`
- D. `sort -n data.csv`

<details>
<summary>Answer</summary>

**B** — `wc -l` counts lines. `-c` counts bytes, `-w` counts words. `grep -c` counts matching lines but requires a pattern argument.

</details>

---

**Q3.** A dataset contains many temperature records where the value is `99999`, which is physically impossible. What type of data quality issue is this?

- A. Missing
- B. Incorrect
- C. Default
- D. Inconsistent

<details>
<summary>Answer</summary>

**C** — A **Default** value is a placeholder (like `99999`, `0`, or `-1`) substituted when the real value is unavailable, rather than leaving the field null. **Incorrect** refers to genuinely wrong values caused by sensor faults or input errors. **Missing** means the field is null/blank.

</details>

---

**Q4.** What does the following Pandas code do?

```python
df['age'].fillna(0).astype(int)
```

- A. Drops all rows where `age` is NaN, then converts to integer
- B. Replaces NaN in `age` with 0, then converts the column to integer type
- C. Replaces 0s in `age` with NaN, then converts to integer
- D. Converts `age` to integer; raises an error if NaN is present

<details>
<summary>Answer</summary>

**B** — `fillna(0)` replaces NaN with 0 first (necessary because Python's `int` type cannot represent NaN), then `astype(int)` converts the whole column to integer. Without `fillna` first, `astype(int)` would raise a `ValueError`.

</details>

---

**Q5.** Which BeautifulSoup call returns **all** `<table>` elements with class `data`?

- A. `content.find('table', 'data')`
- B. `content.find_all('table', 'data')`
- C. `content.select('table#data')`
- D. `content.find(class_='data')`

<details>
<summary>Answer</summary>

**B** — `find_all` returns a list of all matching elements. `find` returns only the first match. Option C uses `#` which selects by **id**, not class. Option D finds any element with that class, not specifically `<table>`.

</details>

---

**Q6.** What does the CSS selector `table.results` match?

- A. A `<table>` with id `results`
- B. Any element with class `results`
- C. A `<table>` with class `results`
- D. A `<table>` containing a child element named `results`

<details>
<summary>Answer</summary>

**C** — `tag.class` syntax selects elements of that tag type with that class. `#results` would select by id. `.results` alone (without the tag) would match any element with that class.

</details>

---

**Q7.** After calling `requests.get()`, a `response.status_code` of `404` means:

- A. Internal server error
- B. Request succeeded
- C. Resource not found
- D. Authentication required

<details>
<summary>Answer</summary>

**C** — HTTP 404 = Not Found. 200 = OK (success). 500 = Internal Server Error. 401 = Unauthorized (authentication required).

</details>

---

**Q8.** Compared to scraping HTML pages directly, what is the primary advantage of using a Web API?

- A. APIs do not require a network connection
- B. APIs return structured data (JSON/XML) that is stable and not affected by page redesigns
- C. APIs are faster because they bypass the HTTP protocol
- D. APIs require no parsing whatsoever

<details>
<summary>Answer</summary>

**B** — APIs expose a stable, structured interface (usually JSON). HTML scraping breaks whenever the website's layout changes. APIs still use HTTP and still require parsing, but the structure is far more predictable.

</details>

---

**Q9.** Which tool is best suited for scraping a website that **requires JavaScript to render** its content?

- A. `requests` + `BeautifulSoup`
- B. `Scrapy`
- C. `Selenium`
- D. `pd.read_html()`

<details>
<summary>Answer</summary>

**C** — Selenium drives a real browser that executes JavaScript. `requests` fetches only the raw HTML; `BeautifulSoup` and `Scrapy` also do not execute JavaScript. `pd.read_html()` only parses static HTML tables.

</details>

---

**Q10.** How many query parameters does the following URL contain?

```
https://api.example.com/data?format=json&limit=100
```

- A. 1
- B. 2
- C. 3
- D. Cannot be determined

<details>
<summary>Answer</summary>

**B** — `format=json` and `limit=100` are two separate query parameters, separated by `&`. The `?` marks the start of the query string.

</details>

---

## Section B — Short Answer (8 marks each, 32 marks total)

**Q11.** Explain the difference between **Bounded** and **Unbounded** data. Give one example of each. What transformation must be applied to unbounded data before it can be processed, and why? (8 marks)

<details>
<summary>Answer</summary>

- **Bounded data**: A dataset with a fixed, finite size. The full dataset is available at the time of processing. *Example*: a CSV file downloaded from a government portal; the result of a SQL query.
- **Unbounded data**: A continuous, never-ending stream of data with no defined endpoint. *Example*: real-time IoT sensor readings; a live social media event stream.
- **Required transformation**: Unbounded data must be divided into **windows** or **batches** before processing. This is necessary because any aggregation (sum, count, average) requires a defined boundary — you cannot compute an average over an infinite sequence. A window imposes a finite scope (e.g., "last 5 minutes" or "1,000 records at a time") so the computation can complete and produce a result.

</details>

---

**Q12.** A data engineer receives a hospital patient record CSV and finds the following issues:
- Several rows have a blank `age` field
- The `gender` column contains `M`, `Male`, and `Male` entries
- Some rows have a `weight` value of `0`, which is medically impossible

Identify the data quality problem type for each issue and describe how to handle it. (8 marks)

<details>
<summary>Answer</summary>

| Issue | Problem Type | Handling |
|-------|-------------|---------|
| Blank `age` field | **Missing** — the value was never recorded or was lost in transmission | Use `fillna()` with a suitable imputation (e.g., median age) or `dropna()` to remove those rows if the field is critical |
| `M` / `Male` / `男` in `gender` | **Inconsistent** — the same concept represented in multiple formats | Standardise with `.replace({'Male': 'M', '男': 'M'})` to unify all entries to a single encoding |
| `weight` = 0 | **Default** — 0 is a placeholder substituted when the true value was unavailable, not a real measurement | Replace 0 with `NaN` (e.g., `df['weight'].replace(0, np.nan)`), then treat as missing |

</details>

---

**Q13.** Compare `requests` + `BeautifulSoup` with `Scrapy` as web scraping tools. When should you choose `Scrapy` over `requests`+`BeautifulSoup`? (8 marks)

<details>
<summary>Answer</summary>

| Dimension | `requests` + `BeautifulSoup` | `Scrapy` |
|-----------|------------------------------|----------|
| Setup complexity | Low — minimal boilerplate | Higher — requires project structure and Spider class |
| Best for | Single pages or a small, known list of URLs | Multi-page crawls that follow links automatically |
| Concurrency | Single-threaded by default | Built-in asynchronous request engine |
| Features | Manual everything | Built-in: deduplication, rate limiting, pipelines, middleware |
| Use case | Quick one-off data extraction | Systematic, recurring, or large-scale crawls |

**Choose Scrapy when**:
- You need to follow pagination links or crawl an entire site structure
- You need to handle retries, rate limiting, or robots.txt compliance automatically
- You want to export data to multiple targets (database, JSON, CSV) through pipelines
- The crawl needs to run repeatedly on a schedule

</details>

---

**Q14.** A data engineer has two choices when querying a database from Python: **"push compute into the DBMS"** or **"pull all data into Python"**. Explain the approach for each, and describe the appropriate use case and limitation of each. (8 marks)

<details>
<summary>Answer</summary>

**Push compute into the DBMS**
- *Approach*: Write SQL that performs filtering, aggregation, and joining inside the database. Python only receives the final, small result set.
- *Use case*: Large tables where only a fraction of data is needed; aggregations that benefit from indexes; queries the database engine can optimise.
- *Limitation*: Complex statistical analysis or machine learning workflows are difficult to express in SQL alone.

**Pull all data into Python**
- *Approach*: Fetch the entire table (or large chunk) into a Pandas DataFrame and perform all processing in Python.
- *Use case*: Exploratory analysis where you need flexible, ad-hoc transformations; small-to-medium datasets that fit in memory.
- *Limitation*: The full dataset must fit in memory (risk of OOM errors on large tables); high network transfer cost; loses database query optimisation.

**Rule of thumb**: prefer pushing compute to the DBMS for data reduction, and pull only the filtered/aggregated result for further Python processing.

</details>

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

<details>
<summary>Answer</summary>

The **second** table on the page. Python list indexing starts at 0, so index `[1]` is the second element.

</details>

**(b)** What does `pd.read_html(str(table))[0]` do? Why is `[0]` needed? (2 marks)

<details>
<summary>Answer</summary>

`pd.read_html()` parses all HTML `<table>` elements found in the given string and returns a **list** of DataFrames. Since `str(table)` contains exactly one table, the list has one element. `[0]` retrieves that first (and only) DataFrame from the list.

</details>

**(c)** What is the difference between `dropna(subset=['Score'])` and `dropna()`? (2 marks)

<details>
<summary>Answer</summary>

- `dropna(subset=['Score'])` drops only rows where the **`Score` column specifically** is NaN. Rows that have NaN in other columns are kept.
- `dropna()` drops any row that has **at least one NaN in any column**, which can remove many more rows than intended and lose valid data.

Using `subset` is safer when only one column is required to be non-null.

</details>

**(d)** Describe what the last three lines do and summarise the overall goal of this script in one sentence. (3 marks)

<details>
<summary>Answer</summary>

The last three lines:
1. `df[df['Score'] > 80]` — filters to keep only rows where Score exceeds 80
2. `.sort_values('Score', ascending=False)` — sorts those rows from highest to lowest score
3. `print(df_top.head(10))` — prints the top 10 rows

**Overall goal**: Scrape a rankings table from a webpage, clean the data, and display the top 10 highest-scoring entries (those with a score above 80).

</details>
