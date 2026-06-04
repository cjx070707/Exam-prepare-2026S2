# COMP5329 Deep Learning — Coding 专项练习

> **覆盖范围**：`手写代码速查表.md` 全部 22 个代码块，按 Tutorial 周次排列。  
> **风格**：每题给情境提示，你从头写代码，写完展开 `> [!success]- Answer` 对照。  
> **用法**：纸笔默写 → 展开答案 → 关键记忆点用 `📌` 标注。  
> **星级**同速查表：`★★★` 必默、`★★` 重要、`★` 有余力。

---

## Week 3 — Foundations

### C1 · Activation Functions (Forward + Backward) `★★★`

Implement **Sigmoid**, **Tanh**, and **ReLU** as classes, each with `forward(z)` and `backward(grad)` methods. Your `backward` must use values cached in `forward` to compute the local gradient and multiply by the incoming `grad`.

> [!success]- Answer
>
> ```python
> # Sigmoid
> def forward(self, z):
>     self.s = 1 / (1 + torch.exp(-z))
>     return self.s
> def backward(self, grad):
>     return grad * self.s * (1 - self.s)
>
> # Tanh
> def forward(self, z):
>     self.out = torch.tanh(z)
>     return self.out
> def backward(self, grad):
>     return grad * (1 - self.out ** 2)
>
> # ReLU
> def forward(self, z):
>     self.z = z
>     return torch.clamp(z, min=0)
> def backward(self, grad):
>     return grad * (self.z > 0).float()
> ```
>
> 📌 **关键**：Sigmoid 导数 $s(1-s)$、Tanh 导数 $1-\tanh^2$、ReLU 导数是 0/1 门控。都要 cache 前向值，backward 里乘 incoming `grad`（链式法则）。

---

### C2 · HiddenLayer (Forward + Backward) `★★★`

Implement a hidden layer with `forward(X)` and `backward(grad)`. Forward: $z = X W + b$, then pass through activation. Backward: compute `dW`, `db`, and return the gradient to pass to the previous layer.

> [!success]- Answer
>
> ```python
> def forward(self, X):
>     self.X = X
>     z = X @ self.W + self.b
>     return self.act.forward(z)
>
> def backward(self, grad):
>     dz = self.act.backward(grad)
>     self.dW = self.X.T @ dz
>     self.db = dz.sum(dim=0, keepdim=True)
>     return dz @ self.W.T
> ```
>
> 📌 **关键**：`dW = X^T @ dz`（输入转置乘局部梯度），`db = dz.sum(dim=0)`（batch 求和），返回 `dz @ W^T` 传给前一层。必须 cache `self.X`。

---

### C3 · CrossEntropyLoss (Forward + Backward) `★★★`

Implement cross-entropy loss with **numerical stability** (log-sum-exp trick). Forward takes `(logits, labels)` and returns scalar loss. Backward returns the gradient w.r.t. logits.

> [!success]- Answer
>
> ```python
> def forward(self, logits, labels):
>     N = logits.shape[0]
>     shifted = logits - logits.max(dim=1, keepdim=True).values
>     log_sum = torch.log(torch.exp(shifted).sum(dim=1, keepdim=True))
>     log_probs = shifted - log_sum
>     self.probs, self.labels = torch.exp(log_probs), labels
>     return -log_probs[torch.arange(N), labels].mean()
>
> def backward(self):
>     N = self.probs.shape[0]
>     grad = self.probs.clone()
>     grad[torch.arange(N), self.labels] -= 1.0
>     return grad / N
> ```
>
> 📌 **关键**：先减 max 防溢出（log-sum-exp trick）。Backward 梯度 = softmax 概率，但正确类位置减 1，再除 N。公式：$\nabla_{\text{logits}} = (\text{softmax} - \text{one\_hot}) / N$。

---

### C4 · Adam Optimizer `★★★`

Given a parameter $\theta$ and its gradient $g$, implement one step of Adam update. Include bias correction.

> [!success]- Answer
>
> ```python
> # 初始化：m = 0, v = 0, t = 0
> t += 1
> m = β1 * m + (1 - β1) * g
> v = β2 * v + (1 - β2) * g ** 2
> m_hat = m / (1 - β1 ** t)
> v_hat = v / (1 - β2 ** t)
> θ -= lr * m_hat / (sqrt(v_hat) + ε)
> ```
>
> 📌 **关键**：m 是一阶矩（方向），v 是二阶矩（缩放），bias correction 除以 $(1-\beta^t)$。典型值 $\beta_1=0.9,\beta_2=0.999,\epsilon=10^{-8}$。

---

### C4b · Weight Initialization (Xavier / He) `★★`

Write the initialization code for Xavier (for Tanh/Sigmoid) and He/Kaiming (for ReLU). Include the 4D conv case.

> [!success]- Answer
>
> ```python
> # Xavier（Tanh / Sigmoid）
> std = (2 / (fan_in + fan_out)) ** 0.5
> W   = torch.randn(fan_in, fan_out) * std
>
> # He（ReLU）
> std = (2 / fan_in) ** 0.5
> W   = torch.randn(fan_in, fan_out) * std
>
> # 4D Conv：fan_in 含 kH*kW
> fan_in  = C_in  * kH * kW
> fan_out = C_out * kH * kW
> ```
>
> 📌 **关键**：He 方差比 Xavier 大（分子 2 vs 分母含 fan_out），因为 ReLU 置零约一半激活。Conv 的 fan_in 要乘 kernel 面积。

---

## Week 4 — Regularization

### C5 · Inverted Dropout `★★★`

Implement inverted dropout for training. Ensure test time needs no change.

> [!success]- Answer
>
> ```python
> # Training
> keep = (torch.rand_like(out) > dropout_rate).float()
> out  = out * keep / (1.0 - dropout_rate)
>
> # Test：直接用 out，不乘 mask，不缩放
> ```
>
> 📌 **关键**：训练时除以 $(1-p)$ 放大存活单元（inverted），这样**测试时不需要任何改动**。注意 `torch.rand_like` 生成 $[0,1)$ 均匀随机，`> dropout_rate` 产生 keep mask。

---

### C6 · Batch Normalization (Forward + Backward) `★★★`

Implement BN forward (compute mean, var, normalize, scale+shift) and backward (gradient w.r.t. input, using cached values).

> [!success]- Answer
>
> ```python
> def forward(self, z):
>     B = z.shape[0]
>     mu  = z.mean(0, keepdim=True)
>     var = z.var(0, keepdim=True, unbiased=False)
>     std = torch.sqrt(var + 1e-5)
>     z_hat = (z - mu) / std
>     self._cache = (z_hat, std, B)
>     return self.gamma * z_hat + self.beta
>
> def backward(self, grad):
>     z_hat, std, B = self._cache
>     dz_hat = grad * self.gamma
>     dz = (1.0 / (B * std)) * (
>         B * dz_hat
>         - dz_hat.sum(0, keepdim=True)
>         - z_hat * (dz_hat * z_hat).sum(0, keepdim=True)
>     )
>     return dz
> ```
>
> 📌 **关键**：Forward 三步：中心化 → 除 std → scale+shift ($\gamma\hat z + \beta$)。Backward 公式有三项（来自对 mean 和 var 的依赖），cache `z_hat, std, B`。`unbiased=False` 用总体方差。

---

### C6b · SGD + L2 Weight Decay `★★`

Write the weight update with L2 regularization.

> [!success]- Answer
>
> ```python
> layer.W -= lr * (dW + weight_decay * layer.W)
> ```
>
> 📌 **关键**：L2 正则梯度 = 原梯度 + $\lambda W$（权重越大惩罚越大）。和 Adam 的 decoupled weight decay (AdamW) 不同——这里是耦合的。

---

### C7b · Early Stopping `★★`

Implement the early stopping logic inside a training loop. Track best validation loss, snapshot model, restore on patience exhaustion.

> [!success]- Answer
>
> ```python
> best_val, best_snap, no_imp = float("inf"), None, 0
> for epoch in range(1, n_epochs + 1):
>     # ... train one epoch ...
>     if X_val is not None:
>         vl = criterion.forward(model.forward(X_val), y_val).item()
>         if patience is not None:
>             if vl < best_val - 1e-5:
>                 best_val, best_snap, no_imp = vl, model.snapshot(), 0
>             else:
>                 no_imp += 1
>                 if no_imp >= patience:
>                     model.restore(best_snap)
>                     break
> ```
>
> 📌 **关键**：val 变好 → 存 snapshot、重置 patience；否则累计 `no_imp`，满 patience 则 **restore best** 并 break。用 `1e-5` 容差防浮点抖动。

---

## Week 5 — CNN

### C7 · Conv2D 尺寸公式 + Naive 实现 `★★★`

Write the output size formula for a conv layer. Then implement a naive `conv2d(x, w, stride, padding)` using loops (no `nn.Conv2d`).

> [!success]- Answer
>
> ```python
> H_out = (H + 2 * padding - kH) // stride + 1
>
> def naive_conv2d(x, w, stride=1, padding=0):
>     N, C_in, H, W = x.shape
>     C_out, _, kH, kW = w.shape
>     H_out = (H + 2 * padding - kH) // stride + 1
>     W_out = (W + 2 * padding - kW) // stride + 1
>     if padding > 0:
>         x = F.pad(x, [padding] * 4)
>     out = torch.zeros(N, C_out, H_out, W_out)
>     for i in range(H_out):
>         for j in range(W_out):
>             patch = x[:, :, i*stride:i*stride+kH, j*stride:j*stride+kW]
>             out[:, :, i, j] = (patch.unsqueeze(1) * w.unsqueeze(0)).sum(dim=(2,3,4))
>     return out
> ```
>
> 📌 **关键**：公式 $(H + 2P - k) / s + 1$（整除）。Naive 实现：滑窗取 patch，与 kernel 逐元素乘再 sum。`patch.unsqueeze(1) * w.unsqueeze(0)` 广播处理 batch 和多 output channel。

---

### C7c · Max Pooling `★★`

Implement `max_pool2d(x, k, stride)`.

> [!success]- Answer
>
> ```python
> def max_pool2d(x, k=2, stride=2):
>     N, C, H, W = x.shape
>     H_out = (H - k) // stride + 1
>     W_out = (W - k) // stride + 1
>     x_col = F.unfold(x, kernel_size=k, stride=stride)
>     x_col = x_col.view(N, C, k * k, H_out * W_out)
>     return x_col.max(dim=2).values.view(N, C, H_out, W_out)
> ```
>
> 📌 **关键**：`unfold` 把每个窗口展成列，再沿窗口维取 max。尺寸公式同 conv 但无 padding。

---

### C8 · ResNet BasicBlock (`nn.Module`) `★★★`

Implement a residual block: two 3×3 conv + BN layers, skip connection with optional 1×1 projection.

> [!success]- Answer
>
> ```python
> class BasicBlock(nn.Module):
>     def __init__(self, in_ch, out_ch, stride=1):
>         super().__init__()
>         self.conv1 = nn.Conv2d(in_ch, out_ch, 3, stride=stride, padding=1, bias=False)
>         self.bn1   = nn.BatchNorm2d(out_ch)
>         self.conv2 = nn.Conv2d(out_ch, out_ch, 3, stride=1, padding=1, bias=False)
>         self.bn2   = nn.BatchNorm2d(out_ch)
>         self.shortcut = nn.Identity()
>         if stride != 1 or in_ch != out_ch:
>             self.shortcut = nn.Sequential(
>                 nn.Conv2d(in_ch, out_ch, 1, stride=stride, bias=False),
>                 nn.BatchNorm2d(out_ch),
>             )
>
>     def forward(self, x):
>         out = F.relu(self.bn1(self.conv1(x)))
>         out = self.bn2(self.conv2(out))
>         return F.relu(out + self.shortcut(x))   # F(x) + x
> ```
>
> 📌 **关键**：`F(x) + x` — 残差连接。stride≠1 或 channel 变时用 1×1 conv 对齐维度。BN 放 conv 后、ReLU 前。最后的 ReLU 在**加完 shortcut 之后**。`bias=False` 因为后面接 BN。

---

### C9 · transforms.Compose + Training Loop (val / 早停 / 存盘) `★★`

Write `transforms.Compose` for ImageNet (resize 224, random flip, to tensor [0,1]). Then write a training loop for 100 epochs with validation every 5 epochs, early stopping, and saving model every 10 epochs.

> [!success]- Answer
>
> ```python
> # transforms
> transform = transforms.Compose([
>     transforms.Resize((224, 224)),
>     transforms.RandomHorizontalFlip(),
>     transforms.ToTensor(),              # float32, RGB ∈ [0, 1]
> ])
> dataset = torchvision.datasets.ImageNet('path', split='train', transform=transform)
> data_loader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)
> ```
>
> ```python
> # Training loop
> best_val_acc, no_improve = 0.0, 0
> for epoch in range(1, 101):
>     model.train()
>     for x, y in train_loader:
>         x, y = x.to(device), y.to(device)
>         optimizer.zero_grad()
>         loss = criterion(model(x), y)
>         loss.backward()
>         optimizer.step()
>
>     if epoch % 5 == 0:                   # validate every 5
>         model.eval()
>         correct = total = 0
>         with torch.no_grad():
>             for x, y in val_loader:
>                 x, y = x.to(device), y.to(device)
>                 correct += (model(x).argmax(1) == y).sum().item()
>                 total += y.size(0)
>         val_acc = correct / total
>         print(f"Epoch {epoch}  val acc: {val_acc:.4f}")
>         if val_acc > best_val_acc:
>             best_val_acc = val_acc
>             best_state = model.state_dict()
>             no_improve = 0
>         else:
>             no_improve += 1
>         if no_improve >= 3:              # early stopping
>             print("Early stopping")
>             model.load_state_dict(best_state)
>             break
>
>     if epoch % 10 == 0:                  # save every 10
>         torch.save(model.state_dict(), "inception.pth")
> ```
>
> 📌 **关键**：`ToTensor()` 自动归到 [0,1]，不要多加 `Normalize` 除非题干要求。`model.train()` / `model.eval()` 切换 BN/Dropout 行为。`torch.no_grad()` 省显存。

---

## Week 6 — Graph Neural Networks

### C10 · build_A_hat_norm + GCNLayer + GCN `★★★`

Implement: (1) the normalized adjacency matrix $\tilde D^{-1/2}\tilde A\tilde D^{-1/2}$ where $\tilde A = A + I$; (2) a single GCN layer; (3) a two-layer GCN classifier.

> [!success]- Answer
>
> ```python
> def build_A_hat_norm(A):
>     n = A.shape[0]
>     A_hat = A + np.eye(n)
>     D_inv_sqrt = np.diag(A_hat.sum(axis=1) ** (-0.5))
>     return torch.tensor(D_inv_sqrt @ A_hat @ D_inv_sqrt, dtype=torch.float32)
> ```
>
> ```python
> class GCNLayer(nn.Module):
>     def __init__(self, in_features, out_features, activation=True):
>         super().__init__()
>         self.W = nn.Parameter(torch.empty(in_features, out_features))
>         self.activation = activation
>         nn.init.xavier_uniform_(self.W)
>
>     def forward(self, H, A_hat_norm):
>         out = (A_hat_norm @ H) @ self.W
>         return F.relu(out) if self.activation else out
>
> class GCN(nn.Module):
>     def __init__(self, in_f, hidden, num_classes):
>         super().__init__()
>         self.gcn1 = GCNLayer(in_f, hidden, True)
>         self.gcn2 = GCNLayer(hidden, num_classes, False)
>
>     def forward(self, H, A_hat_norm):
>         return self.gcn2(self.gcn1(H, A_hat_norm), A_hat_norm)
> ```
>
> 📌 **关键**：$\tilde A = A + I$（自环），$\tilde D^{-1/2}\tilde A\tilde D^{-1/2}$ 对称归一化。GCN 公式 $H^{(l+1)} = \sigma(\hat A H^{(l)} W^{(l)})$。最后一层**不加 ReLU**（输出 logits 给 CrossEntropy）。用 `xavier_uniform_` 初始化。

---

## Week 7 — Sequence Modeling I

### C11 · LSTMCell `★★★`

Implement a single LSTM cell. Input: `x_t` and previous state `(h_prev, c_prev)`. Compute the four gates (input, forget, cell candidate, output) and return `(h_t, c_t)`.

> [!success]- Answer
>
> ```python
> class LSTMCell(nn.Module):
>     def __init__(self, in_features, hidden_size):
>         super().__init__()
>         self.gates = nn.Linear(in_features + hidden_size, 4 * hidden_size)
>
>     def forward(self, x_t, state):
>         h_prev, c_prev = state
>         concat = torch.cat([h_prev, x_t], dim=1)
>         i_pre, f_pre, g_pre, o_pre = self.gates(concat).chunk(4, dim=1)
>         i_t = torch.sigmoid(i_pre)          # input gate
>         f_t = torch.sigmoid(f_pre)          # forget gate
>         g_t = torch.tanh(g_pre)             # candidate
>         o_t = torch.sigmoid(o_pre)          # output gate
>         c_t = f_t * c_prev + i_t * g_t      # cell: 加法更新
>         h_t = o_t * torch.tanh(c_t)         # hidden
>         return h_t, c_t
> ```
>
> 📌 **关键**：四个门共用一个 Linear（拼接后 chunk 分 4 份更高效）。cell 是**加法更新** $c_t = f_t \odot c_{t-1} + i_t \odot g_t$（缓解梯度消失的核心）。三个门用 sigmoid（0-1 门控），candidate 用 tanh（值域 [-1,1]）。

---

### C12 · MultiHeadSelfAttention `★★★`

Implement multi-head self-attention from scratch. Include $W_Q, W_K, W_V, W_O$, splitting into heads, scaled dot-product, optional mask, and concatenation.

> [!success]- Answer
>
> ```python
> class MultiHeadSelfAttention(nn.Module):
>     def __init__(self, d_model, num_heads):
>         super().__init__()
>         assert d_model % num_heads == 0
>         self.num_heads = num_heads
>         self.d_k = d_model // num_heads
>         self.W_q = nn.Linear(d_model, d_model)
>         self.W_k = nn.Linear(d_model, d_model)
>         self.W_v = nn.Linear(d_model, d_model)
>         self.W_o = nn.Linear(d_model, d_model)
>
>     def forward(self, x, mask=None):
>         B, T, _ = x.shape
>         H, d_k = self.num_heads, self.d_k
>         Q = self.W_q(x).view(B, T, H, d_k).transpose(1, 2)  # (B, H, T, d_k)
>         K = self.W_k(x).view(B, T, H, d_k).transpose(1, 2)
>         V = self.W_v(x).view(B, T, H, d_k).transpose(1, 2)
>         scores = (Q @ K.transpose(-2, -1)) / math.sqrt(d_k)  # (B, H, T, T)
>         if mask is not None:
>             scores = scores.masked_fill(mask == 0, float("-inf"))
>         attn = F.softmax(scores, dim=-1)
>         out = (attn @ V).transpose(1, 2).contiguous().view(B, T, -1)
>         return self.W_o(out), attn
> ```
>
> 📌 **关键**：`view(B,T,H,d_k).transpose(1,2)` 把 head 维提到前面。除以 $\sqrt{d_k}$ 防 softmax 饱和。mask 填 `-inf`（不是 0）。最后 `transpose(1,2).contiguous().view` 拼回去过 $W_O$。

---

## Week 8 — Sequence Modeling II

### C13 · ViT Patch Embedding `★★★`

Implement the patch embedding for Vision Transformer: unfold image into patches, project to embeddings, prepend CLS token, add positional embeddings.

> [!success]- Answer
>
> ```python
> class ViTPatchEmbedding(nn.Module):
>     def __init__(self, img_size, patch_size, in_chans, embed_dim):
>         super().__init__()
>         self.num_patches = (img_size // patch_size) ** 2
>         self.unfold = nn.Unfold(kernel_size=patch_size, stride=patch_size)
>         self.proj = nn.Linear(in_chans * patch_size ** 2, embed_dim)
>         self.cls_token = nn.Parameter(torch.zeros(1, 1, embed_dim))
>         self.pos_embed = nn.Parameter(torch.zeros(1, 1 + self.num_patches, embed_dim))
>
>     def forward(self, x):
>         B = x.shape[0]
>         patches = self.unfold(x)                          # (B, C*P*P, N)
>         tokens = self.proj(patches.transpose(1, 2))       # (B, N, embed_dim)
>         cls = self.cls_token.expand(B, -1, -1)            # (B, 1, embed_dim)
>         tokens = torch.cat([cls, tokens], dim=1) + self.pos_embed
>         return tokens
> ```
>
> 📌 **关键**：`Unfold` 切 patch 并展平（等价于 stride=patch_size 的 conv）。CLS token 用 `expand` 广播到 batch。pos_embed 长度 = 1 + num_patches（CLS 也有位置）。所有 patch + CLS **加**位置编码（不是 concat）。

---

### C14 · SSM Convolution Kernel `★★`

Build the SSM convolution kernel: given discretized $\bar A, \bar B, C$ and sequence length $L$, compute $K$ such that $y = \text{conv1d}(u, K)$.

> [!success]- Answer
>
> ```python
> def build_ssm_kernel(A_bar, B_bar, C, L):
>     K = torch.zeros(L)
>     A_pow_B = B_bar.clone()
>     for i in range(L):
>         K[i] = (C @ A_pow_B).squeeze()
>         A_pow_B = A_bar @ A_pow_B
>     return K   # y = conv1d(u, K)
> ```
>
> 📌 **关键**：$K_i = C \bar A^i \bar B$，逐步累积 $\bar A$ 的幂次。这是 SSM 的"卷积视图"——训练时用 FFT 加速，推理时可切回递推。

---

## Week 9 — Multi-Modal Foundation Models

### C15 · Cross-Attention `★★`

Implement cross-attention where Q comes from `x_query` and K, V come from `x_memory` (a different sequence). Support an optional `memory_mask`.

> [!success]- Answer
>
> ```python
> class CrossAttention(nn.Module):
>     def __init__(self, d_model, num_heads):
>         super().__init__()
>         self.num_heads = num_heads
>         self.d_k = d_model // num_heads
>         self.W_q = nn.Linear(d_model, d_model)
>         self.W_k = nn.Linear(d_model, d_model)
>         self.W_v = nn.Linear(d_model, d_model)
>         self.W_o = nn.Linear(d_model, d_model)
>
>     def forward(self, x_query, x_memory, memory_mask=None):
>         B, T_q, _ = x_query.shape
>         T_m = x_memory.size(1)
>         H, d_k = self.num_heads, self.d_k
>         Q = self.W_q(x_query).view(B, T_q, H, d_k).transpose(1, 2)
>         K = self.W_k(x_memory).view(B, T_m, H, d_k).transpose(1, 2)
>         V = self.W_v(x_memory).view(B, T_m, H, d_k).transpose(1, 2)
>         scores = (Q @ K.transpose(-2, -1)) / math.sqrt(d_k)
>         if memory_mask is not None:
>             scores = scores.masked_fill(memory_mask[:, None, None, :] == 0, float("-inf"))
>         attn = F.softmax(scores, dim=-1)
>         context = (attn @ V).transpose(1, 2).contiguous().view(B, T_q, -1)
>         return self.W_o(context), attn
> ```
>
> 📌 **关键**：与 self-attention 唯一区别——**Q 来自 query，K/V 来自 memory**。attention 矩阵 shape 是 $(B,H,T_q,T_m)$，不是方阵。memory_mask 广播到 `[:, None, None, :]` 匹配 (B,H,T_q,T_m)。

---

### C16 · KV Cache `★★`

Implement a KV cache for autoregressive decoding. Each step only computes the new token's K and V, appends to cache, and attends over the full history.

> [!success]- Answer
>
> ```python
> class KVCache:
>     def __init__(self):
>         self.K = self.V = None
>
>     def update(self, new_k, new_v):    # (B, H, 1, d_k)
>         if self.K is None:
>             self.K, self.V = new_k, new_v
>         else:
>             self.K = torch.cat([self.K, new_k], dim=2)
>             self.V = torch.cat([self.V, new_v], dim=2)
>         return self.K, self.V
> ```
>
> 📌 **关键**：每步只算新 token 的 Q/K/V，K/V **append** 到 cache（dim=2 是序列维），attention 对**全长** cache 做。省去重复计算历史 token 的 K/V。代价：内存 $O(N \cdot L \cdot d)$。

---

## Week 10 — Deep Reinforcement Learning

### C17 · QNetwork + ReplayBuffer + DQN Loss `★★`

Implement: (1) a simple Q-network (MLP); (2) a replay buffer with `push` and `sample`; (3) the DQN loss using a target network.

> [!success]- Answer
>
> ```python
> class QNetwork(nn.Module):
>     def __init__(self, state_dim, n_actions, hidden=32):
>         super().__init__()
>         self.net = nn.Sequential(
>             nn.Linear(state_dim, hidden), nn.ReLU(),
>             nn.Linear(hidden, hidden), nn.ReLU(),
>             nn.Linear(hidden, n_actions),
>         )
>     def forward(self, x):
>         return self.net(x)
>
> class ReplayBuffer:
>     def __init__(self, capacity=10000):
>         self.buffer = deque(maxlen=capacity)
>     def push(self, s, a, r, s_next, done):
>         self.buffer.append((s, a, r, s_next, done))
>     def sample(self, batch_size):
>         batch = random.sample(self.buffer, batch_size)
>         s, a, r, sn, d = zip(*batch)
>         return (torch.as_tensor(np.array(s), dtype=torch.float32),
>                 torch.as_tensor(a, dtype=torch.long),
>                 torch.as_tensor(r, dtype=torch.float32),
>                 torch.as_tensor(np.array(sn), dtype=torch.float32),
>                 torch.as_tensor(d, dtype=torch.float32))
>
> def dqn_loss(q_net, target_net, batch, gamma=0.9):
>     s, a, r, s_next, done = batch
>     q_sa = q_net(s).gather(1, a[:, None]).squeeze(1)
>     with torch.no_grad():
>         target = r + gamma * target_net(s_next).max(1).values * (1 - done)
>     return F.mse_loss(q_sa, target)
> ```
>
> 📌 **关键**：`gather` 取当前动作的 Q 值。target 用 **target_net**（`torch.no_grad()`）。`(1-done)` 终止态不加未来奖励。ReplayBuffer 用 `deque(maxlen=...)` 自动淘汰旧经验。

---

### C18 · PPO Loss (Clip) `★`

Implement the PPO clipped surrogate objective.

> [!success]- Answer
>
> ```python
> def ppo_loss(log_probs_new, log_probs_old, advantages, clip_eps=0.2):
>     ratio = torch.exp(log_probs_new - log_probs_old)
>     unclipped = ratio * advantages
>     clipped   = torch.clamp(ratio, 1 - clip_eps, 1 + clip_eps) * advantages
>     return -torch.min(unclipped, clipped).mean()
> ```
>
> 📌 **关键**：$r_t = \pi_\text{new}/\pi_\text{old} = \exp(\log\pi_\text{new} - \log\pi_\text{old})$。取 `min(unclipped, clipped)` 保守更新——好动作不过度增大、坏动作不过度减小。最后取负号（梯度**上升**）。

---

## Week 11 — Self-Supervised Learning

### C19 · InfoNCE / NT-Xent Loss (SimCLR) `★★`

Given two batches of L2-normalized embeddings `z1, z2` of shape `(B, D)`, implement the NT-Xent contrastive loss with temperature `tau`.

> [!success]- Answer
>
> ```python
> def nt_xent_loss(z1, z2, temperature=0.5):
>     B = z1.shape[0]
>     z = torch.cat([z1, z2], dim=0)                          # (2B, D)
>     sim = (z @ z.T) / temperature                           # (2B, 2B)
>     mask = ~torch.eye(2 * B, dtype=torch.bool, device=z.device)
>     sim = sim.masked_select(mask).view(2 * B, 2 * B - 1)   # 去掉对角线
>     labels = torch.cat([torch.arange(B, 2*B), torch.arange(B)], device=z.device)
>     return F.cross_entropy(sim, labels)
> ```
>
> 📌 **关键**：正样本 = 同 index 的另一视角（i↔i+B）。去掉对角线（自身不作正/负样本）。labels 指定每行的正样本列索引。温度 $\tau$ 越小越聚焦 hard negatives。

---

### C20 · MAE Random Masking `★★`

Implement `random_masking(patches, mask_ratio)`: given `(B, N, D)` patch tokens, randomly mask `mask_ratio` fraction and return visible patches, binary mask, and restoration indices.

> [!success]- Answer
>
> ```python
> def random_masking(patches, mask_ratio):
>     B, N, D = patches.shape
>     n_keep = int(N * (1.0 - mask_ratio))
>     noise = torch.rand(B, N, device=patches.device)
>     ids_shuffle = noise.argsort(dim=1)
>     ids_restore = ids_shuffle.argsort(dim=1)
>     ids_keep = ids_shuffle[:, :n_keep]
>     x_visible = torch.gather(patches, 1, ids_keep.unsqueeze(-1).expand(-1, -1, D))
>     mask = torch.ones(B, N, device=patches.device)
>     mask[:, :n_keep] = 0
>     mask = torch.gather(mask, 1, ids_restore)
>     return x_visible, mask, ids_restore
> ```
>
> 📌 **关键**：用 `rand→argsort` 生成随机排列，取前 `n_keep` 个作为可见。`ids_restore` 用于 decoder 端把预测放回原位。loss 只在 **mask=1 的 patch** 上算（被遮住的才需要预测），分母是 `mask.sum()` 不是 `N`。MAE 掩码率约 **75%**（比 BERT 15% 高很多）。

---

## Week 12 — Deep Generative Models

### C21 · GAN Training Step `★★★`

Implement one GAN training step: update D (on real + fake), then update G. Use non-saturating loss (BCE with logits).

> [!success]- Answer
>
> ```python
> def gan_step(G, D, real_batch, g_opt, d_opt, latent_dim):
>     B = real_batch.size(0)
>     ones  = torch.ones(B, 1, device=real_batch.device)
>     zeros = torch.zeros(B, 1, device=real_batch.device)
>
>     # ── D step ──
>     z = torch.randn(B, latent_dim, device=real_batch.device)
>     fake = G(z).detach()                                # detach: 不传梯度给 G
>     d_loss = (F.binary_cross_entropy_with_logits(D(real_batch), ones)
>             + F.binary_cross_entropy_with_logits(D(fake), zeros))
>     d_opt.zero_grad(); d_loss.backward(); d_opt.step()
>
>     # ── G step ──
>     z = torch.randn(B, latent_dim, device=real_batch.device)
>     g_loss = F.binary_cross_entropy_with_logits(D(G(z)), ones)   # -log D(G(z))
>     g_opt.zero_grad(); g_loss.backward(); g_opt.step()
>
>     return d_loss.item(), g_loss.item()
> ```
>
> 📌 **关键**：训 D 时 `fake.detach()` 切断 G 的梯度。G 用 **non-saturating loss**：target=1（让 D 认为 fake 是真的），等价于 $-\log D(G(z))$，比 $\log(1-D)$ 梯度更强。先 D 后 G，各自独立 `zero_grad → backward → step`。

---

### C22 · DDPM (q_sample + Loss + Reverse Step) `★★★`

Implement three DDPM functions: (1) `q_sample` — sample $x_t$ from $x_0$ in one step; (2) `ddpm_loss` — the training objective; (3) `ddpm_reverse_step` — one denoising step at inference.

> [!success]- Answer
>
> ```python
> def q_sample(x0, t, noise, sqrt_ab, sqrt_1m_ab):
>     """x_t = sqrt(ᾱ_t) * x0 + sqrt(1-ᾱ_t) * ε"""
>     sa  = sqrt_ab[t].view(-1, *([1] * (x0.dim() - 1)))
>     s1a = sqrt_1m_ab[t].view(-1, *([1] * (x0.dim() - 1)))
>     return sa * x0 + s1a * noise, noise
>
> def ddpm_loss(eps_model, x0, sqrt_ab, sqrt_1m_ab, T):
>     t = torch.randint(0, T, (x0.shape[0],), device=x0.device)
>     noise = torch.randn_like(x0)
>     x_t, eps = q_sample(x0, t, noise, sqrt_ab, sqrt_1m_ab)
>     return F.mse_loss(eps_model(x_t, t.float()), eps)
>
> @torch.no_grad()
> def ddpm_reverse_step(eps_model, x_t, t, schedule):
>     betas = schedule["betas"]
>     alphas = schedule["alphas"]
>     alpha_bars = schedule["alpha_bars"]
>     B = x_t.size(0)
>     eps_pred = eps_model(x_t, torch.full((B,), t, device=x_t.device, dtype=torch.float))
>     beta_t, alpha_t, ab_t = betas[t], alphas[t], alpha_bars[t]
>     mu = (x_t - beta_t / (1 - ab_t).sqrt() * eps_pred) / alpha_t.sqrt()
>     if t > 0:
>         return mu + betas[t].sqrt() * torch.randn_like(x_t)
>     return mu
> ```
>
> 📌 **关键**：
> - **q_sample**：前向加噪一步到位，$x_t = \sqrt{\bar\alpha_t}x_0 + \sqrt{1-\bar\alpha_t}\epsilon$。`.view(-1, 1, 1, 1)` 广播到图像维度。
> - **ddpm_loss**：随机采 $t$，加噪得 $x_t$，网络预测噪声 $\epsilon_\theta$，与真实 $\epsilon$ 做 MSE。
> - **reverse_step**：去噪均值 $\mu = \frac{1}{\sqrt{\alpha_t}}(x_t - \frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta)$，$t>0$ 时加噪声（随机性），$t=0$ 直接返回均值。`@torch.no_grad()` 推理不需要梯度。

---

> **复习建议**：按星级分层——先默 `★★★`（C1–C4, C5–C6, C7–C8, C10–C13, C21–C22），再补 `★★`（C14–C20），最后 `★`（C18）。每块纸笔写完对照答案，重点看 📌 标注的易错点。
