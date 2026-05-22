You are helping a student structure their study notes with a consistent narrative format.

## Input
Arguments: $ARGUMENTS
Expected format: `[course-folder] [week/section]`
Examples: `COMP5339_DataEngineering W9` | `COMP5339_DataEngineering Quiz2 W9`

---

## Step 1 — Understand the course

1. Find and read the course `CLAUDE.md` (usually at `[course-folder]/CLAUDE.md`) to understand:
   - Course structure and file layout
   - What is exam-relevant vs background knowledge
   - Any special instructions

2. Locate the **lecture slides / 讲义** for the given week. Look in subdirectories like `课件/`, `slides/`, `讲义/`. This is the **primary source of truth** for content coverage.
   - If no slides are found, tell the user and ask if they can provide the path.

3. Locate the existing **study notes** file for the given week/section (secondary reference).

---

## Step 2 — Audit content coverage

Read the lecture slides and check whether the existing study notes cover all exam-relevant content from the slides. Flag any gaps:
- Missing concepts that are likely exam-relevant
- Concepts present in notes but not in slides (double-check necessity)
- Sections that exist but lack depth

Do **not** include content that is clearly background/context-only with no exam value.

---

## Step 3 — Plan the narrative structure

For the target section, plan the following additions using this exact format system:

**A. Content navigation** (at top of file, if not already present):
```
> [!abstract]- 导航
> - [[#Section 1]]
>   - [[#Subsection]]
> - [[#Section 2]]
```

**B. Problem chain** (once per Part/Week, at the top):
```
> [!info] 问题链
> Problem A → solution B, but creates problem C → solution D...
```

**C. Motivation question** (after each `###` section header):
```
> [!tip] One-sentence scenario question — why does this concept exist?
```

**D. Orange transition sentence** (between sections, explains WHY the next topic is needed):
```
<span style="color: #e67e22">*Transition explaining the problem the previous section creates, leading to the next.*</span>
```

**E. Purple 白话理解** (after section content, plain-language intuition):
```
<span style="color: #9b59b6">💡 **白话理解**：Plain-language explanation of the core intuition.</span>
```

**Rules:**
- Never invent content — only add structural elements and plain-language restatements of existing content
- 白话理解 must be genuine intuition, not a paraphrase of the definition
- Transition sentences explain the PROBLEM that motivates the next section
- [!tip] questions must be scenario-based, not "what is X?"
- Check for existing elements before adding — do not duplicate
- ★★★ sections get all elements; ★★ get [!tip] + 白话理解; ★ get 白话理解 only

---

## Step 4 — Preview (REQUIRED before any file changes)

Output a structured preview in this format:

```
## 预览：准备添加以下内容

### 内容覆盖
- ✅ 已覆盖：[list]
- ⚠️ 缺失/需补充：[list, if any]

### 结构添加
1. [位置描述] → [要插入的内容摘要]
2. ...

确认以上修改？(Y 继续 / N 取消 / 具体修改意见)
```

Wait for user confirmation before proceeding.

---

## Step 5 — Apply and push

After confirmation:
1. Edit the file(s) using precise string replacement
2. If content gaps were identified and user approved filling them, add the missing content
3. Commit with a descriptive message
4. Push: `git stash && git pull --rebase && git stash pop && git push`
