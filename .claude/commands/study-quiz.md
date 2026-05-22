You are helping a student generate high-quality, exam-realistic practice questions.

## Input
Arguments: $ARGUMENTS
Expected format: `[course-folder] [week/section]`
Examples: `COMP5339_DataEngineering W9` | `COMP5339_DataEngineering W9 W10` (multi-week)

---

## Step 1 — Understand the course and exam format

1. Read the course `CLAUDE.md` to learn:
   - Exam format (question types, style, marks)
   - What is exam-relevant vs background

2. Read the study notes for the given week(s). Identify all topics by importance:
   - ★★★ Must cover — almost certain to appear
   - ★★ Should cover — high-frequency
   - ★ Skip unless multi-week mock exam

3. Check if past exam questions are recorded in the notes (look for `📎 真题参考`).

---

## Step 2 — Ask about past exam questions

If no `📎 真题参考` marker is found in the notes, ask:

> "这个章节有真实考题可以参考吗？有请粘贴，没有输入 N。"

If the user provides past questions:
- Analyse their complexity, scenario style, and distractor design
- Record `> 📎 真题参考：有` at the top of the relevant notes section
- Use their style as the benchmark for your generated questions

---

## Step 3 — Propose a question plan

Based on the exam format from CLAUDE.md and the number of ★★★/★★ topics, propose:

> "本章有 X 个 ★★★ 考点，Y 个 ★★ 考点。建议出：
> - [N] MCQ（每题对应一个核心考点）
> - [N] 简答/场景题（涵盖 [topics]）
> 你要调整吗？"

Wait for confirmation or adjustment before generating.

---

## Step 4 — Generate questions

### MCQ rules (non-negotiable)
- **Always scenario-based**: open with a concrete situation ("A fintech startup processes 2M transactions/day...", "A hospital's IoT sensors transmit every 30s...")
- **All 4 options similar length** — the correct answer must not stand out by being longer or more comprehensive
- **Distractors reflect real misconceptions** — each wrong option should be something a student who half-understands the topic would genuinely consider
- **No absolute language** in wrong options ("always", "never", "only", "cannot") — these are instant tells
- **Do not make the correct answer the "most complete" sounding one** — correctness comes from matching the scenario, not from sounding thorough
- If past exam questions exist, match their difficulty and style exactly

### Short-answer / scenario question rules
- Ask for **comparison + tradeoff**, not just definition
- Ground every question in a **specific scenario** with constraints (latency requirement, data volume, compliance need...)
- Multi-part questions (a/b/c) should build: (a) identify/classify → (b) explain mechanism → (c) evaluate tradeoff or edge case
- Mark allocation must be visible: **(X Marks)**

### Coverage check
Before finalising, verify:
- Every ★★★ topic appears in at least one question
- No question tests pure memorisation — each requires applying or reasoning about a concept

---

## Step 5 — Preview (REQUIRED before writing)

Output all questions in final format, including answers. Then ask:

> "以上题目确认？(Y 写入文件 / N 取消 / 具体修改意见)"

---

## Step 6 — Write to file and push

After confirmation:

1. Write to the appropriate test file (e.g. `测试/每周测试/第N周 [Topic].md`)
   - Create the file if it doesn't exist, using the established format
   - Append to existing file if it already has questions — add a `---` separator and `> 📌 **新增题目**` marker
   - Use `> [!note]- Answer` for collapsible answers

2. Commit with a descriptive message

3. Push: `git stash && git pull --rebase && git stash pop && git push`
