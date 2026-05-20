# Group 4 — 超越有监督学习
**Week 9: Multi-modal + Week 10: RL + Week 11: Self-Supervised + Week 12: Generative**

---

## 这一组在讲什么

前三组的所有方法都有一个共同前提：**需要标注好的标签**。但标签是昂贵、稀缺、噪声大的。

这一组讲的是四条"不依赖标签（或减少对标签依赖）"的路：

| 方向 | 监督信号来自哪里 | 代表方法 |
|------|---------------|---------|
| **多模态** | 不同模态之间互相监督 | CLIP, BLIP-2, LLaVA |
| **强化学习** | 环境的奖励信号 | Q-Learning, PPO, RLHF |
| **自监督学习** | 数据本身的结构 | MAE, SimCLR, BYOL, DINO |
| **生成模型** | 学习数据分布 | GAN, VAE, DDPM, Flow Matching |

这一组的叙事主线：

> **标签稀缺** → 用数据内部结构监督自己 → 或用环境奖励 → 或用其他模态 → 或干脆学会生成新数据

---

## Week 9 — 多模态大模型（MLLM）

### 核心问题

一个语言模型已经很厉害了，怎么让它同时"看懂"图片？

### 三组件架构

几乎所有 MLLM 都遵循这个架构：

```
图像输入
   ↓
[Vision Encoder]        ← 把图片变成特征向量序列（常用 CLIP-ViT）
   ↓
[Connector Module]      ← 把视觉特征"翻译"成语言模型能理解的 token
   ↓
[Language Model]        ← Transformer Decoder，混合处理视觉+文本 token
   ↓
文字输出（或图像 token）
```

**Vision Encoder**：用 CLIP 预训练的 ViT，已经学会了视觉-语言对齐的表示。

**Connector 的几种设计**：
- **MLP**（LLaVA）：最简单，每个 patch feature 直接线性投影，拼接到文本序列前面
- **Q-Former**（BLIP-2）：用 32 个可学习的 query vector 通过 cross-attention 提炼视觉特征，压缩 token 数量
- **Cross-attention layers**（Flamingo）：在 LLM 的每一层插入 cross-attention，让视觉信息在每个深度都能影响语言理解

**Language Model**：冻结的（或 LoRA 微调的）大型 decoder-only Transformer。

### LoRA：高效微调

把大模型全参数微调代价太高，LoRA 的核心洞察：**微调时权重的更新是低秩的**。

原始权重 $W_0 \in \mathbb{R}^{d \times k}$ 冻结，只训练低秩分解：

$$W = W_0 + \Delta W = W_0 + BA, \quad B \in \mathbb{R}^{d \times r}, A \in \mathbb{R}^{r \times k}, \quad r \ll \min(d, k)$$

参数量从 $dk$ 降到 $r(d+k)$，通常节省 100-500 倍。

**初始化**：$B=0$，$A$ 随机初始化 → 初始时 $\Delta W = BA = 0$，从预训练模型的精确状态开始微调。

### KV Cache：推理加速

自回归生成时，每生成一个新 token，需要重新计算整个序列的 K 和 V。

KV Cache：把已计算的所有位置的 K、V 存起来，下一步只计算新 token 的 K、V，然后拼接到缓存里：

$$\text{output}_t = \sum_{j=1}^{t} \alpha_{t,j} V_j, \quad \text{其中 } K_j, V_j\ (j < t) \text{ 从缓存读取}$$

**代价**：内存正比于 $O(N \cdot L \cdot d)$，长序列时内存压力大。

### MoE：用专家路由扩大容量

Mixture of Experts：维护 $E$ 个独立的 FFN "专家"，每个 token 只激活 top-$k$ 个专家：

$$\text{MoE}(x) = \sum_{i \in \text{top-}k} g_i(x) \cdot f_i(x)$$

**好处**：总参数量 $\propto E$，但每 token 计算量 $\propto k$（$k \ll E$）。大容量，低推理成本。

> **考试提示**：LoRA、KV Cache、MoE 是"效率三件套"，选择题和短答题都可能考它们各自解决什么问题。

---

## Week 10 — 强化学习（RL）

### 为什么需要 RL

监督学习需要"正确答案"标签。但很多任务没有固定的正确答案——下棋、玩游戏、控制机器人——只有"这步走得好不好"的反馈。RL 用**环境奖励**替代标签。

### MDP：RL 的数学框架

**马尔可夫决策过程**（Markov Decision Process）：$(S, A, P, r, \gamma)$

| 符号 | 含义 |
|------|------|
| $S$ | 状态空间 |
| $A$ | 动作空间 |
| $P(s' \| s, a)$ | 状态转移概率 |
| $r(s, a)$ | 即时奖励 |
| $\gamma \in [0,1)$ | 折扣因子（$\gamma$ 越大越有远见）|

**策略** $\pi(a \| s)$：给定状态，输出动作的概率分布。

**目标**：找到最优策略 $\pi^*$，使期望折扣回报最大：

$$J(\pi) = \mathbb{E}_\pi\!\left[\sum_{t=0}^{\infty} \gamma^t r_t\right]$$

### 价值函数

**状态价值函数**：从状态 $s$ 出发、遵循策略 $\pi$ 的期望回报：

$$V^\pi(s) = \mathbb{E}_\pi[G_t \mid s_t = s]$$

**动作价值函数**：在状态 $s$ 执行动作 $a$ 后、遵循策略 $\pi$ 的期望回报：

$$Q^\pi(s, a) = \mathbb{E}_\pi[G_t \mid s_t = s, a_t = a]$$

**优势函数**：动作 $a$ 比平均水平好多少：

$$A^\pi(s, a) = Q^\pi(s, a) - V^\pi(s)$$

**Bellman 方程**（递推结构）：

$$V^\pi(s) = \mathbb{E}_{a \sim \pi}\!\left[r(s,a) + \gamma V^\pi(s')\right]$$

$$Q^*(s,a) = \mathbb{E}\!\left[r + \gamma \max_{a'} Q^*(s', a')\right]$$

### Q-Learning

直接学最优动作价值函数 $Q^*$：

$$Q(s,a) \leftarrow Q(s,a) + \alpha \underbrace{\left[r + \gamma \max_{a'} Q(s', a') - Q(s,a)\right]}_{\text{TD Error}}$$

- **Off-policy**：用 $\max_{a'} Q(s', a')$ 而不管实际采用什么策略
- **Bootstrapping**：用自己当前的估计值更新自己

**DQN**（Deep Q-Network）：用神经网络近似 $Q(s,a)$，加入两个技巧：
- **Experience Replay**：把历史 transitions 存到 buffer，随机采样打破时序相关性
- **Target Network**：用一个慢更新的副本计算目标值，稳定训练

### Policy Gradient

不学价值，直接优化策略参数 $\theta$。**策略梯度定理**：

$$\nabla_\theta J(\theta) = \mathbb{E}\!\left[\nabla_\theta \log \pi_\theta(a_t \mid s_t) \cdot Q^\pi(s_t, a_t)\right]$$

实践中用优势函数 $A^\pi$ 替代 $Q^\pi$（方差更低）：

$$\nabla_\theta J(\theta) = \mathbb{E}\!\left[\nabla_\theta \log \pi_\theta(a \mid s) \cdot A^\pi(s, a)\right]$$

**直觉**：如果这个动作比平均好（$A > 0$），就增大它的概率；如果比平均差（$A < 0$），就减小概率。

### PPO（Proximal Policy Optimization）

策略梯度的问题：步长太大会让策略崩溃。PPO 用 clip 限制每步的策略变化幅度：

$$L^\text{CLIP}(\theta) = \mathbb{E}\!\left[\min\!\left(r_t(\theta) A_t,\ \text{clip}(r_t(\theta), 1-\varepsilon, 1+\varepsilon) A_t\right)\right]$$

其中 $r_t(\theta) = \frac{\pi_\theta(a|s)}{\pi_{\theta_\text{old}}(a|s)}$ 是新旧策略的比值。

### RLHF（Reinforcement Learning from Human Feedback）

用 RL 对齐 LLM 的关键范式（GPT-4、Claude 都用）：

1. **SFT**：在高质量人工示范数据上做有监督微调
2. **Reward Model**：收集人类对模型输出的偏好对，训练一个奖励模型
3. **PPO**：用奖励模型作为环境，用 PPO 优化语言模型策略

---

## Week 11 — 自监督学习（SSL）

### 核心动机

有标注数据少，无标注数据多。能不能用无标注数据学到好的表示？

**自监督学习**：设计一个"借口任务"（pretext task），让数据自己监督自己。

### 生成式 SSL：重建输入

**Autoencoder**：encoder 把输入压缩到瓶颈 $z$，decoder 重建原始输入：

$$\mathcal{L}_\text{AE} = \|x - \hat{x}\|^2$$

**问题**：decoder 太强时，只学像素级重建，encoder 不需要学到语义。

**MAE（Masked Autoencoder）**：遮掉 75% 的 patch，只用剩下 25% 的 patch 重建。任务更难 → encoder 必须学全局语义。

### 对比学习：通过比较来学习

**核心思想**：同一张图的两种增强（正样本对）应该表示相近，不同图的表示应该分开。

**InfoNCE Loss**：

$$\mathcal{L} = -\log \frac{\exp(q \cdot k^+ / \tau)}{\sum_j \exp(q \cdot k_j / \tau)}$$

其中 $q$ 是 query，$k^+$ 是正样本，$k_j$ 包括正负样本，$\tau$ 是温度参数。

**梯度分析**：$\frac{\partial \mathcal{L}}{\partial q} = -\frac{1}{\tau}k^+ + \frac{1}{\tau}\sum_j p_j k_j$

→ 正样本吸引，负样本排斥，且权重 $p_j$ 对**难负样本**（和 $q$ 相似的负样本）更大。

**SimCLR**：最简单的对比学习。同一图的两种随机增强作为正样本，batch 内其他图作为负样本。需要非常大的 batch size。

**MoCo**：用 momentum encoder 维护一个负样本队列，不依赖大 batch：

$$\theta_k \leftarrow m \theta_k + (1-m) \theta_q, \quad m \approx 0.999$$

### 非对比学习：不需要负样本

**BYOL**：teacher-student 架构，student 预测 teacher 的表示：

$$\mathcal{L}_\text{BYOL} = \|q_\theta(x_1) - \text{sg}(z_\xi(x_2))\|^2$$

`sg` 是 stop-gradient。**不对称性**（stop-gradient + predictor）防止了 collapse，不需要负样本。

**SimSiam**：去掉了 momentum teacher，更简单：

$$\mathcal{L} = \frac{1}{2}\|p_1 - \text{sg}(z_2)\|^2 + \frac{1}{2}\|p_2 - \text{sg}(z_1)\|^2$$

### DINO：分布匹配

用 cross-entropy 让 student 匹配 teacher 的 softmax 分布：

$$\mathcal{L}_\text{DINO} = -\sum_k p_t^{(k)} \log p_s^{(k)}$$

两个关键机制：
- **Sharpening**：teacher 用低温度，输出更尖锐（低熵）的分布
- **Centering**：减去 batch 均值，防止某个维度主导，$c \leftarrow mc + (1-m)\mathbb{E}_\text{batch}[z]$

### CLIP：跨模态对比学习

图像 encoder 和文本 encoder 同时训练，让匹配的（图，文）对的相似度最高：

$$\mathcal{L}_\text{CLIP} = -\log \frac{\exp(\text{sim}(v_i, t_i)/\tau)}{\sum_j \exp(\text{sim}(v_i, t_j)/\tau)}$$

**Zero-shot 分类**：把类别名字变成文本描述（"a photo of a dog"），直接和图像比较相似度，不需要任何训练样本。

### 方法对比表

| 方法 | 需要负样本 | 需要 momentum encoder | 核心机制 |
|------|----------|---------------------|---------|
| SimCLR | ✓ (大 batch) | ✗ | 大 batch 对比 |
| MoCo | ✓ (队列) | ✓ | 动量队列 |
| BYOL | ✗ | ✓ | stop-grad + predictor |
| SimSiam | ✗ | ✗ | stop-grad + predictor |
| DINO | ✗ | ✓ | 分布匹配 + centering |
| CLIP | ✓ (跨模态) | ✗ | 图文对比 |

---

## Week 12 — 生成模型

### 核心目标

不是分类，而是**学习数据的分布** $p_\text{data}(x)$，从而能生成新样本。

### 1. GAN（生成对抗网络）

两个网络的博弈：
- **Generator $G$**：把噪声 $z \sim p_z$ 映射到数据空间
- **Discriminator $D$**：判断输入是真实数据还是生成数据（输出 0-1 概率）

**Minimax 目标**：

$$\min_G \max_D \mathcal{L} = \mathbb{E}_{x \sim p_r}[\log D(x)] + \mathbb{E}_{z \sim p_z}[\log(1 - D(G(z)))]$$

**最优判别器**（固定 $G$ 时）：

$$D^*(x) = \frac{p_r(x)}{p_r(x) + p_g(x)}$$

**代入后**，GAN 本质上在最小化真实分布和生成分布的 **Jensen-Shannon 散度**：

$$\mathcal{L}(G, D^*) = 2\,\text{JS}(p_r \| p_g) - 2\log 2$$

**训练不稳定的原因**：当 $p_r$ 和 $p_g$ 的支撑集不重叠时（高维空间中常见），存在完美判别器，Generator 收到的梯度趋近于零。

### 2. WGAN（Wasserstein GAN）

把 JS 散度替换为 **Wasserstein-1 距离**（Earth Mover's Distance），即使分布不重叠也有意义：

$$W(p_r, p_g) = \sup_{\|f\|_L \leq 1} \mathbb{E}_{x \sim p_r}[f(x)] - \mathbb{E}_{x \sim p_g}[f(x)]$$

用 **Lipschitz 连续**的"critic"网络 $f_w$ 近似上确界：

$$\max_w \mathbb{E}_{x \sim p_r}[f_w(x)] - \mathbb{E}_{z \sim p_z}[f_w(G(z))]$$

Lipschitz 约束的实现方式：权重裁剪（原始 WGAN）或 gradient penalty（WGAN-GP）。

### 3. VAE（变分自编码器）

**思路**：假设数据由隐变量 $z$ 生成，先验 $p(z) = \mathcal{N}(0,I)$，生成过程 $x \sim p_\theta(x|z)$。

直接最大化 $\log p_\theta(x)$ 是 intractable，引入近似后验 $q_\phi(z|x)$，推导 **ELBO**（Evidence Lower Bound）：

$$\log p_\theta(x) \geq \underbrace{\mathbb{E}_{z \sim q_\phi}[\log p_\theta(x|z)]}_{\text{重建项}} - \underbrace{D_\text{KL}(q_\phi(z|x) \| p(z))}_{\text{正则项}}$$

- **重建项**：Decoder 要能从 $z$ 重建 $x$
- **KL 正则项**：让近似后验靠近标准高斯先验，使隐空间连续可采样

**重参数化技巧（Reparameterization Trick）**：让采样步骤可以反向传播：

$$z = \mu_\phi(x) + \sigma_\phi(x) \odot \epsilon, \quad \epsilon \sim \mathcal{N}(0,I)$$

**VAE 的缺点**：生成的图像偏模糊（重建 loss 用 MSE，倾向于平均多个模式）。

### 4. DDPM（扩散模型）

**思路**：学会逆转一个逐步加噪的过程。

**前向过程**（加噪，固定无参数）：

$$q(x_t | x_{t-1}) = \mathcal{N}\!\left(x_t; \sqrt{1-\beta_t}\,x_{t-1},\ \beta_t I\right)$$

直接从 $x_0$ 采样 $x_t$：

$$x_t = \sqrt{\bar{\alpha}_t}\,x_0 + \sqrt{1-\bar{\alpha}_t}\,\epsilon, \quad \epsilon \sim \mathcal{N}(0,I)$$

其中 $\bar{\alpha}_t = \prod_{s=1}^{t}(1-\beta_s)$。

**训练目标**：让网络预测被加入的噪声：

$$\mathcal{L} = \mathbb{E}_{x_0, \epsilon, t}\!\left[\|\epsilon - \epsilon_\theta(x_t, t)\|^2\right]$$

**生成时**：从高斯噪声 $x_T$ 出发，反复用网络预测噪声、去噪，逐步恢复 $x_0$。

### 5. Flow Matching（新一代生成框架）

**核心思想**：直接学习一个**速度场** $v_\theta(x,t)$，把噪声分布 $p_0$ 传输到数据分布 $p_1$。

训练数据构建：
$$x_0 \sim \mathcal{N}(0,I), \quad x_1 \sim p_\text{data}, \quad x_t = (1-t)x_0 + t x_1$$

插值点的目标速度（直线路径）：
$$u_t = x_1 - x_0$$

训练目标（监督回归）：
$$\mathcal{L}_\text{FM} = \mathbb{E}_{x_0, x_1, t}\!\left[\|v_\theta(x_t, t) - (x_1 - x_0)\|^2\right]$$

**生成**：从 $x_0 \sim \mathcal{N}(0,I)$ 出发，积分 ODE $\frac{dx}{dt} = v_\theta(x,t)$，得到 $x_1 \sim p_\text{data}$。

### 生成模型对比

| 模型 | 训练方式 | 能否计算密度 | 生成质量 | 代表缺点 |
|------|---------|------------|---------|---------|
| GAN | 对抗博弈 | ✗（隐式）| 高（清晰）| 训练不稳定，mode collapse |
| VAE | 最大化 ELBO | ✓（近似）| 中（模糊）| 生成图偏糊 |
| DDPM | 去噪回归 | ✗ | 高 | 推理步骤多，慢 |
| Flow Matching | 速度场回归 | ✓（ODE）| 高 | 随机配对导致路径不直 |

---

## 能力检查清单

**Week 9 多模态（短答 / 选择）**
- [ ] 描述 MLLM 的三组件架构（视觉编码器、Connector、LLM）
- [ ] 说出 LoRA 的核心公式 $\Delta W = BA$，以及为什么 $B$ 初始化为零
- [ ] 解释 KV Cache 为什么能加速推理，它的内存代价是什么
- [ ] 解释 MoE 的 trade-off：总参数多，每 token 计算少

**Week 10 强化学习（短答 / 论述）**
- [ ] 写出 MDP 的五元组 $(S, A, P, r, \gamma)$，解释每个符号
- [ ] 写出 Bellman 方程（$V^\pi$ 和 $Q^*$ 两个版本）
- [ ] 写出 Q-learning 的更新规则，解释 TD Error
- [ ] 解释策略梯度定理（为什么优化 $\log\pi \cdot A$）
- [ ] 解释 RLHF 的三个步骤（SFT → Reward Model → PPO）

**Week 11 自监督学习（短答 / 选择）**
- [ ] 写出 InfoNCE loss，解释温度参数 $\tau$ 的作用
- [ ] 解释 SimCLR 和 MoCo 的区别（大 batch vs 动量队列）
- [ ] 解释 BYOL 为什么不需要负样本（stop-gradient + predictor 的不对称性）
- [ ] 解释 DINO 的 sharpening 和 centering 各自防止什么（低熵目标 + 防止维度主导）
- [ ] 解释 CLIP 的 zero-shot 分类原理

**Week 12 生成模型（短答 / 论述 / 手写代码）**
- [ ] 写出 GAN 的 minimax 目标，推导最优判别器 $D^*(x) = \frac{p_r}{p_r + p_g}$
- [ ] 解释 GAN 为什么训练不稳定（分布不重叠 → 梯度消失）
- [ ] 解释 WGAN 用什么距离替代 JS 散度，为什么更稳定
- [ ] 写出 VAE 的 ELBO 公式，解释重建项和 KL 正则项各自的作用
- [ ] 解释重参数化技巧为什么必要（采样不可微）
- [ ] 写出 DDPM 的训练目标（预测噪声的 MSE）
- [ ] 解释 Flow Matching 的训练数据如何构建（线性插值），目标速度是什么

---

## 代码对应数学

### 算法一：GAN 训练循环

```python
def train_gan_step(real_data, G, D, g_optim, d_optim):
    B = real_data.shape[0]

    # ── 训练 Discriminator ────────────────────────────────────────
    z = torch.randn(B, latent_dim)
    fake_data = G(z).detach()              # 不需要传梯度给 G

    real_loss = -torch.log(D(real_data) + 1e-8).mean()    # 希望 D(real) → 1
    fake_loss = -torch.log(1 - D(fake_data) + 1e-8).mean() # 希望 D(fake) → 0
    d_loss = real_loss + fake_loss

    d_optim.zero_grad()
    d_loss.backward()
    d_optim.step()

    # ── 训练 Generator ────────────────────────────────────────────
    z = torch.randn(B, latent_dim)
    fake_data = G(z)

    # G 希望 D(G(z)) → 1，所以最小化 -log(D(G(z)))
    g_loss = -torch.log(D(fake_data) + 1e-8).mean()

    g_optim.zero_grad()
    g_loss.backward()
    g_optim.step()
```

---

### 算法二：VAE 前向 + ELBO Loss

```python
class VAE(nn.Module):
    def encode(self, x):
        h = self.encoder(x)
        mu, log_var = self.fc_mu(h), self.fc_var(h)
        return mu, log_var

    def reparameterize(self, mu, log_var):
        # 重参数化：z = mu + std * eps，让梯度能反传
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)      # eps ~ N(0, I)
        return mu + std * eps            # z ~ N(mu, std^2)

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        mu, log_var = self.encode(x)
        z = self.reparameterize(mu, log_var)
        x_hat = self.decode(z)

        # ELBO = 重建项 - KL 散度
        recon_loss = F.mse_loss(x_hat, x, reduction='sum')
        kl_loss = -0.5 * torch.sum(1 + log_var - mu**2 - torch.exp(log_var))
        #                              ↑ KL(N(mu,sigma^2) || N(0,1)) 的解析解

        return recon_loss + kl_loss
```

**记忆要点**：KL 散度有解析解 $-\frac{1}{2}\sum(1 + \log\sigma^2 - \mu^2 - \sigma^2)$；重参数化是让 $z$ 的随机性来自 $\epsilon$，而不是来自 $z$ 本身。

---

### 算法三：DDPM 前向加噪 + 训练

```python
def q_sample(x0, t, alphas_bar):
    # 直接从 x0 采样 x_t：x_t = sqrt(alpha_bar_t) * x0 + sqrt(1-alpha_bar_t) * eps
    sqrt_ab   = alphas_bar[t].sqrt().view(-1, 1, 1, 1)
    sqrt_1_ab = (1 - alphas_bar[t]).sqrt().view(-1, 1, 1, 1)
    eps = torch.randn_like(x0)
    return sqrt_ab * x0 + sqrt_1_ab * eps, eps   # 返回 x_t 和真实噪声 eps

def ddpm_loss(model, x0, alphas_bar):
    B = x0.shape[0]
    t = torch.randint(0, T, (B,))            # 随机采样时间步
    x_t, eps = q_sample(x0, t, alphas_bar)  # 加噪
    eps_pred = model(x_t, t)                 # 网络预测噪声
    return F.mse_loss(eps_pred, eps)         # 预测噪声 vs 真实噪声
```

---

### 默写练习

1. 从空白写出 GAN 的 D 和 G 的损失函数（各一行），以及训练时为什么要 `.detach()`
2. 从空白写出 VAE 的 ELBO 公式，解释重参数化为什么必要
3. 从空白写出 DDPM 的 $q(x_t | x_0)$ 公式（直接从 $x_0$ 采样），以及训练目标
4. 解释：InfoNCE loss 为什么对难负样本（和 query 相似的负样本）赋予更大权重？

---

## 总结：四组的叙事地图

```
Group 1: 基础
  线性 → MLP → Backprop → Adam → Regularization

Group 2: 结构化数据
  MLP 忽略空间 → CNN (局部性+权重共享)
  CNN 需要网格 → GNN (邻居聚合)

Group 3: 序列数据
  静态 → RNN (记忆) → 梯度消失 → LSTM (门控)
  无法并行 → Transformer (Self-Attention)
  BERT (双向,理解) / GPT (因果,生成)
  图像序列化 → ViT
  O(N²) → SSM/Mamba

Group 4: 超越监督
  标签贵 → 自监督 (数据监督自己)
        → 对比学习 (SimCLR → BYOL → DINO)
        → 跨模态 (CLIP, MLLM)
        → 环境奖励 (RL → RLHF)
        → 学会生成 (GAN → VAE → Diffusion → Flow Matching)
```

→ **去每周 Tutorial 的 Part C 做考试题，检验掌握程度。**
