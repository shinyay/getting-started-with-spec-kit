# Task 02: Chapter 1 Part 1 — Sections 1.1–1.3 (22 slides)

> **Scope:** Vibe Coding Problem (6) + SDD Principles & Phases (10) + Spec Kit Overview (6)
> **Plan reference:** `slides/SLIDE-PLAN-EN.md` lines 60–95
> **JP reference:** `slides/spec-kit-presentation.md` lines 92–540

---

## Section 1.1: The Problem — Limits of Vibe Coding (6 slides)

### Slide 1-1: What Is Vibe Coding?

**Plan ref:** Line 64 | **JP ref:** Lines 92–120

```markdown
---

<!-- _paginate: false -->
<!-- _header: "" -->

# Chapter 1: General — SDD Overview & Spec Kit

---

## Section 1.1: The Problem

# What Is Vibe Coding?

> **"Giving AI a rough idea and accepting whatever it produces."**

### A typical pattern

You: "Build me a chat app"

AI **silently decides**:
- Database design (MongoDB? PostgreSQL? Firebase?)
- Authentication model (JWT? Sessions? None?)
- Permission model (Admin? Roles? Everyone equal?)
- Error handling strategy (Silent? Dialog? Retry?)
- Test strategy (None? Jest? Manual?)

**You don't know about these choices. AI decided for you.**
```

**IMPORTANT:** This block produces TWO slides:
1. The section divider (`# Chapter 1: ...`) — slide 1-1 in the plan is actually preceded by the section divider
2. The content slide about vibe coding

Actually, re-examining the plan: slide `1-1` is "What Is Vibe Coding?" — the section divider for Chapter 1 is NOT numbered in the plan. However, looking at the JP presentation, the Chapter 1 divider at line 97 IS counted as a slide (separated by `---`).

**Resolution:** The SLIDE-PLAN-EN.md has 51 numbered slides for Chapter 1 (1-1 through 1-51), but the chapter 1 section divider is NOT among them. The section divider is implicit. Following the JP pattern, insert the Chapter 1 divider as an unnumbered slide BEFORE slide 1-1.

**Corrected structure:**

#### Slide: Chapter 1 Section Divider (unnumbered)

```markdown
---

<!-- _paginate: false -->
<!-- _header: "" -->

# Chapter 1: General — SDD Overview & Spec Kit
```

#### Slide 1-1: What Is Vibe Coding?

```markdown
---

## Section 1.1: The Problem

# What Is Vibe Coding?

> **"Giving AI a rough idea and accepting whatever it produces."**

### A typical pattern

You: "Build me a chat app"

AI **silently decides**:
- Database design (MongoDB? PostgreSQL? Firebase?)
- Authentication model (JWT? Sessions? None?)
- Permission model (Admin? Roles? Everyone equal?)
- Error handling strategy (Silent? Dialog? Retry?)

**You don't know about these choices. AI decided for you.**
```

**Notes:**
- Blockquote for the definition (green left border)
- 4 bullet items under "AI silently decides" (reduced from 5 to stay within limits — test strategy can be merged)
- Bold closing statement
- JP ref lines 103–118

---

### Slide 1-2: The 4 Failure Patterns of Vibe Coding

**Plan ref:** Line 65 | **JP ref:** Lines 120–138

```markdown
---

## Section 1.1: The Problem

# The 4 Failure Patterns of Vibe Coding

### 1. 🔓 AI decides permission rules without asking
"Can users vote on their own posts?" → AI decides silently

### 2. 🐛 Edge cases become production bugs
`0.1 + 0.2 = 0.30000000000000004` → billing bug

### 3. 🏗️ Over-engineered tech stack
"TODO app" → Kubernetes + Redis + GraphQL + microservices

### 4. 🔍 Intent buried in code — unmaintainable
3 months later: "Why this implementation?" → "AI decided. Reason unknown."
```

**Notes:**
- 4 h3 sub-sections with emoji icons
- Each pattern has a concrete one-line example
- Matches JP structure exactly (lines 124–137)

---

### Slide 1-3: "Build Me an App" — The Results

**Plan ref:** Line 66 | **JP ref:** Lines 138–155

```markdown
---

## Section 1.1: The Problem

# "Build Me an App" — The Results

| Aspect | Vibe Coding | SDD |
|---|---|---|
| **Input** | "Build me a chat app" | Structured specification |
| **DB Design** | AI guesses | Defined in spec |
| **Permission Model** | AI guesses | Explicit matrix |
| **Edge Cases** | Discovered in production | Caught in Clarify |
| **Output Quality** | 🎲 Unpredictable | ✅ Predictable |
| **Reproducibility** | ❌ Different every time | ✅ Same spec → same output |

> Same prompt, dramatically different AI output quality when specs exist
```

**Notes:**
- Table: 6 rows × 3 columns (at the limit)
- Blockquote for closing insight
- Bold column headers in first column

---

### Slide 1-4: AI Works Dramatically Better with Structure

**Plan ref:** Line 67 | **JP ref:** Lines 155–176

```markdown
---

## Section 1.1: The Problem

# AI Works Dramatically Better with Structure

### ❌ Without structure (Vibe Coding)

```
Vague prompt → AI guesses → Unpredictable output → Bugs
```

### ✅ With structure (SDD)

```
Structured spec → AI follows → Predictable, high-quality output
```

> **AI is an excellent implementer, but not an excellent designer.**
> Design is your job. Implementation is AI's job.
```

**Notes:**
- Two h3 sub-sections with ❌/✅ icons
- Short code blocks showing flow (2 lines each)
- Blockquote with the **key message** of the entire presentation (bold)
- This is the "aha moment" setup for Chapter 1

---

### Slide 1-5: Question: What's Your Development Flow?

**Plan ref:** Line 68 | **JP ref:** Lines 176–192

```markdown
---

## Section 1.1: The Problem

# Question: What's Your Development Flow?

When you have AI write code…

- Do you write a **specification** before handing it to AI?
- Do you explicitly define **permission rules**?
- Do you identify **edge cases** beforehand?
- Can you **explain** why AI produced a particular output?

> If even one answer is "No," you're **vibe coding**.
> SDD changes that.
```

**Notes:**
- Interactive/discussion slide — meant to engage the audience
- 4 bullet questions
- Blockquote with the punch line

---

### Slide 1-6: Why SDD Matters NOW — 3 Trends

**Plan ref:** Line 69 | **JP ref:** Lines 192–211

```markdown
---

## Section 1.1: The Problem

# Why SDD Matters NOW — 3 Trends

### 1. 🤖 AI Capabilities Have Reached a Threshold
AI can now **reliably** generate working code from natural-language specs.
SDD gives AI's generation power **direction through structure**.

### 2. 📈 Software Complexity Grows Exponentially
Modern systems integrate dozens of services, frameworks, and dependencies.
Maintaining alignment without specs is **practically impossible**.

### 3. ⚡ Pace of Change Accelerates
Pivoting is the norm, not the exception. Requirement change = spec update → regenerate.
SDD makes pivoting a **systematic regeneration**, not a full rewrite.
```

**Notes:**
- 3 h3 sub-sections with emoji + bold
- Source: `spec-driven.md`
- JP ref lines 196–210: nearly identical structure

---

## Section 1.2: SDD Principles & the 6 Phases (10 slides)

### Slide 1-7: What Is Spec-Driven Development?

**Plan ref:** Line 75 | **JP ref:** Lines 212–227

```markdown
---

## Section 1.2: SDD Principles & the 6 Phases

# What Is Spec-Driven Development?

> **"Write structured specifications first, then AI follows them — producing predictable, high-quality output every time."**

### SDD's Key Message

- The spec is the **primary artifact**; code is merely its expression
- Specs are technology-independent — switching React → Vue doesn't change the spec
- Specs catch bugs **before they exist** — problems discovered before any code is written
- The spec is the **Single Source of Truth**
```

**Notes:**
- Large blockquote for the definition
- 4 bullet key messages
- h3 "SDD's Key Message" sub-section

---

### Slide 1-8: The Power Inversion — SDD's Core Insight

**Plan ref:** Line 76 | **JP ref:** Lines 227–260

```markdown
---

## Section 1.2: SDD Principles & the 6 Phases

# The Power Inversion — SDD's Core Insight

> **For decades, code was king. Specs served code.**
> **SDD inverts this: code serves specifications.**

- Specs don't merely guide implementation — they **generate** it
- The gap between spec and implementation is **eliminated**, not narrowed
- "Intent-driven development" — the lingua franca moves to a higher level
- This transforms the traditional SDLC — requirements and design become **continuous activities**, not discrete phases

> **Debugging means fixing specifications. Refactoring means restructuring for clarity.**
```

**Notes:**
- Source: `spec-driven.md`
- Two blockquotes — top (core insight) and bottom (debugging insight)
- 4 bullets for elaboration
- Includes SDLC transformation framing (R10 enhancement)

---

### Slide 1-9: The 6 Phases of SDD (Overview)

**Plan ref:** Line 77 | **JP ref:** Lines 260–285

```markdown
---

## Section 1.2: SDD Principles & the 6 Phases

# The 6 Phases of SDD

```
1. Constitution  → Define project principles and constraints
2. Specify       → Describe what to build (not how)
3. Clarify       → Surface hidden assumptions and edge cases
4. Plan          → Choose architecture and technology
5. Tasks         → Break down into executable steps
6. Implement     → Generate code from specifications
```

> Each phase produces an artifact. Each artifact references the previous one.
```

**Notes:**
- Code block for the 6-phase flow (6 lines — well within limits)
- Numbered list format for clear ordering
- Blockquote for key insight

---

### Slide 1-10: Phase 1: Constitution

**Plan ref:** Line 78 | **JP ref:** Lines 285–310

```markdown
---

## Section 1.2: SDD Principles & the 6 Phases

# Phase 1: Constitution

**"Define project principles and constraints"** — the project's DNA

Without a constitution, AI makes its **own assumptions** about:
- Test coverage requirements
- External dependency policy
- Error handling philosophy
- Code style and architecture patterns

### Example Principles
- "Test coverage ≥ 80%"
- "Minimize external dependencies"
- "Fail-closed on authentication errors"
```

**Notes:**
- Bold definition at top
- 4 bullet examples of what AI assumes without a constitution
- h3 sub-section for concrete examples

---

### Slide 1-11: Phase 2: Specify

**Plan ref:** Line 79 | **JP ref:** Lines 310–340

```markdown
---

## Section 1.2: SDD Principles & the 6 Phases

# Phase 2: Specify

**"Describe what to build (not how)"**

- User stories with acceptance criteria
- Intentional `[NEEDS CLARIFICATION]` markers for ambiguous points
- Technology-independent — no tech stack decisions here

### Example

> **User Story:** "As a team member, I can create retrospective cards."
> **Acceptance:** Card has text (max 280 chars), author, timestamp.
> **`[NEEDS CLARIFICATION]`:** Can users edit others' cards?
```

**Notes:**
- 3 bullets for key concepts
- Blockquote example with `[NEEDS CLARIFICATION]` marker
- Emphasis: no tech stack in Specify phase

---

### Slide 1-12: Phase 3: Clarify ⭐ SDD's True Value

**Plan ref:** Line 80 | **JP ref:** Lines 340–375

```markdown
---

## Section 1.2: SDD Principles & the 6 Phases

# Phase 3: Clarify ⭐ SDD's True Value

**"Surface hidden assumptions and edge cases"**

> **This is where SDD delivers the greatest ROI.**
> Catches ambiguity before a single line of code is written.

### Questions that Clarify surfaces:
- "Can users vote on their own posts?"
- "What happens on network timeout?"
- "Are votes anonymous or visible?"
- "What's the maximum number of cards per session?"

**All of these are things AI decides on its own without specs.**
```

**Notes:**
- ⭐ in the h1 title (matches plan)
- Blockquote for key message
- 4 example clarification questions
- Bold closing statement — this is the "aha moment" setup

---

### Slide 1-13: Phase 4: Plan

**Plan ref:** Line 81 | **JP ref:** Lines 375–405

```markdown
---

## Section 1.2: SDD Principles & the 6 Phases

# Phase 4: Plan

**"Choose architecture and technology"** — technology discussion happens only now

- Separating "what" from "how" means specs survive technology changes
- Example: Switching React → Vue doesn't change the spec
- Research agents can investigate library compatibility, performance benchmarks, and security implications
- Organizational constraints integrate automatically

> Technology choices are **informed by the spec**, not the other way around.
```

**Notes:**
- 4 bullets including Research Agents concept (from `spec-driven.md`, R9 enhancement)
- Blockquote for key insight
- Emphasis on what/how separation

---

### Slide 1-14: Phase 5: Tasks

**Plan ref:** Line 82 | **JP ref:** Lines 405–430

```markdown
---

## Section 1.2: SDD Principles & the 6 Phases

# Phase 5: Tasks

**"Break down into executable steps"**

Each task has 4 essential elements:

1. **Clear scope** — exactly what to implement
2. **Traceable origin** — linked to user story in the spec
3. **Explicit ordering** — dependencies determine sequence
4. **Validation criteria** — how to verify completion

> Tasks are generated FROM the spec — not invented independently.
```

**Notes:**
- Numbered list for the 4 elements (emphasize structure)
- Blockquote for key insight

---

### Slide 1-15: Phase 6: Implement

**Plan ref:** Line 83 | **JP ref:** Lines 430–455

```markdown
---

## Section 1.2: SDD Principles & the 6 Phases

# Phase 6: Implement

**"Generate code from specifications"**

- AI follows `tasks.md` ordering
- References specs while writing code
- Does **NOT** add features not in the spec

### Implementation observation points
- Does the generated code match the spec?
- Are permission rules from the Clarify phase respected?
- Does the test coverage meet the Constitution's requirements?
```

**Notes:**
- 3 bullets + 3 observation points
- Emphasis: AI is constrained by specs

---

### Slide 1-16: 3 Development Modes

**Plan ref:** Line 84 | **JP ref:** Lines 455–490

```markdown
---

## Section 1.2: SDD Principles & the 6 Phases

# 3 Development Modes

### 1. 0-to-1 (Greenfield)
Generate from scratch — full SDD workflow, all 6 phases

### 2. Creative Exploration
Parallel implementations — experiment with diverse solutions from the same spec

### 3. Iterative Enhancement (Brownfield)
Add features to existing projects, modernize legacy codebases

> SDD works for new projects, experimentation, AND existing code.
```

**Notes:**
- Source: `spec-driven.md`
- 3 h3 sub-sections with numbered labels
- Blockquote for closing message

---

## Section 1.3: GitHub Spec Kit — The Toolkit (6 slides)

### Slide 1-17: What Is GitHub Spec Kit?

**Plan ref:** Line 90 | **JP ref:** Lines 490–510

```markdown
---

## Section 1.3: GitHub Spec Kit

# What Is GitHub Spec Kit?

**GitHub's open-source SDD toolkit**

> "Build high-quality software faster."

**Two pillars:**
1. **`specify` CLI** — project setup, validation, versioning
2. **Copilot Chat `/speckit.*` slash commands** — execute each SDD phase

**Supports 20+ AI agents** — Copilot, Claude Code, Gemini CLI, Cursor, Codex, Windsurf, and more
```

**Notes:**
- Tagline in blockquote
- 2 numbered pillars (core architecture)
- Brief mention of broad agent support

---

### Slide 1-18: Spec Kit's Two Pillars

**Plan ref:** Line 91 | **JP ref:** Lines 510–530

```markdown
---

## Section 1.3: GitHub Spec Kit

# Spec Kit's Two Pillars

| | Pillar 1: `specify` CLI | Pillar 2: AI Instructions |
|---|---|---|
| **Language** | Python (installed via `uv`) | Markdown |
| **Function** | Project init, validation, versioning | SDD phase execution |
| **Files** | `specify init`, `specify check`, `specify version` | `.github/prompts/*.prompt.md` + `.github/agents/*.agent.md` |
| **Runtime** | Terminal | Copilot Chat / AI Agent |
```

**Notes:**
- 2-column comparison table (4 rows × 3 columns)
- Clear separation of CLI vs AI instruction files

---

### Slide 1-19: Spec Kit Version Info

**Plan ref:** Line 92 | **JP ref:** Lines 530–550

```markdown
---

## Section 1.3: GitHub Spec Kit

# Spec Kit Version Info

| Component | Details |
|---|---|
| **CLI Version** | Installed via `uv tool install` |
| **Template Version** | Bundled with CLI, pinned per release |
| **Runtime** | Python 3.11+ |
| **Dev Container** | Auto-pins version — no manual management |

> For local use: `specify version` shows CLI and template versions
```

**Notes:**
- Simple 2-column table (4 rows)
- Blockquote for tip

---

### Slide 1-20: Community & Adoption — 20+ Supported AI Agents

**Plan ref:** Line 93 | **JP ref:** Lines 550–580

```markdown
---

## Section 1.3: GitHub Spec Kit

# Community & Adoption — 20+ Supported AI Agents

| Agent | Agent | Agent | Agent |
|---|---|---|---|
| Copilot | Claude Code | Gemini CLI | Cursor |
| Codex | Windsurf | Qwen | opencode |
| Kilocode | Auggie | Roo | CodeBuddy |
| Amp | SHAI | Q | Bob |
| Qoder | Antigravity (agy) | Jules | **Generic** |

> **Generic mode** (`--ai generic`): Bring your own agent — SDD is a process, not tied to any tool
```

**Notes:**
- 5 rows × 4 columns agent table (at the limit)
- Blockquote highlighting generic mode
- Bold "Generic" in the table to draw attention

---

### Slide 1-21: 📽️ Video Overview — See SDD in Action

**Plan ref:** Line 94 | **JP ref:** Lines 500–514

```markdown
---

## Section 1.3: GitHub Spec Kit

# 📽️ Video Overview — See SDD in Action

> **Official Spec Kit team video — full SDD walkthrough on a real project**

**📎** `youtube.com/watch?v=a9eR1xsfvHg`

| Viewing Timing | Effect |
|---|---|
| **After this presentation** | Theory → visual reinforcement |
| **Before hands-on** | Grasp the full flow before starting |
| **Review** | Reconfirm phase connections |

> **Theory → Video → Hands-on — 3 steps to master SDD**
```

**Notes:**
- R1 enhancement slide
- YouTube URL in backtick code format
- 3-row timing table
- Two blockquotes: top (description) and bottom (3-step message)

---

### Slide 1-22: Spec Kit Architecture Overview

**Plan ref:** Line 95 | **JP ref:** Lines 514–542

```markdown
---

## Section 1.3: GitHub Spec Kit

# Spec Kit Architecture Overview

```
┌───────────────┐
│  specify CLI  │  ← Install & initialize
└───────┬───────┘
        │ specify init
        ▼
┌───────────────────────────────────────┐
│  .specify/  │  .github/  │  .vscode/  │  ← Project scaffolding
└──────┬──────┴─────┬──────┴─────┬──────┘
       │            │            │
  Templates    Agents &      VS Code
  & Scripts    Prompts       Settings
       │            │
       ▼            ▼
┌─────────────────────────┐
│  SDD Artifacts          │  ← AI generates
│  constitution / spec /  │
│  plan / tasks / code    │
└─────────────────────────┘
```

> **CLI scaffolds the project → AI executes phases → specs drive code**
```

**Notes:**
- ASCII art diagram in code block (14 lines — slightly over the 10-line guideline, but architecture diagrams are an exception per JP precedent)
- Blockquote for summary message
- JP ref shows identical structure at lines 518–539

---

## ✅ Chapter 1 Part 1 Quality Checks

- [ ] Chapter 1 section divider is present (unnumbered, before slide 1-1)
- [ ] Section 1.1 has exactly 6 content slides (1-1 through 1-6)
- [ ] Section 1.2 has exactly 10 content slides (1-7 through 1-16)
- [ ] Section 1.3 has exactly 6 content slides (1-17 through 1-22)
- [ ] "Power Inversion" slide includes SDLC transformation + "debugging = fixing specs"
- [ ] "Plan" phase slide mentions Research Agents
- [ ] "📽️ Video Overview" slide is present with YouTube link
- [ ] Architecture diagram uses ASCII art (not image references)
- [ ] ⭐ marker on Clarify slide title
- [ ] All h2 labels: `## Section 1.1: The Problem`, `## Section 1.2: SDD Principles...`, `## Section 1.3: GitHub Spec Kit`
- [ ] No Japanese text in any slide
- [ ] Every slide has a `---` separator
- [ ] Content density within limits for every slide
