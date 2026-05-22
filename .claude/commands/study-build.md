You are helping a student build high-quality, exam-oriented study notes from lecture materials.

## Input
Arguments: $ARGUMENTS
Expected format: `[week/section]`
Examples: `W9` | `W7 W8` | `Quiz2`

If no arguments are provided, ask the user which week or section they want to build notes for.

---

## Step 1 — Understand the course

1. **Auto-detect the course**: List subdirectories in the current working directory to find the course folder (look for directories containing a `CLAUDE.md`). If multiple courses exist, ask the user which one.

2. Read the course `CLAUDE.md` to understand:
   - Course structure and file layout
   - What is exam-relevant vs background knowledge
   - Any special instructions about note format or depth

3. **Confirm scope with the user** before proceeding:

   > "准备为 [week/section] 建立复习笔记。这是：
   > - 单周测试（只覆盖本周考点）
   > - 多周测试（W___ 到 W___）
   > - 全范围（Quiz / 期末）
   > 请确认范围。"

---

## Step 2 — Locate sources

**Primary source (required):** Lecture slides / 讲义. Look in subdirectories like `课件/`, `slides/`, `讲义/`, `Lectures/`.
- If slides are not found, tell the user and ask for the path before continuing.
- The slides define what content exists — they are the source of truth.

**Secondary sources:** Only include if the user explicitly mentions them (e.g., tutorial sheets, readings). Do not add secondary sources on your own.

---

## Step 3 — Audit content and assign star ratings

Read the lecture slides carefully. For each concept/topic, assign an importance rating based on:
- Emphasis in slides (bolded, repeated, dedicated section)
- Alignment with past exam patterns (if `CLAUDE.md` mentions them)
- Conceptual depth required (application vs. pure recall)

**Rating system:**
- `★★★` Must cover — almost certain to appear on exam
- `★★` Should cover — high-frequency, likely to appear
- `★` Background only — skip unless building full-range notes

Flag any content that is clearly context-only with no exam value — exclude it.

---

## Step 4 — Check for existing notes

Look for an existing study notes file for the given week/section.

- If found: decide whether to **modify** (add missing content, restructure) or **rewrite** (start fresh with better structure). Either approach is acceptable — choose based on how much is already correct.
- If not found: create a new file at the appropriate path under the course's notes directory.

---

## Step 5 — Plan the narrative structure

For each section, apply the following format based on star rating:

**★★★ sections — all five elements:**

```
> [!info] 问题链
> Problem A → solution B, but creates problem C → solution D...
```
(Once per Part/Week at the top, showing the logical chain across all ★★★ topics)

```
> [!tip] One-sentence scenario question — why does this concept exist?
```
(After each `###` section header)

```
<span style="color: #e67e22">*Transition explaining the problem the previous section creates, leading to the next.*</span>
```
(Between sections)

```
<span style="color: #9b59b6">💡 **白话理解**：Plain-language intuition — not a paraphrase of the definition.</span>
```
(After section content)

**★★ sections:** `[!tip]` + 白话理解 only

**★ sections:** 白话理解 only

**Navigation TOC** (at the top of the file, if not already present):
```
> [!abstract]- 导航
> - [[#Part 1]]
>   - [[#Section A]]
> - [[#Part 2]]
```

**Rules:**
- Never invent content — only add structural elements and plain-language restatements of what the slides actually say
- 白话理解 must be genuine intuition (analogy, contrast, mental model), not just a softer version of the definition
- Transition sentences explain the PROBLEM that motivates the next section, not just "next we discuss X"
- [!tip] questions must be scenario-based ("A hospital's sensors..." not "What is X?")
- All section headers include the star rating: `### Topic Name \`★★★\``

---

## Step 6 — Preview (REQUIRED before writing)

Output a structured preview:

```
## 预览

### 内容覆盖
- ✅ 已覆盖：[list]
- ⚠️ 缺失/需补充：[list]
- ❌ 排除（非考点）：[list]

### 结构计划
- [N] 个 ★★★ 考点，[N] 个 ★★，[N] 个 ★
- 问题链涵盖：[summary]
- 新增 [!tip] × N，过渡句 × N，白话理解 × N

确认以上计划？(Y 开始写 / N 取消 / 具体修改意见)
```

Wait for confirmation before writing anything.

---

## Step 7 — Write and push

After confirmation:

1. Write or modify the notes file with full narrative structure
2. Commit with a descriptive message (e.g., `build: W9 notes — Transformer and BERT`)
3. Push: `git stash && git pull --rebase && git stash pop && git push`
