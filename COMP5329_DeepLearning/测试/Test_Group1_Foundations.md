# Group 1 专项测试 — Foundations of Deep Learning
**Week 2: Neural Networks + Week 3: Regularization**

> 先做题，再看答案。目标：每题都能不看笔记作答。

---

## Part A — 单选题（10 分，每题 2 分）

**A1.** A neural network with two linear layers and no activation function between them is equivalent to:

- (a) A network with one linear layer
- (b) A network with doubled capacity
- (c) A network with ReLU activation
- (d) A support vector machine

---

**A2.** Which activation function suffers from both gradient vanishing AND non-zero-centred output?

- (a) Tanh
- (b) ReLU
- (c) Sigmoid
- (d) Leaky ReLU

---

**A3.** In backpropagation for a 3-layer network with MSE loss $J = \frac{1}{2}\|t - z\|^2$, the output layer error signal $\delta_k$ is:

- (a) $f'(\text{net}_k) \cdot \sum_j w_{kj} \delta_j$
- (b) $(t_k - z_k) \cdot f'(\text{net}_k)$
- (c) $(z_k - t_k) \cdot f(\text{net}_k)$
- (d) $\eta \cdot (t_k - z_k) \cdot y_j$

---

**A4.** Adam uses a second moment estimate $v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$. The purpose of dividing the update by $\sqrt{\hat{v}_t} + \varepsilon$ is:

- (a) To implement momentum by accumulating past gradients
- (b) To adaptively scale the learning rate — parameters with large historical gradients take smaller steps
- (c) To correct the bias introduced by zero-initialising $m_0$
- (d) To prevent the learning rate from decreasing to zero

---

**A5.** L1 regularisation tends to produce sparse weights while L2 does not. The geometric reason is:

- (a) The L1 penalty ball is a hypersphere; its corners lie on the coordinate axes
- (b) The L1 penalty ball is a diamond shape; its corners on the axes make weight solutions where many weights are exactly zero more likely
- (c) L1 penalises large weights more aggressively than L2
- (d) L1 corresponds to a Laplace prior which has heavier tails than Gaussian

---

## Part B — 简答题（30 分）

**B1. (6 分)** 解释 Dead ReLU 问题：

(i) Dead ReLU 是怎么发生的？（什么情况下一个神经元会"死掉"？）  
(ii) 它对训练的影响是什么？  
(iii) Leaky ReLU 是如何解决这个问题的？

---

**B2. (8 分)** 写出 Adam 优化器的完整更新步骤（从梯度 $g_t$ 到参数更新 $\theta_{t+1}$），并回答：

(i) 为什么需要 bias correction？（从 $m_0 = v_0 = 0$ 出发解释）  
(ii) 在训练初期（$t=1$），如果没有 bias correction，$\hat{m}_1$ 和 $m_1$ 有什么关系？以 $\beta_1 = 0.9$ 为例计算。

---

**B3. (8 分)** 解释 Batch Normalisation 的工作原理，并回答：

(i) 写出 BN 的前向计算公式（均值、方差、归一化、缩放平移）  
(ii) 为什么 BN 在测试时不能用 batch 统计量？它用什么替代？  
(iii) $\gamma$ 和 $\beta$ 参数的作用是什么？如果没有它们会有什么问题？

---

**B4. (8 分)** 考虑 L2 正则化的贝叶斯解释：

(i) L2 正则化等价于对权重施加什么先验分布？  
(ii) 写出带 L2 正则化的损失函数，以及对应的梯度更新规则（即 weight decay 形式）  
(iii) 解释"硬约束"和"软约束"的等价性（需要提到拉格朗日乘数）

---

## Part C — 手写代码（25 分）

**C1. (10 分)** 从空白实现一个完整的 `Linear + Activation` 层，包含 forward 和 backward：

```python
class LinearLayer:
    def __init__(self, n_in, n_out, activation='relu'):
        # 用 He 初始化 W，零初始化 b
        # He init: W ~ N(0, sqrt(2/n_in))
        pass

    def forward(self, x):
        # x: (B, n_in)
        # 返回激活后的输出 (B, n_out)
        # 必须缓存中间值供 backward 使用
        pass

    def backward(self, grad):
        # grad: dL/d(output), 形状 (B, n_out)
        # 返回 dx, dW, db
        pass
```

要求：
- `__init__` 实现 He 初始化
- `forward` 支持 `relu` 和 `sigmoid` 两种激活
- `backward` 返回正确的 `dx`、`dW`、`db`

---

**C2. (8 分)** 从空白实现 Adam 的一次更新步骤：

```python
class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        pass

    def step(self, param, grad):
        # param: 要更新的参数张量（原地修改）
        # grad:  对应梯度
        # 返回更新后的 param
        pass
```

---

**C3. (7 分)** 实现 Batch Normalisation 的前向计算（不用 `nn.BatchNorm`）：

```python
def batchnorm_forward(x, gamma, beta, eps=1e-5):
    # x:     (N, C, H, W)
    # gamma: (1, C, 1, 1)
    # beta:  (1, C, 1, 1)
    # 沿 (N, H, W) 维度归一化，每个 channel 独立
    # 返回归一化后的输出，形状与 x 相同
    pass
```

---

## Part D — 论述题（35 分）

**D1. (12 分)** 对比 SGD、SGD + Momentum 和 Adam 三种优化器：

- 各自的更新公式是什么？
- 它们分别解决了什么问题？
- 在什么情况下你会选择 SGD + Momentum 而不是 Adam？

---

**D2. (10 分)** 解释为什么过拟合会发生，以及 Dropout 如何从以下两个角度理解它的防过拟合效果：

(i) **集成学习的角度**：Dropout 训练过程相当于在训练什么？  
(ii) **特征依赖的角度**：Dropout 迫使网络学到什么样的表示？

---

**D3. (13 分)** Universal Approximation Theorem（通用近似定理）说明 MLP 可以逼近任意连续函数。但这并不意味着"用 MLP 就够了"。从以下三个角度分析它的局限：

(i) 定理保证了"存在"一个网络，但没有保证什么？  
(ii) 当输入是高维图像（如 256×256×3）时，MLP 面临什么具体问题？  
(iii) 这些局限如何催生了 CNN 的设计？（用 inductive bias 的概念回答）

---

---

# 参考答案

---

## Part A

| 题号 | 答案 | 关键理由 |
|------|------|---------|
| A1 | **(a)** | $W_2(W_1 x + b_1) + b_2 = (W_2W_1)x + \text{const}$，仍是线性变换 |
| A2 | **(c)** | Sigmoid 输出 $(0,1)$，非零中心；饱和区梯度趋零，梯度消失严重 |
| A3 | **(b)** | $\delta_k = \frac{\partial J}{\partial \text{net}_k} = (t_k - z_k) \cdot f'(\text{net}_k)$，链式法则直接推导 |
| A4 | **(b)** | $\hat{v}_t$ 是梯度平方的指数加权平均，大梯度参数得到更小步长 |
| A5 | **(b)** | L1 球是多面体，顶角在坐标轴上；损失函数等高线与顶角相切时，解恰好落在轴上（某些权重 = 0） |

---

## Part B 参考答案

### B1 — Dead ReLU

**(i) 发生原因：**  
ReLU 在输入 $z \leq 0$ 时输出恒为 0，梯度也恒为 0。如果某个神经元在某次更新后，它对**所有训练样本**的输入都变成负数（比如偏置或权重初始化过大导致 pre-activation 总为负），那么该神经元的梯度永久为 0，权重再也不会被更新。

**(ii) 对训练的影响：**  
死亡神经元对任何输入都不响应，相当于从网络中消失。网络的有效容量下降，在严重情况下大量神经元同时死亡，训练完全停滞。

**(iii) Leaky ReLU 的解决方案：**  
$$f(x) = \begin{cases} x & x > 0 \\ \alpha x & x \leq 0 \end{cases}, \quad \alpha \approx 0.01$$
在负数区间保留一个小斜率 $\alpha$，梯度在负半轴变为 $\alpha \neq 0$，神经元始终能收到梯度信号，不会死亡。

---

### B2 — Adam 完整步骤

完整步骤：

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$
$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \varepsilon} \hat{m}_t$$

**(i) 为什么需要 bias correction：**  
$m_0 = v_0 = 0$（零初始化）。在 $t=1$ 时：
$$m_1 = \beta_1 \cdot 0 + (1-\beta_1) g_1 = (1-\beta_1) g_1$$
如果 $\beta_1 = 0.9$，则 $m_1 = 0.1 g_1$，严重低估了梯度的真实均值。Bias correction 将其放大：$\hat{m}_1 = m_1 / (1 - 0.9^1) = m_1 / 0.1 = g_1$，还原正确估计。

**(ii) 数值示例（$\beta_1 = 0.9, t=1$）：**
$$m_1 = 0.1 g_1, \quad \hat{m}_1 = \frac{0.1 g_1}{1 - 0.9} = g_1$$
没有 correction 时 $m_1 = 0.1 g_1$，仅为真实梯度的 10%，导致前几步更新过小。

---

### B3 — Batch Normalisation

**(i) 前向公式：**
$$\mu = \frac{1}{N} \sum_i x_i, \quad \sigma^2 = \frac{1}{N} \sum_i (x_i - \mu)^2$$
$$\hat{x} = \frac{x - \mu}{\sqrt{\sigma^2 + \varepsilon}}, \quad y = \gamma \hat{x} + \beta$$

**(ii) 测试时为何不能用 batch 统计：**  
测试时可能只有单个样本（batch size = 1），此时 batch 统计量毫无意义。BN 在训练时维护 $\mu$ 和 $\sigma^2$ 的指数移动平均（running statistics），测试时用这些固定值代替实时计算。

**(iii) $\gamma$ 和 $\beta$ 的作用：**  
归一化后所有激活都被强制拉到均值 0、方差 1 附近，这可能损害网络的表达能力（比如 Sigmoid 的非线性区域需要非零均值激活）。$\gamma$ 和 $\beta$ 是可学习参数，让网络可以选择"撤销"归一化，恢复到任意均值和方差。极端情况下，网络可以学到 $\gamma = \sigma$, $\beta = \mu$，完全还原归一化前的分布。

---

### B4 — L2 正则化的贝叶斯解释

**(i) 先验分布：**  
L2 正则化等价于对权重施加均值为 0、方差为 $\frac{1}{2\lambda}$ 的**高斯先验** $p(\theta) = \mathcal{N}(0, \frac{1}{2\lambda}I)$，对应 MAP（最大后验）估计。

**(ii) 损失函数与梯度更新：**
$$\tilde{J}(\theta) = J(\theta) + \lambda \|\theta\|_2^2$$
$$\nabla_\theta \tilde{J} = \nabla_\theta J + 2\lambda\theta$$
$$\theta \leftarrow \theta - \eta(\nabla_\theta J + 2\lambda\theta) = (1 - 2\eta\lambda)\theta - \eta\nabla_\theta J$$
每次更新时权重乘以 $(1-2\eta\lambda) < 1$，即 weight decay。

**(iii) 硬约束与软约束的等价性：**  
- 硬约束：$\min_\theta J(\theta)$ s.t. $\|\theta\|^2 \leq r$  
- 软约束：$\min_\theta J(\theta) + \lambda\|\theta\|^2$

两者通过**拉格朗日乘数法**等价：将约束 $\|\theta\|^2 \leq r$ 引入拉格朗日函数 $\mathcal{L} = J(\theta) + \lambda(\|\theta\|^2 - r)$，在 KKT 条件下，$\lambda$ 是拉格朗日乘数，每个 $\lambda$ 对应唯一的 $r$，反之亦然——因此两种形式描述的是同一族解。

---

## Part C 参考答案

### C1 — LinearLayer

```python
import torch
import math

class LinearLayer:
    def __init__(self, n_in, n_out, activation='relu'):
        self.activation = activation
        # He 初始化：适配 ReLU，std = sqrt(2/n_in)
        self.W = torch.randn(n_in, n_out) * math.sqrt(2.0 / n_in)
        self.b = torch.zeros(1, n_out)
        self._x = None
        self._z = None

    def _act(self, z):
        if self.activation == 'relu':
            return z.clamp(min=0)
        elif self.activation == 'sigmoid':
            return 1.0 / (1.0 + torch.exp(-z))

    def _act_grad(self, z):
        if self.activation == 'relu':
            return (z > 0).float()
        elif self.activation == 'sigmoid':
            s = 1.0 / (1.0 + torch.exp(-z))
            return s * (1 - s)

    def forward(self, x):
        self._x = x                     # cache for backward
        self._z = x @ self.W + self.b   # pre-activation
        return self._act(self._z)       # (B, n_out)

    def backward(self, grad):
        # grad: dL/d(output), (B, n_out)
        dz = grad * self._act_grad(self._z)         # dL/dz,  (B, n_out)
        dW = self._x.T @ dz                         # (n_in, n_out)
        db = dz.sum(dim=0, keepdim=True)            # (1, n_out)
        dx = dz @ self.W.T                          # (B, n_in)
        return dx, dW, db
```

---

### C2 — Adam

```python
class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr
        self.b1 = beta1
        self.b2 = beta2
        self.eps = eps
        self.t = 0
        self._m = None
        self._v = None

    def step(self, param, grad):
        self.t += 1
        if self._m is None:
            self._m = torch.zeros_like(param)
            self._v = torch.zeros_like(param)

        # 一阶矩（梯度的指数移动平均）
        self._m = self.b1 * self._m + (1 - self.b1) * grad
        # 二阶矩（梯度平方的指数移动平均）
        self._v = self.b2 * self._v + (1 - self.b2) * grad ** 2

        # Bias correction
        m_hat = self._m / (1 - self.b1 ** self.t)
        v_hat = self._v / (1 - self.b2 ** self.t)

        # 参数更新
        param -= self.lr * m_hat / (torch.sqrt(v_hat) + self.eps)
        return param
```

---

### C3 — Batch Normalisation

```python
def batchnorm_forward(x, gamma, beta, eps=1e-5):
    # x: (N, C, H, W)，沿 (N, H, W) 归一化，每个 channel 独立
    mu  = x.mean(dim=(0, 2, 3), keepdim=True)          # (1, C, 1, 1)
    var = x.var(dim=(0, 2, 3), keepdim=True)            # (1, C, 1, 1)
    x_hat = (x - mu) / torch.sqrt(var + eps)            # 归一化
    return gamma * x_hat + beta                         # 缩放 + 平移
```

---

## Part D 参考答案

### D1 — 三种优化器对比

**更新公式：**

*SGD:*
$$\theta \leftarrow \theta - \eta \nabla J(\theta)$$

*SGD + Momentum:*
$$v_t = \gamma v_{t-1} + \eta \nabla J(\theta), \quad \theta \leftarrow \theta - v_t$$

*Adam:* （见 B2）

**各自解决的问题：**

- **SGD**：基线方法，无任何改进。在平坦方向收敛慢，在峡谷型损失面上震荡。
- **Momentum**：累积过去梯度方向，在一致方向加速，在震荡方向相互抵消。解决 SGD 在峡谷型损失面的震荡问题，典型加速 10×。
- **Adam**：同时自适应学习率（二阶矩）和动量（一阶矩）。不同参数用不同有效学习率，对稀疏梯度特别有效。

**什么时候选 SGD + Momentum 而非 Adam：**

1. **最终精度要求高的图像分类任务**：有研究表明 SGD + Momentum 配合学习率调度（cosine annealing）往往能达到比 Adam 更低的最终测试误差（Adam 泛化略差的现象）。
2. **超参数调优充分时**：Adam 的自适应性在泛化上有时是双刃剑——它可能过度适应噪声梯度。SGD + Momentum 更"保守"，在有足够计算预算调 $\eta$ 和 $\gamma$ 时往往是更好的选择。
3. **凸优化或简单任务**：Adam 的复杂机制在简单问题上没有收益，还增加了内存和计算开销。

---

### D2 — Dropout 防过拟合的两个角度

**(i) 集成学习的角度：**

每次 forward pass，Dropout 随机关闭一部分神经元，相当于从 $2^n$（$n$ 是神经元数）种可能的子网络中采样一个子网络来训练。训练结束时，整个网络近似于所有这些子网络的**集成**（bagging），而集成模型的泛化能力通常强于单个模型——集成内各模型的错误不完全相关，可以相互抵消。

测试时所有神经元开启并乘以 $(1-p)$，相当于对所有子网络做了一次近似平均预测。

**(ii) 特征依赖的角度：**

在没有 Dropout 的情况下，网络可能学到"co-adaptation"——某几个神经元协同工作，互相依赖来完成某个特征检测。这种高度协同的表示对训练集非常有效，但泛化差（删掉一个神经元整个特征就崩了）。

Dropout 随机删除神经元，强迫每个神经元不能依赖其他特定神经元的存在。网络被迫学习**冗余的、更独立的特征表示**——每个神经元必须单独对结果有贡献，而不是依赖其他神经元"帮它说话"。这样的表示更鲁棒，泛化更好。

---

### D3 — Universal Approximation Theorem 的局限

**(i) 定理保证了"存在"，但没有保证：**

- **如何找到这个网络**：定理是存在性定理，不提供构造方法，也不保证梯度下降能收敛到那个解。
- **需要多少神经元**：定理允许隐藏层神经元数量无限大，实际中可能需要指数级宽度才能逼近复杂函数。
- **样本效率**：逼近任意函数需要足够的训练数据；数据不足时，理论上能逼近并不等于实际能泛化。

**(ii) 高维图像上的具体问题：**

一张 $256 \times 256 \times 3$ 的图片有 196,608 个输入特征。若第一层有 1000 个神经元，参数量接近 **2 亿**，远超典型训练集大小，极易过拟合。更根本的问题是 MLP 对每个像素独立处理——像素的空间关系（哪两个像素相邻）对 MLP 完全不可见，同一只猫出现在不同位置被视为完全不同的输入。

**(iii) CNN 的 inductive bias：**

CNN 将两个领域知识硬编码进了网络结构：

- **局部性**（local connectivity）：每个神经元只连接一小块区域，反映"相邻像素比远处像素更相关"的先验。
- **平移等变性**（translation equivariance）：同一卷积核在整张图上共享权重，反映"同一模式出现在任何位置都应该被同样检测"的先验。

这两个 inductive bias 极大地减少了参数量，并让网络在小数据集上也能泛化良好——因为这些假设对自然图像几乎总是成立。MLP 没有任何 inductive bias，必须从数据中从零学习这些规律，需要指数级更多的数据。
