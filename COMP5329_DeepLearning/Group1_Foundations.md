# Group 1 — Foundations of Deep Learning
**Week 2: Neural Networks + Week 3: Regularization**

---

## 这一组在讲什么

我们想让机器自动分类数据。最直觉的起点是一个线性分类器。但线性分类器有根本性的局限——它只能划一条直线，而很多真实问题根本不是线性可分的。

这一组的叙事线：

> **线性模型不够用** → 加隐藏层+非线性激活 → 用 Backprop 训练 → 用各种 Optimizer 加速 → 但模型开始记住训练数据 → 用 Regularization 限制它

---

## Part 1 — 为什么线性模型不够用

### Perceptron（感知机）

最早的分类器。给定输入 x，计算：

$$\hat{y} = \mathbf{w}^\top \mathbf{x} + b$$

用 sign 函数输出 +1 或 -1。学习规则：对分错的样本做梯度下降。

**致命缺陷**：只能学线性决策边界。XOR 问题就是最简单的反例——四个点，没有任何一条直线能正确分开它们。这一点在 1969 年被 Minsky 和 Papert 证明，直接导致了第一次 AI 寒冬。

### 解决方案：加隐藏层 + 非线性激活函数

$$\text{hidden: } y_j = f\!\left(\sum_i w_{ji} x_i + b_j\right)$$
$$\text{output: } z_k = f\!\left(\sum_j w_{kj} y_j + b_k\right)$$

**两个条件缺一不可**：隐藏层提供了中间表示的空间，但如果 $f$ 是线性函数，多层线性变换的复合仍然是线性变换，等价于单层——加多少层都没用。$f$ 必须是非线性激活函数（如 ReLU、Sigmoid），才能让网络表达非线性决策边界。

**为什么有用**：激活函数把输入映射到新的特征空间，在这个空间里原本线性不可分的数据可能变得线性可分。只要有足够多的隐藏单元，MLP 可以逼近任意连续函数——这叫**Universal Approximation Theorem**（通用近似定理）。

> **考试提示**：选择题常考"为什么 XOR 需要隐藏层"和"Universal Approximation Theorem 说了什么"。

---

## Part 2 — 激活函数：非线性从哪来

没有激活函数，再深的网络也等价于一个线性变换（因为线性的复合还是线性）。

### Sigmoid

$$f(x) = \frac{1}{1 + e^{-x}}, \quad \text{输出范围} (0, 1)$$

**问题**：
1. **梯度消失**：当 x 很大或很小时，f'(x) ≈ 0，梯度乘上去就消失了，深层网络训练不动
2. **输出不以 0 为中心**：导致梯度更新的方向总是同号（全正或全负），收敛慢

### Tanh

$$f(x) = \tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}, \quad \text{输出范围} (-1, 1)$$

**改进**：输出以 0 为中心，解决了 Sigmoid 的第二个问题。但**梯度消失依然存在**。

### ReLU（最常用）

$$f(x) = \max(0, x)$$

**优点**：
- 正区间梯度恒为 1，不消失
- 计算简单，没有 exp

**缺点**：**Dead ReLU 问题**——如果某个神经元的输入一直是负数，梯度永远是 0，这个神经元"死掉"了，再也不会更新。

### Leaky ReLU（修复 Dead ReLU）

$$f(x) = \begin{cases} x & x > 0 \\ \alpha x & x \leq 0 \end{cases}, \quad \alpha \approx 0.01$$

给负数区间一个小斜率，保证梯度不为零。

| 激活函数 | 输出范围 | 零中心 | 梯度消失 | Dead 神经元 |
|---------|---------|--------|---------|------------|
| Sigmoid | (0,1) | ✗ | 严重 | ✗ |
| Tanh | (-1,1) | ✓ | 有 | ✗ |
| ReLU | [0,∞) | ✗ | 无（正区间）| 有 |
| Leaky ReLU | (-∞,∞) | ✗ | 无 | ✗ |

> **考试提示**：常考"为什么用 ReLU 而不用 Sigmoid"，答：计算快 + 不饱和（正区间）+ 不消失。配合 He 初始化效果最好。

---

## Part 3 — Backpropagation：网络怎么学习

有了网络结构，问题变成：怎么知道每个权重应该往哪个方向更新？

### 核心思想

链式法则（chain rule）从输出层的误差，一层一层往回传播梯度。

### 具体推导（3 层网络）

**损失函数**：

$$J(\mathbf{w}) = \frac{1}{2}\|\mathbf{t} - \mathbf{z}\|^2$$

**输出层权重的梯度**（隐藏层到输出层，权重 $w_{kj}$）：

$$\delta_k = (t_k - z_k) \cdot f'(\text{net}_k) \quad \text{（输出层误差信号）}$$

$$\Delta w_{kj} = \eta \cdot \delta_k \cdot y_j$$

**隐藏层权重的梯度**（输入层到隐藏层，权重 $w_{ji}$）：

$$\delta_j = f'(\text{net}_j) \cdot \sum_k w_{kj} \delta_k \quad \text{（误差从输出层传回来）}$$

$$\Delta w_{ji} = \eta \cdot \delta_j \cdot x_i$$

**关键理解**：隐藏层的误差信号 $\delta_j$ 是输出层误差 $\delta_k$ 的加权和，权重就是连接权重 $w_{kj}$。这就是"反向传播"名字的来源。

> **手写代码考点**：能从空白写出 3 层网络的 forward + backward，包括激活函数的导数。重点是 $\delta_k$、$\delta_j$ 的公式，和参数更新的方向。

---

## Part 4 — Optimizer：怎么走得更快更稳

梯度下降告诉我们方向，但怎么走这条路是另一个问题。

### Vanilla SGD

$$\theta \leftarrow \theta - \eta \nabla J(\theta)$$

**问题**：在"峡谷型"损失面上（一个方向很陡，另一个很平坦），梯度方向主要指向陡的那侧，导致来回震荡，收敛慢。

### Momentum（动量）

$$v_t = \gamma v_{t-1} + \eta \nabla J(\theta)$$
$$\theta \leftarrow \theta - v_t$$

累积过去的梯度方向（$\gamma \approx 0.9$）。在一致的方向上加速，在震荡的方向上抵消。效果：快 10 倍以上。

### Adam（最常用）

同时解决两个问题：用过去梯度的**一阶矩**（方向），和**二阶矩**（幅度）来自适应调整每个参数的学习率。

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t \quad \text{（一阶矩，均值）}$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2 \quad \text{（二阶矩，方差）}$$

偏差修正（初始时 $m_0 = v_0 = 0$ 导致估计偏小）：

$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t}$$

更新：

$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \varepsilon} \hat{m}_t$$

**直觉**：梯度大且噪声大的参数 → $\hat{v}_t$ 大 → 步长小。梯度小且稳定的参数 → $\hat{v}_t$ 小 → 相对步长大。

默认参数：$\eta = 0.001$，$\beta_1 = 0.9$，$\beta_2 = 0.999$，$\varepsilon = 10^{-8}$。

| Optimizer | 核心改进 | 典型用途 |
|-----------|---------|---------|
| SGD | 基线 | 简单任务 |
| SGD + Momentum | 累积方向，减少震荡 | 图像分类 |
| Adam | 自适应学习率 + 动量 | 大多数深度学习任务 |

> **考试提示**：Adam 为什么需要 bias correction？因为 $m_0 = v_0 = 0$，初期估计偏低，不修正的话前几步学习率会偏大。

---

## Part 5 — Regularization：防止过拟合

现在网络能学了，但出现了新问题：**过拟合**（Overfitting）。

训练损失很低，但验证集损失很高——网络记住了训练数据，而不是学到了规律。

### 什么是 Regularization

任何能防止过拟合、提升泛化能力的方法。

### L2 正则化（Weight Decay）

在损失函数上加一个惩罚项：

$$\tilde{J}(\theta) = J(\theta) + \lambda \|\theta\|_2^2$$

梯度更新变成：

$$\theta \leftarrow (1 - \eta\lambda)\theta - \eta \nabla J(\theta)$$

效果：每次更新时权重都会缩小（decay），防止权重变得太大。

**贝叶斯解释**：L2 等价于对权重施加一个均值为 0 的高斯先验（MAP 估计）。$\lambda$ 越大，先验越强，模型越简单。

**硬约束 vs 软约束**（常考）：

- 硬约束：$\min J(\theta)$ s.t. $\|\theta\|^2 \leq r$
- 软约束（等价）：$\min J(\theta) + \lambda\|\theta\|^2$

两者在数学上通过拉格朗日乘数等价，$\lambda$ 和 $r$ 一一对应。

### L1 正则化

$$\tilde{J}(\theta) = J(\theta) + \lambda \|\theta\|_1$$

效果：倾向于产生**稀疏权重**（很多权重变成 0），相当于做了特征选择。

### Dropout

训练时，每个神经元以概率 $p$ 被随机置零。

**直觉**：强迫网络不能依赖任何单个神经元 → 学到更鲁棒的特征。  
**测试时**：所有神经元都开，但输出乘以 $(1-p)$（期望一致）。

### Normalization Methods（归一化）

过拟合的另一个来源是内部激活值变化太大（Internal Covariate Shift）。归一化在中间层稳定分布。

**Batch Normalization（BN）**：
沿 batch 维度 + 空间维度计算均值和方差，学习两个参数 $\gamma$（缩放）和 $\beta$（平移）：

$$\hat{x} = \frac{x - \mu_\text{batch}}{\sqrt{\sigma^2_\text{batch} + \varepsilon}}, \quad y = \gamma\hat{x} + \beta$$

- 优点：加速训练，允许更大学习率
- 缺点：**依赖 batch size**，batch 太小统计不稳定；测试时用移动平均

**Layer Normalization（LN）**：
沿 channel + 空间维度计算（单个样本内部），不依赖 batch。

- Transformer 默认用 LN（因为 NLP 任务 batch 通常很小）
- 测试时行为与训练完全一样

**Instance Normalization（IN）**：
每个样本、每个 channel 单独归一化（沿空间维度）。用于风格迁移。

**对比表**：

| 方法 | 归一化维度 | 依赖 batch？ | 常用场景 |
|------|----------|------------|---------|
| Batch Norm | N, H, W | ✓ | CNN 图像分类 |
| Layer Norm | C, H, W | ✗ | Transformer |
| Instance Norm | H, W | ✗ | 风格迁移 |
| Group Norm | 部分 C, H, W | ✗ | 小 batch CNN |

> **考试提示**：常考"为什么 Transformer 用 LN 而不用 BN"——因为 NLP 任务序列长度可变，batch size 小，BN 的统计不稳定；LN 不依赖 batch，且对序列天然适用。

---

## 能力检查清单

学完这一组，你应该能做到：

**概念理解（短答 / 选择）**
- [ ] 用一句话解释为什么 Perceptron 解决不了 XOR
- [ ] 解释 Universal Approximation Theorem 的含义和局限
- [ ] 说出 Sigmoid 的两个主要缺点（梯度消失 + 不以零为中心）
- [ ] 解释为什么深层网络首选 ReLU 而非 Sigmoid
- [ ] 解释 Adam 为什么需要 bias correction
- [ ] 说出 L2 正则化的贝叶斯解释
- [ ] 解释 BatchNorm 和 LayerNorm 的区别，以及各自适合什么场景

**手写代码（手写代码题）**
- [ ] 写出 3 层 MLP 的 forward pass（含激活函数）
- [ ] 写出 Backprop 的 $\delta_k$、$\delta_j$ 公式和权重更新规则
- [ ] 写出 Adam 的完整更新步骤（含 bias correction）
- [ ] 手写 BatchNorm 的前向计算

**分析比较（论述题）**
- [ ] 比较 SGD / Momentum / Adam 的优缺点，各自适合什么场景
- [ ] 解释 L1 vs L2 正则化的效果差异（L1 稀疏，L2 缩小）
- [ ] 分析 dropout 为什么能防止过拟合

---

## 下一组预告

Group 1 解决了"让机器学习"的基本问题，但 MLP 有一个严重的局限：

**它把图片的每个像素当成独立特征来处理。** 一张 256×256 的 RGB 图片有将近 20 万个像素，第一层就需要数千万个参数，而且完全不利用像素之间的空间关系。

一只猫不管出现在图片左上角还是右下角，应该被识别为同一只猫——MLP 对此完全无感，而 CNN 把这个直觉直接编进了网络结构里。

→ **Group 2：结构化数据（CNN + GNN）**

---

## 代码对应数学

> 使用方法：先读每段的公式，再看代码，确保你能解释每一行为什么这样写。
> 最终目标：合上文档，从空白默写。
> 练习题：完成后去 `Tutorial/Week3_Foundation.ipynb` Part C 做考试题。

---

### 算法一：激活函数 Forward + Backward

**数学**：
- Sigmoid: $f(z) = \frac{1}{1+e^{-z}}$，导数 $f'(z) = f(z)(1-f(z))$
- ReLU: $f(z) = \max(0, z)$，导数 $f'(z) = \mathbf{1}[z > 0]$

```python
class Activation:
    def __init__(self, name):
        self.name = name
        self._z = None          # 缓存 z，backward 时需要用

    def forward(self, z):
        self._z = z             # 必须缓存，backward 要用到
        if self.name == "sigmoid":
            return 1.0 / (1.0 + torch.exp(-z))
        elif self.name == "relu":
            return z.clamp(min=0)   # max(0, z) 的向量化写法

    def backward(self, grad):
        # grad 是上游传来的 dL/d(output)
        # 返回 dL/dz = grad * f'(z)
        z = self._z
        if self.name == "sigmoid":
            s = 1.0 / (1.0 + torch.exp(-z))
            return grad * s * (1.0 - s)    # f'(z) = f(z)(1-f(z))
        elif self.name == "relu":
            return grad * (z > 0).float()  # f'(z) = 1 if z>0 else 0
```

**记忆要点**：forward 必须缓存 z，因为 backward 计算 f'(z) 时需要用到原始的 z 值。

---

### 算法二：MLP Forward Pass

**数学**：每层计算 $\text{output} = f(XW + b)$

| 符号 | 形状 | 含义 |
|------|------|------|
| $X$ | $(B, n_\text{in})$ | 输入，B 是 batch size |
| $W$ | $(n_\text{in}, n_\text{out})$ | 权重矩阵 |
| $b$ | $(1, n_\text{out})$ | 偏置（自动广播到每个样本）|
| output | $(B, n_\text{out})$ | 激活后的输出 |

```python
def forward(self, x):
    self._x = x                    # 缓存输入，backward 时计算 dW 需要用
    z = x @ self.W + self.b        # (B, n_in) @ (n_in, n_out) = (B, n_out)
    return self.act.forward(z)     # 过激活函数
```

**记忆要点**：矩阵乘法的维度顺序是 $(B, n_\text{in}) \times (n_\text{in}, n_\text{out})$，内层维度 $n_\text{in}$ 消掉，结果是 $(B, n_\text{out})$。

---

### 算法三：Backpropagation

**数学**（单层的链式法则）：

$$\delta_z = f'(z) \odot \delta_\text{out} \quad \text{（过激活函数的梯度）}$$
$$\nabla_W = X^\top \delta_z \quad \text{（权重的梯度）}$$
$$\nabla_b = \sum_\text{batch} \delta_z \quad \text{（偏置的梯度）}$$
$$\delta_\text{in} = \delta_z W^\top \quad \text{（传给上一层的梯度）}$$

```python
def backward(self, grad):
    # grad = dL/d(output)，形状 (B, n_out)

    dz = self.act.backward(grad)        # dL/dz，形状 (B, n_out)
                                        # 对应公式：δ_z = f'(z) ⊙ grad

    dW = self._x.T @ dz                 # 形状 (n_in, B) @ (B, n_out) = (n_in, n_out)
                                        # 对应公式：∇W = X^T δ_z

    db = dz.sum(dim=0, keepdim=True)    # 形状 (1, n_out)
                                        # 对应公式：∇b = Σ_batch δ_z

    dx = dz @ self.W.T                  # 形状 (B, n_out) @ (n_out, n_in) = (B, n_in)
                                        # 对应公式：δ_in = δ_z W^T，传给上一层

    return dx, dW, db
```

**记忆要点**：
- `dW = x.T @ dz`：x 要转置，因为公式是 $X^\top \delta_z$
- `dx = dz @ W.T`：W 要转置，因为公式是 $\delta_z W^\top$
- 两者转置的位置不同，容易混，记住形状检查：dW 的形状必须和 W 一样

---

### 算法四：Adam Optimizer

**数学**：

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t \quad \text{（一阶矩）}$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2 \quad \text{（二阶矩）}$$
$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t} \quad \text{（bias correction）}$$
$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \varepsilon} \hat{m}_t$$

```python
def step(self, layers, grads):
    self.t += 1     # 时间步，bias correction 要用

    for layer, (dW, db) in zip(layers, grads):
        # ── 一阶矩（梯度的指数移动平均）──────────────────
        self._mW = self.b1 * self._mW + (1 - self.b1) * dW
        # ── 二阶矩（梯度平方的指数移动平均）──────────────
        self._vW = self.b2 * self._vW + (1 - self.b2) * dW ** 2

        # ── Bias correction（修正初期低估）───────────────
        mW_hat = self._mW / (1 - self.b1 ** self.t)
        vW_hat = self._vW / (1 - self.b2 ** self.t)

        # ── 参数更新 ──────────────────────────────────────
        layer.W -= self.lr * mW_hat / (torch.sqrt(vW_hat) + self.eps)
        #          ↑ 学习率   ↑ 方向    ↑ 自适应步长（梯度大的参数步长小）
```

**记忆要点**：
- 二阶矩用的是 `dW ** 2`（梯度的平方），不是 dW
- bias correction 分母是 `1 - beta^t`（t 是时间步），t 越大修正越小，最终趋近于 1
- 更新时除以 `sqrt(v_hat)` 的直觉：历史梯度大的参数 → 步长自动缩小

---

### 算法五：Batch Normalization Forward

**数学**：

$$\mu = \frac{1}{N}\sum_i x_i, \quad \sigma^2 = \frac{1}{N}\sum_i (x_i - \mu)^2$$
$$\hat{x} = \frac{x - \mu}{\sqrt{\sigma^2 + \varepsilon}}, \quad y = \gamma \hat{x} + \beta$$

```python
def batchnorm_forward(x, gamma, beta, eps=1e-5):
    # x 形状：(N, C, H, W)，沿 N, H, W 维度归一化

    mu    = x.mean(dim=(0, 2, 3), keepdim=True)   # 每个 channel 的均值
    var   = x.var(dim=(0, 2, 3), keepdim=True)    # 每个 channel 的方差
    x_hat = (x - mu) / torch.sqrt(var + eps)      # 归一化，+eps 防止除以零
    out   = gamma * x_hat + beta                  # 学习缩放和平移（恢复表达能力）
    return out
```

**记忆要点**：
- BN 沿 `(N, H, W)` 求统计量，每个 channel 独立归一化
- `+eps` 是为了数值稳定（方差可能为 0）
- `gamma` 和 `beta` 是可学习参数，让网络可以选择撤销归一化
- **LayerNorm 区别**：沿 `(C, H, W)` 求统计量，每个样本独立，不依赖 batch

---

### 默写练习（合上文档再做）

1. 从空白写出 `Activation` 类的 `forward` 和 `backward`（sigmoid + relu 两种）
2. 从空白写出单层的 `backward`，给出 `dW`、`db`、`dx` 三个公式
3. 从空白写出 Adam 的一次完整更新步骤（含 bias correction）
4. 用 5 行以内的代码写出 BatchNorm 的前向计算
