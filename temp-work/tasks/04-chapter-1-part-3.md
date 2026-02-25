# Task 04: Chapter 1 Part 3 — Sections 1.7–1.10 (16 slides)

> **Scope:** SDD Artifacts (5) + Constitution Deep-Dive (3) + Extension System (3) + Comparison (5)
> **Plan reference:** `slides/SLIDE-PLAN-EN.md` lines 125–160
> **JP reference:** `slides/spec-kit-presentation.md` lines 870–1190

---

## Section 1.7: SDD Artifacts — What Spec Kit Generates (5 slides)

### Slide 1-36: SDD Artifact Overview & Relationship Diagram

**Plan ref:** Line 129 | **JP ref:** Lines 870–900

```markdown
---

## Section 1.7: SDD Artifacts

# SDD Artifact Overview & Relationship Diagram

```
constitution.md  →  spec.md  →  clarifications
      ↓                ↓              ↓
   Principles      What to       Resolved
   & constraints   build         ambiguities
                                     ↓
                      plan.md + data-model.md  →  tasks.md  →  Code
                         ↓                          ↓
                      How to                    Step-by-step
                      build                     ordering
```

> **Each artifact references the previous one — a chain of traceability**
```

**Notes:**
- ASCII diagram showing artifact relationships (8 lines)
- Blockquote for key insight

---

### Slide 1-37: Template Contents — Constitution Template Example

**Plan ref:** Line 130 | **JP ref:** Lines 900–920

```markdown
---

## Section 1.7: SDD Artifacts

# Template Contents — Constitution Template Example

```markdown
## Core Principles

### [PRINCIPLE_NAME]
[PRINCIPLE_DESCRIPTION]

### [PRINCIPLE_NAME]
[PRINCIPLE_DESCRIPTION]

## Technology Constraints

### [CONSTRAINT_NAME]
[CONSTRAINT_DESCRIPTION]
```

> AI fills in `[PLACEHOLDERS]` following the template structure.
> **Templates ensure quality and consistency across all projects.**
```

**Notes:**
- Markdown-within-markdown code block showing template structure (10 lines)
- Blockquote explaining how AI uses the template

---

### Slide 1-38: The Constitution's 9 Articles

**Plan ref:** Line 131 | **JP ref:** Lines 920–950

```markdown
---

## Section 1.7: SDD Artifacts

# The Constitution's 9 Articles — Immutable Principles

Based on `spec-driven.md`:

1. **Simplicity gate** — no over-engineering
2. **Library-first** — use existing solutions
3. **Pure-function core** — predictable business logic
4. **Observability via CLI** — debuggable from the terminal
5. **Single source of truth** — one canonical location per fact

### 4 Design Philosophies

Modularity > Monoliths · Observability > Opacity
Simplicity > Cleverness · Integration > Isolation

> These are **immutable** — implementation details evolve, principles remain constant
```

**Notes:**
- 5 articles shown (not all 9 — content density limit). Plan says 9 but showing all 9 would exceed 5-bullet limit
- Alternative: show 5 in list + "and 4 more: test-first, modular by default, config over code, security by default" as text
- h3 for design philosophies (compact inline format)
- Blockquote for immutability message

---

### Slide 1-39: 7 Template Patterns That Constrain the LLM

**Plan ref:** Line 132 | **JP ref:** Lines 950–980

```markdown
---

## Section 1.7: SDD Artifacts

# 7 Template Patterns That Constrain the LLM

| # | Pattern | Effect |
|---|---|---|
| 1 | **What/How separation** | No tech stack in Specify phase |
| 2 | **`[NEEDS CLARIFICATION]`** | No guessing on ambiguity |
| 3 | **Checklists** | No skipping self-review |
| 4 | **Phase -1 Gates** | No over-complex designs |
| 5 | **Hierarchical detail** | No code in primary documents |
| 6 | **Test-first ordering** | No implementation before tests |

> **Templates = "unit tests for specifications"**

*Pattern 7: No speculative features — no adding "nice to haves"*
```

**Notes:**
- 6-row × 3-column table (at the row limit) — pattern 7 below as italic text
- Blockquote for metaphor
- This is one of the most important conceptual slides

---

### Slide 1-40: SDD Artifact Flow — Live Demo Image

**Plan ref:** Line 133 | **JP ref:** Lines 980–1010

```markdown
---

## Section 1.7: SDD Artifacts

# SDD Artifact Flow — Live Demo

```
① specify init . --ai copilot
    ↓
② Copilot Chat: /speckit.constitution
    ↓
③ constitution.md generated
    ↓
④ /speckit.specify  →  ⑤ spec.md generated
    ↓
⑥ /speckit.plan     →  ⑦ plan.md generated
    ↓
⑧ /speckit.implement  →  ⑨ Code generated from specs
```

> **Each step reads the previous artifact to generate the next**
```

**Notes:**
- Numbered step diagram in code block (10 lines — at the limit)
- Shows the complete flow from init to code
- Blockquote for key message

---

## Section 1.8: Constitution Deep-Dive — Gates & Compound Effects (3 slides)

### Slide 1-41: Phase -1 Gates — Pre-Implementation Quality Checks

**Plan ref:** Line 139 | **JP ref:** Lines 1010–1040

```markdown
---

## Section 1.8: Constitution Deep-Dive

# Phase -1 Gates — Pre-Implementation Quality Checks

```markdown
### Phase -1: Pre-Implementation Gates

#### Simplicity Gate (Article VII)
- [ ] Can this be solved with a single function?
- [ ] Does this need a new abstraction?

#### Anti-Abstraction Gate (Article VIII)
- [ ] Is a new interface justified?
- [ ] Would a concrete implementation suffice?
```

> If a gate **fails** → document justification in "Complexity Tracking"
> **Gates act as compile-time checks for architectural principles**
```

**Notes:**
- R3 enhancement — dedicated slide for Phase -1 Gates
- Code block showing actual gate check markdown (8 lines)
- Blockquote explaining failure handling

---

### Slide 1-42: The Compound Effect — Constraints Working Together

**Plan ref:** Line 140 | **JP ref:** Lines 1040–1070

```markdown
---

## Section 1.8: Constitution Deep-Dive

# The Compound Effect — Constraints Working Together

| Quality | Enabled By |
|---|---|
| **Complete** | Checklists + no speculative features |
| **Unambiguous** | `[NEEDS CLARIFICATION]` markers |
| **Testable** | Test-first ordering + Phase -1 gates |
| **Maintainable** | Hierarchical detail + What/How separation |
| **Implementable** | Phase -1 gates + clear phase definitions |

> 7 constraint patterns don't work individually — they **combine**
> LLM transforms: **Creative Writer → Disciplined Specification Engineer**
```

**Notes:**
- R4 enhancement — "The Compound Effect" slide
- 5-row × 2-column mapping table
- Blockquote with the key insight (LLM transformation)

---

### Slide 1-43: Concrete Example: Traditional ~12h vs SDD 15min

**Plan ref:** Line 141 | **JP ref:** Lines 1070–1100

```markdown
---

## Section 1.8: Constitution Deep-Dive

# Concrete Example: Traditional ~12h vs SDD 15min

### Chat feature — from requirements to implementation

| Phase | Traditional | SDD |
|---|---|---|
| **Requirements** | PRD manual writing (2–3h) | `/speckit.specify` (5 min) |
| **Technical Design** | Design doc (3–4h) | `/speckit.plan` (5 min) |
| **Test Planning** | Manual scenarios (2h) | `/speckit.tasks` (5 min) |
| **Total** | **~12 hours** | **~15 minutes** |

Output: `spec.md` + `plan.md` + `data-model.md` + `tasks.md`

> **Not just faster — templates enforce consistency and completeness**
```

**Notes:**
- R5 enhancement — concrete ROI example
- 4-row × 3-column comparison table (including total row)
- Output artifact list
- Blockquote for the "not just faster" message — important persuasion point

---

## Section 1.9: Extension System — Modular Extensibility (3 slides)

### Slide 1-44: Extension System — Modular Extensibility

**Plan ref:** Line 147 | **JP ref:** Lines 1076–1095

```markdown
---

## Section 1.9: Extension System

# Extension System — Modular Extensibility

| Command | Purpose |
|---|---|
| `specify extension add <repo>` | Install extension |
| `specify extension remove <name>` | Uninstall extension |
| `specify extension list` | Show installed extensions |
| `specify extension search <query>` | Search extension catalog |
| `specify extension update` | Update extensions |
| `specify extension enable/disable` | Toggle extensions |

> **Customize and extend the SDD workflow for your team**
```

**Notes:**
- R6 enhancement — dedicated Extension System section
- 6-row × 2-column command table (at the limit)
- Blockquote for key message

---

### Slide 1-45: Extension Manifest & Organization Customization

**Plan ref:** Line 148 | **JP ref:** Lines 1095–1115

```markdown
---

## Section 1.9: Extension System

# Extension Manifest & Organization Customization

```yaml
extension:
  name: spec-kit-jira
  version: "0.1.0"
provides:
  commands:
    - name: jira-sync
      script: jira-sync.sh
hooks:
  after_tasks:
    - sync-to-jira.sh
```

- Custom catalog URL (`SPECKIT_CATALOG_URL`)
- Hooks for automation after SDD phases
- Distribute via GitHub repo tags → whole team
```

**Notes:**
- YAML code block (10 lines — at the limit)
- 3 bullet features for org-level customization
- Demonstrates hook system

---

### Slide 1-46: Example: Jira Integration Extension

**Plan ref:** Line 149 | **JP ref:** Lines 1115–1140

```markdown
---

## Section 1.9: Extension System

# Example: Jira Integration Extension

```bash
specify extension add github.com/mbachorik/spec-kit-jira
```

### What it does
- Syncs `tasks.md` items to Jira issues (like `/speckit.taskstoissues`)
- Maps SDD phases to Jira workflow states
- Integrates with existing project management tools

> **SDD doesn't replace your workflow — it enhances it**
```

**Notes:**
- Install command in code block (1 line)
- h3 sub-section with 3 bullets
- Blockquote for key message — important for enterprise adoption

---

## Section 1.10: Vibe Coding vs SDD — Detailed Comparison (5 slides)

### Slide 1-47: Vibe Coding vs SDD — Detailed Comparison

**Plan ref:** Line 155 | **JP ref:** Lines 1140–1170

```markdown
---

## Section 1.10: Vibe Coding vs SDD

# Vibe Coding vs SDD — Detailed Comparison

| Axis | Vibe Coding | SDD |
|---|---|---|
| **Starting point** | Vague prompt | Structured specification |
| **Edge cases** | Discovered in production | Caught in Clarify phase |
| **Documentation** | None (or outdated) | Specs ARE the documentation |
| **Pivot cost** | Full rewrite | Spec update → regenerate |
| **Where intent lives** | Buried in code | Explicit in specs |
| **AI output quality** | 🎲 Unpredictable | ✅ Predictable |
```

**Notes:**
- 6-row × 3-column comparison table (at the row limit)
- This is the comprehensive comparison slide — the "definitive answer"

---

### Slide 1-48: "Is SDD Slow?"

**Plan ref:** Line 156 | **JP ref:** Lines 1170–1195

```markdown
---

## Section 1.10: Vibe Coding vs SDD

# "Is SDD Slow?"

> **Time writing specs < Time fixing bugs**

- Bugs caught in Clarify are bugs that **never exist**
- Pivoting is low-cost — specs are reusable across tech stacks
- The spec survives technology changes — code doesn't
- 3 months later: "Why this design?" → read the spec (not reverse-engineer the code)

> **"Writing correctly IS true speed"**
```

**Notes:**
- Common objection response slide
- Two blockquotes (opening and closing)
- 4 bullets for counterarguments

---

### Slide 1-49: Where SDD Shines (and Where It's Overkill)

**Plan ref:** Line 157 | **JP ref:** Lines 1195–1220

```markdown
---

## Section 1.10: Vibe Coding vs SDD

# Where SDD Shines (and Where It's Overkill)

### ✅ Best for:
- Team development (shared understanding through specs)
- AI-assisted development (AI follows structured specs)
- External service integrations (contracts prevent misunderstandings)
- Financial/security-critical systems (specs enforce correctness)
- Long-term maintenance projects (specs = living documentation)

### ⚠️ Overkill for:
- Throwaway scripts
- Exploratory prototypes (but move to SDD once you have direction)
```

**Notes:**
- Two h3 sub-sections with ✅/⚠️ icons
- 5 "best for" items + 2 "overkill" items
- Balanced perspective — acknowledges SDD isn't always needed

---

### Slide 1-50: Bidirectional Feedback — Specs ↔ Production

**Plan ref:** Line 158 | **JP ref:** Lines 1220–1250

```markdown
---

## Section 1.10: Vibe Coding vs SDD

# Bidirectional Feedback — Specs ↔ Production

- Production metrics and incidents don't just trigger hotfixes — they **update specifications**
- Performance bottlenecks become new non-functional requirements
- Security vulnerabilities become constraints for all future generations

> **Continuous evolution, not one-shot generation**

SDD transforms the traditional SDLC:
- Requirements and design become **continuous activities**
- Not discrete phases that happen once and are forgotten
```

**Notes:**
- Source: `spec-driven.md`
- 3 bullets for feedback examples
- Blockquote for key message
- 2 bullets for SDLC transformation (R10 enhancement)

---

### Slide 1-51: Branching for Exploration

**Plan ref:** Line 159 | **JP ref:** Lines 1250–1280

```markdown
---

## Section 1.10: Vibe Coding vs SDD

# Branching for Exploration

SDD supports **parallel implementations** from the same spec:
- Different tech stacks (React vs Vue vs Svelte)
- Different architectures (monolith vs microservices)
- Different UX patterns — all generated from ONE specification

```
0 → 1, (1', 1'', …), 2, 3, N
```

### Team process
- Specs are versioned in branches, reviewed, and merged
- `specs/[branch]/` for team review workflows

> **Branching isn't just for code — it's for exploring design alternatives**
```

**Notes:**
- Source: `spec-driven.md`
- 3 bullet examples + code block for branching notation
- h3 for team process angle (Enhancement D)
- Blockquote for closing message

---

## ✅ Chapter 1 Part 3 Quality Checks

- [ ] Section 1.7 has exactly 5 slides (1-36 through 1-40)
- [ ] Section 1.8 has exactly 3 slides (1-41 through 1-43)
- [ ] Section 1.9 has exactly 3 slides (1-44 through 1-46)
- [ ] Section 1.10 has exactly 5 slides (1-47 through 1-51)
- [ ] Phase -1 Gates has its own dedicated slide (1-41)
- [ ] Compound Effect slide is present (1-42) with quality mapping table
- [ ] ROI example (~12h vs 15min) is present (1-43)
- [ ] Extension System has 3 dedicated slides including YAML manifest
- [ ] Bidirectional Feedback includes SDLC transformation message
- [ ] Branching slide includes team process / branch versioning
- [ ] All tables ≤ 6 rows × 4 columns
- [ ] All code blocks ≤ 10 lines
- [ ] All h2 labels: `## Section 1.7`, `## Section 1.8`, `## Section 1.9`, `## Section 1.10`
- [ ] No Japanese text
