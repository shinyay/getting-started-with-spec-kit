# Scenario P: Order Fulfillment Saga — Distributed Workflow Orchestrator

| | |
|---|---|
| **Level** | ⭐⭐⭐⭐ Advanced |
| **Duration** | ~120 min |
| **Key SDD themes** | Saga pattern, compensating transactions, timeout semantics, exactly-once processing, long-running state machines |
| **Why it tests SDD** | "Just call the services in order" breaks on the first timeout — the spec must define compensation for every step failure, because the state machine has more failure paths than happy paths |
| **Best for** | Backend developers building multi-service workflows; anyone who wants to understand why distributed transactions need explicit specs |

---

## The Concept

You are building an order fulfillment system — when a customer places an order, the system must: validate inventory, authorize payment, reserve stock, capture payment, create a shipment, and send a confirmation. Six steps. Simple, right?

Except:
- Payment authorization succeeds, but inventory reservation fails. Do you void the auth or retry inventory? The spec must say.
- Payment capture times out. Did it succeed or fail? You don't know. Retrying might double-charge. Not retrying might lose revenue. The spec must define "timeout = unknown."
- The shipping service is down for 2 hours. Do pending orders wait? Time out? Move to manual review? Each answer creates different states.
- Step 3 of 6 fails. Steps 1 and 2 already succeeded. You need to undo them — but "undo payment" (refund) is a different operation than "undo payment auth" (void). The compensation depends on HOW FAR you got.

This scenario teaches that **failure is the default state in distributed systems** — the happy path is one path; the failure paths are combinatorial. Without a spec, the AI will implement the happy path and improvise the rest, producing code that silently corrupts state on partial failure.

This is the same skill that appears at a simpler scale in:
- Scenario D (⭐⭐⭐): Stripe subscription state machine (one external service)
- Scenario M (⭐⭐): URL shortener idempotency (single-service idempotency)
- Scenario F (⭐⭐⭐⭐): Pipeline reliability mindset (but for data, not workflows)

**Tech stack:** Node.js + Express + PostgreSQL + BullMQ (Redis-backed job queue)

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a distributed order fulfillment saga. Prioritize: correctness over speed (never ship an unpaid order; never charge without fulfillment intent), explicit compensation (every step that can succeed must have a defined compensation/rollback if a later step fails), idempotency everywhere (every service call uses an idempotency key; duplicate processing is safe), timeout means unknown (a timed-out call is neither success nor failure — the spec must define a resolution path), audit everything (every state transition is logged with correlation ID, who/what/when, and the triggering event), fail toward human review (when automated recovery fails, escalate to a human — never silently drop an order), and testability (include chaos tests for every failure mode in the failure model).
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Correctness over speed principle
- [ ] Explicit compensation for every step
- [ ] Idempotency with key strategy
- [ ] Timeout = unknown principle
- [ ] Audit trail with correlation ID
- [ ] Escalation to human review
- [ ] Chaos testing requirements

---

### Specification

```
/speckit.specify Build OrderFlow — a saga-based order fulfillment orchestrator.

Architecture: single service with logical subsystems (not microservices). The orchestrator drives steps and writes saga state. External services are mocked adapters with configurable failure modes.

Saga steps (in order):
1. Validate Order — check items exist, prices match, quantities available. Pure validation, no side effects.
2. Authorize Payment — hold funds on customer's payment method. Side effect: creates a payment authorization. Compensation: void authorization.
3. Reserve Inventory — decrement available stock for each line item. Side effect: creates inventory reservations. Compensation: release reservations.
4. Capture Payment — convert authorization to actual charge. Side effect: transfers money. Compensation: refund (different from void — refund has fees and takes days).
5. Create Shipment — register shipment with carrier, get tracking number. Side effect: shipment record created. Compensation: cancel shipment (only possible before carrier pickup).
6. Send Confirmation — email/notification to customer. Side effect: notification sent. Compensation: send correction/cancellation email.

Step dependency rules:
- Steps 1→2→3 are strictly sequential (each depends on previous).
- Steps 4 and 5 can run in parallel after step 3 succeeds (payment capture + shipment creation are independent).
- Step 6 runs after BOTH 4 and 5 complete.
- If step 4 (capture) succeeds but step 5 (shipment) fails: refund payment + release inventory.
- If step 5 (shipment) succeeds but step 4 (capture) fails: cancel shipment + release inventory.

Saga state machine:
- CREATED → VALIDATING → PAYMENT_AUTHORIZED → INVENTORY_RESERVED → CAPTURING_AND_SHIPPING → FULFILLED
- Any step failure → COMPENSATING → COMPENSATED (or COMPENSATION_FAILED → REQUIRES_MANUAL_REVIEW)
- Timeout at any step → STEP_TIMEOUT → retry (up to 3 attempts) → REQUIRES_MANUAL_REVIEW

Compensation rules (symmetrical pairs):
| Step | Forward Action | Compensation | Compensation Notes |
|---|---|---|---|
| 2 | Authorize payment | Void authorization | Free, instant; only valid before capture |
| 3 | Reserve inventory | Release reservation | Instant; restores available stock |
| 4 | Capture payment | Refund | May incur fees; takes 5-10 business days |
| 5 | Create shipment | Cancel shipment | Only possible before carrier pickup |
| 6 | Send confirmation | Send cancellation email | Best-effort; cannot unsend |

Compensation execution order: reverse of forward execution. If steps 2, 3, 4 succeeded and step 5 fails, compensate in order: 4 (refund), 3 (release inventory), 2 (void auth — but auth was already captured, so this is a no-op).

Timeout semantics:
- Each step has a configurable timeout (default: 30 seconds).
- Timeout does NOT mean failure. Timeout means "unknown."
- On timeout: check step status via a separate "status query" endpoint on the adapter. If status is "succeeded," proceed. If "failed," compensate. If "still unknown" after 3 retries, move to REQUIRES_MANUAL_REVIEW.
- A timed-out payment capture is the most dangerous case: retrying might double-charge. The spec must define: query payment status first, only retry if status is definitively "not captured."

Idempotency:
- Every forward step call includes an idempotency key: `{orderId}-{stepName}-{attemptNumber}`.
- Every compensation call includes: `{orderId}-{stepName}-compensate-{attemptNumber}`.
- Adapters must return the same result for the same idempotency key (no side effects on retry).
- The saga orchestrator stores processed step results; on restart, it resumes from the last completed step (not from scratch).

Concurrency control:
- Only one saga instance per order (enforced by DB lock or unique constraint on orderId in saga table).
- If a duplicate "create order" event arrives, return the existing saga state (idempotent).

Data model:
- orders: id, customerId, items (JSON), totalCents (INTEGER), status, createdAt, updatedAt
- sagas: id, orderId (FK, UNIQUE), currentStep, status, startedAt, completedAt, failedStep, failureReason
- saga_steps: id, sagaId (FK), stepName, status (pending/running/succeeded/failed/compensating/compensated/timeout), attempt, idempotencyKey, request (JSON), response (JSON), startedAt, completedAt
- outbox: id, sagaId, eventType, payload (JSON), publishedAt (NULL until published)

Observability:
- Every saga has a correlationId (= orderId) propagated to all adapter calls.
- Every state transition is logged with: timestamp, sagaId, orderId, fromState, toState, stepName, attempt, duration.
- Audit log: who/what/when for every state change (queryable by orderId).
- Metrics: saga completion rate, p50/p95/p99 duration, failure rate by step, compensation rate, REQUIRES_MANUAL_REVIEW rate.
- Alert: REQUIRES_MANUAL_REVIEW count > 0.

Order cancellation:
- Customer can cancel an order while saga is in progress.
- Cancellation triggers immediate compensation of all completed steps.
- Cancellation is only allowed in states: CREATED, VALIDATING, PAYMENT_AUTHORIZED, INVENTORY_RESERVED.
- After CAPTURING_AND_SHIPPING: cancellation is not allowed (too late — shipment may be in transit). Return 409 Conflict.

Sample data:
- 3 orders: one FULFILLED (happy path completed), one COMPENSATED (payment auth succeeded but inventory failed), one REQUIRES_MANUAL_REVIEW (payment capture timed out).
- Adapter mock with configurable failure modes: always-succeed, always-fail, fail-on-nth-attempt, timeout.

Scope tiers:
- MVP (required): Orchestrated saga with 3 sequential steps (validate → authorize → reserve) + compensation + idempotency. Mock adapters. Saga state persisted in PostgreSQL. Contract tests for each step's success/failure/compensation paths.
- Core (recommended): + Capture + shipment (parallel steps) + timeout handling with status query + outbox pattern + retry worker + audit log + order cancellation.
- Stretch (optional): + Partial fulfillment (some items ship, others backorder) + manual review UI + reconciliation job + chaos testing (random adapter failures) + metrics dashboard.
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: Orchestrated saga (central orchestrator) or event choreography (services react to events)?
2. Decision needed: Do we authorize then capture payment, or capture immediately in one step?
3. Decision needed: If payment capture times out, do we retry immediately or query status first?
4. Decision needed: If inventory is insufficient, do we backorder (wait for restock) or fail the order?
5. Decision needed: Is partial fulfillment allowed (some items ship) or must it be all-or-nothing?
6. Decision needed: Compensation failure policy — retry forever, retry N times, or escalate immediately?
7. Decision needed: What is the event delivery guarantee — at-least-once with idempotent handlers, or exactly-once?
8. Decision needed: When can a customer cancel — which saga states allow cancellation?
9. Decision needed: What idempotency key structure prevents cross-order collisions?
10. Decision needed: What is the "source of truth" for order status — the order table or the saga table?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/P-order-fulfillment-saga-answers.md`](_answers/P-order-fulfillment-saga-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] Saga steps with forward actions and compensations
- [ ] Step dependency graph (sequential vs parallel)
- [ ] Timeout semantics ("timeout = unknown")
- [ ] Idempotency key strategy
- [ ] Safety invariants and liveness goals
- [ ] Failure model
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguities above
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify
```

Review the questions surfaced by Spec Kit. Use the deliberate ambiguity list above as a checklist — did the AI catch all 10? If not, add the missed ones manually.

**Manual refinement:**

```
For sample data: the COMPENSATED order should show the full compensation chain in saga_steps (authorize succeeded → reserve failed → void authorization). The REQUIRES_MANUAL_REVIEW order should show 3 timeout attempts on payment capture with the status queries.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] All 10 decision questions resolved
- [ ] Compensation is defined for every step (symmetrical pairs)
- [ ] Timeout handling has a concrete resolution path
- [ ] Order cancellation rules are explicit by state
- [ ] Concurrency control prevents duplicate sagas per order

---

### Plan

```
/speckit.plan Use Node.js with Express and PostgreSQL. BullMQ (Redis-backed) for the saga worker queue. Saga orchestrator pattern — central state machine drives steps. Each external service is a mock adapter with configurable failure modes (succeed, fail, timeout). Outbox pattern: saga state changes write to outbox table; a separate publisher reads outbox and emits events. Idempotency keys on every adapter call. All state transitions in database transactions.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Saga orchestrator architecture, step execution engine |
| `data-model.md` | orders, sagas, saga_steps, outbox tables with constraints |
| `research.md` | Saga vs 2PC, orchestration vs choreography, outbox pattern |
| `quickstart.md` | Test scenarios for each failure mode |

**Validate the plan:**

```
Review the plan and check: (1) Is the saga state machine explicitly defined with ALL states and transitions? (2) Does every adapter call use an idempotency key? (3) Is timeout handling a separate code path from failure handling? (4) Are compensations executed in reverse order? (5) Is there a reconciliation story for REQUIRES_MANUAL_REVIEW orders?
```

**Checkpoint:**
- [ ] Saga state machine has all states including compensation and manual review
- [ ] Idempotency key structure prevents collision
- [ ] Timeout triggers status query (not blind retry)
- [ ] Compensation order is reverse of forward execution
- [ ] Outbox pattern separates state change from event publication

---

### Tasks

```
/speckit.tasks
```

**What to observe:**
- Saga state machine and step executor are early tasks (before any adapter)
- Mock adapters with configurable failure modes are independent tasks
- Happy-path saga completes first; then failure/compensation paths
- Timeout handling is a separate task from failure handling
- Idempotency is tested explicitly (run same saga twice, verify no side effects)
- MVP / Core / Stretch ordering respected

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> This is critical for saga scenarios — verify that EVERY step's failure has a compensation test, and that the timeout path has a test for each of: "status = succeeded," "status = failed," and "status = still unknown."

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- Saga state machine persists state before executing each step (crash recovery)
- Idempotency keys are deterministic (`{orderId}-{stepName}-{attempt}`)
- Timeout handling queries adapter status before retrying
- Compensation runs in reverse order of completion
- Concurrency: duplicate order creation returns existing saga (not new one)
- Outbox: state change and outbox write are in the same DB transaction
- No order ships without captured payment (safety invariant)

---

## Extension Activities

### Add a Feature: Partial Fulfillment

What if some items are in stock but others aren't? The saga needs to split into sub-sagas per item group — some items ship now, others backorder. The compensation rules change: you can't void the entire payment, only refund the backorder portion.

```
/speckit.specify Add partial fulfillment to OrderFlow. When some order items are available and others are not, split the order into "shippable now" and "backordered" groups. Ship available items immediately; reserve backordered items when stock arrives. Payment is captured only for shipped items; backorder items are charged on ship. How does cancellation work for partially fulfilled orders? What if the customer wants to cancel only the backordered items?
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test: Add Real External Services

Replace mock adapters with actual (sandbox) external APIs — Stripe for payment, a shipping API, etc. What changes in the spec when latency is real, errors are unpredictable, and webhooks arrive asynchronously?

```
/speckit.specify Replace mock adapters with real external services. Payment uses Stripe API (test mode). Shipping uses a third-party shipping API. Inventory uses an external warehouse API. Now: timeouts are real, errors are unpredictable, and some services use webhooks instead of synchronous responses. How does the saga handle webhook-driven step completion? What about webhook delivery failures?
```

This bridges directly to Scenario D (Stripe billing) and Scenario F (pipeline reliability).
