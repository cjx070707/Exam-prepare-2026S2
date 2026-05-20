# Group 1 Test — Foundations of Deep Learning
**Week 2: Neural Networks + Week 3: Regularization**

---

## Section A — Multiple Choice (10 pts, 2 pts each)

---

**A1.** A neural network with two linear layers and no activation function between them is equivalent to:

- (a) A network with one linear layer
- (b) A network with doubled capacity
- (c) A network with ReLU activation
- (d) A support vector machine

> [!success]- Answer
> 
> **(a)**
> 
> $W_2(W_1 x + b_1) + b_2 = (W_2W_1)x + \text{const}$，两个线性变换的复合仍然是线性的。不管叠多少个线性层，网络都等价于一个 affine map。必须引入 non-linear activation function 才能打破这个限制。

---

**A2.** Which activation function suffers from both gradient vanishing AND non-zero-centred output?

- (a) Tanh
- (b) ReLU
- (c) Sigmoid
- (d) Leaky ReLU

> [!success]- Answer
> 
> **(c) Sigmoid**
> 
> Sigmoid 输出范围 $(0,1)$，始终为正，因此不是 zero-centred。在饱和区（$|x| \gg 0$）时，$f'(x) \approx 0$，造成严重的 gradient vanishing。Tanh 是 zero-centred 但同样会饱和。ReLU 和 Leaky ReLU 在正区不会饱和。

---

**A3.** In backpropagation for a 3-layer network with MSE loss $J = \frac{1}{2}\|t - z\|^2$, the output layer error signal $\delta_k$ is:

- (a) $f'(\text{net}_k) \cdot \sum_j w_{kj} \delta_j$
- (b) $(t_k - z_k) \cdot f'(\text{net}_k)$
- (c) $(z_k - t_k) \cdot f(\text{net}_k)$
- (d) $\eta \cdot (t_k - z_k) \cdot y_j$

> [!success]- Answer
> 
> **(b)**
> 
> 由 chain rule 推导：$\delta_k = \frac{\partial J}{\partial \text{net}_k} = \frac{\partial J}{\partial z_k} \cdot f'(\text{net}_k) = (t_k - z_k) \cdot f'(\text{net}_k)$。
> 
> 选项 (a) 是 hidden layer 的公式，不是 output layer。

---

**A4.** Adam uses a second moment estimate $v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$. Dividing the update by $\sqrt{\hat{v}_t} + \varepsilon$ serves to:

- (a) Implement momentum by accumulating past gradients
- (b) Adaptively scale the learning rate — parameters with large historical gradients take smaller steps
- (c) Correct the bias introduced by zero-initialising $m_0$
- (d) Prevent the learning rate from increasing over time

> [!success]- Answer
> 
> **(b)**
> 
> $\hat{v}_t$ 估计了每个参数历史梯度平方的典型幅度。对历史梯度大的参数，$\hat{v}_t$ 大，$\eta/\sqrt{\hat{v}_t}$ 小（步长保守）；梯度小或稀疏的参数则获得相对更大的有效 learning rate，实现 per-parameter adaptive scaling。
> 
> 选项 (c) 描述的是 bias correction（$1-\beta^t$ 那一项），不是 $\sqrt{\hat{v}_t}$ 的作用。

---

**A5.** L1 regularisation tends to produce sparse weights while L2 does not. The best geometric explanation is:

- (a) The L1 ball is a hypersphere; its corners lie on the coordinate axes
- (b) The L1 ball is a diamond; its corners on the coordinate axes make axis-aligned solutions — where some weights are exactly zero — more likely when the loss contours intersect the constraint region
- (c) L1 penalises large weights more aggressively than L2
- (d) L1 corresponds to a Laplace prior which forces weights to zero

> [!success]- Answer
> 
> **(b)**
> 
> 在二维空间，L1 ball $\|\theta\|_1 \leq r$ 是菱形，角点在坐标轴上（$(\pm r, 0)$ 和 $(0, \pm r)$）。loss function 的等高线在向最优点收缩时，几何上更容易先碰到这些角点——而角点恰好在坐标轴上，即某个权重精确为零。L2 ball 是光滑球形，没有角点，交点处两个权重通常都非零。

---

## Section B — Short Answer (30 pts)

---

**B1. (6 pts)** Explain the Dead ReLU problem: (i) how does a neuron die? (ii) what is the effect on training? (iii) how does Leaky ReLU fix it?

> [!success]- Answer
> 
> **(i) 神经元如何死亡：**
> ReLU 在 pre-activation $z \leq 0$ 时输出为 0 且梯度为零。如果一次大的梯度更新把某个神经元的 bias 推得非常负，导致对所有训练样本都有 $z < 0$，则该神经元的梯度永远为零，权重不再更新。
> 
> **(ii) 对训练的影响：**
> Dead neuron 在 forward pass 中贡献为零，backward pass 也收不到梯度，相当于从网络中消失。严重时大批神经元同时 die，训练完全停滞。
> 
> **(iii) Leaky ReLU 的修复：**
> $$f(x) = \begin{cases} x & x > 0 \\ \alpha x & x \leq 0 \end{cases}, \quad \alpha \approx 0.01$$
> 在负区保留斜率 $\alpha$，保证梯度 $= \alpha \neq 0$，即使神经元处于 "off" 状态也能持续收到梯度信号，随时可以恢复。

---

**B2. (8 pts)** Write the complete Adam update steps from gradient $g_t$ to $\theta_{t+1}$, and answer: (i) why is bias correction needed? (ii) at $t=1$ with $\beta_1 = 0.9$, what is $\hat{m}_1 / m_1$?

> [!success]- Answer
> 
> **完整步骤：**
> $$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$$
> $$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$
> $$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t}$$
> $$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t}+\varepsilon}\,\hat{m}_t$$
> 
> **(i) 为什么需要 bias correction：**
> $m_0 = 0$，所以第 1 步 $m_1 = (1-0.9)g_1 = 0.1\,g_1$，只有真实梯度的 10%。moving average 因没有历史 "热身" 数据而被初始化过低。Bias correction 通过除以 $(1-\beta_1^t)$ 来恢复正确的估计值。
> 
> **(ii) 数值例子：**
> $\hat{m}_1 = m_1 / (1 - 0.9^1) = 0.1\,g_1 / 0.1 = g_1$，因此 $\hat{m}_1/m_1 = 10$。不做 correction 的话，第一步的梯度估计小了 10 倍。

---

**B3. (8 pts)** Explain how Batch Normalisation works: (i) write the BN forward equations, (ii) why can't BN use batch statistics at test time, (iii) what is the role of $\gamma$ and $\beta$?

> [!success]- Answer
> 
> **(i) BN forward pass：**
> $$\mu_B = \frac{1}{N}\sum_i x_i, \quad \sigma_B^2 = \frac{1}{N}\sum_i(x_i-\mu_B)^2$$
> $$\hat{x} = \frac{x - \mu_B}{\sqrt{\sigma_B^2+\varepsilon}}, \quad y = \gamma\hat{x} + \beta$$
> 
> **(ii) 测试时为何不能用 batch statistics：**
> 测试时可能只有一个样本，batch statistics 没有意义。BN 在训练过程中维护 exponential moving averages $\mu_\text{run}$、$\sigma^2_\text{run}$，测试时用这些固定值替代。
> 
> **(iii) $\gamma$ 和 $\beta$ 的作用：**
> Normalization 强制每层输出均值为 0、方差为 1，可能损害表达能力（例如 sigmoid 会被迫工作在近线性区）。$\gamma$（scale）和 $\beta$（shift）是可学习参数，让网络在需要时撤销 normalization。没有它们，每层的 representational capacity 将被永久限制。

---

**B4. (8 pts)** Consider the Bayesian interpretation of L2 regularisation: (i) what prior does it correspond to? (ii) write the regularised loss and weight update rule. (iii) explain the hard vs soft constraint equivalence.

> [!success]- Answer
> 
> **(i) Prior：**
> L2 regularization 对应各向同性的 **Gaussian prior** $p(\theta) = \mathcal{N}(0,\frac{1}{2\lambda}I)$——在该 prior 下做 MAP estimation 等价于最小化 L2 正则化的 loss。
> 
> **(ii) Loss 和 update：**
> $$\tilde{J}(\theta) = J(\theta) + \lambda\|\theta\|_2^2$$
> $$\theta \leftarrow (1-2\eta\lambda)\theta - \eta\nabla_\theta J$$
> 系数 $(1-2\eta\lambda)<1$ 在每步将权重向零衰减，因此称为 "weight decay"。
> 
> **(iii) Hard vs soft 等价：**
> Hard：$\min J(\theta)$ s.t. $\|\theta\|^2 \leq r$
> Soft：$\min J(\theta) + \lambda\|\theta\|^2$
> 
> 通过 Lagrangian $\mathcal{L} = J(\theta) + \lambda(\|\theta\|^2 - r)$，KKT 条件表明对每个 $r$ 存在唯一的 $\lambda \geq 0$ 使两者解重合。两种形式参数化了同一族解。

---

## Section C — Coding (25 pts)

---

**C1. (10 pts)** Implement a `LinearLayer` class with forward and backward passes (He init, support `relu` and `sigmoid`):

```python
class LinearLayer:
    def __init__(self, n_in, n_out, activation='relu'):
        pass
    def forward(self, x):   # x: (B, n_in) → (B, n_out)
        pass
    def backward(self, grad):  # grad: (B, n_out) → dx, dW, db
        pass
```

> [!success]- Answer
> 
> ```python
> import torch, math
> 
> class LinearLayer:
>     def __init__(self, n_in, n_out, activation='relu'):
>         self.activation = activation
>         self.W = torch.randn(n_in, n_out) * math.sqrt(2.0 / n_in)  # He init
>         self.b = torch.zeros(1, n_out)
>         self._x = None
>         self._z = None
> 
>     def _act(self, z):
>         if self.activation == 'relu':
>             return z.clamp(min=0)
>         elif self.activation == 'sigmoid':
>             return 1.0 / (1.0 + torch.exp(-z))
> 
>     def _act_grad(self, z):
>         if self.activation == 'relu':
>             return (z > 0).float()
>         elif self.activation == 'sigmoid':
>             s = 1.0 / (1.0 + torch.exp(-z))
>             return s * (1.0 - s)
> 
>     def forward(self, x):
>         self._x = x
>         self._z = x @ self.W + self.b
>         return self._act(self._z)
> 
>     def backward(self, grad):
>         dz = grad * self._act_grad(self._z)   # (B, n_out)
>         dW = self._x.T @ dz                   # (n_in, n_out)
>         db = dz.sum(dim=0, keepdim=True)       # (1, n_out)
>         dx = dz @ self.W.T                     # (B, n_in)
>         return dx, dW, db
> ```
> 
> **要点：** He init 用 `sqrt(2/n_in)`。必须同时缓存 `x`（用于 `dW = x.T @ dz`）和 `z`（用于计算 activation gradient）。`dW` 的 shape 必须和 `W` 一致。

---

**C2. (8 pts)** Implement Adam as a stateful class:

```python
class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        pass
    def step(self, param, grad):
        pass
```

> [!success]- Answer
> 
> ```python
> class Adam:
>     def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
>         self.lr, self.b1, self.b2, self.eps = lr, beta1, beta2, eps
>         self.t = 0
>         self._m = None
>         self._v = None
> 
>     def step(self, param, grad):
>         self.t += 1
>         if self._m is None:
>             self._m = torch.zeros_like(param)
>             self._v = torch.zeros_like(param)
> 
>         self._m = self.b1 * self._m + (1 - self.b1) * grad
>         self._v = self.b2 * self._v + (1 - self.b2) * grad ** 2
> 
>         m_hat = self._m / (1 - self.b1 ** self.t)
>         v_hat = self._v / (1 - self.b2 ** self.t)
> 
>         param -= self.lr * m_hat / (torch.sqrt(v_hat) + self.eps)
>         return param
> ```
> 
> **要点：** 先递增 `t` 再做 bias correction。Second moment 用 `grad**2`。懒初始化避免了在构造时就需要知道参数 shape。

---

**C3. (7 pts)** Implement Batch Normalisation forward pass:

```python
def batchnorm_forward(x, gamma, beta, eps=1e-5):
    # x: (N,C,H,W)  gamma,beta: (1,C,1,1)
    # normalise over (N,H,W) per channel
    pass
```

> [!success]- Answer
> 
> ```python
> def batchnorm_forward(x, gamma, beta, eps=1e-5):
>     mu  = x.mean(dim=(0, 2, 3), keepdim=True)
>     var = x.var(dim=(0, 2, 3), keepdim=True)
>     x_hat = (x - mu) / torch.sqrt(var + eps)
>     return gamma * x_hat + beta
> ```
> 
> **要点：** `dim=(0,2,3)` 在 batch + spatial 维度上求均值，保留 channel 维度。`keepdim=True` 保持 shape 以便 broadcasting。`+eps` 防止除以零。

---

## Section D — Essay (35 pts)

---

**D1. (12 pts)** Compare SGD, SGD + Momentum, and Adam: write each update equation, what problem each solves, and when you would prefer SGD + Momentum over Adam.

> [!success]- Answer
> 
> **更新公式：**
> 
> SGD：$\theta \leftarrow \theta - \eta\nabla J(\theta)$
> 
> SGD + Momentum：$v_t = \gamma v_{t-1} + \eta\nabla J(\theta)$，$\theta \leftarrow \theta - v_t$
> 
> Adam：见 B2。
> 
> **各自解决的问题：**
> - SGD：基准方法，无额外机制。在 ill-conditioned 的 loss surface 上震荡，收敛慢。
> - SGD + Momentum：在一致的梯度方向上累积 velocity（加速），在震荡方向上相互抵消（阻尼）。在 valley-shaped loss surface 上通常有约 10× 的加速。
> - Adam：通过 second moment 实现 per-parameter adaptive learning rate，加上 momentum。几乎不需要调参；对 sparse gradient 和非平稳 loss surface 效果好。
> 
> **何时选 SGD + Momentum：**
> 1. **最终 test accuracy**：在图像分类（CIFAR、ImageNet）上，搭配 cosine annealing 的 SGD + Momentum 通常比 Adam 达到更低的 test error。Adam 的 adaptive scaling 可能轻微损害 generalization。
> 2. **有调参余量时**：Adam 是捷径；如果能做充分的 learning rate sweep，SGD + Momentum 往往是长期更好的选择。
> 3. **内存受限场景**：Adam 需要为每个参数存储两个 moment 向量，SGD + Momentum 只需一个 velocity 向量。

---

**D2. (10 pts)** Explain why overfitting occurs, and analyse how Dropout prevents it from: (i) the ensemble learning perspective, and (ii) the co-adaptation perspective.

> [!success]- Answer
> 
> **为什么会 overfitting：**
> 当模型 capacity 相对于训练集过大时，模型会记住训练数据中特有的噪声，而不是学习底层分布。Training loss 低，generalization 差。
> 
> **(i) Ensemble learning 视角：**
> 每次训练步，Dropout 通过以概率 $p$ 随机将神经元置零来采样不同的 sub-network。训练过程中相当于同时训练 $2^n$ 个不同的 sub-network（每种 binary mask 对应一个）。测试时所有神经元都开启（scaled by $1-p$），近似所有 sub-network 预测的几何均值。Ensemble 之所以 generalize 更好，是因为各 sub-network 的错误部分不相关，会相互抵消。
> 
> **(ii) Co-adaptation 视角：**
> 不加 Dropout 时，神经元之间可能形成紧密协作的组——神经元 A 只在神经元 B 永远存在时才能正常工作。这种 co-adaptation 产生对训练数据有效、但对新数据脆弱的表示。
> 
> Dropout 随机去除神经元，迫使每个神经元独立学习有用特征，产生更冗余、更鲁棒的表示，从而更好地 generalize。

---

**D3. (13 pts)** The Universal Approximation Theorem states that an MLP can approximate any continuous function. Analyse three limitations: (i) what does the theorem not guarantee? (ii) specific problems with high-dimensional image inputs. (iii) how these motivate CNNs via inductive bias.

> [!success]- Answer
> 
> **(i) 定理没有保证什么：**
> 定理保证了存在一个足够宽的 single-hidden-layer 网络可以逼近 compact domain 上的任意连续函数，但不保证：
> - 如何找到这个网络（gradient descent 不一定收敛到它）
> - 网络必须有多宽（可能需要指数级宽度）
> - Sample efficiency（可能需要海量训练数据）
> - Generalization（拟合训练点 ≠ 在新输入上正确）
> 
> **(ii) 高维图像输入的问题：**
> 一张 $256\times256\times3$ 的图像有 196,608 个特征。第一层 MLP 有 1000 个神经元就需要约 2 亿个参数，远超典型数据集规模，导致灾难性 overfitting。更根本的是，MLP 将图像展平为一维向量，丢弃了所有空间结构。位置 $(i,j)$ 的猫和位置 $(i',j')$ 的猫被视为完全不同的输入，MLP 必须对每个可能位置分别学习猫的检测器。
> 
> **(iii) CNN 通过 inductive bias 的动机：**
> Inductive bias 是内嵌在模型架构中的先验假设，无需从数据中学习即可约束假设空间。
> 
> CNN 为自然图像编码了两个正确的先验：
> 1. **Locality**：相邻像素比远处像素更具信息量 → local receptive fields
> 2. **Translation equivariance**：同一 pattern 出现在任何位置都应给出相同响应 → weight sharing
> 
> 这使第一层参数从约 2 亿减少到约 7000，而这对自然图像几乎总是正确的。结果：模型从小数据集也能良好 generalize，因为假设空间已被约束在合理解的附近。MLP 没有 inductive bias，必须从头发现这些规律，需要数量级更多的数据。
