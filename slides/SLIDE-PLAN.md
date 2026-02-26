# 📊 Spec Kit Presentation — English Slide Design Plan

> **Ultra-Detailed Edition — Stop vibe coding. Start specifying.**

---

## 🎯 Presentation Overview

| Item | Details |
|------|---------|
| **Title** | Introduction to Spec-Driven Development (SDD) — Building Better Software in the AI Era with GitHub Spec Kit |
| **Subtitle** | Stop vibe coding. Start specifying. |
| **Target Audience** | Beginner to advanced engineers (all levels) |
| **Language** | English |
| **Marp Theme** | `github-dark` (custom theme) |
| **Estimated Duration** | 60–90 minutes (full version) |
| **Slide Format** | Marp Markdown (`---` slide separators) |
| **Presenter** | Shinya Yanagihara (`@shinyay`), Developer Global BlackBelt, Microsoft Corporation |

---

## 📐 Overall Structure: 7 Chapters

```
Chapter 0: Title & Introduction                        [   5 slides ]
Chapter 1: General — SDD Overview & Spec Kit           [  51 slides ]
Chapter 2: Beginner — SDD Workflow Fundamentals        [  18 slides ]
Chapter 3: Intermediate — Server-Side & API Contracts  [  16 slides ]
Chapter 4: Intermediate–Advanced — Real-World Complexity [ 16 slides ]
Chapter 5: Advanced — Distributed Systems & Failure Models [ 18 slides ]
Chapter 6: Summary & Next Steps                        [   7 slides ]
─────────────────────────────────────────────────────────────────────
Total:                                                  ~131 slides
```

---

## 🏗️ Chapter-by-Chapter Slide Design

---

### Chapter 0: Title & Introduction (5 slides)

**Purpose:** Hook the audience and present the presentation's overall structure.

| # | Slide Title | Content | Design Notes |
|---|---|---|---|
| 0-1 | **Introduction to Spec-Driven Development (SDD)** | Main title + subtitle "Building Better Software in the AI Era with GitHub Spec Kit" + presenter `@shinyay` + date | Title slide (`section:first-of-type` CSS applied) |
| 0-2 | **Today's Agenda** | Visual display of 6 chapters. Each chapter with difficulty icon (⭐–⭐⭐⭐⭐) and duration | Chapter list |
| 0-3 | **Who Is This Presentation For?** | 3 personas: **Beginners** ("I let AI write code, but things keep breaking…"), **Intermediate** ("How should I design API contracts?"), **Advanced** ("How do I write specs for distributed systems?") | 3-group bulleted layout |
| 0-4 | **Prerequisites by Chapter** | Matrix table: Beginner = none, Intermediate = Node.js basics, Int-Adv = external API experience, Advanced = distributed systems fundamentals | Table |
| 0-5 | **Hands-On Environment** | GitHub Codespaces badge, QR code, `specify init . --ai copilot` command | Setup instructions |

---

### Chapter 1: General — SDD Overview & Spec Kit (51 slides)

**Purpose:** Convey the SDD concept, background, and significance to all audience levels. Cover Spec Kit from installation to CLI operations, directory structure, and command system. Prepare everyone for hands-on practice.

#### Section 1.1: The Problem — Limits of Vibe Coding (6 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 1-1 | **What Is Vibe Coding?** | Definition: "Giving AI a rough idea and accepting whatever it produces." Concrete example: "Build me a chat app" → AI unilaterally decides DB design, auth model, error handling, permissions | Set up the problem with a relatable "been there" feeling |
| 1-2 | **The 4 Failure Patterns of Vibe Coding** | (1) AI decides permission rules without asking, (2) Edge cases become production bugs, (3) Over-engineered tech stack, (4) Intent buried in code — unmaintainable | Each pattern with a concrete example icon |
| 1-3 | **"Build Me an App" — The Results** | Before/After comparison: Vibe coding output (unpredictable) vs SDD output (predictable). Same prompt, dramatically different AI output quality when specs exist | Comparison table |
| 1-4 | **AI Works Dramatically Better with Structure** | Vague prompt → AI guesses → bugs. Structured spec → AI follows → predictable, high-quality output. "AI is an excellent implementer, but not an excellent designer." | Arrow-style bulleted flow |
| 1-5 | **Question: What's Your Development Flow?** | Discussion prompt: "When you have AI write code, how much specification do you write beforehand?" | Interactive question slide |
| 1-6 | **Why SDD Matters NOW — 3 Trends** | (1) AI capabilities have reached a threshold for reliable code generation from specs, (2) Software complexity grows exponentially — alignment through specs, (3) Pace of change accelerates — pivoting requires specs, not manual propagation | From `spec-driven.md` |

#### Section 1.2: SDD Principles & the 6 Phases (10 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 1-7 | **What Is Spec-Driven Development?** | Definition: "Write structured specifications first, then AI follows them — producing predictable, high-quality output every time." Key message: **The spec is the primary artifact; code is its expression.** | Large key message |
| 1-8 | **The Power Inversion — SDD's Core Insight** | "For decades, code was king. Specs served code. SDD inverts this: code serves specifications." Specs don't guide implementation — they *generate* it. The gap between spec and implementation is eliminated, not narrowed. "Intent-driven development" — the lingua franca moves to a higher level. | From `spec-driven.md`. Bold conceptual slide |
| 1-9 | **The 6 Phases of SDD (Overview)** | `Constitution → Specify → Clarify → Plan → Tasks → Implement` — numbered flow with one-line descriptions per phase | Flow-style list |
| 1-10 | **Phase 1: Constitution** | "Define project principles and constraints" — the project's DNA. Without a constitution, AI makes its own assumptions. Examples: "Test coverage ≥80%", "Minimize external dependencies" | With concrete examples |
| 1-11 | **Phase 2: Specify** | "Describe what to build (not how)" — user stories, acceptance criteria, intentional `[NEEDS CLARIFICATION]` markers. Specs are technology-independent | With concrete examples |
| 1-12 | **Phase 3: Clarify** ⭐ SDD's True Value | "Surface hidden assumptions and edge cases" — **This is where SDD delivers the greatest ROI.** Catches ambiguity before a single line of code is written. Examples: "Can users vote on their own posts?", "What state on timeout?" | ⭐ marked, emphasize "SDD's true value is here" |
| 1-13 | **Phase 4: Plan** | "Choose architecture and technology" — technology discussion happens only now. Separating "what" from "how" means specs survive technology changes. Example: "Switching React → Vue doesn't change the spec." Research agents can investigate library compatibility, performance benchmarks, and security implications. Organizational constraints integrate automatically | With concrete example. Research agents concept from `spec-driven.md` |
| 1-14 | **Phase 5: Tasks** | "Break down into executable steps" — each task has: (1) clear scope, (2) traceable origin (user story), (3) explicit ordering, (4) validation criteria | Emphasize the 4 elements |
| 1-15 | **Phase 6: Implement** | "Generate code from specifications" — AI follows `tasks.md` ordering, references specs while coding. Does NOT add features not in the spec | Implementation observation points |
| 1-16 | **3 Development Modes** | (1) **0-to-1 (Greenfield)**: Generate from scratch, (2) **Creative Exploration**: Parallel implementations — experiment with diverse solutions, (3) **Iterative Enhancement (Brownfield)**: Add features, modernize legacy | From `spec-driven.md`. 3-mode comparison |

#### Section 1.3: GitHub Spec Kit — The Toolkit (6 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 1-17 | **What Is GitHub Spec Kit?** | GitHub's open-source SDD toolkit. Tagline: "Build high-quality software faster." Two pillars: (1) `specify` CLI — project setup & validation, (2) Copilot Chat `/speckit.*` slash commands — execute each SDD phase. Supports 20+ AI agents | Logo/badge + supported AI list |
| 1-18 | **Spec Kit's Two Pillars** | Pillar 1: `specify` CLI (Python, installed via `uv`) → project init, validation, versioning. Pillar 2: `.github/prompts/*.prompt.md` + `.github/agents/*.agent.md` → instruction files for AI agents to execute SDD phases in a structured manner | 2-column comparison |
| 1-19 | **Spec Kit Version Info** | CLI Version / Template Version / Runtime: Python 3.11+. Dev Container auto-pins version. How to specify version for local use | Version table |
| 1-20 | **Community & Adoption — 20+ Supported AI Agents** | Full agent support table: Copilot, Claude Code, Gemini CLI, Cursor, Codex, Windsurf, Qwen, opencode, Kilocode, Auggie, Roo, CodeBuddy, Amp, SHAI, Q, Bob, Qoder, Antigravity (agy), Jules, and Generic (bring your own agent) | Agent compatibility table |
| 1-21 | **📽️ Video Overview — See SDD in Action** | Official Spec Kit team video — full SDD walkthrough on a real project. Link: `youtube.com/watch?v=a9eR1xsfvHg`. Viewing timing table: After presentation → visual reinforcement, Before hands-on → grasp the full flow, Review → reconfirm phase connections. **Theory → Video → Hands-on — 3 steps to master SDD** | Video link + timing table |
| 1-22 | **Spec Kit Architecture Overview** | Diagram: `specify CLI` →(init)→ `.specify/` + `.github/` + `.vscode/` →(AI Agent)→ SDD artifacts (constitution, spec.md, plan.md, tasks.md) → implementation code. **CLI scaffolds the project → AI executes phases → specs drive code** | Architecture diagram |

#### Section 1.4: `specify` CLI — Installation & Basic Commands (5 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 1-23 | **Installing the `specify` CLI** | Method 1: Dev Container (recommended, pre-installed). Method 2: Local `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`. Prerequisites: Python 3.11+, uv, git, Node.js LTS | Installation commands (code block) |
| 1-24 | **3 CLI Commands** | `specify init` — initialize project (download templates + generate directories). `specify check` — verify required tool installations (git, AI tools, editor). `specify version` — show CLI/template version + system info | Command table |
| 1-25 | **`specify init` — Options in Detail** | `specify init <project_name> --ai <AI>` to create new directory. `specify init . --ai copilot --force` to initialize existing directory. `--ai` options: copilot, claude, gemini, cursor-agent, codex, windsurf, qwen, opencode, kilocode, auggie, roo, codebuddy, amp, shai, q, bob, qodercli, agy, generic. New: `--ai-skills` for Prompt.MD templates, `--script ps` for PowerShell, `--no-git` to skip Git init. `SPECIFY_FEATURE` env var for non-Git feature detection | Init options table |
| 1-26 | **`--ai generic` — Bring Your Own Agent** | `specify init my-project --ai generic --ai-commands-dir .myagent/commands/`. Comparison table: Normal agents → `specify check` validates / agent-specific directory / pre-defined config. Generic → no check needed / custom `--ai-commands-dir` / no config. **SDD is a process, not tied to any specific tool — technology independence proven** | Comparison table + code example |
| 1-27 | **`specify check` — Environment Diagnostics** | Example output (tree format): `● Git (available)` / `○ GitHub Copilot (IDE-based)` / `● Claude Code (not found)`. **See at a glance what's available.** Troubleshoot: if command not found, run `uv tool install specify-cli --force` | Screenshot-style recreation of `specify check` output |

#### Section 1.5: Directory Structure Generated by `specify init` (4 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 1-28 | **Project Structure After `specify init`** | Directory tree: `my-project/` → `.specify/` (scripts + templates), `.github/` (agents + prompts), `.vscode/` (settings). **Three directories form Spec Kit's scaffolding** | Tree diagram (code block) |
| 1-29 | **`.specify/` Directory — Scripts & Templates** | `scripts/bash/`: `check-prerequisites.sh`, `common.sh`, `create-new-feature.sh`, `setup-plan.sh`, `update-agent-context.sh`. `templates/`: `constitution-template.md`, `spec-template.md`, `plan-template.md`, `tasks-template.md`, `checklist-template.md`, `agent-file-template.md`. **Templates are the blueprints for SDD artifacts** | Two subdirectories in table format |
| 1-30 | **`.github/` Directory — AI Agents & Prompts** | `agents/` (9 files): `speckit.constitution.agent.md`, `speckit.specify.agent.md`, `speckit.clarify.agent.md`, `speckit.plan.agent.md`, `speckit.tasks.agent.md`, `speckit.implement.agent.md`, `speckit.analyze.agent.md`, `speckit.checklist.agent.md`, `speckit.taskstoissues.agent.md`. `prompts/` (9 files): matching `.prompt.md` files. **agent.md = agent mode, prompt.md = slash command** | File list (agents ↔ prompts correspondence table) |
| 1-31 | **`.vscode/settings.json` — VS Code Integration** | Generated settings: `chat.promptFilesRecommendations` (recommend speckit.* commands in Copilot Chat), `chat.tools.terminal.autoApprove` (auto-approve .specify/scripts/ terminal). **Just open VS Code and `/speckit.*` commands are ready** | JSON settings content |

#### Section 1.6: `/speckit.*` Command System — Full Reference (4 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 1-32 | **Core Commands (6) — Mapped to the 6 SDD Phases** | Table: (1) `/speckit.constitution` → Generate constitution, (2) `/speckit.specify` → Define spec + `[NEEDS CLARIFICATION]` markers, (3) `/speckit.clarify` → Ask and resolve ambiguities, (4) `/speckit.plan` → Architecture + data model, (5) `/speckit.tasks` → Task breakdown + ordering, (6) `/speckit.implement` → Generate code from specs. **Each command runs in Copilot Chat** (not the terminal) | 6-command table with phase numbers |
| 1-33 | **Optional Commands (3) — Quality Enhancement** | (1) `/speckit.clarify` (optional) — resolve ambiguity before Plan, (2) `/speckit.analyze` (optional) — cross-artifact consistency check after Tasks, (3) `/speckit.checklist` (optional) — generate quality checklist after Plan. **Core commands are required; optional commands enhance quality** | Core vs optional distinction table |
| 1-34 | **Recommended Execution Flow** | Flow: `/speckit.constitution` → `/speckit.specify` → (opt) `/speckit.clarify` → `/speckit.plan` → (opt) `/speckit.checklist` → `/speckit.tasks` → (opt) `/speckit.analyze` → `/speckit.implement`. + Special: `/speckit.taskstoissues` converts tasks.md to GitHub Issues | Flow diagram with branches |
| 1-35 | **3 Modes — prompt.md / agent.md / SKILL.md** | `prompt.md`: Execute as Copilot Chat slash command (`/speckit.specify`). `agent.md`: Use in Copilot Agent mode for long-running tasks. `SKILL.md`: New — install as agent skills with `--ai-skills` flag. **Same SDD phase, three execution modes.** Workshop uses slash commands (prompt.md) | Comparison table |

#### Section 1.7: SDD Artifacts — What Spec Kit Generates (5 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 1-36 | **SDD Artifact Overview & Relationship Diagram** | 6 interconnected artifacts: (1) `constitution.md` — project principles, (2) `spec.md` — defines What (user stories, acceptance criteria), (3) Clarifications — ambiguity resolution records, (4) `plan.md` + `data-model.md` — defines How (tech choices, DB design), (5) `tasks.md` — implementation task ordering, (6) Implementation code. **Each artifact references the previous one** | Relationship diagram (→ arrow list) |
| 1-37 | **Template Contents — Constitution Template Example** | Structure of `constitution-template.md`: `## Core Principles` → `### [PRINCIPLE_NAME]` + `[PRINCIPLE_DESCRIPTION]` placeholders. AI fills in content following the template. **Templates ensure quality and consistency** | Template excerpt (code block) |
| 1-38 | **The Constitution's 9 Articles — Immutable Architecture Principles** | Based on `spec-driven.md`: Simplicity gate, library-first, pure-function core, observability via CLI, single source of truth, test-first, modular by default, configuration over code, security by default. These are **immutable** — while implementation details evolve, core principles remain constant. 4 design philosophies: Modularity > Monoliths · Observability > Opacity · Simplicity > Cleverness · Integration > Isolation | Article list with descriptions |
| 1-39 | **7 Template Patterns That Constrain the LLM** | (1) What/How separation — no tech stack in Specify, (2) `[NEEDS CLARIFICATION]` — no guessing on ambiguity, (3) Checklists — no skipping self-review, (4) Phase -1 Gates — no over-complex designs, (5) Hierarchical detail management — no code in primary documents, (6) Test-first ordering — no implementation before tests, (7) No speculative features — no adding "nice to haves." **Templates = "unit tests for specifications"** | 7-pattern table |
| 1-40 | **SDD Artifact Flow — Live Demo Image** | Step diagram: ① `specify init . --ai copilot` → ② Copilot Chat `/speckit.constitution` → ③ `constitution.md` generated → ④ `/speckit.specify` → ⑤ `spec.md` generated → … → ⑧ `/speckit.implement` → ⑨ Code generated from specs. **Each step reads the previous artifact to generate the next** | Step-by-step diagram |

#### Section 1.8: Constitution Deep-Dive — Gates & Compound Effects (3 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 1-41 | **Phase -1 Gates — Pre-Implementation Quality Checks** | Code example: `### Phase -1: Pre-Implementation Gates` → `#### Simplicity Gate (Article VII)` → checklist items. `#### Anti-Abstraction Gate (Article VIII)` → checklist items. If a gate fails → document justification in "Complexity Tracking" section. **Gates act as compile-time checks for architectural principles — the LLM cannot proceed without passing** | Code block example of gate checks |
| 1-42 | **The Compound Effect — Constraints Working Together** | 7 constraint patterns don't work individually — they combine to produce 5 quality characteristics: **Complete** (checklists + no speculative features), **Unambiguous** (`[NEEDS CLARIFICATION]` markers), **Testable** (test-first + Phase -1 gates), **Maintainable** (hierarchical detail + What/How separation), **Implementable** (Phase -1 gates + clear phase definitions). **LLM transforms: Creative Writer → Disciplined Specification Engineer** | Quality characteristics mapping table |
| 1-43 | **Concrete Example: Traditional ~12h vs SDD 15min** | Chat feature comparison table: Requirements (PRD manual 2-3h vs `/speckit.specify` 5min), Technical design (design doc 3-4h vs `/speckit.plan` 5min), Test planning (manual scenarios 2h vs `/speckit.tasks` 5min). Total: **~12 hours → 15 minutes**. Output: spec.md + plan.md + data-model.md + contracts/ + tasks.md. **Not just faster — templates enforce consistency and completeness** | ROI comparison table |

#### Section 1.9: Extension System — Modular Extensibility (3 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 1-44 | **Extension System — Modular Extensibility** | Main commands: `specify extension add <repo>` (install), `specify extension remove <name>` (uninstall), `specify extension list` (show installed), `specify extension search <query>` (search catalog). Also: `update`, `info`, `enable`, `disable`. **Customize and extend the SDD workflow for your team** | Extension command table |
| 1-45 | **Extension Manifest & Organization Customization** | `extension.yml` example: `extension: { name: spec-kit-jira, version: "0.1.0" }`, `provides: commands: [{ name: jira-sync, script: jira-sync.sh }]`, `hooks: after_tasks: [sync-to-jira.sh]`. Org-level features: custom catalog URL (`SPECKIT_CATALOG_URL`), hooks for automation after SDD phases, distribute via GitHub repo tags → whole team. **Share team-standard workflows as extensions** | YAML example + org features table |
| 1-46 | **Example: Jira Integration Extension** | `specify extension add github.com/mbachorik/spec-kit-jira` → adds `/speckit.taskstoissues`-style sync to Jira. Demonstrates how SDD integrates with existing project management tools. **SDD doesn't replace your workflow — it enhances it** | Concrete example |

#### Section 1.10: Vibe Coding vs SDD — Detailed Comparison (5 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 1-47 | **Vibe Coding vs SDD — Detailed Comparison** | 6-axis comparison table: Starting point, edge case discovery timing, documentation, pivot cost, where intent lives, AI output quality | Large comparison table |
| 1-48 | **"Is SDD Slow?"** | Counterargument: "Time writing specs < Time fixing bugs." Bugs caught in Clarify are bugs that never exist. Pivoting is low-cost (specs are reusable). The spec survives technology changes — code doesn't. **"Writing correctly IS true speed"** | Common objection response |
| 1-49 | **Where SDD Shines (and Where It's Overkill)** | Best for: (1) Team development, (2) AI-assisted development, (3) External service integrations, (4) Financial/security-critical systems, (5) Long-term maintenance projects. Overkill for: throwaway scripts, exploratory prototypes | Use-case matrix |
| 1-50 | **Bidirectional Feedback — Specs ↔ Production** | Production metrics and incidents don't just trigger hotfixes — they update specifications. Performance bottlenecks become new non-functional requirements. Security vulnerabilities become constraints for all future generations. **Continuous evolution, not one-shot generation.** SDD transforms the traditional SDLC — requirements and design become continuous activities rather than discrete phases | From `spec-driven.md`. Feedback loop diagram |
| 1-51 | **Branching for Exploration** | SDD supports parallel implementations from the same spec. Different tech stacks, architectures, UX patterns — all generated from one specification. `0 → 1, (1', 1'', …), 2, 3, N` — creative branching and iterative evolution. Team process: specs are versioned in branches, reviewed, and merged. **Branching isn't just for code — it's for exploring design alternatives** | From `spec-driven.md`. Team workflow aspect |

---

### Chapter 2: Beginner — SDD Workflow Fundamentals (18 slides)

**Purpose:** Experience SDD's 6 phases through real scenarios. No server, no DB. Learn the SDD workflow itself.

**Target Level:** ⭐ Beginner (basic programming knowledge is sufficient)

#### Section 2.1: Beginner Scenario Introduction (3 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 2-1 | **Chapter 2: Beginner — SDD Workflow Fundamentals** | Section divider. "No server, no database. Learn the SDD workflow itself." | Section divider (`section:has(> h1:only-child)` CSS) |
| 2-2 | **Beginner Scenarios** | 4-scenario table: A (QuickRetro), J (Pomodoro), K (MarkdownPad), L (RecipeBox). What you build, SDD skills learned, duration for each | Table |
| 2-3 | **Beginner Tech Stack** | Vanilla HTML/CSS/JS + localStorage. No build tools, no frameworks. Why: eliminate technical complexity to focus on learning SDD | Tech stack diagram |

#### Section 2.2: Scenario A — QuickRetro: Full SDD Walkthrough (8 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 2-4 | **Scenario A: QuickRetro** | Build a team retrospective board. SDD skills: data modeling, CRUD specs, permissions. Duration: ~90 min | Scenario overview |
| 2-5 | **Constitution in Practice** | Example principles: simplicity, readability, minimal dependencies, test coverage, accessible UI. **Key point: principles are short in proportion to risk** (4–5 principles) | Actual output example |
| 2-6 | **Specify in Practice — Intentional Ambiguity** | Spec contents: fixed user selection (4 users), 3 fixed columns, card CRUD, voting rules. **`[NEEDS CLARIFICATION]` markers** appear in the output | Spec excerpt |
| 2-7 | **Clarify in Practice — 10 Hidden Assumptions** | 10 intentional ambiguities. Examples: "Can anyone create a session, or only admins?", "Can you vote on your own card?", "Are votes anonymous or visible?" **All of these are things AI decides on its own without specs** | Ambiguity list. **Bold: "AI decides without asking"** |
| 2-8 | **The Clarify "Aha Moment"** | Deep-dive example: "Can you vote on your own card?" → Without specs, AI silently picks "yes" or "no." Both designs are reasonable. But **user intent can only be communicated through specs** | Deep-dive on one example |
| 2-9 | **Plan → Tasks → Implement** | Plan: Vanilla HTML/CSS/JS + localStorage → Task breakdown: data model → service → UI ordering → Implementation: AI follows task ordering. Permission checks are centrally managed | 3 phases condensed into 1 slide |
| 2-10 | **Permission Matrix** | From the answer key: complete matrix of who can do what. This is **an artifact that doesn't get generated without a spec** | Table |
| 2-11 | **QuickRetro Takeaways** | (1) Completed the full 6-phase SDD workflow, (2) Permission rules must be explicitly specified, (3) Clarify step has the highest ROI, (4) Without specs, AI decides your design for you | Learning summary |

#### Section 2.3: Other Beginner Scenarios — Different SDD Skills (4 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 2-12 | **Scenario J: Pomodoro Timer — State Machine Specification** | 5 timer states (Idle, Focus, Short Break, Long Break, Paused). SDD lesson: **Behavior is specified using state machines.** Wall-clock vs `setInterval` drift problem | State transition text diagram |
| 2-13 | **Scenario K: MarkdownPad — Output Correctness Specification** | Whitelist approach: "If it's not on the list, don't render it." SDD lesson: **Output specs are directly tied to security (XSS prevention).** URL scheme restrictions | Whitelist vs blacklist |
| 2-14 | **Scenario L: RecipeBox — Calculation Correctness Specification** | Fraction arithmetic: `{ numerator, denominator }` representation (not `parseFloat`). SDD lesson: **Calculation specs must state precision requirements explicitly.** The "1.5 eggs" problem | Calculation example (fraction → decimal pitfall) |
| 2-15 | **Beginner Progression — Skills That Build on Each Other** | Learning sequence: A (data modeling + CRUD) → J (state machines) → K (output correctness + security) → L (calculation correctness). Each step adds a new SDD skill | Progression table |

#### Section 2.4: Beginner Summary (3 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 2-16 | **4 Core Beginner Lessons** | (1) **Permission specs**: Who can do what → A, (2) **Behavior specs**: What are the state transitions → J, (3) **Output specs**: What to render → K, (4) **Calculation specs**: What are the precision requirements → L | 4 core lessons displayed large |
| 2-17 | **Common Beginner Pitfalls** | (1) Permission checks scattered across click handlers, (2) State machines become `if/else` chains, (3) "Render everything" instead of whitelisting, (4) `parseFloat` for fraction arithmetic | Anti-pattern list |
| 2-18 | **Bridge to Intermediate** | Beginner: client-side only → Intermediate: **a server enters the picture.** API contracts, HTTP semantics, databases. How do specs change? | Lead-in to next chapter |

---

### Chapter 3: Intermediate — Server-Side & API Contracts (16 slides)

**Purpose:** Introduce server-side development. Learn to specify API contracts, HTTP semantics, and data validation.

**Target Level:** ⭐⭐ Intermediate (Node.js fundamentals required)

#### Section 3.1: Intermediate Scenario Introduction (3 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 3-1 | **Chapter 3: Intermediate — Server-Side & API Contracts** | Section divider. "Add a server. API contracts become the center of your specs." | Section divider |
| 3-2 | **Intermediate Scenarios** | 4-scenario table: H (CLI), M (ShortLink), N (KanbanFlow), O (MoneyTrail). What you build, SDD skills learned | Table |
| 3-3 | **Baseline Contract** | All ⭐⭐ scenarios share: standard error envelope (JSON), cursor pagination, ISO 8601 dates, DB conventions (`PRAGMA foreign_keys`, id/createdAt/updatedAt), standard scripts (`npm start`/`npm test`) | Contract list |

#### Section 3.2: Scenario M — ShortLink: API Contract Design (7 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 3-4 | **Scenario M: ShortLink — URL Shortener + Analytics** | Looks simple. But when you write the spec: 301 vs 302? Route ordering? Deleted short URLs? Idempotency? SDD lesson: **The API contract IS the product** | "Looks simple, runs deep" theme |
| 3-5 | **HTTP Status Codes Are Part of the Spec** | 301 (permanent redirect — browser caches → analytics stops) vs 302 (temporary redirect — goes through server each time → analytics continues). **Status code selection is a business decision, not a technical one** | 301 vs 302 comparison |
| 3-6 | **Route Safety — Express Mount Order** | `/:slug` catches all requests. Must mount `/api/*` first or API becomes unreachable. **Route ordering should be explicitly specified** | Code example |
| 3-7 | **Idempotency — Shorten the Same URL Twice?** | Options: (1) Generate a new slug (201), (2) Return existing active link (200). SDD resolves this in Clarify. Without specs, AI picks one arbitrarily | Idempotency spec example |
| 3-8 | **Deletion Semantics — 404 vs 410** | Deleted link: 404 (as if it never existed) vs 410 (once existed → slug cannot be reused). **`410 Gone` + tombstone** is the recommended answer. Reason: slug permanence guarantee | Deletion behavior comparison |
| 3-9 | **Error Format Split** | Browser hits `GET /:slug` → HTML error. API client hits `POST /api/shorten` → JSON error. **Same app, different consumers = different error formats** | Format split table |
| 3-10 | **ShortLink Takeaways** | (1) HTTP status codes are part of the spec, (2) Route ordering must be explicitly specified, (3) Idempotency is resolved in Clarify, (4) Deletion semantics are business rules, (5) Error format varies by consumer | Learning summary |

#### Section 3.3: Other Intermediate Scenarios — Different Contract Challenges (3 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 3-11 | **Scenario H: CLI — Output Contract** | CLI's "screen" = stdout. Output itself IS the contract. stderr/stdout separation, exit codes, JSON schema. SDD lesson: **Non-web software has contracts too** | CLI specification |
| 3-12 | **Scenario N: KanbanFlow — Fractional Indexing** | Card ordering is "data." Fractional indexing manages order numerically. Intent-based API (client says "move between A and B," server calculates position). SDD lesson: **Ordering algorithms are part of the spec** | Fractional index concept |
| 3-13 | **Scenario O: MoneyTrail — Data Validation Pipeline** | Each CSV row gets a verdict (success/warning/error/skipped). `parseCents()` uses string splitting (not `parseFloat`). SDD lesson: **Data quality specs design the validation pipeline** | `Math.round(parseFloat('1.005') * 100)` trap |

#### Section 3.4: Intermediate Summary (3 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 3-14 | **Intermediate Progression** | H (output contract) → M (API contract) → N (ordering algorithm) → O (data validation). Each step adds a new server-side SDD skill | Progression table |
| 3-15 | **Beginner vs Intermediate — What Changed?** | Comparison: tech stack (localStorage → SQLite), spec center (UI behavior → API contract), testing (manual → supertest), constitution density (4 → 6 principles), consumer (self → external clients) | Comparison table |
| 3-16 | **Bridge to Intermediate–Advanced** | Intermediate: single service + own DB → Int-Advanced: **external service integrations, auth, multi-tenancy, financial correctness.** Where missing specs cause real damage | Lead-in to next chapter |

---

### Chapter 4: Intermediate–Advanced — Real-World Complexity (16 slides)

**Purpose:** Learn to specify external services, auth, financial, and infrastructure. Where missing specs cause "real damage."

**Target Level:** ⭐⭐⭐ Intermediate–Advanced (external API integration experience)

#### Section 4.1: Intermediate–Advanced Scenario Introduction (2 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 4-1 | **Chapter 4: Intermediate–Advanced — Real-World Complexity** | Section divider. "Where missing specs cause real damage." | Section divider |
| 4-2 | **Intermediate–Advanced Scenarios** | 5-scenario table: B (PWA), C (OIDC SSO), D (Stripe), G (Terraform), I (API Versioning). What you build, SDD skills learned | Table |

#### Section 4.2: Scenario D — Stripe: Specifying Financial Correctness (7 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 4-3 | **Scenario D: Stripe Subscriptions** | Subscription + dunning flow. SDD skills: monetary correctness, idempotency, webhook state machines. **Billing bug = losing real money** | "Money is at stake" scenario |
| 4-4 | **Integer Cents — The Floating-Point Trap** | `0.1 + 0.2 !== 0.3` demo. Amounts MUST be stored as integer cents. `parseFloat` is forbidden. SDD makes this explicit in the constitution: "monetary precision = integer cents" | Floating-point demo |
| 4-5 | **Complex State Machine — 9 Transitions** | Subscription states: trial → active → past_due → canceled → suspended (8+ states, 9 transitions). Evolution from beginner Pomodoro (5 states). **If you don't specify every state transition, users get incorrectly billed** | State transition text diagram |
| 4-6 | **Webhook Reliability — "At Least Once" Delivery** | Stripe webhooks are at-least-once. Duplicate processing = double billing. Must specify: signature verification, event deduplication, async queue processing, ignoring stale events | Webhook challenge list |
| 4-7 | **Idempotency Keys — Every Stripe API Call** | Without idempotency: network error → retry → double charge. SDD makes "idempotency everywhere" a constitutional principle | Idempotency concrete example |
| 4-8 | **The Clarify "Aha Moment" — Unused Seat Refunds** | "What about unused seat credits at cancellation? Refund? Forfeit? Apply to final invoice?" — Without specs, AI decides arbitrarily. **Financial edge cases must be explicitly decided in specs** | Deep-dive example |
| 4-9 | **Constitution Density Comparison** | Beginner (4–5 principles) vs Intermediate–Advanced (11 principles). Constitution grows proportionally to risk. D's constitution: correctness-first, integer cents, idempotency, eventual consistency, fail-safe access, webhook verification, PCI compliance, audit logs… | Comparison list |

#### Section 4.3: Other Intermediate–Advanced Scenarios (4 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 4-10 | **Scenario B: Field Inspection PWA — Offline Sync** | Specifying offline-first behavior. Conflict resolution rules, media upload retry, sync queue ordering. SDD lesson: **"What happens offline?" is answered in the spec** | Offline sync challenges |
| 4-11 | **Scenario C: OIDC SSO + RBAC — Security Contract** | Fail-closed principle, tenant isolation, secret rotation. SDD lesson: **Security isn't bolted on later — it's defined in the constitution** | Security-first specification |
| 4-12 | **Scenario G: Terraform + GitHub Actions — Infrastructure Spec** | "Infrastructure itself IS the spec." Drift detection, blast radius control, no manual changes. SDD lesson: **SDD applies to ops, not just apps** | IaC + SDD |
| 4-13 | **Scenario I: API Versioning — Backward Compatibility Spec** | v1→v2 migration. Shim layer, deprecation timeline, `410 Gone`. SDD lesson: **200 consumers depend on v1 → compatibility is a spec requirement** | API migration strategy |

#### Section 4.4: Intermediate–Advanced Summary (3 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 4-14 | **Intermediate vs Intermediate–Advanced — What Changed?** | Comparison: external services (none → Stripe/IdP/Terraform), stakes (UI bugs → real money/security breaches), constitution density (6 → 11 principles), eventual consistency (not needed → required), testing (contract → chaos testing) | Comparison table |
| 4-15 | **"Missing Specs Cause Real Damage" — Case Studies** | (1) Double billing (D), (2) Cross-tenant data leak (C), (3) Offline data loss (B), (4) Sudden API shutdown (I), (5) Infrastructure drift (G). **All preventable with Clarify** | Case study list |
| 4-16 | **Bridge to Advanced** | Int-Advanced: external service integrations → Advanced: **distributed systems, failure is the default state, safety invariants vs liveness goals.** Specs must define failure models | Lead-in to next chapter |

---

### Chapter 5: Advanced — Distributed Systems & Failure Models (18 slides)

**Purpose:** Learn to specify distributed systems. Failure models, safety invariants, liveness goals, idempotency, observability. Push SDD to its limits.

**Target Level:** ⭐⭐⭐⭐ Advanced (distributed systems fundamentals required)

#### Section 5.1: Advanced Scenario Introduction (3 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 5-1 | **Chapter 5: Advanced — Distributed Systems & Failure Models** | Section divider. "Failure is the default state. Specs define the failure model." | Section divider |
| 5-2 | **Advanced Scenarios** | 5-scenario table: E (Whiteboard), F (Pipeline), P (OrderFlow), Q (PlugKit), R (FlagShip). What you build, SDD skills learned | Table |
| 5-3 | **Advanced Baseline Contract** | Required for all ⭐⭐⭐⭐ scenarios: (1) Failure model section, (2) Safety invariants vs liveness goals, (3) Idempotency rules, (4) Observability requirements (correlation ID, audit logs, reconciliation) | Contract list |

#### Section 5.2: Safety Invariants vs Liveness Goals (2 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 5-4 | **Safety Invariants — Things That Must NEVER Happen** | Examples: "Never ship an unpaid order" (P), "Never assign a user to two mutually exclusive experiments" (R), "Deleted objects never appear to other users" (E). **Explicitly enumerate in the spec** | Safety concrete examples |
| 5-5 | **Liveness Goals — Things That Must EVENTUALLY Happen** | Examples: "All clients eventually converge" (E), "Buffered events are eventually processed" (F), "Orders eventually complete or get compensated" (P). **"Eventually" is the keyword** | Liveness concrete examples |

#### Section 5.3: Scenario P — OrderFlow: Learning the Saga Pattern (6 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 5-6 | **Scenario P: OrderFlow Saga** | 6-step order fulfillment (Validate → Authorize → Reserve → Capture → Ship → Confirm). SDD skills: compensating transactions, timeout semantics, exactly-once | Scenario overview |
| 5-7 | **Compensation Pairs & the Cost Gradient** | Compensation table per step: Validate→none, Authorize→Void (free), Reserve→Release (free), Capture→Refund (fee + 5–10 days), Ship→Cancel (time-limited). **The further you go, the more expensive compensation becomes → step ordering matters** | Compensation table |
| 5-8 | **"Timeout = Unknown" Paradigm** | Payment capture times out. Question: "Was the customer charged?" → **Answer: unknown.** Therefore: query status before retrying on timeout. In vibe coding this becomes "retry → double charge" | **Advanced "aha moment"** |
| 5-9 | **Failure Paths Outnumber the Happy Path** | One happy path. Combinatorial explosion of failure paths: 6 steps × multiple failure modes × partial completion states × timeouts. **Without specs, it's impossible to discover all failure paths** | Combinatorial diagram |
| 5-10 | **The Outbox Pattern** | State change and event publishing in the same DB transaction. Why: state changes but event not sent → inconsistency. Specify event delivery guarantees in the spec | Outbox concept diagram |
| 5-11 | **OrderFlow Takeaways** | (1) Compensate cheaply first (step ordering matters), (2) Timeout ≠ failure, (3) Failure path specs are combinatorial, (4) Safety invariant: never ship unpaid, (5) Outbox pattern for event delivery guarantees | Learning summary |

#### Section 5.4: Other Advanced Scenarios — Different Distributed Challenges (4 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 5-12 | **Scenario E: Collaborative Whiteboard — Consistency Model** | Consistency model choice (CRDT vs OT vs authoritative server) determines entire architecture. Quantitative latency budget (local <16ms, remote p95 <200ms). SDD lesson: **Architecture decisions happen in the spec/plan phase** | Consistency model comparison |
| 5-13 | **Scenario F: Event Ingestion Pipeline — SLO Specification** | Ban vague "high performance." Concrete SLOs: throughput X/sec, p99 latency Y ms. Backpressure (429), schema evolution. SDD lesson: **Performance requirements must be quantitatively specified** | SLO quantification |
| 5-14 | **Scenario Q: PlugKit Runtime — Your Spec IS the Product** | Plugin API is what external developers depend on. Spec = product. Sandboxed execution (Worker Thread), capability permissions, threat model. SDD lesson: **Public API specs can't be changed after release** | API contract specifics |
| 5-15 | **Scenario R: FlagShip — Statistical Correctness Specification** | Deterministic bucketing (`Math.random` forbidden, hash functions), SRM detection (chi-square test), kill switch bypasses all caches. SDD lesson: **Statistical correctness is part of the spec** | Bucketing algorithm |

#### Section 5.5: Advanced Summary (3 slides)

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 5-16 | **Advanced Progression** | E (consistency model) → F (SLO + backpressure) → P (compensating transactions) → Q (public API) → R (statistical correctness). Each step adds a new distributed systems SDD skill | Progression table |
| 5-17 | **Cross-Level Comparison — What Changed Across All Levels?** | 4-level comparison table: Constitution density, state complexity, failure model, idempotency requirements, testing approach, "aha moment" | Large comparison table |
| 5-18 | **SDD Skill Growth Map** | 5 skill axes across levels: (1) State machines: J→D→P→E, (2) Permissions: A→M→D→E, (3) Idempotency: none→API→Webhook→Per-step, (4) Consistency: localStorage→single DB→eventual consistency→real-time convergence, (5) Constitution: short→medium→long→distributed guarantees | Growth map |

---

### Chapter 6: Summary & Next Steps (7 slides)

**Purpose:** Review the full presentation and provide actionable next steps for tomorrow.

| # | Slide Title | Content | Notes |
|---|---|---|---|
| 6-1 | **Chapter 6: Summary** | Section divider | Section divider |
| 6-2 | **The Transformation — What SDD Changes** | SDD isn't about replacing developers or automating creativity. It's about amplifying human capability by automating mechanical translation. "Debugging means fixing specifications. Refactoring means restructuring for clarity." SDD transforms the traditional SDLC — requirements and design become continuous activities, not discrete phases. Comparison table: Central asset (code → spec), Maintenance (fix code → evolve spec), Pivoting (rewrite → regenerate), Developer role (mechanical translation → creativity, experimentation, critical thinking). **The lingua franca of development moves from code to natural-language specifications** | From `spec-driven.md`. Closing philosophy + comparison table |
| 6-3 | **4 Core SDD Principles** | (1) **Specs catch bugs before they exist**, (2) **AI works dramatically better with structure**, (3) **Pivoting becomes low-cost**, (4) **The spec is the single source of truth** | 4 principles displayed large |
| 6-4 | **Recommended Learning Paths** | Paths: 90 min → A / Half day → A+M / Full day → A→J→K→M→N→⭐⭐⭐ / Advanced track → M→D→P→R / Team training → everyone A + self-select by level / Conference talk (60 min) → A or J, MVP tier only. Tips: Never skip Clarify, check answer keys after (not during), watch constitution density grow with risk | Learning path matrix |
| 6-5 | **SDD Practice Guide — Start Today Checklist** | 6 actionable items: (1) `specify init` to initialize project — constitution + templates auto-generated, (2) Write constitution first — principles before specs, (3) Never skip Clarify — `[NEEDS CLARIFICATION]` resolution is SDD's ROI source, (4) Manage specs in branches — `specs/[branch]/` for team review & merge, (5) Start with one small feature — experience specify → plan → tasks on one feature first, (6) Verify AI output against spec — always cross-check generated code. **Mindset shift: Before writing code, ask "Is the spec sufficient?"** SDD isn't a tool problem — it's the discipline of treating specs as the source of truth | Actionable checklist table |
| 6-6 | **Resources** | Spec Kit: repo (`github.com/github/spec-kit`), 📽️ Video Overview (`youtube.com/watch?v=a9eR1xsfvHg`), 📖 Docs (`github.github.io/spec-kit/`), Workshop Guide (`WORKSHOP.md`), Scenarios (`SCENARIOS.md`). SDD Methodology: Complete guide (`spec-driven.md`), Phase details (each `/speckit.*` prompt file). Getting started code: `specify init my-first-sdd-project --ai copilot && cd my-first-sdd-project && code .` | Categorized resource links + getting-started code block |
| 6-7 | **Thank You** | "Stop vibe coding. Start specifying." + QR code + `@shinyay` contact info | Ending slide. Footer override: "Stop vibe coding. Start writing specs. — @shinyay" |

---

## 📊 Slide Statistics

| Chapter | Slides | Estimated Time |
|---|---|---|
| Chapter 0: Title & Introduction | 5 | 3 min |
| Chapter 1: General | 51 | 37 min |
| Chapter 2: Beginner | 18 | 15 min |
| Chapter 3: Intermediate | 16 | 12 min |
| Chapter 4: Intermediate–Advanced | 16 | 12 min |
| Chapter 5: Advanced | 18 | 15 min |
| Chapter 6: Summary | 7 | 5 min |
| **Total** | **131** | **~99 min** |

---

## 🎨 Design Guidelines

### Marp Theme Settings
- **Theme:** `github-dark` ([slides/themes/github-dark.css](themes/github-dark.css))
- **Background:** `#0d1117`
- **Text:** `#c9d1d9`
- **Headings:** `#ffffff`
- **Accent color:** `#7ee787` (green)
- **Code background:** `#161b22`
- **Font:** Mona Sans (primary), system sans-serif fallback; theme font stack also includes `Noto Sans JP`, `Hiragino Kaku Gothic ProN`, and `Meiryo` for Japanese text compatibility

### Marp Front-Matter (exact block for the English presentation)

```yaml
---
marp: true
theme: github-dark
paginate: true
header: "Introduction to SDD — GitHub Spec Kit"
footer: "Shinya Yanagihara, Developer Global BlackBelt, Microsoft Corporation"
---
```

### Slide Type Design

| Type | Usage | CSS Class/Feature |
|---|---|---|
| **Title slide** | Chapter 0 only | `section:first-of-type` (centered, large h1) |
| **Section divider** | First slide of each chapter | h1-only slide (`section:has(> h1:only-child)`) |
| **Content slide** | Standard slides | h2 (green subtitle) + h1 + body |
| **Comparison table** | vs comparisons, progressions | Table usage |
| **Code slide** | Command examples, JSON | Code block usage |
| **Blockquote slide** | Key messages | Blockquote usage |

### Content Density Rules
- **1 slide = 1 message** (don't cram multiple points)
- **Bullet points: max 5 items**
- **Tables: max 6 rows × 4 columns**
- **Code blocks: max 10 lines**
- **Keep default font size (22px)** — never shrink it

---

## 🔑 Key Messages by Chapter

| Chapter | Key Message (1 sentence) |
|---|---|
| **Chapter 1: General** | "The spec is the primary artifact; code is its expression." |
| **Chapter 2: Beginner** | "Without specs, AI decides your design for you." |
| **Chapter 3: Intermediate** | "The API contract IS the product, and HTTP status codes are part of the spec." |
| **Chapter 4: Intermediate–Advanced** | "Missing specs mean losing real money, real security, and real data." |
| **Chapter 5: Advanced** | "In distributed systems, failure is the default state — specs must define the failure model." |

---

## 🧭 Story Arc (Narrative Structure)

```
Act 1 — Problem & Solution (Chapters 0–1)
  "You're vibe coding? → SDD flips the script."
  ↓
Act 2 — Progressive Practice (Chapters 2–5)
  Beginner: Learn the workflow → Intermediate: Learn contracts
  → Intermediate–Advanced: Real-world complexity → Advanced: Failure models
  ↓
Act 3 — Summary & Call to Action (Chapter 6)
  "Stop vibe coding. Start specifying. Here's how to start."
```

**"Aha Moments" by Chapter:**

| Chapter | "Aha Moment" |
|---|---|
| 1 | "AI is an excellent implementer, but not an excellent designer." |
| 2 | "Can you vote on your own card? → AI decided without asking!" |
| 3 | "301 vs 302 breaks your analytics!" |
| 4 | "`0.1 + 0.2 !== 0.3` → billing bug!" |
| 5 | "Timeout → did it charge? → retry → double charge!" |

---

## ✅ Quality Checklist

Pre-implementation checks:

- [ ] Every slide follows "1 slide = 1 message"
- [ ] Every chapter has an "aha moment"
- [ ] Concrete examples (from scenarios) exist in all chapters
- [ ] Comparison tables show "evolution from the previous level"
- [ ] Code examples are minimal and effective
- [ ] Natural English phrasing (no "translatese" or mechanical translation)
- [ ] Compliant with Marp `github-dark` theme design guidelines
- [ ] h1/h2 usage is correct (h2 = section label, h1 = main title)
- [ ] Pagination enabled
- [ ] Header/footer configured in English (matches front-matter block above)
- [ ] Spec Kit terminology matches the official repository
- [ ] All 20+ supported AI agents referenced where relevant
- [ ] `spec-driven.md` concepts (Power Inversion, 3 modes, constitution articles) are incorporated
- [ ] Workshop scenarios (A–R) are all referenced with English descriptions
- [ ] Slide count matches statistics table (131 slides total)
- [ ] 📽️ Video Overview slide is included (Section 1.3)
- [ ] Extension System section is present (Section 1.9, 3 slides)
- [ ] Phase -1 Gates has its own dedicated slide (Section 1.8)
- [ ] The Compound Effect slide is present (Section 1.8)
- [ ] Concrete ROI example (~12h vs 15min) is present (Section 1.8)
- [ ] No `Noto Sans JP` font reference in English theme/front-matter
- [ ] Marp front-matter block is specified in Design Guidelines
- [ ] Chapter 6 has separate slides for: Transformation, Principles, Learning Paths, Practice Checklist, Resources, Thank You
