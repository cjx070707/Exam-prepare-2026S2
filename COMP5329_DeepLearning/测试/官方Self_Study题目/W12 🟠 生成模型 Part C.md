# W12 — Part C Exam-Style Questions
**来源：Week12_Deep_Generative_Models.ipynb（官方 tutorial，未改动）**

> [!warning] 备考优先级：高概率

---

---
# Part C · Exam-Style Questions

Three questions, each with three sub-parts. Try to answer before expanding the model solution.

## Q1 · Why the non-saturating GAN loss?  *(7 marks)*

The original GAN paper's generator minimises $\log(1-D(G(z)))$ but the implementation we wrote in Task B2 maximises $\log D(G(z))$ (equivalently, BCE with target = 1 on fakes).

**(a)** *(3 marks)* Consider the **saturating** loss $\mathcal{L}_G^{\text{sat}}(\theta)=\mathbb{E}_z[\log(1-D(G(z)))]$. Compute $\partial \mathcal{L}_G^{\text{sat}}/\partial D(G(z))$ and show that it tends to **0** as $D(G(z))\to 0$. Explain in one sentence why this is exactly the regime *early* training is in.

**(b)** *(2 marks)* Now consider the **non-saturating** loss $\mathcal{L}_G^{\text{NS}}(\theta)=-\mathbb{E}_z[\log D(G(z))]$. Compute $\partial\mathcal{L}_G^{\text{NS}}/\partial D(G(z))$ and describe its behaviour as $D(G(z))\to 0$. Contrast with part (a).

**(c)** *(2 marks)* The two losses share the **same fixed point** $D(G(z))=\tfrac12$ (at which $G$ stops moving). Given that, why do we still bother to switch? Answer in terms of what the gradient contributes when $D$ is *confidently wrong* about the generator's current output.

<details><summary><b>▸ Answer sketch — Q1</b></summary>

**(a)** With $u:=D(G(z))$ we have $\mathcal{L}_G^{\text{sat}}=\log(1-u)$, so
$$\frac{\partial \mathcal{L}_G^{\text{sat}}}{\partial u}=\frac{-1}{1-u}.$$
As $u\to 0$ this derivative tends to $-1$ in magnitude, but what matters is the **upstream** gradient that reaches $\theta$: by chain rule
$$\frac{\partial \mathcal{L}_G^{\text{sat}}}{\partial \theta}=\frac{\partial \mathcal{L}_G^{\text{sat}}}{\partial u}\,\frac{\partial u}{\partial \theta}=\frac{-1}{1-u}\,\sigma(z_{\text{logit}})(1-\sigma(z_{\text{logit}}))\frac{\partial z_{\text{logit}}}{\partial\theta}=\frac{-u(1-u)}{1-u}\,\frac{\partial z_{\text{logit}}}{\partial\theta}=-u\,\frac{\partial z_{\text{logit}}}{\partial\theta}.$$
As $u=D(G(z))\to 0$ the factor $u$ kills the gradient. **Early in training the generator is bad, $D$ confidently classifies fakes as fake ($u\approx 0$), and the generator receives essentially no gradient** — it cannot climb out of the hole.

**(b)** Now $\mathcal{L}_G^{\text{NS}}=-\log u$, so $\partial/\partial u=-1/u$ and the chain rule gives
$$\frac{\partial \mathcal{L}_G^{\text{NS}}}{\partial\theta}=-\frac{1}{u}\,u(1-u)\,\frac{\partial z_{\text{logit}}}{\partial\theta}=-(1-u)\,\frac{\partial z_{\text{logit}}}{\partial\theta}.$$
As $u\to 0$ the coefficient tends to $-1$: the generator still gets **strong** signal. As $u\to 1$ (generator is winning) the coefficient shrinks toward 0 — exactly the regime where we no longer need to push.

**(c)** Both losses are stationary when $u=\tfrac12$ (strictly, both have the same global optimum for $G$ against the optimal $D^\star$), but **the saturating loss has near-zero gradient whenever $D$ is confidently right and $G$ is losing**, which is *precisely* the early-training regime. The non-saturating loss delivers a gradient of order $1$ in that regime and only fades when training has already succeeded. This is a pure optimisation fix — same game, same fixed points, very different gradient fields — and it is why every modern GAN codebase uses it.
</details>

## Q2 · $\varepsilon$-prediction is score matching  *(7 marks)*

DDPM trains a network $\varepsilon_\theta(x_t,t)$ with
$$\mathcal{L}(\theta)=\mathbb{E}_{x_0,\varepsilon,t}\!\left[\,\lVert\varepsilon_\theta(x_t,t)-\varepsilon\rVert^2\right],\qquad x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon.$$

**(a)** *(3 marks)* Using $q(x_t\mid x_0)=\mathcal{N}(\sqrt{\bar\alpha_t}\,x_0,(1-\bar\alpha_t)I)$, show that
$$\nabla_{x_t}\log q(x_t\mid x_0)\;=\;-\frac{x_t-\sqrt{\bar\alpha_t}\,x_0}{1-\bar\alpha_t}\;=\;-\frac{\varepsilon}{\sqrt{1-\bar\alpha_t}}.$$
Hence give the formula that converts a trained noise predictor into an estimate of the *marginal* score $s_\theta(x_t,t)\approx\nabla_{x_t}\log p_t(x_t)$.

**(b)** *(2 marks)* DDPM could equivalently be parameterised to predict $x_0$ directly, or the posterior mean $\mu_\theta$. Why is **$\varepsilon$-prediction** preferred in practice? Answer in terms of the *scale* of the target across timesteps and what that implies for the loss landscape near $t\to 0$ and $t\to T$.

**(c)** *(2 marks)* On high-resolution images, DDPM typically uses $T\approx 1000$ reverse steps. Explain **why 1000** — i.e. what goes wrong if you train with $T=1000$ but then run the reverse chain with only, say, 10 steps of the *DDPM* updater (not a fancy DDIM sampler)? Phrase your answer in terms of the local-Markov assumption used to derive the DDPM update formula in Task B5.

<details><summary><b>▸ Answer sketch — Q2</b></summary>

**(a)** For $q(x_t\mid x_0)=\mathcal{N}(\mu,\sigma^2 I)$ with $\mu=\sqrt{\bar\alpha_t}\,x_0$ and $\sigma^2=1-\bar\alpha_t$,
$$\log q(x_t\mid x_0)=-\frac{\lVert x_t-\mu\rVert^2}{2\sigma^2}+\text{const}\;\Longrightarrow\;\nabla_{x_t}\log q=-\frac{x_t-\sqrt{\bar\alpha_t}x_0}{1-\bar\alpha_t}.$$
Substitute the forward equation $x_t-\sqrt{\bar\alpha_t}x_0=\sqrt{1-\bar\alpha_t}\,\varepsilon$:
$$\nabla_{x_t}\log q(x_t\mid x_0)=-\frac{\sqrt{1-\bar\alpha_t}\,\varepsilon}{1-\bar\alpha_t}=-\frac{\varepsilon}{\sqrt{1-\bar\alpha_t}}.\;\blacksquare$$
Denoising score matching trains $s_\theta$ to match the **conditional** score in expectation; an elementary identity shows this also matches the **marginal** score $\nabla_{x_t}\log p_t(x_t)$. Therefore
$$\boxed{\;s_\theta(x_t,t)=-\,\frac{\varepsilon_\theta(x_t,t)}{\sqrt{1-\bar\alpha_t}}.\;}$$
This is the bridge that lets us plug a DDPM-trained network straight into a score-SDE or probability-flow ODE sampler.

**(b)** The target $\varepsilon\sim\mathcal{N}(0,I)$ has **timestep-independent unit variance**, so the MSE loss has a **uniform scale** over every $t$ and can be trained with a single global learning rate. Predicting $x_0$ directly means the target is at data scale; the residual is multiplied by $\sqrt{\bar\alpha_t}$ which shrinks to $0$ near $t=T$, so the network receives almost no gradient there — it is being asked to recover a clean sample from pure noise. Predicting $\mu_\theta$ has the same problem because $\mu$ scales with $\sqrt{\alpha_t}$. $\varepsilon$-prediction is the unique parameterisation whose target has the same scale at every $t$; this is why Ho et al. (2020) adopted it and why essentially every diffusion model since has followed suit.

**(c)** The DDPM reverse step we derived in Task B5 is a **local-Markov** approximation to the true reverse kernel: it assumes the gap $t\to t-1$ is *small* so that $q(x_{t-1}\mid x_t,x_0)$ is well-approximated by a Gaussian whose mean is linear in $\varepsilon_\theta$. With $T=1000$ each step really is small ($\beta_t\lesssim 0.02$) and the approximation is accurate. If we try to run the *same* updater with only 10 steps on a $T=1000$ schedule, each step now has to jump by 100 indices — the local Gaussian assumption collapses, the posterior at such large gaps is highly non-Gaussian and multi-modal, and the iterates diverge into garbage. This is **exactly** the setting DDIM was designed for: it re-derives a non-Markovian, deterministic update that is **valid for any sub-sequence** of timesteps and therefore lets the same trained $\varepsilon_\theta$ be sampled in, say, 10 or 50 steps without retraining. So the answer to "why 1000" is: 1000 is what the *derivation* of the DDPM step needs in order for its local-Gaussian approximation to be accurate; fewer-step sampling needs a *different* sampler (DDIM, DPM-Solver, consistency distillation, ...), not a shorter run of the same one.
</details>

## Q3 · GANs vs DDPMs — the likelihood-free trade-off  *(8 marks)*

**(a)** *(3 marks)* Neither GANs nor DDPMs evaluate $p_\theta(x)$ directly. Explain, for **each** model, **what** object is learned in place of the likelihood and **how** that object is used to (i) train and (ii) sample. Your answer should make clear that a GAN learns a **sampler** and a **critic**, while a DDPM learns a **noise predictor** that is (up to a constant) an estimate of $\nabla_{x_t}\log p_t(x_t)$.

**(b)** *(3 marks)* Describe the **sampling-cost vs coverage** trade-off. Which model samples in one forward pass, and which needs hundreds of forward passes? Which is prone to **mode collapse**, and **why** does the other one mostly avoid it? Tie the "why" back to the training objective: what is it about the $\varepsilon$-prediction MSE that forces $\varepsilon_\theta$ to be informative at **every** noise level, including the ones near clean data where small errors matter most?

**(c)** *(2 marks)* Given that a DDPM learns $\varepsilon_\theta(x_t,t)$, **why can't we just take $-\varepsilon_\theta$ as a one-shot sampler** — i.e. draw $x_T\sim\mathcal{N}(0,I)$ and return $x_T-\varepsilon_\theta(x_T,T)$ as the sample? Say in one or two sentences what this shortcut is estimating, and why it is fundamentally different from what the iterative reverse chain computes.

<details><summary><b>▸ Answer sketch — Q3</b></summary>

**(a)** **GAN.** Learns two objects: a sampler $G_\theta(z)$ and a critic $D_\phi(x)$. Neither is a density. Training is the adversarial minimax game: $D$ is trained with binary cross-entropy to tell real from fake, and $G$ is trained (via the non-saturating loss) to push its fake outputs toward $D(G(z))=1$. Sampling is trivial — one forward pass $z\to G(z)$ — and the critic $D$ is thrown away at inference time. **DDPM.** Learns a single object: a noise predictor $\varepsilon_\theta(x_t,t)$. By Q2(a) this is equivalent (up to $-1/\sqrt{1-\bar\alpha_t}$) to an estimate of the **score** $\nabla_{x_t}\log p_t(x_t)$ at a whole family of noise levels. Training is the MSE objective $\mathbb E\lVert\varepsilon-\varepsilon_\theta(x_t,t)\rVert^2$, which is denoising score matching. Sampling is iterative: start at $x_T\sim\mathcal{N}(0,I)$, apply the reverse step from Task B5 for $t=T,T-1,\dots,1$. So both models give up on the likelihood but replace it with different auxiliary objects: an **implicit** sampler–critic pair in the GAN case, and an **explicit** score field in the DDPM case.

**(b)** **Cost.** GAN: one forward pass; DDPM: one forward pass **per reverse step**, so $\sim T$ passes ($T\!\approx\!1000$ on images). GANs win sampling cost by 2–3 orders of magnitude. **Coverage.** GANs are famously prone to mode collapse because the generator's loss is fully satisfied by producing *any* output the discriminator accepts as real — nothing in $\mathcal{L}_G^{\text{NS}}$ rewards $G$ for covering all of $p_{\text{data}}$. DDPMs mostly avoid mode collapse: the loss $\mathbb E_{x_0}\lVert\varepsilon-\varepsilon_\theta(x_t,t)\rVert^2$ is taken over **every** training sample $x_0$ and **every** timestep $t$. To drive the loss down the network has to predict the correct noise for $x_t$ values that came from *every* mode at *every* noise level — averaging over training data directly forces coverage. In particular, the tight-scale $\varepsilon$ target near $t\approx 0$ means the model cannot ignore any mode without paying a large loss on samples from that mode.

**(c)** $-\varepsilon_\theta(x_T,T)$ is an estimate of the **score** of $p_T$, which is already $\approx\mathcal{N}(0,I)$ — so the shortcut $x_T-\varepsilon_\theta(x_T,T)$ is essentially a single Langevin half-step against an isotropic Gaussian prior and brings you nowhere near $p_{\text{data}}$. The iterative reverse chain is valuable precisely because it integrates the score $\nabla_{x_t}\log p_t$ along the **whole** path $t:T\to 0$, interleaving many small denoising corrections with stochastic kicks; the one-shot shortcut throws away all the intermediate score estimates $\varepsilon_\theta(x_t,t)$ for $t<T$ — which is where the mass of the learned distribution actually lives. Collapsing 1000 steps to 1 in a principled way is exactly the motivation for consistency models and distillation — it is *not* free.
</details>
