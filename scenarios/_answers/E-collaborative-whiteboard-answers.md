# Scenario E: Collaborative Whiteboard — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Consistency Model Summary

| Aspect | v1 Decision | Rationale |
|---|---|---|
| Architecture | Authoritative server | Simpler than CRDT; sufficient for 50 users; guaranteed convergence |
| Client prediction | Optimistic apply + server rollback | <16ms local responsiveness |
| Conflict: shapes | Last-writer-wins on position/properties | Simple, deterministic |
| Conflict: text | Object-level locking | Character-level merge (CRDT) is Stretch complexity |
| Conflict: delete vs move | Delete wins | Prevents ghost objects; user B sees disappearance |

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Text editing: merge or lock? | Object-level locking for v1. Lock on double-click, auto-release after 30s idle or on click-away. Disconnect releases lock after 10s. | Character-level merging requires CRDT — too complex for v1 |
| 2 | Undo stack on reconnect | Clear undo stack on reconnect (client memory only) | Avoids reconciliation of undone operations against new server state |
| 3 | Board Owner undo powers | Cannot undo other users' actions; can delete objects or restore snapshots | Owner undo of others' work creates confusing UX and complex causal chains |
| 4 | Z-order conflicts | Last-writer-wins; z-order changes propagate like property changes | Consistent with shape conflict resolution; simple |
| 5 | Invite flow | Email link with token; existing users added directly; new users sign up first (token preserved); tokens expire in 7 days | Standard invite pattern; token expiry prevents stale links |
| 6 | Max message size | 64KB per WebSocket message; strokes >1000 points split across messages; server rejects oversized | Prevents memory abuse; splitting is transparent to rendering |
| 7 | Board deletion | All collaborators disconnected + notified; soft-delete recoverable by support for 30 days | Prevents accidental permanent loss |
| 8 | Consistency model | Authoritative server for v1 | Simpler than CRDT, sufficient for target scale, avoids text CRDT complexity |
| 9 | Large board progressive loading | Load viewport-visible objects first, background-load rest | Prevents slow-connection users from blocking on full load |
| 10 | Presence channel | Separate lossy channel, throttled to 10 updates/sec per user; Redis pub/sub for cross-instance | Operations need reliability; presence does not — separate channels prevent congestion |

## Failure Model Reference

| Failure | Behavior |
|---|---|
| Client disconnect mid-stroke | Discard incomplete stroke; do not persist half-drawn paths |
| Server restart | Clients reconnect; server sends delta (ops since last seq) or full snapshot |
| Duplicate message | Server deduplicates by operation ID; idempotent application |
| Out-of-order messages | Server applies by sequence number; rejects stale operations |
| Access revoked while drawing | Disconnect immediately; discard buffered-but-unsynced operations |

## Facilitator Notes

- **After Constitution**: "Ask: what's the difference between 'no data loss' (liveness) and 'no duplicate objects' (safety)? Advanced scenarios require both."
- **After Specify**: "The consistency model decision is THE architectural choice. Ask teams to argue for CRDT vs authoritative server before revealing the recommended answer."
- **After Clarify**: "Object-level locking vs character merge is the decision that defines v1 complexity. If a team picks merge, they've committed to CRDT — make sure they understand the implication."
- **After Plan**: "Does the plan separate the operations channel from the presence channel? If not, presence spam will congest operation delivery."
- **Common mistake**: Teams treat undo as global (all users' actions) instead of per-user scoped.
