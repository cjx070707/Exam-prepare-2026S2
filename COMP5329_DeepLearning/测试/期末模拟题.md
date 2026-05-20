# COMP5329 Deep Learning — Mock Final Exam

> **Instructions**: This mock exam covers all four study groups (Weeks 2–12).
> Section A: Multiple Choice (20 pts) | Section B: Short Answer (30 pts) | Section C: Coding (25 pts) | Section D: Essay (25 pts)

---

## Section A — Multiple Choice (20 pts, 2 pts each)

---

**A1.** A 3-layer MLP with no activation on the hidden layer is equivalent to:

- (a) A 2-layer MLP with a nonlinear hidden layer
- (b) A single linear classifier
- (c) A kernel SVM
- (d) A network with half the parameters

> [!success]- Answer
> 
> **(b)**
> 
> $W_2(W_1 x+b_1)+b_2=(W_2W_1)x+\text{const}$，线性映射的复合仍然是线性的。只增加深度而不加 nonlinear activation 不增加任何表达能力。

---

**A2.** The primary reason ReLU is preferred over Sigmoid in deep networks:

- (a) ReLU outputs are zero-centred
- (b) ReLU has a bounded output range
- (c) ReLU does not saturate in the positive region, avoiding gradient vanishing
- (d) ReLU requires less memory

> [!success]- Answer
> 
> **(c)**
> 
> 对 $x>0$，$f'(x)=1$——梯度恒定，不会 vanish。Sigmoid 在两端都会饱和（$f'(x)\to0$，当 $|x|\gg0$）。注意 ReLU 并非 zero-centred（输出 $\geq0$），所以选项 (a) 是错的。

---

**A3.** Adam's bias correction divides $m_t$ by $(1-\beta_1^t)$. What does this solve?

- (a) Prevents the learning rate from growing unboundedly
- (b) Corrects underestimation of the first moment caused by zero-initialising $m_0=0$
- (c) Replaces the need for a separate learning rate hyperparameter
- (d) Ensures $v_t$ stays positive

> [!success]- Answer
> 
> **(b)**
> 
> $m_0=0$，$\beta_1=0.9$ 时，第 1 步：$m_1=0.1\,g_1$，只有真实梯度的 10%。Correction 后：$\hat{m}_1=m_1/(1-0.9)=g_1$。不做 correction 的话，早期步骤过于保守。

---

**A4.** Input $32\times32$, filter $5\times5$, padding $=2$, stride $=2$. Output size?

- (a) $28\times28$
- (b) $16\times16$
- (c) $14\times14$
- (d) $32\times32$

> [!success]- Answer
> 
> **(b) $16\times16$**
> 
> $\lfloor(32-5+2\times2)/2\rfloor+1=\lfloor31/2\rfloor+1=16$

---

**A5.** In Kipf & Welling's GCN, why is $\hat{A}=A+I$ used?

- (a) To make $\hat{A}$ invertible
- (b) To include each node's own features in its aggregation
- (c) To ensure all eigenvalues of $\hat{A}$ are positive
- (d) To reduce computation cost

> [!success]- Answer
> 
> **(b)**
> 
> 不加 self-loop 时，$AH$ 只聚合邻居。加上 $I$ 后 $\hat{A}_{ii}=1$，每个节点在更新时也包含自己的 feature。

---

**A6.** The vanishing gradient problem in vanilla RNNs is primarily caused by:

- (a) Using tanh, which clips activations to $(-1,1)$
- (b) Repeatedly multiplying $\tanh'(\cdot)\cdot W_{hh}$ across time steps, producing a product typically much less than 1
- (c) The lack of a cell state
- (d) Using a fixed-length context vector

> [!success]- Answer
> 
> **(b)**
> 
> BPTT 要求梯度从第 $k$ 步传回第 1 步，经过 $\prod_{t=2}^k\tanh'(\cdot)W_{hh}$。由于 $\tanh'\in[0,1]$（通常 $\ll1$），这个连乘积指数级衰减。选项 (c) 是结果，不是机制。

---

**A7.** In scaled dot-product attention, $QK^\top$ is divided by $\sqrt{d_k}$. Why?

- (a) To ensure unit variance output
- (b) To prevent large dot products from pushing softmax into saturation where gradients vanish
- (c) To normalise attention weights to sum to one
- (d) To reduce memory cost

> [!success]- Answer
> 
> **(b)**
> 
> 当 $q,k\sim\mathcal{N}(0,1)$，维度为 $d_k$ 时，dot product 的方差为 $d_k$。不 scale 时，$d_k$ 大 → softmax 接近 one-hot → 梯度接近零。除以 $\sqrt{d_k}$ 恢复单位方差。（softmax 本来就归一化到和为 1，这不是 scale 的原因。）

---

**A8.** Why can't BERT be used directly for autoregressive generation?

- (a) BERT was not pre-trained on enough data
- (b) BERT's bidirectional attention allows future tokens to influence current predictions, violating the autoregressive requirement
- (c) BERT's vocabulary is too small
- (d) BERT does not use positional encodings

> [!success]- Answer
> 
> **(b)**
> 
> Autoregressive generation 要求 $p(x_t|x_{<t})$——预测只能使用过去的 token。BERT 的 full attention 让每个位置都能关注包括未来在内的所有位置，逐 token 生成时会产生循环依赖。

---

**A9.** In LoRA, $\Delta W=BA$ initialises $B=0$. Why?

- (a) To ensure $A$ dominates at the start
- (b) So $\Delta W=0$ at initialisation, preserving the exact pretrained model state
- (c) To prevent rank from growing beyond $r$
- (d) To make gradient of $A$ zero initially

> [!success]- Answer
> 
> **(b)**
> 
> 初始化时 $\Delta W=B\cdot A=0\cdot A=0$，模型与原始 pretrained checkpoint 完全相同。Fine-tuning 从这个精确状态出发，不引入任何扰动。

---

**A10.** Which self-supervised method does NOT require negative samples?

- (a) SimCLR
- (b) MoCo
- (c) BYOL
- (d) CLIP

> [!success]- Answer
> 
> **(c) BYOL**
> 
> BYOL 使用 teacher-student 架构，对 teacher 做 stop-gradient。这种不对称设计（stop-gradient + 只有 student 有 predictor head）在不需要 negative sample 的情况下防止了 representational collapse。SimCLR 用 in-batch negatives；MoCo 用 queue；CLIP 用跨模态 negatives。

---

## Section B — Short Answer (30 pts)

---

**B1. (6 pts)** Explain BN vs LN: (i) which dimensions each normalises over, (ii) batch size dependence, (iii) why Transformers use LN.

> [!success]- Answer
> 
> **(i) 归一化的维度：**
> - **BN**：在 $(N,H,W)$ 上归一化，每个 channel $C$ 独立。Statistics 在 batch 内所有样本间共享。
> - **LN**：在 $(C,H,W)$ 上归一化，每个样本 $N$ 独立。每个样本只用自己的 statistics。
> 
> **(ii) 对 batch size 的依赖：**
> - BN：有依赖。Batch 小 → statistics 噪声大、不可靠。训练和测试时行为不同（batch stats vs running stats）。
> - LN：无依赖。Per-sample 归一化，训练和测试时行为完全一致。
> 
> **(iii) 为什么 Transformer 用 LN：**
> NLP 任务序列长度可变，每个设备上的有效 batch size 较小。对长度不同的序列计算 BN statistics 定义不清。LN 对每个 token 单独归一化，天然处理可变长度，且无 train/test 差异。

---

**B2. (6 pts)** Describe the three-component MLLM architecture. For each: role and one concrete example.

> [!success]- Answer
> 
> | 组件 | 作用 | 具体例子 |
> |------|------|----------|
> | **Vision Encoder** | 将图像转为视觉 feature vector 序列（每个 patch 一个） | CLIP-ViT：在 4 亿图文对上预训练，patch embedding 与语言对齐 |
> | **Connector Module** | 桥接视觉 feature 和 LLM token 空间 | Q-Former（BLIP-2）：32 个可学习 query 通过 cross-attention 压缩视觉 feature；MLP projection（LLaVA）是更简单的线性替代 |
> | **Language Model** | 冻结或 LoRA fine-tuned 的 decoder-only Transformer，联合处理视觉和文本 token | LLaMA、Vicuna |

---

**B3. (8 pts)** Write the InfoNCE loss. Answer: (i) role of $\tau$, (ii) why hard negatives receive larger gradient weight (show gradient), (iii) SimCLR vs MoCo difference.

> [!success]- Answer
> 
> $$\mathcal{L}=-\log\frac{\exp(q\cdot k^+/\tau)}{\sum_j\exp(q\cdot k_j/\tau)}$$
> 
> **(i) $\tau$ 的作用：**
> 控制 softmax 分布在 negatives 上的锐利程度。$\tau$ 小 → 集中关注最难的 negatives（梯度信号强，但训练不稳定）。$\tau$ 大 → 对所有 negatives 一视同仁。
> 
> **(ii) Hard negatives 在梯度中的体现：**
> $$\frac{\partial\mathcal{L}}{\partial q}=-\frac{k^+}{\tau}+\frac{1}{\tau}\sum_j p_j k_j,\quad p_j=\frac{\exp(q\cdot k_j/\tau)}{\sum_{j'}\exp(q\cdot k_{j'}/\tau)}$$
> Hard negatives（$q\cdot k_j$ 大）有更高的 softmax 权重 $p_j$，对推开 $q$ 与错误表示的力度更大。Easy negatives 的 $p_j\approx0$，几乎不影响训练。
> 
> **(iii) SimCLR vs MoCo 的区别：**
> SimCLR 用当前 mini-batch 内的其他样本作为 negatives——需要极大的 batch（4096+）。MoCo 维护一个存储过去 batch 编码 key 的 FIFO queue；key encoder 通过 EMA（$m\approx0.999$）更新，使得无需大 batch 也能保持 negatives 的一致性。

---

**B4. (10 pts)** (a) Write the LSTM cell state update. (b) Explain precisely why $\partial c_t/\partial c_{t-1}$ does not decay exponentially. (c) What does $f_t\approx0$ for all steps imply?

> [!success]- Answer
> 
> **(a)：**
> $$c_t=c_{t-1}\otimes f_t+\tilde{c}_t\otimes i_t$$
> 其中 $f_t=\sigma(W_f[h_{t-1};x_t])$，$i_t=\sigma(W_i[h_{t-1};x_t])$，$\tilde{c}_t=\tanh(W_c[h_{t-1};x_t])$。
> 
> **(b)：** 梯度的主项为：
> $$\frac{\partial c_t}{\partial c_{t-1}}\approx f_t$$
> 梯度每步乘以 $f_t$。但 $f_t$ 是**可学习的 gate**——网络可以训练 $f_t\approx1$ 来维持长期记忆，使得 $\prod_t f_t\approx1$，梯度不会衰减。
> 
> 相比之下，vanilla RNN 的因子是 $\tanh'(\text{net}_t)\cdot W_{hh}$——$\tanh'\leq1$（通常 $\ll1$）且不可学习，连乘积指数级衰减。关键区别：LSTM 的梯度因子是*可学习的*，RNN 的不是。
> 
> **(c)：** 当 $f_t\approx0$ 时，$c_t\approx\tilde{c}_t\otimes i_t$——上一步的 cell state 被完全清除。网络没有任何长期记忆，每步只处理当前输入。对需要长距离依赖的任务来说是灾难性的。

---

## Section C — Coding (25 pts)

---

**C1. (10 pts)** Implement scaled dot-product attention from scratch:

```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    # Q,K: (B,N,d_k)  V: (B,N,d_v)
    # mask: (B,N,N) bool — True = masked
    # returns: output (B,N,d_v), weights (B,N,N)
    pass
```

> [!success]- Answer
> 
> ```python
> import math, torch
> 
> def scaled_dot_product_attention(Q, K, V, mask=None):
>     d_k = Q.shape[-1]
>     scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
>     if mask is not None:
>         scores = scores.masked_fill(mask, float('-inf'))
>     weights = torch.softmax(scores, dim=-1)
>     output  = weights @ V
>     return output, weights
> ```
> 
> **要点：** 用 `K.transpose(-2,-1)` 而非 `.T`——`.T` 会反转所有维度，破坏 batched tensor。`masked_fill` 填 `-inf` → softmax 后对应位置精确为 0。

---

**C2. (10 pts)** Implement a single LSTM time step:

```python
def lstm_step(x_t, h_prev, c_prev, W_f, W_i, W_o, W_c, b_f, b_i, b_o, b_c):
    # x_t:(B,input)  h_prev,c_prev:(B,hidden)
    # W_*:(input+hidden,hidden)  b_*:(hidden,)
    # returns h_t, c_t both (B,hidden)
    pass
```

> [!success]- Answer
> 
> ```python
> def lstm_step(x_t, h_prev, c_prev, W_f, W_i, W_o, W_c, b_f, b_i, b_o, b_c):
>     combined = torch.cat([h_prev, x_t], dim=-1)
>     f_t      = torch.sigmoid(combined @ W_f + b_f)
>     i_t      = torch.sigmoid(combined @ W_i + b_i)
>     o_t      = torch.sigmoid(combined @ W_o + b_o)
>     c_tilde  = torch.tanh(combined @ W_c + b_c)
>     c_t      = c_prev * f_t + c_tilde * i_t
>     h_t      = o_t * torch.tanh(c_t)
>     return h_t, c_t
> ```
> 
> **要点：** 三个 gate 用 sigmoid，candidate 用 tanh。Cell state 以加法方式更新：`c_prev * f_t + c_tilde * i_t`。

---

**C3. (5 pts)** Implement VAE reparameterisation and KL loss:

```python
def reparameterize(mu, log_var):
    pass  # returns z ~ N(mu, exp(log_var)), differentiable

def kl_loss(mu, log_var):
    pass  # closed-form KL(N(mu,sigma^2) || N(0,I))
```

> [!success]- Answer
> 
> ```python
> def reparameterize(mu, log_var):
>     std = torch.exp(0.5 * log_var)
>     eps = torch.randn_like(std)
>     return mu + std * eps
> 
> def kl_loss(mu, log_var):
>     return 0.5 * torch.sum(torch.exp(log_var) + mu**2 - 1 - log_var)
> ```
> 
> **为什么需要 reparameterization：** 直接采样 $z\sim\mathcal{N}(\mu,\sigma^2)$ 是不可微的。将其改写为 $z=\mu+\sigma\cdot\epsilon$，$\epsilon\sim\mathcal{N}(0,I)$，把随机性隔离在 $\epsilon$ 中（无参数），梯度就能正常地流过 $\mu$ 和 $\sigma$。

---

## Section D — Essay (25 pts)

---

**D1. (12 pts)** Compare CNNs and ViT for image classification: inductive biases, small vs large dataset performance, computational complexity, and one ViT design choice compensating for the lack of spatial bias.

> [!success]- Answer
> 
> **Inductive biases：**
> CNN 硬编码了两个先验：*locality*（local receptive fields）和 *translation equivariance*（weight sharing）。ViT 没有任何空间 inductive bias——所有空间关系都必须从数据中学习。
> 
> **小数据集 vs 大数据集：**
> 小数据集上，CNN 优于 ViT。CNN 的内置 bias 相当于强正则化，泛化所需样本更少，ViT 在缺乏 locality prior 时更容易 overfit。大数据集（JFT-300M、ImageNet-21k）上，ViT 能与或超越 CNN，学习到 patch 间的强全局关系，且 scale 能力更好。
> 
> **计算复杂度：**
> 
> | | CNN | ViT |
> |---|---|---|
> | 每层 | $O(N\cdot F^2\cdot C^2)$，与图像大小线性相关 | $O(T^2\cdot D)$，与 patch 数 $T$ 的平方相关 |
> | 分辨率 scaling | 线性 | 二次 |
> 
> 高分辨率输入时，ViT 的 $O(T^2)$ attention 代价很高。Swin Transformer 等高效变体将其降为线性。
> 
> **补偿设计——Learned Positional Embeddings：**
> 没有 positional encoding 时，self-attention 对输入顺序不敏感（permutation invariant），无法区分 patch 的位置。ViT 在每个 patch token 输入 encoder 前加上可学习的 $p_i\in\mathbb{R}^D$，让网络从数据中学习位置嵌入与空间结构的对应关系。比 CNN 硬编码的 locality 更灵活，但因此需要更多数据。

---

**D2. (13 pts)** GAN training is unstable. Explain the root cause and how WGAN addresses it. Include: minimax objective, optimal discriminator, generator gradient with disjoint supports, Wasserstein-1 distance, and Lipschitz enforcement.

> [!success]- Answer
> 
> **GAN minimax objective：**
> $$\min_G\max_D\;\mathbb{E}_{x\sim p_r}[\log D(x)]+\mathbb{E}_{z\sim p_z}[\log(1-D(G(z)))]$$
> 
> **Optimal discriminator：**
> 对固定的 $G$，在每个 $x$ 处最大化被积项：
> $$D^*(x)=\frac{p_r(x)}{p_r(x)+p_g(x)}$$
> 
> **Disjoint support 下的 generator 梯度：**
> 代入 $D^*$ 得 $\mathcal{L}(G,D^*)=2\,\text{JS}(p_r\|p_g)-2\log2$。在高维空间中，$p_r$ 和 $p_g$ 分布在低维流形上，几乎总是不相交。此时 JS divergence 恒等于 $\log2$，与两个分布有多近无关——loss 面是平的，$\nabla_G\mathcal{L}\approx0$。训练良好的 discriminator 反而扼杀了 generator 的学习信号。
> 
> **Wasserstein-1 distance：**
> $$W(p_r,p_g)=\sup_{\|f\|_L\leq1}\;\mathbb{E}_{p_r}[f(x)]-\mathbb{E}_{p_g}[f(x)]$$
> 与 JS divergence 不同，$W$ 在分布 support 不相交时仍然有明确定义且提供平滑、非零的梯度——它衡量将 $p_g$ 传输到 $p_r$ 所需的最小"代价"，随 generator 参数连续变化。
> 
> **Lipschitz 约束的实现：**
> supremum 是在 1-Lipschitz 函数（$\|\nabla f\|_2\leq1$）上取的。实现方式：
> 1. **Weight clipping**（原始 WGAN）：将 critic 权重裁剪到 $[-c,c]$。简单但限制了模型容量。
> 2. **Gradient penalty**（WGAN-GP，更常用）：在 loss 中加 $\lambda\,\mathbb{E}_{\hat{x}}[(\|\nabla_{\hat{x}}f_w(\hat{x})\|_2-1)^2]$，其中 $\hat{x}$ 是真实数据和生成数据的插值点。可微且训练更稳定。
> 
> WGAN 的 critic 始终给 generator 提供有意义的、不会消失的梯度信号，从根本上解决了原始 GAN 的训练不稳定问题。
