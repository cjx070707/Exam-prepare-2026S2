# W10 — Part C Exam-Style Questions
**来源：Week10_Deep_Reinforcement_Learning.ipynb（官方 tutorial，未改动）**

> [!info] 备考优先级：轻量

---

---
# Part C · Exam-Style Questions

> Three short-answer questions at medium-high difficulty. Each has a hidden **Model Answer** cell directly below with the key points the tutor will draw out during discussion.

## Q1 · Why DQN needs a target network

Suppose you implement DQN exactly as in Tasks B1–B3, but you **remove the target network** — that is, the TD target uses the *same* `q_net` that is being optimised:
$$y_i \;=\; r_i \;+\; \gamma \, \max_{a'} Q_\theta(s'_i, a') \, (1 - \text{done}_i).$$

**(a)** Describe the **forward-pass symptom** you would observe on a training run: what happens to the TD loss curve over the first few thousand steps, and why?

**(b)** Describe the **gradient symptom**: what does the gradient $\nabla_\theta \mathcal{L}$ pick up that it would *not* pick up with a frozen target, and why does this break the contraction argument that guarantees convergence to $Q^*$?

**(c)** Someone suggests that a single `.detach()` on `Q_\theta(s', a')` is enough — no need for a separate target network, no need to sync weights every $C$ steps. In one or two sentences, explain why this is only a partial fix and what is still unstable.

<details>
<summary><b>▸ Model Answer · Q1</b></summary>

**(a) Forward-pass symptom.** The TD loss curve typically **drops rapidly** for the first few hundred steps and then **oscillates wildly** or **diverges outright**. The reason: every gradient step moves $Q_\theta(s, a)$ *towards* the target $y = r + \gamma \max_{a'} Q_\theta(s', a')$, but it *also* moves the target itself, because the target is computed with the same network. You are chasing a point that moves in response to your own step — a classic **moving-target** problem. In practice the Bellman residual does not settle; you see large fluctuations and, on harder environments, NaN explosions.

**(b) Gradient symptom.** With a frozen target, the gradient is
$$\nabla_\theta \mathcal{L} \;=\; -\bigl(y - Q_\theta(s, a)\bigr)\, \nabla_\theta Q_\theta(s, a),$$
the **semi-gradient** — only the prediction depends on $\theta$. Removing the target makes $y$ itself a function of $\theta$, so the full gradient gains an extra term
$$-\bigl(y - Q_\theta(s, a)\bigr)\,\gamma\, \nabla_\theta \bigl[\max_{a'} Q_\theta(s', a')\bigr]$$
that pulls the target *toward* the prediction on every step. The Bellman operator is a $\gamma$-contraction *only when the target is held fixed*; once we let both endpoints move, the iteration is no longer guaranteed to be a contraction, and Q-learning's convergence theorem does not apply. Empirically the result is oscillation or divergence.

**(c) Is `.detach()` enough?** `.detach()` stops the gradient from flowing into $\theta$ through the target, which fixes the *gradient* symptom. But the *values* returned by the detached expression still come from the **current** $\theta$, so the target moves every single step — only the semi-gradient property is restored, not the stationary-target property. A separate `target_net` synced every $C$ steps gives a **stationary target for $C$ steps**, which is what the contraction argument actually needs in the function-approximation setting. `.detach()` = half the fix; the target network is the other half.

**Key points the tutor will land:**
- Moving-target $\Rightarrow$ broken contraction $\Rightarrow$ loss diverges.
- Semi-gradient vs. full gradient — name the distinction.
- `.detach()` fixes the gradient but not the stationarity; you need *both*.
</details>

## Q2 · Reading the PPO clipping landscape

Consider the PPO clipped surrogate with $\varepsilon = 0.2$, evaluated for a single transition with advantage $\hat A_t$ and importance ratio $r_t = r$.

**(a)** For a **positive** advantage $\hat A_t = +1$, write $\mathcal{L}^{\text{CLIP}}$ as an explicit piecewise function of $r$, and state the value of $\partial \mathcal{L}^{\text{CLIP}} / \partial r$ in each piece. Sketch the curve in words (three regions).

**(b)** Repeat for $\hat A_t = -1$. In which region is the gradient **zero**, and what is the practical interpretation of that region?

**(c)** A student proposes to *drop the outer `min`* and just use the clipped term $\text{clip}(r, 0.8, 1.2) \cdot \hat A_t$ as the loss. Give one concrete failure case — a scenario where this modified loss produces a **wrong-direction** or **runaway** update that the original PPO objective correctly suppresses.

<details>
<summary><b>▸ Model Answer · Q2</b></summary>

**(a) Positive advantage, $\hat A_t = +1$.** Here $\text{clip}(r, 0.8, 1.2) \cdot 1 = \text{clip}(r, 0.8, 1.2)$ and the `min` picks the smaller of $r$ and the clipped value. For $r < 1$ the clipped term is at least $0.8 > r$ is *not* always true — let's just do each region cleanly:

$$\mathcal{L}^{\text{CLIP}}(r) \;=\; \begin{cases} r, & 0 \le r \le 1.2, \\[2pt] 1.2, & r > 1.2. \end{cases}$$

(Note: for $r < 0.8$, $\min(r, 0.8) = r$; for $0.8 \le r \le 1.2$, $\min(r, r) = r$; for $r > 1.2$, $\min(r, 1.2) = 1.2$.)

So
$$\frac{\partial \mathcal{L}^{\text{CLIP}}}{\partial r} \;=\; \begin{cases} 1, & r < 1.2, \\[2pt] 0, & r > 1.2. \end{cases}$$

**Three regions in words.** (i) Well below the trust region ($r < 0.8$): the objective is still $r$, gradient $+1$, the update still pushes the probability *up* — PPO does not "repel" you back into the trust region, it just doesn't penalise you for being below. (ii) Inside the trust region ($0.8 \le r \le 1.2$): linear with slope $+1$, normal policy-gradient behaviour. (iii) Above the trust region ($r > 1.2$): **flat**, gradient $0$, no further reward for increasing the probability — the update *halts* on this sample.

**(b) Negative advantage, $\hat A_t = -1$.** Symmetrically,
$$\mathcal{L}^{\text{CLIP}}(r) \;=\; \begin{cases} -0.8, & r < 0.8, \\[2pt] -r, & 0.8 \le r \le 2.5. \end{cases}$$

The **gradient is zero for $r < 0.8$**. Practical interpretation: once we have already reduced the probability of a bad action to 80 % of its old value, PPO **stops pushing it further down on this sample**. Without the flat region, a single large negative advantage could drive a probability to zero in one epoch — exactly the destructively-large update the clip is designed to prevent.

**(c) Dropping the outer `min`.** Consider $\hat A_t = +1$ and $r = 5$ (the new policy has, for whatever reason, put 5× as much probability on this action as the old one). With the original objective, $\mathcal{L}^{\text{CLIP}} = \min(5, 1.2) = 1.2$ — gradient zero, *no further update*. With the modified "clip-only" loss, the value is $\text{clip}(5, 0.8, 1.2) = 1.2$ — also flat, in this case. So for $\hat A > 0$ the clip-only variant happens to coincide above the trust region.

The failure case is on the **other side**: $\hat A_t = -1$ and $r = 5$ (a formerly rare-but-bad action has become dominant — exactly the case we most urgently need to correct). Original PPO gives $\min(5 \cdot -1,\; 1.2 \cdot -1) = \min(-5, -1.2) = -5$ — a *large negative objective*, and maximising means pushing $r$ **down** strongly. The clip-only version gives $1.2 \cdot -1 = -1.2$ with zero gradient — **no corrective force at all**, even though the action is bad and its probability has ballooned. The `min` is what ensures PPO stays **pessimistic** on the "wrong" side of the trust region; without it, catastrophic probability inflations go uncorrected.

**Key points the tutor will land:**
- The clip gives the *shape*; the `min` gives the *direction*.
- PPO is **not** a symmetric trust region — it is pessimistic outside the box.
- Zero-gradient regions are a feature, not a bug: they bound the per-sample update.
</details>

## Q3 · On-policy vs. off-policy: why replay buffers do not transplant

DQN stores transitions in a replay buffer and reuses them for many gradient updates. PPO collects trajectories under $\pi_{\theta_\text{old}}$, performs a few epochs of updates, and then **throws the data away** and collects new trajectories.

**(a)** Explain, in terms of the Bellman equation, why DQN is an **off-policy** algorithm and is therefore free to reuse old transitions — even transitions collected by a very different policy.

**(b)** Explain why PPO is an **on-policy** algorithm and why re-using data from a stale policy *would* bias its gradient. In which quantity of the PPO objective does the staleness show up, and what does the clipping mechanism do to bound (but not eliminate) the bias?

**(c)** A student suggests: "Why not just apply DQN-style clipping to the PPO loss — clip the TD error to $\pm\varepsilon$ and put PPO's old transitions in a replay buffer for free sample efficiency?" Explain the conceptual error. (Hint: what does the `min`/`clip` in PPO *bound* that has no analogue in the DQN loss, and what would clipping the TD error in DQN actually accomplish?)

<details>
<summary><b>▸ Model Answer · Q3</b></summary>

**(a) Why DQN is off-policy.** The Bellman optimality equation
$$Q^*(s, a) = \mathbb{E}_{s' \sim P}\!\bigl[r + \gamma \max_{a'} Q^*(s', a')\bigr]$$
is a statement about the **environment dynamics** $P$ and the **greedy** operator $\max_{a'}$ — the behaviour policy that *generated* the transition $(s, a, r, s')$ does not appear anywhere on the right-hand side. As long as the transition tuple is a valid draw from $P$ (which it always is, because it actually happened in the environment), it is a valid Monte-Carlo sample of the Bellman target regardless of which policy chose $a$. This is exactly why DQN can reuse millions of old transitions from a replay buffer, and also why $\varepsilon$-greedy exploration is allowed — the behaviour policy and the target policy (greedy) are formally different, but Q-learning's update is agnostic.

**(b) Why PPO is on-policy.** PPO's gradient estimator is built from the identity
$$\nabla_\theta J(\theta) \;=\; \mathbb{E}_{a \sim \pi_{\theta_\text{old}}}\!\Bigl[\frac{\pi_\theta(a \mid s)}{\pi_{\theta_\text{old}}(a \mid s)} \, \nabla_\theta \log \pi_\theta(a \mid s) \cdot \hat A_t\Bigr],$$
which is an **importance-sampling** estimator centred on $\pi_{\theta_\text{old}}$. It is only unbiased when the expectation is taken over samples drawn from **the same distribution** the importance weight was computed against. As $\theta$ drifts from $\theta_\text{old}$, the ratio $r_t(\theta)$ deviates from 1, the true expectation is no longer what the batch approximates, and the estimator becomes **biased**. The staleness shows up in the importance ratio. The clip $\text{clip}(r_t, 1-\varepsilon, 1+\varepsilon)$ prevents the ratio from growing unboundedly — it **bounds** the bias-amplification per sample — but it does **not** restore unbiasedness. This is why PPO re-collects fresh trajectories every few epochs: it trusts the importance weight only inside the clip box.

**(c) The conceptual error.** The `min`/`clip` in PPO is not a "TD-error clipper" — it is a **trust-region bound on the policy change**. It clips the *importance ratio* $\pi_\theta / \pi_{\theta_\text{old}}$, a quantity that has no analogue in DQN, because DQN has no $\pi_\theta$ to ratio against a $\pi_{\theta_\text{old}}$ in the first place (DQN is implicitly policy-free — it learns $Q$ and acts greedily). Clipping the TD error in DQN would be a completely different operation: it would just be a form of **Huber loss / gradient clipping** on the Bellman residual, bounding the magnitude of the regression target per sample. That is a mild variance-reduction trick and is in fact sometimes done in practice (Rainbow DQN uses Huber loss) — but it does **not** make PPO's ratio-clipping and DQN's error-clipping the same operation, and it does **not** justify dumping old-policy trajectories into a PPO replay buffer. DQN can reuse old data because the Bellman target is policy-agnostic; PPO cannot because the policy gradient is not. No amount of loss-side clipping changes that.

**Key points the tutor will land:**
- The Bellman target has no $\pi_\theta$ in it — that is what "off-policy" *means*.
- The policy gradient has $\pi_\theta$ front and centre, and PPO is an importance-sampled version of it.
- Clipping in the two algorithms bounds **different things**: ratio (policy change) vs. TD residual (regression magnitude).
- Replay buffer + PPO = biased gradient; you would need a different correction (e.g. V-trace, Retrace) to make it work.
</details>
