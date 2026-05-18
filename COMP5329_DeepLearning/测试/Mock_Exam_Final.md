# COMP5329 Deep Learning — Mock Final Exam

> **Instructions**: This mock exam covers all four study groups (Weeks 2–12).  
> Section A: Multiple Choice (20 pts) | Section B: Short Answer (30 pts) | Section C: Coding (25 pts) | Section D: Essay (25 pts)

---

## Section A — Multiple Choice (20 pts, 2 pts each)

---

**A1.** A 3-layer MLP (input → hidden → output) with no activation function applied to the hidden layer is equivalent to:

- (a) A 2-layer MLP with a nonlinear hidden layer
- (b) A single linear classifier
- (c) A kernel SVM
- (d) A network with half the parameters

<details>
<summary>Answer</summary>

**(b)**

$W_2(W_1 x + b_1) + b_2 = (W_2W_1)x + \text{const}$ — composition of linear maps is linear. Depth alone adds no expressive power without nonlinear activations.

</details>

---

**A2.** Which of the following is the primary reason ReLU is preferred over Sigmoid in deep networks?

- (a) ReLU outputs are zero-centred
- (b) ReLU has a bounded output range
- (c) ReLU does not saturate in the positive region, avoiding gradient vanishing
- (d) ReLU requires less memory than Sigmoid

<details>
<summary>Answer</summary>

**(c)**

For $x > 0$, $f'(x) = 1$ — gradient is constant and never vanishes. Sigmoid saturates at both ends ($f'(x) \to 0$ for $|x| \gg 0$), causing vanishing gradients in deep networks. Note: ReLU is *not* zero-centred (outputs $\geq 0$), so (a) is wrong.

</details>

---

**A3.** In Adam, bias correction divides $m_t$ by $(1 - \beta_1^t)$. What problem does this solve?

- (a) It prevents the learning rate from growing unboundedly
- (b) It corrects the underestimation of the first moment caused by zero-initialising $m_0 = 0$
- (c) It replaces the need for a separate learning rate hyperparameter
- (d) It ensures the second moment $v_t$ stays positive

<details>
<summary>Answer</summary>

**(b)**

With $m_0 = 0$ and $\beta_1 = 0.9$, at step 1: $m_1 = 0.1\,g_1$ — only 10% of the true gradient. Bias correction rescales: $\hat{m}_1 = m_1/(1-0.9) = g_1$, recovering the correct estimate. Without this, early steps are far too conservative.

</details>

---

**A4.** An input of size $32 \times 32$ passes through a conv layer with filter size $5 \times 5$, padding $= 2$, stride $= 2$. What is the output spatial size?

- (a) $28 \times 28$
- (b) $16 \times 16$
- (c) $14 \times 14$
- (d) $32 \times 32$

<details>
<summary>Answer</summary>

**(b) $16 \times 16$**

$\lfloor(32 - 5 + 2 \times 2)/2\rfloor + 1 = \lfloor 31/2 \rfloor + 1 = 15 + 1 = 16$.

</details>

---

**A5.** In Kipf & Welling's GCN, the adjacency matrix is modified to $\hat{A} = A + I$. The purpose of adding $I$ is:

- (a) To make $\hat{A}$ invertible
- (b) To include each node's own features in its aggregation
- (c) To ensure all eigenvalues of $\hat{A}$ are positive
- (d) To reduce the cost of matrix multiplication

<details>
<summary>Answer</summary>

**(b)**

Without self-loops, multiplying by $A$ aggregates only neighbours, not the node itself. Adding $I$ sets $\hat{A}_{ii} = 1$, so each node contributes its own features to its own updated representation.

</details>

---

**A6.** The vanishing gradient problem in vanilla RNNs is primarily caused by:

- (a) Using tanh, which clips activations to $(-1, 1)$
- (b) Repeatedly multiplying $\tanh'(\cdot) \cdot W_{hh}$ across time steps, producing a product typically much less than 1
- (c) The lack of a cell state to carry long-term information
- (d) Using a fixed-length context vector in the encoder

<details>
<summary>Answer</summary>

**(b)**

BPTT requires the gradient to travel from step $k$ to step 1 via $\prod_{t=2}^{k} \tanh'(\cdot) W_{hh}$. Since $\tanh' \in [0,1]$ (usually $\ll 1$), this product decays exponentially with sequence length. Option (c) is the consequence, not the mechanism.

</details>

---

**A7.** In scaled dot-product attention, scores $QK^\top$ are divided by $\sqrt{d_k}$. The best reason is:

- (a) To ensure the output has unit variance
- (b) To prevent large dot products from pushing softmax into saturation where gradients vanish
- (c) To normalise attention weights to sum to one
- (d) To reduce memory cost of the attention matrix

<details>
<summary>Answer</summary>

**(b)**

For $q, k \sim \mathcal{N}(0,1)$ with dimension $d_k$, the dot product has variance $d_k$. Without scaling, large $d_k$ produces very large logits → softmax approaches one-hot → near-zero gradients. Dividing by $\sqrt{d_k}$ restores unit variance. (Softmax already handles summing to one — that is not why we scale.)

</details>

---

**A8.** BERT uses bidirectional attention while GPT uses causal masking. Why can't BERT be used directly for autoregressive text generation?

- (a) BERT was not pre-trained on enough data
- (b) BERT's bidirectional attention allows future tokens to influence current predictions, violating the autoregressive requirement
- (c) BERT's vocabulary is too small for generation tasks
- (d) BERT does not use positional encodings

<details>
<summary>Answer</summary>

**(b)**

Autoregressive generation requires $p(x_t | x_{<t})$ — predictions must use only past tokens. BERT's full attention allows every position to attend to every other position, including future ones. Generating token-by-token with BERT would create a circular dependency where earlier predictions depend on later ones that haven't been generated yet.

</details>

---

**A9.** In LoRA, the weight update $\Delta W = BA$ initialises $B = 0$. The reason is:

- (a) To ensure $A$ dominates at the start of training
- (b) So that $\Delta W = 0$ at initialisation, preserving the exact pretrained model state
- (c) To prevent the rank from growing beyond $r$ during training
- (d) To make the gradient of $A$ zero initially

<details>
<summary>Answer</summary>

**(b)**

At initialisation $\Delta W = B \cdot A = 0 \cdot A = 0$, so the model is identical to the original pretrained model. Fine-tuning then starts from the exact pretrained checkpoint rather than a perturbed state.

</details>

---

**A10.** Which self-supervised learning method does NOT require negative samples?

- (a) SimCLR
- (b) MoCo
- (c) BYOL
- (d) CLIP

<details>
<summary>Answer</summary>

**(c) BYOL**

BYOL uses a teacher-student architecture with stop-gradient on the teacher. The asymmetry (stop-gradient + predictor head on the student side only) prevents representational collapse without needing negative pairs. SimCLR uses in-batch negatives; MoCo uses a queue of negatives; CLIP uses cross-modal negatives.

</details>

---

## Section B — Short Answer (30 pts)

---

**B1. (6 pts)** Explain the difference between Batch Normalisation (BN) and Layer Normalisation (LN). State: (i) which dimensions each normalises over, (ii) whether each depends on batch size, and (iii) why Transformers use LN rather than BN.

<details>
<summary>Answer</summary>

**(i) Normalisation dimensions:**
- **BN**: normalises over $(N, H, W)$ — across the batch and spatial dimensions — independently per channel $C$. Statistics are shared across all samples in a batch.
- **LN**: normalises over $(C, H, W)$ — across all feature dimensions — independently per sample $N$. Each sample uses only its own statistics.

**(ii) Batch size dependence:**
- BN: yes. Small batches → noisy, unreliable statistics. Also requires different behaviour (batch vs running stats) at train vs test time.
- LN: no. Each sample is normalised using only its own features; behaviour is identical at train and test time.

**(iii) Why Transformers use LN:**
NLP tasks have variable sequence lengths and are often trained with small effective batch sizes per device. BN statistics over a batch of variable-length sequences are poorly defined. LN normalises per token, handling variable lengths naturally and with no train/test discrepancy.

</details>

---

**B2. (6 pts)** Describe the three-component architecture of a Multimodal Large Language Model (MLLM). For each component, state its role and give one concrete example.

<details>
<summary>Answer</summary>

| Component | Role | Example |
|-----------|------|---------|
| **Vision Encoder** | Converts the raw image into a sequence of visual feature vectors (one per patch) | CLIP-ViT: pretrained on 400M image-text pairs; outputs patch embeddings aligned with language |
| **Connector Module** | Bridges visual features and the LLM's token space — translates patch features into tokens the LLM can process | Q-Former (BLIP-2): 32 learnable query vectors compress visual features via cross-attention; MLP projection (LLaVA) is a simpler linear alternative |
| **Language Model** | Frozen or LoRA fine-tuned decoder-only Transformer that processes the concatenated visual + text token sequence | LLaMA, Vicuna — handles both modalities jointly |

</details>

---

**B3. (8 pts)** Write the InfoNCE loss and answer: (i) what does $\tau$ control? (ii) Using the gradient w.r.t. $q$, explain why hard negatives receive larger weight. (iii) State one key difference between SimCLR and MoCo.

<details>
<summary>Answer</summary>

$$\mathcal{L} = -\log \frac{\exp(q \cdot k^+ / \tau)}{\sum_{j=1}^{N} \exp(q \cdot k_j / \tau)}$$

**(i) Role of $\tau$:**
Controls the sharpness of the softmax distribution over negatives. Low $\tau$ → distribution concentrates on hardest negatives (strong signal, instability risk). High $\tau$ → uniform over all negatives (softer signal). Typical values: $0.07$–$0.2$.

**(ii) Hard negatives in the gradient:**
$$\frac{\partial \mathcal{L}}{\partial q} = -\frac{k^+}{\tau} + \frac{1}{\tau}\sum_j p_j k_j, \quad p_j = \frac{\exp(q \cdot k_j/\tau)}{\sum_{j'}\exp(q \cdot k_{j'}/\tau)}$$
Hard negatives (high $q \cdot k_j$) receive high softmax weight $p_j$. They contribute more force to push $q$ away from incorrect representations. Easy negatives (low similarity) get $p_j \approx 0$ and barely affect training.

**(iii) SimCLR vs MoCo:**
SimCLR uses all other samples in the current mini-batch as negatives — requires very large batch sizes (4096+). MoCo maintains a FIFO queue of encoded keys from past batches; the key encoder is updated via EMA ($m \approx 0.999$), so negatives are consistent without a large batch.

</details>

---

**B4. (10 pts)** (a) Write the LSTM cell state update equation. (b) Explain precisely why $\partial c_t/\partial c_{t-1}$ does not suffer exponential decay. (c) What does $f_t \approx 0$ for all steps imply?

<details>
<summary>Answer</summary>

**(a):**
$$c_t = c_{t-1} \otimes f_t + \tilde{c}_t \otimes i_t$$
where $f_t = \sigma(W_f[h_{t-1};x_t])$, $i_t = \sigma(W_i[h_{t-1};x_t])$, $\tilde{c}_t = \tanh(W_c[h_{t-1};x_t])$.

**(b):** The dominant term of the gradient is:
$$\frac{\partial c_t}{\partial c_{t-1}} \approx f_t$$
The gradient is multiplied by $f_t$ at each step — but $f_t$ is a **learnable gate**. The network can train $f_t \approx 1$ for tasks requiring long-term memory, keeping $\prod_t f_t \approx 1$ so gradients flow back across many steps without decay.

In a vanilla RNN the corresponding factor is $\tanh'(\text{net}_t) \cdot W_{hh}$. $\tanh'$ is at most 1 (typically much less) and fixed — not learnable — so the product over $k$ steps decays exponentially. The key distinction is not addition vs multiplication but that LSTM's gradient factor is *learned* while RNN's is not.

**(c):** When $f_t \approx 0$, $c_t \approx \tilde{c}_t \otimes i_t$ — the previous cell state is almost completely erased every step. The network has no long-term memory; each step processes only the current input. This is appropriate when history is irrelevant but catastrophic for long-range dependencies.

</details>

---

## Section C — Coding (25 pts)

---

**C1. (10 pts)** Implement scaled dot-product attention from scratch (no `nn.MultiheadAttention`).

```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: (B, N, d_k)
    K: (B, N, d_k)
    V: (B, N, d_v)
    mask: (B, N, N) bool — True = masked (set to -inf)
    Returns: output (B, N, d_v), attention_weights (B, N, N)
    """
    pass
```

<details>
<summary>Answer</summary>

```python
import math, torch

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]

    # Scaled similarity  (B, N, N)
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)

    # Apply mask: -inf → 0 after softmax
    if mask is not None:
        scores = scores.masked_fill(mask, float('-inf'))

    weights = torch.softmax(scores, dim=-1)   # (B, N, N)
    output  = weights @ V                      # (B, N, d_v)

    return output, weights
```

**Key points:** `K.transpose(-2, -1)` works on batched tensors; `.T` does not. `masked_fill` with `-inf` produces exactly 0 after softmax.

</details>

---

**C2. (10 pts)** Implement a single LSTM time step from scratch.

```python
def lstm_step(x_t, h_prev, c_prev, W_f, W_i, W_o, W_c, b_f, b_i, b_o, b_c):
    """
    x_t:    (B, input_size)
    h_prev: (B, hidden_size)
    c_prev: (B, hidden_size)
    W_*: (input_size + hidden_size, hidden_size),  b_*: (hidden_size,)
    Returns: h_t, c_t  both (B, hidden_size)
    """
    pass
```

<details>
<summary>Answer</summary>

```python
def lstm_step(x_t, h_prev, c_prev, W_f, W_i, W_o, W_c, b_f, b_i, b_o, b_c):
    combined = torch.cat([h_prev, x_t], dim=-1)   # (B, hidden+input)

    f_t     = torch.sigmoid(combined @ W_f + b_f)  # forget gate
    i_t     = torch.sigmoid(combined @ W_i + b_i)  # input gate
    o_t     = torch.sigmoid(combined @ W_o + b_o)  # output gate
    c_tilde = torch.tanh(combined @ W_c + b_c)     # candidate cell

    c_t = c_prev * f_t + c_tilde * i_t             # cell state update
    h_t = o_t * torch.tanh(c_t)                    # hidden state

    return h_t, c_t
```

**Key points:** Three gates use sigmoid; candidate uses tanh. Cell state is updated additively (`c_prev * f_t + c_tilde * i_t`).

</details>

---

**C3. (5 pts)** Implement VAE reparameterisation and KL loss.

```python
def reparameterize(mu, log_var):
    # Returns z ~ N(mu, exp(log_var)), differentiable w.r.t. mu, log_var
    pass

def kl_loss(mu, log_var):
    # Closed-form KL(N(mu, sigma^2) || N(0, I))
    pass
```

<details>
<summary>Answer</summary>

```python
def reparameterize(mu, log_var):
    std = torch.exp(0.5 * log_var)
    eps = torch.randn_like(std)       # randomness isolated in eps
    return mu + std * eps             # gradient flows through mu and std

def kl_loss(mu, log_var):
    # KL = 0.5 * sum(exp(log_var) + mu^2 - 1 - log_var)
    return 0.5 * torch.sum(torch.exp(log_var) + mu**2 - 1 - log_var)
```

**Why reparameterisation:** Sampling $z \sim \mathcal{N}(\mu, \sigma^2)$ directly is non-differentiable. Writing $z = \mu + \sigma \cdot \epsilon$ moves stochasticity into $\epsilon$ (no parameters), letting gradients flow through $\mu$ and $\sigma$.

</details>

---

## Section D — Essay (25 pts)

---

**D1. (12 pts)** Compare CNNs and Vision Transformers (ViT) for image classification. Cover: inductive biases, small- vs large-dataset performance, computational complexity, and one ViT design choice that compensates for lacking spatial bias.

<details>
<summary>Answer</summary>

**Inductive biases:**

CNNs hard-code two priors:
- *Locality*: each neuron connects only to a small receptive field — nearby pixels are treated as more related.
- *Translation equivariance*: the same filter is used at every spatial position (weight sharing), so a pattern detected anywhere produces the same response.

ViT encodes **no spatial inductive bias**. Images are split into patches, each treated as a sequence token. Self-attention is permutation-equivariant — the network must learn all spatial relationships from data.

---

**Small- vs large-dataset performance:**

On small datasets, CNNs outperform ViT. CNN's built-in locality and equivariance act as strong regularisers; fewer examples are needed to generalise. ViT without prior spatial knowledge overfits more easily.

On large datasets (JFT-300M, ImageNet-21k), ViT matches or surpasses CNNs. With sufficient data it learns powerful global relationships between distant patches — something CNNs only approximate through many stacked layers. ViT also scales more favourably with compute.

---

**Computational complexity:**

| | CNN | ViT |
|---|---|---|
| Per layer | $O(N \cdot F^2 \cdot C^2)$, linear in image size | $O(T^2 \cdot D)$, quadratic in patch count $T$ |
| Resolution scaling | Linear | Quadratic |

For high-resolution inputs, ViT's $O(T^2)$ attention is expensive. Efficient variants (Swin Transformer, local windows) reduce this to linear.

---

**Compensating for lack of spatial bias — Learned Positional Embeddings:**

Without positional encoding, self-attention is permutation-invariant and cannot distinguish patch location. ViT prepends a learnable positional embedding $p_i \in \mathbb{R}^D$ to each patch token before the encoder. The network learns from data that positional embeddings correlate with spatial structure. This is less constrained than CNN's hard-wired locality — hence the larger data requirement — but also more flexible, enabling non-local and non-Euclidean spatial relationships that CNNs cannot easily model.

</details>

---

**D2. (13 pts)** GAN training is notoriously unstable. Explain the root cause and how WGAN addresses it. Include: minimax objective, optimal discriminator, generator gradient issue with disjoint supports, Wasserstein-1 distance, and Lipschitz enforcement.

<details>
<summary>Answer</summary>

**GAN minimax objective:**
$$\min_G \max_D \;\mathbb{E}_{x \sim p_r}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1-D(G(z)))]$$

---

**Optimal discriminator:**

For fixed $G$, the integrand at each $x$ is $p_r(x)\log D(x) + p_g(x)\log(1-D(x))$. Setting the derivative to zero:
$$D^*(x) = \frac{p_r(x)}{p_r(x) + p_g(x)}$$

---

**Generator gradient with disjoint supports:**

Substituting $D^*$ yields $\mathcal{L}(G, D^*) = 2\,\text{JS}(p_r \| p_g) - 2\log 2$.

In high dimensions, $p_r$ and $p_g$ typically lie on low-dimensional manifolds with disjoint support. JS divergence then equals $\log 2$ regardless of how close the two distributions actually are — the loss is flat and $\nabla_G \mathcal{L} \approx 0$. A well-trained discriminator kills the generator's learning signal entirely.

---

**Wasserstein-1 distance:**
$$W(p_r, p_g) = \sup_{\|f\|_L \leq 1}\;\mathbb{E}_{x \sim p_r}[f(x)] - \mathbb{E}_{x \sim p_g}[f(x)]$$

Unlike JS divergence, $W$ is well-defined and provides a smooth, non-zero gradient **even when the two distributions have disjoint support**. It measures the minimum "work" (mass × distance) to transport $p_g$ onto $p_r$, which always varies continuously with the generator's parameters.

---

**Lipschitz constraint and enforcement:**

The supremum is over 1-Lipschitz functions $f$ ($\|\nabla f\|_2 \leq 1$ everywhere). In practice a neural network "critic" $f_w$ approximates this.

1. **Weight clipping** (original WGAN): clip all critic weights to $[-c, c]$ after each update. Simple but limits capacity and causes slow convergence.
2. **Gradient penalty** (WGAN-GP, preferred): add $\lambda\,\mathbb{E}_{\hat{x}}[(\|\nabla_{\hat{x}} f_w(\hat{x})\|_2 - 1)^2]$ where $\hat{x}$ are sampled along linear interpolations between real and generated pairs. Differentiable and empirically more stable.

The WGAN critic loss (maximised): $\mathbb{E}_{p_r}[f_w(x)] - \mathbb{E}_{p_z}[f_w(G(z))]$

Because $W$ varies continuously with generator parameters, the generator always receives a meaningful, non-vanishing gradient signal — resolving the original instability.

</details>
