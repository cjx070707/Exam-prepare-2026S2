# USYD COMP5339 Data Engineering — Exam Revision Guide

## Course Overview

This is a revision workspace for COMP5339 Data Engineering (USYD 2026 S1).
Course slides are in `课件/`.

## Exam Format

- **Short-answer questions** — explain a concept, compare two systems, or describe a tradeoff in 2–5 sentences
- **MCQ** — key facts, system comparisons, scenario-based tool selection
- **Code reading** — given a snippet (Python/SQL/HTML), explain what it does or identify a problem; no hand-writing code from scratch

## Study Structure: Four Narrative Groups

The course follows one engineering chain: **data grows more complex and larger → existing tools break down → pick a better-suited tool**.

Each group documents one stage of that chain.

---

### Group 1 — 获取与清洗 `→` [Group1_Ingestion.md](Group1_Ingestion.md)
**Week 1 (Intro + Unix) + Week 2 (Acquisition & Cleaning) + Week 4 (Web Scraping & APIs)**

The story: data lives in many places (files, databases, web, APIs) → pull it in →
it arrives dirty (missing, incorrect, inconsistent) → clean it before downstream use.

---

### Group 2 — 存储系统 `→` [Group2_Storage.md](Group2_Storage.md)
**Week 3 (Databases, Warehouses, Lakes) + Week 5 (NoSQL & Semi-structured)**

The story: structured data fits relational DBs (OLTP) → analytics needs a different shape (OLAP, star schema) →
not all data is structured → NoSQL handles semi-structured (JSON/XML, MongoDB, Graph DBs) →
massive raw data needs a data lake.

---

### Group 3 — 特殊数据类型 `→` [Group3_SpecialData.md](Group3_SpecialData.md)
**Week 6 (Spatial) + Week 7 (Temporal) + Week 8 (Unstructured)**

The story: general-purpose storage and queries aren't enough for spatial, time-series, or
unstructured data → each type has its own indexing, query patterns, and tooling.

---

### Group 4 — 规模化与运维 `→` [Group4_ScaleAndOps.md](Group4_ScaleAndOps.md)
**Week 9 (Stream Processing) + Week 10 (Scalable Engineering) + Week 11 (DataOps & ML)**

The story: single-machine batch processing can't keep up with volume or latency requirements →
distributed systems (Hadoop/Spark/Flink) scale out → data arrives continuously → stream
processing handles real-time → pipelines in production need monitoring, orchestration, and
governance (DataOps) → ML adds a serving layer on top.

---

## How to Use This Workspace

### When I ask for help studying a topic
Teach me using the narrative structure: what engineering problem motivated this tool or concept,
what it solves, and what limitation it still has (which motivates the next topic).

### When I ask you to quiz me
- **MCQ**: give a scenario or concept question with 4 options, wait for my answer, then explain
  why each option is right or wrong
- **Short answer**: give the question, wait for my typed answer, then give structured feedback
  highlighting key terms or comparisons I missed
- **Code reading**: show me a Python/SQL/HTML snippet, ask what it does or what's wrong,
  evaluate my answer

### Study preferences
- Explain in a mix of Chinese and English: Chinese for discussion, English for technical terms
- For system comparisons, always lead with the tradeoff, not just the definition
- Point out what is commonly tested vs. what is just background knowledge
- Be direct about what I got wrong — don't soften feedback

## Key Files

```
5339/
├── CLAUDE.md                  ← this file (framework + instructions)
├── Group1_Ingestion.md        ← W1 + W2 + W4 study notes
├── Group2_Storage.md          ← W3 + W5 study notes
├── Group3_SpecialData.md      ← W6 + W7 + W8 study notes
├── Group4_ScaleAndOps.md      ← W9 + W10 + W11 study notes
└── 课件/                      ← PDF slides (primary reading)
```
