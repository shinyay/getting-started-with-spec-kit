# Workshop: Spec-Driven Development with Spec Kit

> **From idea to implementation in 90 minutes — without vibe coding.**

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shinyay/getting-started-with-spec-kit)

---

## Workshop Overview

| | |
|---|---|
| **Duration** | 90 minutes |
| **Level** | Beginner–Intermediate |
| **Audience** | Software developers, tech leads, engineering managers |
| **Format** | Hands-on, instructor-led |
| **Max Participants** | 30 (recommended) |

### What You Will Learn

- The principles of **Spec-Driven Development (SDD)** and how it differs from ad-hoc "vibe coding"
- How to use the **Spec Kit** toolkit and `specify` CLI to create structured, executable specifications
- The full SDD lifecycle: Constitution → Specify → Clarify → Plan → Tasks → Implement
- How AI agents produce dramatically better results when guided by specifications

### What You Will Build

**QuickRetro** — a lightweight team retrospective board where team members can add cards, vote, and track action items across retro sessions.

---

## Prerequisites

- A **GitHub account** (with access to GitHub Codespaces)
- Basic familiarity with **Git** and a code editor
- A general understanding of **web application** concepts

> [!NOTE]
> No local installation is required. Everything runs inside a pre-configured Dev Container on GitHub Codespaces.

---

## Part 1: Setup & Context [15 min]

### 1.1 Why Spec-Driven Development?

Traditional development often follows an improvised pattern — start coding from a vague idea, fix problems as they appear, and end up with software that drifts from original intent. This is sometimes called **"vibe coding."**

**Spec-Driven Development flips this:** specifications become the primary artifact, and code becomes their expression. Instead of coding first and documenting later, you specify first and generate implementation from that specification.

| Vibe Coding | Spec-Driven Development |
|---|---|
| Start coding from a rough idea | Start with structured specifications |
| Discover edge cases during implementation | Discover edge cases during specification |
| Documentation is an afterthought | Specification IS the documentation |
| Difficult to pivot or re-implement | Pivot by updating specs and regenerating |
| Intent gets lost in code | Intent is preserved in specifications |

### 1.2 Launch Your Environment

1. Click the **"Open in GitHub Codespaces"** badge at the top of this page
2. Wait for the Dev Container to build (~2–3 minutes)
3. Once the terminal is ready, verify the setup:

```bash
specify check
```

You should see confirmation that `specify`, `uv`, `git`, `python`, and `node` are installed.

### 1.3 Initialize Spec Kit

```bash
specify init . --ai copilot --force
```

This scaffolds the `.specify/` directory with templates, scripts, and configuration for GitHub Copilot as your AI agent.

> [!TIP]
> After initialization, open **GitHub Copilot Chat** in VS Code (Ctrl+Shift+I or Cmd+Shift+I). You should see the `/speckit.*` slash commands available.

---

## Part 2: Establish Your Constitution [10 min]

The **constitution** defines your project's governing principles — the non-negotiable rules that guide all subsequent development. Think of it as the "architectural DNA" of your project.

### Why This Matters

Without a constitution, AI agents make their own assumptions about code quality, testing, and architecture. A constitution ensures consistency and prevents over-engineering.

### Hands-On

In Copilot Chat, run:

```
/speckit.constitution Create principles for a lightweight web application focused on simplicity, readability, and maintainability. Prioritize minimal dependencies, clear separation of concerns, comprehensive test coverage, and accessible UI. The application should work without a build step where possible. Avoid over-engineering — no abstractions until the third use case demands it.
```

### ✅ Checkpoint

Review the generated `.specify/memory/constitution.md` file. Verify that it includes:

- [ ] Code quality and simplicity guidelines
- [ ] Testing expectations
- [ ] Architectural constraints (minimal dependencies, no premature abstraction)
- [ ] UI/UX principles

> [!TIP]
> The constitution is YOUR document. If the AI generated something you disagree with, edit it directly or ask the AI to revise it. This is not a one-shot exercise.

---

## Part 3: Define Your Specification [20 min]

This is the most critical phase of SDD. You will describe **what** you want to build and **why**, without specifying **how**.

### The QuickRetro Concept

QuickRetro is a team retrospective board. Teams use it after a sprint or project milestone to reflect on what happened. The key elements:

- **Retro sessions** with a title and date
- **Three columns**: 🟢 Went Well, 🟡 To Improve, 🔵 Action Items
- **Cards** that team members add to each column
- **Voting** to surface the most important items
- **Pre-defined team members** (no authentication in this version)

### Hands-On

In Copilot Chat, run:

```
/speckit.specify Build QuickRetro, a team retrospective board application. When the app launches, it displays a list of pre-defined team members (4 people: two engineers, one designer, one product manager) to select from — no password required. After selecting a user, you see a list of retro sessions. Clicking a session opens the retro board with three columns: "Went Well," "To Improve," and "Action Items." Any team member can add cards to any column. Cards show the author name and creation time. Each team member can vote once per card using a thumbs-up button — you cannot vote on your own card. Cards are sorted by vote count (highest first) within each column. You can only edit or delete cards you created. Action Item cards have an additional "Mark Complete" checkbox that anyone can toggle. There should be 2 sample retro sessions pre-loaded with 3-5 cards each, distributed across all columns.
```

### What to Observe

After the command runs, examine the generated specification:

1. **Branch**: A feature branch like `001-quick-retro` should be created
2. **Spec file**: `specs/001-quick-retro/spec.md` should contain:
   - User stories with acceptance criteria
   - Functional requirements
   - `[NEEDS CLARIFICATION]` markers for ambiguous areas
   - A review and acceptance checklist

### 🤔 Discussion Point

Look at what the AI captured vs. what it flagged as unclear. Some deliberate ambiguities in the prompt above:

- Can a user create new retro sessions, or are they admin-only?
- What happens when all action items are marked complete?
- Is there a limit on card length or comment count?
- Are votes anonymous to other users?
- Can you reopen a "completed" retro session?

These are exactly the kinds of questions that **vibe coding misses** and **SDD surfaces early**.

---

## Part 4: Clarify the Specification [15 min]

Now we refine. This step is where SDD delivers its highest ROI — catching ambiguity **before** a single line of code is written.

### 4.1 Structured Clarification

In Copilot Chat, run:

```
/speckit.clarify
```

The AI will ask you a series of targeted questions about gaps in the specification. Answer them thoughtfully. Suggested answers for the workshop:

| Question Theme | Suggested Answer |
|---|---|
| Session creation | Any team member can create a new retro session |
| Card length | Maximum 280 characters per card |
| Completed retros | Sessions can be archived but not deleted |
| Vote visibility | Votes are visible (show who voted) |
| Concurrent editing | Last-write-wins, no real-time sync needed for v1 |

### 4.2 Manual Refinement

After the structured clarification, add any details the AI missed:

```
For the pre-loaded sample data: create one retro titled "Sprint 23 Retro" and another titled "Q4 Planning Retro." Distribute sample cards across all three columns with varied vote counts so the sorting is visible. Ensure at least one action item is already marked as complete in the sample data.
```

### 4.3 Validate the Checklist

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

### ✅ Checkpoint

Your specification should now have:

- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] Clear user stories with testable acceptance criteria
- [ ] Sample data requirements defined
- [ ] Edge cases explicitly addressed

---

## Part 5: Create the Implementation Plan [15 min]

Now — and only now — do we talk about technology. The specification is stable; it's time to decide **how** to build it.

### Hands-On

In Copilot Chat, run:

```
/speckit.plan Use vanilla HTML, CSS, and JavaScript with no build tools or frameworks. Store all data in the browser using localStorage. The app should be a single index.html file with linked CSS and JS files. Keep it simple — no bundlers, no transpilers, no package managers needed for the frontend.
```

### What Gets Generated

Review the output artifacts in your `.specify/specs/001-quick-retro/` directory:

| File | Purpose |
|---|---|
| `plan.md` | High-level implementation plan with phases |
| `data-model.md` | Data structures for sessions, cards, votes |
| `research.md` | Technical research (localStorage limits, drag-drop APIs) |
| `quickstart.md` | Key validation scenarios |

### Validate the Plan

Ask the AI to audit itself:

```
Review the implementation plan and check: (1) Are there any over-engineered components that violate our constitution's simplicity principle? (2) Does every technical choice trace back to a requirement in the spec? (3) Is the phase ordering logical — can each phase be validated independently?
```

> [!WARNING]
> AI agents tend to over-engineer. Watch for unnecessary abstractions, excess libraries, or "future-proofing" that nobody asked for. Push back if you see it.

### ✅ Checkpoint

- [ ] Tech stack matches what you specified (vanilla HTML/CSS/JS + localStorage)
- [ ] No unnecessary dependencies or abstractions
- [ ] Data model covers all entities: sessions, cards, users, votes

---

## Part 6: Generate Task Breakdown [5 min]

Convert the plan into an ordered, executable task list.

### Hands-On

In Copilot Chat, run:

```
/speckit.tasks
```

### What to Observe in `tasks.md`

- **Tasks grouped by user story** — each user story becomes an implementation phase
- **Dependency ordering** — data models before services, services before UI
- **`[P]` markers** — tasks that can run in parallel
- **File paths** — each task specifies exactly which files to create or modify
- **Checkpoints** — validation steps between phases

### 🤔 Discussion Point

Compare this structured task breakdown to how you would normally start coding. With SDD, every task has:
1. A clear scope (what to do)
2. A traceable origin (which user story)
3. An explicit order (what comes first)
4. Validation criteria (how to know it's done)

---

## Part 7: Implement [10 min]

Start the implementation. In a workshop setting, we will observe the process rather than wait for full completion.

### Hands-On

In Copilot Chat, run:

```
/speckit.implement
```

### What Happens

The AI agent will:
1. Validate that all prerequisites exist (constitution, spec, plan, tasks)
2. Parse the task breakdown from `tasks.md`
3. Begin executing tasks in order, creating files, writing code
4. Follow the test-driven approach defined in your task plan

### What to Watch For

- The AI follows the **task order** from `tasks.md`, not its own improvised order
- Generated code references back to **spec requirements**
- The data model matches what was defined in `data-model.md`
- No features are added that weren't in the specification

> [!NOTE]
> Full implementation may take 10–30 minutes depending on complexity. For this workshop, observe the first few tasks being implemented, then we will discuss the results.

---

## Wrap-Up & Discussion [10 min]

### What We Accomplished

In ~80 minutes, we went from a blank project to:

1. ✅ **Constitution** — governing principles for consistent development
2. ✅ **Specification** — complete, unambiguous requirements with user stories
3. ✅ **Clarifications** — edge cases and ambiguities resolved before coding
4. ✅ **Implementation Plan** — tech stack decisions with documented rationale
5. ✅ **Task Breakdown** — ordered, executable tasks with dependencies
6. ✅ **Implementation** — code generated from specifications, not from vibes

### Key Takeaways

1. **Specs catch bugs before they exist.** The clarification step surfaces edge cases that would otherwise become production bugs.
2. **AI works dramatically better with structure.** Compare the output quality of a guided `/speckit.specify` to a simple "build me a retro board" prompt.
3. **Pivoting becomes cheap.** Want to rebuild QuickRetro in React? Change the plan, regenerate tasks, re-implement. The spec stays the same.
4. **The spec is the source of truth.** Code can be regenerated; intent cannot. Preserving intent in specifications makes software maintainable.

### Discussion Questions

- How would you adapt SDD to your current team's workflow?
- What types of projects benefit most from SDD? Where might it be overkill?
- How does SDD change the role of code review?
- What happens when the AI generates code that doesn't match the spec?

---

## Bonus: Extension Activities

If you finish early or want to continue after the workshop:

### Extension 1: Add a Feature

Add a new feature to QuickRetro using the SDD workflow:

```
/speckit.specify Add a "Timer" feature to QuickRetro. When a retro session is active, the facilitator can start a countdown timer (configurable: 5, 10, or 15 minutes) that is visible to all participants. When the timer expires, a notification appears. The timer is per-column — the facilitator advances through columns with the timer.
```

Then continue through `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Extension 2: Rebuild with a Different Tech Stack

Keep the same specification but create a new implementation plan with a different stack:

```
/speckit.plan Rebuild QuickRetro using React with TypeScript. Use Vite as the build tool. Store data in a local SQLite database via sql.js (WASM). Create a component-based architecture with proper state management using React Context.
```

This demonstrates SDD's tech independence — the same spec produces different implementations.

### Extension 3: Cross-Artifact Analysis

Run the optional analysis command to check consistency:

```
/speckit.analyze
```

This validates that your spec, plan, and tasks are aligned with no gaps or contradictions.

---

## Facilitator Guide

### Before the Workshop

- [ ] Test the Codespace build yourself (ensure no Docker/build issues)
- [ ] Create a Codespace and run through the full flow at least once
- [ ] Prepare reference outputs for each step (spec.md, plan.md, tasks.md) as fallback
- [ ] Ensure participants have GitHub accounts with Codespaces access
- [ ] Have a backup plan for network issues (screenshots of expected outputs)

### Timing Tips

| Phase | Time | Buffer | Notes |
|---|---|---|---|
| Setup & Context | 15 min | +5 min | Codespace build is the bottleneck; start this first, present slides while waiting |
| Constitution | 10 min | +3 min | Quick step; don't let participants over-optimize |
| Specification | 20 min | +5 min | Core phase; allow time for reading and discussion |
| Clarification | 15 min | +5 min | High-value phase; encourage participants to answer differently and compare |
| Plan | 15 min | +5 min | Watch for over-engineering; guide participants to push back |
| Tasks | 5 min | — | Fast step; focus on reading the output |
| Implementation | 10 min | — | Observation phase; don't wait for full completion |
| Wrap-Up | 10 min | — | Reserve this time; the discussion is essential |

### Common Issues & Solutions

| Issue | Solution |
|---|---|
| Codespace takes >5 min to build | Have participants start setup immediately; present context slides while waiting |
| `specify` command not found | Run: `uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git` |
| Slash commands not visible in Copilot | Re-run `specify init . --ai copilot --force`; restart Copilot Chat |
| AI generates overly complex plan | Prompt: "Simplify this plan. Remove any frameworks or libraries not explicitly requested." |
| Participants at different speeds | Fast finishers → Extension activities. Slow finishers → Skip to `/speckit.tasks` with facilitator-provided plan |
| AI output differs between participants | This is expected and a teaching moment. Compare outputs to discuss how AI interprets ambiguity. |

### Key Teaching Moments

1. **After Step 3 (Specify):** Ask participants to compare their generated specs. Differences highlight why specification matters — same prompt, different interpretations.
2. **After Step 4 (Clarify):** Have 2–3 participants share the most surprising question the AI asked. This demonstrates the value of structured clarification.
3. **After Step 5 (Plan):** Ask if anyone's plan includes something they didn't request. Use this to discuss AI over-engineering and the importance of constitution constraints.

---

## References

- [Spec Kit Repository](https://github.com/github/spec-kit)
- [Spec-Driven Development Methodology](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [Spec Kit Video Overview](https://www.youtube.com/watch?v=a9eR1xsfvHg)
- [Dev Containers Specification](https://containers.dev/)
