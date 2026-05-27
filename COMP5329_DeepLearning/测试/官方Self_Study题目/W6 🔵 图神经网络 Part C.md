# W6 — Part C Exam-Style Questions
**来源：Week6_Graph_Neural_Networks.ipynb（官方 tutorial，未改动）**

> [!info] 备考优先级：轻量

---

---
# Part C · Exam-Style Questions

> Three short-answer questions at medium-high difficulty. Each has a hidden **Solution** cell directly below with a model answer and the key points the tutor will draw out during discussion.

## Q1 · The normalisation choice

The GCN propagation rule uses the **symmetric** normalisation $\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$.

**(a)** Write the propagation rule that would result if we instead used **row normalisation** $\hat{D}^{-1}\hat{A}$. What does each row of $\hat{D}^{-1}\hat{A}H$ compute, in plain words?

**(b)** Give one concrete reason why symmetric normalisation is usually preferred over row normalisation in GCNs. Your answer should make reference to **how information flows between a high-degree node and a low-degree node**.

**(c)** What failure mode would you expect if we dropped normalisation altogether and used $\hat{A}HW$ directly in a **deep** GCN (say 10 layers)? Describe the forward-pass symptom and one gradient-related symptom.


<details>
<summary><b>▸ Model Answer · Q1</b></summary>

**(a)** The rule becomes $H^{(l+1)} = \sigma(\hat{D}^{-1}\hat{A}\,H^{(l)}\,W^{(l)})$. Each row of $\hat{D}^{-1}\hat{A}H$ is the *unweighted mean* of the node's own features and its neighbours' features — an averaging operator where every neighbour contributes with weight $1/\hat{d}_i$.

**(b)** With row normalisation, the contribution a high-degree node sends to a low-degree neighbour is divided by the **sender's** large degree, so the low-degree node barely hears it; information flow is asymmetric. Symmetric normalisation splits the $1/\sqrt{d}$ factor across sender *and* receiver, giving a reciprocal weight $\frac{1}{\sqrt{\hat d_i \hat d_j}}$. The resulting propagation matrix is symmetric, which is essential for the connection to the **normalised graph Laplacian** and for stable spectral-view interpretation.

**(c)** Forward-pass symptom: $\hat{A}H$ *sums* neighbour features instead of averaging, so feature magnitudes scale roughly with node degree at every layer. Stacking $L$ layers blows up activations by a factor $\sim \bar{d}^{L}$, and loss quickly overflows. Gradient symptom: exploding gradients at high-degree nodes, vanishing gradients at leaves — training diverges within a few epochs.

**Key points the tutor must land:**
- Symmetric form ⟺ symmetric matrix ⟺ spectral view holds (eigendecomposition of $I - \hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$).
- Normalisation is not just aesthetics — without it, depth immediately destabilises training.
- The "averaging" interpretation (row normalisation) *is* pedagogically cleaner but is asymmetric and gives up reciprocity.
</details>


## Q2 · Semi-supervised power with only 2 labels

In the Karate Club demo you just ran, the GCN is trained on **only 2 labelled nodes** (node 0 = *Mr. Hi*, node 33 = *Officer*) but achieves near-perfect accuracy on all 34 nodes.

**(a)** Suppose a classmate tries to reproduce this result with a **plain MLP** that takes the same one-hot identity node features as input and is trained on the same 2 labelled examples. Predict the classmate's test accuracy on the other 32 nodes and explain your prediction in one sentence.

**(b)** Explain mechanistically **how** a 2-layer GCN can correctly classify an unlabelled node that is 2 hops away from node 0. Your answer should make reference to (i) the **receptive field** of a 2-layer GCN and (ii) the **loss function**, which is evaluated only on nodes 0 and 33.

**(c)** What would happen to the GCN's accuracy on a node that is **4 hops** away from *both* labelled nodes? Propose one architectural fix and one non-trivial side-effect of that fix.


<details>
<summary><b>▸ Model Answer · Q2</b></summary>

**(a)** ≈ 50% (chance level). One-hot identity features are pairwise orthogonal — they encode *node identity* and nothing else. The MLP sees 34 unrelated inputs with only 2 labelled, so it memorises the 2 training points and has no basis for generalising to the other 32. (This is exactly why GCNs are a win here: the graph structure is the only inductive bias that ties the unlabelled nodes to the labelled ones.)

**(b)** The 2-layer GCN's receptive field is **exactly 2 hops**: layer 1 mixes a node's features with its 1-hop neighbours, layer 2 mixes those mixed features with 1-hop neighbours again, so each node's logits are a function of every node within 2 hops. The cross-entropy loss is computed **only at node 0 and node 33**, but because the shared weights $W^{(1)}, W^{(2)}$ are used at every node, the gradient back-propagates through every edge inside the 2-hop neighbourhoods of node 0 and node 33 and updates the *same* weights. Any unlabelled node that sits inside either 2-hop ball therefore inherits consistent, community-aligned embeddings at inference time.

**(c)** A node 4 hops from both labelled nodes sits **outside** the 2-layer receptive field — the path from the supervision signal to that node's embeddings is cut, so its logits depend only on untrained initialisation and accuracy collapses to chance.

- **Fix**: stack more GCN layers (e.g., 4 layers → 4-hop receptive field) *or* add residual / skip connections.
- **Side-effect**: **over-smoothing** — as depth grows, repeated multiplication by $\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$ drives every node's representation toward the dominant eigenvector of that matrix, so all nodes start to look alike and the class boundary disappears. This is the well-known depth tradeoff in vanilla GCNs and motivates residual connections (GCNII, JK-Nets).

**Key points:**
- Receptive field = depth (for GCN, one hop per layer).
- Loss-at-a-few-points + weight sharing + multi-hop propagation = label propagation through the graph.
- Depth is not free — over-smoothing is the hidden cost.
</details>


## Q3 · Weight sharing: GCN vs. CNN  *(cross-week synthesis with Week 5)*

Both CNNs (Week 5) and GCNs (this week) are described as using **weight sharing** across spatial/graph positions.

**(a)** For a single 2-D convolutional layer with a $3\times 3$ kernel and a single GCN layer, precisely identify *which* tensor is the "shared weight" and *what entity* it is shared across.

**(b)** Name **one** property that weight sharing gives CNNs that weight sharing does **not** give GCNs, and explain *why* the difference arises. (Hint: think about what the neighbourhood of a pixel looks like vs. what the neighbourhood of a graph node looks like.)

**(c)** Imagine a **single GCN layer applied to a 2-D grid graph** (each pixel connected to its 4 cardinal neighbours). Argue whether this reproduces a $3\times 3$ convolution. If not, precisely identify what is different — and explain why this difference is exactly *why* GCNs are used for unordered data.


<details>
<summary><b>▸ Model Answer · Q3</b></summary>

**(a)**
- **CNN**: the $3\times 3 \times C_{\text{in}} \times C_{\text{out}}$ kernel is the shared weight; it is shared across **every spatial location** of the feature map.
- **GCN**: the weight matrix $W\in\mathbb{R}^{F_{\text{in}}\times F_{\text{out}}}$ is the shared weight; it is shared across **every node** of the graph.

**(b)** CNNs are **translation-equivariant**: shifting the input image by one pixel shifts the output by one pixel identically. GCNs are instead **permutation-equivariant**: relabelling the graph's nodes permutes the output identically. The asymmetry arises from the structure of the neighbourhood: pixels have a fixed, *ordered* neighbourhood (N / S / E / W / NE / …), so a $3\times 3$ kernel can assign a **distinct weight** to each neighbour position. Graph nodes have unordered, variable-size neighbourhoods, so a GCN must treat all neighbours **symmetrically** and cannot distinguish "the neighbour above" from "the neighbour to the left."

**(c)** **No — a single GCN layer on a grid graph is strictly less expressive than a $3\times 3$ convolution.** On a 4-neighbour grid, every non-corner node has the same aggregation pattern (centre + 4 cardinals), so the GCN is equivalent to a convolution whose $3\times 3$ kernel is constrained to have only **2 distinct values**: one weight for the centre, one weight shared across all 4 cardinal neighbours, and zero at the 4 corner positions. A real $3\times 3$ kernel has **9 independent weights** and can therefore learn **directional** filters (horizontal edges ≠ vertical edges, Sobel operators, oriented gradients). The GCN cannot represent any directional filter — exactly because it sacrifices directionality for permutation invariance. This is the right trade-off when the graph has no canonical ordering (social networks, molecules) but the wrong trade-off when the graph is an ordered grid (images).

**Key points:**
- Weight sharing is real in both cases but shared *over different symmetry groups*: the translation group for CNNs, the node-permutation group for GCNs.
- GCNs give up directionality to gain permutation invariance — this is the single most important conceptual bridge between the two architectures.
- The grid-graph exercise is a good sanity check: if someone claims "GCNs subsume CNNs," show them a Sobel filter.
</details>

---

*End of Part C.*

