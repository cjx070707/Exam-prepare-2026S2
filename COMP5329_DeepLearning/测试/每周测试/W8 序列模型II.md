# W8 — Sequence Modeling II
**考点来源：复习笔记/第三组 序列数据.md（W8 部分）**

---

## Multiple Choice Questions

---

**Question 1.** *(BERT vs GPT ★★★)* A startup builds two NLP products: (1) a content moderation classifier that reads a full tweet and labels it toxic/non-toxic; (2) a writing assistant that suggests the next sentence given what the user has typed so far. Which pairing and rationale is correct?

- [ ] A. Task 1 → BERT, because bidirectional attention lets `[CLS]` aggregate full-sentence context for classification; Task 2 → GPT, because causal masking trains the model to predict the next token from prior context only
- [ ] B. Task 1 → GPT, because next-token prediction implicitly learns sentence representations useful for classification; Task 2 → BERT, because masked language modeling teaches contextual embeddings useful for generation
- [ ] C. Task 1 → BERT, because BERT's MLM loss directly optimizes classification objectives; Task 2 → GPT, because GPT's encoder stack processes the full input before generating each token
- [ ] D. Task 1 → GPT, because GPT produces one output per input token matching the binary classification setup; Task 2 → BERT, because its `[SEP]` token separates input from the generated continuation

> [!note]- Answer
> **A**
>
> Task 1 是理解任务（读全文分类）→ BERT 双向 attention 让 `[CLS]` 能看到整句上下文，fine-tune 一个 Linear 头即可。Task 2 是生成任务（给定前缀预测下一句）→ GPT 因果 mask 训练的就是"看到前缀预测下一个 token"，天然匹配。
> - **B 错**：GPT 不是句子分类的自然选择；BERT 的 MLM 不支持自回归生成
> - **C 错**：GPT 是 Decoder-only，没有"encoder stack"；MLM 不是分类目标
> - **D 错**：描述完全混淆了两者的架构和 token 作用

---

**Question 2.** *(ViT 小数据局限 ★★★)* A medical imaging team trains ResNet-50 and ViT-Base/16 from scratch on 8,000 labeled chest X-rays. ViT performs significantly worse. Which explanation is most accurate?

- [ ] A. ViT's 16×16 patch size is too coarse for chest X-rays, causing the model to miss fine-grained pathological details that a CNN's 3×3 sliding kernel captures
- [ ] B. ViT's learned positional encodings overfit on small datasets because they are additional trainable parameters tied to specific positions
- [ ] C. ViT lacks built-in assumptions about locality and spatial regularity, so it must learn these from data — but 8,000 images is insufficient to discover structure that CNN's inductive biases provide for free
- [ ] D. ViT's $O(T^2)$ attention cost causes the attention weights to overfit training images, degrading generalization on small datasets

> [!note]- Answer
> **C**
>
> CNN 内置了局部性（local connectivity）和平移等变性（translation equivariance）两个 inductive bias，这些假设与图像数据结构完全匹配，小数据下先验"做了大量工作"。ViT 没有这些假设，需要从数据中自学，8000 张图远远不够——这正是 PDF p40 的核心结论（ViT 在 ImageNet-1K 上不如 EfficientNet-B7）。
> - **A 错**：patch size 是可调的超参数，不是结构上的根本原因
> - **B 错**：positional encoding 只是 ViT 的一小部分参数，不是主要瓶颈
> - **D 错**：$O(T^2)$ 是计算复杂度问题，不是过拟合机制

---

## Short-Answer Questions

---

**Question 3.** *(BERT Fine-tuning 格式 ★★)* A team wants to use pre-trained BERT for three tasks: (i) classifying movie reviews as positive/negative; (ii) identifying entities in a sentence (e.g., labelling each word as PERSON/ORG/O); (iii) answering questions from a given paragraph (finding the answer span). **(4 Marks)**

(a) 对于任务 (i) 和 (ii)，分别描述输入格式、使用哪个位置的输出、以及输出头的结构。**(2 Marks)**

(b) 任务 (iii) 对应 BERT Case 4（SQuAD）。描述输入格式，以及如何用两个可学习向量预测答案的起止位置。**(2 Marks)**

> [!note]- Answer
> **(a)**
> **任务 (i) — 句子分类（Case 1）**：
> 输入格式：`[CLS] w₁ w₂ … wₙ`。使用 `[CLS]` 位置的最终隐状态，接一个 Linear 分类头输出 class logit。BERT 主干 fine-tune，头部从头训练。
>
> **任务 (ii) — Token 级分类（Case 2）**：
> 输入格式：`[CLS] w₁ w₂ … wₙ`。对每个词 token $w_i$ 的最终隐状态分别接一个独立的 Linear 分类头，输出该词的实体标签（如 B-PER/I-PER/O）。`[CLS]` 位置忽略。
>
> **(b)**
> **输入格式**：`[CLS] question_tokens [SEP] document_tokens [SEP]`。
>
> 引入两个可学习向量 $s$（start vector）和 $e$（end vector），维度与 BERT 隐层相同。对文档区域每个 token 位置 $i$ 的隐状态 $h_i$ 分别计算：
> - start logit $= s \cdot h_i$
> - end logit $= e \cdot h_i$
>
> 对所有文档位置分别做 softmax，argmax 得到 start position $s^*$ 和 end position $e^*$，答案为文档中 $[s^*, e^*]$ 区间的 tokens。

---

**Question 4.** *(SSM / Mamba ★★)* A genomics team processes DNA sequences of length $T=100{,}000$. Transformer's $O(T^2)$ cost is prohibitive. They consider S4 and Mamba. **(5 Marks)**

(a) 从离散 SSM 递推 $h_k = \bar{A} h_{k-1} + \bar{B} x_k$，$y_k = C h_k$ 出发，令 $h_0 = 0$，推导 $y_k$ 可以写成卷积 $y_k = (K * x)_k$ 的形式，并写出卷积核 $K_i$ 的表达式。**(2 Marks)**

(b) S4 利用卷积形式实现 $O(N \log N)$ 并行训练。Mamba 引入输入相关的参数 $B_t, C_t, \Delta_t$。解释这一改动为什么使卷积形式无法使用，以及 Mamba 训练时改用什么方法。**(2 Marks)**

(c) 推理阶段，比较 Transformer（带 KV-cache）和 Mamba 每生成一个新 token 时的内存开销。哪个随序列长度增长，哪个是常数？**(1 Mark)**

> [!note]- Answer
> **(a)**
> 逐步展开递推（$h_0=0$）：
> $$h_1 = \bar{B}x_0,\quad h_2 = \bar{A}\bar{B}x_0 + \bar{B}x_1,\quad \ldots,\quad h_k = \sum_{i=0}^{k} \bar{A}^{k-i}\bar{B}\,x_i$$
> $$y_k = Ch_k = \sum_{i=0}^{k} \underbrace{C\bar{A}^{k-i}\bar{B}}_{K_{k-i}} x_i = (K * x)_k$$
>
> **卷积核**：$K_i = C\bar{A}^i\bar{B}$
>
> 这是与输入无关的固定核，可预先计算后用 FFT 做 $O(N\log N)$ 卷积。
>
> **(b)**
> S4 卷积形式成立的前提：$K_i = C\bar{A}^i\bar{B}$ 是**固定核**（与输入无关），可一次性预计算并重复使用。
>
> Mamba 中 $B_t, C_t, \Delta_t$ 均为 $x_t$ 的函数，每个时间步的 $\bar{A}_t, \bar{B}_t, C_t$ 都不同，卷积核随位置变化，无法表示为单一固定 $K$ 与 $x$ 的卷积。卷积形式失效。
>
> Mamba 训练时改用 **Parallel Scan（并行扫描）**算法：利用关联操作的分治合并性质，在 $O(\log T)$ 深度、$O(N)$ 总计算量内并行计算所有时间步的隐状态。
>
> **(c)**
> - **Transformer（KV-cache）**：每生成一个新 token，需存储所有历史 token 的 K 和 V，内存随序列长度线性增长：$O(T \cdot d)$（每层）。
> - **Mamba**：推理时以递推形式运行，仅维护固定大小的隐状态 $h_t$，**与序列长度无关**，内存为 $O(N_\text{state})$（常数）。
>
> Mamba 推理内存是**常数**；Transformer 推理内存**随序列长度线性增长**。
