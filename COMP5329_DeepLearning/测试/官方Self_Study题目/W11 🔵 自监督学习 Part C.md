# W11 — Part C Exam-Style Questions
**来源：Week11_Self_Supervised_Representation_Learning.ipynb（官方 tutorial，未改动）**

> [!info] 备考优先级：轻量

---

---
# Part C · Exam-Style Questions

> Three short-answer questions at medium-high difficulty. Each has a hidden **Model Answer** cell directly below with the key points the tutor will draw out during discussion.

## Q1 · MAE — why the loss is on masked positions only

In your Task B1 implementation, `mae_loss` returns `(per_patch * mask).sum() / mask.sum()`, i.e. the MSE is averaged **only** over patches where `mask == 1` (the hidden patches). A student suggests a "simpler" alternative: average the MSE over **all** $N$ patches (visible *and* masked), arguing it should still push the reconstructions to be accurate.

**(a)** Write the one-line code change that implements the student's alternative, and express the resulting loss as a weighted combination of the "visible" and "masked" terms. (Use $\mathcal{M}$ for the masked set and $\mathcal{V}$ for the visible set; $|\mathcal{M}| + |\mathcal{V}| = N$.)

**(b)** Why is the student's alternative a **bad** objective for representation learning? Your answer should mention the word "shortcut" and should reason about what a trained MAE encoder would do to minimise each of the two terms you identified in (a).

**(c)** MAE uses a **75%** mask ratio, whereas BERT (masked language modelling) uses only **15%**. Give one information-theoretic reason why the image-modality ratio needs to be so much higher.

<details>
<summary><b>▸ Model Answer · Q1</b></summary>

**(a)** The one-line change is replacing the masked average with a full mean:

```python
loss_all = ((pred - target) ** 2).mean()         # average over B * N * D
```

Equivalently,
$$\mathcal{L}_{\text{all}} = \frac{|\mathcal{V}|}{N}\underbrace{\frac{1}{|\mathcal{V}|}\sum_{i \in \mathcal{V}}\lVert\hat{x}_i - x_i\rVert^2}_{\text{visible term}} + \frac{|\mathcal{M}|}{N}\underbrace{\frac{1}{|\mathcal{M}|}\sum_{i \in \mathcal{M}}\lVert\hat{x}_i - x_i\rVert^2}_{\text{masked term}}.$$

At 75% masking, $|\mathcal{V}|/N = 0.25$ and $|\mathcal{M}|/N = 0.75$, so the visible term receives a quarter of the total weight.

**(b)** The visible term is trivially minimisable: the encoder sees patch $i \in \mathcal{V}$ as input and is asked to reproduce it as output. The model can route the visible patch through the network as an **identity shortcut** (a skip connection, or simply a near-identity transform in the decoder) and drive the visible-term MSE to ≈0 *without ever learning anything semantic*. Because $|\mathcal{V}|/N = 0.25$ is a large slice of the loss, optimisation will greedily exploit this shortcut, which in turn reduces the gradient pressure on the masked term. The encoder ends up as a glorified autoencoder-with-a-shortcut, and the representation transfers poorly to downstream tasks. Restricting the loss to $\mathcal{M}$ makes the shortcut impossible — the model can *only* receive gradient for predicting content it has **not** seen, which is exactly the signal that forces it to build a world-model of the input distribution.

**(c)** Text is **discrete and information-dense**: each word carries a lot of entropy, and with 15% masking BERT cannot simply copy a neighbour because adjacent words are usually semantically different. Images are **continuous and spatially redundant**: neighbouring patches share colour, texture, and edges, so with 15% masking a trivial linear interpolation of the visible neighbours already reconstructs the missing patch very well — the pretext task is too easy to force the model to learn global structure. Raising the mask ratio to 75% removes enough *local* context that the model *must* rely on **global, semantic** reasoning to fill in the missing regions, which is exactly the kind of representation we want to transfer.

**Key points:**
- Loss on masked-only = shortcut-free gradient = genuine representation learning.
- The mask ratio has to match the intrinsic redundancy of the modality — vision is redundant, language is not.
- The same argument explains why MAE needs an asymmetric encoder/decoder: running the big encoder on 25% of patches (vs 100%) is a free ~4× speedup that only works because the loss *ignores* the visible patches anyway.
</details>

## Q2 · SimCLR — temperature extremes

In Task B2 you plotted the NT-Xent loss as a function of $\tau$ on random (un-trained) embeddings and observed two failure regimes.

**(a)** For $\tau \to 0^{+}$: describe what the softmax distribution $p_k = \text{softmax}(\text{sim}_{i,k}/\tau)_k$ converges to, and what the gradient $\partial \mathcal{L} / \partial z_i$ concentrates on. Why is this a *training* problem rather than just a numerical one?

**(b)** For $\tau \to \infty$: describe the same two quantities, and compute the limiting loss value (as a closed-form expression in $B$). What does this imply for the gradient signal and therefore for learning?

**(c)** Production SimCLR uses $\tau \approx 0.1$–$0.5$ while CLIP uses $\tau \approx 0.07$ and additionally **learns** $\tau$ as a parameter (clamped so that $\log(1/\tau) \le \log 100$). Why does CLIP get away with a sharper temperature, and why does letting $\tau$ be a learned parameter act as a **self-regulation** mechanism?

<details>
<summary><b>▸ Model Answer · Q2</b></summary>

**(a)** As $\tau \to 0^{+}$, every logit $\ell_k = \text{sim}_{i,k}/\tau$ diverges in magnitude, and the softmax converges to a one-hot distribution on whichever non-self index has the largest similarity — i.e. the **single hardest negative** (or, once training is well underway, the positive). The loss gradient
$$\frac{\partial \mathcal{L}}{\partial z_i} = \frac{1}{\tau}\Big(\sum_{k} p_k z_k - z_{i^+}\Big)$$
has (i) a $1/\tau$ scaling that blows up, and (ii) a softmax weight vector $p$ concentrated on a *single* $k$. So each update step is a large, high-variance move that only accounts for one negative at a time; the next step may see a different hardest negative, and the representation oscillates. This is a **training** failure, not just numerical — even in infinite precision, the optimiser cannot average out gradient information from the other negatives, so convergence stalls or diverges.

**(b)** As $\tau \to \infty$, every logit $\ell_k \to 0$, so the softmax becomes the **uniform** distribution $p_k = 1/(2B-1)$ over the $2B-1$ non-self entries. The loss per row is therefore $-\log(1/(2B-1)) = \log(2B-1)$, independent of the actual embeddings — this is the dashed line in your temperature-sweep plot. The gradient
$$\frac{\partial \mathcal{L}}{\partial z_i} = \frac{1}{\tau}\Big(\sum_{k \ne i} \tfrac{1}{2B-1} z_k - z_{i^+}\Big) \to 0$$
because of the prefactor $1/\tau$. There is essentially no learning signal: the loss does not care which embedding is the positive, so the encoder cannot improve.

**(c)** CLIP's positive pair is (image, matching caption) — a **cross-modal** pair whose semantic gap to a random non-matching caption is enormous ("a dog on a beach" vs "a stock price chart"). The margin between positives and negatives in embedding space is intrinsically wide, so a sharper temperature can be tolerated without the $\tau \to 0$ failure mode. SimCLR's positives are two augmentations of the **same** image, and within a batch of natural images there are usually other images that are visually similar (same class, similar colour palette), so the positives-vs-negatives margin is narrower and $\tau$ must be larger to prevent hard negatives from producing noisy one-hot softmaxes. **Learnable $\tau$ self-regulates** because the cross-entropy loss, viewed as a function of $\tau$, is convex near the optimal sharpness: if training accidentally drives $\tau$ too small, the loss starts rising (we are in the noisy $\tau \to 0$ regime), and gradient descent on $\tau$ *increases* it again. The $\log(1/\tau) \le \log 100$ clamp is just a safety rail to keep $\tau$ from numerically underflowing.

**Key points:**
- Both extremes kill learning, for opposite reasons: $\tau\to 0$ has enormous but noisy gradients; $\tau\to\infty$ has vanishing gradients.
- The useful temperature depends on the **intrinsic positive/negative margin** of your task.
- Learning $\tau$ is a cheap trick that lets the model find its own sweet spot — you almost always want to do it.
</details>

## Q3 · Do we actually need negatives?  *(cross-cutting question)*

SimCLR's whole loss is built around contrasting a positive against $2B-2$ negatives. **SimSiam** (a non-contrastive method from the self-study notebook) uses *no negatives at all* — its loss is simply
$$\mathcal{L}_{\text{SimSiam}} = -\tfrac{1}{2}\big[\cos(\text{pred}(z_a),\, \text{stopgrad}(z_b)) + \cos(\text{pred}(z_b),\, \text{stopgrad}(z_a))\big]$$
and yet it learns useful representations comparable to SimCLR.

**(a)** What **failure mode** do negatives prevent in contrastive learning? Describe it concretely in terms of what the encoder might output in their absence.

**(b)** In SimSiam, negatives are absent — so what is preventing that failure mode? Explain the role played by (i) the **predictor head** on one branch only and (ii) the **stop-gradient** on the other branch. A one-sentence intuition per mechanism is enough, but both must appear.

**(c)** SimCLR's loss, in the limit of very large $B$, approximates a mutual-information lower bound between the two views; SimSiam has no such interpretation. Despite that, SimSiam often matches SimCLR's linear-probe accuracy on ImageNet. What does that tell you about the **role of negatives** in practice — are they about *information*, or about *optimisation*?

<details>
<summary><b>▸ Model Answer · Q3</b></summary>

**(a)** The failure mode is **representation collapse**: without negatives, the trivial solution to "make two views of the same image agree in embedding space" is for the encoder to map *every* input to the *same* constant vector. If $f(x) = c$ for all $x$, then the cosine similarity of any two views is 1 and the loss is 0 — a global minimum that is useless for downstream tasks. In practice the encoder doesn't collapse all the way to a point but to a **low-dimensional degenerate subspace**, which still destroys discriminative power. Negatives prevent this because pushing the constant-solution embedding apart from $2B-2$ "negatives" that are *also* equal to $c$ is infeasible — the softmax denominator in NT-Xent is saturated and the loss stays high, so the optimiser is forced to spread embeddings out.

**(b)**
- **(i) The predictor head**: SimSiam's online branch has an extra MLP $h$ on top of the projection, so that branch outputs $h(z_a)$ while the other outputs $z_b$. This asymmetry means the two sides are **not computing the same function**, so the collapsed solution "everything maps to a single constant" no longer satisfies the optimum — for the predictor-side output to match the un-predicted side, the representation has to carry enough information for $h$ to reconstruct a *direction*, not just a point.
- **(ii) Stop-gradient**: The `stop_grad(z_b)` target makes one branch an "oracle" that the other branch chases. Without stop-gradient, the encoder could minimise the loss by moving $z_b$ and $z_a$ *toward each other* simultaneously — the fastest way being to collapse both to the same constant. With stop-gradient, only the predictor-side pathway receives gradient; $z_b$ is treated as fixed, so the loss can only be decreased by making $h(z_a)$ match a target that the network *cannot currently reshape*. Empirically, removing either the predictor or the stop-gradient causes immediate collapse, so both are load-bearing.

**(c)** Negatives in SimCLR are primarily an **optimisation** device, not an *information* one. The theoretical story (InfoNCE as an MI lower bound) is elegant but the **practical function** of negatives is to inject a repulsive force that keeps the encoder from collapsing. SimSiam shows that an equivalent repulsive force can be obtained from **architectural asymmetry** (predictor head + stop-gradient) without any explicit negatives in the loss. Put differently: the role of negatives is to prevent a degenerate optimum, not to maximise mutual information — any mechanism that achieves the former (negatives, stop-grad asymmetry, DINO's centering + sharpening, Barlow Twins' cross-correlation decorrelation) can produce representations of comparable quality.

**Key points:**
- "Contrastive vs non-contrastive" is about *collapse avoidance mechanisms*, not about whether information is preserved.
- Negatives, stop-grad, centering, decorrelation — all different answers to the same engineering question: "how do I keep the encoder from outputting a constant?"
- This is why the SSL literature has converged: by 2022–2023 contrastive and non-contrastive methods reach near-identical linear-probe accuracy, suggesting the exact mechanism matters less than having **some** anti-collapse term.
</details>
