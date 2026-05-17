# COMP5329 Deep Learning — Mock Final Exam

> **Instructions**: This mock exam covers all four study groups. Attempt all sections.  
> Section A: Multiple Choice (20 pts) | Section B: Short Answer (30 pts) | Section C: Coding (25 pts) | Section D: Essay (25 pts)  
> Model answers are at the bottom — attempt each section before checking.

---

## Section A — Multiple Choice (20 pts, 2 pts each)

**Circle the single best answer.**

---

**A1.** A 3-layer MLP (input → hidden → output) with no activation functions applied to the hidden layer is equivalent to:

- (a) A 2-layer MLP with a nonlinear hidden layer  
- (b) A single linear classifier  
- (c) A kernel SVM  
- (d) A network with half the parameters  

---

**A2.** Which of the following is the primary reason ReLU is preferred over Sigmoid in deep networks?

- (a) ReLU outputs are zero-centred  
- (b) ReLU has a bounded output range  
- (c) ReLU does not saturate in the positive region, avoiding gradient vanishing  
- (d) ReLU requires less memory than Sigmoid  

---

**A3.** In Adam optimiser, bias correction divides $m_t$ by $(1 - \beta_1^t)$. What problem does this solve?

- (a) It prevents the learning rate from growing unboundedly  
- (b) It corrects the underestimation of the first moment caused by zero initialisation of $m_0$  
- (c) It replaces the need for a separate learning rate hyperparameter  
- (d) It ensures the second moment $v_t$ remains positive  

---

**A4.** An input of size $32 \times 32$ is passed through a convolutional layer with filter size $5 \times 5$, padding $= 2$, stride $= 2$. What is the output spatial size?

- (a) $28 \times 28$  
- (b) $16 \times 16$  
- (c) $14 \times 14$  
- (d) $32 \times 32$  

---

**A5.** In Kipf & Welling's GCN, the adjacency matrix $A$ is modified to $\hat{A} = A + I$ before symmetric normalisation. The purpose of adding the identity matrix $I$ is:

- (a) To make $\hat{A}$ invertible  
- (b) To include each node's own features in its aggregation  
- (c) To ensure all eigenvalues of $\hat{A}$ are positive  
- (d) To reduce the computational cost of matrix multiplication  

---

**A6.** The vanishing gradient problem in vanilla RNNs is primarily caused by:

- (a) Using tanh activation, which clips activations to $(-1, 1)$  
- (b) The repeated multiplication of $\tanh'(\cdot) \cdot W_{hh}$ across time steps, which is typically much less than 1  
- (c) The lack of a cell state to carry long-term information  
- (d) The use of a fixed-length context vector in the encoder  

---

**A7.** In scaled dot-product attention, the scores $QK^\top$ are divided by $\sqrt{d_k}$. Which statement best explains why?

- (a) To ensure the output has unit variance  
- (b) To prevent large dot products from pushing softmax into saturation regions where gradients vanish  
- (c) To normalise the attention weights so they sum to one  
- (d) To reduce the memory cost of computing the attention matrix  

---

**A8.** BERT uses bidirectional attention while GPT uses causal (lower-triangular) masking. Which of the following best explains why BERT cannot directly be used for autoregressive text generation?

- (a) BERT was not pre-trained on enough data  
- (b) BERT's bidirectional attention allows future tokens to influence the prediction, violating the autoregressive requirement  
- (c) BERT's vocabulary is too small for generation tasks  
- (d) BERT does not use positional encodings  

---

**A9.** In LoRA, the weight update is parameterised as $\Delta W = BA$ where $B \in \mathbb{R}^{d \times r}$ and $A \in \mathbb{R}^{r \times k}$, with $r \ll \min(d, k)$. $B$ is initialised to zero. What is the reason for this initialisation?

- (a) To ensure $A$ dominates at the start of training  
- (b) So that at initialisation $\Delta W = 0$, preserving the exact pretrained model state  
- (c) To prevent the rank from growing beyond $r$ during training  
- (d) To make the gradient with respect to $A$ equal to zero initially  

---

**A10.** Which of the following self-supervised methods does NOT require negative samples?

- (a) SimCLR  
- (b) MoCo  
- (c) BYOL  
- (d) CLIP  

---

## Section B — Short Answer (30 pts)

*Write your answers in clear English. Be precise — vague answers will not receive full marks.*

---

**B1. (6 pts)** Explain the difference between Batch Normalisation (BN) and Layer Normalisation (LN).

In your answer, state:  
(i) which dimensions each method normalises over,  
(ii) whether each method depends on batch size, and  
(iii) why Transformers use LN rather than BN.

---

**B2. (6 pts)** Describe the three-component architecture of a Multimodal Large Language Model (MLLM).

For each component, name it, state its role, and give one concrete example (e.g. a specific model or design choice).

---

**B3. (8 pts)** Write out the InfoNCE loss function and answer the following:

(i) What role does the temperature parameter $\tau$ play?  
(ii) Show, using the gradient of InfoNCE with respect to $q$, why the loss places larger weight on **hard negatives** (negatives that are similar to the query).  
(iii) State one difference between SimCLR and MoCo in how they source negative samples.

---

**B4. (10 pts)** Consider the following questions about LSTM and the vanishing gradient problem.

(a) Write out the cell state update equation for an LSTM.  
(b) Using the equation from (a), explain why the gradient $\partial c_t / \partial c_{t-1}$ does not suffer from the same exponential decay as in a vanilla RNN. Be precise about what makes the difference.  
(c) The forget gate $f_t$ uses a sigmoid activation. If $f_t \approx 0$ for all time steps, what does this imply about the network's behaviour and its ability to retain long-term information?

---

## Section C — Coding (25 pts)

*Write clean, correct Python/PyTorch code. You may use standard library functions (torch.softmax, F.mse_loss, etc.). Comments are encouraged but not required.*

---

**C1. (10 pts)** Implement scaled dot-product attention **from scratch** (without using `nn.MultiheadAttention`).

Your function signature:

```python
def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: (B, N, d_k)
    K: (B, N, d_k)
    V: (B, N, d_v)
    mask: (B, N, N) boolean tensor, True = position is masked (set to -inf)
    Returns: output (B, N, d_v), attention_weights (B, N, N)
    """
```

Requirements:
- Compute the scaled scores
- Apply the mask if provided
- Return both the output and the attention weights

---

**C2. (10 pts)** Implement a single LSTM time step from scratch.

Your function signature:

```python
def lstm_step(x_t, h_prev, c_prev, W_f, W_i, W_o, W_c, b_f, b_i, b_o, b_c):
    """
    x_t:    (B, input_size)
    h_prev: (B, hidden_size)
    c_prev: (B, hidden_size)
    W_f, W_i, W_o, W_c: (input_size + hidden_size, hidden_size)
    b_f, b_i, b_o, b_c: (hidden_size,)
    Returns: h_t (B, hidden_size), c_t (B, hidden_size)
    """
```

---

**C3. (5 pts)** Implement the VAE reparameterisation trick and the KL divergence term of the ELBO loss.

```python
def reparameterize(mu, log_var):
    # mu, log_var: (B, latent_dim)
    # Returns z: (B, latent_dim) sampled from N(mu, exp(log_var))
    pass

def kl_loss(mu, log_var):
    # Returns scalar KL divergence: KL(N(mu, sigma^2) || N(0, I))
    # Use the closed-form solution
    pass
```

---

## Section D — Essay (25 pts)

*Write structured, technical responses. Use equations where helpful. Each question is marked on accuracy, depth, and clarity.*

---

**D1. (12 pts)** Compare CNNs and Vision Transformers (ViT) for image classification.

Your answer should cover:
- The inductive biases each architecture encodes (or does not encode)
- Why ViT underperforms CNNs on small datasets but often surpasses them on large datasets
- The computational complexity trade-offs (attention vs convolution)
- One concrete design choice in ViT that compensates for the lack of spatial inductive bias

---

**D2. (13 pts)** GAN training is notoriously unstable. Explain the root cause of this instability and how WGAN addresses it.

Your answer should include:
- The original GAN minimax objective
- The optimal discriminator $D^*(x)$ (derive or state with justification)
- What happens to the generator's gradient when the discriminator is near-optimal and the two distributions have disjoint support
- The Wasserstein-1 distance and why it provides a more stable training signal
- The Lipschitz constraint in WGAN and how it is enforced in practice

---

---

# Model Answers

---

## Section A — Answers

| Q | Answer | Key reason |
|---|--------|-----------|
| A1 | **(b)** | Linear ∘ Linear = Linear; the hidden layer adds no expressive power |
| A2 | **(c)** | Positive region gradient = 1, no saturation, no vanishing |
| A3 | **(b)** | $m_0 = 0$ biases early estimates low; correction factor $1/(1-\beta_1^t) > 1$ compensates |
| A4 | **(b)** | $(32 - 5 + 2 \times 2)/2 + 1 = 16$ |
| A5 | **(b)** | Without $I$, $AH$ only aggregates neighbours; $\hat{A} = A+I$ adds the node itself |
| A6 | **(b)** | BPTT multiplies $\tanh'(\cdot) W_{hh}$ at each step; this product is typically $\ll 1$, causing exponential decay |
| A7 | **(b)** | Large $d_k$ → large dot products → softmax saturates → near-zero gradients |
| A8 | **(b)** | Autoregressive generation requires position $i$ to depend only on $j < i$; BERT's full attention violates this |
| A9 | **(b)** | $\Delta W = BA = 0$ at init; fine-tuning starts exactly from the pretrained checkpoint |
| A10 | **(c)** | BYOL uses stop-gradient + predictor asymmetry to avoid collapse without negatives |

---

## Section B — Model Answers

### B1 — BN vs LN

**(i) Normalisation dimensions:**

- **Batch Norm**: normalises over the batch and spatial dimensions $(N, H, W)$ for each channel $C$ independently. Statistics ($\mu$, $\sigma^2$) are shared across samples in a batch.
- **Layer Norm**: normalises over the feature dimensions $(C, H, W)$ for each sample $N$ independently. Statistics are computed per sample.

**(ii) Dependence on batch size:**

- BN depends on batch size. With small batches, the per-channel statistics are noisy and unreliable.
- LN does not depend on batch size. Each sample is normalised using only its own features.

**(iii) Why Transformers use LN:**

In NLP, sequences vary in length and batch sizes are often small. BN statistics would be unreliable across variable-length sequences. LN computes statistics independently per token (per sample), making it well-suited to sequential data and small-batch settings. Additionally, LN's training and inference behaviour are identical, whereas BN must switch between batch and running statistics at test time.

---

### B2 — MLLM Three-Component Architecture

| Component | Role | Example |
|-----------|------|---------|
| **Vision Encoder** | Converts the raw image into a sequence of visual feature vectors | CLIP-ViT: pretrained on image-text pairs, produces patch-level embeddings aligned with language |
| **Connector Module** | Bridges visual features and the language model's token space — translates vision features into tokens the LLM can process | Q-Former (BLIP-2): 32 learnable query vectors attend to visual features via cross-attention, compressing them to a fixed-length token sequence; or MLP projection (LLaVA) for direct linear mapping |
| **Language Model** | Processes the combined sequence of visual tokens and text tokens to generate output | A frozen or LoRA-finetuned decoder-only Transformer (e.g. LLaMA, Vicuna) |

The key design challenge is the connector: it must compress and translate visual information efficiently without losing semantic content.

---

### B3 — InfoNCE Loss

**Loss function:**

$$\mathcal{L}_\text{InfoNCE} = -\log \frac{\exp(q \cdot k^+ / \tau)}{\sum_{j=1}^{N} \exp(q \cdot k_j / \tau)}$$

where $q$ is the query, $k^+$ is the positive key, and $k_j$ ranges over all keys (positive + negatives).

**(i) Role of temperature $\tau$:**

$\tau$ controls the sharpness of the distribution over negatives. Low $\tau$ → the distribution concentrates on the highest-scoring negatives (harder training signal, but risk of instability). High $\tau$ → the distribution is more uniform, treating all negatives equally (softer signal, easier to train but less informative).

**(ii) Hard negative weighting:**

The gradient with respect to $q$ is:

$$\frac{\partial \mathcal{L}}{\partial q} = -\frac{1}{\tau} k^+ + \frac{1}{\tau} \sum_j p_j k_j, \quad p_j = \frac{\exp(q \cdot k_j / \tau)}{\sum_{j'} \exp(q \cdot k_{j'} / \tau)}$$

The weight $p_j$ is the softmax probability assigned to key $j$. Keys with high similarity to $q$ receive higher $p_j$. These are precisely the **hard negatives** — they are most confused with the positive. The gradient pushes $q$ away from them with proportionally larger force. Easy negatives (low similarity) get low $p_j$ and contribute little.

**(iii) SimCLR vs MoCo:**

- **SimCLR**: negatives are all other samples within the current mini-batch. Requires a very large batch size (e.g., 4096) to have enough negatives.
- **MoCo**: maintains a separate FIFO queue of encoded keys from past mini-batches. The key encoder is updated via momentum ($\theta_k \leftarrow m\theta_k + (1-m)\theta_q$), so queue keys are consistent without needing a large batch.

---

### B4 — LSTM and Gradient Flow

**(a) Cell state update:**

$$c_t = c_{t-1} \otimes f_t + \tilde{c}_t \otimes i_t$$

where $f_t = \sigma(W_f [h_{t-1}; x_t])$, $i_t = \sigma(W_i [h_{t-1}; x_t])$, $\tilde{c}_t = \tanh(W_c [h_{t-1}; x_t])$.

**(b) Why LSTM does not suffer the same exponential decay:**

From the cell state update, the gradient of $c_t$ with respect to $c_{t-1}$ is approximately:

$$\frac{\partial c_t}{\partial c_{t-1}} \approx f_t$$

(This ignores secondary paths through $f_t$'s own dependence on $h_{t-1}$, which depends on $c_{t-1}$, but the dominant term is $f_t$.)

In a vanilla RNN, the corresponding factor is $\tanh'(\text{net}_t) \cdot W_{hh}$. Since $\tanh' \leq 1$ and is typically much smaller, and since this is multiplied across all time steps, the product decays exponentially.

The crucial difference: $f_t$ is a **learnable gate** (output in $(0,1)$) that the network can train to be close to 1. When $f_t \approx 1$ across all steps, the gradient product $\prod_t f_t \approx 1$ — gradients flow without decay. The network learns to "keep the highway open" for long-range dependencies.

**(c) When $f_t \approx 0$:**

If $f_t \approx 0$ at every step, the cell state update becomes:

$$c_t \approx \tilde{c}_t \otimes i_t$$

The previous cell state $c_{t-1}$ is completely forgotten at each step. The LSTM degenerates to a memoryless model — it cannot retain any long-term information. This is equivalent to the network choosing to reset its memory at every time step, which is appropriate for inputs where history is irrelevant but would be catastrophic for tasks requiring long-range dependencies.

---

## Section C — Model Answers

### C1 — Scaled Dot-Product Attention

```python
import math
import torch

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: (B, N, d_k)
    K: (B, N, d_k)
    V: (B, N, d_v)
    mask: (B, N, N) bool tensor, True = masked out
    Returns: output (B, N, d_v), attention_weights (B, N, N)
    """
    d_k = Q.shape[-1]

    # Step 1: compute raw scores — (B, N, N)
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)

    # Step 2: apply mask (e.g. causal mask for GPT)
    if mask is not None:
        scores = scores.masked_fill(mask, float('-inf'))

    # Step 3: softmax over last dim → attention weights
    attention_weights = torch.softmax(scores, dim=-1)  # (B, N, N)

    # Step 4: weighted sum of values
    output = attention_weights @ V  # (B, N, d_v)

    return output, attention_weights
```

**Key points examiners look for:**
- Division by `sqrt(d_k)` before softmax
- `masked_fill` with `-inf` so masked positions become 0 after softmax
- `K.transpose(-2, -1)` (not `.T`, which doesn't work for batched tensors)

---

### C2 — LSTM Single Time Step

```python
def lstm_step(x_t, h_prev, c_prev, W_f, W_i, W_o, W_c, b_f, b_i, b_o, b_c):
    """
    x_t:    (B, input_size)
    h_prev: (B, hidden_size)
    c_prev: (B, hidden_size)
    W_*:    (input_size + hidden_size, hidden_size)
    b_*:    (hidden_size,)
    """
    # Concatenate h_{t-1} and x_t along feature dim
    combined = torch.cat([h_prev, x_t], dim=-1)  # (B, input_size + hidden_size)

    # Three gates — all use sigmoid (output in (0,1), acts as a valve)
    f_t = torch.sigmoid(combined @ W_f + b_f)   # forget gate
    i_t = torch.sigmoid(combined @ W_i + b_i)   # input gate
    o_t = torch.sigmoid(combined @ W_o + b_o)   # output gate

    # Candidate cell state — tanh keeps values in (-1, 1)
    c_tilde = torch.tanh(combined @ W_c + b_c)

    # Cell state update: additive structure preserves gradient highway
    c_t = c_prev * f_t + c_tilde * i_t

    # Hidden state
    h_t = o_t * torch.tanh(c_t)

    return h_t, c_t
```

**Key points:**
- All gates use `sigmoid`; candidate uses `tanh`
- Cell state is updated additively: `c_prev * f_t + c_tilde * i_t`
- `h_t = o_t * tanh(c_t)` — output gate reads from cell state

---

### C3 — VAE Reparameterisation + KL

```python
def reparameterize(mu, log_var):
    # std = exp(0.5 * log_var) = sqrt(var)
    std = torch.exp(0.5 * log_var)
    # Sample noise from N(0, I) — randomness is isolated here, not in z
    eps = torch.randn_like(std)
    # z = mu + std * eps  →  z ~ N(mu, std^2), but gradient flows through mu and log_var
    return mu + std * eps

def kl_loss(mu, log_var):
    # Closed-form KL: KL(N(mu, sigma^2) || N(0, I))
    # = 0.5 * sum(sigma^2 + mu^2 - 1 - log(sigma^2))
    # = 0.5 * sum(exp(log_var) + mu^2 - 1 - log_var)
    return 0.5 * torch.sum(torch.exp(log_var) + mu**2 - 1 - log_var)
```

**Why reparameterisation is necessary:** The sampling step $z \sim \mathcal{N}(\mu, \sigma^2)$ is not differentiable with respect to $\mu$ and $\sigma$. By writing $z = \mu + \sigma \odot \epsilon$ with $\epsilon \sim \mathcal{N}(0,I)$, the randomness is moved into $\epsilon$ (a fixed sample), and gradients can flow back through $\mu$ and $\sigma$ normally.

---

## Section D — Model Answers

### D1 — CNN vs ViT for Image Classification (12 pts)

**Inductive biases:**

CNNs encode two strong inductive biases directly into their architecture:
- *Local connectivity*: each neuron sees only a small receptive field, reflecting the assumption that nearby pixels are more informative than distant ones.
- *Translation equivariance*: the same filter is applied at every spatial position (weight sharing), so detecting a feature at one location generalises to all locations.

ViT encodes **no spatial inductive bias**. The image is split into patches, each treated as a token in a sequence. Self-attention is permutation-equivariant by default — shuffling the patches produces the same set of outputs (just reordered). The network must *learn* spatial relationships from data.

**Performance gap on small vs large datasets:**

On small datasets, CNNs generalise better because their built-in biases act as a strong regulariser — fewer examples are needed to learn that edges and textures are locally structured. ViT has no such shortcut: it must discover spatial structure from scratch, which requires far more data to avoid overfitting.

On large datasets (e.g. ImageNet-21k, JFT-300M), ViT matches or exceeds CNN performance because it has greater capacity to learn global relationships between distant patches — something CNNs approximate only indirectly through stacked layers and growing receptive fields.

**Computational complexity:**

| | CNN | ViT |
|---|---|---|
| Self-attention | Not applicable | $O(N^2 d)$ where $N$ = number of patches |
| Convolution | $O(N \cdot F^2 \cdot C_\text{in} \cdot C_\text{out})$ | Not applicable |
| Scaling with image size | Linear in pixels | Quadratic in number of patches |

For high-resolution images, ViT's $O(N^2)$ attention cost becomes prohibitive. Efficient variants (Swin Transformer, local attention) mitigate this.

**Design choice compensating for lack of spatial bias:**

ViT adds **learned positional embeddings** to each patch token before the Transformer encoder. Without positional encoding, self-attention is entirely permutation-invariant and cannot distinguish a patch in the top-left corner from one in the bottom-right. The positional embeddings give the network a learnable coordinate system — it must learn, from data, that adjacent patches tend to be spatially related.

---

### D2 — GAN Instability and WGAN (13 pts)

**Original GAN objective:**

$$\min_G \max_D \mathcal{L}(G, D) = \mathbb{E}_{x \sim p_r}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]$$

The discriminator $D$ is trained to maximise this (distinguish real from fake), while $G$ is trained to minimise it (fool $D$).

**Optimal discriminator:**

For a fixed generator $G$, the optimal discriminator can be found by maximising pointwise:

$$D^*(x) = \frac{p_r(x)}{p_r(x) + p_g(x)}$$

This is derived by treating the objective as an integral and maximising the integrand $p_r(x) \log D(x) + p_g(x) \log(1-D(x))$ pointwise with respect to $D(x)$, yielding the above ratio.

**Gradient vanishing when distributions are disjoint:**

Substituting $D^*$ back into the GAN objective yields:

$$\mathcal{L}(G, D^*) = 2\,\text{JS}(p_r \| p_g) - 2\log 2$$

In high-dimensional spaces, $p_r$ and $p_g$ are almost always supported on low-dimensional manifolds that are essentially disjoint. In this case, there exists a perfect discriminator ($D^* \approx 1$ on real data, $D^* \approx 0$ on fake data). Consequently:

$$\nabla_G \mathcal{L} \approx 0$$

The generator receives near-zero gradients and cannot improve. This is the root cause of GAN training instability: a well-trained discriminator kills the generator's learning signal.

**Wasserstein-1 distance:**

WGAN replaces the JS divergence with the Wasserstein-1 (Earth Mover's) distance:

$$W(p_r, p_g) = \sup_{\|f\|_L \leq 1} \mathbb{E}_{x \sim p_r}[f(x)] - \mathbb{E}_{x \sim p_g}[f(x)]$$

Unlike JS divergence, $W(p_r, p_g)$ is well-defined and provides a meaningful gradient **even when the two distributions have disjoint support**. Intuitively, it measures the minimum "work" required to transport mass from $p_g$ to $p_r$, which is always finite and smooth.

**Lipschitz constraint and enforcement:**

The supremum is taken over all 1-Lipschitz functions $f$ (functions with gradient norm $\leq 1$ everywhere). In practice, $f$ is parameterised by a neural network (the "critic"). Two approaches to enforce the Lipschitz constraint:

1. **Weight clipping** (original WGAN): clip all critic weights to $[-c, c]$ after each update. Simple but can limit the critic's capacity and cause slow convergence.
2. **Gradient penalty** (WGAN-GP): instead of clipping, add a penalty term $\lambda \mathbb{E}_{\hat{x}}[(\|\nabla_{\hat{x}} f(\hat{x})\|_2 - 1)^2]$ where $\hat{x}$ is sampled along linear interpolations between real and fake data. This soft constraint is differentiable and empirically more stable.

The resulting WGAN critic loss to maximise is:

$$\max_w \mathbb{E}_{x \sim p_r}[f_w(x)] - \mathbb{E}_{z \sim p_z}[f_w(G(z))]$$

Because $W$ is continuous and differentiable almost everywhere under mild conditions, the generator always receives a meaningful (non-zero) gradient signal, resolving the instability of the original GAN.

---

*End of Mock Exam*
