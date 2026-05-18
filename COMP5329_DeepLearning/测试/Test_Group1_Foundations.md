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

<details>
<summary>Answer</summary>

**(a)**

$W_2(W_1 x + b_1) + b_2 = (W_2 W_1)x + \text{const}$ — the composition of two linear transformations is still a linear transformation. No matter how many linear layers you stack, the entire network collapses to a single affine map. Non-linear activation functions are required to break this.

</details>

---

**A2.** Which activation function suffers from both gradient vanishing AND non-zero-centred output?

- (a) Tanh
- (b) ReLU
- (c) Sigmoid
- (d) Leaky ReLU

<details>
<summary>Answer</summary>

**(c) Sigmoid**

Sigmoid outputs values in $(0, 1)$ — always positive, so the output is not zero-centred. In saturated regions ($x \gg 0$ or $x \ll 0$), $f'(x) \approx 0$, causing severe gradient vanishing. Tanh is zero-centred but still saturates. ReLU and Leaky ReLU do not saturate in the positive region.

</details>

---

**A3.** In backpropagation for a 3-layer network with MSE loss $J = \frac{1}{2}\|t - z\|^2$, the output layer error signal $\delta_k$ is:

- (a) $f'(\text{net}_k) \cdot \sum_j w_{kj} \delta_j$
- (b) $(t_k - z_k) \cdot f'(\text{net}_k)$
- (c) $(z_k - t_k) \cdot f(\text{net}_k)$
- (d) $\eta \cdot (t_k - z_k) \cdot y_j$

<details>
<summary>Answer</summary>

**(b)**

By the chain rule: $\delta_k = \frac{\partial J}{\partial \text{net}_k} = \frac{\partial J}{\partial z_k} \cdot \frac{\partial z_k}{\partial \text{net}_k} = (t_k - z_k) \cdot f'(\text{net}_k)$.

Note the sign: with $J = \frac{1}{2}\|t-z\|^2$, $\frac{\partial J}{\partial z_k} = -(t_k - z_k)$, but the convention $\delta_k = (t_k - z_k) f'$ uses the "credit signal" where positive $\delta$ means the weight should increase. Option (a) is the hidden-layer formula, not the output-layer formula.

</details>

---

**A4.** Adam uses a second moment estimate $v_t = \beta_2 v_{t-1} + (1-\beta_2)g_t^2$. Dividing the update by $\sqrt{\hat{v}_t} + \varepsilon$ serves to:

- (a) Implement momentum by accumulating past gradients
- (b) Adaptively scale the learning rate — parameters with large historical gradients take smaller steps
- (c) Correct the bias introduced by zero-initialising $m_0$
- (d) Prevent the learning rate from increasing over time

<details>
<summary>Answer</summary>

**(b)**

$\hat{v}_t$ is an exponentially weighted average of $g_t^2$ — it estimates the typical magnitude of the gradient for each parameter. A parameter with consistently large gradients will have large $\hat{v}_t$, so $\eta / \sqrt{\hat{v}_t}$ will be small (conservative step). A parameter with small, stable gradients gets a relatively larger effective learning rate. This is the adaptive per-parameter learning rate mechanism.

Option (c) describes bias correction, which is the division by $(1-\beta^t)$, not the $\sqrt{\hat{v}_t}$ term.

</details>

---

**A5.** L1 regularisation tends to produce sparse weights while L2 does not. The best geometric explanation is:

- (a) The L1 penalty ball is a hypersphere; its corners lie on the coordinate axes
- (b) The L1 penalty ball is a diamond (cross-polytope); its corners lie on the axes, making axis-aligned solutions — where some weights are exactly zero — more likely when the loss contours intersect the constraint region
- (c) L1 penalises large weights more aggressively than L2
- (d) L1 corresponds to a Laplace prior which forces weights to zero

<details>
<summary>Answer</summary>

**(b)**

The L1 ball $\|\theta\|_1 \leq r$ in 2D is a diamond with corners at $(\pm r, 0)$ and $(0, \pm r)$. When the loss function's contour lines (typically elliptical) shrink toward the optimum, they are geometrically more likely to first touch the L1 ball at one of its corners — and those corners sit exactly on a coordinate axis, meaning one weight is zero. The L2 ball is smooth (a sphere) with no corners, so the intersection point is generic and both weights are typically nonzero.

</details>

---

## Section B — Short Answer (30 pts)

---

**B1. (6 pts)** Explain the Dead ReLU problem:

(i) How does a neuron "die"?
(ii) What is the effect on training?
(iii) How does Leaky ReLU fix it?

<details>
<summary>Answer</summary>

**(i) How a neuron dies:**
ReLU outputs 0 and has zero gradient whenever its pre-activation input $z \leq 0$. If a neuron's weights and bias are such that its pre-activation is negative for *every* training sample — which can happen after a large gradient update pushes the bias very negative — the gradient through that neuron is permanently zero. The weights will never be updated again.

**(ii) Effect on training:**
A dead neuron contributes nothing to the forward pass and receives no gradient in the backward pass. It effectively disappears from the network, reducing effective capacity. In severe cases, a large fraction of neurons die simultaneously, and training stalls entirely.

**(iii) Leaky ReLU fix:**
$$f(x) = \begin{cases} x & x > 0 \\ \alpha x & x \leq 0 \end{cases}, \quad \alpha \approx 0.01$$
The small slope $\alpha$ in the negative region ensures the gradient is $\alpha \neq 0$ even when the neuron is "off". The neuron always receives some gradient signal and can recover from negative pre-activations.

</details>

---

**B2. (8 pts)** Write out the complete Adam update steps (from gradient $g_t$ to updated parameter $\theta_{t+1}$), and answer:

(i) Why is bias correction needed? Explain starting from $m_0 = v_0 = 0$.
(ii) At step $t = 1$ with $\beta_1 = 0.9$, what is the ratio $\hat{m}_1 / m_1$ without and with bias correction?

<details>
<summary>Answer</summary>

**Complete Adam steps:**
$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t \qquad \text{(1st moment)}$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2 \qquad \text{(2nd moment)}$$
$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}, \quad \hat{v}_t = \frac{v_t}{1 - \beta_2^t} \qquad \text{(bias correction)}$$
$$\theta_{t+1} = \theta_t - \frac{\eta}{\sqrt{\hat{v}_t} + \varepsilon}\,\hat{m}_t$$

**(i) Why bias correction is needed:**
Both $m_0 = 0$ and $v_0 = 0$. At step $t=1$: $m_1 = (1-\beta_1)g_1$. Since $\beta_1 = 0.9$, this gives $m_1 = 0.1 g_1$ — only 10% of the actual gradient. The exponential moving average is initialised too low because the "warm-up" of past values is missing. Bias correction rescales by $1/(1-\beta_1^t)$ to recover the correct estimate.

**(ii) Numerical example at $t=1$, $\beta_1=0.9$:**
- Without correction: $m_1 = (1-0.9)g_1 = 0.1\,g_1$, ratio $= 1$ (no correction applied, uses $m_1$ directly)
- With correction: $\hat{m}_1 = m_1/(1-0.9^1) = 0.1\,g_1/0.1 = g_1$, ratio $\hat{m}_1/m_1 = 10$

Without bias correction the first update uses a gradient estimate that is $10\times$ too small, resulting in an extremely slow first step despite a nominally large learning rate.

</details>

---

**B3. (8 pts)** Explain how Batch Normalisation works:

(i) Write the BN forward pass equations (mean, variance, normalise, scale-and-shift).
(ii) Why can't BN use batch statistics at test time? What does it use instead?
(iii) What is the role of the learnable parameters $\gamma$ and $\beta$? What would go wrong without them?

<details>
<summary>Answer</summary>

**(i) BN forward pass:**
$$\mu_B = \frac{1}{N}\sum_{i=1}^N x_i, \quad \sigma_B^2 = \frac{1}{N}\sum_{i=1}^N (x_i - \mu_B)^2$$
$$\hat{x} = \frac{x - \mu_B}{\sqrt{\sigma_B^2 + \varepsilon}}, \quad y = \gamma\,\hat{x} + \beta$$

**(ii) Test-time behaviour:**
At test time the batch may contain only one sample, making the batch statistics ($\mu_B$, $\sigma_B^2$) meaningless or undefined. BN maintains **running (exponential moving average) statistics** $\mu_\text{run}$ and $\sigma^2_\text{run}$ during training, updating them as $\mu_\text{run} \leftarrow (1-m)\mu_\text{run} + m\,\mu_B$ after each batch. At test time these fixed running statistics replace the batch statistics.

**(iii) Role of $\gamma$ and $\beta$:**
Normalisation forces every layer's output to have zero mean and unit variance, potentially limiting the network's expressiveness — for example, a sigmoid activation after BN would always operate in its near-linear regime. $\gamma$ (scale) and $\beta$ (shift) are learnable parameters that allow the network to undo the normalisation if needed. In the extreme case, the network can learn $\gamma = \sigma_B$, $\beta = \mu_B$ to exactly cancel BN. Without them, the network is constrained to unit-variance, zero-mean activations at every layer, which restricts representational capacity.

</details>

---

**B4. (8 pts)** Consider the Bayesian interpretation of L2 regularisation:

(i) What prior distribution over weights does L2 regularisation correspond to?
(ii) Write the regularised loss and the resulting weight update rule (the weight decay form).
(iii) Explain the equivalence between the hard-constraint and soft-constraint formulations.

<details>
<summary>Answer</summary>

**(i) Prior distribution:**
L2 regularisation is equivalent to placing an isotropic **Gaussian prior** $p(\theta) = \mathcal{N}(0,\, \frac{1}{2\lambda}I)$ on the weights. Maximising the posterior $p(\theta | \mathcal{D}) \propto p(\mathcal{D}|\theta)\,p(\theta)$ under this prior (MAP estimation) is equivalent to minimising the L2-regularised loss.

**(ii) Regularised loss and weight update:**
$$\tilde{J}(\theta) = J(\theta) + \lambda\|\theta\|_2^2$$
$$\nabla_\theta \tilde{J} = \nabla_\theta J + 2\lambda\theta$$
$$\theta \leftarrow \theta - \eta(\nabla_\theta J + 2\lambda\theta) = \underbrace{(1 - 2\eta\lambda)}_{\text{decay factor}}\theta - \eta\nabla_\theta J$$
At each step, the weights are multiplied by $(1-2\eta\lambda) < 1$ — they "decay" toward zero before the gradient update.

**(iii) Hard vs soft constraint equivalence:**
- Hard constraint: $\min_\theta J(\theta)$ subject to $\|\theta\|^2 \leq r$
- Soft constraint: $\min_\theta J(\theta) + \lambda\|\theta\|^2$

Via the Lagrangian $\mathcal{L} = J(\theta) + \lambda(\|\theta\|^2 - r)$, KKT conditions show that for every value of the constraint radius $r$ there exists a unique Lagrange multiplier $\lambda \geq 0$ such that the soft-constraint solution equals the hard-constraint solution, and vice versa. The two formulations parameterise the same family of solutions — $\lambda$ and $r$ are in one-to-one correspondence.

</details>

---

## Section C — Coding (25 pts)

---

**C1. (10 pts)** Implement a `LinearLayer` class with forward and backward passes:

```python
class LinearLayer:
    def __init__(self, n_in, n_out, activation='relu'):
        # He initialisation: W ~ N(0, sqrt(2/n_in)), b = 0
        pass

    def forward(self, x):
        # x: (B, n_in) → returns activated output (B, n_out)
        # Cache intermediate values needed for backward
        pass

    def backward(self, grad):
        # grad: dL/d(output), shape (B, n_out)
        # Returns dx, dW, db
        pass
```

Support `relu` and `sigmoid` activations.

<details>
<summary>Answer</summary>

```python
import torch, math

class LinearLayer:
    def __init__(self, n_in, n_out, activation='relu'):
        self.activation = activation
        self.W = torch.randn(n_in, n_out) * math.sqrt(2.0 / n_in)  # He init
        self.b = torch.zeros(1, n_out)
        self._x = None   # cache input for dW
        self._z = None   # cache pre-activation for activation gradient

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
            return s * (1.0 - s)

    def forward(self, x):
        self._x = x                      # cache: needed for dW = x.T @ dz
        self._z = x @ self.W + self.b    # pre-activation (B, n_out)
        return self._act(self._z)

    def backward(self, grad):
        # grad = dL/d(output), shape (B, n_out)
        dz = grad * self._act_grad(self._z)    # dL/dz  (B, n_out)
        dW = self._x.T @ dz                    # (n_in, n_out)  — same shape as W
        db = dz.sum(dim=0, keepdim=True)       # (1, n_out)
        dx = dz @ self.W.T                     # (B, n_in)  — passes gradient upstream
        return dx, dW, db
```

**Key points:**
- He init: `sqrt(2/n_in)` (designed for ReLU; keeps variance stable across layers)
- Must cache both `x` (for `dW = x.T @ dz`) and `z` (for the activation derivative)
- Shape check: `dW` must match `W`, i.e. `(n_in, n_out)`

</details>

---

**C2. (8 pts)** Implement Adam as a stateful class:

```python
class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        pass

    def step(self, param, grad):
        # Update param in-place and return it
        pass
```

<details>
<summary>Answer</summary>

```python
class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr    = lr
        self.b1    = beta1
        self.b2    = beta2
        self.eps   = eps
        self.t     = 0
        self._m    = None   # 1st moment (initialised lazily)
        self._v    = None   # 2nd moment

    def step(self, param, grad):
        self.t += 1
        if self._m is None:
            self._m = torch.zeros_like(param)
            self._v = torch.zeros_like(param)

        # Update biased moment estimates
        self._m = self.b1 * self._m + (1 - self.b1) * grad
        self._v = self.b2 * self._v + (1 - self.b2) * grad ** 2

        # Bias correction
        m_hat = self._m / (1 - self.b1 ** self.t)
        v_hat = self._v / (1 - self.b2 ** self.t)

        # Parameter update
        param -= self.lr * m_hat / (torch.sqrt(v_hat) + self.eps)
        return param
```

**Key points:**
- `self.t` must be incremented before bias correction (correction factor uses current $t$)
- Second moment uses `grad ** 2` (element-wise square), not `grad`
- Lazy init of `_m`, `_v` avoids needing to know param shape at construction time

</details>

---

**C3. (7 pts)** Implement Batch Normalisation forward pass (without `nn.BatchNorm`):

```python
def batchnorm_forward(x, gamma, beta, eps=1e-5):
    # x:     (N, C, H, W)
    # gamma: (1, C, 1, 1)  — learnable scale
    # beta:  (1, C, 1, 1)  — learnable shift
    # Normalise over (N, H, W) independently per channel C
    pass
```

<details>
<summary>Answer</summary>

```python
def batchnorm_forward(x, gamma, beta, eps=1e-5):
    # Compute per-channel statistics over (N, H, W)
    mu  = x.mean(dim=(0, 2, 3), keepdim=True)   # (1, C, 1, 1)
    var = x.var(dim=(0, 2, 3), keepdim=True)     # (1, C, 1, 1)

    x_hat = (x - mu) / torch.sqrt(var + eps)     # normalise; +eps avoids divide-by-zero
    return gamma * x_hat + beta                  # scale and shift
```

**Key points:**
- `dim=(0, 2, 3)` averages over batch, height, width — leaving only the channel dimension
- `keepdim=True` preserves shape for broadcasting against `x`
- `eps` prevents numerical instability when variance is near zero

</details>

---

## Section D — Essay (35 pts)

---

**D1. (12 pts)** Compare SGD, SGD + Momentum, and Adam:

- Write the update equation for each.
- What problem does each one solve?
- When would you prefer SGD + Momentum over Adam?

<details>
<summary>Answer</summary>

**Update equations:**

*Vanilla SGD:*
$$\theta \leftarrow \theta - \eta \nabla J(\theta)$$

*SGD + Momentum:*
$$v_t = \gamma v_{t-1} + \eta \nabla J(\theta), \qquad \theta \leftarrow \theta - v_t$$

*Adam:* (see Section B2 above)

---

**Problems each one solves:**

- **SGD**: Baseline. No additional mechanism. Oscillates on ill-conditioned loss surfaces (narrow valley in one direction, flat in another) and converges slowly.

- **SGD + Momentum**: Accumulates a velocity vector that is a running average of past gradients. In consistent directions the velocity grows, accelerating convergence. In oscillating directions the velocity terms cancel, damping oscillations. Typical speedup: 10× on valley-shaped surfaces.

- **Adam**: Combines momentum (1st moment) with per-parameter adaptive learning rates (2nd moment). Parameters with consistently large gradients get smaller effective learning rates; parameters with small or sparse gradients get relatively larger steps. Well-suited to non-stationary and sparse gradient problems. Requires almost no learning-rate tuning.

---

**When to prefer SGD + Momentum over Adam:**

1. **Final accuracy on image classification**: Empirically, SGD + Momentum with a carefully tuned learning rate schedule (e.g. cosine annealing) often achieves lower test error than Adam on benchmarks like CIFAR-10/ImageNet. Adam's adaptive scaling can hurt generalisation slightly (the "AdamW" fix partially addresses this).

2. **When you have time to tune hyperparameters**: Adam's adaptive mechanism is a shortcut when tuning $\eta$ is expensive. If compute budget allows a proper learning-rate sweep, SGD + Momentum is often the better long-run choice.

3. **Convex or simple problems**: Adam's extra state (two moment vectors) doubles memory overhead compared to SGD. For simple problems the adaptive mechanism provides no benefit.

</details>

---

**D2. (10 pts)** Explain why overfitting occurs, and analyse how Dropout prevents it from two perspectives:

(i) The ensemble learning perspective.
(ii) The co-adaptation perspective.

<details>
<summary>Answer</summary>

**Why overfitting occurs:**
A model overfits when its capacity (number of parameters) is large relative to the amount of training data. The model memorises idiosyncratic patterns in the training set — including noise — rather than learning the underlying data distribution. Training loss is low but generalisation is poor.

---

**(i) Ensemble learning perspective:**

At each training step, Dropout randomly zeros out each neuron independently with probability $p$. This is equivalent to sampling a different sub-network (a "thinned" network) from the $2^n$ possible sub-networks defined by the $n$ binary masks. Over training, each sub-network is trained on a different subset of the data.

At test time, all neurons are active (no dropout), but their outputs are scaled by $(1-p)$ so that the expected activation matches the training distribution. This is an approximate **geometric mean** of all $2^n$ sub-network predictions — a form of ensemble averaging. Ensembles generalise better than any individual model because their errors are partly uncorrelated and can cancel.

---

**(ii) Co-adaptation perspective:**

Without Dropout, neurons can learn to work in tight coordinated groups — neuron A learns to detect a feature only because neuron B is always there to compensate for A's errors. This *co-adaptation* produces brittle representations that work well on training data but fail when the pattern shifts.

Dropout randomly removes neurons during training, so each neuron cannot rely on any specific other neuron being present. Each neuron is forced to learn features that are independently useful. The result is a more redundant, distributed representation where individual features are meaningful on their own — and such representations generalise much better.

</details>

---

**D3. (13 pts)** The Universal Approximation Theorem states that an MLP can approximate any continuous function. Analyse three limitations this theorem does not address:

(i) What does the theorem guarantee, and what does it *not* guarantee?
(ii) What specific problems does an MLP face when the input is a high-dimensional image (e.g. 256×256×3)?
(iii) How do these limitations motivate the design of CNNs? Use the concept of inductive bias.

<details>
<summary>Answer</summary>

**(i) What the theorem guarantees vs. what it does not:**

The theorem guarantees the *existence* of a network with a single hidden layer (of sufficient width) that can approximate any continuous function on a compact domain to arbitrary precision.

It does **not** guarantee:
- **How to find that network**: gradient descent may converge to a suboptimal solution; the theorem says nothing about learnability.
- **How wide the network must be**: the required width may be exponential in the input dimension.
- **Sample efficiency**: even if the network exists, the amount of training data needed to find it from examples may be enormous.
- **Generalisation**: approximating a function on training points does not imply correct behaviour on unseen inputs.

---

**(ii) Specific problems with high-dimensional image inputs:**

A $256\times256\times3$ image has $196{,}608$ input features. A first layer with 1,000 neurons requires ~200M parameters — far exceeding typical dataset sizes, leading to catastrophic overfitting.

More fundamentally, an MLP flattens the image into a 1D vector, discarding all spatial structure. Adjacent pixels carry no special status compared to distant ones. A cat in the top-left corner and a cat in the bottom-right corner are treated as completely different inputs, because the same pixel values appear at different indices. The network must learn separately that a cat-like pattern at every one of $256 \times 256$ positions corresponds to "cat" — a massively redundant and inefficient learning problem.

---

**(iii) How these limitations motivate CNNs via inductive bias:**

An *inductive bias* is any prior assumption about the data distribution or solution structure that is built into the model architecture, reducing the hypothesis space without requiring data to learn it.

The MLP has essentially no inductive bias for images — it must learn everything from data. CNNs encode two strong, correct priors about natural images:

1. **Locality**: Nearby pixels are more informative than distant pixels for detecting local patterns (edges, textures, shapes). Implemented via local receptive fields — each neuron only connects to a small spatial region.

2. **Translation equivariance**: A visual pattern (an edge, a face) is equally meaningful regardless of where it appears in the image. Implemented via weight sharing — the same filter is convolved across all spatial positions.

These two biases reduce the effective parameter count from ~200M to ~7,000 for the first layer of a typical CNN, and they are almost always correct for natural images. The result is a model that generalises well from small datasets because the hypothesis space has already been constrained to plausible solutions.

</details>
