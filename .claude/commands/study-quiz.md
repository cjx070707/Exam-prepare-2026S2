You are helping a student generate high-quality, exam-realistic practice questions.

## Input
Arguments: $ARGUMENTS
Expected format: `[week/section]`
Examples: `W9` | `W9 W10` | `Quiz2`

If no arguments are provided, ask the user which week or section they want to be tested on.

---

## Step 1 — Understand the course and exam format

1. **Auto-detect the course**: List subdirectories in the current working directory to find the course folder (look for directories containing a `CLAUDE.md`). If multiple courses exist, ask the user which one.

2. Read the course `CLAUDE.md` to learn:
   - Exam format: question types available (MCQ, short answer, scenario, calculation, etc.)
   - Mark allocation and question structure
   - What is exam-relevant vs background

   If no `CLAUDE.md` exists, ask the user:
   > "找不到课程配置文件。这门课考什么题型？（如：MCQ、简答、场景题）有没有分值信息？"
   > 可选：是否帮你创建一个 CLAUDE.md？

3. **Confirm scope with the user:**

   > "准备为 [section] 出题。这是：
   > - 单周测试（只考本周）
   > - 多周测试（W___ 到 W___）
   > - 全范围（Quiz / 期末）"

4. Read the study notes for the given week(s). Identify all topics by importance:
   - ★★★ Must cover — almost certain to appear
   - ★★ Should cover — high-frequency
   - ★ Skip unless multi-week or full-range mock exam

---

## Step 2 — Ask about past exam questions

Check the notes for a `📎 真题参考` marker. If not found, ask:

> "这个章节有真实考题可以参考吗？有请粘贴，没有输入 N。"

If the user provides past questions:
- Analyse their complexity, scenario style, and distractor design
- Record `> 📎 真题参考：有` at the top of the relevant notes section
- Use their style as the benchmark for generated questions

---

## Step 3 — Confirm question types

Based on `CLAUDE.md`, propose the question types for this session. **Always ask the user to confirm** — do not assume:

> "根据课程配置，可用题型有：[list from CLAUDE.md]
> 本次出题建议用：[your recommendation]
> 你要调整吗？"

Different courses have different formats — never hardcode question types.

---

## Step 4 — Propose a question plan

Based on the number of ★★★/★★ topics and the confirmed question types, propose:

> "本章有 X 个 ★★★ 考点，Y 个 ★★ 考点。建议出：
> - [N] MCQ（对应考点：[list]）
> - [N] 简答/场景题（涵盖：[topics]）
> 你要调整吗？"

Wait for confirmation or adjustment before generating.

---

## Step 5 — Generate questions

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

## Step 6 — Preview (REQUIRED before writing)

Output all questions in final format, including answers. Then ask:

> "以上题目确认？(Y 写入文件 / N 取消 / 具体修改意见)"

---

## Step 7 — Write to file and push

After confirmation:

1. Write to the appropriate test file (e.g., `测试/每周测试/第N周 [Topic].md`)
   - Create the file if it doesn't exist, using the established format
   - Append to existing file if it already has questions — add a `---` separator and `> 📌 **新增题目**` marker
   - Use `> [!note]- Answer` for collapsible answers

2. Commit with a descriptive message (e.g., `quiz: W9 stream processing practice questions`)

3. Push: `git stash && git pull --rebase && git stash pop && git push`
