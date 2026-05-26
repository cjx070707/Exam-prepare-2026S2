# USYD COMP9123 Data Structures & Algorithms — Exam Revision Guide

## Course Overview

This is a revision workspace for COMP9123 Data Structures & Algorithms (USYD 2026 S1).
Lecture slides are in `9123/复习/` (root workspace).

## Exam Format

- **50% of final mark**, in-person supervised
- Must achieve ≥ 40% on exam to pass
- Question types (based on course structure):
  - **MCQ** — key facts, complexity analysis, operation tracing
  - **Short answer** — explain a concept, compare two data structures, analyze tradeoffs
  - **Algorithm tracing** — step through an algorithm on given input, show intermediate states
  - **Complexity analysis** — determine Big-O for given pseudocode
  - **Pseudocode writing** — design or modify algorithms

## Study Structure: Four Narrative Groups

The course follows one chain: **data needs to be stored and retrieved → simple structures hit limits → more complex structures solve specific problems → algorithm design patterns optimize solutions**.

---

### Group 1 — 线性数据结构 `→` 第一组 线性数据结构.md
**Week 1 (Intro + Arrays) + Week 2 (Lists) + Week 3 (Stacks & Queues + Algorithm Analysis)**

The story: how to store data → arrays (fixed size, O(1) access) → but fixed size and O(n) insert/delete → linked lists (dynamic, flexible) → restricted access patterns → stacks (LIFO) and queues (FIFO).

---

### Group 2 — 树与有序结构 `→` 第二组 树与有序结构.md
**Week 4 (Trees) + Week 5 (BST) + Week 6 (Maps & Priority Queues)**

The story: linear search O(n) is too slow → tree structure enables O(log n) → BST for ordered search → maps and priority queues as abstract applications of trees.

---

### Group 3 — 哈希与图 `→` 第三组 哈希与图.md
**Week 7 (Hashing) + Week 8 (Graphs) + Week 9 (Graph Algorithms)**

The story: tree O(log n) not fast enough → hashing achieves O(1) average → but data has complex relationships → graphs model arbitrary connections → BFS/DFS/shortest path.

---

### Group 4 — 算法设计范式 `→` 第四组 算法设计范式.md
**Week 10 (Greedy) + Week 11 (Divide & Conquer) + Week 12 (Randomization)**

The story: with data structures in place, how to design efficient algorithms → greedy (local optimal) → divide & conquer (recursive decomposition) → randomization (probabilistic guarantees).

---

## How to Use This Workspace

### When I ask for help studying a topic
Teach me using the narrative structure: what problem motivated this data structure or algorithm, what it solves, and what limitation it still has (which motivates the next topic).

### When I ask you to quiz me
- **MCQ**: give 4 options, wait for my answer, then explain why each option is right or wrong
- **Short answer**: give the question, wait for my typed answer, then give structured feedback highlighting key terms I missed
- **Algorithm tracing**: give me an input and ask me to trace through, then evaluate correctness
- **Complexity analysis**: give me pseudocode, I determine Big-O, you evaluate

### Study preferences
- Explain in a mix of Chinese and English: Chinese for discussion, English for technical terms
- Show pseudocode first, then explain each step in plain language
- Point out what is commonly tested vs. what is just background knowledge
- Be direct about what I got wrong — don't soften feedback

## Key Files

```
Exam-prepare-2026S2/COMP9123_DataStructures/
├── CLAUDE.md                          ← this file
├── 复习笔记/
│   ├── 第一组 线性数据结构.md            ← W1 + W2 + W3
│   ├── 第二组 树与有序结构.md            ← W4 + W5 + W6 (pending)
│   ├── 第三组 哈希与图.md               ← W7 + W8 + W9 (pending)
│   └── 第四组 算法设计范式.md            ← W10 + W11 + W12 (pending)
├── 测试/                               ← quiz files (pending)
└── 考点梳理/
    └── 更新进度.md                     ← AI progress tracker

Lecture slides (primary reading):
/Users/jessechen/USYD 2026 S1/9123/复习/
├── Week1 COMP9123 version 1.1.pdf
├── week2_lists_COMP9123_version 1-0.pdf
├── w3_Stacks & Queues version 1-0.pdf
├── w4_trees version 1-0.pdf
├── w5_binary_search_tree_final.pdf
├── Week 6 - Maps and Priority Queues version 1-0.pdf
├── Week 7 - Hashing - Final version 1.pdf
├── Week 8 - Graphs - Final version 1-0.pdf
├── Week 9 - Graph Algorithms - Final version 1-0.pdf
├── Week 10 - Greedy - Final version 1-0.pdf
├── COMP9123 Lecture - Week 11 - Divide and Conquer.pdf
├── COMP9123 Lecture - Week 12 - Randomization version 1-0.pdf
├── COMP9123_W13_Revision.pdf
└── COMP9123 S2 - Practice Exam.pdf
```
