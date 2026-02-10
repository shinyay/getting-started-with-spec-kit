# Scenario E: Real-time Collaborative Whiteboard

| | |
|---|---|
| **Level** | ⭐⭐⭐⭐ Advanced |
| **Duration** | ~120 min |
| **Key SDD themes** | Concurrency, consistency models (CRDT/OT), real-time state, latency budgets, reconnection |
| **Why it tests SDD** | Concurrent editing + consistency + latency constraints cannot be improvised; unspecified conflict semantics = diverging clients |
| **Best for** | Developers building real-time/collaborative features; anyone interested in distributed systems at the client level |

---

## The Concept

Multiple users simultaneously draw on a shared whiteboard — pen strokes, shapes, sticky notes, text — and see each other's cursors and edits in real-time. Users can go offline and re-sync. The system must converge to the same state on all clients without losing edits.

This scenario stress-tests SDD because:
- **Concurrency is the default state** — every operation races with every other user's operations
- **Consistency model is an architectural decision** that must be made in the spec/plan phase (CRDT vs OT vs authoritative server), not discovered during implementation
- **Undo/redo across multiple users** is a famously hard problem that needs explicit specification
- **Latency is perceptible** — users notice >100ms delay; the spec must define quantitative latency budgets
- **Object types have different conflict semantics** — two users moving a shape ≠ two users editing the same sticky note text

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create a constitution for a real-time collaborative whiteboard feature.

Non-negotiables:
- Consistency convergence: when two users modify the same object simultaneously, both edits must be preserved (no silent overwrites). All clients must converge to the same state.
- Latency budget: local operations must render immediately (<16ms / same frame). Remote operations must propagate to all connected clients within 200ms (95th percentile) under normal network conditions.
- Handle network interruptions gracefully: reconnect, rehydrate state, no data loss. Edits made offline must be buffered and synced on reconnect.
- Graceful degradation: if the real-time connection degrades, the app continues to function with increased latency rather than failing entirely.
- Data durability: board state must be persisted durably. A server crash must not lose more than 5 seconds of edits.
- Scalability targets: support boards with up to 50 concurrent users and up to 10,000 objects without degradation.
- Performance: limit payload sizes; batch high-frequency updates; avoid unbounded memory growth. Presence updates (cursors) use a separate, lossy channel.
- Security: board access control (owner/collaborator/viewer), invite-link safety (revocable, optionally expiring), and protection against abusive payloads (rate limiting, max object counts).
- Testing: include concurrency-focused tests, reconnection simulation, out-of-order message handling, and large-board performance tests.
- Observability: track operation latency (p50/p95/p99), message rates, active connections, error rates, and state divergence detection.
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Consistency convergence guarantee (no silent overwrites)
- [ ] Quantitative latency budget (<16ms local, <200ms remote p95)
- [ ] Network interruption / reconnection handling
- [ ] Data durability guarantee
- [ ] Scalability targets (50 users, 10,000 objects)
- [ ] Security and rate limiting
- [ ] Observability requirements

---

### Specification

```
/speckit.specify Build a collaborative whiteboard where multiple users can draw and see each other's changes in real-time.

Users:
- Board Owner: creates boards, manages access, can delete any object.
- Collaborator (invited via email or share link): full editing access within the board.
- Viewer (read-only link): can see the board and cursor positions but cannot edit. Can export.

Board model:
- The canvas is infinite and pannable/zoomable. Coordinates are in a world-space system independent of viewport.
- Objects have a z-order (stacking). Users can bring objects forward/backward.
- Maximum 10,000 objects per board (soft limit with warning at 8,000).

Object types and their properties:
- Pen stroke: array of points with pressure, color, thickness. Immutable once the stroke ends (no partial editing).
- Highlighter stroke: same as pen but semi-transparent. Immutable once drawn.
- Eraser: removes objects it intersects (object-level eraser, not pixel-level).
- Shape (rectangle, ellipse, arrow, line): position, size, rotation, color, fill, border. Editable after creation (move, resize, recolor).
- Sticky note: position, size, background color, text content (rich text: bold, italic, bullet list). Editable after creation.
- Text: position, font, size, color, content. Editable after creation.

Drawing tools:
- Pen, highlighter, eraser, shape picker, sticky note, text, selection tool.
- Selection tool: click to select one object, drag to select multiple. Selected objects can be moved, resized, deleted, or recolored as a group.

Presence:
- See all connected users' cursors with their name labels, color-coded.
- See which object each user currently has selected (selection highlight).
- Presence updates are high-frequency and lossy (latest position wins).

Collaboration / conflict handling:
- Two users drawing new strokes simultaneously: no conflict (independent objects created).
- Two users moving the same shape simultaneously: last-writer-wins on position, but both moves are visible in real-time (no snapping/jumping). The final position is the last received.
- Two users editing the same sticky note text simultaneously: character-level merging (both edits preserved, like Google Docs). If this is too complex for v1, use object-level locking — when one user starts editing text, others see a lock indicator and cannot edit that text until the first user finishes.
- User A deletes an object while User B is moving it: deletion wins. User B sees the object disappear. User B's move operation is discarded.

Undo/redo:
- Each user has their own undo/redo stack scoped to their actions.
- Undo reverses the user's last action (create, move, resize, delete, text edit).
- If a user undoes a "create stroke" but another user has since moved or annotated near that stroke, the undo still removes it (no causal dependency tracking in v1).
- Redo re-applies the undone action if it is still valid (e.g., re-creating a deleted stroke at its original position).
- Maximum undo depth: 50 actions per user.

History:
- Board state is autosaved every 5 seconds and on every user disconnect.
- A version history of the last 100 snapshots is kept. Board Owner can restore to a previous snapshot (overwrites current state for all users with a confirmation dialog).

Permissions:
- Owner can invite collaborators (email or share link), revoke access, and set board to read-only.
- Share links can be set to "Collaborator" or "Viewer" access. Links are revocable and optionally expire.
- Revoking access while a user is connected: disconnect them immediately with a notification.

Export:
- Export current board as PNG (rasterized at 2x resolution) or PDF (vector where possible).
- Export reflects the current state at the moment of export, consistent across all clients.

Acceptance criteria:
- With 10 concurrent collaborators, drawing remains smooth (60fps locally) and updates propagate within 200ms (p95).
- Reconnect after network interruption does not duplicate objects or lose edits made offline.
- Undo/redo behaves predictably per the rules above — undoing a stroke removes it even if other users have since added objects nearby.
- Export includes the latest state and produces identical output regardless of which client triggers it.
- A Viewer cannot create, modify, or delete any object (enforced server-side, not just UI).

Edge cases to explicitly cover:
- User disconnects mid-stroke (partial drawing): discard the incomplete stroke; do not persist half-drawn paths.
- Board Owner revokes collaborator access while the collaborator is actively drawing: disconnect immediately; discard any buffered-but-unsynced operations from the revoked user.
- Rapid successive edits from one user (e.g., fast freehand drawing): batch into a single message per animation frame, not per point.
- Very large board (approaching 10,000 objects): show a warning banner; degrade rendering (hide objects far from viewport) rather than crashing.
- Two users create objects at the exact same position: both objects exist (overlapping); z-order determined by creation timestamp.
- User with slow connection joins a large board: progressive loading (load viewport-visible objects first, then background-load the rest).

Non-goals (explicitly out of scope):
- Real-time audio/video communication (use a separate tool).
- Image/file embedding on the whiteboard (future iteration).
- Handwriting recognition or shape auto-correction.
- Mobile/touch-optimized UI (desktop-first for v1).
```

**Deliberate ambiguities to watch for:**
- How should the text cursor behave when two users edit the same sticky note? (blinking cursor position conflicts)
- What happens to a user's undo stack when they disconnect and reconnect?
- Can a Board Owner undo another user's actions?
- How is z-order conflict resolved when two users reorder the same object simultaneously?
- What is the invite email flow? (accept link, create account if needed?)

**Checkpoint** — verify the generated spec contains:
- [ ] User stories with acceptance criteria
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguous areas
- [ ] Object type definitions with properties
- [ ] Conflict handling rules per object type
- [ ] Undo/redo behavior rules
- [ ] A review and acceptance checklist

---

### Clarification

```
/speckit.clarify Review the collaborative whiteboard spec and ask me about every ambiguity, unstated assumption, and gap — especially around: concurrent text editing behavior (locking vs merging), undo stack persistence across reconnects, Board Owner undo powers, z-order conflict resolution, invite flow details, and any concurrency edge cases you can identify.
```

Suggested answers for the workshop:

| Question Theme | Suggested Answer |
|---|---|
| Concurrent text editing (v1) | Use object-level locking for v1. When a user double-clicks a sticky note or text to edit, they acquire a lock. Other users see a lock icon and the editor's name. Lock auto-releases after 30 seconds of inactivity or when the user clicks away. If the lock holder disconnects, the lock releases after 10 seconds. |
| Undo stack on reconnect | Undo stack is kept in client memory only. On reconnect, the stack is cleared (fresh start). This avoids complex reconciliation of undone operations. |
| Board Owner undo powers | Board Owner cannot undo other users' actions. They can only delete objects or restore to a previous snapshot. |
| Z-order conflicts | Last-writer-wins for z-order changes. If two users reorder the same object simultaneously, the last received z-order value is used. Z-order changes propagate like any other property change. |
| Invite flow | Email invite contains a link with a token. If the recipient has an account, they are added as a collaborator. If not, they must sign up first (the token is preserved). Invite tokens expire after 7 days. |
| Max message size | Individual WebSocket messages are capped at 64KB. Strokes with >1000 points are split across multiple messages. Server rejects messages exceeding the limit. |
| Board deletion | Board Owner can delete a board. All collaborators are disconnected and notified. Board data is soft-deleted (recoverable by support for 30 days). |

**Manual refinement:**

```
For sample data: create 2 boards — "Sprint Planning" (owned by Alice, 3 collaborators, ~50 objects including shapes, sticky notes, and pen strokes) and "Architecture Diagram" (owned by Bob, 1 collaborator, ~200 objects, heavy on shapes and text). Include a snapshot history with 3 versions for the first board.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] Conflict handling is defined for every object type
- [ ] Undo/redo rules are explicit and testable
- [ ] Presence protocol is specified (high-frequency, lossy)
- [ ] Reconnection behavior is fully defined (state rehydration, undo stack, buffered ops)
- [ ] All edge cases have defined behaviors

---

### Plan

```
/speckit.plan Create a technical plan for the collaborative whiteboard.

Tech stack:
- Frontend: TypeScript + React, HTML5 Canvas API for rendering (not SVG — performance at 10,000 objects), Vite for build.
- Real-time: WebSocket (ws library on server, native WebSocket on client). Consider Socket.IO for reconnection/fallback if justified.
- Backend: Node.js + Express for REST API, WebSocket server co-located.
- Database: PostgreSQL for board metadata, access control, and user data. Redis for presence state and pub/sub between server instances.
- Object storage: S3-compatible for exported PNGs/PDFs and board snapshots.
- Deployment: Docker, CI/CD via GitHub Actions.

The plan must include:
- Object/state model: typed objects with unique IDs (ULID for ordering), properties per type, z-order, and a version counter per object for conflict detection.
- Consistency strategy: authoritative server model for v1 (server is the source of truth; clients send operations, server validates and broadcasts). Explain why this was chosen over CRDTs for v1 (simpler, sufficient for 50 users, avoids CRDT complexity for text editing). Document the tradeoff: slightly higher latency than pure CRDT but guaranteed convergence.
- Client-side prediction: client applies operations optimistically for instant feedback (<16ms). If server rejects an operation (e.g., stale version, no permission), client rolls back to server state.
- Message protocol: JSON messages over WebSocket. Define message types: operation (create/update/delete), presence (cursor position, selection), ack, snapshot, error. Batch multiple operations per frame (16ms window). Compress large payloads (strokes) with a binary sub-protocol if needed.
- Presence protocol: separate from operations. Throttled to 10 updates/second per user. Lossy (missed presence updates are acceptable). Uses Redis pub/sub for cross-server-instance distribution.
- Reconnection strategy: on disconnect, client buffers operations locally. On reconnect, client sends its last known server sequence number. Server sends a delta (operations since that sequence) or a full snapshot if the delta is too large (>1000 operations).
- Persistence: autosave every 5 seconds (debounced — save on quiescence, not during active drawing). Snapshots stored as compressed JSON in PostgreSQL (boards <1MB) or S3 (larger boards). Version history with configurable retention.
- Object-level locking for text editing: lock table in Redis with TTL. Lock acquisition/release messages over WebSocket. Stale lock detection and auto-release.
- Permission enforcement: server validates every operation against the user's role before applying. REST API for board management (create, invite, revoke). WebSocket for real-time operations.
- Rate limiting: per-user operation rate limit (100 ops/second), per-board total rate limit (500 ops/second), max message size (64KB).
- Rendering architecture: Canvas API with a scene graph. Viewport culling (only render objects in the visible area). Dirty-region repainting for efficiency. Off-screen canvas for export.
- Testing plan: unit tests for operation validation and conflict resolution, integration tests for the full operation cycle (client → server → broadcast → client), concurrency tests with simulated multi-user scenarios, reconnection tests (disconnect mid-operation, reconnect with buffered ops), out-of-order message tests, large-board performance tests (10,000 objects, 50 users), and export consistency tests.
- Rollout: feature flag for whiteboard access, internal dogfooding first, then limited beta with monitoring.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Implementation plan with architecture and phases |
| `data-model.md` | Object types, board schema, operation log, lock table |
| `research.md` | CRDT vs OT vs authoritative server analysis, Canvas performance, WebSocket libraries |
| `contracts/` | WebSocket message schema (with examples), REST API contracts |
| `quickstart.md` | Key validation scenarios |

**Validate the plan:**

```
Review the implementation plan and check: (1) Is the consistency model clearly documented with tradeoffs? (2) Does client-side prediction handle server rejection correctly (rollback)? (3) Is the reconnection strategy efficient for both small and large deltas? (4) Are presence updates separated from operations to avoid congestion? (5) Does the rendering architecture handle 10,000 objects without frame drops?
```

**Checkpoint:**
- [ ] Consistency strategy is chosen and justified (authoritative server for v1)
- [ ] Client-side prediction with optimistic rendering is documented
- [ ] Message protocol is defined with types, batching, and size limits
- [ ] Reconnection uses sequence-based delta sync with snapshot fallback
- [ ] Text editing locking mechanism is specified
- [ ] Rendering uses viewport culling and dirty-region repainting
- [ ] Rate limiting exists at per-user and per-board levels

---

### Tasks

```
/speckit.tasks Break down implementation tasks.

Task preferences:
- Separate client rendering tasks from server sync tasks from persistence tasks.
- Include a dedicated task to define, document, and validate the WebSocket message schema with examples for every message type (this is the contract between client and server — do it first).
- Include a dedicated task for the Canvas rendering engine (scene graph, viewport culling, dirty-region repainting) — this is independent of networking.
- Include a dedicated task for the object-level locking mechanism (acquire, release, stale detection).
- Include a dedicated task for undo/redo stack implementation with tests for the specified rules.
- Include tasks for presence (cursor broadcasting, selection highlighting) separate from object operations.
- Include tasks for soak/perf testing: 50 simulated users on a 10,000-object board for 30 minutes.
- Include tasks for reconnection/offline simulation: disconnect mid-stroke, reconnect with buffered ops, reconnect to a board that changed significantly.
- Include an early "vertical slice" task: one user draws a stroke, it appears on another user's screen, both see each other's cursors. This validates the full pipeline before building out features.
```

**What to observe in `tasks.md`:**
- Message schema definition appears very early (it's the contract)
- Canvas rendering engine is a separate track from WebSocket sync
- "Vertical slice" task validates the full pipeline early
- Presence tasks are separate from operation tasks
- Undo/redo is its own task with explicit test criteria
- Performance/soak tests exist with concrete parameters (50 users, 10K objects, 30 min)
- Reconnection simulation tests cover multiple scenarios

---

### Implement

```
/speckit.implement Execute all tasks in order. After completing the message schema and vertical slice, demonstrate the end-to-end flow (draw on one client, see on another) before proceeding to additional features. Run concurrency tests after implementing the server operation handler.
```

**What to watch for:**
- The AI follows the task order from `tasks.md`
- Message schema is defined before any WebSocket code is written
- Canvas rendering is decoupled from networking (can render locally without a server)
- Operations are validated server-side before broadcast (not just client-side)
- Presence updates use a separate throttled channel
- Undo/redo only affects the current user's actions
- Rate limiting is applied on the server, not just the client

---

## Extension Activities

### Add a Feature: Image and File Embedding

Extend the whiteboard with media support:

```
/speckit.specify Add image and file embedding to the collaborative whiteboard. Users can drag-and-drop or paste images onto the canvas. Images are uploaded to object storage and displayed at their original aspect ratio. Users can resize, move, and delete embedded images like any other object. Support JPEG, PNG, GIF, and SVG formats. Max file size: 10MB. Include thumbnail generation for board snapshots. Consider: how do images interact with the export feature? How does a large image affect real-time sync performance?
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test the Spec: Switch to CRDTs

Challenge the architecture with a fundamental change:

```
A new requirement has emerged: the business wants to support true offline editing — users should be able to edit a board for hours without connectivity and merge all changes when they reconnect, even if other users made conflicting edits during that time. The current authoritative-server model cannot handle this. Update the spec and plan to evaluate switching to a CRDT-based consistency model (e.g., Yjs or Automerge). What changes in the message protocol? How does undo/redo change? What are the tradeoffs in complexity, payload size, and merge semantics?
```

This demonstrates how SDD handles fundamental architectural pivots — the spec forces you to think through consequences before rewriting code.
