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
> $W_2(W_1 x+b_1)+b_2=(W_2W_1)x+\text{const}$ — composition of linear maps is linear. Depth alone adds no expressive power without nonlinear activations.

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
> For $x>0$, $f'(x)=1$ — gradient is constant and never vanishes. Sigmoid saturates at both ends ($f'(x)\to0$ for $|x|\gg0$). Note: ReLU is *not* zero-centred (outputs $\geq0$), so (a) is wrong.

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
> With $m_0=0$ and $\beta_1=0.9$, at step 1: $m_1=0.1\,g_1$ — only 10% of the true gradient. Correction: $\hat{m}_1=m_1/(1-0.9)=g_1$. Without this, early steps are far too conservative.

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
> Without self-loops, $AH$ aggregates only neighbours. Adding $I$ sets $\hat{A}_{ii}=1$, so each node includes its own features in its updated representation.

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
> BPTT requires the gradient to travel from step $k$ to step 1 via $\prod_{t=2}^k\tanh'(\cdot)W_{hh}$. Since $\tanh'\in[0,1]$ (usually $\ll1$), this product decays exponentially. Option (c) is the consequence, not the mechanism.

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
> For $q,k\sim\mathcal{N}(0,1)$ with dimension $d_k$, the dot product has variance $d_k$. Without scaling, large $d_k$ → near one-hot softmax → near-zero gradients. Dividing by $\sqrt{d_k}$ restores unit variance. (Softmax already sums to one — that is not why we scale.)

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
> Autoregressive generation requires $p(x_t|x_{<t})$ — predictions must use only past tokens. BERT's full attention lets every position attend to every other position including future ones, creating a circular dependency when generating token by token.

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
> At init $\Delta W=B\cdot A=0\cdot A=0$, so the model is identical to the original pretrained checkpoint. Fine-tuning starts from this exact state.

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
> BYOL uses a teacher-student architecture with stop-gradient on the teacher. The asymmetry (stop-gradient + predictor head on student only) prevents representational collapse without negatives. SimCLR uses in-batch negatives; MoCo uses a queue; CLIP uses cross-modal negatives.

---

## Section B — Short Answer (30 pts)

---

**B1. (6 pts)** Explain BN vs LN: (i) which dimensions each normalises over, (ii) batch size dependence, (iii) why Transformers use LN.

> [!success]- Answer
> 
> **(i) Dimensions:**
> - **BN**: normalises over $(N,H,W)$ independently per channel $C$. Statistics are shared across all samples in the batch.
> - **LN**: normalises over $(C,H,W)$ independently per sample $N$. Each sample uses only its own statistics.
> 
> **(ii) Batch size dependence:**
> - BN: yes. Small batches → noisy, unreliable statistics. Also requires different behaviour (batch vs running stats) at train vs test time.
> - LN: no. Per-sample normalisation; identical behaviour at train and test time.
> 
> **(iii) Why Transformers use LN:**
> NLP tasks have variable sequence lengths and small effective batch sizes per device. BN statistics over variable-length sequences are poorly defined. LN normalises per token, handling variable lengths naturally and with no train/test discrepancy.

---

**B2. (6 pts)** Describe the three-component MLLM architecture. For each: role and one concrete example.

> [!success]- Answer
> 
> | Component | Role | Example |
> |-----------|------|---------|
> | **Vision Encoder** | Converts image into sequence of visual feature vectors (one per patch) | CLIP-ViT: pretrained on 400M image-text pairs; patch embeddings aligned with language |
> | **Connector Module** | Bridges visual features and LLM token space | Q-Former (BLIP-2): 32 learnable queries compress visual features via cross-attention; MLP projection (LLaVA) is a simpler linear alternative |
> | **Language Model** | Frozen or LoRA fine-tuned decoder-only Transformer processing visual + text tokens | LLaMA, Vicuna — handles both modalities jointly |

---

**B3. (8 pts)** Write the InfoNCE loss. Answer: (i) role of $\tau$, (ii) why hard negatives receive larger gradient weight (show gradient), (iii) SimCLR vs MoCo difference.

> [!success]- Answer
> 
> $$\mathcal{L}=-\log\frac{\exp(q\cdot k^+/\tau)}{\sum_j\exp(q\cdot k_j/\tau)}$$
> 
> **(i) Role of $\tau$:**
> Controls sharpness of the softmax distribution over negatives. Low $\tau$ → concentrates on hardest negatives (strong signal, instability risk). High $\tau$ → uniform treatment of all negatives.
> 
> **(ii) Hard negatives in the gradient:**
> $$\frac{\partial\mathcal{L}}{\partial q}=-\frac{k^+}{\tau}+\frac{1}{\tau}\sum_j p_j k_j,\quad p_j=\frac{\exp(q\cdot k_j/\tau)}{\sum_{j'}\exp(q\cdot k_{j'}/\tau)}$$
> Hard negatives (high $q\cdot k_j$) receive high softmax weight $p_j$. They contribute more force to push $q$ away from wrong representations. Easy negatives get $p_j\approx0$ and barely affect training.
> 
> **(iii) SimCLR vs MoCo:**
> SimCLR uses all other samples in the current mini-batch as negatives — requires large batch (4096+). MoCo maintains a FIFO queue of encoded keys from past batches; key encoder updated via EMA ($m\approx0.999$), so negatives are consistent without a large batch.

---

**B4. (10 pts)** (a) Write the LSTM cell state update. (b) Explain precisely why $\partial c_t/\partial c_{t-1}$ does not decay exponentially. (c) What does $f_t\approx0$ for all steps imply?

> [!success]- Answer
> 
> **(a):**
> $$c_t=c_{t-1}\otimes f_t+\tilde{c}_t\otimes i_t$$
> where $f_t=\sigma(W_f[h_{t-1};x_t])$, $i_t=\sigma(W_i[h_{t-1};x_t])$, $\tilde{c}_t=\tanh(W_c[h_{t-1};x_t])$.
> 
> **(b):** The dominant term of the gradient is:
> $$\frac{\partial c_t}{\partial c_{t-1}}\approx f_t$$
> The gradient is multiplied by $f_t$ at each step. But $f_t$ is a **learnable gate** — the network can train $f_t\approx1$ for long-term memory tasks, keeping $\prod_t f_t\approx1$ so gradients flow without decay.
> 
> In vanilla RNN the factor is $\tanh'(\text{net}_t)\cdot W_{hh}$ — $\tanh'\leq1$ (typically $\ll1$) and not learnable, so the product decays exponentially. The key distinction: LSTM's gradient factor is *learned*; RNN's is not.
> 
> **(c):** When $f_t\approx0$, $c_t\approx\tilde{c}_t\otimes i_t$ — the previous cell state is completely erased every step. The network has no long-term memory; each step processes only the current input. Catastrophic for tasks requiring long-range dependencies.

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
> **Key points:** `K.transpose(-2,-1)` not `.T` — `.T` reverses all dims, breaks batched tensors. `masked_fill` with `-inf` → exactly 0 after softmax.

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
> **Key points:** Three gates use sigmoid; candidate uses tanh. Cell state updated additively: `c_prev * f_t + c_tilde * i_t`.

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
> **Why reparameterisation:** Sampling $z\sim\mathcal{N}(\mu,\sigma^2)$ directly is non-differentiable. Writing $z=\mu+\sigma\cdot\epsilon$ with $\epsilon\sim\mathcal{N}(0,I)$ isolates randomness in $\epsilon$ (no parameters), so gradients flow through $\mu$ and $\sigma$.

---

## Section D — Essay (25 pts)

---

**D1. (12 pts)** Compare CNNs and ViT for image classification: inductive biases, small vs large dataset performance, computational complexity, and one ViT design choice compensating for the lack of spatial bias.

> [!success]- Answer
> 
> **Inductive biases:**
> CNNs hard-code two priors: *locality* (local receptive fields) and *translation equivariance* (weight sharing). ViT encodes no spatial inductive bias — all spatial relationships must be learned from data.
> 
> **Small vs large dataset:**
> On small datasets, CNNs outperform ViT. CNN's built-in biases act as strong regularisers; fewer examples needed to generalise. ViT overfits more easily without locality priors.
> On large datasets (JFT-300M, ImageNet-21k), ViT matches or surpasses CNNs. With sufficient data it learns powerful global relationships between distant patches. ViT also scales better with compute.
> 
> **Computational complexity:**
> 
> | | CNN | ViT |
> |---|---|---|
> | Per layer | $O(N\cdot F^2\cdot C^2)$, linear in image size | $O(T^2\cdot D)$, quadratic in patch count $T$ |
> | Resolution scaling | Linear | Quadratic |
> 
> For high-resolution inputs, ViT's $O(T^2)$ attention is expensive. Efficient variants (Swin Transformer) reduce this to linear.
> 
> **Compensating design choice — Learned Positional Embeddings:**
> Without positional encoding, self-attention is permutation-invariant and cannot distinguish patch location. ViT prepends a learnable $p_i\in\mathbb{R}^D$ to each patch token before the encoder. The network learns from data that positional embeddings correlate with spatial structure. Less constrained than CNN's hard-wired locality, hence the larger data requirement — but more flexible for non-local and non-Euclidean spatial relationships.

---

**D2. (13 pts)** GAN training is unstable. Explain the root cause and how WGAN addresses it. Include: minimax objective, optimal discriminator, generator gradient with disjoint supports, Wasserstein-1 distance, and Lipschitz enforcement.

> [!success]- Answer
> 
> **GAN minimax objective:**
> $$\min_G\max_D\;\mathbb{E}_{x\sim p_r}[\log D(x)]+\mathbb{E}_{z\sim p_z}[\log(1-D(G(z)))]$$
> 
> **Optimal discriminator:**
> For fixed $G$, maximise the integrand at each $x$:
> $$D^*(x)=\frac{p_r(x)}{p_r(x)+p_g(x)}$$
> 
> **Generator gradient with disjoint supports:**
> Substituting $D^*$ gives $\mathcal{L}(G,D^*)=2\,\text{JS}(p_r\|p_g)-2\log2$.
> In high dimensions, $p_r$ and $p_g$ lie on low-dimensional manifolds that are almost always disjoint. JS divergence then equals $\log2$ regardless of how close the distributions are — the loss surface is flat and $\nabla_G\mathcal{L}\approx0$. A well-trained discriminator kills the generator's learning signal.
> 
> **Wasserstein-1 distance:**
> $$W(p_r,p_g)=\sup_{\|f\|_L\leq1}\;\mathbb{E}_{p_r}[f(x)]-\mathbb{E}_{p_g}[f(x)]$$
> Unlike JS divergence, $W$ is well-defined and provides a smooth, non-zero gradient even when distributions have disjoint support — it measures minimum "work" to transport $p_g$ onto $p_r$, which always varies continuously with generator parameters.
> 
> **Lipschitz enforcement:**
> The supremum is over 1-Lipschitz functions ($\|\nabla f\|_2\leq1$). Enforced via:
> 1. **Weight clipping** (original WGAN): clip critic weights to $[-c,c]$. Simple but limits capacity.
> 2. **Gradient penalty** (WGAN-GP, preferred): add $\lambda\,\mathbb{E}_{\hat{x}}[(\|\nabla_{\hat{x}}f_w(\hat{x})\|_2-1)^2]$ where $\hat{x}$ are interpolations between real and fake data. Differentiable and more stable.
> 
> The WGAN critic always provides a meaningful, non-vanishing gradient signal to the generator — resolving the original instability.
