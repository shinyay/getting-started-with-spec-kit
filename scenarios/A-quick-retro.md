# Scenario A: QuickRetro — Team Retrospective Board

| | |
|---|---|
| **Level** | ⭐ Beginner |
| **Duration** | ~90 min |
| **Key SDD themes** | CRUD, permissions, voting logic |
| **Why it tests SDD** | Permissions and voting edge cases need clear specs — without them, the AI guesses who can do what |
| **Best for** | First-time SDD learners |

---

## The Concept

QuickRetro is a team retrospective board. Teams use it after a sprint to reflect on what happened — adding cards to columns (Went Well, To Improve, Action Items), voting to surface the most important items, and tracking action items to completion.

Everyone understands CRUD. But CRUD + permissions + voting creates surprising edge cases:

- Who can edit a card — the author only, or anyone?
- Can you vote on your own card? Can you un-vote?
- What happens when you edit a card that already has votes — do the votes stay?
- Is "archived" the same as "read-only"?

This scenario teaches that **permission rules and voting constraints must be explicitly specified**. Without them, the AI makes silent assumptions — and every assumption is a potential bug.

This is the same skill that appears at higher difficulty in:
- Scenario N (⭐⭐): Kanban Board has the same columns-and-cards structure but adds server-side API contracts and positional ordering
- Scenario C (⭐⭐⭐): OIDC SSO + RBAC turns "who can do what" into enterprise-grade role hierarchies across tenants

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a lightweight web application focused on simplicity, readability, and maintainability. Prioritize minimal dependencies, clear separation of concerns, comprehensive test coverage, and accessible UI. The application should work without a build step where possible. Avoid over-engineering — no abstractions until the third use case demands it.
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Code quality and simplicity guidelines
- [ ] Testing expectations
- [ ] Architectural constraints (minimal dependencies, no premature abstraction)
- [ ] UI/UX principles

---

### Specification

```
/speckit.specify Build QuickRetro — a team retrospective board for sprint reflection.

User selection:
- On launch, display 4 pre-defined team members (2 engineers, 1 designer, 1 product manager) as selection cards — no password required.
- Selected user persists in the browser session until explicitly switched via a "Switch User" button in the header.

Retro sessions:
- Session has: title (string, required), date (YYYY-MM-DD), status (active | archived).
- Session list view shows all sessions sorted by date (newest first).
- Any team member can create a new session with a title and optional date (defaults to today).

Board & columns:
- Three fixed columns: 🟢 "Went Well", 🟡 "To Improve", 🔵 "Action Items".
- Columns are structural — they cannot be renamed, reordered, or added/removed.
- Cards display: text content, author name, creation timestamp, vote count with thumbs-up button.
- Cards sorted by vote count (highest first) within each column. Ties broken by creation time (oldest first).

Card rules:
- Any team member can add a card to any column.
- Card text is plain text only (no markdown, no HTML).
- Only the card author can edit or delete their own cards.

Voting:
- Each team member can vote once per card using a thumbs-up button.
- You cannot vote on your own card — the button is disabled with a tooltip "Can't vote on your own card."
- Votes are visible — clicking the vote count shows the list of voters.

Action items:
- Action Item column cards have an additional "Mark Complete" checkbox.
- Any team member can toggle the checkbox (not restricted to author).
- Completed action items show with strikethrough text and a ✅ indicator.

Sample data:
- Session 1: "Sprint 23 Retro" — 5 cards across all three columns with varied vote counts so sort order is visible.
- Session 2: "Q4 Planning Retro" — 3 cards across columns.
- At least one action item already marked complete in sample data.
- At least one card with 0 votes and one with 3+ votes (to demonstrate sorting).

Scope tiers:
- MVP (required): User selection + session list + board with 3 columns + add/view cards + sample data
- Core (recommended): + Voting (one per user, no self-vote, sort by votes) + edit/delete own cards + Action Item checkbox
- Stretch (optional): + Create new sessions + archive sessions + card character limit enforcement + voter list display
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: Can a user create new retro sessions, or is session management admin-only?
2. Decision needed: Is there a character limit on card text? If so, what limit, and is it enforced on input or on submit?
3. Decision needed: Are votes anonymous or visible (show who voted)?
4. Decision needed: Can you un-vote (remove your vote) after voting on a card?
5. Decision needed: What happens when all action items in a session are marked complete — any visual indicator or session state change?
6. Decision needed: Can a retro session be archived? If so, what does "archived" mean — read-only, or hidden from the main list?
7. Decision needed: What happens to votes if the card author edits the card text — are votes preserved or reset?
8. Decision needed: Can cards be moved between columns (e.g., "To Improve" → "Action Items"), or only added to a specific column?
9. Decision needed: If two browser tabs are open on the same session and one adds a card, does the other tab see it without manually refreshing?
10. Decision needed: Is there a maximum number of cards per column or per session, or is it unbounded?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/A-quick-retro-answers.md`](_answers/A-quick-retro-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] User stories with acceptance criteria
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguous areas
- [ ] Permission matrix (who can edit, delete, vote on what)
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify
```

Review the questions surfaced by Spec Kit. Use the deliberate ambiguity list above as a checklist — did the AI catch all 10? If not, add the missed ones manually.

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
- [ ] All 10 deliberate ambiguities have documented resolutions
- [ ] Clear user stories with testable acceptance criteria
- [ ] Sample data requirements defined
- [ ] Edge cases explicitly addressed (vote on own card, edit preserves votes, etc.)

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
Review the implementation plan and check: (1) Are there any over-engineered components that violate our constitution's simplicity principle? (2) Does every technical choice trace back to a requirement in the spec? (3) Is the phase ordering logical — can each phase be validated independently? (4) Is the permission logic (who can edit/delete/vote) centralized, not scattered across UI event handlers?
```

**Checkpoint:**
- [ ] Tech stack matches what you specified (vanilla HTML/CSS/JS + localStorage)
- [ ] No unnecessary dependencies or abstractions
- [ ] Data model covers all entities: sessions, cards, users, votes
- [ ] Permission logic is a defined module, not ad-hoc

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
- MVP / Core / Stretch ordering is respected

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Run `/speckit.analyze` after tasks to check cross-artifact consistency. It validates that every spec requirement has a corresponding task, and every task traces back to the spec. Optional but especially valuable for beginners learning to trust the SDD process.

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- The AI follows the task order from `tasks.md`, not its own improvised order
- Generated code references back to spec requirements
- The data model matches `data-model.md`
- Permission checks (edit/delete/vote) are centralized, not duplicated
- No features are added that weren't in the specification
- No features outside the specified scope tier

---

## Extension Activities

### Add a Feature: Timer

Add a "Timer" feature using the full SDD workflow:

```
/speckit.specify Add a "Timer" feature to QuickRetro. When a retro session is active, the facilitator can start a countdown timer (configurable: 5, 10, or 15 minutes) that is visible to all participants. When the timer expires, a notification appears. The timer is per-column — the facilitator advances through columns with the timer.
```

Then continue through `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test: Multi-Team Support

What happens when "one team" becomes "many teams"? This challenges the "flat user list" assumption:

```
/speckit.specify Update QuickRetro to support multiple teams. Each team has its own set of members and retro sessions. A user can belong to multiple teams. The session list is filtered by the selected team. Team management (create team, add/remove members) is restricted to team admins. How does this affect the voting and permission rules — can a user from Team A see Team B's retros?
```

Re-run `/speckit.clarify` to discover new ambiguities: cross-team visibility, admin permissions, user-team assignment. This demonstrates how a "simple" organizational change cascades through permissions, data model, and UI.
