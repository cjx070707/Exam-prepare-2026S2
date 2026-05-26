# Week 1 Test — Introduction & Unix Tools

---

## Multiple Choice

**1.** Which of the following is an example of Semi-structured data?

- A. A row in a PostgreSQL relational table
- B. An MP3 audio file
- C. A JSON file
- D. A JPEG image

> [!tip]- Answer
> **答案：C**
> Semi-structured 数据具有一定的自描述结构（键值对、标签），但不遵循严格的 Relational Schema，字段可嵌套或缺失。JSON 和 XML 是典型代表。关系表是 Structured；MP3 和 JPEG 是 Unstructured。

---

**2.** In the Data Engineering Lifecycle, how is the "Storage" stage best characterized?

- A. It only appears after Transformation to store final results
- B. It underpins the entire lifecycle, from Ingestion through Serving
- C. It is equivalent to a Data Warehouse, dedicated to analytical queries
- D. It only exists in the Generation stage, managed by source systems

> [!tip]- Answer
> **答案：B**
> Reis & Housley 明确指出 Storage 是整个生命周期的 Underpinning（底座），贯穿从 Acquisition 到 Serving 的所有阶段，而非某个单独的步骤。选项 A 把它定位在末端；C 混淆了物理系统与阶段概念；D 指的是源系统存储。

---

**3.** What is the correct order of the Data Science Hierarchy of Needs pyramid, from bottom to top?

- A. Collect → Explore/Transform → Move/Store → Aggregate/Label → Learn → AI/Deep Learning
- B. Collect → Move/Store → Explore/Transform → Aggregate/Label → Learn → AI/Deep Learning
- C. Move/Store → Collect → Aggregate/Label → Explore/Transform → Learn → AI/Deep Learning
- D. Collect → Aggregate/Label → Move/Store → Explore/Transform → AI/Deep Learning → Learn

> [!tip]- Answer
> **答案：B**
> 金字塔底层是最基础的数据工程工作：先 **Collect**（采集），然后 **Move/Store**（传输与存储），再 **Explore/Transform**（探索与清洗），然后 **Aggregate/Label**（聚合与标注），之后才是 **Learn**（ML 建模），最顶层是 **AI/Deep Learning**。数据工程师主要工作在底部三层。

---

**4.** Which statement best describes the difference between a Type A and Type B Data Engineer?

- A. Type A builds custom low-level data frameworks; Type B uses managed cloud services
- B. Type A manages data pipelines using existing abstraction tools; Type B builds custom low-level infrastructure
- C. Type A suits startups; Type B only exists at large tech companies
- D. The distinction between Type A and Type B is whether they use batch or stream processing

> [!tip]- Answer
> **答案：B**
> Reis & Housley 定义：**Type A（Abstraction）** 使用现成工具（如 Airflow、dbt、Fivetran）管理数据管道，避免重复造轮子；**Type B（Build）** 在现有工具无法满足规模或需求时，自研底层系统。两种类型与公司规模无直接绑定关系，也与 Batch/Stream 无关。

---

**5.** Which of the following statements about Unbounded Data is correct?

- A. Unbounded Data fundamentally cannot be processed and must wait until the data stops
- B. Unbounded Data refers to datasets whose size exceeds single-machine memory
- C. Unbounded Data is a continuously generated stream with no fixed endpoint; batch systems typically slice it into bounded windows for processing
- D. Unbounded Data can only be handled by stream processing systems; batch systems cannot process it at all

> [!tip]- Answer
> **答案：C**
> Unbounded（无界）数据没有固定的开始和结束点，例如实时日志流、传感器数据。Batch 处理系统处理它的常见做法是划定时间窗口将其转化为 Bounded（有界）批次。选项 A 错误（可以处理）；B 混淆了数据大小与有界性；D 过于绝对，Batch 通过窗口化仍可处理无界数据。

---

**6.** A company subscribes to a Kafka topic to receive user behaviour events in real time. Which data ingestion pattern does this represent?

- A. Poll
- B. Pull
- C. Push
- D. Batch

> [!tip]- Answer
> **答案：C**
> **Push 模式**中，数据源主动将数据推送给接收方。Kafka 生产者将消息发布到 Topic，消费者订阅后被动接收，数据由源端驱动——这是 Push 的典型形态。**Pull** 是接收方主动向源端请求数据（如调用 REST API）；**Poll** 是接收方周期性地定时查询源端是否有新数据（如爬虫定时抓取）。

---

**7.** According to Reis & Housley (2022), what is the most essential definition of Data Engineering?

- A. Data Engineering is the end-to-end process of building machine learning models and deploying them to production
- B. Data Engineering is the development and maintenance of systems and processes that transform raw data into high-quality information for downstream use
- C. Data Engineering is equivalent to database administration, with a core responsibility of ensuring data storage security and availability
- D. Data Engineering is a subset of data science, responsible for data collection and storage

> [!tip]- Answer
> **答案：B**
> Reis & Housley 的定义核心是 **"raw data → high-quality information"**，强调系统与流程的开发和维护，服务于下游（分析师、数据科学家、业务决策）。数据工程不等同于 DBA（C），也不是数据科学的子集（D），更不包含 ML 模型训练和部署（A）。

---

**8.** Which of the following belongs to the Undercurrents of the Data Engineering Lifecycle, rather than a primary stage?

- A. Transformation
- B. Orchestration
- C. Serving
- D. Acquisition

> [!tip]- Answer
> **答案：B**
> Lifecycle 的五个主要阶段是 Generation、Acquisition/Ingestion、Transformation、Serving（Storage 贯穿其中）。**Undercurrents** 是横跨所有阶段的基础能力，包括：Security、DataOps、Data Architecture、**Orchestration**、Software Engineering。Transformation、Serving、Acquisition 都是主要阶段。

---

## Short Answer

**9.** Explain the difference between the Push, Pull, and Poll data ingestion patterns. Give one real-world example for each.

> [!tip]- Answer
> - **Push（推送）**：数据源主动将数据发送给接收方，接收方被动等待。数据由源端驱动，延迟低。例：Kafka 生产者将用户点击事件实时推送到 Topic，下游消费者订阅接收。
> - **Pull（拉取）**：接收方主动向数据源发起请求获取数据。例：数据管道定时调用第三方 REST API，获取最新的商品价格列表。
> - **Poll（轮询）**：接收方按固定时间间隔反复查询数据源，检查是否有新数据到达。例：爬虫每隔10分钟访问一次新闻网站，检测是否有新文章发布。
>
> **关键区别**：Push 由源端发起；Pull 由目标端按需发起（通常为一次性或事件驱动）；Poll 由目标端按时间周期发起（定时检查）。

---

**10.** What are Bounded Data and Unbounded Data? Why must batch processing systems convert Unbounded Data into Bounded form before processing?

> [!tip]- Answer
> - **Bounded Data（有界数据）**：数据集有明确的开始和结束点，大小有限，可以完整加载后处理。例：昨天的全量订单记录文件。
> - **Unbounded Data（无界数据）**：数据持续不断产生，没有固定终点。例：实时传感器数据流、用户行为日志流。
>
> **为何需要转化**：Batch 处理系统（如 Hadoop MapReduce、Spark Batch）的设计前提是数据集是有限的——只有拿到完整数据才能执行全局排序、聚合等操作。对于无界数据，系统无法"等到数据全部到达"再处理，因此需要按时间窗口（如每小时/每天）将数据流切分成有界批次，才能套用 Batch 处理逻辑。流处理系统（如 Flink）则可以原生处理无界数据，无需预先转化。

---

**11.** Describe the role of each primary stage in the Data Engineering Lifecycle, and explain why Storage is classified as "underpinning the entire lifecycle" rather than a fixed stage.

> [!tip]- Answer
> **各主要阶段**：
> - **Generation（生成）**：数据在源系统（数据库、IoT 设备、应用日志）中产生，数据工程师通常不控制此阶段但需了解源数据特征。
> - **Acquisition/Ingestion（采集/摄取）**：将数据从源系统提取并传输到数据平台，包括 Batch、Stream、Push/Pull 等模式。
> - **Transformation（转换）**：对原始数据进行清洗、规范化、聚合、建模，使其符合下游需求。
> - **Serving（服务）**：将处理后的数据交付给最终用户或系统，包括分析仪表板、ML 训练数据集、API 接口等。
>
> **Storage 为何贯穿全程**：每个阶段都需要持久化数据——Ingestion 后需要 Raw 存储（Data Lake），Transformation 过程中需要中间层存储（Staging Area），Serving 阶段需要查询优化的存储（Data Warehouse）。Storage 不是一个独立的时间节点，而是支撑所有阶段运转的基础设施层。
