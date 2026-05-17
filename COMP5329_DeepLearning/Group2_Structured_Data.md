# Group 2 — Structured Data
**Week 4: Convolutional Neural Networks + Week 5: Graph Neural Networks**

---

## 这一组在讲什么

Group 1 解决了"让机器学习"的基本问题，但 MLP 有一个根本性的局限——它完全不理解数据的结构。

这一组的叙事线：

> **MLP 忽略图像的空间结构** → CNN 利用局部性和平移不变性 → 但 CNN 只能处理规则的网格数据 → **GNN 把卷积的思想推广到任意图结构**

---

## Part 1 — MLP 在图像上的问题

一张 256×256 的 RGB 图片有 $256 \times 256 \times 3 = 196,608$ 个像素。如果第一层有 1000 个神经元，光第一层就需要将近 **2 亿个参数**。

更严重的问题是：MLP 把每个像素当成独立的特征，完全没有用到像素之间的空间关系。一只猫出现在图片左上角还是右下角，MLP 会当成完全不同的输入来处理——这显然是错的。

**MLP 缺少两个对图像很重要的直觉**：
1. **局部性**：相邻的像素比远处的像素更相关
2. **平移不变性**：一只猫不管在哪个位置都应该被识别为猫

CNN 把这两个直觉直接编进了网络结构。

---

## Part 2 — CNN：把直觉编进结构

### 核心思想：局部连接 + 权重共享

**局部连接**：每个神经元只看输入的一小块区域（比如 3×3 的 patch），而不是整张图片。

**权重共享**：同一个 filter（卷积核）在整张图片上滑动，所有位置用同一组权重。这意味着网络在每个位置都用同样的"眼睛"去看，无论猫在哪里，都用同一个"猫探测器"。

这两个设计让 CNN 的参数量从数亿降到数千。

### 卷积操作

Filter 在输入上滑动，每个位置做矩阵点积然后求和，生成一个 feature map：

$$\text{output}[i,j] = \sum_{m}\sum_{n} \text{input}[i \cdot S + m,\ j \cdot S + n] \cdot \text{filter}[m, n]$$

其中 $S$ 是 stride（步长）。

**输出尺寸公式**（必须记住）：

$$\text{output size} = \frac{W - F + 2P}{S} + 1$$

| 符号 | 含义 |
|------|------|
| $W$ | 输入宽度 |
| $F$ | filter 大小 |
| $P$ | padding（补零的圈数）|
| $S$ | stride（滑动步长）|

**例子**：输入 $32 \times 32$，filter $3 \times 3$，padding $= 1$，stride $= 1$：

$$\frac{32 - 3 + 2 \times 1}{1} + 1 = 32 \quad \text{（same padding，尺寸不变）}$$

### Padding 的两种选择

- **Same padding**（补零）：输出和输入尺寸相同，保留边缘信息
- **Valid padding**（不补零）：输出比输入小，边缘被丢弃

### Stride 和 Dilated Convolution

**Stride > 1**：filter 每次跳过多个像素，输出尺寸缩小，起到下采样的作用。

**Dilated Convolution（空洞卷积）**：在 filter 的元素之间插入"洞"，扩大感受野但不增加参数。膨胀率 $r=2$ 时，$3\times3$ 的 filter 实际覆盖 $5\times5$ 的区域。

$$\text{dilated receptive field} = F + (F-1)(r-1)$$

**好处**：参数量不变，但感受野指数级增长。

---

## Part 3 — CNN 的关键组件

### Pooling（池化）

卷积层之后通常接一个 Pooling 层，作用是：
1. 降低特征图的空间维度（减少计算量）
2. 提供一定程度的平移不变性

**Max Pooling**：取区域内的最大值，保留最强的激活  
**Average Pooling**：取区域内的平均值，更平滑

### 1×1 Convolution

Filter 大小为 $1\times1$，只在 channel 维度做线性组合。用途：
- **降维**：把 192 个 channel 压缩成 64 个，减少后续计算量（ResNet、Inception 都用这个技巧）
- **增加非线性**：加一个 ReLU 就多一层非线性变换
- **Bottleneck 结构**：先用 $1\times1$ 降维，做 $3\times3$ 卷积，再用 $1\times1$ 升维

### Receptive Field（感受野）

一个神经元能"看到"的输入区域大小。越深的层感受野越大，能捕捉越全局的信息。

增大感受野的方法：
- 堆叠更多卷积层
- 使用 Pooling 或大 stride
- 使用 Dilated Convolution

> **考试提示**：感受野是 CNN 设计的核心概念，常考"为什么要设计这么深的网络"——因为要让最终的特征能看到足够大的输入区域。

### Group Convolution

把 input channels 分成 $G$ 组，每组独立卷积。参数量变为原来的 $\frac{1}{G}$。

当 $G = C$（组数等于 channel 数）时，退化为 **Depthwise Convolution**——每个 channel 用一个独立的 filter，MobileNet 的核心操作。

---

## Part 4 — CNN vs MLP：Inductive Bias

| | MLP | CNN |
|---|---|---|
| 连接方式 | 全连接 | 局部连接 |
| 权重 | 每个连接独立 | 空间位置共享 |
| 平移不变性 | ✗ | ✓（近似）|
| 参数量 | 极大 | 很小 |
| 内置假设（inductive bias）| 无 | 局部性 + 平移不变性 |

**Inductive bias 的双刃剑**：CNN 的假设在自然图像上几乎总是成立，所以小数据集上表现很好；但这些假设也限制了 CNN，比如它不擅长捕捉全局依赖（这是 ViT 的优势，Group 3 会讲）。

> **考试高频论述题**："CNN 和 MLP 的 inductive bias 有什么区别？各自适合什么场景？"

---

## Part 5 — 从 CNN 到 GNN：当数据不是网格

CNN 很强，但它有一个隐含的前提：**输入是规则的网格结构**（像素的二维阵列）。

现实中很多重要的数据不是网格：
- **社交网络**：节点是用户，边是关注关系
- **分子结构**：节点是原子，边是化学键
- **引用网络**：节点是论文，边是引用关系
- **知识图谱**：节点是实体，边是关系

这些数据上，CNN 的"局部连接 + 权重共享"不能直接用，因为：
1. 每个节点的邻居数量不固定（图片每个像素的邻居数固定是 8）
2. 节点之间没有空间顺序（图片有上下左右的概念）

**GNN 的核心问题**：如何在任意图结构上做"类卷积"的聚合？

---

## Part 6 — GCN：图卷积网络

### 图的表示

一个图 $G = (V, E)$：
- $V$：节点集合，$N$ 个节点
- $E$：边集合
- $X \in \mathbb{R}^{N \times D}$：节点特征矩阵（每个节点有 $D$ 维特征）
- $A \in \mathbb{R}^{N \times N}$：邻接矩阵，$A_{ij} = 1$ 表示节点 $i$ 和 $j$ 相连

### Spatial GCN（空间域）

最直觉的想法：每个节点的新特征 = 聚合自己邻居的特征。

**最简单的传播规则**：

$$H^{l+1} = \sigma(A H^l W^l)$$

其中 $H^l$ 是第 $l$ 层的节点特征矩阵，$W^l$ 是可学习的权重矩阵。

**问题一**：乘以 $A$ 只聚合了邻居，没有包含节点自身。

**修复**：加上自环，$\hat{A} = A + I$（$I$ 是单位矩阵）

**问题二**：$A$ 没有归一化，邻居多的节点（度大的节点）聚合后特征值会很大，破坏量纲。

**修复**：对称归一化，$\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2}$，其中 $\hat{D}$ 是 $\hat{A}$ 的度矩阵。

**最终传播规则（Kipf & Welling, 2016）**：

$$\boxed{H^{l+1} = \sigma\!\left(\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2} H^l W^l\right)}$$

**直觉**：每个节点的新特征 = 对自己和邻居的特征做归一化加权平均，然后线性变换 + 激活。

### Spectral GCN（谱域）

从信号处理的角度来看图卷积。

**图拉普拉斯矩阵**：

$$\Delta = I - D^{-1/2}AD^{-1/2}$$

衡量每个节点的特征值和其邻居平均值之间的差——图上的"平滑度"。

**图上的 Fourier 变换**：将拉普拉斯矩阵做特征分解：

$$\Delta = \Phi \Lambda \Phi^\top$$

其中 $\Phi$ 的列是特征向量（图的"频率基"），$\Lambda$ 是特征值（频率）。

图上的卷积 = 频域的点乘：

$$h^{l+1} = \sigma\!\left(\Phi \hat{w}^l(\Lambda) \Phi^\top h^l\right)$$

**谱域 vs 空间域**：
- 谱域：数学严谨，但需要计算特征分解（$O(N^3)$，节点多时很慢）
- 空间域：直接聚合邻居，计算高效，更实用

> **考试提示**：谱域方法一般考"定义和理解"，空间域方法（Kipf 的传播公式）更可能考手写代码。

---

## Part 7 — CNN vs GNN：本质的联系

两者其实是同一个思想的不同形态：

| | CNN | GNN |
|---|---|---|
| 数据结构 | 规则网格（图片）| 任意图 |
| 聚合方式 | 固定 $F \times F$ 邻域 | 可变的邻居集合 |
| 权重共享 | 同一 filter 在所有位置共享 | 同一 $W^l$ 对所有节点共享 |
| 顺序依赖 | 有（上下左右）| 无（图是置换不变的）|
| Inductive bias | 局部性 + 平移不变性 | 图结构上的局部性 |

**GNN 的核心 inductive bias**：相邻节点的特征应该相似（homophily 假设）。这在社交网络（物以类聚）和分子（相邻原子性质相关）上成立，但不总是成立。

---

## 能力检查清单

**概念理解（短答 / 选择）**
- [ ] 给出输入尺寸、filter 大小、padding、stride，计算输出尺寸
- [ ] 解释 weight sharing 为什么能大幅减少参数量
- [ ] 解释 1×1 convolution 的作用（降维 + 非线性）
- [ ] 解释 dilated convolution 如何在不增加参数的情况下扩大感受野
- [ ] 解释为什么 CNN 不能直接用在图数据上
- [ ] 写出 GCN 的传播公式，解释 $\hat{A} = A + I$ 和归一化各自解决什么问题
- [ ] 说出图拉普拉斯矩阵的定义和含义

**手写代码（手写代码题）**
- [ ] 手写 2D 卷积的前向计算（双重循环版本）
- [ ] 手写 Max Pooling 的前向计算
- [ ] 手写 GCN 一层的前向传播（给定 $\hat{A}$、$H$、$W$）

**分析比较（论述题）**
- [ ] 比较 MLP 和 CNN 在图像任务上的 inductive bias 差异
- [ ] 比较 CNN 和 GNN 的相似性和区别
- [ ] 分析 Spectral GCN 和 Spatial GCN 各自的优缺点

---

## 代码对应数学

### 算法一：2D 卷积前向计算

**数学**：output$[i,j] = \sum_m \sum_n \text{input}[i \cdot S + m,\ j \cdot S + n] \cdot \text{filter}[m, n]$

```python
def conv2d_forward(input, filter, stride=1, padding=0):
    # input:  (H_in, W_in)
    # filter: (F, F)
    H, W = input.shape
    F = filter.shape[0]

    # 补零
    if padding > 0:
        input = torch.nn.functional.pad(input, [padding]*4)

    H_out = (H + 2*padding - F) // stride + 1  # 输出尺寸公式
    W_out = (W + 2*padding - F) // stride + 1
    output = torch.zeros(H_out, W_out)

    for i in range(H_out):
        for j in range(W_out):
            # 取出对应的 patch，做点积
            patch = input[i*stride : i*stride+F,
                          j*stride : j*stride+F]   # (F, F)
            output[i, j] = (patch * filter).sum()   # 点积求和

    return output
```

**记忆要点**：输出位置 `[i, j]` 对应输入的起始位置是 `[i*stride, j*stride]`，终止位置是 `[i*stride+F, j*stride+F]`。

---

### 算法二：Max Pooling

**数学**：output$[i,j] = \max_{m,n}$ input$[i \cdot S + m,\ j \cdot S + n]$

```python
def max_pool2d(input, pool_size=2, stride=2):
    H, W = input.shape
    H_out = (H - pool_size) // stride + 1
    W_out = (W - pool_size) // stride + 1
    output = torch.zeros(H_out, W_out)

    for i in range(H_out):
        for j in range(W_out):
            patch = input[i*stride : i*stride+pool_size,
                          j*stride : j*stride+pool_size]
            output[i, j] = patch.max()   # 取最大值
    return output
```

---

### 算法三：GCN 一层前向传播

**数学**：$H^{l+1} = \sigma\!\left(\hat{D}^{-1/2}\hat{A}\hat{D}^{-1/2} H^l W^l\right)$

```python
def gcn_layer_forward(A, H, W):
    # A: (N, N) 邻接矩阵
    # H: (N, D_in) 节点特征
    # W: (D_in, D_out) 可学习权重

    # 第一步：加自环 A_hat = A + I
    N = A.shape[0]
    A_hat = A + torch.eye(N)                         # Â = A + I

    # 第二步：计算度矩阵 D_hat
    D_hat = torch.diag(A_hat.sum(dim=1))             # 每行求和得到度

    # 第三步：对称归一化
    D_inv_sqrt = torch.diag(1.0 / D_hat.diag().sqrt())
    A_norm = D_inv_sqrt @ A_hat @ D_inv_sqrt          # D^{-1/2} Â D^{-1/2}

    # 第四步：传播 + 线性变换 + 激活
    out = torch.relu(A_norm @ H @ W)                  # σ(A_norm H W)
    return out
```

**记忆要点**：
- `A + I`：加自环，让节点聚合自己的特征
- 归一化：防止度大的节点特征值爆炸
- 矩阵乘法顺序：先聚合邻居 (`A_norm @ H`)，再线性变换 (`@ W`)

---

### 默写练习（合上文档再做）

1. 给定输入 $7\times7$，filter $3\times3$，padding $= 0$，stride $= 2$，手算输出尺寸
2. 从空白写出 2D 卷积的双重循环实现（关键是 patch 的索引）
3. 从空白写出 GCN 一层的前向传播，解释每一步的目的
4. 用一句话解释为什么 GCN 需要对 $A$ 加自环并做归一化

---

## 下一组预告

CNN 和 GNN 都处理的是**静态数据**——一张图片、一个图。但还有一类数据天生是**有顺序的**：文字、语音、时间序列。

"今天天气很好"和"好很天气今天"意思完全不同——顺序是信息的一部分。MLP 和 CNN 都无法捕捉这种时序依赖，因为它们的输入长度是固定的，而且不区分前后。

→ **Group 3：序列数据（RNN → Transformer → SSM）**
