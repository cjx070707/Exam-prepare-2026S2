# W7 — Exam-style Questions
**来源：Week7_Self_Study.ipynb § 8（官方原题，未改动）**

> [!danger] 备考优先级：必考

---

## Q1 — Why $\sqrt{d_k}$?
*(Week 3 connection: softmax / gradient flow)*

Scaled dot-product attention computes

$$\text{Attn}(Q, K, V) = \mathrm{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V.$$

Suppose the entries of $Q$ and $K$ are i.i.d. with zero mean and unit variance.

**(a)** Show that each entry of $Q K^\top$ has variance $d_k$.

**(b)** Explain what happens to the output of the softmax as $d_k \to \infty$ **without** the $\sqrt{d_k}$ scaling.

**(c)** Using what you know about the softmax Jacobian, explain why this is a problem for gradient-based training, and argue why dividing by $\sqrt{d_k}$ — as opposed to $d_k$ or $1$ — is the right fix.

> [!note]- Answer sketch — Q1
> **(a)** Let $q, k \in \mathbb{R}^{d_k}$ be a query/key pair. Their inner product is $\langle q, k \rangle = \sum_{i=1}^{d_k} q_i k_i$. Each $q_i k_i$ has mean $\mathbb{E}[q_i]\mathbb{E}[k_i] = 0$ and variance $\mathrm{Var}(q_i)\mathrm{Var}(k_i) = 1$, and the terms are independent. Therefore $\mathrm{Var}(\langle q, k \rangle) = d_k$ and the standard deviation grows like $\sqrt{d_k}$.
>
> **(b)** Without scaling, the logits fed into softmax have magnitude on the order of $\sqrt{d_k}$. For large $d_k$, the largest logit dominates and the softmax output concentrates on a single position — it approaches a one-hot distribution.
>
> **(c)** The Jacobian of softmax is $J_{ij} = p_i(\delta_{ij} - p_j)$. When the output is near one-hot ($p \approx e_{i^\star}$), every entry of $J$ is near zero, so **gradients vanish into $Q$ and $K$**. The fix needs to keep the *variance* of the logits at $O(1)$, which is exactly what dividing by $\sqrt{d_k}$ achieves. Dividing by $d_k$ instead would shrink the standard deviation to $1/\sqrt{d_k} \to 0$, over-flattening the softmax and destroying the model's ability to *select* anything — the opposite failure mode.

---

## Q2 — RNN vs. self-attention: FLOPs, path length, parallelism
*(Week 5 connection: complexity analysis)*

Consider processing a sequence of length $T$ with hidden/model dimension $d$.

**(a)** Give the time complexity of one forward pass through (i) a single vanilla RNN layer and (ii) a single self-attention layer.

**(b)** Give the **maximum path length** between any two tokens in each model.

**(c)** Which of the two architectures can be parallelised across the time dimension during training, and why does the other fundamentally cannot?

**(d)** For what regime of $T$ and $d$ is self-attention cheaper than an RNN in raw FLOPs?

> [!note]- Answer sketch — Q2
> **(a)** RNN per step: one matmul of size $O(d^2)$, repeated for $T$ steps → $O(T d^2)$. Self-attention: the $Q K^\top$ product and the attention-weighted sum of $V$ cost $O(T^2 d)$; the $Q/K/V/O$ projections cost $O(T d^2)$. Total: $O(T^2 d + T d^2)$.
>
> **(b)** RNN: $O(T)$ — information from token 1 reaches token $T$ only by traversing $T-1$ recurrent steps. Self-attention: $O(1)$ — every token attends directly to every other token in a single layer.
>
> **(c)** Self-attention can be fully parallelised across the time axis because the computation at position $t$ does **not** depend on the representation at position $t-1$; all $T$ positions are computed from the same input tensor. The RNN hidden state satisfies $h_t = f(h_{t-1}, x_t)$, so computing $h_t$ requires $h_{t-1}$ — the recurrence is inherently sequential.
>
> **(d)** Self-attention is cheaper when $T^2 d < T d^2$, i.e. when $T < d$. In practice Transformers win on *path length and parallelism*, not on asymptotic FLOPs.

---

## Q3 — Permutation equivariance and positional encoding
*(Week 5/6 connection: symmetry and inductive biases)*

Let $\text{Attn}(X)$ denote self-attention applied to a sequence $X \in \mathbb{R}^{T \times d}$, with $Q = X W_Q$, $K = X W_K$, $V = X W_V$. Let $P \in \mathbb{R}^{T \times T}$ be any permutation matrix.

**(a)** Prove that $\text{Attn}(P X) = P \cdot \text{Attn}(X)$. (I.e., self-attention is **permutation-equivariant**.)

**(b)** A classmate argues:
> *"Since self-attention is permutation-equivariant, a Transformer cannot distinguish 'dog bites man' from 'man bites dog'. Adding positional encodings fixes this because the positional vectors break the symmetry."*

Is the conclusion correct? Is the reasoning rigorous? If not, what is the subtle gap?

**(c)** For sequence modelling, is permutation equivariance a desirable inductive bias or an obstacle?

> [!note]- Answer sketch — Q3
> **(a)** With $X' = P X$ we get $Q' = P X W_Q = P Q$ and likewise $K' = P K$, $V' = P V$. Then
> $$Q' K'^{\top} = P Q K^\top P^\top.$$
> Softmax is applied **row-wise**, and row permutation commutes with any row-wise function, so
> $$\mathrm{softmax}\!\left(\tfrac{Q' K'^\top}{\sqrt{d_k}}\right) = P\, \mathrm{softmax}\!\left(\tfrac{Q K^\top}{\sqrt{d_k}}\right) P^\top.$$
> Multiplying by $V' = P V$ and using $P^\top P = I$:
> $$\text{Attn}(P X) = P\, \mathrm{softmax}(\cdots)\, P^\top P V = P\, \mathrm{softmax}(\cdots) V = P\, \text{Attn}(X). \quad\blacksquare$$
>
> **(b) Conclusion correct, reasoning loose.** The conclusion is right. But "adding positional encodings breaks the symmetry" is not automatic. The symmetry is only broken because PE depends on position index, not on token identity, and is **not** permuted along with the tokens. If you permuted PE together with X, you would get $\text{Attn}(P(X + \text{PE})) = P\,\text{Attn}(X + \text{PE})$ by part (a), and the problem would reappear. The gap: they did not explain *why* PE is not permuted.
>
> **(c)** It is an **obstacle**. In sequence data the *order* is meaningful — "dog bites man" ≠ "man bites dog". This is the opposite of GNNs, where permutation equivariance is desirable because node labels are arbitrary. Positional encoding exists precisely to cancel the symmetry.
