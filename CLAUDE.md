# USYD COMP5329 Deep Learning — Exam Revision Guide

## Course Overview

This is a revision workspace for COMP5329 Deep Learning (USYD 2026 S1).
Course materials are in `Materials2026/` (cloned from GitHub).

## Exam Format

- **Single choice questions** — key facts, historical milestones, conceptual distinctions
- **Short-answer questions** — explain a concept in 2–5 sentences with correct terminology
- **Handwritten coding questions** — reproduce key algorithms from scratch (no autograd)
- **Essay questions** — structured comparative analysis (why A > B under condition C)

## Study Structure: Four Narrative Groups

The course is organised as a chain of problems and solutions.
Each group is documented in its own file.

---

### Group 1 — Foundations `→` [Group1_Foundations.md](Group1_Foundations.md)
**Week 2 (Neural Networks) + Week 3 (Regularization)**

The story: linear models fail → add hidden layers + non-linearity → learn via backprop →
model overfits → regularization fixes this.

---

### Group 2 — Structured Data `→` [Group2_Structured_Data.md](Group2_Structured_Data.md)
**Week 4 (CNN) + Week 5 (GNN)**

The story: MLP ignores spatial structure in images → CNN exploits locality and translation
equivariance → but CNN requires grid data → GNN extends convolution to arbitrary graphs.

---

### Group 3 — Sequential Data *(coming soon)*
**Week 7 (RNN/LSTM/GRU) + Week 8 (Transformer, BERT, GPT, ViT, SSM)**

The story: static models can't handle sequences → RNN adds memory → but gradients vanish
over long sequences → Transformer replaces recurrence with global attention → SSM offers a
cheaper alternative.

---

### Group 4 — Beyond Supervised Learning *(coming soon)*
**Week 9 (Multi-modal) + Week 10 (RL) + Week 11 (Self-supervised) + Week 12 (Generative)**

The story: supervised learning requires labels → four escape routes:
multi-modal pretraining, environment rewards (RL), data as its own signal (SSL),
and learning to generate (GANs, VAEs, Diffusion).

---

## How to Use This Workspace

### When I ask for help studying a topic
Teach me using the narrative structure: what problem motivated this idea, what the solution is,
and what limitation it still leaves (which motivates the next topic).

### When I ask you to quiz me
- **MCQ**: give 4 options, wait for my answer, then explain why each option is right or wrong
- **Short answer**: give the question, wait for my typed answer, then give structured feedback
  highlighting key terms I missed
- **Handwritten coding**: give me a prompt, I type my answer, you evaluate correctness and
  point out any missing steps or shape errors
- **Essay**: give me a question, I write a paragraph, you score it on: structure / technical
  accuracy / use of examples

### Study preferences
- Explain in a mix of Chinese and English: Chinese for discussion, English for technical terms
- Show formulas first, then explain each symbol in plain language
- Point out what is commonly tested vs. what is just background knowledge
- Be direct about what I got wrong — don't soften feedback

## Key Files

```
claude 复习/
├── CLAUDE.md                    ← this file (framework + instructions)
├── Group1_Foundations.md        ← Week 2 + 3 study notes
├── Materials2026/
│   ├── Lecture/                 ← PDF slides + Notes PDFs (primary reading)
│   └── Tutorial/                ← Jupyter notebooks (Part B: coding, Part C: exam Qs)
```
