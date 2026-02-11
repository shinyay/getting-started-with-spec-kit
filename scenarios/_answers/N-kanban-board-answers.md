# Scenario N: Kanban Board — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## API Contract Summary (Expected Output)

| Method | Path | Success | Error |
|---|---|---|---|
| GET | `/api/boards/:id` | 200 (full hydration) | 404 |
| POST | `/api/boards` | 201 | 400 |
| POST | `/api/columns` | 201 | 400, 404 (board) |
| PATCH | `/api/columns/:id` | 200 | 400, 404 |
| POST | `/api/columns/:id/archive` | 200 | 400, 404, 409 (conflict) |
| POST | `/api/cards` | 201 | 400, 404 (column) |
| PATCH | `/api/cards/:id` | 200 | 400, 404, 409 (position conflict) |
| DELETE | `/api/cards/:id` | 204 | 404 |

Key implementation details:
- **Position type:** REAL with UNIQUE(columnId, position) constraint
- **Initial gaps:** 1000, 2000, 3000 — rebalance only when gap < 1.0
- **Move intent:** Client sends `afterCardId`, server computes midpoint position
- **Cascade delete:** Application-level in a single transaction (NOT DB CASCADE)
- **Column archive:** Uses POST (not DELETE-with-body) for maximum tooling compatibility

## Fractional Indexing Quick Reference

| Operation | Position Calculation |
|---|---|
| Insert at end of column | Last card position + 1000 (or 1000 if empty) |
| Insert at beginning | First card position / 2 |
| Insert between A and B | (A.position + B.position) / 2 |
| After 50 inserts between same neighbors | Gap may approach 1.0 → trigger rebalance |
| Rebalance | Renumber all items: 1000, 2000, 3000, ... in one transaction |

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Empty column position | 1000 (first standard position) | Consistent with large-gap strategy |
| 2 | Max cards per column | No hard limit in v1 (spec this as Stretch) | Workshop simplicity |
| 3 | Multiple labels per card | Yes — via card_labels join table | Already in data model; teaches many-to-many |
| 4 | Column delete default | No default — action is required in body | Prevents accidental data loss |
| 5 | Description format | Plain text v1; markdown is Stretch | Avoid markdown rendering complexity at ⭐⭐ |
| 6 | Rebalance trigger | Automatic when gap < 1.0, in same transaction | Transparent to client; workshop-safe |
| 7 | Undo card deletion | Stretch feature — soft-delete with 30s restore window | Core: hard delete; Stretch: undo |
| 8 | Full board in one call | Yes — single GET /api/boards/:id returns everything | Avoids N+1; teaches hydration pattern |
| 9 | Due date display | API returns YYYY-MM-DD; display format is a UI decision | API contract is format-agnostic |
| 10 | Concurrent delete target | 409 Conflict — transaction serialization catches it | Server rejects; client retries |

## Facilitator Notes

- **After Constitution**: "Principle #1 'ordering is data' is the core lesson. Ask: how would you implement card ordering without reading the spec? Most will say array index — which breaks on concurrent inserts."
- **After Specify**: "Highlight the intent-based move API. The client says 'after card X', not 'position 1500'. This is API-first thinking."
- **After Clarify**: "The cascade question reveals whether teams think about data integrity. 'Just delete everything' vs 'ask the user' is a product decision that must be in the spec."
- **After Plan**: "Check if rebalance is in the same transaction as the move. If it's a separate request, what happens if the server crashes between them?"
- **Common mistake**: Teams forget UNIQUE constraint on position — leads to tie-breaking bugs that surface only with >10 cards.
