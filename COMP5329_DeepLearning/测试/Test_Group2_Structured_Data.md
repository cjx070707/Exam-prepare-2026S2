# Group 2 专项测试 — Structured Data
**Week 4: CNN + Week 5: GNN**

> 先做题，再看答案。目标：每题都能不看笔记作答。

---

## Part A — 单选题（10 分，每题 2 分）

**A1.** An input of size $28 \times 28$ passes through a conv layer with filter size $3 \times 3$, padding $= 0$, stride $= 1$. What is the output size?

- (a) $28 \times 28$
- (b) $27 \times 27$
- (c) $26 \times 26$
- (d) $25 \times 25$

---

**A2.** A $1 \times 1$ convolution applied to a feature map of shape $(N, 192, H, W)$ with 64 output channels produces an output of shape:

- (a) $(N, 64, H, W)$
- (b) $(N, 192, H, W)$
- (c) $(N, 64, 1, 1)$
- (d) $(N, 192, 64, W)$

---

**A3.** In Kipf & Welling's GCN, the propagation rule is $H^{l+1} = \sigma(\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2} H^l W^l)$. If the symmetric normalisation $\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$ is replaced with the unnormalised $\hat{A}$, what is the main problem?

- (a) The model loses the ability to learn from neighbours
- (b) High-degree nodes will dominate — their aggregated features will have much larger magnitude than low-degree nodes
- (c) The model becomes equivalent to a linear classifier
- (d) The model can no longer be trained with gradient descent

---

**A4.** Dilated convolution with dilation rate $r=3$ and filter size $F=3$ has an effective receptive field size of:

- (a) $5 \times 5$
- (b) $7 \times 7$
- (c) $9 \times 9$
- (d) $11 \times 11$

---

**A5.** Which of the following best describes the key inductive bias of GNNs that makes them unsuitable for data where the homophily assumption fails?

- (a) GNNs can only process undirected graphs
- (b) GNNs aggregate features from neighbours, assuming connected nodes tend to share similar properties
- (c) GNNs require fixed-size input graphs
- (d) GNNs cannot handle node features with different dimensions

---

## Part B — 简答题（30 分）

**B1. (6 分)** 解释 CNN 中 weight sharing（权重共享）的含义及其两个主要好处：

(i) 什么是 weight sharing？（用卷积的角度描述）  
(ii) 它如何大幅减少参数量？（与 MLP 对比，给出定性分析）  
(iii) 它如何赋予网络平移等变性？

---

**B2. (8 分)** 解释 Spectral GCN 和 Spatial GCN 的核心思想与区别：

(i) Spectral GCN 的图傅里叶变换是什么？图拉普拉斯矩阵 $\Delta$ 的特征分解是什么？  
(ii) 用一句话说明谱域卷积的含义（类比经典信号处理）  
(iii) 为什么实际中更常用 Spatial GCN？（从计算复杂度角度回答）

---

**B3. (8 分)** 一个 CNN 模型用于图像分类，你发现验证集精度饱和但训练集精度仍在上升。你决定加大 filter 数量来提升模型容量，但效果没有改善。

回答以下问题：

(i) 过拟合和"感受野不足"都可能导致类似现象，如何区分这两种情况？  
(ii) 如果问题是"感受野不足"（模型看不到足够大的上下文），列出三种扩大感受野的方法，并说明各自的代价。  
(iii) 如果问题是过拟合，加大 filter 数量为什么无效？应该怎么做？

---

**B4. (8 分)** GCN 的核心传播公式是：

$$H^{l+1} = \sigma\!\left(\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2} H^l W^l\right)$$

逐步解释这个公式的构建过程：

(i) 最简单的传播规则是 $H^{l+1} = \sigma(AH^lW^l)$，它有什么问题？  
(ii) 加入自环 $\hat{A} = A + I$ 解决了什么？  
(iii) 对称归一化 $\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$ 解决了什么？为什么是"对称"而不是 $\hat{D}^{-1}\hat{A}$？

---

## Part C — 手写代码（25 分）

**C1. (12 分)** 从空白实现 2D 卷积前向计算（双重循环版本，单通道）：

```python
def conv2d_forward(x, kernel, stride=1, padding=0):
    """
    x:      (H_in, W_in)      输入特征图（单通道）
    kernel: (F, F)             卷积核（正方形）
    stride: int
    padding: int               补零的圈数
    返回:   (H_out, W_out)     输出特征图
    """
    pass
```

要求：
- 手动实现 padding（用 `torch.zeros` 或 `F.pad`）
- 用双重循环逐位置计算
- 输出尺寸公式：$\lfloor(H + 2P - F) / S\rfloor + 1$

---

**C2. (8 分)** 从空白实现 GCN 一层前向传播：

```python
def gcn_forward(A, H, W):
    """
    A: (N, N)     邻接矩阵（无自环）
    H: (N, D_in)  节点特征矩阵
    W: (D_in, D_out) 可学习权重
    返回: (N, D_out) 下一层节点特征
    """
    # Step 1: 加自环
    # Step 2: 计算度矩阵
    # Step 3: 对称归一化
    # Step 4: 传播 + 线性变换 + 激活
    pass
```

---

**C3. (5 分)** 实现 Max Pooling 前向计算（双重循环版本）：

```python
def max_pool2d(x, pool_size=2, stride=2):
    """
    x:         (H, W)
    pool_size: int
    stride:    int
    返回:      (H_out, W_out)
    """
    pass
```

---

## Part D — 论述题（35 分）

**D1. (10 分)** 比较 MLP 和 CNN 在处理图像时的根本区别：

- 从参数量、空间关系、平移不变性三个维度对比
- 解释什么是 inductive bias，以及 CNN 的 inductive bias 是什么
- 讨论 CNN 的 inductive bias 在什么情况下反而是一种"限制"

---

**D2. (12 分)** 解释为什么 CNN 不能直接处理图数据，以及 GCN 是如何解决这个问题的：

(i) CNN 隐含了什么关于数据结构的假设？这些假设在图数据上为什么不成立？  
(ii) GCN 的"聚合邻居"操作与 CNN 的"滑动 filter"操作有什么相似之处？  
(iii) GCN 是置换不变（permutation invariant）的——解释这意味着什么，以及这对图学习任务是否是好事？

---

**D3. (13 分)** Group Convolution 和 Depthwise Separable Convolution：

(i) 解释什么是 Group Convolution（$G$ 组时参数量如何变化？）  
(ii) 当 $G = C$（通道数）时，退化为什么操作？  
(iii) Depthwise Separable Convolution = Depthwise Conv + Pointwise Conv。用参数量和计算量说明它与标准卷积的区别（以输入 $C_\text{in}$ 通道、输出 $C_\text{out}$ 通道、filter $F \times F$ 为例）  
(iv) 这种设计被广泛用于什么场景？为什么？

---

---

# 参考答案

---

## Part A

| 题号 | 答案 | 计算/理由 |
|------|------|---------|
| A1 | **(c)** | $(28 - 3 + 0)/1 + 1 = 26$ |
| A2 | **(a)** | $1\times1$ conv 只改变 channel 数，不改变 $H, W$ |
| A3 | **(b)** | 度大的节点聚合后特征值 $\propto$ degree，破坏量纲一致性 |
| A4 | **(b)** | $F + (F-1)(r-1) = 3 + 2 \times 2 = 7$，即 $7 \times 7$ |
| A5 | **(b)** | GCN 假设相邻节点特征相似（homophily）；若相邻节点差异大（heterophily），聚合邻居反而会混淆特征 |

---

## Part B 参考答案

### B1 — Weight Sharing

**(i) 什么是 weight sharing：**  
同一个卷积核（filter）在输入特征图的所有空间位置上滑动时使用完全相同的一组权重。无论 filter 在左上角还是右下角，都用同一套参数做点积运算。

**(ii) 减少参数量：**  
一个 MLP 的第一层若输入 $256 \times 256 \times 3 = 196608$ 个特征，输出 256 个神经元，需要约 $5000$ 万参数。相比之下，一个 $3 \times 3 \times 3$ 的卷积核只有 27 个参数，即使有 256 个这样的 filter 也只有 $27 \times 256 \approx 7000$ 个参数——减少了约 7000 倍。参数量从 $O(H \cdot W \cdot C \cdot n_\text{out})$ 降到 $O(F^2 \cdot C \cdot n_\text{filters})$。

**(iii) 平移等变性：**  
由于同一 filter 在所有位置共享，当输入中的某个模式（如一条边）从左移到右，filter 在新的位置同样能检测到它，并在输出特征图的对应位置激活。即输入的平移导致输出特征图的对应平移，而不改变检测结果。这使得"猫在左上角"和"猫在右下角"被同样的 filter 激活，只是激活位置不同。

---

### B2 — Spectral vs Spatial GCN

**(i) 图傅里叶变换与 Laplacian 特征分解：**

图拉普拉斯矩阵：$\Delta = I - D^{-1/2}AD^{-1/2}$

特征分解（$\Delta$ 是对称半正定矩阵）：
$$\Delta = \Phi \Lambda \Phi^\top$$
其中 $\Phi$ 的列是特征向量（图的"频率基"），$\Lambda$ 是对角矩阵（特征值，对应各频率的大小）。

图傅里叶变换：将节点信号 $h$ 投影到特征向量基上：$\hat{h} = \Phi^\top h$

**(ii) 谱域卷积的含义：**  
图上的卷积 = 在频域（特征向量空间）中的逐点乘积，然后变换回空间域：
$$h^{l+1} = \sigma(\Phi \, \hat{w}(\Lambda) \, \Phi^\top h^l)$$
这是经典卷积定理（"时域卷积 = 频域乘积"）在图上的推广。

**(iii) 实际更常用 Spatial GCN 的原因：**  
谱域方法需要对拉普拉斯矩阵做完整特征分解，复杂度为 $O(N^3)$——节点数多时完全不可接受。此外，学到的 filter 依赖特定图的拉普拉斯矩阵，无法迁移到不同结构的图。Spatial GCN 直接在空间域聚合邻居，复杂度 $O(|E| \cdot D)$（$E$ 是边数），且对不同图结构通用。

---

### B3 — 过拟合 vs 感受野不足

**(i) 如何区分：**

- **过拟合**：训练集损失低、验证集损失高，两者差距随训练持续扩大。增大模型容量通常会让验证集更差。
- **感受野不足**：训练集和验证集的损失都停滞在较高水平——不是泛化问题，而是模型根本看不到做决策所需的上下文（比如分类"足球场"需要看全局，而感受野只有小 patch）。可以通过可视化特征图或对比使用全局 pooling 时的精度来诊断。

**(ii) 三种扩大感受野的方法：**

| 方法 | 原理 | 代价 |
|------|------|------|
| 堆叠更多卷积层 | 每层感受野线性增大 | 更深的网络，梯度消失风险，训练更慢 |
| Max Pooling 或 Stride > 1 | 下采样缩小空间尺寸，后续层感受野覆盖原始更大范围 | 损失空间分辨率，细节信息丢失 |
| Dilated (Atrous) Convolution | 在 filter 元素间插入空洞，$3\times3$ filter 覆盖 $7\times7$ 区域 | 参数不变，但可能引入"棋盘格"伪影；需要合理设置 dilation rate |

**(iii) 过拟合时加大 filter 无效的原因：**  
过拟合是模型容量相对数据量过大，加大 filter 数量进一步增大容量，过拟合只会更严重。应该：
- 加 Dropout / L2 正则化
- 数据增强（随机裁剪、翻转等）
- 减小模型容量（减少 filter 数量、减层）
- 收集更多训练数据

---

### B4 — GCN 传播公式的构建逻辑

**(i) $H^{l+1} = \sigma(AH^lW^l)$ 的问题：**  
乘以 $A$ 只聚合了邻居节点的特征，没有包含节点本身的信息。一个节点更新后的表示完全取决于邻居，而与自己当前的特征无关，这在大多数任务下是不合理的。

**(ii) 加自环 $\hat{A} = A + I$ 的作用：**  
$\hat{A}_{ii} = 1$ 意味着每个节点都有一条指向自身的边，聚合时会包含节点自身的特征。更新后的表示 = 自身特征 + 邻居特征的聚合，更符合实际需求。

**(iii) 对称归一化的作用及为何是"对称"：**  

**解决问题**：度大的节点（邻居多）聚合后，特征向量的每个分量会累加更多项，数值更大，与度小的节点完全不在同一量纲上，破坏训练稳定性。归一化让每个节点的聚合结果是邻居特征的**加权平均**（权重与度成反比），而非加权求和。

**为何对称而非 $\hat{D}^{-1}\hat{A}$（随机游走归一化）：**  
$\hat{D}^{-1}\hat{A}$ 是非对称矩阵，它会让高度节点的特征被稀释（除以大度数），但低度节点收到高度节点的贡献时没有对应的稀释，不对称。$\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$ 是对称的半正定矩阵，保持了谱图理论中的良好性质（特征值实数、可谱分解），且聚合是双向归一化的——节点 $i$ 给节点 $j$ 的贡献同时被 $i$ 和 $j$ 的度数归一化。

---

## Part C 参考答案

### C1 — 2D 卷积前向计算

```python
import torch

def conv2d_forward(x, kernel, stride=1, padding=0):
    H, W = x.shape
    F = kernel.shape[0]

    # 补零
    if padding > 0:
        x = torch.nn.functional.pad(x, [padding] * 4)  # 四周各补 padding 圈

    H_out = (H + 2 * padding - F) // stride + 1
    W_out = (W + 2 * padding - F) // stride + 1
    output = torch.zeros(H_out, W_out)

    for i in range(H_out):
        for j in range(W_out):
            # 取出输入中对应位置的 patch
            patch = x[i*stride : i*stride+F,
                      j*stride : j*stride+F]   # (F, F)
            output[i, j] = (patch * kernel).sum()  # 逐元素乘后求和

    return output
```

**记忆要点：**
- patch 的起始位置是 `[i*stride, j*stride]`，大小是 `F×F`
- `(patch * kernel).sum()` 就是点积（Frobenius inner product）

---

### C2 — GCN 前向传播

```python
def gcn_forward(A, H, W):
    N = A.shape[0]

    # Step 1: 加自环
    A_hat = A + torch.eye(N)                               # Â = A + I

    # Step 2: 度矩阵（每行求和）
    deg = A_hat.sum(dim=1)                                 # (N,)
    D_hat = torch.diag(deg)                                # (N, N)

    # Step 3: 对称归一化 D^{-1/2} Â D^{-1/2}
    D_inv_sqrt = torch.diag(1.0 / deg.sqrt())              # (N, N)
    A_norm = D_inv_sqrt @ A_hat @ D_inv_sqrt               # (N, N)

    # Step 4: 传播 + 线性变换 + 激活
    return torch.relu(A_norm @ H @ W)                     # (N, D_out)
```

---

### C3 — Max Pooling

```python
def max_pool2d(x, pool_size=2, stride=2):
    H, W = x.shape
    H_out = (H - pool_size) // stride + 1
    W_out = (W - pool_size) // stride + 1
    output = torch.zeros(H_out, W_out)

    for i in range(H_out):
        for j in range(W_out):
            patch = x[i*stride : i*stride+pool_size,
                      j*stride : j*stride+pool_size]
            output[i, j] = patch.max()

    return output
```

---

## Part D 参考答案

### D1 — MLP vs CNN on Images

**三维对比：**

| 维度 | MLP | CNN |
|------|-----|-----|
| 参数量 | $O(H \cdot W \cdot C \cdot n_\text{out})$，极大 | $O(F^2 \cdot C_\text{in} \cdot C_\text{out})$，极小 |
| 空间关系 | 像素被展平为 1D 向量，相邻性完全丢失 | 局部连接保留了像素的空间相对位置 |
| 平移不变性 | 无：猫在左上 vs 右下是完全不同的输入 | 有（近似）：同一 filter 响应所有位置的相同模式 |

**Inductive bias 的定义：**  
Inductive bias 是模型在未见数据上泛化时所依赖的先验假设，这些假设被编码进了模型结构本身（不需要从数据中学习）。

**CNN 的 inductive bias：**
1. 局部性（locality）：相邻像素比远处像素更相关
2. 平移等变性（translation equivariance）：同一模式出现在不同位置应有相同响应

**什么时候 inductive bias 是限制：**
- 当任务需要**全局依赖**时：CNN 的感受野是逐层局部扩大的，要捕捉全局关系（如图像两端的物体之间的关系）需要非常深的网络，且信息传递路径很长。Vision Transformer 直接用 self-attention 让任意两个 patch 直接交互，不受局部性限制。
- 当数据**不满足平移不变性**时：例如医学影像中病灶的位置本身就是诊断信息，平移等变性反而丢弃了有用的位置信息。

---

### D2 — CNN 不能处理图数据 / GCN 如何解决

**(i) CNN 的隐含假设在图上失效：**

CNN 假设：
- 输入是**规则网格**：像素按二维规则排列，每个像素有固定数量的相邻像素（上下左右斜角，最多 8 个）
- 存在**空间顺序**：像素有上下左右的方向性，"左边的像素"有明确含义

图数据违反了这两点：
- 每个节点的邻居数量**不固定**（度数各异）
- 节点之间**没有空间顺序**（图是置换不变的，重新编号节点不改变图的结构）

因此 CNN 的 filter 无法在图上"滑动"——没有固定的邻域形状可以用来定义 filter。

**(ii) GCN 聚合 vs CNN 滑动 filter 的相似性：**

| | CNN | GCN |
|---|---|---|
| 操作 | Filter 在固定邻域内做加权求和 | 对变长邻居集合做加权聚合（求和/平均）|
| 权重共享 | 同一 filter 用于所有位置 | 同一 $W^l$ 用于所有节点 |
| 非线性 | ReLU 等激活函数 | 同样使用非线性激活 |
| 层次结构 | 多层叠加扩大感受野 | 多层叠加传播更远距离邻居的信息（2-hop, 3-hop...）|

本质上，GCN 是 CNN 的"去结构化"版本——将固定邻域推广为任意拓扑邻域。

**(iii) 置换不变性：**

GCN 是置换不变的——将图的节点重新编号（即置换节点顺序），节点特征矩阵 $H$ 的行被重排，邻接矩阵 $A$ 的行列同时被重排，最终输出的节点特征集合不变（只是顺序变了）。

**对图学习任务的意义：**
- **好事**：图没有自然的节点编号，同一个图的不同编号方案应该给出相同的结果（比如分子图，原子标号不同但结构相同的分子应有相同预测）。置换不变性保证了这一点。
- **潜在问题**：在某些任务中节点的"角色"（如某节点是否是中心节点）很重要，纯粹的置换不变聚合可能无法区分结构相似但语义不同的节点。解决方案是加入位置编码或使用更强的聚合函数。

---

### D3 — Group Conv & Depthwise Separable Conv

**(i) Group Convolution：**

将 $C_\text{in}$ 个输入通道分成 $G$ 组，每组有 $C_\text{in}/G$ 个输入通道和 $C_\text{out}/G$ 个输出通道，每组独立做卷积，最后拼接。

参数量变化：  
标准卷积：$F^2 \cdot C_\text{in} \cdot C_\text{out}$  
Group Conv：$F^2 \cdot (C_\text{in}/G) \cdot (C_\text{out}/G) \cdot G = F^2 \cdot C_\text{in} \cdot C_\text{out} / G$  
参数量变为原来的 $1/G$。

**(ii) $G = C$ 时退化为 Depthwise Convolution：**

每个通道用一个独立的 $F \times F$ filter，通道之间完全不交叉。参数量降至 $F^2 \cdot C_\text{in}$，但通道间没有任何信息混合。

**(iii) Depthwise Separable Conv 与标准卷积的对比：**

标准卷积（$C_\text{in}$ → $C_\text{out}$，filter $F\times F$）：
- 参数：$F^2 \cdot C_\text{in} \cdot C_\text{out}$
- 计算量：$F^2 \cdot C_\text{in} \cdot C_\text{out} \cdot H \cdot W$

Depthwise Separable = Depthwise Conv（$C_\text{in}$ → $C_\text{in}$）+ Pointwise Conv（$1\times1$，$C_\text{in}$ → $C_\text{out}$）：
- 参数：$F^2 \cdot C_\text{in} + 1^2 \cdot C_\text{in} \cdot C_\text{out} = C_\text{in}(F^2 + C_\text{out})$
- 计算量：$F^2 \cdot C_\text{in} \cdot H \cdot W + C_\text{in} \cdot C_\text{out} \cdot H \cdot W$

相对于标准卷积的比率：$\approx \frac{1}{C_\text{out}} + \frac{1}{F^2}$

以 $F=3, C_\text{out}=256$ 为例，参数量约为标准卷积的 $1/8 \sim 1/9$。

**(iv) 应用场景：**

Depthwise Separable Conv 是 **MobileNet** 系列的核心操作，广泛用于**移动端和嵌入式设备**的部署。在参数量和计算量大幅减少（8-9 倍）的情况下，精度损失相对有限，非常适合算力受限的场景。EfficientNet 也在此基础上进行了进一步优化。
