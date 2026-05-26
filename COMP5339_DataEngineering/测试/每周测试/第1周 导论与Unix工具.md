# 第1周测试 — 导论与 Unix 工具

---

## 选择题

**1.** 以下哪种数据属于 Semi-structured（半结构化）数据？

- A. PostgreSQL 关系表中的一行记录
- B. 一段 MP3 音频文件
- C. 一个 JSON 文件
- D. 一张 JPEG 图片

> [!tip]- 答案
> **答案：C**
> 解析：Semi-structured 数据有一定的自描述结构（键值对、标签），但不遵循严格的 relational schema，字段可嵌套或缺失。JSON 和 XML 是典型代表。关系表是 Structured；MP3 和 JPEG 是 Unstructured。

---

**2.** 在 Data Engineering Lifecycle 中，"Storage"阶段的定位是？

- A. 仅出现在 Transformation 之后，用于保存最终结果
- B. 贯穿整个生命周期，从 Ingestion 到 Serving 各阶段都依赖它
- C. 等同于 Data Warehouse，专门服务于分析查询
- D. 只在 Generation 阶段由数据源系统负责

> [!tip]- 答案
> **答案：B**
> 解析：Reis & Housley 明确指出 Storage 是 underpinning（底座），贯穿从 Acquisition 到 Serving 的所有阶段，而非某个单独的步骤。选项 A 把它定位在末端，C 混淆了物理系统与阶段概念，D 指的是源系统存储。

---

**3.** Data Science Hierarchy of Needs 金字塔从底层到顶层的正确顺序是？

- A. Collect → Explore/Transform → Move/Store → Aggregate/Label → Learn → AI/Deep Learning
- B. Collect → Move/Store → Explore/Transform → Aggregate/Label → Learn → AI/Deep Learning
- C. Move/Store → Collect → Aggregate/Label → Explore/Transform → Learn → AI/Deep Learning
- D. Collect → Aggregate/Label → Move/Store → Explore/Transform → AI/Deep Learning → Learn

> [!tip]- 答案
> **答案：B**
> 解析：金字塔底层是最基础的数据工程工作：先 **Collect**（采集），然后 **Move/Store**（传输与存储），再 **Explore/Transform**（探索与清洗），然后 **Aggregate/Label**（聚合与标注），之后才是 **Learn**（ML 建模），最顶层是 **AI/Deep Learning**。数据工程师主要工作在底部三层。

---

**4.** 关于 Type A 与 Type B Data Engineer 的描述，哪项最准确？

- A. Type A 专注构建定制化的底层数据框架，Type B 使用托管云服务
- B. Type A 利用现成抽象工具管理数据管道，Type B 自研底层基础设施
- C. Type A 适合初创公司，Type B 只存在于大型科技公司
- D. Type A 与 Type B 的区别在于使用批处理还是流处理

> [!tip]- 答案
> **答案：B**
> 解析：Reis & Housley 定义：**Type A（Abstraction）** 使用现成工具（如 Airflow、dbt、Fivetran）管理数据管道，避免重复造轮子；**Type B（Build）** 在现有工具无法满足规模或需求时，自研底层系统。两种类型与公司规模无直接绑定关系，也与批处理/流处理无关。

---

**5.** 以下关于 Unbounded Data 的描述，哪项正确？

- A. Unbounded Data 本质上无法被处理，需等数据停止后才能分析
- B. Unbounded Data 是指数据大小超过单机内存的数据集
- C. Unbounded Data 是持续产生、没有固定终点的数据流，批处理系统通常需将其切分为有界窗口才能处理
- D. Unbounded Data 只适合用流处理系统处理，批处理系统完全无法处理

> [!tip]- 答案
> **答案：C**
> 解析：Unbounded（无界）数据没有固定的开始和结束点，例如实时日志流、传感器数据。批处理系统处理它的常见做法是划定时间窗口将其转化为 Bounded（有界）批次。选项 A 错误（可以处理）；B 混淆了数据大小与有界性；D 过于绝对，批处理通过窗口化仍可处理无界数据。

---

**6.** 一家公司通过订阅 Kafka topic 的方式实时接收用户行为事件，这属于哪种数据摄取（Ingestion）模式？

- A. Poll（轮询）
- B. Pull（拉取）
- C. Push（推送）
- D. Batch（批量）

> [!tip]- 答案
> **答案：C**
> 解析：**Push 模式**中，数据源主动将数据推送给接收方。Kafka 生产者将消息发布到 topic，消费者订阅后被动接收，数据由源端驱动——这是 Push 的典型形态。**Pull** 是接收方主动向源端请求数据（如调用 REST API）；**Poll** 是接收方周期性地定时查询源端是否有新数据（如爬虫定时抓取）。

---

**7.** 关于 Data Engineering 的定义，Reis & Housley（2022）最核心的表述是？

- A. 数据工程是构建机器学习模型并将其部署到生产环境的全过程
- B. 数据工程是将原始数据转化为高质量信息以供下游使用的系统与流程的开发与维护
- C. 数据工程等同于数据库管理，核心职责是保证数据存储的安全与可用
- D. 数据工程是数据科学的子集，负责数据的采集和存储环节

> [!tip]- 答案
> **答案：B**
> 解析：Reis & Housley 的定义核心是 **"raw data → high-quality information"**，强调的是系统与流程的开发和维护，服务于下游（分析师、数据科学家、业务决策）。数据工程不等同于 DBA（C），也不是数据科学的子集（D），更不包含 ML 模型训练和部署（A）。

---

**8.** 以下哪项属于 Data Engineering Lifecycle 的 Undercurrents（底层支撑），而非某个主要阶段？

- A. Transformation
- B. Orchestration
- C. Serving
- D. Acquisition

> [!tip]- 答案
> **答案：B**
> 解析：Lifecycle 的五个主要阶段是 Generation、Acquisition/Ingestion、Transformation、Serving（Storage 贯穿其中）。**Undercurrents** 是横跨所有阶段的基础能力，包括：Security、DataOps、Data Architecture、**Orchestration**、Software Engineering。Transformation、Serving、Acquisition 都是主要阶段。

---

## 简答题

**9.** 解释 Push、Pull、Poll 三种数据摄取模式的区别，各举一个实际场景。

> [!tip]- 答案
> - **Push（推送）**：数据源主动将数据发送给接收方，接收方被动等待。数据由源端驱动，延迟低。例：Kafka 生产者将用户点击事件实时推送到 topic，下游消费者订阅接收。
> - **Pull（拉取）**：接收方主动向数据源发起请求获取数据。例：数据管道定时调用第三方 REST API，获取最新的商品价格列表。
> - **Poll（轮询）**：接收方按固定时间间隔反复查询数据源，检查是否有新数据到达。例：爬虫每隔10分钟访问一次新闻网站，检测是否有新文章发布。
>
> **关键区别**：Push 由源端发起；Pull 由目标端按需发起（通常为一次性或事件驱动）；Poll 由目标端按时间周期发起（定时检查）。

---

**10.** 什么是 Bounded Data 与 Unbounded Data？为什么批处理系统处理 Unbounded Data 时需要将其转化为 Bounded？

> [!tip]- 答案
> - **Bounded Data（有界数据）**：数据集有明确的开始和结束点，大小有限，可以完整加载后处理。例：昨天的全量订单记录文件。
> - **Unbounded Data（无界数据）**：数据持续不断产生，没有固定终点。例：实时传感器数据流、用户行为日志流。
>
> **为何需要转化**：批处理系统（如 Hadoop MapReduce、Spark Batch）的设计前提是数据集是有限的——只有拿到完整数据才能执行全局排序、聚合等操作。对于无界数据，系统无法"等到数据全部到达"再处理，因此需要按时间窗口（如每小时/每天）将数据流切分成有界批次，才能套用批处理逻辑。流处理系统（如 Flink）则可以原生处理无界数据，无需预先转化。

---

**11.** 解释 Data Engineering Lifecycle 中各主要阶段的作用，并说明 Storage 为何被单独归为"贯穿全程"而非某个固定阶段。

> [!tip]- 答案
> **各主要阶段**：
> - **Generation（生成）**：数据在源系统（数据库、IoT 设备、应用日志）中产生，数据工程师通常不控制此阶段但需了解源数据特征。
> - **Acquisition/Ingestion（采集/摄取）**：将数据从源系统提取并传输到数据平台，包括 batch、stream、Push/Pull 等模式。
> - **Transformation（转换）**：对原始数据进行清洗、规范化、聚合、建模，使其符合下游需求。
> - **Serving（服务）**：将处理后的数据交付给最终用户或系统，包括分析仪表板、ML 训练数据集、API 接口等。
>
> **Storage 为何贯穿全程**：每个阶段都需要持久化数据——Ingestion 后需要 raw 存储（data lake），Transformation 过程中需要中间层存储（staging area），Serving 阶段需要查询优化的存储（data warehouse）。Storage 不是一个独立的时间节点，而是支撑所有阶段运转的基础设施层。
