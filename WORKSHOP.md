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

### Choose Your Scenario

This workshop includes multiple scenarios at different difficulty levels. Choose one and follow its prompts through each SDD phase.

| | Scenario A | Scenario B |
|---|---|---|
| **Name** | QuickRetro | Field Inspection PWA |
| **What you build** | Team retrospective board | Offline-first field inspection app |
| **Level** | ⭐ Beginner | ⭐⭐⭐ Intermediate–Advanced |
| **Duration** | ~90 min | ~120 min |
| **Key SDD themes** | CRUD, permissions, voting logic | Offline-first, sync conflicts, media uploads |
| **Why it tests SDD** | Permissions and voting edge cases need clear specs | Offline + sync + conflict resolution cannot be vibe-coded |
| **Best for** | First-time SDD learners | Developers who want a production-grade challenge |

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

#### Scenario A: QuickRetro

In Copilot Chat, run:

```
/speckit.constitution Create principles for a lightweight web application focused on simplicity, readability, and maintainability. Prioritize minimal dependencies, clear separation of concerns, comprehensive test coverage, and accessible UI. The application should work without a build step where possible. Avoid over-engineering — no abstractions until the third use case demands it.
```

#### Scenario B: Field Inspection PWA

In Copilot Chat, run:

```
/speckit.constitution Create a constitution for an offline-first field inspection PWA that will be used on-site with unstable connectivity.

Non-negotiables:
- Offline-first is mandatory: core flows must work with no network.
- Never lose user-entered data: drafts, photos, notes must be durable.
- Conflict handling must be explicit (no "last write wins" without user awareness).
- Progressive enhancement: core inspection completion must work on limited browsers; PWA-specific features (background sync, push notifications) are enhancements, not requirements.
- Graceful degradation for hardware APIs: if camera access or storage is unavailable, offer an alternative path or clear explanation — never a silent failure.
- Data lifecycle: define explicit retention and cleanup rules; submitted inspections may be purged from local storage after confirmed server receipt.
- Accessibility: keyboard navigation + screen-reader-friendly forms; clear error messages.
- Performance: fast launch; avoid heavy bundles; keep memory usage reasonable.
- Security/privacy: treat photos and notes as sensitive; no sensitive data in logs; sanitize analytics.
- Testing: require automated tests for sync/conflict logic and critical UI flows; include regression tests for bug fixes.
- Documentation: include a "How offline sync works" doc and a troubleshooting section for support.
```

### ✅ Checkpoint

Review the generated `.specify/memory/constitution.md` file. Verify that it includes:

- [ ] Code quality and simplicity guidelines
- [ ] Testing expectations
- [ ] Architectural constraints
- [ ] UI/UX and accessibility principles

**Scenario B participants** — also verify:
- [ ] Offline-first is stated as a non-negotiable
- [ ] Data durability principle is present
- [ ] Conflict handling rules are explicit

> [!TIP]
> The constitution is YOUR document. If the AI generated something you disagree with, edit it directly or ask the AI to revise it. This is not a one-shot exercise.

---

## Part 3: Define Your Specification [15–20 min]

This is the most critical phase of SDD. You will describe **what** you want to build and **why**, without specifying **how**.

### Hands-On

#### Scenario A: QuickRetro

**The concept:** A team retrospective board. Teams use it after a sprint to reflect on what happened — adding cards to columns (Went Well, To Improve, Action Items), voting to surface the most important items, and tracking action items to completion.

In Copilot Chat, run:

```
/speckit.specify Build QuickRetro, a team retrospective board application. When the app launches, it displays a list of pre-defined team members (4 people: two engineers, one designer, one product manager) to select from — no password required. After selecting a user, you see a list of retro sessions. Clicking a session opens the retro board with three columns: "Went Well," "To Improve," and "Action Items." Any team member can add cards to any column. Cards show the author name and creation time. Each team member can vote once per card using a thumbs-up button — you cannot vote on your own card. Cards are sorted by vote count (highest first) within each column. You can only edit or delete cards you created. Action Item cards have an additional "Mark Complete" checkbox that anyone can toggle. There should be 2 sample retro sessions pre-loaded with 3-5 cards each, distributed across all columns.
```

**Deliberate ambiguities to watch for:**
- Can a user create new retro sessions, or are they admin-only?
- What happens when all action items are marked complete?
- Is there a limit on card length?
- Are votes anonymous to other users?
- Can you reopen a "completed" retro session?

#### Scenario B: Field Inspection PWA

**The concept:** Inspectors perform safety/compliance checks at physical sites — basements, industrial areas, places with poor connectivity. They need to complete checklists, attach photos, add notes, and submit when back online. Supervisors review the submissions remotely.

In Copilot Chat, run:

```
/speckit.specify Build an offline-first "Field Inspection" web app for inspectors performing safety/compliance checks at physical sites.

Context & goals:
- Inspectors work in basements/industrial areas with poor connectivity.
- They need to complete checklists, attach photos, add notes, and submit when back online.
- Reduce time-to-complete and reduce rework due to lost data.

Users:
- Inspector (primary): logs in with email/password; session persists offline once authenticated.
- Supervisor (reviews submitted inspections).

Core flows:
1) Inspector selects a site + inspection template (checklist) and starts an inspection.
2) App saves progress continuously (auto-save).
3) Inspector can attach multiple photos per checklist item, add notes, and mark pass/fail/NA.
4) Inspector can complete inspection offline and "Submit" later when online.
5) Supervisor can review submitted inspections, leave comments, and export a PDF summary.

Functional requirements:
- Inspection templates: grouped sections, required vs optional items. Templates are managed by admins and synced to devices; inspectors cannot modify templates.
- Draft state: list drafts, search by site, show last-edited time, resume draft.
- Attachments: capture from camera + upload from device; max 10 photos per checklist item; JPEG/PNG only, max 10 MB each; no video in v1. Show upload status; allow delete/replace.
- Sync:
  - Automatic background sync when connectivity returns.
  - Clear status UI (Offline / Syncing / Synced / Needs Attention).
  - If the same inspection draft was edited on two devices, show a conflict resolution UI.

Non-goals (explicitly out of scope):
- No real-time collaboration on the same draft.
- No complex permissions beyond Inspector vs Supervisor.
- No video capture.

Acceptance criteria (examples):
- If the app crashes or the tab closes, reopening restores the latest draft state.
- Submitting offline queues the submission; when online, submission completes without user re-entering data.
- Conflict resolution shows the differing fields and lets the user choose per-field or per-section.
- Supervisor export includes checklist results, notes, and photo thumbnails/links.

Edge cases to explicitly cover:
- Large photo uploads on slow connections, retries, and partial failures.
- Duplicate submissions (user taps Submit multiple times).
- Time drift between devices.
- Template updates while an inspection is in progress.
- Storage full on device while inspection is in progress.
```

**Deliberate ambiguities to watch for:**
- What is the completed inspection lifecycle? (After supervisor approval — archive? delete? retention period?)
- Does the supervisor get notified of new submissions? (Push? Email? Dashboard badge?)
- What happens to local data after confirmed server receipt?
- Can a supervisor reject an inspection and send it back for rework?
- How are template versions managed when inspectors have cached old versions?

### What to Observe

After the command runs, examine the generated specification:

1. **Branch**: A feature branch should be created (e.g., `001-quick-retro` or `001-field-inspection`)
2. **Spec file**: The `spec.md` should contain:
   - User stories with acceptance criteria
   - Functional requirements
   - `[NEEDS CLARIFICATION]` markers for ambiguous areas
   - A review and acceptance checklist

### 🤔 Discussion Point

Look at what the AI captured vs. what it flagged as unclear. These are exactly the kinds of questions that **vibe coding misses** and **SDD surfaces early**. In a traditional workflow, these ambiguities become production bugs.

---

## Part 4: Clarify the Specification [10–15 min]

Now we refine. This step is where SDD delivers its highest ROI — catching ambiguity **before** a single line of code is written.

### 4.1 Structured Clarification

#### Scenario A: QuickRetro

In Copilot Chat, run:

```
/speckit.clarify
```

Suggested answers for the workshop:

| Question Theme | Suggested Answer |
|---|---|
| Session creation | Any team member can create a new retro session |
| Card length | Maximum 280 characters per card |
| Completed retros | Sessions can be archived but not deleted |
| Vote visibility | Votes are visible (show who voted) |
| Concurrent editing | Last-write-wins, no real-time sync needed for v1 |

#### Scenario B: Field Inspection PWA

In Copilot Chat, run:

```
/speckit.clarify Review the Field Inspection spec and ask me about every ambiguity, unstated assumption, and gap — especially around: authentication flow, completed inspection lifecycle, supervisor notification mechanism, data retention policy, template versioning, and the specific behavior for each listed edge case.
```

Suggested answers for the workshop:

| Question Theme | Suggested Answer |
|---|---|
| Completed inspection lifecycle | After supervisor approval, inspection is archived. Local cache is purged after confirmed server receipt. Server retains data for 7 years (compliance). |
| Supervisor notifications | Badge count on supervisor dashboard; optional email digest (daily). No push notifications in v1. |
| Supervisor rejection | Supervisor can reject with comments; inspection returns to Inspector as a draft with rejection notes visible. |
| Duplicate submission prevention | Idempotency key per submission; server deduplicates; UI disables button after first tap and shows spinner. |
| Time drift | Use server timestamps as authoritative for sync ordering; device timestamps used only for local display. |
| Template versioning | Inspection keeps the template version it was started with. If a newer template is available, show a non-blocking banner — do not force migration mid-inspection. |
| Storage full | Warn at 80% capacity; block new photo attachments (not text) at 95%; never lose existing draft data. |
| Camera access denied | Show a clear message explaining why the camera is needed; allow file upload from device as fallback. |

### 4.2 Manual Refinement

After the structured clarification, add any details the AI missed:

**Scenario A:**

```
For the pre-loaded sample data: create one retro titled "Sprint 23 Retro" and another titled "Q4 Planning Retro." Distribute sample cards across all three columns with varied vote counts so the sorting is visible. Ensure at least one action item is already marked as complete in the sample data.
```

**Scenario B:**

```
For sample data: create 2 inspection templates — "Fire Safety Quarterly" (3 sections, 12 items) and "Electrical Compliance" (2 sections, 8 items). Pre-load 1 completed inspection and 1 in-draft state. Include at least one item with multiple photo attachments and one with a detailed note.
```

### 4.3 Validate the Checklist

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

### ✅ Checkpoint

- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] Clear user stories with testable acceptance criteria
- [ ] Sample data requirements defined
- [ ] Edge cases explicitly addressed

**Scenario B participants** — also verify:
- [ ] Sync behavior is fully specified (online → offline → online transitions)
- [ ] Conflict resolution UX is described (per-field or per-section choice)
- [ ] Every listed edge case has a defined behavior

---

## Part 5: Create the Implementation Plan [15–20 min]

Now — and only now — do we talk about technology. The specification is stable; it's time to decide **how** to build it.

### Hands-On

#### Scenario A: QuickRetro

In Copilot Chat, run:

```
/speckit.plan Use vanilla HTML, CSS, and JavaScript with no build tools or frameworks. Store all data in the browser using localStorage. The app should be a single index.html file with linked CSS and JS files. Keep it simple — no bundlers, no transpilers, no package managers needed for the frontend.
```

#### Scenario B: Field Inspection PWA

In Copilot Chat, run:

```
/speckit.plan Create a technical plan for the Field Inspection PWA, adhering to the constitution.

Tech stack:
- Frontend: TypeScript + React, built with Vite, Workbox for service worker management.
- Local storage: IndexedDB via Dexie.js for structured data; Cache API for static assets.
- Backend: Node.js + Fastify, PostgreSQL for persistent storage.
- File storage: S3-compatible object store for photo uploads.
- Deployment: containerized (Docker), deployed via CI/CD.

The plan must include:
- Architecture overview (frontend, backend, storage, sync strategy).
- PWA strategy: service worker lifecycle, cache-first vs network-first decisions per resource type, app install prompt, update notification UX.
- Offline storage approach: what data goes where, durability guarantees, IndexedDB schema versioning/migration.
- Sync protocol: identifiers, idempotency, retries, conflict detection strategy, and conflict resolution UX design.
- Data model: inspection templates, inspections, checklist items, attachments, submission status, supervisor review comments.
- API design: endpoints/contracts for templates, drafts, submissions, exports, and attachment upload (including multipart + resumable upload for large photos).
- Attachment strategy: client-side compression/thumbnail generation before storage in IndexedDB, upload queue with retry, server-side thumbnail generation for PDF export.
- Observability: event logging (non-sensitive), error tracking, sync failure diagnostics.
- Testing plan: unit tests for sync/conflict engine, integration tests for offline-to-online flows, e2e tests for critical paths (complete inspection offline → submit online → supervisor review).
- Rollout plan: feature flags for sync and offline features, safe IndexedDB schema migration strategy.
```

### What Gets Generated

Review the output artifacts in your `.specify/specs/` feature directory:

| File | Purpose |
|---|---|
| `plan.md` | High-level implementation plan with phases |
| `data-model.md` | Data structures for all entities |
| `research.md` | Technical research and library evaluations |
| `quickstart.md` | Key validation scenarios |
| `contracts/` | API specifications (Scenario B) |

### Validate the Plan

Ask the AI to audit itself:

```
Review the implementation plan and check: (1) Are there any over-engineered components that violate our constitution's simplicity principle? (2) Does every technical choice trace back to a requirement in the spec? (3) Is the phase ordering logical — can each phase be validated independently?
```

> [!WARNING]
> AI agents tend to over-engineer. Watch for unnecessary abstractions, excess libraries, or "future-proofing" that nobody asked for. Push back if you see it.

### ✅ Checkpoint

- [ ] Tech stack matches what you specified
- [ ] No unnecessary dependencies or abstractions
- [ ] Data model covers all entities from the spec

**Scenario B participants** — also verify:
- [ ] Sync protocol is described with conflict detection and resolution steps
- [ ] Service worker strategy is documented (cache-first vs network-first per resource)
- [ ] Attachment lifecycle is clear (capture → compress → IndexedDB → upload queue → S3)

---

## Part 6: Generate Task Breakdown [5 min]

Convert the plan into an ordered, executable task list.

### Hands-On

#### Scenario A: QuickRetro

In Copilot Chat, run:

```
/speckit.tasks
```

#### Scenario B: Field Inspection PWA

In Copilot Chat, run:

```
/speckit.tasks Break down the plan into small, ordered tasks.

Task breakdown rules:
- Each task should have a clear objective, explicit inputs/outputs, and "done when" checks.
- Prefer tasks that touch 1–2 files/components/modules at a time.
- Identify tasks that can be parallelized safely.
- Include dedicated tasks for tests (unit/integration/e2e) and documentation.
- Include tasks for edge cases (conflicts, retries, duplicate submissions, large attachments).
- Include integration checkpoint tasks where independently-built components are wired together and validated.
- Include an early end-to-end "golden path" task: Inspector logs in → starts inspection → fills checklist → attaches photo → goes offline → completes inspection → comes back online → submits → Supervisor reviews. This validates the full flow before edge cases are implemented.
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

## Part 7: Implement [10–15 min]

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

**Scenario B participants** — specifically watch for:
- Service worker registration happens early
- IndexedDB schema setup matches the data model
- Sync engine is implemented before UI features that depend on it

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
5. **Complexity demands specification.** *(Scenario B)* Could you vibe-code a sync conflict resolver with offline-first media uploads? SDD makes the hard parts tractable.

### Discussion Questions

- How would you adapt SDD to your current team's workflow?
- What types of projects benefit most from SDD? Where might it be overkill?
- How does SDD change the role of code review?
- What happens when the AI generates code that doesn't match the spec?
- *(Scenario B)* How would you handle a situation where the sync protocol needs to change after implementation has started?

---

## Bonus: Extension Activities

If you finish early or want to continue after the workshop:

### For Scenario A: QuickRetro

**Extension A1: Add a feature** — Add a "Timer" feature using the full SDD workflow:

```
/speckit.specify Add a "Timer" feature to QuickRetro. When a retro session is active, the facilitator can start a countdown timer (configurable: 5, 10, or 15 minutes) that is visible to all participants. When the timer expires, a notification appears. The timer is per-column — the facilitator advances through columns with the timer.
```

Then continue through `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

**Extension A2: Rebuild with a different tech stack** — Same spec, different implementation:

```
/speckit.plan Rebuild QuickRetro using React with TypeScript. Use Vite as the build tool. Store data in a local SQLite database via sql.js (WASM). Create a component-based architecture with proper state management using React Context.
```

This demonstrates SDD's tech independence — the same spec produces different implementations.

### For Scenario B: Field Inspection PWA

**Extension B1: Add a feature** — Add real-time supervisor notifications:

```
/speckit.specify Add a real-time notification system for supervisors. When an inspector submits an inspection, the supervisor's dashboard shows a toast notification and updates the badge count without a page refresh. Use Server-Sent Events (SSE) for push — not WebSockets — to keep complexity low. Include a notification history page showing the last 50 events.
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

**Extension B2: Stress-test the spec with a new edge case** — Add this to the existing spec and see how it ripples through the plan and tasks:

```
A new requirement has emerged: inspectors may now hand off an in-progress inspection to a different inspector mid-visit (shift change). Update the spec, plan, and tasks to handle this. Consider: what happens to the original inspector's locally cached data? Does the new inspector's device need to pull the partial draft? How does this interact with conflict resolution?
```

This demonstrates SDD's iterative enhancement capability — specs evolve, and the toolchain propagates changes.

### For All Scenarios

**Cross-artifact analysis** — Run the optional consistency check:

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
| Experienced developers, want a real-world challenge | **Scenario B** (Field Inspection PWA) |
| Mixed audience | Let participants self-select; pair beginners together on A |
| Conference talk (tight time) | **Scenario A** only (fits 90 min) |
| Half-day workshop (3+ hours) | Both scenarios sequentially — A first, then B |

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
| Clarification | 15 min | +5 min | **Highest-value phase for this scenario** — the sync/conflict questions are eye-opening |
| Plan | 20 min | +5 min | Most complex phase; lots of generated artifacts to review |
| Tasks | 10 min | +3 min | Task list is long; focus on dependency ordering and the golden-path task |
| Implementation | 15 min | — | Observe service worker and sync engine tasks being created |
| Wrap-Up | 15 min | — | Rich discussion — offline-first is a great topic for debate |

### Common Issues & Solutions

| Issue | Solution |
|---|---|
| Codespace takes >5 min to build | Have participants start setup immediately; present context slides while waiting |
| `specify` command not found | Run: `uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git` |
| Slash commands not visible in Copilot | Re-run `specify init . --ai copilot --force`; restart Copilot Chat |
| AI generates overly complex plan | Prompt: "Simplify this plan. Remove any frameworks or libraries not explicitly requested." |
| Participants at different speeds | Fast finishers → Extension activities. Slow finishers → Skip to `/speckit.tasks` with facilitator-provided plan |
| AI output differs between participants | This is expected and a teaching moment. Compare outputs to discuss how AI interprets ambiguity. |
| Scenario B spec is too complex for audience | Fall back to Scenario A; use Scenario B as a demo-only walkthrough |
| AI doesn't address offline/sync in plan (Scenario B) | Prompt: "The constitution says offline-first is non-negotiable. Revise the plan to put offline storage and sync protocol as Phase 1, before any UI work." |

### Key Teaching Moments

1. **After Part 3 (Specify):** Ask participants to compare their generated specs. Differences highlight why specification matters — same prompt, different interpretations.
2. **After Part 4 (Clarify):** Have 2–3 participants share the most surprising question the AI asked. This demonstrates the value of structured clarification. *(Scenario B: the sync conflict and template versioning questions are particularly powerful.)*
3. **After Part 5 (Plan):** Ask if anyone's plan includes something they didn't request. Use this to discuss AI over-engineering and the importance of constitution constraints. *(Scenario B: watch for the AI adding WebSocket real-time features that were explicitly listed as a non-goal.)*
4. **After Part 6 (Tasks — Scenario B only):** Ask participants to find the golden-path task and trace it back through the plan to the spec. This demonstrates full traceability — the core SDD value proposition.

---

## References

- [Spec Kit Repository](https://github.com/github/spec-kit)
- [Spec-Driven Development Methodology](https://github.com/github/spec-kit/blob/main/spec-driven.md)
- [Spec Kit Video Overview](https://www.youtube.com/watch?v=a9eR1xsfvHg)
- [Dev Containers Specification](https://containers.dev/)
