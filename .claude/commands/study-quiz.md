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

4. **Source hierarchy (non-negotiable):**
   - **复习笔记** is the authoritative source for question content — all question stems, answer explanations, and concept descriptions must be traceable to what the notes actually say.
   - 复习笔记 is itself derived from lecture PDFs. If a topic is not in the notes, do not generate questions on it using training knowledge — flag the gap instead.
   - **Never inject content from training knowledge.** Every fact in a question must appear in the notes you have read.

5. Read the study notes for the given week(s). Identify all topics by importance:
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
- **Scenario-based, but concise**: open with a concrete situation, but cut all corporate fluff. Keep only the cause-effect chain that sets up the question. Target ~25–35 words for the stem.
  - ✅ "A linear regression model fails regardless of weight tuning. The team switches to an MLP. Which statement best explains why?"
  - ❌ "A fintech startup builds a loan-default prediction model. Their initial linear regression model achieves poor training accuracy regardless of how weights are tuned. The team decides to switch to a three-layer MLP. Which statement most accurately explains..."
- **Never hint at the answer in the stem** — do not include phrases that imply the correct direction (e.g., "suggesting the data is non-linear" gives away the answer)
- **All 4 options must be similar length** — if the correct answer is noticeably longer or more detailed, rewrite the distractors to match. Length must not be a signal.
- **Distractors must sound plausible** — each wrong option should reflect a real misconception a half-understanding student would genuinely consider. Never write a distractor that is obviously absurd or trivially false.
- **No absolute language in any option** ("always", "never", "only", "cannot", "all", "none") — these are instant elimination tells. Rephrase to sound equally hedged across all options.
- **Do not make the correct answer the most thorough-sounding one** — wrong options should also sound specific and reasoned, not vague or circular. The difference between options should be *what* they claim, not *how confidently* they claim it.
- If past exam questions exist, match their difficulty and style exactly
- MCQ options **must use checkbox format** for Obsidian interactivity:
  ```
  - [ ] A. Option text
  - [ ] B. Option text
  - [ ] C. Option text
  - [ ] D. Option text
  ```

### Short-answer / scenario question rules
- Ask for **comparison + tradeoff**, not just definition
- Ground every question in a **specific scenario** with constraints (latency requirement, data volume, compliance need...)
- Multi-part questions (a/b/c) should build: (a) identify/classify → (b) explain mechanism → (c) evaluate tradeoff or edge case
- Mark allocation must be visible: **(X Marks)**

### Coverage rules (non-negotiable)
- **The pipeline is: Lecture PDF → 复习笔记 → 测试题.** Questions are generated from the notes; the notes are generated from PDFs. Never shortcut from PDF directly to questions, and never use training knowledge to fill either layer.
- Before finalising questions, cross-check each ★★★ topic in the notes to confirm it has at least one question.
- Every ★★★ topic must appear in at least one question. If a gap is found, **fill it immediately without asking** — generate the missing question and add it.
- No question tests pure memorisation — each requires applying or reasoning about a concept.
- **Gap-filling is automatic**: if the coverage audit reveals an uncovered ★★★ topic, add the question directly to the file. Do not ask for confirmation first.

### Numbering rules
- Questions are numbered **globally and sequentially** across all question types: Q1, Q2, Q3 ... regardless of section (MCQ / SA / Coding / Essay).
- Never reuse a number within the same file. MCQ Q6 and SA Q6 in the same file is a bug — SA must continue from where MCQ left off.

---

## Step 6 — Preview (REQUIRED before writing)

Output all questions in final format, including answers. Then ask:

> "以上题目确认？(Y 写入文件 / N 取消 / 具体修改意见)"

**Exception**: If filling a coverage gap (Step 5 coverage rules), write directly to file without preview — the gap is clear, the user has already approved the overall plan.

---

## Step 7 — Write to file and push

After confirmation:

1. Write to the appropriate test file (e.g., `测试/每周测试/第N周 [Topic].md`)
   - Create the file if it doesn't exist, using the established format
   - Append to existing file if it already has questions — add a `---` separator and `> 📌 **新增题目**` marker
   - Use `> [!note]- Answer` for collapsible answers
   - MCQ options must use checkbox format for Obsidian interactivity:
     ```
     - [ ] A. Option text
     - [ ] B. Option text
     - [ ] C. Option text
     - [ ] D. Option text
     ```

2. Commit with a descriptive message (e.g., `quiz: W9 stream processing practice questions`)

3. Push: `git stash && git pull --rebase && git stash pop && git push`
