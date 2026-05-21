# 第1周测试 — 导论与 Unix 工具

---

## 选择题

**1.** 以下哪种数据属于 Semi-structured（半结构化）数据？

- A. PostgreSQL 关系表中的一行记录
- B. 一段 MP3 音频文件
- C. 一个 JSON 文件
- D. 一张 JPEG 图片

<details><summary>答案</summary>

**答案：C**

解析：Semi-structured 数据有一定的自描述结构（键值对、标签），但不遵循严格的 relational schema，字段可嵌套或缺失。JSON 和 XML 是典型代表。关系表是 Structured；MP3 和 JPEG 是 Unstructured。

</details>

---

**2.** Unix 命令 `sort -u` 的效果等价于？

- A. `sort | head -1`
- B. `sort | uniq`
- C. `uniq | sort`
- D. `sort -r | uniq -c`

<details><summary>答案</summary>

**答案：B**

解析：`sort -u` 先排序再去重，与 `sort | uniq` 效果相同。注意 `uniq` 只去除相邻重复行，必须先 sort 才能去除全局重复，所以 C（先 uniq 再 sort）结果不同。

</details>

---

**3.** 以下 Unix 命令中，哪个用于按列提取文本字段？

- A. `grep`
- B. `sed`
- C. `wc`
- D. `cut`

<details><summary>答案</summary>

**答案：D**

解析：`cut -d',' -f2` 可按分隔符提取第2列。`grep` 用于模式匹配行过滤；`sed` 用于流式文本替换/编辑；`wc` 统计行数/字数/字节数。

</details>

---

**4.** 以下命令的输出是什么？

```bash
echo -e "apple\nbanana\napple\ncherry" | sort | uniq -c | sort -rn | head -1
```

- A. `apple`
- B. `2 apple`
- C. `1 cherry`
- D. `3 apple`

<details><summary>答案</summary>

**答案：B**

解析：流程：sort 排序 → uniq -c 统计每行出现次数 → sort -rn 按数字降序 → head -1 取第一行。"apple" 出现2次排名最高，输出为 `      2 apple`。

</details>

---

**5.** `grep -E "^[0-9]{3}-[0-9]{4}$" file.txt` 能匹配以下哪个字符串？

- A. `12-3456`
- B. `123-456`
- C. `123-4567`
- D. `1234-567`

<details><summary>答案</summary>

**答案：C**

解析：正则 `^[0-9]{3}-[0-9]{4}$` 表示：行首 + 3位数字 + 连字符 + 4位数字 + 行尾。只有 `123-4567`（3位 + `-` + 4位）满足。

</details>

---

**6.** 在 Data Engineering 生命周期中，正确的阶段顺序是？

- A. Transformation → Acquisition → Storage → Serving
- B. Acquisition → Storage → Transformation → Serving
- C. Storage → Acquisition → Serving → Transformation
- D. Acquisition → Transformation → Serving → Storage

<details><summary>答案</summary>

**答案：B**

解析：标准 Data Engineering 生命周期：**Acquisition/Ingestion**（获取原始数据）→ **Storage**（存储）→ **Transformation**（清洗转换）→ **Serving**（交付下游消费）。Storage 贯穿全程，但在逻辑顺序上位于获取之后。

</details>

---

**7.** 以下 `awk` 命令的作用是？

```bash
awk -F',' '$3 > 100 {print $1, $3}' data.csv
```

- A. 打印 CSV 所有行的第1和第3列
- B. 打印第3列值大于100的行的第1列和第3列
- C. 删除第3列小于等于100的行
- D. 统计第3列大于100的行数

<details><summary>答案</summary>

**答案：B**

解析：`-F','` 设定逗号为列分隔符；`$3 > 100` 是过滤条件；`{print $1, $3}` 是满足条件后执行的动作——打印第1和第3字段。

</details>

---

**8.** `wc -l file.txt` 输出 `42 file.txt`，说明？

- A. 文件有 42 个单词
- B. 文件有 42 个字符
- C. 文件有 42 行
- D. 文件大小为 42 字节

<details><summary>答案</summary>

**答案：C**

解析：`wc -l` 统计行数（line count）。`wc -w` 统计单词数，`wc -c` 统计字节数，`wc -m` 统计字符数。

</details>

---

## 简答题

**9.** 解释 Structured、Semi-structured、Unstructured 三种数据类型的区别，各举一个例子。

<details><summary>答案</summary>

- **Structured**：有严格预定义的 schema，存储在关系表中，每行每列类型固定。例：PostgreSQL 中的 `orders` 表。
- **Semi-structured**：有自描述结构（标签/键值对），但不强制固定 schema，字段可缺失或嵌套。例：JSON 文件、XML 文件。
- **Unstructured**：无内在数据模型，内容不可直接被数据库解析。例：图片（JPEG）、音频（MP3）、自由文本（邮件正文）。

**考试重点**：Semi-structured 是最易混淆的——它"有结构"但结构灵活，不是 schema-on-write 强制的。

</details>

---

**10.** 解释 Unix pipe（`|`）的作用，并写出一条命令：统计 `log.txt` 中包含 "ERROR" 的行数。

<details><summary>答案</summary>

**Pipe 的作用**：将前一个命令的标准输出（stdout）直接连接为后一个命令的标准输入（stdin），实现命令链式组合，无需写中间临时文件。

**命令**：
```bash
grep "ERROR" log.txt | wc -l
```

或直接：
```bash
grep -c "ERROR" log.txt
```

</details>

---

**11.** 以下 `sed` 命令的作用是什么？

```bash
sed 's/,/\t/g' data.csv > data.tsv
```

<details><summary>答案</summary>

将 `data.csv` 中每行的所有逗号（`,`）替换为制表符（`\t`），输出保存到 `data.tsv`。

- `s/,/\t/g`：substitute 替换命令；`g` flag 表示全局替换（每行所有匹配，而非只替换第一个）。
- `>` 将 stdout 重定向到新文件，原文件 `data.csv` 不变。

用途：将 CSV 格式转换为 TSV（Tab-Separated Values）格式。

</details>
