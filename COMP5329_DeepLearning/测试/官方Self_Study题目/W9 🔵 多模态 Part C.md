# W9 — Part C Exam-Style Questions
**来源：Week9 - MultiModal_Foundation_Models.ipynb（官方 tutorial，未改动）**

> [!info] 备考优先级：轻量

---

---
# Part C · Exam-Style Questions

> Three short-answer questions at medium-high difficulty. Each has a collapsed **Model Answer** cell directly below with the key points the tutor will draw out during discussion.

## Q1 · Cross-attention vs self-attention — shapes and uses

**(a)** For a single multi-head attention block with $H$ heads and head dimension $d_k$, write down the shape of the attention weight tensor in both the self-attention case (sequence length $T$) and the cross-attention case (query length $T_q$, memory length $T_m$). State one architecturally significant difference between the two shapes.

**(b)** Give **one concrete example** of cross-attention where $T_q \ll T_m$ and **one** where $T_q \gg T_m$. In each case, identify which tensor is the query, which is the memory, and why the asymmetry makes sense.

**(c)** During training, self-attention inside a GPT decoder uses a **causal** mask, whereas cross-attention inside an encoder–decoder Transformer uses a **padding** mask on the memory side. Explain *why* these two masks are different — in particular, why it would be a bug to apply a causal mask to cross-attention, and why a padding mask alone would not suffice inside a GPT decoder.

<details>
<summary><b>▸ Model Answer · Q1</b></summary>

**(a)** Self-attention weight tensor: $(B, H, T, T)$ — **square**, one row and one column per sequence position. Cross-attention weight tensor: $(B, H, T_q, T_m)$ — **rectangular**, rows indexed by *query* positions and columns indexed by *memory* positions. The rectangular shape is the architectural fingerprint of cross-attention: there is no notion of "the diagonal" because queries and memory are not aligned position by position.

**(b)** $T_q \ll T_m$: an **image-captioning decoder** where a short text query of ~20 tokens attends over a long sequence of image patch features (e.g. $T_m = 256$ for a $16\times16$ ViT grid) — the short caption "looks at" the much larger image. The query is the text decoder state; the memory is the ViT output. $T_q \gg T_m$: a **LLM decoder reading a compressed knowledge vector**, such as Flamingo's Perceiver Resampler, which always emits exactly 64 learned visual tokens regardless of image size — here a long text context ($T_q = $ thousands) queries a small, fixed-size visual memory ($T_m = 64$). In both cases the query supplies the "what do I want to know?" signal and the memory supplies the "what is available to be looked up?".

**(c)** A causal mask enforces the rule "position $t$ may only attend to positions $\leq t$ within the *same* sequence" — it is about *time ordering inside one sequence*. A padding mask enforces the rule "some positions are not real tokens" — it is about *data validity across any sequence*.

- In **cross-attention**, query positions and memory positions are in different sequences; there is no temporal "before" relationship between them. Applying a causal mask would arbitrarily forbid query position 3 from looking at memory position 5 — which would be wrong, since the memory is *not* on the same timeline as the query. Hence cross-attention uses a padding mask on the memory side only.
- In a **GPT decoder**, self-attention operates on one sequence that may contain left-padding or right-padding (from batch packing). A padding mask on its own would let position 7 attend to position 9 if both were valid tokens — peeking at future text. So we need the causal mask *in addition* to any padding mask the batch happens to require.

**Key takeaway:** causal masks prevent *time-travel*; padding masks ignore *non-tokens*. They are orthogonal concerns, and which one applies where is determined by the architecture of the block, not by personal preference.
</details>


## Q2 · KV cache — complexity and validity

Consider a decoder-only Transformer with $d_{\text{model}} = 4096$, $L = 32$ layers, and a final generated sequence length of $T = 2048$ tokens. Assume $K$ and $V$ are stored per layer in `fp16` (2 bytes per scalar).

**(a)** Derive an expression in **big-O** notation for the cost of generating **one token at decode step $t$**, both *without* and *with* a KV cache. Sum both expressions over $t=1,\dots,T$ to get the total decode cost, and state the asymptotic ratio between the two.

**(b)** Compute the total KV cache memory footprint (in bytes, then gigabytes) for one sequence of length $T=2048$ at the settings above. Show your arithmetic. Why is batched long-context serving so expensive even when the model weights themselves easily fit in GPU memory?

**(c)** Name **two concrete situations** in which the KV cache you just built would become **invalid** and must be discarded or rebuilt. For each case, explain in one sentence *why* the cached $K,V$ no longer match the semantics of the current computation.

<details>
<summary><b>▸ Model Answer · Q2</b></summary>

**(a)** Without the cache, step $t$ must re-project all $t$ tokens to obtain $Q, K, V$ ($O(t d^2)$) and then run self-attention over the length-$t$ prefix ($O(t^2 d)$). The attention term dominates, so **one step = $O(t^2 d)$**. Summing over $t=1,\dots,T$:
$$\sum_{t=1}^{T} O(t^2 d) = O(T^3 d).$$
With the cache, step $t$ projects *only the new token* ($O(d^2)$) and attends its length-1 query against the length-$t$ cache ($O(t d)$). So **one step = $O(t d + d^2)$**, and summed:
$$\sum_{t=1}^{T} O(t d + d^2) = O(T^2 d + T d^2).$$
**Ratio.** Cached total / naive total $\sim O((T^2 d + T d^2) / (T^3 d)) = O(1/T + 1/(T^2/d)) \to 0$ as $T$ grows — the speedup is **$\Theta(T)$ per token**, turning a cubic cost into a quadratic one.

**(b)** Per layer we store both $K$ and $V$, each of shape $(T, d_{\text{model}})$. Per sequence:
$$\text{elements} = 2 \cdot L \cdot T \cdot d_{\text{model}} = 2 \cdot 32 \cdot 2048 \cdot 4096 \approx 5.37 \times 10^8$$
$$\text{bytes}    = 5.37 \times 10^8 \cdot 2 \approx 1.07 \times 10^9 \approx 1.0 \text{ GiB}.$$
This is **per sequence**, so serving a batch of 16 long-context requests on a 7B-parameter model easily consumes ~16 GiB just for the caches — more than the model weights themselves in fp16 (~14 GB). That is why the KV cache, not the parameters, is the memory bottleneck for long-context LLM serving, and why techniques like PagedAttention, MQA/GQA, and KV-cache quantisation exist.

**(c)** Two situations in which the cache becomes invalid:
1. **Out-of-order decoding or token rollback** (e.g. speculative decoding that rejects a draft, beam search pruning a hypothesis). The cache still holds $K,V$ for tokens that are no longer part of the current prefix, so attention would condition on a ghost past. Fix: truncate the cache back to the common prefix length before continuing.
2. **Any change in the context that sits "inside" the prefix** — editing a system prompt, changing a retrieval passage, switching user turn in an in-place multi-turn setup. The $K,V$ in the cache were computed from the *old* input embeddings and the *old* attention layers; if the tokens those entries represent changed, the cached keys/values no longer match the semantics of the current query.

*(Bonus third case, sometimes asked:* model-weight change — LoRA adapter swap, quantisation change. The $K,V$ tensors were computed by the old $W_k, W_v$, so they are stale.)

**Key takeaway:** a KV cache is a *memoisation* — it is only valid as long as the input sequence and the function computing $K,V$ both stay fixed. Any edit invalidates the memo.
</details>


## Q3 · Where is the cross-attention in LLaVA?

Part A contrasted LLaVA (projector + concat) with Flamingo (gated cross-attention layers). Both are VLMs, but only Flamingo has explicit cross-attention modules in its architecture.

**(a)** Draw the data-flow (in words is fine) of how an image and a text prompt pass through LLaVA — from raw pixels all the way to the first LLM self-attention layer. At which exact step do the visual features enter the LLM, and in what shape?

**(b)** LLaVA uses **no cross-attention module** anywhere. Explain, referring to the mechanics of self-attention on the mixed `[image_tokens ; text_tokens]` sequence, *why LLaVA does not need one*. Your answer should make clear what role the projector MLP plays and what role the LLM's existing self-attention plays.

**(c)** Flamingo, by contrast, inserts **gated cross-attention** layers into the frozen LLM. (i) Why is cross-attention the right mechanism here — i.e., why not just concatenate like LLaVA does? (ii) The gate $\tanh(\alpha)$ is initialised with $\alpha = 0$. Explain the purpose of this zero-initialisation trick, and what would go wrong if $\alpha$ were initialised to, say, $1$ instead.

<details>
<summary><b>▸ Model Answer · Q3</b></summary>

**(a)** LLaVA's forward pass, in order:
1. Image → frozen **CLIP ViT** → patch features of shape $(N_v, d_v)$, e.g. $(576, 1024)$ for a $336\times336$ image with $14\times14$ patches.
2. Patch features → **MLP projector** → projected visual tokens of shape $(N_v, d_{\text{llm}})$, e.g. $(576, 4096)$ for LLaMA-2.
3. Tokenise the text prompt → text embeddings of shape $(N_t, d_{\text{llm}})$.
4. **Concatenate** $[ \text{visual}_1, \dots, \text{visual}_{N_v},\, \text{text}_1, \dots, \text{text}_{N_t} ]$ into one sequence of length $N_v + N_t$ and dimension $d_{\text{llm}}$.
5. Feed this mixed sequence into the LLM's first self-attention layer exactly as if it were all text.

Visual features enter the LLM at **step 4**, in shape $(B, N_v + N_t, d_{\text{llm}})$ — indistinguishable from text at the tensor level.

**(b)** The projector MLP's one job is to **map CLIP's visual features into the LLM's token embedding space**. After this mapping, each visual token is a vector in $\mathbb{R}^{d_{\text{llm}}}$ drawn from roughly the same distribution as the LLM's own text-token embeddings. Once image and text live in the same vector space, **self-attention cannot tell them apart** — the attention mechanism only cares about pairwise dot products $q \cdot k$, not about where $q$ or $k$ came from. So self-attention on the mixed sequence naturally performs the fusion: whenever a text query says "describe the red cup", its $Q$ vector develops a high inner product with whichever visual $K$ vector represents the red cup, and the corresponding $V$ (also visual) is read back. Cross-attention is unnecessary because we turned the vision–text interaction into a *self*-attention problem by first aligning the two spaces with the projector.

**Role summary:**
- **Projector MLP** — makes vision and text *commensurate* in a shared space (the hard part, learned on (image, caption) data).
- **LLM self-attention** — performs the *fusion* for free, because after projection there is only one sequence, not two.

**(c)** **(i) Why cross-attention in Flamingo.** Flamingo was specifically designed to **keep both the vision encoder and the LLM frozen** and insert new layers between them. Concatenation à la LLaVA requires the text-token and image-token spaces to be compatible, which in turn requires training a projector *plus* (in practice) fine-tuning the LLM on visual instruction data. Flamingo instead leaves the LLM weights untouched and uses cross-attention to let the frozen text hidden states *query* a compressed set of visual tokens. That way the visual information is read on-demand by each text position, no pre-alignment of spaces is needed, and the LLM's language abilities are preserved exactly. Cross-attention is the natural fit because $Q$ and $K,V$ genuinely come from different sources here.

**(ii) Why $\tanh(0) = 0$.** At initialisation, the newly inserted cross-attention layer's weights are essentially random. If you used the raw cross-attention output as a residual addition to the frozen LLM's hidden state, the LLM would be **flooded with random junk from the first training step**, destabilising or overwriting the pretrained language representations before the new weights have learned anything useful. Initialising $\alpha = 0$ makes the gated residual $x + \tanh(0)\cdot\text{CrossAttn}(x, v) = x$ — the inserted layer is mathematically a **no-op** at $t=0$, so the frozen LLM behaves exactly as before. As training progresses, $\alpha$ slowly grows and visual information bleeds in smoothly, but only after the new cross-attention weights have stabilised. Initialising $\alpha=1$ would skip this warm-up and is known to degrade or destroy the pretrained LLM behaviour.

*(This zero-init trick recurs throughout modern DL: LoRA initialises its second low-rank matrix $B$ to zero for the same reason, and ControlNet uses "zero convolutions" — both preserve the pretrained function at $t=0$.)*
</details>

---

*End of Part C.*

