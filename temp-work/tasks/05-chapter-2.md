# Task 05: Chapter 2 — Beginner Scenarios (18 slides)

> **Purpose:** Experience SDD's 6 phases through real scenarios. No server, no DB. Learn the SDD workflow itself.
> **Target Level:** ⭐ Beginner
> **Plan reference:** `slides/SLIDE-PLAN-EN.md` lines 163–206
> **JP reference:** `slides/spec-kit-presentation.md` lines 1280–1600
> **Scenarios:** `scenarios/A-quick-retro.md`, `scenarios/J-pomodoro-timer.md`, `scenarios/K-markdown-notes.md`, `scenarios/L-recipe-collection.md`

---

## Section 2.1: Beginner Scenario Introduction (3 slides)

### Slide 2-1: Chapter 2 Section Divider

**Plan ref:** Line 173 | **JP ref:** ~Line 1280

```markdown
---

<!-- _paginate: false -->
<!-- _header: "" -->

# Chapter 2: Beginner — SDD Workflow Fundamentals
```

**Notes:**
- Section divider — h1 only, centered via CSS

---

### Slide 2-2: Beginner Scenarios

**Plan ref:** Line 174 | **JP ref:** ~Line 1290

```markdown
---

## Section 2.1: Introduction

# Beginner Scenarios

| Scenario | Build | SDD Skills | Time |
|---|---|---|---|
| **A: QuickRetro** | Retrospective board | Data modeling, CRUD, permissions | ~90 min |
| **J: Pomodoro** | Timer app | State machine specification | ~60 min |
| **K: MarkdownPad** | Markdown editor | Output correctness, security | ~60 min |
| **L: RecipeBox** | Recipe manager | Calculation correctness | ~60 min |

> No server, no database. **Learn the SDD workflow itself.**
```

---

### Slide 2-3: Beginner Tech Stack

**Plan ref:** Line 175 | **JP ref:** ~Line 1300

```markdown
---

## Section 2.1: Introduction

# Beginner Tech Stack

- **HTML / CSS / JavaScript** — vanilla, no frameworks
- **localStorage** — client-side persistence
- **No build tools** — no webpack, no bundler
- **No server** — everything runs in the browser

> Why? **Eliminate technical complexity to focus on learning SDD.**
> The workflow is the same regardless of tech stack.
```

---

## Section 2.2: Scenario A — QuickRetro: Full SDD Walkthrough (8 slides)

### Slide 2-4: Scenario A: QuickRetro

**Plan ref:** Line 181 | **JP ref:** ~Line 1320

```markdown
---

## Section 2.2: QuickRetro Walkthrough

# Scenario A: QuickRetro

**Build a team retrospective board**

- Create/edit/delete retrospective cards
- Fixed user selection (4 team members)
- 3 columns: Good / Improve / Action Items
- Voting system with rules

### SDD Skills
Data modeling, CRUD specifications, permission matrix

> Duration: ~90 minutes
```

---

### Slide 2-5: Constitution in Practice

**Plan ref:** Line 182 | **JP ref:** ~Line 1340

```markdown
---

## Section 2.2: QuickRetro Walkthrough

# Constitution in Practice

### Example Principles (QuickRetro)

1. **Simplicity** — vanilla JS, no frameworks
2. **Readability** — code should be self-documenting
3. **Minimal dependencies** — no external libraries
4. **Test coverage** — core logic must be testable
5. **Accessible UI** — basic ARIA compliance

> **Key point: principles are short in proportion to risk.**
> Beginner project = 4–5 principles. Enterprise = 11+.
```

---

### Slide 2-6: Specify in Practice — Intentional Ambiguity

**Plan ref:** Line 183 | **JP ref:** ~Line 1360

```markdown
---

## Section 2.2: QuickRetro Walkthrough

# Specify in Practice — Intentional Ambiguity

### Spec contents:
- Fixed user selection (4 users)
- 3 fixed columns (Good / Improve / Action Items)
- Card CRUD operations
- Voting rules

### `[NEEDS CLARIFICATION]` markers appear:
- Can anyone create a session, or only admins?
- Can users edit **other people's** cards?
- Can you vote on your **own** card?

> The spec **intentionally leaves ambiguities** for the Clarify phase
```

---

### Slide 2-7: Clarify in Practice — 10 Hidden Assumptions

**Plan ref:** Line 184 | **JP ref:** ~Line 1380

```markdown
---

## Section 2.2: QuickRetro Walkthrough

# Clarify in Practice — 10 Hidden Assumptions

- "Can anyone create a session, or only admins?"
- "Can you vote on your own card?"
- "Are votes anonymous or visible?"
- "Can users change their vote?"
- "What's the maximum number of cards per session?"

> **All of these are things AI decides on its own without specs.**

If you don't specify → AI silently picks an answer.
Both "yes" and "no" are reasonable. But **only the user knows the intent.**
```

---

### Slide 2-8: The Clarify "Aha Moment"

**Plan ref:** Line 185 | **JP ref:** ~Line 1400

```markdown
---

## Section 2.2: QuickRetro Walkthrough

# The Clarify "Aha Moment"

### "Can you vote on your own card?"

Without specs, AI silently picks "yes" or "no."

- **If "yes"** → users can inflate their own card importance
- **If "no"** → voting reflects genuine team consensus

Both designs are reasonable. But the business intent is completely different.

> **User intent can only be communicated through specifications.**
> This single question illustrates SDD's entire value proposition.
```

**Notes:**
- This is Chapter 2's "aha moment" — the most impactful slide

---

### Slide 2-9: Plan → Tasks → Implement

**Plan ref:** Line 186 | **JP ref:** ~Line 1420

```markdown
---

## Section 2.2: QuickRetro Walkthrough

# Plan → Tasks → Implement

### Plan
Vanilla HTML/CSS/JS + localStorage → no build step, no server

### Tasks (ordering matters)
1. Data model (Card, User, Vote, Session)
2. Service layer (CRUD + permission checks)
3. UI components (card rendering, voting, column layout)

### Implement
- AI follows task ordering
- Permission checks are centrally managed (not scattered in click handlers)

> **3 phases condensed — but each reads the previous artifact**
```

---

### Slide 2-10: Permission Matrix

**Plan ref:** Line 187 | **JP ref:** ~Line 1440

```markdown
---

## Section 2.2: QuickRetro Walkthrough

# Permission Matrix

| Action | Card Author | Other Users | Session Admin |
|---|---|---|---|
| Create card | ✅ | ✅ | ✅ |
| Edit card | ✅ | ❌ | ✅ |
| Delete card | ✅ | ❌ | ✅ |
| Vote on card | ❌ (own) | ✅ | ✅ |
| Create session | ❌ | ❌ | ✅ |

> **This matrix doesn't get generated without a spec.**
> Without SDD, AI decides all of these silently.
```

**Notes:**
- 5-row × 4-column matrix (within limits)
- The "❌ (own)" shows the Clarify result
- Blockquote reinforces SDD value

---

### Slide 2-11: QuickRetro Takeaways

**Plan ref:** Line 188 | **JP ref:** ~Line 1460

```markdown
---

## Section 2.2: QuickRetro Walkthrough

# QuickRetro Takeaways

1. **Completed the full 6-phase SDD workflow** — Constitution through Implement
2. **Permission rules must be explicitly specified** — AI cannot infer business intent
3. **Clarify has the highest ROI** — catches decisions before code exists
4. **Without specs, AI decides your design for you** — silently, without asking

> Chapter 2's key message: **"Without specs, AI decides your design for you."**
```

---

## Section 2.3: Other Beginner Scenarios (4 slides)

### Slide 2-12: Scenario J: Pomodoro Timer — State Machine Specification

**Plan ref:** Line 194 | **JP ref:** ~Line 1480

```markdown
---

## Section 2.3: Other Beginner Scenarios

# Scenario J: Pomodoro Timer — State Machine Specification

5 timer states: **Idle → Focus → Short Break → Long Break → Paused**

### SDD Lesson
- **Behavior is specified using state machines**
- Every state transition must be explicitly defined
- Wall-clock vs `setInterval` drift problem → spec must address timing precision

> Without a state machine spec, AI invents its own transitions
```

---

### Slide 2-13: Scenario K: MarkdownPad — Output Correctness Specification

**Plan ref:** Line 195 | **JP ref:** ~Line 1500

```markdown
---

## Section 2.3: Other Beginner Scenarios

# Scenario K: MarkdownPad — Output Correctness

### The security question: What does the editor render?

- **Whitelist approach:** "If it's not on the list, don't render it"
- **Blacklist approach:** "Block known-dangerous tags" (vulnerable to new attacks)

### SDD Lesson
- **Output specs are directly tied to security (XSS prevention)**
- URL scheme restrictions: only `http:`, `https:`, `mailto:`
- `javascript:` URLs must be explicitly blocked in the spec

> Without output specs, AI renders everything — including `<script>` tags
```

---

### Slide 2-14: Scenario L: RecipeBox — Calculation Correctness

**Plan ref:** Line 196 | **JP ref:** ~Line 1520

```markdown
---

## Section 2.3: Other Beginner Scenarios

# Scenario L: RecipeBox — Calculation Correctness

### The "1.5 eggs" problem

```javascript
// ❌ parseFloat approach
Math.round(parseFloat('1.005') * 100) // → 100, not 101!

// ✅ Fraction arithmetic
{ numerator: 3, denominator: 2 } // 1.5 — exact representation
```

### SDD Lesson
- **Calculation specs must state precision requirements explicitly**
- `{ numerator, denominator }` representation avoids floating-point errors
- Rounding rules must be in the spec (round up? truncate? banker's rounding?)
```

---

### Slide 2-15: Beginner Progression

**Plan ref:** Line 197 | **JP ref:** ~Line 1540

```markdown
---

## Section 2.3: Other Beginner Scenarios

# Beginner Progression — Skills That Build

| Order | Scenario | New SDD Skill |
|---|---|---|
| 1st | **A: QuickRetro** | Data modeling + CRUD + permissions |
| 2nd | **J: Pomodoro** | State machine specification |
| 3rd | **K: MarkdownPad** | Output correctness + security |
| 4th | **L: RecipeBox** | Calculation correctness |

> Each step adds a **new specification skill** — not just a new app
```

---

## Section 2.4: Beginner Summary (3 slides)

### Slide 2-16: 4 Core Beginner Lessons

**Plan ref:** Line 203 | **JP ref:** ~Line 1560

```markdown
---

## Section 2.4: Beginner Summary

# 4 Core Beginner Lessons

1. **Permission specs** — Who can do what → Scenario A
2. **Behavior specs** — What are the state transitions → Scenario J
3. **Output specs** — What to render (and what NOT to) → Scenario K
4. **Calculation specs** — What are the precision requirements → Scenario L

> 4 types of specification. 4 types of bugs prevented.
```

---

### Slide 2-17: Common Beginner Pitfalls

**Plan ref:** Line 204 | **JP ref:** ~Line 1575

```markdown
---

## Section 2.4: Beginner Summary

# Common Beginner Pitfalls

1. Permission checks **scattered across click handlers** (not centralized)
2. State machines become **`if/else` chains** (not explicit state transitions)
3. **"Render everything"** instead of whitelisting (XSS vulnerability)
4. **`parseFloat`** for fraction arithmetic (precision errors)

> Every pitfall is a **missing specification** that AI fills with its own assumptions
```

---

### Slide 2-18: Bridge to Intermediate

**Plan ref:** Line 205 | **JP ref:** ~Line 1590

```markdown
---

## Section 2.4: Beginner Summary

# Bridge to Intermediate

**Beginner:** client-side only → localStorage → no API

**Intermediate:** a server enters the picture

- API contracts become the center of your specs
- HTTP semantics matter (status codes, methods, headers)
- Databases replace localStorage
- Multiple consumers (browser, mobile, CLI) hit the same API

> How do specs change when there's a server? → **Chapter 3**
```

---

## ✅ Chapter 2 Quality Checks

- [ ] Section divider for Chapter 2 present (unnumbered)
- [ ] 18 numbered slides (2-1 through 2-18)
- [ ] QuickRetro walkthrough covers all 6 SDD phases (slides 2-5 through 2-9)
- [ ] Permission matrix table present (slide 2-10)
- [ ] "Aha moment" — self-voting question deeply explored (slide 2-8)
- [ ] Each scenario (J, K, L) has its own slide with SDD lesson
- [ ] `parseFloat` trap code example present (slide 2-14)
- [ ] Progression table shows skill build-up (slide 2-15)
- [ ] Bridge slide transitions to Chapter 3 (slide 2-18)
- [ ] All h2 labels: `## Section 2.1`, `## Section 2.2`, `## Section 2.3`, `## Section 2.4`
- [ ] No Japanese text
- [ ] Content density within limits
