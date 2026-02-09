# Scenario A: QuickRetro — Team Retrospective Board

| | |
|---|---|
| **Level** | ⭐ Beginner |
| **Duration** | ~90 min |
| **Key SDD themes** | CRUD, permissions, voting logic |
| **Why it tests SDD** | Permissions and voting edge cases need clear specs |
| **Best for** | First-time SDD learners |

---

## The Concept

QuickRetro is a team retrospective board. Teams use it after a sprint to reflect on what happened — adding cards to columns (Went Well, To Improve, Action Items), voting to surface the most important items, and tracking action items to completion.

Key elements:
- **Retro sessions** with a title and date
- **Three columns**: 🟢 Went Well, 🟡 To Improve, 🔵 Action Items
- **Cards** that team members add to each column
- **Voting** to surface the most important items
- **Pre-defined team members** (no authentication in this version)

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a lightweight web application focused on simplicity, readability, and maintainability. Prioritize minimal dependencies, clear separation of concerns, comprehensive test coverage, and accessible UI. The application should work without a build step where possible. Avoid over-engineering — no abstractions until the third use case demands it.
```

**Checkpoint** — verify the generated `.specify/memory/constitution.md` includes:
- [ ] Code quality and simplicity guidelines
- [ ] Testing expectations
- [ ] Architectural constraints (minimal dependencies, no premature abstraction)
- [ ] UI/UX principles

---

### Specification

```
/speckit.specify Build QuickRetro, a team retrospective board application. When the app launches, it displays a list of pre-defined team members (4 people: two engineers, one designer, one product manager) to select from — no password required. After selecting a user, you see a list of retro sessions. Clicking a session opens the retro board with three columns: "Went Well," "To Improve," and "Action Items." Any team member can add cards to any column. Cards show the author name and creation time. Each team member can vote once per card using a thumbs-up button — you cannot vote on your own card. Cards are sorted by vote count (highest first) within each column. You can only edit or delete cards you created. Action Item cards have an additional "Mark Complete" checkbox that anyone can toggle. There should be 2 sample retro sessions pre-loaded with 3-5 cards each, distributed across all columns.
```

**Deliberate ambiguities to watch for:**
- Can a user create new retro sessions, or are they admin-only?
- What happens when all action items are marked complete?
- Is there a limit on card length?
- Are votes anonymous to other users?
- Can you reopen a "completed" retro session?

**Checkpoint** — verify the generated spec contains:
- [ ] User stories with acceptance criteria
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguous areas
- [ ] A review and acceptance checklist

---

### Clarification

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

**Manual refinement** — add details the AI missed:

```
For the pre-loaded sample data: create one retro titled "Sprint 23 Retro" and another titled "Q4 Planning Retro." Distribute sample cards across all three columns with varied vote counts so the sorting is visible. Ensure at least one action item is already marked as complete in the sample data.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] Clear user stories with testable acceptance criteria
- [ ] Sample data requirements defined
- [ ] Edge cases explicitly addressed

---

### Plan

```
/speckit.plan Use vanilla HTML, CSS, and JavaScript with no build tools or frameworks. Store all data in the browser using localStorage. The app should be a single index.html file with linked CSS and JS files. Keep it simple — no bundlers, no transpilers, no package managers needed for the frontend.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | High-level implementation plan with phases |
| `data-model.md` | Data structures for sessions, cards, votes |
| `research.md` | Technical research (localStorage limits, drag-drop APIs) |
| `quickstart.md` | Key validation scenarios |

**Validate the plan:**

```
Review the implementation plan and check: (1) Are there any over-engineered components that violate our constitution's simplicity principle? (2) Does every technical choice trace back to a requirement in the spec? (3) Is the phase ordering logical — can each phase be validated independently?
```

**Checkpoint:**
- [ ] Tech stack matches what you specified (vanilla HTML/CSS/JS + localStorage)
- [ ] No unnecessary dependencies or abstractions
- [ ] Data model covers all entities: sessions, cards, users, votes

---

### Tasks

```
/speckit.tasks
```

**What to observe in `tasks.md`:**
- Tasks grouped by user story
- Dependency ordering — data models before services, services before UI
- `[P]` markers for tasks that can run in parallel
- File paths for each task
- Checkpoints between phases

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- The AI follows the task order from `tasks.md`, not its own improvised order
- Generated code references back to spec requirements
- The data model matches `data-model.md`
- No features are added that weren't in the specification

---

## Extension Activities

### Add a Feature

Add a "Timer" feature using the full SDD workflow:

```
/speckit.specify Add a "Timer" feature to QuickRetro. When a retro session is active, the facilitator can start a countdown timer (configurable: 5, 10, or 15 minutes) that is visible to all participants. When the timer expires, a notification appears. The timer is per-column — the facilitator advances through columns with the timer.
```

Then continue through `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Rebuild with a Different Tech Stack

Same spec, different implementation — demonstrates SDD's tech independence:

```
/speckit.plan Rebuild QuickRetro using React with TypeScript. Use Vite as the build tool. Store data in a local SQLite database via sql.js (WASM). Create a component-based architecture with proper state management using React Context.
```
