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
> $1\times1$ conv 只在 channel 维度操作——对每个空间位置做跨 channel 的线性组合。空间维度 $H$ 和 $W$ 不变，只有 channel 数从 192 变为 64。

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
> 不做 normalization 时，有 100 个邻居的节点会累加 100 个 feature vector；只有 2 个邻居的节点只累加 2 个。各节点的 feature 处于完全不同的量级。Symmetric normalization 对每条边 $(i,j)$ 乘以 $1/\sqrt{d_i \cdot d_j}$，把 aggregation 变成加权平均，使所有节点不论 degree 大小都处于可比的尺度。

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
> Effective receptive field $= F + (F-1)(r-1) = 3 + 2\times2 = 7$。
> $r=3$ 时，filter 的采样点落在位置 $0, 3, 6$，跨度为 7。

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
> GCN aggregation 将节点自身与邻居的 feature 取平均。这在 **homophily**（相似节点相连，如引文网络或社交网络）下有利。在 **heterophily**（如二部图中相连节点类型总是不同）下，聚合邻居反而会让节点的表示远离正确类别，损害性能。

---

## Section B — Short Answer (30 pts)

---

**B1. (6 pts)** Explain weight sharing in CNNs: (i) what is it? (ii) how does it reduce parameter count vs MLP? (iii) how does it produce translation equivariance?

> [!success]- Answer
> 
> **(i) 什么是 weight sharing：**
> 同一组 filter 权重在滑动遍历输入的每个空间位置时被复用。所有输出位置共享一套权重，而不是每个位置各有独立权重。
> 
> **(ii) 参数量的减少：**
> 将 $256\times256\times3$ 的输入映射到 256 个神经元的 MLP 需要约 5000 万参数。256 个 $3\times3\times3$ filter 的 conv layer 只有 $256\times27 \approx 7{,}000$ 个参数——少约 7000 倍。参数量只取决于 filter 大小 $F^2 C_\text{in} C_\text{out}$，与图像尺寸 $HW$ 无关。
> 
> **(iii) Translation equivariance：**
> 因为每个位置使用相同的 filter，filter 相当于一个均匀的 pattern 检测器。如果某个 pattern 从 $(i,j)$ 移动到 $(i,j+5)$，filter 会在输出 feature map 的对应平移位置响应——检测结果相同，只是坐标改变了。

---

**B2. (8 pts)** Explain Spectral vs Spatial GCN: (i) define the graph Laplacian $\Delta$ and its eigendecomposition, (ii) in one sentence what does spectral graph convolution mean, (iii) why is Spatial GCN preferred in practice?

> [!success]- Answer
> 
> **(i) Graph Laplacian 和 eigendecomposition：**
> $$\Delta = I - D^{-1/2}AD^{-1/2}$$
> $\Delta$ 是对称半正定矩阵，因此：
> $$\Delta = \Phi\Lambda\Phi^\top$$
> 其中 $\Phi$ 的列为特征向量（图的 "Fourier basis"），$\Lambda$ 对角线为特征值（频率）。
> 
> **(ii) Spectral convolution 一句话：**
> 图上的 spectral convolution 是将信号的图 Fourier 变换 $(\Phi^\top h)$ 与可学习的 spectral filter $\hat{g}(\Lambda)$ 做逐元素乘法，再做逆变换——即空域卷积定理在图上的类比：*空域卷积 = 频域乘法*。
> 
> **(iii) 为什么 Spatial GCN 更常用：**
> 计算 $\Delta$ 的完整 eigendecomposition 需要 $O(N^3)$——对大规模图（数百万节点）完全不可行。Kipf 的 spatial propagation rule 复杂度为 $O(|E| \cdot D)$，与边数成正比，且无需对每种图结构重新计算特征向量，泛化性更好。

---

**B3. (8 pts)** A CNN's validation accuracy plateaus while training accuracy rises. Adding more filters doesn't help. Answer: (i) how do you distinguish overfitting from insufficient receptive field? (ii) three methods to increase receptive field with costs. (iii) if overfitting, why does more filters make it worse, and what should you do?

> [!success]- Answer
> 
> **(i) 区分两种原因：**
> - **Overfitting**：training loss 低但 validation loss 明显更高，gap 随 capacity 增加而扩大。
> - **Receptive field 不足**：training 和 validation loss 同时在较高值处 plateau。模型因"看不到"足够多的上下文而无法区分类别。诊断方法：把最后几个 conv layer 换成 global average pooling，若性能提升则是 receptive field 问题。
> 
> **(ii) 三种扩大 receptive field 的方法：**
> 
> | 方法 | 原理 | 代价 |
> |------|------|------|
> | 堆叠更多 conv layer | 每层在 receptive field 上增加 $F-1$ | 参数更多，gradient vanishing 风险，训练更慢 |
> | Stride $>1$ 或 Max Pooling | 空间下采样，后续层覆盖更多原始图像 | 丢失空间分辨率，细粒度细节被丢弃 |
> | Dilated Convolution | 在 filter 元素间插入间隔；$r=2$ 的 $3\times3$ 覆盖 $5\times5$ | 参数不变，但可能出现 checkerboard artifacts，dilation rate 需精心设计 |
> 
> **(iii) 为什么更多 filter 会加重 overfitting：**
> 更多 filter 增加了模型 capacity，而训练数据量不变。已经 overfit 的模型 capacity 已超出需要，继续增加只是提供更多空间记住噪声。正确做法：添加 Dropout、L2 regularization、data augmentation（随机裁剪、翻转、color jitter），或减少模型深度/宽度。

---

**B4. (8 pts)** Derive the GCN propagation formula step by step: (i) problem with $H^{l+1}=\sigma(AH^lW^l)$, (ii) what adding self-loops $\hat{A}=A+I$ fixes, (iii) what symmetric normalisation fixes and why symmetric rather than $\hat{D}^{-1}\hat{A}$.

> [!success]- Answer
> 
> **(i) 朴素 $\sigma(AH^lW^l)$ 的问题：**
> 乘以 $A$ 只聚合了邻居——节点自身被排除在外。经过一层后，节点 $i$ 的表示中没有自身之前的 feature，只有邻居的信息，对大多数任务来说是不可取的。
> 
> **(ii) Self-loops $\hat{A}=A+I$ 的作用：**
> 设 $\hat{A}_{ii}=1$，为每个节点添加一条指向自身的边。aggregation 现在包含节点自身的 feature：更新后的表示 = 自身 feature + 邻居 feature。
> 
> **(iii) Symmetric normalization 的作用：**
> **解决的问题：** 不做 normalization 时，有 100 个邻居的节点累加 100 个 feature vector，只有 2 个邻居的节点只累加 2 个，量级差异极大，训练不稳定。
> 
> **为什么用 symmetric（$\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$）而非 row-wise（$\hat{D}^{-1}\hat{A}$）：**
> Row-wise normalization 只从接收方（receiver）的角度 scale。Symmetric normalization 对边 $(i,j)$ 乘以 $1/\sqrt{d_i \cdot d_j}$，同时从发送方和接收方双向 scale。这保留了矩阵的对称性和半正定性，维护了 graph Laplacian 的 spectral 性质，训练更稳定。

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
> **要点：** padding 后 `x` 的 shape 变为 $(H+2P, W+2P)$，循环中要用 padding 后的 `x`。每个 patch 的起始位置是 `[i*stride, j*stride]`。`(patch * kernel).sum()` 计算的是 Frobenius inner product。

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
>     A_hat = A + torch.eye(N)                         # 添加 self-loops
>     deg = A_hat.sum(dim=1)                           # 每个节点的 degree
>     D_inv_sqrt = torch.diag(1.0 / deg.sqrt())        # D^{-1/2}
>     A_norm = D_inv_sqrt @ A_hat @ D_inv_sqrt          # symmetric normalization
>     return torch.relu(A_norm @ H @ W)                # 聚合 → 线性变换 → 激活
> ```
> 
> **要点：** `A_hat.sum(dim=1)` 给出每个节点的 degree。顺序很关键：先聚合（`A_norm @ H`），再做线性变换（`@ W`）。

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
> Max pooling 没有可学习参数。它提供 translation invariance 并缩减空间维度。

---

## Section D — Essay (35 pts)

---

**D1. (10 pts)** Compare MLP and CNN for image tasks across parameter count, spatial structure, and translation invariance. Define inductive bias, state CNN's inductive biases, and discuss when they become a limitation.

> [!success]- Answer
> 
> **对比：**
> 
> | 维度 | MLP | CNN |
> |------|-----|-----|
> | 参数量 | $O(HWC \cdot n_\text{out})$，256×256 图像约 2 亿 | $O(F^2 C_\text{in} C_\text{out})$，约 7K，与图像尺寸无关 |
> | 空间结构 | 图像被展平为 1D，像素邻接关系丢失 | Local connectivity 保留了 2D 邻域关系 |
> | Translation invariance | 无：同一 pattern 出现在不同位置 = 不同输入 | 近似：同一 filter 在任意位置都会响应 |
> 
> **Inductive bias：** 内嵌在模型架构中的先验假设，无需从数据中学习即可约束假设空间。
> 
> **CNN 的 inductive bias：**
> 1. *Locality*——相邻像素比远处像素更具信息量 → local receptive fields
> 2. *Translation equivariance*——同一 pattern 出现在任何位置应给出相同响应 → weight sharing
> 
> **何时成为局限：**
> 1. **全局依赖**：CNN 的 receptive field 只随深度缓慢增长。ViT 用 self-attention 直接关联任意两个 patch，更适合全局推理。
> 2. **位置本身有语义意义**：医学影像中，异常的精确位置是诊断关键，translation equivariance 会丢弃这一位置信息。
> 3. **非网格数据**：CNN 的滑动 filter 依赖规则网格，无法直接应用于点云、图或不规则传感器阵列。

---

**D2. (12 pts)** Explain why CNNs cannot handle graph data, how GCN generalises convolution to graphs, and what permutation equivariance means and why it matters.

> [!success]- Answer
> 
> **(i) 为什么 CNN 无法处理图数据：**
> CNN 假设：(a) **规则网格**——每个像素在固定的空间排列中有固定数量的邻居；(b) **标准排序**——"左"、"右"、"上"、"下"有明确定义。
> 
> 图数据两者都不满足：节点的 degree 可变（0 到数百个邻居），邻居之间没有自然顺序。固定大小的 convolutional filter 无从定义。
> 
> **(ii) GCN 如何将卷积推广到图：**
> 
> | | CNN | GCN |
> |---|---|---|
> | 聚合方式 | 固定 $F\times F$ 邻域 | 可变大小的邻居集合 |
> | Weight sharing | 每个位置用同一 filter | 每个节点用同一 $W^l$ |
> | 深度 | $k$ 层 → receptive field $k(F-1)+1$ | $k$ 层 → $k$-hop 邻域 |
> | 非线性 | ReLU | 相同 |
> 
> GCN 用图的邻接结构替代固定拓扑邻域。传播公式 $H^{l+1}=\sigma(\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}H^lW^l)$ 是一种可学习的、感知图拓扑的邻域聚合——即图上卷积的类比。
> 
> **(iii) Permutation equivariance：**
> 对节点重新标号（一致地置换 $A$ 的行列和 $H$ 的行），输出 feature 以相同方式置换。
> 
> 这一性质很重要，因为图没有标准节点顺序——同一分子或社交网络，不管节点如何标号，都应得到相同的表示。Permutation equivariance 保证了这一点。
> 
> *局限：* 纯邻域聚合无法区分某些结构不同的图（受 Weisfeiler-Leman isomorphism test 限制）。更强表达力的 GNN（GIN、高阶方法）以更高复杂度为代价解决了这一问题。

---

**D3. (13 pts)** Explain Group Convolution and Depthwise Separable Convolution with a quantitative parameter count comparison against standard convolution.

> [!success]- Answer
> 
> **Standard convolution 基准**（输入 $C_\text{in}$ 通道，输出 $C_\text{out}$ 通道，filter $F\times F$）：
> - 参数量：$F^2 C_\text{in} C_\text{out}$
> 
> ---
> 
> **Group Convolution（$G$ 组）：**
> 将 $C_\text{in}$ 分为 $G$ 组，每组有 $C_\text{in}/G$ 个输入通道和 $C_\text{out}/G$ 个输出通道，各组独立运算，输出拼接。
> - 参数量：$G \times F^2 \times (C_\text{in}/G) \times (C_\text{out}/G) = F^2 C_\text{in} C_\text{out}/G$
> - 减少比例：standard convolution 的 $1/G$
> 
> 当 $G = C_\text{in}$ 时 → **Depthwise Convolution**：每个 channel 有自己的 $F\times F$ filter，channels 之间不混合。
> - 参数量：$F^2 C_\text{in}$
> 
> ---
> 
> **Depthwise Separable Convolution = Depthwise + Pointwise：**
> 1. Depthwise Conv：$C_\text{in}$ 个 $F\times F$ filter → 输出 $(C_\text{in}, H, W)$，参数量 $= F^2 C_\text{in}$
> 2. Pointwise Conv：$1\times1$，$C_\text{out}$ 个输出通道 → 混合 channels，参数量 $= C_\text{in} C_\text{out}$
> 
> 总参数量：$C_\text{in}(F^2 + C_\text{out})$
> 
> 与 standard 的比值：$\dfrac{1}{C_\text{out}} + \dfrac{1}{F^2}$
> 
> 以 $F=3$，$C_\text{out}=256$ 为例：比值 $\approx \frac{1}{256} + \frac{1}{9} \approx \frac{1}{8.6}$——大约 **少 8–9 倍参数**。
> 
> ---
> 
> **应用场景：**
> Depthwise Separable Convolution 是 **MobileNet** 和 **Xception** 的核心模块，适用于移动端和 edge device 部署。核心思想：将空间过滤（depthwise）和 channel 混合（pointwise）分解为两个独立操作，在几乎不损失表达能力的前提下大幅压缩计算量和参数量。
