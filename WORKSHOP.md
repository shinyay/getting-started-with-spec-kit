# Workshop: Spec-Driven Development with Spec Kit

> **From idea to implementation — without vibe coding.**

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/shinyay/getting-started-with-spec-kit)

---

## Workshop Overview

| | |
|---|---|
| **Duration** | 90–120 minutes (varies by scenario) |
| **Level** | Beginner–Advanced |
| **Audience** | Software developers, tech leads, engineering managers |
| **Format** | Hands-on, instructor-led |
| **Max Participants** | 30 (recommended) |

### What You Will Learn

- The principles of **Spec-Driven Development (SDD)** and how it differs from ad-hoc "vibe coding"
- How to use the **Spec Kit** toolkit and `specify` CLI to create structured, executable specifications
- The full SDD lifecycle: Constitution → Specify → Clarify → Plan → Tasks → Implement
- How AI agents produce dramatically better results when guided by specifications

---

## Scenarios

Choose a scenario based on your experience level and interests. Each scenario provides complete prompts for every SDD phase.

| | Scenario | Level | Duration | Key SDD Themes |
|---|---|---|---|---|
| **A** | [QuickRetro — Team Retrospective Board](scenarios/A-quick-retro.md) | ⭐ Beginner | ~90 min | CRUD, permissions, voting logic |
| **B** | [Field Inspection PWA — Offline-first](scenarios/B-field-inspection-pwa.md) | ⭐⭐⭐ Intermediate–Advanced | ~120 min | Offline-first, sync conflicts, media uploads |
| **C** | [OIDC SSO + RBAC — Brownfield Auth](scenarios/C-oidc-sso-rbac.md) | ⭐⭐⭐ Intermediate–Advanced | ~120 min | Brownfield, security/auth, multi-tenancy |
| **D** | [Stripe Subscriptions + Dunning](scenarios/D-stripe-subscriptions.md) | ⭐⭐⭐ Intermediate–Advanced | ~120 min | Money correctness, idempotency, state machines |
| **E** | [Collaborative Whiteboard — Real-time](scenarios/E-collaborative-whiteboard.md) | ⭐⭐⭐⭐ Advanced | ~120 min | Concurrency, consistency models, latency budgets |
| **F** | [Event Ingestion Pipeline — IoT](scenarios/F-event-ingestion-pipeline.md) | ⭐⭐⭐⭐ Advanced | ~120 min | Data quality, schema evolution, backpressure, SLOs |

> [!TIP]
> Open your chosen scenario file alongside this guide. This page explains each SDD phase; the scenario file provides the specific prompts and checkpoints.

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

**Why this matters:** Without a constitution, AI agents make their own assumptions about code quality, testing, and architecture. A constitution ensures consistency and prevents over-engineering.

👉 **Run the `/speckit.constitution` prompt from your [scenario file](#scenarios).**

> [!TIP]
> The constitution is YOUR document. If the AI generated something you disagree with, edit it directly or ask the AI to revise it. This is not a one-shot exercise.

---

## Part 3: Define Your Specification [15–20 min]

This is the most critical phase of SDD. You will describe **what** you want to build and **why**, without specifying **how**.

**Why this matters:** A well-written specification forces you to think about requirements, user stories, and edge cases before writing any code. The AI will generate structured user stories and flag ambiguities with `[NEEDS CLARIFICATION]` markers.

👉 **Run the `/speckit.specify` prompt from your [scenario file](#scenarios).**

After the command runs, examine the generated specification:

1. **Branch**: A feature branch should be created automatically
2. **Spec file**: The `spec.md` should contain user stories, functional requirements, ambiguity markers, and a review checklist

### 🤔 Discussion Point

Look at what the AI captured vs. what it flagged as unclear. These are exactly the kinds of questions that **vibe coding misses** and **SDD surfaces early**. In a traditional workflow, these ambiguities become production bugs.

---

## Part 4: Clarify the Specification [10–15 min]

Now we refine. This step is where SDD delivers its highest ROI — catching ambiguity **before** a single line of code is written.

**Why this matters:** The `/speckit.clarify` command asks structured, coverage-based questions about gaps in your specification. Every ambiguity resolved here is a bug that will never exist.

👉 **Run the `/speckit.clarify` prompt from your [scenario file](#scenarios).** Use the suggested answers provided, or answer with your own decisions.

After structured clarification, validate the acceptance checklist:

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

---

## Part 5: Create the Implementation Plan [15–20 min]

Now — and only now — do we talk about technology. The specification is stable; it's time to decide **how** to build it.

**Why this matters:** Separating "what" from "how" means your specification survives technology changes. Want to rebuild with a different framework? Change the plan, keep the spec.

�� **Run the `/speckit.plan` prompt from your [scenario file](#scenarios).**

After the plan is generated, ask the AI to audit itself:

```
Review the implementation plan and check: (1) Are there any over-engineered components that violate our constitution's simplicity principle? (2) Does every technical choice trace back to a requirement in the spec? (3) Is the phase ordering logical — can each phase be validated independently?
```

> [!WARNING]
> AI agents tend to over-engineer. Watch for unnecessary abstractions, excess libraries, or "future-proofing" that nobody asked for. Push back if you see it.

---

## Part 6: Generate Task Breakdown [5–10 min]

Convert the plan into an ordered, executable task list.

👉 **Run the `/speckit.tasks` prompt from your [scenario file](#scenarios).**

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

## Part 7: Implement [10–15 min]

Start the implementation. In a workshop setting, we will observe the process rather than wait for full completion.

In Copilot Chat, run:

```
/speckit.implement
```

The AI agent will:
1. Validate that all prerequisites exist (constitution, spec, plan, tasks)
2. Parse the task breakdown from `tasks.md`
3. Begin executing tasks in order, creating files, writing code
4. Follow the test-driven approach defined in your task plan

**What to watch for:**
- The AI follows the **task order** from `tasks.md`, not its own improvised order
- Generated code references back to **spec requirements**
- The data model matches what was defined in `data-model.md`
- No features are added that weren't in the specification

👉 **Check your [scenario file](#scenarios) for scenario-specific things to watch during implementation.**

> [!NOTE]
> Full implementation may take 10–30+ minutes depending on scenario complexity. For this workshop, observe the first few tasks being implemented, then we will discuss the results.

---

## Wrap-Up & Discussion [10 min]

### What We Accomplished

From a blank project, we produced six interconnected artifacts through the SDD lifecycle:

1. ✅ **Constitution** — governing principles for consistent development
2. ✅ **Specification** — complete, unambiguous requirements with user stories
3. ✅ **Clarifications** — edge cases and ambiguities resolved before coding
4. ✅ **Implementation Plan** — tech stack decisions with documented rationale
5. ✅ **Task Breakdown** — ordered, executable tasks with dependencies
6. ✅ **Implementation** — code generated from specifications, not from vibes

### Key Takeaways

1. **Specs catch bugs before they exist.** The clarification step surfaces edge cases that would otherwise become production bugs.
2. **AI works dramatically better with structure.** Compare the output quality of a guided `/speckit.specify` to a simple "build me an app" prompt.
3. **Pivoting becomes cheap.** Want to rebuild with a different tech stack? Change the plan, regenerate tasks, re-implement. The spec stays the same.
4. **The spec is the source of truth.** Code can be regenerated; intent cannot. Preserving intent in specifications makes software maintainable.

### Discussion Questions

- How would you adapt SDD to your current team's workflow?
- What types of projects benefit most from SDD? Where might it be overkill?
- How does SDD change the role of code review?
- What happens when the AI generates code that doesn't match the spec?

👉 **Check your [scenario file](#scenarios) for extension activities to continue after the workshop.**

---

## Cross-Artifact Analysis (All Scenarios)

After completing any scenario, run the optional consistency check:

```
/speckit.analyze
```

This validates that your spec, plan, and tasks are aligned with no gaps or contradictions.

---

## Facilitator Guide

### Before the Workshop

- [ ] Test the Codespace build yourself (ensure no Docker/build issues)
- [ ] Create a Codespace and run through the full flow at least once **for each scenario you plan to use**
- [ ] Prepare reference outputs for each step (spec.md, plan.md, tasks.md) as fallback
- [ ] Ensure participants have GitHub accounts with Codespaces access
- [ ] Have a backup plan for network issues (screenshots of expected outputs)
- [ ] Decide which scenario(s) to offer based on audience level

### Scenario Selection Guide

| Audience | Recommended Scenario |
|---|---|
| First-time SDD learners, mixed experience levels | **Scenario A** (QuickRetro) |
| Experienced developers, want a real-world challenge | **Scenario B** (Field Inspection PWA) or **C** (OIDC SSO) |
| Mixed audience | Let participants self-select; pair beginners together on A |
| Conference talk (tight time) | **Scenario A** only (fits 90 min) |
| Half-day workshop (3+ hours) | Multiple scenarios sequentially — A first, then harder ones |

### Timing Tips

**Scenario A (QuickRetro) — 90 minutes:**

| Phase | Time | Buffer | Notes |
|---|---|---|---|
| Setup & Context | 15 min | +5 min | Codespace build is the bottleneck; start this first, present slides while waiting |
| Constitution | 10 min | +3 min | Quick step; don't let participants over-optimize |
| Specification | 15 min | +5 min | Core phase; allow time for reading and discussion |
| Clarification | 10 min | +5 min | High-value phase; encourage participants to answer differently and compare |
| Plan | 15 min | +5 min | Watch for over-engineering; guide participants to push back |
| Tasks | 5 min | — | Fast step; focus on reading the output |
| Implementation | 10 min | — | Observation phase; don't wait for full completion |
| Wrap-Up | 10 min | — | Reserve this time; the discussion is essential |

**Scenario B (Field Inspection PWA) — 120 minutes:**

| Phase | Time | Buffer | Notes |
|---|---|---|---|
| Setup & Context | 15 min | +5 min | Same as Scenario A |
| Constitution | 10 min | +3 min | Constitution is longer; allow time to read the offline-first principles |
| Specification | 20 min | +5 min | Complex domain; participants may need to re-read the prompt |
| Clarification | 15 min | +5 min | **Highest-value phase for this scenario** — sync/conflict questions are eye-opening |
| Plan | 20 min | +5 min | Most complex phase; lots of generated artifacts to review |
| Tasks | 10 min | +3 min | Task list is long; focus on dependency ordering and the golden-path task |
| Implementation | 15 min | — | Observe service worker and sync engine tasks being created |
| Wrap-Up | 15 min | — | Rich discussion — offline-first is a great topic for debate |

**Scenario C (OIDC SSO + RBAC) — 120 minutes:**

| Phase | Time | Buffer | Notes |
|---|---|---|---|
| Setup & Context | 15 min | +5 min | Same as other scenarios |
| Constitution | 10 min | +3 min | Security principles are dense; ensure participants read the fail-closed and tenant isolation rules |
| Specification | 20 min | +5 min | Auth specs are long; focus on the identity-linking and logout sections |
| Clarification | 15 min | +5 min | Security edge cases dominate; the secret rotation and impersonation questions are eye-opening |
| Plan | 20 min | +5 min | Threat model section is unique to this scenario; ensure participants review it |
| Tasks | 10 min | +3 min | Look for the "attack mindset" and "canary tenant" tasks |
| Implementation | 15 min | — | Watch for RBAC middleware, migration rollback scripts, and secret handling |
| Wrap-Up | 15 min | — | Discussion: how does SDD change security-critical development? |

**Scenario D (Stripe Subscriptions) — 120 minutes:**

| Phase | Time | Buffer | Notes |
|---|---|---|---|
| Setup & Context | 15 min | +5 min | Same as other scenarios |
| Constitution | 10 min | +3 min | Focus on correctness-over-speed and fail-safe access principles |
| Specification | 20 min | +5 min | State machine is the core — ensure participants understand all transitions |
| Clarification | 15 min | +5 min | Proration and dunning timeline questions are critical; financial edge cases are eye-opening |
| Plan | 20 min | +5 min | Webhook architecture (async queue, deduplication) is the most technical section |
| Tasks | 10 min | +3 min | Look for "financial correctness" and "reconciliation verification" tasks |
| Implementation | 15 min | — | Watch for idempotency keys, integer cents, and entitlement middleware |
| Wrap-Up | 15 min | — | Discussion: how does SDD prevent billing bugs that cost real money? |

**Scenario E (Collaborative Whiteboard) — 120 minutes:**

| Phase | Time | Buffer | Notes |
|---|---|---|---|
| Setup & Context | 15 min | +5 min | Same as other scenarios |
| Constitution | 10 min | +3 min | Latency budgets and convergence guarantees are the key principles to verify |
| Specification | 20 min | +5 min | Object types and conflict rules per type are dense; ensure participants understand the differences |
| Clarification | 15 min | +5 min | Text-editing locking vs merging is the pivotal decision; undo stack persistence sparks good debate |
| Plan | 20 min | +5 min | Consistency model choice (authoritative server vs CRDT) is the most important architectural discussion |
| Tasks | 10 min | +3 min | Look for the "vertical slice" task and separation of rendering vs sync tracks |
| Implementation | 15 min | — | Watch for message schema defined before WebSocket code; Canvas rendering decoupled from networking |
| Wrap-Up | 15 min | — | Discussion: how would switching to CRDTs change the spec and plan? |

**Scenario F (Event Ingestion Pipeline) — 120 minutes:**

| Phase | Time | Buffer | Notes |
|---|---|---|---|
| Setup & Context | 15 min | +5 min | Same as other scenarios |
| Constitution | 10 min | +3 min | "No silent data loss" and cost awareness are the defining principles |
| Specification | 20 min | +5 min | Throughput numbers and SLOs are concrete — verify participants understand the dual-layer storage |
| Clarification | 15 min | +5 min | Late-arriving events, batch semantics, and cost constraints produce the most insight |
| Plan | 20 min | +5 min | Kafka topic design and backpressure at each boundary are the critical architecture sections |
| Tasks | 10 min | +3 min | Happy-path-first ordering is key; look for load test tasks with specific throughput targets |
| Implementation | 15 min | — | Watch for schema validation at ingestion, Parquet batching, and 429 backpressure responses |
| Wrap-Up | 15 min | — | Discussion: how does SDD prevent silent data loss in distributed pipelines? |

### Common Issues & Solutions

| Issue | Solution |
|---|---|
| Codespace takes >5 min to build | Have participants start setup immediately; present context slides while waiting |
| `specify` command not found | Run: `uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git` |
| Slash commands not visible in Copilot | Re-run `specify init . --ai copilot --force`; restart Copilot Chat |
| AI generates overly complex plan | Prompt: "Simplify this plan. Remove any frameworks or libraries not explicitly requested." |
| Participants at different speeds | Fast finishers → Extension activities in scenario file. Slow finishers → Skip to `/speckit.tasks` with facilitator-provided plan |
| AI output differs between participants | This is expected and a teaching moment. Compare outputs to discuss how AI interprets ambiguity. |
| Scenario seems too complex for audience | Fall back to Scenario A; use the harder scenario as a demo-only walkthrough |

### Key Teaching Moments

1. **After Part 3 (Specify):** Ask participants to compare their generated specs. Differences highlight why specification matters — same prompt, different interpretations.
2. **After Part 4 (Clarify):** Have 2–3 participants share the most surprising question the AI asked. This demonstrates the value of structured clarification.
3. **After Part 5 (Plan):** Ask if anyone's plan includes something they didn't request. Use this to discuss AI over-engineering and the importance of constitution constraints.
4. **After Part 6 (Tasks):** Ask a participant to pick one task and trace it back through the plan to the spec. This demonstrates full traceability — the core SDD value proposition.

---

## References

- [Spec Kit Repository](https://github.com/github/spec-kit)
- [Spec-Driven Development Methodology](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [Spec Kit Video Overview](https://www.youtube.com/watch?v=a9eR1xsfvHg)
- [Dev Containers Specification](https://containers.dev/)
