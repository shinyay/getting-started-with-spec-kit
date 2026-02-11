# Scenario N: Kanban Task Board with Server Persistence

| | |
|---|---|
| **Level** | ⭐⭐ Intermediate |
| **Duration** | ~100 min |
| **Key SDD themes** | Multi-entity relationships, ordering algorithms (fractional indexing), cascade operations |
| **Why it tests SDD** | "Just move the card" hides a complex ordering problem — without specifying how positions are stored, compared, and rebalanced, the AI will produce code that breaks on reload or concurrent use |
| **Best for** | Developers learning to specify data relationships and ordering as explicit contracts |

---

## The Concept

You are building a Kanban task board — boards contain columns, columns contain cards, and users can drag cards between columns. Simple CRUD, right?

Except:
- How do you persist card order? Array indices break on concurrent inserts. Database `ORDER BY` needs a sortable field. What type — integer, float, string?
- When you delete a column, what happens to its cards? Are they deleted? Moved? The user must choose — and the API must enforce it.
- When you move a card to position 3, what position value does it get? The client shouldn't compute this — the server should.
- If two users move cards simultaneously, can positions collide? How do you recover?

This scenario teaches that **ordering is data, not UI** — it must be specified, persisted, and survive page reload. And that **cascading operations must be explicit** — "delete a column" is three different operations depending on what the spec says about its cards.

This is the same skill that appears at higher difficulty in:
- Scenario E (⭐⭐⭐⭐): Collaborative z-index ordering with real-time conflict resolution
- Scenario B (⭐⭐⭐): Offline sync of ordered items across devices

**Tech stack:** Node.js + Express + SQLite (see [Intermediate Baseline Contract](#intermediate-baseline-contract) in WORKSHOP.md)

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a Kanban task board with server-persisted ordering. Prioritize: ordering is data, not UI (positions must be persistable, deterministic, and survive reload), cascading operations are explicit (deleting a column defines what happens to its cards — the user must choose), API-first (the board works entirely via API; the client sends intent like "move after card X" and the server computes positions), no data loss (confirmation for destructive operations; undo where feasible), consistent state (no orphan cards, no duplicate positions; foreign keys enforced), and testability (unit tests for ordering algorithm; integration tests for cascading).
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Ordering as a first-class data concern
- [ ] Explicit cascading policy for column deletion
- [ ] API-first: client sends intent, server computes positions
- [ ] Foreign key enforcement
- [ ] Testing requirements for ordering algorithm

---

### Specification

```
/speckit.specify Build KanbanFlow — a task board API with drag-and-drop ordering.

Data model:
- Board: id, title, createdAt, updatedAt
- Column: id, boardId (FK → Board), title, position (REAL), createdAt, updatedAt
- Card: id, columnId (FK → Column), title, description (plain text v1), position (REAL), dueDate (YYYY-MM-DD, optional), createdAt, updatedAt
- Label: id, boardId (FK → Board), name, color (palette: red, orange, yellow, green, blue, purple, gray)
- card_labels: cardId (FK → Card), labelId (FK → Label), PRIMARY KEY (cardId, labelId)

DB constraint: UNIQUE(columnId, position) on cards table. UNIQUE(boardId, position) on columns table. If violated during move, server retries position computation or triggers rebalance.

Fractional indexing for ordering:
- New items start at positions 1000, 2000, 3000, ... (large initial gaps).
- Insert between position 1000 and 2000 → position 1500.
- Rebalance trigger: gap between adjacent positions < 1.0.
- Rebalance: renumber all items in the container to 1000, 2000, 3000, ... within a single transaction.
- Rebalance response: server returns updated positions for ALL items in the affected container.

API endpoints:
- GET /api/boards/:id — full board hydration: board + columns (ordered by position ASC) + cards per column (ordered by position ASC). Stable sort: on position tie, secondary sort by id ASC. Response shape: { board: { ...fields, columns: [{ ...fields, cards: [...] }] } }.
- POST /api/boards — create board.
- POST /api/columns — create column in board (server assigns next position).
- PATCH /api/columns/:id — update column title or move column (with afterColumnId for position intent).
- POST /api/columns/:id/archive — archive column with action. Body: { "action": "delete" } deletes column and all its cards. Body: { "action": "move", "targetColumnId": "..." } moves all cards to target column, then deletes the original column. Both operations in a single transaction. Missing/invalid body → 400.
- POST /api/cards — create card in column (server assigns next position).
- PATCH /api/cards/:id — update card fields OR move card. Move intent: { columnId, afterCardId: "xyz" } places card after xyz. { columnId, afterCardId: null } places at beginning. { columnId } alone (no afterCardId key) places at end.
- DELETE /api/cards/:id — delete single card. Returns 204.

Client sends intent, server computes position:
- Client does NOT compute fractional positions.
- Move requests specify afterCardId (or afterColumnId for columns).
- Server looks up the position of afterCardId and the next card, computes midpoint.
- Response always includes the card's new computed position.

Foreign key enforcement:
- PRAGMA foreign_keys = ON in every connection.
- Card.columnId → Column.id (NO CASCADE — cascading is application-level via POST /api/columns/:id/archive).
- Column.boardId → Board.id (CASCADE on board delete).
- card_labels join table with FK constraints.
- All multi-table operations in transactions.

Sample data:
- 1 board with 3 columns ("To Do", "In Progress", "Done")
- 6 cards distributed across columns with varied positions
- 3 labels (Bug/red, Feature/blue, Urgent/orange) assigned to some cards

Scope tiers:
- MVP (required): Board + columns + cards CRUD + intent-based ordering API + simple UI with Move Up/Down/To Column buttons. API-first; ordering is visible without drag-and-drop.
- Core (recommended): + Drag-and-drop UI + labels + due dates + filter by label/search.
- Stretch (optional): + Keyboard movement (Ctrl+arrows) + URL-based filter sharing + bulk column operations + undo (soft-delete with 30s restore).
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: When a card is moved to an empty column, what position value does it get?
2. Decision needed: Is there a maximum number of cards per column or per board?
3. Decision needed: Can a card have multiple labels?
4. Decision needed: When a column is deleted, must the user choose move-or-delete, or is there a default?
5. Decision needed: Should card descriptions support markdown or plain text only?
6. Decision needed: When does rebalance happen — automatically on threshold, or only via explicit endpoint?
7. Decision needed: Can you undo a card deletion? If so, what's the time window?
8. Decision needed: Should the full board load in one API call or separate calls per column?
9. Decision needed: Due date display — relative ("in 2 days"), absolute ("Feb 12"), or both?
10. Decision needed: What happens if the target column in a "move cards" archive is also being deleted simultaneously?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/N-kanban-board-answers.md`](_answers/N-kanban-board-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] Data model with all entities and relationships
- [ ] Position type (REAL) and fractional indexing strategy
- [ ] Full board hydration endpoint with response shape
- [ ] Cascade delete API with both action types
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguities above
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify
```

Review the questions surfaced by Spec Kit. Use the deliberate ambiguity list above as a checklist — did the AI catch all 10? If not, add the missed ones manually.

**Manual refinement** — add details the AI missed:

```
For sample data: the 6 cards should have non-sequential positions (e.g., 1000, 2500, 3000) to demonstrate that ordering works by position value, not insertion order. At least one card should have a due date set to tomorrow. Assign labels to 3 of the 6 cards.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] All 10 decision questions resolved
- [ ] Cascade behavior unambiguous
- [ ] Rebalance trigger and response defined
- [ ] Position semantics (REAL, large gaps, midpoint calculation) explicit

---

### Plan

```
/speckit.plan Use Node.js with Express and better-sqlite3. Follow the Intermediate Baseline Contract. Fractional indexing positions stored as REAL with large initial gaps (1000, 2000, 3000). Rebalance is automatic when gap < 1.0, runs in same transaction. Foreign keys ON, all cascade operations in transactions. Client sends intent (afterCardId), server computes position midpoint.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Architecture + middleware strategy |
| `data-model.md` | All 5 tables with constraints, FK relationships |
| `research.md` | Fractional indexing, rebalance algorithms |
| `quickstart.md` | API contract test scenarios |

**Validate the plan:**

```
Review the plan and check: (1) Is position stored as REAL with UNIQUE constraint per container? (2) Does the midpoint calculation handle the empty-column case? (3) Is rebalance in the same transaction as the move? (4) Does the cascade delete use a transaction? (5) Are there contract tests for each move scenario (after specific card, beginning, end)?
```

**Checkpoint:**
- [ ] UNIQUE(columnId, position) constraint defined
- [ ] Rebalance is transactional, not a separate request
- [ ] Cascade operations are application-level (not DB CASCADE)
- [ ] Move API: client sends intent, server computes position

---

### Tasks

```
/speckit.tasks
```

**What to observe:**
- Fractional indexing helper is an early, independently-testable task
- Board hydration is a single endpoint returning nested data (not N+1 queries)
- Cascade delete has its own task with transaction boundary defined
- Move/reorder tasks come after basic CRUD
- MVP / Core / Stretch ordering respected

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Focus on the ordering algorithm — are there test cases for: insert at beginning, insert at end, insert between two items, insert into empty column, rebalance trigger?

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- `PRAGMA foreign_keys = ON` is set on every connection
- Position is REAL, not INTEGER
- UNIQUE(columnId, position) constraint exists
- Move endpoint accepts `afterCardId` intent (not raw position values)
- Cascade delete is in a single transaction
- Board hydration uses JOINs or subqueries (not N+1)
- Rebalance happens in the same transaction as the triggering move

---

## Extension Activities

### Add a Feature: Card Checklists

Nested data within nested data: Board → Column → Card → Checklist → Item. How does the ordering spec extend to checklist items? Does the board hydration endpoint include checklists, or is it a separate call?

```
/speckit.specify Add checklists to KanbanFlow cards. Each card can have one checklist containing ordered items. Items can be checked/unchecked. The card detail view shows progress (3/5 items done). How does this affect the board hydration endpoint? Should checklist items use fractional indexing too?
```

Then continue through `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test: Real-time Sync

What happens when two users edit the same board? Concurrent position updates, column deletions while a move is in flight. This bridges directly to Scenario E (collaborative design tool).

```
/speckit.specify Add real-time sync to KanbanFlow. When user A moves a card, user B sees it update immediately. When two users move cards simultaneously, how are conflicts resolved? What happens if user A deletes a column while user B is moving a card into it?
```
