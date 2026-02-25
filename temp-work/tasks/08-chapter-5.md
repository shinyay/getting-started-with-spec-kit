# Task 08: Chapter 5 — Advanced Scenarios (18 slides)

> **Purpose:** Learn to specify distributed systems. Failure models, safety invariants, liveness goals, idempotency, observability.
> **Target Level:** ⭐⭐⭐⭐ Advanced
> **Plan reference:** `slides/SLIDE-PLAN-EN.md` lines 297–344
> **JP reference:** `slides/spec-kit-presentation.md` lines 2180–2455
> **Scenarios:** `scenarios/E-collaborative-whiteboard.md`, `scenarios/F-event-ingestion-pipeline.md`, `scenarios/P-order-fulfillment-saga.md`, `scenarios/Q-plugin-runtime.md`, `scenarios/R-feature-flag-experimentation.md`

---

## Section 5.1: Advanced Scenario Introduction (3 slides)

### Slide 5-1: Chapter 5 Section Divider

**Plan ref:** Line 307

```markdown
---

<!-- _paginate: false -->
<!-- _header: "" -->

# Chapter 5: Advanced — Distributed Systems & Failure Models
```

---

### Slide 5-2: Advanced Scenarios

**Plan ref:** Line 308

```markdown
---

## Section 5.1: Introduction

# Advanced Scenarios

| Scenario | Build | SDD Skills |
|---|---|---|
| **E: Whiteboard** | Collaborative whiteboard | Consistency model, latency budget |
| **F: Pipeline** | Event ingestion pipeline | SLO specification, backpressure |
| **P: OrderFlow** | Order fulfillment saga | Compensating transactions, outbox |
| **Q: PlugKit** | Plugin runtime | Public API contract, sandboxing |
| **R: FlagShip** | Feature flag system | Statistical correctness, bucketing |

> **Failure is the default state. Specs define the failure model.**
```

---

### Slide 5-3: Advanced Baseline Contract

**Plan ref:** Line 309

```markdown
---

## Section 5.1: Introduction

# Advanced Baseline Contract

Required for ALL ⭐⭐⭐⭐ scenarios:

1. **Failure model section** — enumerate what can fail and how
2. **Safety invariants vs liveness goals** — things that must NEVER happen vs things that must EVENTUALLY happen
3. **Idempotency rules** — per-operation idempotency guarantees
4. **Observability** — correlation IDs, audit logs, reconciliation endpoints

> Without a failure model, your spec only covers the happy path.
> **In distributed systems, the happy path is the exception.**
```

---

## Section 5.2: Safety Invariants vs Liveness Goals (2 slides)

### Slide 5-4: Safety Invariants — Things That Must NEVER Happen

**Plan ref:** Line 315

```markdown
---

## Section 5.2: Safety vs Liveness

# Safety Invariants — Things That Must NEVER Happen

- **"Never ship an unpaid order"** (Scenario P: OrderFlow)
- **"Never assign a user to two mutually exclusive experiments"** (Scenario R: FlagShip)
- **"Deleted objects never appear to other users"** (Scenario E: Whiteboard)
- **"Never process the same event twice"** (Scenario F: Pipeline)

> **Explicitly enumerate safety invariants in the spec.**
> If AI doesn't know what must NEVER happen, it can't prevent it.
```

---

### Slide 5-5: Liveness Goals — Things That Must EVENTUALLY Happen

**Plan ref:** Line 316

```markdown
---

## Section 5.2: Safety vs Liveness

# Liveness Goals — Things That Must EVENTUALLY Happen

- **"All clients eventually converge"** (Scenario E: Whiteboard)
- **"Buffered events are eventually processed"** (Scenario F: Pipeline)
- **"Orders eventually complete or get compensated"** (Scenario P: OrderFlow)
- **"Feature flag changes eventually propagate"** (Scenario R: FlagShip)

> **"Eventually" is the keyword.**
> Liveness goals define the system's convergence guarantees.
```

---

## Section 5.3: Scenario P — OrderFlow: Learning the Saga Pattern (6 slides)

### Slide 5-6: Scenario P: OrderFlow Saga

**Plan ref:** Line 322

```markdown
---

## Section 5.3: OrderFlow Walkthrough

# Scenario P: OrderFlow Saga

**6-step order fulfillment:**

```
Validate → Authorize → Reserve → Capture → Ship → Confirm
```

### SDD Skills
- Compensating transactions (undo each step)
- Timeout semantics ("timeout = unknown")
- Exactly-once processing guarantees

> Duration: ~120 minutes (most complex scenario)
```

---

### Slide 5-7: Compensation Pairs & the Cost Gradient

**Plan ref:** Line 323

```markdown
---

## Section 5.3: OrderFlow Walkthrough

# Compensation Pairs & the Cost Gradient

| Step | Compensation | Cost |
|---|---|---|
| Validate | None | Free |
| Authorize | Void authorization | Free |
| Reserve | Release inventory | Free |
| Capture | Refund | 💸 Fee + 5–10 days |
| Ship | Cancel shipment | ⏰ Time-limited |

> **The further you go, the more expensive compensation becomes.**
> Step ordering matters — compensate cheaply first.
```

**Notes:**
- 5-row compensation table — the key conceptual model

---

### Slide 5-8: "Timeout = Unknown" Paradigm

**Plan ref:** Line 324

```markdown
---

## Section 5.3: OrderFlow Walkthrough

# "Timeout = Unknown" Paradigm

### Payment capture times out. Was the customer charged?

**Answer: Unknown.**

- ❌ Retry immediately → potential **double charge**
- ❌ Assume failure → customer charged but order not fulfilled
- ✅ **Query status first**, then decide next action

> **In vibe coding, timeout becomes "retry → double charge."**
> SDD forces you to specify timeout behavior for every step.
```

**Notes:**
- This is Chapter 5's "aha moment" — `Timeout → did it charge? → retry → double charge!`

---

### Slide 5-9: Failure Paths Outnumber the Happy Path

**Plan ref:** Line 325

```markdown
---

## Section 5.3: OrderFlow Walkthrough

# Failure Paths Outnumber the Happy Path

**One happy path.** But:

- 6 steps × multiple failure modes
- Partial completion states
- Timeout at any step
- Network errors between services
- Concurrent saga instances

> **Without specs, it's impossible to discover all failure paths.**
> Combinatorial explosion makes "figure it out later" catastrophic.
```

---

### Slide 5-10: The Outbox Pattern

**Plan ref:** Line 326

```markdown
---

## Section 5.3: OrderFlow Walkthrough

# The Outbox Pattern

### Problem:
State changes in DB, but event NOT sent to message queue → inconsistency

### Solution: Outbox Pattern
```
BEGIN TRANSACTION
  UPDATE orders SET status = 'captured'
  INSERT INTO outbox (event_type, payload) VALUES ('captured', ...)
COMMIT
-- Background worker reads outbox → publishes events
```

> **Specify event delivery guarantees in the spec.**
> "State change + event" must be atomic — no partial updates.
```

---

### Slide 5-11: OrderFlow Takeaways

**Plan ref:** Line 327

```markdown
---

## Section 5.3: OrderFlow Walkthrough

# OrderFlow Takeaways

1. **Compensate cheaply first** — step ordering matters
2. **Timeout ≠ failure** — query status before retrying
3. **Failure paths are combinatorial** — specs enumerate them
4. **Safety invariant: never ship unpaid** — explicitly in spec
5. **Outbox pattern** — atomic state change + event publishing

> Saga specs are the most complex — but also where SDD provides the **greatest protection**
```

---

## Section 5.4: Other Advanced Scenarios (4 slides)

### Slide 5-12: Scenario E: Collaborative Whiteboard — Consistency Model

**Plan ref:** Line 333

```markdown
---

## Section 5.4: Other Advanced Scenarios

# Scenario E: Collaborative Whiteboard — Consistency Model

Consistency model choice determines **entire architecture**:

| Model | Pros | Cons |
|---|---|---|
| **CRDT** | No central server | Complex merge logic |
| **OT** | Proven (Google Docs) | Requires transform functions |
| **Authoritative** | Simple | Single point of failure |

Quantitative latency budget: local < 16ms, remote p95 < 200ms

> SDD lesson: **Architecture decisions happen in the spec/plan phase**
```

---

### Slide 5-13: Scenario F: Event Ingestion Pipeline — SLO Specification

**Plan ref:** Line 334

```markdown
---

## Section 5.4: Other Advanced Scenarios

# Scenario F: Event Ingestion Pipeline — SLO Specification

> **Ban vague "high performance." Specify concrete SLOs.**

- **Throughput:** X events/sec sustained
- **Latency:** p99 < Y milliseconds
- **Backpressure:** return `429 Too Many Requests` when overloaded
- **Schema evolution:** backward-compatible event format changes

> SDD lesson: **Performance requirements must be quantitatively specified.**
> "Fast" is not a specification.
```

---

### Slide 5-14: Scenario Q: PlugKit Runtime — Your Spec IS the Product

**Plan ref:** Line 335

```markdown
---

## Section 5.4: Other Advanced Scenarios

# Scenario Q: PlugKit Runtime — Your Spec IS the Product

The plugin API is what external developers depend on.

- **Sandboxed execution** — Worker Thread isolation
- **Capability permissions** — plugins declare what they need
- **Threat model** — malicious plugins can't escape sandbox
- **Versioning** — plugin API v1 must remain stable

> SDD lesson: **Public API specs can't be changed after release.**
> Your spec literally IS the product contract.
```

---

### Slide 5-15: Scenario R: FlagShip — Statistical Correctness Specification

**Plan ref:** Line 336

```markdown
---

## Section 5.4: Other Advanced Scenarios

# Scenario R: FlagShip — Statistical Correctness

- **Deterministic bucketing** — `Math.random()` is **forbidden**
  - Use hash functions for reproducible assignment
- **SRM detection** — chi-square test for Sample Ratio Mismatch
- **Kill switch** — bypasses all caches, immediate flag override

> SDD lesson: **Statistical correctness is part of the spec.**
> A bucketing bug invalidates every experiment result.
```

---

## Section 5.5: Advanced Summary (3 slides)

### Slide 5-16: Advanced Progression

**Plan ref:** Line 342

```markdown
---

## Section 5.5: Advanced Summary

# Advanced Progression

| Order | Scenario | New Distributed Systems SDD Skill |
|---|---|---|
| 1st | **E: Whiteboard** | Consistency model, latency budget |
| 2nd | **F: Pipeline** | SLO quantification, backpressure |
| 3rd | **P: OrderFlow** | Compensating transactions, outbox |
| 4th | **Q: PlugKit** | Public API contract, sandboxing |
| 5th | **R: FlagShip** | Statistical correctness, bucketing |

> Each step adds a new **distributed systems specification skill**
```

---

### Slide 5-17: Cross-Level Comparison — What Changed Across All Levels?

**Plan ref:** Line 343

```markdown
---

## Section 5.5: Advanced Summary

# Cross-Level Comparison — What Changed?

| Axis | ⭐ Beginner | ⭐⭐ Intermediate | ⭐⭐⭐ Int–Adv | ⭐⭐⭐⭐ Advanced |
|---|---|---|---|---|
| **Constitution** | 4–5 | 6 | 11 | 11+ |
| **State complexity** | 5 states | — | 8+ states | Saga + CRDT |
| **Failure model** | None | API errors | Webhooks | Combinatorial |
| **Idempotency** | None | API level | Webhook + API | Per-step |
| **"Aha moment"** | Self-voting | 301 vs 302 | Float trap | Timeout=unknown |
```

**Notes:**
- 5-row × 5-column table (within limits — 5 columns allowed as rows ≤ 6)
- Comprehensive cross-level comparison

---

### Slide 5-18: SDD Skill Growth Map

**Plan ref:** Line 344

```markdown
---

## Section 5.5: Advanced Summary

# SDD Skill Growth Map

### State Machines
```
J (5 states) → D (8+ states, billing) → P (Saga, 6-step + compensation) → E (CRDT)
```

### Permissions
```
A (matrix) → M (route safety) → D (PCI compliance) → E (object ownership)
```

### Idempotency
```
None → API level (M) → Webhook (D) → Per-step key (P)
```

### Consistency
```
localStorage → Single DB (M) → Eventual consistency (D) → Real-time convergence (E)
```
```

**Notes:**
- 4 skill axes with code-block progression chains
- Shows how the same concept evolves across difficulty levels
- Final slide before Chapter 6 — sense of accomplishment

---

## ✅ Chapter 5 Quality Checks

- [ ] Section divider for Chapter 5 present
- [ ] 18 numbered slides (5-1 through 5-18)
- [ ] Safety invariants vs liveness goals clearly distinguished (slides 5-4, 5-5)
- [ ] OrderFlow walkthrough covers: compensation pairs, timeout=unknown, failure paths, outbox (6 slides)
- [ ] "Aha moment" — timeout → double charge (slide 5-8)
- [ ] Outbox pattern with SQL code example (slide 5-10)
- [ ] Each scenario (E, F, Q, R) has its own slide
- [ ] Consistency model comparison table for Whiteboard (slide 5-12)
- [ ] Cross-level comparison table spans all 4 levels (slide 5-17)
- [ ] Skill growth map shows 4 axes of evolution (slide 5-18)
- [ ] All h2 labels correct
- [ ] No Japanese text
- [ ] Content density within limits (5-17 table is at 5 columns — verify readability)
