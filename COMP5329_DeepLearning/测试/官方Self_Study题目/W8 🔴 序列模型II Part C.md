# W8 — Part C Exam-Style Questions
**来源：Week8_Sequence_Modeling_Architectures_II.ipynb（官方 tutorial，未改动）**

> [!danger] 备考优先级：必考

---

---
# Part C · Exam-Style Questions

> Three short-answer questions at medium-high difficulty. Each has a collapsed **Model Answer** cell directly below — attempt each question on paper first, then expand the solution.

---

## Q1 · ViT patch-size trade-off and inductive bias *(Part B Task 1)*

A Vision Transformer splits a $224 \times 224$ image into non-overlapping $P \times P$ patches, linearly projects each patch to dimension $D$, prepends a learnable `[CLS]` token, adds a learnable positional encoding, and feeds the resulting $(T+1, D)$ sequence into a standard Transformer encoder.

**(a)** Suppose we change the patch size from $P=16$ to $P=32$. Compute explicitly how (i) the sequence length $T$, (ii) the FLOPs of a single self-attention layer (which scale as $T^2 D$), and (iii) the spatial area each token covers change. Use concrete numbers.

**(b)** Explain, in terms of the `forward` pipeline you implemented in Task B1, **exactly why** the learnable positional embedding is necessary. What would go wrong if we simply removed it?

**(c)** ViT underperforms a strong CNN (e.g. EfficientNet-B7) when both are trained only on ImageNet-1K, but *surpasses* it when pre-trained on JFT-300M. Using Week 4's concept of **inductive bias**, explain what built-in assumptions CNNs make that ViT does not, and why those assumptions help on small data but become a ceiling on large data.

*Your answer:*

<details>
<summary><b>▸ Model Answer · Q1</b></summary>

**(a)** With $P=16$: $T = (224/16)^2 = 14^2 = 196$. With $P=32$: $T = (224/32)^2 = 7^2 = 49$. So:

- **(i)** $T$ drops from 196 to 49 — a factor of **4× fewer tokens**.
- **(ii)** Self-attention FLOPs scale as $T^2 D$, so they drop by $(196/49)^2 = 16$× — **16× cheaper attention**.
- **(iii)** The spatial area a single token covers goes from $16 \times 16 = 256$ pixels to $32 \times 32 = 1024$ pixels — **4× coarser** spatial granularity.

Trade-off: larger patches = cheaper attention + coarser spatial detail; smaller patches = more expressive + quadratically more expensive. This is exactly the compute–accuracy dial ViT exposes.

**(b)** In the Task B1 pipeline, the patch embedding after step 3 is `(B, T+1, D)`, a **set of tokens** with no intrinsic spatial ordering — unfold produces them in row-major order, but a Transformer encoder sees them as an unordered multiset because self-attention is **permutation-equivariant**: shuffle the token sequence and you get the same output set in the shuffled order. Without a positional embedding, the model cannot tell "the patch at the top-left of the image" apart from "the patch at the bottom-right." A ViT without positional encoding would be invariant to permutations of the 16 patches — a cat centred in the image and a cat whose patches were randomly shuffled would produce *identical* hidden states. The learnable `pos_embed` breaks this symmetry by adding a distinct vector to each slot, turning a permutation-invariant set into a structured sequence.

**(c)** Convolutional layers bake in three inductive biases:
1. **Locality** — a filter only looks at a small neighbourhood.
2. **Translation equivariance** — the same filter slides across the whole image, so a cat in the top-left and a cat in the bottom-right activate the same features (just shifted).
3. **Hierarchical composition** — shallow layers learn textures, deep layers learn semantics.

These are hand-engineered priors matched to natural-image statistics. ViT's self-attention has none of these — it is a global, permutation-respecting pairwise operator, and any spatial structure must be *learned* from data. On **small** datasets (ImageNet-1K ≈ 1.2M images), the CNN's priors are exactly right; ViT cannot see enough images to rediscover them, and underperforms. On **large** datasets (JFT-300M ≈ 300M images), ViT has enough data to learn spatial organisations that are more flexible than the hard-coded CNN priors — including global, long-range dependencies in a single layer — and the rigid CNN priors become a *ceiling*.

**One-line summary**: inductive bias is a double-edged sword — it does your homework for you when data is scarce, and holds you back when data is abundant.
</details>

---

## Q2 · SSM recurrent ↔ convolutional equivalence *(Part B Task 2)*

The discrete SSM is
$$h_{k+1} = \bar A\,h_k + \bar B\,u_k, \qquad y_k = C\,h_k$$
with $\bar A \in \mathbb R^{N\times N}$, $\bar B \in \mathbb R^{N \times 1}$, $C \in \mathbb R^{1 \times N}$.

**(a)** Starting from this recurrence with $h_0 = 0$, derive the closed-form expression for $y_k$ as a function of the inputs $u_{0}, u_1, \ldots, u_k$. Give an explicit formula for the length-$L$ kernel $K$ such that $y = K * u$ (causal convolution).

**(b)** Standard scaled dot-product (softmax) attention computes $y_t = \sum_{i \le t} \alpha_{t,i}\,v_i$ with $\alpha_{t,i} = \exp(q_t^\top k_i)/Z_t$. Explain why this **cannot** be written as $y = K * u$ for any input-independent $K$. Point to the specific algebraic obstruction — two sentences max.

**(c)** In Task B2 you observed that `build_ssm_kernel` uses an *incremental* running product `A_pow_B = A_bar @ A_pow_B` rather than calling `torch.matrix_power(A_bar, i) @ B_bar` at each iteration. Give the asymptotic cost of each approach and explain in one sentence why the incremental version is asymptotically optimal.

*Your answer:*

<details>
<summary><b>▸ Model Answer · Q2</b></summary>

**(a)** Unroll the recurrence with $h_0 = 0$:
$$h_1 = \bar B\,u_0,\quad h_2 = \bar A\bar B\,u_0 + \bar B\,u_1,\quad h_3 = \bar A^2\bar B\,u_0 + \bar A\bar B\,u_1 + \bar B\,u_2,\ \ldots$$
In closed form:
$$h_{k+1} = \sum_{i=0}^{k} \bar A^{\,k-i}\,\bar B\,u_i \quad\Longrightarrow\quad y_k = C h_{k+1} = \sum_{i=0}^{k}\big(C\,\bar A^{\,k-i}\,\bar B\big)\,u_i$$
Define $K_i = C\,\bar A^{\,i}\,\bar B$ for $i = 0, 1, \ldots, L-1$. Then
$$y_k = \sum_{i=0}^{k} K_{k-i}\,u_i = (K * u)_k$$
— a length-$L$ **causal convolution**. The algebraic property that makes this work is that $\bar A, \bar B, C$ are **constants** (independent of $k$ and of $u$), so the weight linking $u_i$ to $y_k$ depends only on the *gap* $k - i$ — precisely the definition of a convolution kernel.

**(b)** The attention weight $\alpha_{t,i}$ depends on $t$ (through $q_t$) and $i$ (through $k_i$) via the inner product $q_t^\top k_i$ — the two indices are **entangled, not separable**, so the weight is not a function of $t - i$ alone. On top of that, $Z_t = \sum_{j \le t}\exp(q_t^\top k_j)$ is a softmax normaliser that depends on the entire prefix and is non-linear — even the numerator $\exp(q_t^\top k_i)\,v_i$ would not separate. No fixed, input-independent $K$ can reproduce these weights, so no convolution form exists.

**(c)**
- **Naive** `torch.matrix_power(A_bar, i) @ B_bar` at each step: computing $\bar A^i$ fresh every iteration costs $O(i \cdot N^3)$, so the whole loop is $O(L^2 N^3)$.
- **Incremental** `A_pow_B = A_bar @ A_pow_B`: each iteration is one matrix-vector multiply `(N,N) · (N,1)`, costing $O(N^2)$. Total is $O(L \cdot N^2)$.

The incremental version is asymptotically optimal because it reuses the previous power: $\bar A^{i+1}\bar B = \bar A\,(\bar A^i \bar B)$, so each new kernel entry costs only one matrix-vector multiply on top of what is already in memory — no wasted work. This is the same "prefix-sum / running product" idea that makes cumulative-sum, dynamic programming, and RNN unrolling efficient.

**Key points the tutor will land:**
- The kernel $K_i = C\bar A^i\bar B$ is literally the **impulse response** of the linear system — drive the SSM with $u_0 = 1, u_{>0} = 0$ and you read off $K$ at the output.
- Convolution-form equivalence is exactly why S4-style SSMs can be trained on TPU/GPU at Transformer speeds, while still running in $O(N)$ per step at inference time.
- What Mamba gives up: making $\bar A, \bar B, C$ depend on $u_k$ destroys both the "constants" hypothesis (so the separable gap-only weight disappears) *and* the incremental-power trick (every step has its own $\bar A$, so $\bar A^i$ is not well-defined). Mamba recovers parallel training via a parallel scan instead.
</details>

---

## Q3 · BERT vs. GPT — masking *is* the architecture *(Part A §1–§2)*

BERT and GPT are both Transformer stacks, both pretrained on massive text corpora, and both produce contextual token representations. Yet one is an *encoder-only* model used for understanding, and the other is a *decoder-only* model used for generation.

**(a)** For a sequence of length $T$, write down the **attention mask** used by BERT and by GPT as a $T \times T$ matrix (or describe it precisely — "entry $(i,j)$ equals 1 if token $i$ can attend to token $j$, else 0"). What shape does each mask have?

**(b)** BERT is pretrained with masked language modelling (MLM): 15% of input tokens are replaced by `[MASK]` and the model predicts the originals. Explain in one sentence why this objective **requires** BERT's bidirectional attention — i.e. why it would fail on a causally-masked GPT.

**(c)** You want to use a pretrained model to do two things:
*(i)* classify movie reviews as positive or negative;
*(ii)* generate a continuation of a user's half-written email.

Which of BERT / GPT is the natural choice for each, and **why**? Your answer must refer to the attention mask from part (a), not just handwave "BERT is for understanding."

*Your answer:*

<details>
<summary><b>▸ Model Answer · Q3</b></summary>

**(a)**

- **BERT** uses a **full (all-ones) mask**: $M_{ij} = 1$ for every $(i, j)$, so every token attends to every other token in both directions. Shape $T \times T$, every entry is 1.
- **GPT** uses a **lower-triangular (causal) mask**: $M_{ij} = 1$ if $j \le i$, else 0. Shape $T \times T$; the upper triangle is zero. In code this is the attention-logit mask
$$M = \begin{pmatrix} 1 & 0 & 0 & \cdots & 0 \\ 1 & 1 & 0 & \cdots & 0 \\ 1 & 1 & 1 & \cdots & 0 \\ \vdots & & & \ddots & \vdots \\ 1 & 1 & 1 & \cdots & 1 \end{pmatrix}$$
applied as additive $-\infty$ on the masked positions before the softmax so they contribute zero weight.

**(b)** MLM replaces a token in the *middle* of the sequence and asks the model to predict it from its context. To get any signal about the original token, the encoder at the masked position must be able to attend to tokens both to its **left** AND **right** — the right-hand context is critical (the cat sat on the \_\_\_ → "mat" only from the left; the \_\_\_ sat on the mat → "cat" only from the right; in practice both are needed). A causally-masked GPT can only see tokens to the *left* of each position, so it literally cannot condition on the right context and the MLM objective is strictly weaker than predicting the next token from the prefix. GPT's causal mask is incompatible with MLM.

**(c)**

- **(i) Movie-review sentiment classification → BERT.** For a classification task you see the *entire* review up front and want the best possible representation at a single `[CLS]` position. BERT's bidirectional attention mask (the all-ones matrix above) lets the `[CLS]` representation at the top of the stack combine information from every word in the review — left context and right context, early and late — in a single forward pass. A GPT `[CLS]` at position 0 could never see a single word of the review (upper triangle zeroed), and a GPT `[CLS]` at position $T$ could see the whole review but with the strict ordering constraint that forces every attention weight to be a function of a one-way prefix, losing the symmetric pair-interactions BERT has. Bidirectional = better for "look at everything at once" tasks.

- **(ii) Email-continuation generation → GPT.** Here you are given a prefix and must produce tokens one at a time. This is literally the objective GPT was pretrained on: $p_\theta(x_t \mid x_{<t})$ with a causal mask. At inference you feed the prefix, sample $x_{T+1}$, append it, and repeat — the causal mask guarantees that the prediction at each new step only looks at tokens that already exist, so the sampling procedure is consistent with training. You could in principle fine-tune BERT for generation, but the MLM objective does not match how you'd actually call the model at inference (there's no `[MASK]` in the user's half-written email, and BERT was never trained to produce coherent long sequences), so you would need architectural hacks that defeat the point of pretraining. Causal mask = naturally fits autoregressive generation.

**Key points:**
- The attention mask **is** the architecture. BERT and GPT share 95% of their PyTorch code; the only structural difference is whether the attention logits get the causal triangle applied or not, and that single bit determines whether the model is an encoder (understanding) or a decoder (generation).
- Pretraining objective and attention mask must agree: bidirectional encoder ↔ MLM; causal decoder ↔ next-token prediction. Mixing them breaks both the training signal and the inference story.
</details>

---

*End of Part C.*

---
## Summary

| Section | Key concept |
|---|---|
| **Part A §0** | Pretraining paradigm — self-supervised pretraining on massive unlabelled corpora, then fine-tuning on small labelled tasks |
| **Part A §1** | BERT = encoder-only + bidirectional attention + masked LM; `[CLS]` head for classification |
| **Part A §2** | GPT = decoder-only + causal (lower-triangular) attention mask + next-token prediction; same objective at train and inference |
| **Part A §3** | ViT = image → patches → linear projection → prepend `[CLS]` + learnable positional embedding → standard Transformer encoder |
| **Part A §4** | Discrete SSM: $h_{k+1} = \bar A h_k + \bar B u_k$, $y_k = C h_k$; unroll → $y = K*u$ with $K_i = C\bar A^i\bar B$ |
| **Part A §5** | Mamba = selective SSM: $\bar A, \bar B, C$ depend on $u_k$; kernel disappears; recovered by parallel scan |
| **Part B Task 1** | `ViTPatchEmbedding`: `nn.Unfold` → `nn.Linear` → prepend `[CLS]` token → add `pos_embed` |
| **Part B Task 2** | `ssm_recurrent` (RNN-style, $O(N)$ state) and `ssm_conv` (build $K$ incrementally, apply as 1-D causal convolution) — numerically identical |

**Take-aways:**
- Pretraining + fine-tuning is the default paradigm for modern Transformers; BERT, GPT, and ViT all share the encoder or decoder block but differ in mask + objective.
- ViT turns an image into a token sequence via patchification; positional encoding is *required* because self-attention is permutation-invariant.
- Linear SSMs are dually a recurrence (cheap inference) *and* a convolution (parallel training) — same weights, two views. The equivalence rests on $\bar A, \bar B, C$ being input-independent.
- Mamba trades the convolution form for input-dependent selectivity and recovers parallel training via a parallel scan. Exam Q2 and Q3 push on these two ideas.

