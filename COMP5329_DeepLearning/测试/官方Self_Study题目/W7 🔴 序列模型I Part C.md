# W7 — Part C Exam-Style Questions
**来源：Week7_Sequence_Modeling_Architectures_I.ipynb（官方 tutorial，未改动）**

> [!danger] 备考优先级：必考

---

---
# Part C · Exam-Style Questions

> Three short-answer questions at medium-to-high difficulty, each with a collapsed **Model Answer**. Try them on paper first, then expand the answer to check your reasoning and pick up the "key points".

## Q1 · Why $\sqrt{d_k}$? (softmax / gradient flow)

Scaled dot-product attention computes

$$\mathrm{Attn}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V.$$

Suppose the entries of $Q$ and $K$ are i.i.d. with zero mean and unit variance.

**(a)** Show that each entry of $QK^{\top}$ has variance $d_k$.

**(b)** Explain what happens to the softmax output as $d_k \to \infty$ **without** the $\sqrt{d_k}$ scaling.

**(c)** Using the softmax Jacobian, explain why this is a problem for gradient-based training, and argue why dividing by $\sqrt{d_k}$ — as opposed to $d_k$ or $1$ — is the right fix.

<details>
<summary><b>▸ Model Answer · Q1</b></summary>

**(a)** Let $q, k \in \mathbb{R}^{d_k}$ be a query/key pair. Their inner product is $\langle q, k\rangle = \sum_{i=1}^{d_k} q_i k_i$. Each $q_i k_i$ has mean $\mathbb{E}[q_i]\mathbb{E}[k_i] = 0$ and variance $\mathrm{Var}(q_i)\mathrm{Var}(k_i) = 1$, and the terms are independent. Therefore $\mathrm{Var}(\langle q, k\rangle) = d_k$, and the standard deviation grows like $\sqrt{d_k}$.

**(b)** Without scaling, the logits fed into softmax have magnitude on the order of $\sqrt{d_k}$. For large $d_k$, the largest logit dominates and the softmax output concentrates on a single position — it approaches a one-hot distribution.

**(c)** The Jacobian of softmax is $J_{ij} = p_i(\delta_{ij} - p_j)$. When the output is near one-hot ($p \approx e_{i^\star}$), every entry of $J$ is near zero, so **gradients vanish into $Q$ and $K$**. The fix must keep the *variance* of the logits at $O(1)$, and that is exactly what dividing by $\sqrt{d_k}$ achieves. Dividing by $d_k$ instead would shrink the standard deviation to $1/\sqrt{d_k}\to 0$ — over-flattening the softmax and destroying the model's ability to *select* anything (the opposite failure mode).

**Key points:**
- Variance argument, not mean argument — softmax cares about *spread*.
- Saturating softmax ⇒ zero Jacobian ⇒ dead gradients, by exactly the same mechanism that kills deep sigmoid networks.
- $\sqrt{d_k}$ is the unique scale that preserves $O(1)$ logit variance.
</details>

---

## Q2 · RNN vs. self-attention: complexity, path length, parallelism

Consider processing a sequence of length $T$ with hidden / model dimension $d$.

**(a)** Give the time complexity of one forward pass through (i) a single LSTM layer and (ii) a single self-attention layer.

**(b)** Give the **maximum path length** between any two tokens in each model — i.e. the minimum number of layer operations a signal must traverse to connect token $i$ to token $j$.

**(c)** Training throughput matters as much as asymptotic cost. Which of the two architectures can be parallelised across the time dimension during training, and why can the other one fundamentally *not*?

**(d)** For what regime of $T$ and $d$ is self-attention cheaper than an LSTM in raw FLOPs, ignoring parallelism?

<details>
<summary><b>▸ Model Answer · Q2</b></summary>

**(a)** LSTM per step: four $O(d^2)$ gate matmuls (or one fused $O(d^2)$ matmul on concatenated input), repeated for $T$ steps → $O(Td^2)$. Self-attention: $QK^{\top}$ and the attention-weighted sum of $V$ cost $O(T^2 d)$; the $Q/K/V/O$ projections cost $O(Td^2)$. Total $O(T^2 d + Td^2)$.

**(b)** LSTM: $O(T)$ — information from token $1$ reaches token $T$ only by traversing $T-1$ recurrent steps, even if the forget gates let the gradient through. Self-attention: $O(1)$ — every token attends to every other token in a *single* layer.

**(c)** Self-attention can be fully parallelised over the time axis during training: the representation at position $t$ does **not** depend on the representation at position $t-1$ — all $T$ positions are computed from the same input tensor in a handful of large matmuls. The LSTM hidden / cell state satisfies $(h_t, c_t) = f(h_{t-1}, c_{t-1}, x_t)$, so computing step $t$ needs step $t-1$ to already be done. The recurrence is inherently sequential and cannot be unrolled on a GPU, no matter how many cores you have.

**(d)** Comparing the dominant terms, self-attention is cheaper in raw FLOPs when $T^2 d < T d^2$, i.e. when $T < d$. In practice modern Transformers run with $T \sim d$ or $T > d$, so Transformers win on **path length and parallelism**, not on asymptotic FLOPs — which is the important take-away.

**Key points:**
- Sequential dependence is the hard blocker for LSTM parallelism, not FLOPs.
- $O(1)$ path length is why attention models long-range dependencies so well.
- Asymptotic FLOPs and wall-clock throughput can disagree; GPU parallelism decides.
</details>

---

## Q3 · Permutation equivariance and positional encoding

Let $\mathrm{Attn}(X)$ denote self-attention applied to a sequence $X \in \mathbb{R}^{T\times d}$, with $Q = XW^Q$, $K = XW^K$, $V = XW^V$. Let $P \in \mathbb{R}^{T\times T}$ be any permutation matrix.

**(a)** Prove that $\mathrm{Attn}(PX) = P\,\mathrm{Attn}(X)$. (I.e., self-attention is **permutation-equivariant** over tokens.)

**(b)** A classmate argues:
> *"Since self-attention is permutation-equivariant, a Transformer cannot distinguish 'dog bites man' from 'man bites dog'. Adding positional encodings to the input embeddings fixes this because the positional vectors break the symmetry."*

Is the classmate's **conclusion** correct? Is the **reasoning** rigorous? If not, what is the subtle gap?

**(c)** In Week 5 (CNN) we relied on translation equivariance, and in Week 6 (GNN) we relied on permutation equivariance over nodes, as *desirable* inductive biases. For sequence modelling, is permutation equivariance a desirable inductive bias or an obstacle? Justify in one or two sentences.

<details>
<summary><b>▸ Model Answer · Q3</b></summary>

**(a)** With $X' = PX$ we get $Q' = PXW^Q = PQ$ and similarly $K' = PK$, $V' = PV$. Then
$$Q'{K'}^{\top} = PQK^{\top}P^{\top}.$$
Softmax is applied **row-wise**, and row permutation commutes with any row-wise function, so
$$\mathrm{softmax}\!\left(\tfrac{Q'{K'}^{\top}}{\sqrt{d_k}}\right) = P\,\mathrm{softmax}\!\left(\tfrac{QK^{\top}}{\sqrt{d_k}}\right)P^{\top}.$$
Multiplying by $V' = PV$ and using $P^{\top}P = I$:
$$\mathrm{Attn}(PX) = P\,\mathrm{softmax}(\cdots)P^{\top}PV = P\,\mathrm{softmax}(\cdots)V = P\,\mathrm{Attn}(X). \qquad \blacksquare$$

**(b)** **Conclusion correct, reasoning loose.** The conclusion that a vanilla Transformer cannot distinguish the two sentences is right. But "adding positional encodings breaks the symmetry" is not automatic. The symmetry is only broken because positional encodings are a **fixed reference frame**: $\mathrm{PE}$ depends on position index, not on token identity, and is **not** permuted along with the tokens. If you permuted $\mathrm{PE}$ together with $X$ (i.e., treated $\mathrm{PE}$ as part of the token features), you would end up with $\mathrm{Attn}(P(X+\mathrm{PE})) = P\,\mathrm{Attn}(X+\mathrm{PE})$ by part (a), and the problem would reappear. The gap in the classmate's argument is that they did not explain *why* $\mathrm{PE}$ is not permuted — that is the actual symmetry-breaking step.

**(c)** It is an **obstacle**. In sequence data (language, time series) the *order* is meaningful — "dog bites man" ≠ "man bites dog" — so a good sequence model must be position-*sensitive*. This is the opposite of GNNs, where node labels are arbitrary and permutation equivariance is exactly what we want, and different from CNNs, where translation equivariance holds because pixel coordinates lie in a metric space with meaningful shifts. Positional encoding exists precisely to cancel the symmetry that self-attention would otherwise enforce.

**Key points:**
- The proof uses only two facts: $P^{\top}P = I$ and row-wise commutation of softmax with $P$.
- "Breaks symmetry" needs to be spelled out — PE is a *fixed* frame, not a feature permuted with the tokens.
- CNN / GNN / Transformer inductive biases each match a specific symmetry group (translations, node permutations, *none* over sequence positions respectively).
</details>

---
## Summary

| Section | Key concept |
|---|---|
| **§1** | Vanilla RNN recurrence $h_t = \tanh(W_{xh}x_t + W_{hh}h_{t-1} + b)$; gradient is a Jacobian product $\Rightarrow$ vanishing / exploding |
| **§2** | LSTM gates + additive cell update $c_t = f_t\odot c_{t-1} + i_t\odot\tilde c_t$; long-range gradient $= \prod_t f_t$, learnable $\approx 1$ |
| **§3** | Self-attention $\mathrm{softmax}(QK^{\top}/\sqrt{d_k})V$; $O(1)$ path length, fully parallel; multi-head runs $h$ projections in parallel |
| **§3.3** | Positional encoding breaks the permutation symmetry of self-attention |

**Take-aways:**
- Vanilla RNNs fail on long range because of *multiplicative* gradient flow; LSTMs fix it with an *additive* cell state.
- Transformers go further: they drop recurrence entirely, trading sequential memory for direct all-pairs interactions and full GPU parallelism.
- Every architectural choice in Part B (four gates, $\sqrt{d_k}$ scaling, head splitting, output projection) maps directly onto a specific failure mode of the alternative — you should be able to *justify* each line, not just write it.

