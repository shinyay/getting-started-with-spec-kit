# Scenario A: QuickRetro — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Permission Matrix (Expected Output)

A well-run SDD process should produce a permission matrix similar to this:

| Action | Own Card | Other's Card | Any Card |
|---|---|---|---|
| Create | ✅ (any column) | — | — |
| Read | ✅ | ✅ | ✅ |
| Edit text | ✅ | ❌ | — |
| Delete | ✅ | ❌ | — |
| Vote | ❌ (self-vote blocked) | ✅ (once per card) | — |
| Un-vote | — | ✅ (toggle off) | — |
| Mark Complete | — | — | ✅ (Action Items only) |

Key decisions embedded in this matrix:
- **Edit/Delete** is author-only — no admin override in v1
- **Self-vote** is blocked per card, not per column — you CAN vote on other cards in a column where you authored a card
- **Un-vote** is allowed (toggle behavior) — simpler UX than "vote is permanent"
- **Mark Complete** is open to any team member — the whole team owns action items
- **Voting on edited cards**: votes are preserved when card text is edited (see Reference Answer #7)

## Voting Rules Summary

| Rule | Behavior |
|---|---|
| Votes per user per card | Exactly 1 (toggle: click to vote, click again to un-vote) |
| Self-vote | Blocked — button disabled with tooltip |
| Vote visibility | Visible — clicking count shows voter names |
| Votes on edit | Preserved — editing text doesn't reset votes |
| Votes on delete | Removed — deleting a card removes all its votes |
| Sort order | Highest vote count first; ties broken by creation time (oldest first) |

## Session Lifecycle

```
Active → (archive) → Archived
                          ↓
                    Read-only: cards visible, voting disabled,
                    no new cards, no edits, no deletes
                    (session stays in list, grayed out)
```

- **Active** sessions: full CRUD + voting
- **Archived** sessions: read-only view, grayed in list, cannot be re-activated in v1
- Sessions **cannot be deleted** — only archived

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Session creation | Any team member can create sessions | No admin concept in a beginner app — keep it simple |
| 2 | Card character limit | 280 characters, enforced on input (counter + truncation) | Mirrors tweet-length; enforcing on input prevents frustrating "submit rejected" |
| 3 | Vote visibility | Visible — show who voted | Transparency builds trust in retros; anonymous voting adds complexity |
| 4 | Un-vote | Yes — toggle behavior (click to vote, click to un-vote) | Simpler mental model than "permanent vote"; prevents accidental vote lock-in |
| 5 | All action items complete | Show a "🎉 All done!" banner on the session board; no auto-archive | Visual reward without surprising state changes |
| 6 | Archive behavior | Read-only: cards visible, voting/editing disabled, session grayed in list | "Hidden" is confusing ("where did my session go?"); read-only is predictable |
| 7 | Votes on edit | Preserved — votes are for the idea, not the exact text | Resetting votes punishes the author for fixing a typo |
| 8 | Move cards between columns | Not in v1 — cards stay in the column where created | Moving cards adds drag-drop complexity; keep beginner scope focused |
| 9 | Multi-tab sync | No auto-sync; last-write-wins with manual refresh | Real-time sync (WebSocket/storage events) is a significant complexity leap for beginners |
| 10 | Card limit | No hard limit in v1; UI degrades gracefully (scrollable column) | Enforcing limits adds validation logic; localStorage will naturally cap at ~5 MB |

## Facilitator Notes

- **After Constitution**: "This constitution is 4–5 principles. Compare with Scenario D (billing): 12 principles. A constitution should match the project's risk profile — QuickRetro has no money, no auth, no compliance."
- **After Specify**: "Did the generated spec produce a permission matrix? If not, who decides whether you can vote on your own card? The AI decided — and you don't know what it chose."
- **After Clarify**: "The un-vote question (#4) seems trivial. But imagine the AI assumed votes are permanent. Users click the wrong card, can't undo, get frustrated. A one-line spec decision prevents a UX bug."
- **After Plan**: "Check: is permission logic in one place (a `canEdit(user, card)` function), or scattered across click handlers? Centralized permission logic is the #1 thing beginners miss in their plans."
- **After Implement**: "Count the permission checks in the generated code. Are they consistent? Does the 'edit' button check the same condition as the 'delete' button? Inconsistent permission checks are the most common beginner implementation bug."
