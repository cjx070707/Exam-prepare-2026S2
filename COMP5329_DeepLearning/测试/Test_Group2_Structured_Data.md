# Group 2 Test — Structured Data
**Week 4: CNN + Week 5: GNN**

---

## Section A — Multiple Choice (10 pts, 2 pts each)

---

**A1.** An input of size $28 \times 28$ passes through a conv layer with filter $3 \times 3$, padding $= 0$, stride $= 1$. Output size?

- (a) $28 \times 28$
- (b) $27 \times 27$
- (c) $26 \times 26$
- (d) $25 \times 25$

> [!success]- Answer
> 
> **(c) $26 \times 26$**
> 
> $\lfloor(28 - 3 + 0)/1\rfloor + 1 = 26$

---

**A2.** A $1\times1$ conv applied to $(N, 192, H, W)$ with 64 output channels produces shape:

- (a) $(N, 64, H, W)$
- (b) $(N, 192, H, W)$
- (c) $(N, 64, 1, 1)$
- (d) $(N, 192, 64, W)$

> [!success]- Answer
> 
> **(a) $(N, 64, H, W)$**
> 
> A $1\times1$ conv operates only in the channel dimension — a linear combination across channels at each spatial location. Spatial dimensions $H$ and $W$ are unchanged; only the channel count changes from 192 to 64.

---

**A3.** In Kipf & Welling's GCN, replacing symmetric normalisation $\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$ with unnormalised $\hat{A}$ causes:

- (a) The model loses the ability to aggregate neighbour information
- (b) High-degree nodes dominate — their aggregated features have much larger magnitude than low-degree nodes
- (c) The model becomes equivalent to a linear classifier
- (d) Gradient descent can no longer optimise the model

> [!success]- Answer
> 
> **(b)**
> 
> Without normalisation, a node with 100 neighbours sums 100 feature vectors; a node with 2 neighbours sums 2. Features are on completely different scales. Symmetric normalisation scales each edge $(i,j)$ by $1/\sqrt{d_i \cdot d_j}$, turning aggregation into a weighted average so all nodes are comparable regardless of degree.

---

**A4.** Dilated convolution with rate $r=3$ and filter size $F=3$ has effective receptive field:

- (a) $5 \times 5$
- (b) $7 \times 7$
- (c) $9 \times 9$
- (d) $11 \times 11$

> [!success]- Answer
> 
> **(b) $7 \times 7$**
> 
> Effective receptive field $= F + (F-1)(r-1) = 3 + 2\times2 = 7$.
> With $r=3$, filter elements sit at positions $0, 3, 6$ — spanning 7.

---

**A5.** Which statement best describes the key inductive bias of GNNs and when it fails?

- (a) GNNs can only process undirected graphs
- (b) GNNs aggregate neighbour features, assuming connected nodes share similar properties (homophily); this fails when neighbouring nodes are dissimilar
- (c) GNNs require all nodes to have the same feature dimension
- (d) GNNs cannot handle graphs with more than 1000 nodes

> [!success]- Answer
> 
> **(b)**
> 
> GCN aggregation averages a node's features with its neighbours'. This is beneficial under **homophily** (similar nodes connect, as in citation or social networks). Under **heterophily** (e.g. bipartite graphs where connected nodes are always different types), aggregating neighbours moves a node's representation further from the correct class, hurting performance.

---

## Section B — Short Answer (30 pts)

---

**B1. (6 pts)** Explain weight sharing in CNNs: (i) what is it? (ii) how does it reduce parameter count vs MLP? (iii) how does it produce translation equivariance?

> [!success]- Answer
> 
> **(i) What is weight sharing:**
> The same filter weights are used at every spatial position when sliding across the input. All output locations share one set of weights rather than having independent weights per position.
> 
> **(ii) Parameter reduction:**
> An MLP mapping $256\times256\times3$ input to 256 neurons needs ~50M parameters. A conv layer with 256 filters of $3\times3\times3$ has only $256\times27 \approx 7{,}000$ parameters — ~7000× fewer. Parameter count scales with filter size $F^2 C_\text{in} C_\text{out}$, not image size $HW C_\text{in} C_\text{out}$.
> 
> **(iii) Translation equivariance:**
> Because every position uses the same filter, the filter acts as a uniform pattern detector across the image. If a pattern shifts from $(i,j)$ to $(i, j+5)$, the filter fires at the new position in the output feature map at the corresponding shifted location. Detection result is the same — only its spatial coordinate changes.

---

**B2. (8 pts)** Explain Spectral vs Spatial GCN: (i) define the graph Laplacian $\Delta$ and its eigendecomposition, (ii) in one sentence what does spectral graph convolution mean, (iii) why is Spatial GCN preferred in practice?

> [!success]- Answer
> 
> **(i) Graph Laplacian and eigendecomposition:**
> $$\Delta = I - D^{-1/2}AD^{-1/2}$$
> $\Delta$ is symmetric positive semi-definite, so:
> $$\Delta = \Phi\Lambda\Phi^\top$$
> where $\Phi$ has eigenvectors as columns (graph "Fourier basis") and $\Lambda$ contains eigenvalues (frequencies).
> 
> **(ii) Spectral convolution in one sentence:**
> Graph convolution in the spectral domain is element-wise multiplication of the signal's graph Fourier transform $(\Phi^\top h)$ with a learnable spectral filter $\hat{g}(\Lambda)$, followed by the inverse transform — the graph-domain analogue of the convolution theorem: *convolution in space = multiplication in frequency*.
> 
> **(iii) Why Spatial GCN is preferred:**
> Computing the full eigendecomposition of $\Delta$ costs $O(N^3)$ — infeasible for large graphs (millions of nodes). Kipf's spatial propagation rule has complexity $O(|E| \cdot D)$ proportional to edges, and generalises across different graph structures without recomputing eigenvectors.

---

**B3. (8 pts)** A CNN's validation accuracy plateaus while training accuracy rises. Adding more filters doesn't help. Answer: (i) how do you distinguish overfitting from insufficient receptive field? (ii) three methods to increase receptive field with costs. (iii) if overfitting, why does more filters make it worse, and what should you do?

> [!success]- Answer
> 
> **(i) Distinguishing causes:**
> - **Overfitting**: large gap between low training loss and high validation loss. More capacity widens the gap further.
> - **Insufficient receptive field**: both training and validation loss plateau at a relatively high value. The model cannot distinguish classes because it cannot "see" enough context. Diagnostic: swap final conv layers for global average pooling and check if performance improves.
> 
> **(ii) Three methods to increase receptive field:**
> 
> | Method | How | Cost |
> |--------|-----|------|
> | Stack more conv layers | Each layer adds $F-1$ to receptive field | More parameters, gradient vanishing risk, slower training |
> | Stride $>1$ or Max Pooling | Spatially downsamples; subsequent layers cover more original image | Loss of spatial resolution; fine-grained details discarded |
> | Dilated Convolution | Inserts gaps between filter elements; $3\times3$ with $r=2$ covers $5\times5$ | Same parameters but checkerboard artefacts possible; dilation rates need careful design |
> 
> **(iii) Why more filters worsen overfitting:**
> More filters increase model capacity while training data stays fixed. An already overfit model has more capacity than needed; adding more just provides extra room to memorise noise. Correct approaches: add Dropout, L2 regularisation, data augmentation (random crops, flips, colour jitter), or reduce model depth/width.

---

**B4. (8 pts)** Derive the GCN propagation formula step by step: (i) problem with $H^{l+1}=\sigma(AH^lW^l)$, (ii) what adding self-loops $\hat{A}=A+I$ fixes, (iii) what symmetric normalisation fixes and why symmetric rather than $\hat{D}^{-1}\hat{A}$.

> [!success]- Answer
> 
> **(i) Problem with naive $\sigma(AH^lW^l)$:**
> Multiplying by $A$ aggregates only neighbours — the node itself is excluded. After one layer, node $i$'s representation contains no information about its own previous features, only its neighbours'. For most tasks this is undesirable.
> 
> **(ii) Self-loops $\hat{A}=A+I$:**
> Sets $\hat{A}_{ii}=1$, adding an edge from every node to itself. The aggregation now includes the node's own features: updated representation = self-feature + neighbour-features.
> 
> **(iii) Symmetric normalisation:**
> **What it fixes:** Without normalisation, a node with 100 neighbours accumulates 100 feature vectors; one with 2 accumulates only 2. Features are on vastly different scales, destabilising training.
> 
> **Why symmetric ($\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$) rather than row-wise ($\hat{D}^{-1}\hat{A}$):**
> Row-wise normalisation scales only from the receiver's perspective. Symmetric normalisation scales edge $(i,j)$ by $1/\sqrt{d_i \cdot d_j}$, normalising from both sender and receiver. This preserves the matrix's symmetry and positive semi-definiteness, keeping the spectral properties of the graph Laplacian intact and resulting in more stable training.

---

## Section C — Coding (25 pts)

---

**C1. (12 pts)** Implement 2D convolution forward pass from scratch (single-channel, double loop):

```python
def conv2d_forward(x, kernel, stride=1, padding=0):
    # x: (H_in, W_in),  kernel: (F, F)
    # returns: (H_out, W_out)
    pass
```

> [!success]- Answer
> 
> ```python
> import torch
> 
> def conv2d_forward(x, kernel, stride=1, padding=0):
>     H, W = x.shape
>     F = kernel.shape[0]
> 
>     if padding > 0:
>         x = torch.nn.functional.pad(x, [padding] * 4)
> 
>     H_out = (H + 2*padding - F) // stride + 1
>     W_out = (W + 2*padding - F) // stride + 1
>     output = torch.zeros(H_out, W_out)
> 
>     for i in range(H_out):
>         for j in range(W_out):
>             patch = x[i*stride : i*stride+F,
>                       j*stride : j*stride+F]
>             output[i, j] = (patch * kernel).sum()
> 
>     return output
> ```
> 
> **Key points:** after padding `x` has shape $(H+2P, W+2P)$ — use the padded `x` in the loop. Patch start: `[i*stride, j*stride]`. `(patch * kernel).sum()` is the Frobenius inner product.

---

**C2. (8 pts)** Implement one GCN layer forward pass:

```python
def gcn_forward(A, H, W):
    # A:(N,N) no self-loops,  H:(N,D_in),  W:(D_in,D_out)
    # returns (N, D_out)
    pass
```

> [!success]- Answer
> 
> ```python
> import torch
> 
> def gcn_forward(A, H, W):
>     N = A.shape[0]
>     A_hat = A + torch.eye(N)                         # add self-loops
>     deg = A_hat.sum(dim=1)                           # degree vector
>     D_inv_sqrt = torch.diag(1.0 / deg.sqrt())        # D^{-1/2}
>     A_norm = D_inv_sqrt @ A_hat @ D_inv_sqrt          # symmetric normalisation
>     return torch.relu(A_norm @ H @ W)                # propagate → linear → activate
> ```
> 
> **Key points:** `A_hat.sum(dim=1)` gives degree per node. Order matters: aggregate first (`A_norm @ H`), then transform (`@ W`).

---

**C3. (5 pts)** Implement Max Pooling forward (double loop):

```python
def max_pool2d(x, pool_size=2, stride=2):
    # x: (H, W) → (H_out, W_out)
    pass
```

> [!success]- Answer
> 
> ```python
> def max_pool2d(x, pool_size=2, stride=2):
>     H, W = x.shape
>     H_out = (H - pool_size) // stride + 1
>     W_out = (W - pool_size) // stride + 1
>     output = torch.zeros(H_out, W_out)
> 
>     for i in range(H_out):
>         for j in range(W_out):
>             patch = x[i*stride : i*stride+pool_size,
>                       j*stride : j*stride+pool_size]
>             output[i, j] = patch.max()
> 
>     return output
> ```
> 
> Max pooling has no learnable parameters. It provides translation invariance and reduces spatial dimensions.

---

## Section D — Essay (35 pts)

---

**D1. (10 pts)** Compare MLP and CNN for image tasks across parameter count, spatial structure, and translation invariance. Define inductive bias, state CNN's inductive biases, and discuss when they become a limitation.

> [!success]- Answer
> 
> **Comparison:**
> 
> | Dimension | MLP | CNN |
> |-----------|-----|-----|
> | Parameter count | $O(HWC \cdot n_\text{out})$ — ~200M for 256×256 image | $O(F^2 C_\text{in} C_\text{out})$ — ~7K, independent of image size |
> | Spatial structure | Image flattened to 1D; pixel adjacency lost | Local connectivity preserves 2D neighbourhood relationships |
> | Translation invariance | None: same pattern at different positions = different input | Approximate: same filter fires at any position |
> 
> **Inductive bias:** A prior assumption built into the model architecture that constrains the hypothesis space without requiring data to learn it.
> 
> **CNN's inductive biases:**
> 1. *Locality* — nearby pixels are more informative than distant ones → local receptive fields
> 2. *Translation equivariance* — same pattern anywhere → same response → weight sharing
> 
> **When they become a limitation:**
> 1. **Global dependencies**: CNN receptive fields grow only gradually through depth. ViT uses self-attention to directly relate any two patches, making global reasoning easier.
> 2. **Position is semantically important**: In medical imaging, the exact location of an abnormality is diagnostically critical. Translation equivariance discards this positional information.
> 3. **Non-grid data**: CNN's sliding-filter mechanism requires a regular grid. It cannot be applied to point clouds, graphs, or irregular sensor arrays without preprocessing.

---

**D2. (12 pts)** Explain why CNNs cannot handle graph data, how GCN generalises convolution to graphs, and what permutation equivariance means and why it matters.

> [!success]- Answer
> 
> **(i) Why CNNs fail on graphs:**
> CNNs assume: (a) a **regular grid** — every pixel has a fixed number of neighbours in a consistent spatial arrangement; (b) a **canonical ordering** — "left", "right", "up", "down" have well-defined meanings.
> 
> Neither holds for graphs: nodes have variable degree (0 to hundreds of neighbours), and there is no natural ordering of neighbours. A convolutional filter of fixed size cannot be defined.
> 
> **(ii) How GCN generalises convolution:**
> 
> | | CNN | GCN |
> |---|---|---|
> | Aggregation | Fixed $F\times F$ neighbourhood | Variable-size neighbour set |
> | Weight sharing | Same filter at every position | Same $W^l$ for every node |
> | Depth | $k$ layers → receptive field $k(F-1)+1$ | $k$ layers → $k$-hop neighbourhood |
> | Non-linearity | ReLU | Same |
> 
> GCN replaces the fixed-topology neighbourhood with the graph's adjacency structure. The propagation rule $H^{l+1}=\sigma(\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}H^lW^l)$ is a learned, graph-topology-aware neighbourhood aggregation — the graph-domain analogue of convolution.
> 
> **(iii) Permutation equivariance:**
> Relabelling nodes (permuting rows/columns of $A$ and rows of $H$ consistently) produces the same set of output features in the permuted order.
> 
> This is desirable because a graph has no canonical node ordering — the same molecule or social network should receive the same representation regardless of how nodes are labelled. Permutation equivariance guarantees this.
> 
> *Limitation*: pure neighbourhood aggregation cannot distinguish certain structurally different graphs (bounded by the Weisfeiler-Leman isomorphism test). More expressive GNNs (GIN, higher-order methods) address this at the cost of complexity.

---

**D3. (13 pts)** Explain Group Convolution and Depthwise Separable Convolution with a quantitative parameter count comparison against standard convolution.

> [!success]- Answer
> 
> **Standard convolution baseline** (input $C_\text{in}$ ch, output $C_\text{out}$ ch, filter $F\times F$):
> - Parameters: $F^2 C_\text{in} C_\text{out}$
> 
> ---
> 
> **Group Convolution ($G$ groups):**
> Partition $C_\text{in}$ into $G$ equal groups; each group has $C_\text{in}/G$ input and $C_\text{out}/G$ output channels and operates independently. Outputs are concatenated.
> - Parameters: $G \times F^2 \times (C_\text{in}/G) \times (C_\text{out}/G) = F^2 C_\text{in} C_\text{out}/G$
> - Reduction: $1/G$ of standard convolution
> 
> When $G = C_\text{in}$ → **Depthwise Convolution**: each channel gets its own $F\times F$ filter, channels never mix.
> - Parameters: $F^2 C_\text{in}$
> 
> ---
> 
> **Depthwise Separable Convolution = Depthwise + Pointwise:**
> 1. Depthwise Conv: $C_\text{in}$ filters of $F\times F$ → output $(C_\text{in}, H, W)$, params $= F^2 C_\text{in}$
> 2. Pointwise Conv: $1\times1$ with $C_\text{out}$ channels → mixes channels, params $= C_\text{in} C_\text{out}$
> 
> Total params: $C_\text{in}(F^2 + C_\text{out})$
> 
> Ratio vs standard: $\dfrac{1}{C_\text{out}} + \dfrac{1}{F^2}$
> 
> For $F=3$, $C_\text{out}=256$: ratio $\approx \frac{1}{256} + \frac{1}{9} \approx \frac{1}{8.6}$ — roughly **8–9× fewer parameters**.
> 
> ---
> 
> **Applications:**
> Depthwise Separable Convolution is the core building block of **MobileNet** (mobile/embedded deployment) and **Xception**. It achieves near-standard accuracy at a fraction of compute and memory, making it ideal for inference on resource-constrained hardware (smartphones, edge devices, IoT).
> The key insight: spatial filtering (depthwise) and channel mixing (pointwise) are separate concerns that can be factored without significant loss of expressiveness.
