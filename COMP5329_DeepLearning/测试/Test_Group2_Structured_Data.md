# Group 2 Test — Structured Data
**Week 4: CNN + Week 5: GNN**

---

## Section A — Multiple Choice (10 pts, 2 pts each)

---

**A1.** An input of size $28 \times 28$ passes through a convolutional layer with filter size $3 \times 3$, padding $= 0$, stride $= 1$. What is the output spatial size?

- (a) $28 \times 28$
- (b) $27 \times 27$
- (c) $26 \times 26$
- (d) $25 \times 25$

<details>
<summary>Answer</summary>

**(c) $26 \times 26$**

Output size $= \lfloor(W - F + 2P)/S\rfloor + 1 = (28 - 3 + 0)/1 + 1 = 26$.

</details>

---

**A2.** A $1 \times 1$ convolution applied to a feature map of shape $(N, 192, H, W)$ with 64 output channels produces output of shape:

- (a) $(N, 64, H, W)$
- (b) $(N, 192, H, W)$
- (c) $(N, 64, 1, 1)$
- (d) $(N, 192, 64, W)$

<details>
<summary>Answer</summary>

**(a) $(N, 64, H, W)$**

A $1\times1$ convolution operates only in the channel dimension — it is a linear combination across channels at each spatial location. Spatial dimensions $H$ and $W$ are unchanged; only the channel count changes from 192 to 64.

</details>

---

**A3.** In Kipf & Welling's GCN, if the symmetric normalisation $\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$ is replaced with the unnormalised $\hat{A}$, the main problem is:

- (a) The model loses the ability to aggregate neighbour information
- (b) High-degree nodes dominate — their aggregated features have much larger magnitude than low-degree nodes
- (c) The model becomes equivalent to a linear classifier
- (d) Gradient descent can no longer optimise the model

<details>
<summary>Answer</summary>

**(b)**

Without normalisation, a node with 100 neighbours sums 100 feature vectors; a node with 2 neighbours sums only 2. The resulting features are on completely different scales. Symmetric normalisation scales each entry by $1/\sqrt{d_i \cdot d_j}$, making the aggregation a weighted average (all nodes comparable regardless of degree).

</details>

---

**A4.** Dilated convolution with dilation rate $r = 3$ and filter size $F = 3$ has an effective receptive field of:

- (a) $5 \times 5$
- (b) $7 \times 7$
- (c) $9 \times 9$  
- (d) $11 \times 11$

<details>
<summary>Answer</summary>

**(b) $7 \times 7$**

Effective receptive field $= F + (F-1)(r-1) = 3 + 2 \times 2 = 7$.

With $r=3$, a $3\times3$ filter has gaps of 2 between each element, covering positions $0, 3, 6$ — a span of 7.

</details>

---

**A5.** Which statement best describes the key inductive bias of GNNs and when it fails?

- (a) GNNs can only process undirected graphs
- (b) GNNs aggregate features from neighbours, assuming connected nodes tend to share similar properties (homophily); this fails when neighbouring nodes are dissimilar
- (c) GNNs require all nodes to have the same feature dimension
- (d) GNNs cannot handle graphs with more than 1000 nodes

<details>
<summary>Answer</summary>

**(b)**

GCN-style aggregation averages a node's features with its neighbours'. This is beneficial under **homophily** (birds of a feather flock together — similar nodes connect to each other, as in citation networks or social networks). Under **heterophily** (e.g. bipartite graphs where connected nodes are always different types), aggregating neighbours actually moves a node's representation further from the correct class, hurting performance.

</details>

---

## Section B — Short Answer (30 pts)

---

**B1. (6 pts)** Explain weight sharing in CNNs and its two main benefits:

(i) What is weight sharing?
(ii) How does it reduce parameter count compared to an MLP? (Give a qualitative argument.)
(iii) How does it give the network approximate translation equivariance?

<details>
<summary>Answer</summary>

**(i) What is weight sharing:**
The same set of weights (a filter / convolutional kernel) is used at every spatial position when sliding across the input. Rather than each output location having its own independent set of weights, all locations share one filter.

**(ii) Parameter reduction vs MLP:**
An MLP with input $256 \times 256 \times 3 = 196{,}608$ and 256 output neurons requires $\approx 50\text{M}$ parameters for the first layer. A convolutional layer with 256 filters of size $3 \times 3 \times 3$ has only $256 \times 27 \approx 7{,}000$ parameters — a reduction of roughly $7{,}000\times$. The key insight: parameter count scales with filter size ($F^2 \cdot C_\text{in} \cdot C_\text{out}$), not with image size ($H \cdot W \cdot C_\text{in} \cdot C_\text{out}$).

**(iii) Translation equivariance:**
Because every spatial location uses the same filter weights, the filter acts as a uniform "pattern detector" across the image. If a pattern (e.g. a horizontal edge) shifts from position $(i,j)$ to $(i, j+5)$, the filter will fire at the new position in the output feature map at the corresponding shifted location. The detection result is the same — only its spatial coordinate changes. This is translation equivariance: shifting the input shifts the output but does not change what is detected.

</details>

---

**B2. (8 pts)** Explain the core ideas of Spectral and Spatial GCN, and their trade-offs:

(i) Define the graph Laplacian $\Delta$ and write its eigendecomposition.
(ii) In one sentence, what does spectral-domain graph convolution mean (analogous to classical signal processing)?
(iii) Why is Spatial GCN preferred in practice? (Computational complexity perspective.)

<details>
<summary>Answer</summary>

**(i) Graph Laplacian and eigendecomposition:**

The normalised graph Laplacian:
$$\Delta = I - D^{-1/2}AD^{-1/2}$$
where $D$ is the diagonal degree matrix. $\Delta$ is symmetric positive semi-definite, so it admits an eigendecomposition:
$$\Delta = \Phi \Lambda \Phi^\top$$
where $\Phi \in \mathbb{R}^{N \times N}$ has eigenvectors as columns (the graph's "Fourier basis") and $\Lambda$ is a diagonal matrix of eigenvalues (analogous to frequencies).

**(ii) Spectral-domain convolution in one sentence:**
Graph convolution in the spectral domain is the point-wise multiplication of the signal's graph Fourier transform $(\Phi^\top h)$ with a learnable spectral filter $\hat{g}(\Lambda)$, followed by the inverse transform $(\Phi)$ — exactly the convolution theorem: *convolution in the spatial domain equals multiplication in the frequency domain*.

**(iii) Why Spatial GCN is preferred:**
Computing the full eigendecomposition of $\Delta$ costs $O(N^3)$, which is completely infeasible for large graphs (e.g. a social network with millions of nodes). Spatial GCN (Kipf's propagation rule) directly aggregates neighbours in the graph domain with complexity $O(|E| \cdot D)$ proportional to the number of edges, and generalises across different graph structures without recomputing eigenvectors.

</details>

---

**B3. (8 pts)** A CNN classifier's validation accuracy plateaus while training accuracy keeps improving. You increase the number of filters but performance does not improve. Answer:

(i) How can you distinguish between overfitting and insufficient receptive field as causes of this behaviour?
(ii) If the cause is insufficient receptive field, list three methods to increase it and state one cost of each.
(iii) If the cause is overfitting, why does increasing filter count make things worse, and what should you do instead?

<details>
<summary>Answer</summary>

**(i) Distinguishing the two causes:**
- **Overfitting**: large gap between training loss (low) and validation loss (high). The model has memorised training data. Increasing capacity widens the gap further.
- **Insufficient receptive field**: both training and validation loss plateau at a relatively high value — the model cannot distinguish classes because it cannot "see" enough context. Validation loss does not worsen with more capacity; it simply fails to improve. Diagnostic: compare performance when replacing the final conv layers with a global average pool (forces global context), or visualise feature map activation patterns.

**(ii) Three methods to increase receptive field:**

| Method | How it works | Cost |
|--------|-------------|------|
| Stack more conv layers | Each layer adds $F-1$ to the receptive field | Deeper network, more parameters, gradient vanishing risk |
| Stride $> 1$ or Max Pooling | Spatially downsamples feature maps; subsequent layers cover more of the original image | Loss of spatial resolution; fine-grained details are discarded |
| Dilated (Atrous) Convolution | Inserts gaps between filter elements; a $3\times3$ filter with $r=2$ covers $5\times5$ | Same parameter count but can introduce checkerboard artefacts; dilation rates must be carefully designed |

**(iii) Why more filters worsen overfitting:**
More filters increase the model's capacity — the number of parameters grows, while the training data remains fixed. An overfit model already has more capacity than needed to memorise the training set; adding more capacity just gives it more "room" to memorise more idiosyncratic noise, making generalisation worse.

Correct approaches: add Dropout, L2 regularisation, data augmentation (random crops, flips, colour jitter), or reduce model depth/width.

</details>

---

**B4. (8 pts)** Derive the GCN propagation formula step by step:

$$H^{l+1} = \sigma\!\left(\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2} H^l W^l\right)$$

(i) What is wrong with the naive rule $H^{l+1} = \sigma(AH^lW^l)$?
(ii) What does adding self-loops $\hat{A} = A + I$ fix?
(iii) What does symmetric normalisation $\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$ fix, and why symmetric rather than $\hat{D}^{-1}\hat{A}$?

<details>
<summary>Answer</summary>

**(i) Problem with $H^{l+1} = \sigma(AH^lW^l)$:**
Multiplying by $A$ aggregates only the features of a node's neighbours — the node itself is excluded. After one layer, node $i$'s new representation contains no information about its own previous features, only about its neighbours'. For most tasks this is undesirable.

**(ii) Self-loops $\hat{A} = A + I$:**
Setting $\hat{A}_{ii} = 1$ adds an edge from every node to itself. The aggregation now includes the node's own features alongside its neighbours'. Updated representation = self-feature + neighbour-features, which is the natural analogue of "a pixel's new feature depends on itself and its neighbours".

**(iii) Symmetric normalisation:**

*What it fixes:* Without normalisation, a node with 100 neighbours accumulates 100 feature vectors; a node with 2 neighbours accumulates only 2. The resulting embeddings are on vastly different scales, destabilising training and making comparisons across nodes meaningless. Normalisation turns the aggregation into a weighted average, making all nodes comparable.

*Why symmetric ($\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$) rather than row-wise ($\hat{D}^{-1}\hat{A}$):*
Row-wise normalisation $\hat{D}^{-1}\hat{A}$ normalises from the receiver's perspective only — when a high-degree sender $i$ contributes to a low-degree receiver $j$, the contribution is divided by $j$'s degree but not $i$'s. Symmetric normalisation scales the edge weight $(i,j)$ by $1/\sqrt{d_i \cdot d_j}$, normalising from both ends. This preserves the matrix's symmetry and positive semi-definiteness, keeping the nice spectral properties of the graph Laplacian and resulting in more stable training.

</details>

---

## Section C — Coding (25 pts)

---

**C1. (12 pts)** Implement 2D convolution forward pass from scratch (single-channel, double loop):

```python
def conv2d_forward(x, kernel, stride=1, padding=0):
    """
    x:       (H_in, W_in)   input feature map
    kernel:  (F, F)          square convolution kernel
    Returns: (H_out, W_out)
    """
    pass
```

Requirements: manually handle padding; use a double loop; output size formula: $\lfloor(H + 2P - F)/S\rfloor + 1$.

<details>
<summary>Answer</summary>

```python
import torch

def conv2d_forward(x, kernel, stride=1, padding=0):
    H, W = x.shape
    F = kernel.shape[0]

    if padding > 0:
        x = torch.nn.functional.pad(x, [padding] * 4)  # pad all four sides

    H_out = (H + 2 * padding - F) // stride + 1
    W_out = (W + 2 * padding - F) // stride + 1
    output = torch.zeros(H_out, W_out)

    for i in range(H_out):
        for j in range(W_out):
            # Extract patch starting at (i*stride, j*stride)
            patch = x[i*stride : i*stride + F,
                      j*stride : j*stride + F]   # shape (F, F)
            output[i, j] = (patch * kernel).sum()  # element-wise multiply then sum

    return output
```

**Key points:**
- After padding, `x` shape becomes $(H + 2P, W + 2P)$ — use the padded `x` in the loop
- Patch start: `[i*stride, j*stride]`; patch end: `[i*stride + F, j*stride + F]`
- `(patch * kernel).sum()` is the Frobenius inner product (equivalent to dot product)

</details>

---

**C2. (8 pts)** Implement one GCN layer forward pass from scratch:

```python
def gcn_forward(A, H, W):
    """
    A: (N, N)     adjacency matrix (no self-loops)
    H: (N, D_in)  node feature matrix
    W: (D_in, D_out)  learnable weight matrix
    Returns: (N, D_out)
    """
    # Step 1: add self-loops
    # Step 2: compute degree matrix
    # Step 3: symmetric normalisation
    # Step 4: propagate, linear transform, activate
    pass
```

<details>
<summary>Answer</summary>

```python
import torch

def gcn_forward(A, H, W):
    N = A.shape[0]

    # Step 1: add self-loops  Â = A + I
    A_hat = A + torch.eye(N)

    # Step 2: degree matrix  D̂_ii = sum of row i of Â
    deg = A_hat.sum(dim=1)               # (N,)
    D_hat = torch.diag(deg)              # (N, N)

    # Step 3: symmetric normalisation  D̂^{-1/2} Â D̂^{-1/2}
    D_inv_sqrt = torch.diag(1.0 / deg.sqrt())
    A_norm = D_inv_sqrt @ A_hat @ D_inv_sqrt   # (N, N)

    # Step 4: aggregate, linear transform, activate
    return torch.relu(A_norm @ H @ W)          # (N, D_out)
```

**Key points:**
- `A_hat.sum(dim=1)` gives the degree of each node in the self-loop graph
- `D_inv_sqrt` is computed element-wise on the diagonal (no matrix inversion needed)
- Order matters: aggregate first (`A_norm @ H`), then transform (`@ W`)

</details>

---

**C3. (5 pts)** Implement Max Pooling forward pass (double loop):

```python
def max_pool2d(x, pool_size=2, stride=2):
    """
    x:         (H, W)
    Returns:   (H_out, W_out)
    """
    pass
```

<details>
<summary>Answer</summary>

```python
def max_pool2d(x, pool_size=2, stride=2):
    H, W = x.shape
    H_out = (H - pool_size) // stride + 1
    W_out = (W - pool_size) // stride + 1
    output = torch.zeros(H_out, W_out)

    for i in range(H_out):
        for j in range(W_out):
            patch = x[i*stride : i*stride + pool_size,
                      j*stride : j*stride + pool_size]
            output[i, j] = patch.max()

    return output
```

**Note:** Max pooling has no learnable parameters. It provides translation invariance (not just equivariance) and reduces spatial dimensions, decreasing computation in subsequent layers.

</details>

---

## Section D — Essay (35 pts)

---

**D1. (10 pts)** Compare MLP and CNN for image tasks across three dimensions — parameter count, spatial structure, and translation invariance — and discuss when CNN's inductive biases become a limitation.

<details>
<summary>Answer</summary>

**Three-dimensional comparison:**

| Dimension | MLP | CNN |
|-----------|-----|-----|
| Parameter count | $O(H \cdot W \cdot C \cdot n_\text{out})$ — enormous; 200M+ for a 256×256 image | $O(F^2 \cdot C_\text{in} \cdot C_\text{out})$ — tiny; independent of image resolution |
| Spatial structure | Image flattened to 1D; adjacency of pixels is lost; same pixel values at different positions are treated as different inputs | Local connectivity preserves 2D neighbourhood; adjacent pixels are naturally related via the receptive field |
| Translation invariance | None: a cat at position $(i,j)$ and at $(i',j')$ produce entirely different activations | Approximate (exact equivariance per layer; global average pooling or CLS token adds invariance) |

**Inductive bias and when it is a limitation:**

CNN encodes two priors: *locality* (nearby pixels are more related) and *translation equivariance* (same pattern anywhere → same response). These are almost always correct for natural images and allow CNNs to generalise from small datasets.

However, these biases become limitations when:

1. **Global context matters**: CNN receptive fields grow only gradually through depth. Long-range dependencies (e.g. relating the sky in the top half to the sea in the bottom half) are difficult to capture without very deep networks. Vision Transformers (ViT) use self-attention to directly relate any two patches in a single layer, making long-range modelling easier.

2. **Position is semantically meaningful**: In medical imaging, the precise location of an abnormality can be diagnostically critical. Translation equivariance discards positional information that may be important.

3. **Non-grid-structured data**: CNN's sliding-filter mechanism fundamentally requires a regular grid. It cannot be applied to point clouds, graphs, or irregular sensor layouts without preprocessing.

</details>

---

**D2. (12 pts)** Explain why CNNs cannot directly handle graph data, how GCN generalises the convolution idea to graphs, and what it means for GCN to be permutation invariant.

<details>
<summary>Answer</summary>

**(i) Why CNNs fail on graphs:**

CNNs implicitly assume two structural properties:
- A **regular grid**: every node (pixel) has the same number of neighbours (up to 8 for 2D), and these neighbours are arranged in a consistent spatial pattern.
- A **canonical ordering**: "left", "right", "up", "down" have well-defined meanings; the 3rd element of a 3×3 patch is always the top-right.

Neither holds for graphs: nodes have variable degree (0 to hundreds of neighbours), and there is no natural ordering of those neighbours. A convolutional filter of fixed size cannot be applied in a well-defined way.

**(ii) How GCN generalises convolution to graphs:**

| | CNN | GCN |
|---|---|---|
| Aggregation | Fixed $F \times F$ neighbourhood, element-wise weighted sum | Variable-size neighbour set, sum/average over all neighbours |
| Weight sharing | Same filter weights at every spatial position | Same weight matrix $W^l$ for every node |
| Depth = receptive field | $k$ layers → receptive field $k(F-1)+1$ | $k$ layers → aggregates $k$-hop neighbourhood |
| Non-linearity | ReLU after each layer | Same |

GCN replaces the fixed-topology neighbourhood with the graph's adjacency structure. Instead of "which pixel is 3 steps to the right", it asks "which nodes are connected". The propagation rule $H^{l+1} = \sigma(\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2} H^l W^l)$ is a learned, graph-topology-aware neighbourhood aggregation — the graph-domain analogue of convolution.

**(iii) Permutation invariance:**

GCN is permutation equivariant: relabelling the nodes (permuting rows and columns of $A$ and rows of $H$ consistently) produces the same set of output features, just in the permuted order. Node-level tasks are thus permutation equivariant; graph-level tasks (using a global aggregation like sum-pooling over nodes) are permutation invariant.

This is desirable because a graph has no canonical node ordering — the same molecule or social network should receive the same representation regardless of how we label its nodes. Permutation equivariance guarantees this, unlike an MLP applied to a flattened adjacency matrix (which would treat two orderings of the same graph as completely different inputs).

*Potential limitation*: pure neighbourhood aggregation can fail to distinguish structurally different graphs (the Weisfeiler-Leman graph isomorphism test shows the limits). More expressive GNNs (Graph Isomorphism Network, higher-order methods) address this at the cost of complexity.

</details>

---

**D3. (13 pts)** Explain Group Convolution and Depthwise Separable Convolution, including a quantitative comparison of parameter count and computation with standard convolution.

<details>
<summary>Answer</summary>

**Standard convolution baseline** (input: $C_\text{in}$ channels, output: $C_\text{out}$ channels, filter: $F \times F$, spatial size $H \times W$):
- Parameters: $F^2 \cdot C_\text{in} \cdot C_\text{out}$
- Multiply-adds: $F^2 \cdot C_\text{in} \cdot C_\text{out} \cdot H \cdot W$

---

**Group Convolution ($G$ groups):**

Partition the $C_\text{in}$ input channels into $G$ equal groups. Each group has $C_\text{in}/G$ input channels and $C_\text{out}/G$ output channels; the $G$ groups operate independently in parallel, and their outputs are concatenated.

- Parameters: $G \times F^2 \times (C_\text{in}/G) \times (C_\text{out}/G) = F^2 \cdot C_\text{in} \cdot C_\text{out} / G$
- Reduction: $1/G$ of standard convolution

**Depthwise Convolution** is Group Convolution with $G = C_\text{in}$: each input channel gets its own independent $F \times F$ filter; channels do not mix.
- Parameters: $F^2 \cdot C_\text{in}$ (one filter per channel)

---

**Depthwise Separable Convolution = Depthwise + Pointwise:**

1. **Depthwise Conv**: $C_\text{in}$ independent $F \times F$ filters → output $(C_\text{in}, H, W)$, parameters $= F^2 C_\text{in}$
2. **Pointwise Conv**: $1 \times 1$ conv with $C_\text{out}$ output channels → mixes channel information, parameters $= C_\text{in} \cdot C_\text{out}$

Total parameters: $C_\text{in}(F^2 + C_\text{out})$

Ratio vs standard convolution:
$$\frac{C_\text{in}(F^2 + C_\text{out})}{F^2 C_\text{in} C_\text{out}} = \frac{1}{C_\text{out}} + \frac{1}{F^2}$$

For $F=3$, $C_\text{out}=256$: ratio $\approx 1/9$ — roughly 8–9× fewer parameters and FLOPs.

---

**Applications:**

Depthwise Separable Convolution is the core building block of **MobileNet** (designed for mobile and embedded devices) and also appears in **Xception** and **EfficientNet**. It achieves near-standard-convolution accuracy at a fraction of the compute and memory cost, making it ideal for inference on resource-constrained hardware (smartphones, edge devices, IoT sensors).

The key insight: spatial filtering (depthwise) and channel mixing (pointwise) are separate concerns that can be factored without significant loss of expressiveness.

</details>
