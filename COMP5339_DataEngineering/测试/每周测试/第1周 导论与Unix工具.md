# 第1周测试 — 导论与 Unix 工具

---

## 一、选择题

**1.** 下列哪种数据属于 Unbounded 数据？

- A. 从政府网站下载的 CSV 文件
- B. 数据库查询返回的结果集
- C. IoT 传感器持续产生的读数流
- D. 一次 API 调用返回的 JSON

**2.** Unix 命令 `wc -l data.csv` 的作用是？

- A. 统计文件的列数
- B. 统计文件的行数
- C. 统计文件的字节大小
- D. 统计文件的单词数

**3.** 以下命令的输出结果是什么？

```bash
cat data.csv | grep "Sydney" | wc -l
```

- A. data.csv 的总行数
- B. data.csv 中包含 "Sydney" 的行数
- C. "Sydney" 在文件中出现的总次数
- D. data.csv 的文件大小

**4.** 关于 Unix 管道（Pipe），说法正确的是？

- A. 管道需要将中间结果写入磁盘文件
- B. 管道将前一个命令的输出作为后一个命令的输入
- C. 管道只能连接两个命令
- D. 管道只适用于文本文件

---

## 二、简答题

**5.** 解释 Bounded 和 Unbounded 数据的区别，并各举一个例子。

**6.** 写出一个 Unix 命令，从 `students.csv` 中找出所有包含 "COMP" 的行，并只显示前 10 行。

**7.** `cut -d',' -f1,3 data.csv` 这条命令做了什么？`-d` 和 `-f` 参数分别代表什么？

---

## 三、应用题

**8.** 你有一个大型日志文件 `server.log`，需要：
1. 找出所有包含 "ERROR" 的行
2. 统计出共有多少条错误记录

写出完整的 Unix 命令（一行搞定）。

---

## 参考答案

1. **C**
2. **B**
3. **B**
4. **B**
5. Bounded 数据有固定大小和终点，如下载的 CSV 文件；Unbounded 数据持续产生、没有终点，如传感器数据流。处理 Unbounded 数据前需划定窗口将其转为 Bounded。
6. `grep "COMP" students.csv | head -10`
7. 按逗号（`,`）分隔符切分每行，只保留第1列和第3列。`-d` 指定分隔符（delimiter），`-f` 指定保留的列号（field）。
8. `grep "ERROR" server.log | wc -l`
