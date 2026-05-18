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
> $W_2(W_1 x + b_1) + b_2 = (W_2W_1)x + \text{const}$ — the composition of two linear transformations is still linear. No matter how many linear layers you stack, the network collapses to a single affine map. Non-linear activation functions are required to break this.

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
> Sigmoid outputs values in $(0,1)$ — always positive, so not zero-centred. In saturated regions ($|x| \gg 0$), $f'(x) \approx 0$, causing severe gradient vanishing. Tanh is zero-centred but still saturates. ReLU and Leaky ReLU do not saturate in the positive region.

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
> By chain rule: $\delta_k = \frac{\partial J}{\partial \text{net}_k} = \frac{\partial J}{\partial z_k} \cdot f'(\text{net}_k) = (t_k - z_k) \cdot f'(\text{net}_k)$.
> 
> Option (a) is the hidden-layer formula, not the output-layer formula.

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
> $\hat{v}_t$ estimates the typical squared magnitude of the gradient for each parameter. A parameter with consistently large gradients has large $\hat{v}_t$, so $\eta/\sqrt{\hat{v}_t}$ is small (conservative step). Sparse or small-gradient parameters get a relatively larger effective learning rate.
> 
> Option (c) describes bias correction (the $1-\beta^t$ division), not the $\sqrt{\hat{v}_t}$ term.

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
> In 2D, the L1 ball $\|\theta\|_1 \leq r$ is a diamond with corners at $(\pm r, 0)$ and $(0, \pm r)$. As the loss function's contour lines shrink toward the optimum, they geometrically tend to first touch the diamond at one of its corners — which sit exactly on a coordinate axis, meaning one weight is zero. The L2 ball is a smooth sphere with no corners, so the intersection is generic and weights are typically both nonzero.

---

## Section B — Short Answer (30 pts)

---

**B1. (6 pts)** Explain the Dead ReLU problem: (i) how does a neuron die? (ii) what is the effect on training? (iii) how does Leaky ReLU fix it?

> [!success]- Answer
> 
> **(i) How a neuron dies:**
> ReLU outputs 0 and has zero gradient whenever pre-activation $z \leq 0$. If a large gradient update pushes a neuron's bias very negative so that $z < 0$ for every training sample, the gradient through that neuron is permanently zero — weights never update again.
> 
> **(ii) Effect on training:**
> A dead neuron contributes nothing to the forward pass and receives no gradient in the backward pass. It effectively disappears from the network. In severe cases, large fractions of neurons die simultaneously and training stalls entirely.
> 
> **(iii) Leaky ReLU fix:**
> $$f(x) = \begin{cases} x & x > 0 \\ \alpha x & x \leq 0 \end{cases}, \quad \alpha \approx 0.01$$
> The small slope $\alpha$ in the negative region ensures gradient $= \alpha \neq 0$ even when the neuron is "off". The neuron can always receive a gradient signal and recover.

---

**B2. (8 pts)** Write the complete Adam update steps from gradient $g_t$ to $\theta_{t+1}$, and answer: (i) why is bias correction needed? (ii) at $t=1$ with $\beta_1 = 0.9$, what is $\hat{m}_1 / m_1$?

> [!success]- Answer
> 
> **Complete steps:**
> $$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$$
> $$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$
> $$\hat{m}_t = \frac{m_t}{1-\beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1-\beta_2^t}$$
> $$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t}+\varepsilon}\,\hat{m}_t$$
> 
> **(i) Why bias correction:**
> $m_0 = 0$, so at $t=1$: $m_1 = (1-0.9)g_1 = 0.1\,g_1$ — only 10% of the actual gradient. The moving average is initialised too low because there is no "warm-up" history. Bias correction rescales by $1/(1-\beta_1^t)$ to recover the correct estimate.
> 
> **(ii) Numerical example:**
> $\hat{m}_1 = m_1 / (1 - 0.9^1) = 0.1\,g_1 / 0.1 = g_1$, so $\hat{m}_1/m_1 = 10$.
> Without correction the first update uses a gradient estimate 10× too small.

---

**B3. (8 pts)** Explain how Batch Normalisation works: (i) write the BN forward equations, (ii) why can't BN use batch statistics at test time, (iii) what is the role of $\gamma$ and $\beta$?

> [!success]- Answer
> 
> **(i) BN forward pass:**
> $$\mu_B = \frac{1}{N}\sum_i x_i, \quad \sigma_B^2 = \frac{1}{N}\sum_i(x_i-\mu_B)^2$$
> $$\hat{x} = \frac{x - \mu_B}{\sqrt{\sigma_B^2+\varepsilon}}, \quad y = \gamma\hat{x} + \beta$$
> 
> **(ii) Test time:**
> At test time the batch may contain only one sample, making batch statistics meaningless. BN maintains exponential moving averages $\mu_\text{run}$, $\sigma^2_\text{run}$ during training and uses them as fixed values at test time.
> 
> **(iii) Role of $\gamma$ and $\beta$:**
> Normalisation forces every layer's output to zero mean and unit variance, potentially harming expressiveness (e.g. sigmoid would always operate in its near-linear region). $\gamma$ (scale) and $\beta$ (shift) are learnable parameters that let the network undo the normalisation if needed. Without them the representational capacity of each layer is permanently constrained.

---

**B4. (8 pts)** Consider the Bayesian interpretation of L2 regularisation: (i) what prior does it correspond to? (ii) write the regularised loss and weight update rule. (iii) explain the hard vs soft constraint equivalence.

> [!success]- Answer
> 
> **(i) Prior:**
> L2 regularisation corresponds to an isotropic **Gaussian prior** $p(\theta) = \mathcal{N}(0,\frac{1}{2\lambda}I)$ — MAP estimation under this prior is equivalent to minimising the L2-regularised loss.
> 
> **(ii) Loss and update:**
> $$\tilde{J}(\theta) = J(\theta) + \lambda\|\theta\|_2^2$$
> $$\theta \leftarrow (1-2\eta\lambda)\theta - \eta\nabla_\theta J$$
> The factor $(1-2\eta\lambda)<1$ decays weights toward zero at each step — hence "weight decay".
> 
> **(iii) Hard vs soft equivalence:**
> Hard: $\min J(\theta)$ s.t. $\|\theta\|^2 \leq r$
> Soft: $\min J(\theta) + \lambda\|\theta\|^2$
> 
> Via the Lagrangian $\mathcal{L} = J(\theta) + \lambda(\|\theta\|^2 - r)$, KKT conditions show that for every $r$ there exists a unique $\lambda \geq 0$ such that the solutions coincide. The two formulations parameterise the same family of solutions.

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
> **Key points:** He init uses `sqrt(2/n_in)`. Must cache both `x` (for `dW = x.T @ dz`) and `z` (for activation gradient). `dW` shape must match `W`.

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
> **Key points:** increment `t` before bias correction. Second moment uses `grad**2`. Lazy init avoids needing param shape at construction.

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
> **Key points:** `dim=(0,2,3)` averages over batch + spatial, leaving channel. `keepdim=True` preserves shape for broadcasting. `+eps` prevents divide-by-zero.

---

## Section D — Essay (35 pts)

---

**D1. (12 pts)** Compare SGD, SGD + Momentum, and Adam: write each update equation, what problem each solves, and when you would prefer SGD + Momentum over Adam.

> [!success]- Answer
> 
> **Update equations:**
> 
> SGD: $\theta \leftarrow \theta - \eta\nabla J(\theta)$
> 
> SGD + Momentum: $v_t = \gamma v_{t-1} + \eta\nabla J(\theta)$, $\theta \leftarrow \theta - v_t$
> 
> Adam: see B2 above.
> 
> **Problems solved:**
> - SGD: baseline, no extra mechanism. Oscillates on ill-conditioned surfaces, converges slowly.
> - SGD + Momentum: accumulates velocity in consistent gradient directions (accelerates), cancels in oscillating directions (damps). Typical 10× speedup on valley-shaped loss surfaces.
> - Adam: per-parameter adaptive learning rates via second moment + momentum. Near-zero tuning required; well-suited to sparse gradients and non-stationary loss surfaces.
> 
> **When to prefer SGD + Momentum:**
> 1. **Final test accuracy**: on image classification (CIFAR, ImageNet), SGD + Momentum with cosine annealing often achieves lower final test error than Adam. Adam's adaptive scaling can slightly hurt generalisation.
> 2. **When tuning budget exists**: Adam is a shortcut; given proper learning-rate sweeps, SGD + Momentum is often the better long-run choice.
> 3. **Memory-constrained settings**: Adam requires storing two moment vectors per parameter. SGD + Momentum stores only one velocity vector.

---

**D2. (10 pts)** Explain why overfitting occurs, and analyse how Dropout prevents it from: (i) the ensemble learning perspective, and (ii) the co-adaptation perspective.

> [!success]- Answer
> 
> **Why overfitting occurs:**
> When model capacity is large relative to the training set, the model memorises idiosyncratic noise in the training data rather than the underlying distribution. Training loss is low; generalisation is poor.
> 
> **(i) Ensemble learning perspective:**
> Each training step, Dropout samples a different sub-network by randomly zeroing neurons with probability $p$. Over all steps, the network is effectively training $2^n$ different sub-networks (one per binary mask). At test time, all neurons are on (scaled by $1-p$) — this approximates the geometric mean of all sub-network predictions. Ensembles generalise better than single models because their errors are partly uncorrelated and cancel.
> 
> **(ii) Co-adaptation perspective:**
> Without Dropout, neurons can learn to work in tightly coordinated groups — neuron A only functions correctly because neuron B is always present to compensate. This co-adaptation produces brittle representations that work on training data but fail on unseen data.
> 
> Dropout randomly removes neurons during training, so each neuron cannot rely on any specific other neuron being present. Each neuron is forced to learn independently useful features — producing a more redundant, robust representation that generalises better.

---

**D3. (13 pts)** The Universal Approximation Theorem states that an MLP can approximate any continuous function. Analyse three limitations: (i) what does the theorem not guarantee? (ii) specific problems with high-dimensional image inputs. (iii) how these motivate CNNs via inductive bias.

> [!success]- Answer
> 
> **(i) What the theorem does NOT guarantee:**
> The theorem guarantees the *existence* of a sufficiently wide single-hidden-layer network that approximates any continuous function on a compact domain. It does not guarantee:
> - How to find that network (gradient descent may not converge to it)
> - How wide the network must be (may require exponential width)
> - Sample efficiency (the required training data may be enormous)
> - Generalisation (fitting training points ≠ correct behaviour on unseen inputs)
> 
> **(ii) Problems with high-dimensional image inputs:**
> A $256\times256\times3$ image has 196,608 features. A first MLP layer with 1,000 neurons needs ~200M parameters — far exceeding typical dataset sizes, causing catastrophic overfitting. More fundamentally, the MLP flattens the image into a 1D vector, discarding all spatial structure. Adjacent pixels have no special relationship to distant ones. A cat at position $(i,j)$ and at $(i',j')$ are treated as entirely different inputs; the MLP must learn the cat detector separately for every possible position.
> 
> **(iii) How these motivate CNNs via inductive bias:**
> An *inductive bias* is a prior assumption built into the model architecture that constrains the hypothesis space without requiring data to learn it.
> 
> CNNs encode two correct priors for natural images:
> 1. **Locality**: nearby pixels are more informative than distant ones → local receptive fields
> 2. **Translation equivariance**: the same pattern anywhere should give the same response → weight sharing
> 
> These reduce first-layer parameters from ~200M to ~7,000, and are almost always correct for natural images. The result: the model generalises well from small datasets because the hypothesis space is already constrained to plausible solutions. The MLP, with no inductive bias, must discover these regularities from scratch — requiring orders of magnitude more data.
