# W7 — Sequence Modeling I
**考点来源：复习笔记/第三组 序列数据.md（W7 部分）**

> [!danger] 备考优先级：必考

---

## Multiple Choice Questions

---

**Question 1.** *(BPTT 梯度消失 ★★★)* A team trains a vanilla RNN to classify 200-word product reviews. The model's predictions are heavily influenced by the last 10–20 words; the first 100+ words are effectively ignored. What is the most direct cause?

- [ ] A. The hidden state $h_t$ has fixed dimensionality, so it cannot encode more than a bounded number of words regardless of sequence length
- [x] B. The gradient path to early time steps traverses a repeated product of $\tanh'(\cdot) \cdot W_{hh}$, which shrinks exponentially when the spectral radius of $W_{hh}$ is below 1
- [ ] C. Each time step computes a new hidden state that structurally overwrites the previous one, erasing early-token information after each forward step
- [ ] D. Gradient clipping truncates small gradient values to zero during backpropagation, preventing updates from reaching early time steps

> [!note]- Answer
> **B**
>
> BPTT 梯度路径：$\frac{\partial h_t}{\partial h_{t-k}} = \prod_{i} \tanh'(\cdot) \cdot W_{hh}$。每步乘以 $\tanh'$（最大值 1，通常远小于 1）和 $W_{hh}$，若谱半径小于 1 则连乘后指数级衰减，早期 token 的梯度趋近于零。
> - **A 错**：固定维度导致信息压缩，但不是梯度消失的机制
> - **C 错**：隐状态会传递给下一步，并非"覆盖"——问题是梯度传不回去，不是前向信息消失
> - **D 错**：Gradient clipping 截断的是**大**梯度（防爆炸），不截断小梯度；对梯度消失无效

---

**Question 2.** *(LSTM 梯度路径 ★★★)* A team compares a vanilla RNN and an LSTM (forget gate initialized near 1) on a T=500 long-range dependency task. Why does the LSTM's cell state provide a more stable gradient path?

- [ ] A. The LSTM applies layer normalization along the cell state gradient path, preventing both vanishing and exploding before the gradient reaches earlier steps
- [ ] B. The update $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$ creates an additive path where $\partial c_t / \partial c_{t-1} \approx f_t$, a learnable value that can be trained close to 1
- [ ] C. The output gate $o_t$ rescales the hidden state before backpropagation, reducing the effective per-step gradient magnitude and preventing numerical instability
- [x] D. LSTM's three gates partition the gradient into three parallel streams, so even if two streams vanish, the third preserves the signal to earlier layers

> [!note]- Answer
> **B**
>
> $\frac{\partial c_t}{\partial c_{t-1}} = f_t$，即遗忘门的输出值（可学习标量）。当网络训练 $f_t \approx 1$ 时，梯度可以近乎无损通过，无需经过 $\tanh'(\cdot) \cdot W_{hh}$ 的连乘。LSTM 没有消除乘法，而是用可学习的 $f_t$ 替换了固定的小常数。
> - **A 错**：LSTM 的梯度路径中没有 Layer Normalization
> - **C 错**：输出门影响 $h_t$，不在 cell state 的梯度路径上
> - **D 错**：三个门是串行乘法关系，不是独立并行流

---

**Question 3.** *(Scaled Dot-Product Attention ★★★)* An engineer implements self-attention with $d_k=64$. During debugging, she removes the $\sqrt{d_k}$ scaling. Gradient norms for $W_Q$ and $W_K$ collapse to near-zero within the first few iterations. What is the most direct cause?

- [ ] A. Without scaling, $QK^\top$ logits grow large, pushing softmax toward a near-one-hot distribution whose Jacobian is near-zero, killing gradients into $Q$ and $K$
- [ ] B. Without scaling, attention weights sum to more than 1.0 per row, violating the probability constraint and making the loss numerically undefined
- [ ] C. Without scaling, the value vectors $V$ receive attention weights larger than 1.0, causing the weighted sum to overflow floating-point precision in the forward pass
- [ ] D. Without scaling, all positions receive equal attention weight, making the output identical to mean-pooling of $V$, which provides no gradient signal for $W_Q$ or $W_K$

> [!note]- Answer
> **A**
>
> $d_k=64$ 时，$q \cdot k$ 的方差 $\approx d_k = 64$，标准差 $\approx 8$。大 logit 进入 softmax 后输出接近 one-hot。Softmax 的 Jacobian $J_{ij} = p_i(\delta_{ij} - p_j)$，当 $p \approx e_{i^*}$ 时所有元素趋近于 0，梯度无法传回 $W_Q, W_K$。
> - **B 错**：softmax 无论输入多大，输出必然和为 1
> - **C 错**：softmax 输出在 $(0,1)$ 之间，不会大于 1
> - **D 错**：logit 很大时 softmax 输出是 one-hot（极度不均匀），而非均匀分布

---

## Short-Answer Questions

---

**Question 4.** *(LSTM vs GRU 综合 ★★★)* A team processes 1,000-step sensor sequences to detect rare failure events, comparing LSTM and GRU. **(5 Marks)**

(a) LSTM 的 cell state 更新为 $c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t$。解释 $\partial c_t / \partial c_{t-1}$ 等于什么，以及为什么这比 RNN 的梯度路径更稳定。**(2 Marks)**

(b) 写出 GRU 的隐状态更新公式，并说明 update gate $z_t$ 在这个公式中控制什么。**(2 Marks)**

(c) 从参数量的角度解释为什么 GRU 比 LSTM 计算效率更高。**(1 Mark)**

> [!note]- Answer
> **(a)**
> $\frac{\partial c_t}{\partial c_{t-1}} = f_t$，即遗忘门的输出值（可学习标量，范围在 0 到 1 之间）。
>
> 当网络训练 $f_t \approx 1$ 时，梯度可以近乎无损地从 $c_t$ 传回 $c_{t-1}$，无需经过 $\tanh'(\cdot) \cdot W_{hh}$ 的连乘。相比之下，RNN 每步梯度必须乘以 $\tanh'(\cdot) \cdot W_{hh}$（两者均 $\leq 1$），$T$ 步后指数级衰减趋近于零。LSTM 的关键在于用可学习的 $f_t$ 替换了固定的小常数。
>
> **(b)**
> $$h_t = (1 - z_t) \odot h_{t-1} + z_t \odot \tilde{h}_t, \quad \tilde{h}_t = \tanh(W[r_t \odot h_{t-1},\; x_t])$$
>
> $z_t$ 是更新门，控制新旧隐状态的**插值比例**：$z_t \to 0$ 时完全保留旧隐状态，$z_t \to 1$ 时完全用候选状态替换。
>
> **(c)**
> LSTM 有 4 组权重矩阵（forget/input/output gate + candidate），参数量约为等规模 RNN 的 **4 倍**；GRU 有 3 组（reset/update gate + candidate），约 **3 倍**。参数少 → 每步前向/反向计算量少 → 训练更快，两者性能接近。

---

**Question 5.** *(Transformer 架构综合 ★★★)* A team implements a 12-layer Transformer encoder for document classification with only Multi-Head Self-Attention — no FFN, no residual connections, no LayerNorm. **(5 Marks)**

(a) 模型在 12 层时无法收敛。指出两个缺失的稳定化组件（不包括 FFN），并解释每个组件在深层 Transformer 中的具体作用。**(2 Marks)**

(b) Self-attention 是置换等变的：打乱 token 顺序，输出也对应打乱。解释这对序列建模是什么问题；并对比 sinusoidal 和 learned 两种位置编码的关键区别（各一点）。**(2 Marks)**

(c) 一位成员认为"FFN 是多余的——self-attention 已经混合了所有 token 的信息"。给出一个反驳论点。**(1 Mark)**

> [!note]- Answer
> **(a)**
> **残差连接（Residual Connection）**：$x \leftarrow x + \text{Sublayer}(x)$。反向传播时梯度含 "+1" 项，提供一条不经过子层的直接梯度通路，即使子层梯度趋近于零，全局梯度仍可传回浅层，缓解深层网络梯度消失。
>
> **Layer Normalization**：对每个 token 的特征维度做归一化，使不同层的激活值保持在稳定数值范围内，防止激活爆炸或极端缩放导致训练不稳定。
>
> **(b)**
> **问题**：置换等变性使模型把 "dog bites man" 和 "man bites dog" 视为同一组 token 的集合，丢失词序信息，无法区分语义完全不同的句子。
>
> **Sinusoidal PE**：固定函数（$\sin/\cos$），无需训练，能外推到比训练序列更长的位置。
>
> **Learned PE（BERT、ViT）**：位置编码作为可学习参数，更灵活；但无法外推到训练时未见过的更长序列位置。
>
> **(c)**
> Self-attention 的输出是 Value 向量的加权**线性组合**——虽然混合了跨 token 的信息，但组合本身是线性变换。FFN 在每个 token 上独立引入**非线性变换**，将 attention 聚合的线性混合提升到更复杂的特征空间。若去掉 FFN，多层 attention 的叠加实质上仍是线性运算，表达能力极为有限。

---

## Handwritten Coding Questions

---

**Question 6.** *(Scaled Dot-Product Attention ★★★)* Implement scaled dot-product attention in NumPy. **(6 Marks)**

```python
import numpy as np

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: (T, d_k)
    K: (T, d_k)
    V: (T, d_v)
    mask: (T, T) bool array, True = positions to mask out (set to -inf)
    returns: (T, d_v)
    """
    ...
```

**(2 Marks)** 计算正确的 scaled attention scores 矩阵，形状 (T, T)

**(2 Marks)** 正确应用 mask 并逐行计算 softmax（含数值稳定处理）

**(2 Marks)** 返回 attention-weighted 输出

> [!note]- Answer
> ```python
> import numpy as np
>
> def scaled_dot_product_attention(Q, K, V, mask=None):
>     d_k = Q.shape[-1]
>
>     # Step 1: scaled scores
>     scores = Q @ K.T / np.sqrt(d_k)          # (T, T)
>
>     # Step 2: apply mask, then softmax
>     if mask is not None:
>         scores[mask] = -np.inf
>
>     scores_max = np.max(scores, axis=-1, keepdims=True)   # numerical stability
>     exp_scores = np.exp(scores - scores_max)
>     attn_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)  # (T, T)
>
>     # Step 3: weighted sum of V
>     return attn_weights @ V                   # (T, d_v)
> ```
>
> **关键点**：
> - `Q @ K.T` 注意是 $K$ 的转置，再除以 `np.sqrt(d_k)`
> - mask 必须在 softmax **之前**应用，设为 `-np.inf`（不是 0）
> - softmax 减去 max 做数值稳定，沿 `axis=-1`（每行归一化）
> - 最终 `attn_weights @ V`，形状 (T, d_v)
> - 常见错误：mask 在 softmax 后应用、忘记除以 `sqrt(d_k)`、softmax 沿错误轴计算
