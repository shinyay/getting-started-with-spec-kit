# Task 07: Chapter 4 — Intermediate–Advanced Scenarios (16 slides)

> **Purpose:** Learn to specify external services, auth, financial, and infrastructure. Where missing specs cause "real damage."
> **Target Level:** ⭐⭐⭐ Intermediate–Advanced
> **Plan reference:** `slides/SLIDE-PLAN-EN.md` lines 253–293
> **JP reference:** `slides/spec-kit-presentation.md` lines 1900–2180
> **Scenarios:** `scenarios/B-field-inspection-pwa.md`, `scenarios/C-oidc-sso-rbac.md`, `scenarios/D-stripe-subscriptions.md`, `scenarios/G-terraform-github-actions.md`, `scenarios/I-api-versioning-migration.md`

---

## Section 4.1: Intermediate–Advanced Scenario Introduction (2 slides)

### Slide 4-1: Chapter 4 Section Divider

**Plan ref:** Line 263

```markdown
---

<!-- _paginate: false -->
<!-- _header: "" -->

# Chapter 4: Intermediate–Advanced — Real-World Complexity
```

---

### Slide 4-2: Intermediate–Advanced Scenarios

**Plan ref:** Line 264

```markdown
---

## Section 4.1: Introduction

# Intermediate–Advanced Scenarios

| Scenario | Build | SDD Skills |
|---|---|---|
| **B: PWA** | Field inspection app | Offline sync, conflict resolution |
| **C: OIDC SSO** | SSO + RBAC | Fail-closed, tenant isolation |
| **D: Stripe** | Subscription billing | Monetary correctness, idempotency |
| **G: Terraform** | IaC pipeline | Drift detection, blast radius |
| **I: API Versioning** | v1→v2 migration | Backward compatibility |

> **Where missing specs cause real damage.**
```

---

## Section 4.2: Scenario D — Stripe: Specifying Financial Correctness (7 slides)

### Slide 4-3: Scenario D: Stripe Subscriptions

**Plan ref:** Line 270

```markdown
---

## Section 4.2: Stripe Walkthrough

# Scenario D: Stripe Subscriptions

**Subscription + dunning flow**

### SDD Skills
- Monetary correctness (integer cents)
- Idempotency (every API call)
- Webhook state machines (at-least-once delivery)

> **Billing bug = losing real money.**
> This is where specification rigor pays for itself.
```

---

### Slide 4-4: Integer Cents — The Floating-Point Trap

**Plan ref:** Line 271

```markdown
---

## Section 4.2: Stripe Walkthrough

# Integer Cents — The Floating-Point Trap

```javascript
// ❌ The trap
0.1 + 0.2           // → 0.30000000000000004
19.99 * 100          // → 1998.9999999999998

// ✅ Integer cents — always exact
1999                 // $19.99 stored as 1999 cents
1999 + 500           // $19.99 + $5.00 = $24.99 (2499 cents)
```

> SDD makes this explicit in the constitution:
> **"monetary precision = integer cents. `parseFloat` is forbidden."**
```

**Notes:**
- This is Chapter 4's "aha moment" — `0.1 + 0.2 !== 0.3 → billing bug!`

---

### Slide 4-5: Complex State Machine — 9 Transitions

**Plan ref:** Line 272

```markdown
---

## Section 4.2: Stripe Walkthrough

# Complex State Machine — 9 Transitions

```
trial → active → past_due → canceled
  ↓        ↓         ↓
active   past_due   suspended
              ↓
           canceled → (end)
```

Evolution from beginner Pomodoro: 5 states → **8+ states, 9 transitions**

> **If you don't specify every state transition, users get incorrectly billed.**
> A missing transition = a billing bug in production.
```

---

### Slide 4-6: Webhook Reliability — "At Least Once" Delivery

**Plan ref:** Line 273

```markdown
---

## Section 4.2: Stripe Walkthrough

# Webhook Reliability — "At Least Once" Delivery

Stripe webhooks are delivered **at least once** — duplicates happen.

Must specify:
1. **Signature verification** — reject unsigned events
2. **Event deduplication** — track processed event IDs
3. **Async queue processing** — don't block the webhook endpoint
4. **Stale event handling** — ignore events older than current state

> **Duplicate processing = double billing.**
> Without specs, AI skips deduplication entirely.
```

---

### Slide 4-7: Idempotency Keys — Every Stripe API Call

**Plan ref:** Line 274

```markdown
---

## Section 4.2: Stripe Walkthrough

# Idempotency Keys — Every Stripe API Call

### Without idempotency:
```
POST /charge → network error → retry → 💸 double charge!
```

### With idempotency:
```
POST /charge (key: abc123) → error → retry (key: abc123) → ✅ same result
```

> SDD makes **"idempotency everywhere"** a constitutional principle.
> Every Stripe API call must include an idempotency key — no exceptions.
```

---

### Slide 4-8: The Clarify "Aha Moment" — Unused Seat Refunds

**Plan ref:** Line 275

```markdown
---

## Section 4.2: Stripe Walkthrough

# The Clarify "Aha Moment" — Unused Seat Refunds

### "What about unused seat credits at cancellation?"

- **Refund** pro-rata to the customer?
- **Forfeit** — credits expire at cancellation?
- **Apply to final invoice** — credit against outstanding balance?

Each option has different financial, legal, and UX implications.

> **Without specs, AI decides your refund policy.**
> Financial edge cases must be explicitly decided — never left to AI.
```

---

### Slide 4-9: Constitution Density Comparison

**Plan ref:** Line 276

```markdown
---

## Section 4.2: Stripe Walkthrough

# Constitution Density Comparison

| | ⭐ Beginner | ⭐⭐⭐ Stripe |
|---|---|---|
| **Principles** | 4–5 | 11 |
| **Examples** | Simplicity, readability | Correctness-first, integer cents |
| | Minimal deps, test coverage | Idempotency, eventual consistency |
| | | Fail-safe access, webhook verification |
| | | PCI compliance, audit logs |

> **Constitution grows proportionally to risk.**
> More money at stake → more principles required.
```

---

## Section 4.3: Other Intermediate–Advanced Scenarios (4 slides)

### Slide 4-10: Scenario B: Field Inspection PWA — Offline Sync

**Plan ref:** Line 282

```markdown
---

## Section 4.3: Other Scenarios

# Scenario B: Field Inspection PWA — Offline Sync

Specifying offline-first behavior:

- **Conflict resolution rules** — last-write-wins? merge? user chooses?
- **Media upload retry** — resume interrupted uploads
- **Sync queue ordering** — which changes sync first?
- Queue persistence across app restarts

> SDD lesson: **"What happens offline?" is answered in the spec.**
> Without specs, offline behavior is undefined — data loss in the field.
```

---

### Slide 4-11: Scenario C: OIDC SSO + RBAC — Security Contract

**Plan ref:** Line 283

```markdown
---

## Section 4.3: Other Scenarios

# Scenario C: OIDC SSO + RBAC — Security Contract

- **Fail-closed principle** — on auth error, deny access (never fail-open)
- **Tenant isolation** — user A must NEVER see user B's data
- **Secret rotation** — IdP signing keys rotate; app must handle gracefully
- **RBAC matrix** — define roles × permissions × resources

> SDD lesson: **Security isn't bolted on later — it's defined in the constitution.**
> A missing `fail-closed` principle → cross-tenant data leak.
```

---

### Slide 4-12: Scenario G: Terraform + GitHub Actions — Infrastructure Spec

**Plan ref:** Line 284

```markdown
---

## Section 4.3: Other Scenarios

# Scenario G: Terraform + GitHub Actions — Infrastructure Spec

> **"Infrastructure itself IS the spec."**

- **Drift detection** — alert when actual state ≠ desired state
- **Blast radius control** — limit what a single change can affect
- **No manual changes** — all changes through `terraform apply`
- **State locking** — prevent concurrent modifications

> SDD lesson: **SDD applies to ops, not just apps.**
> Infrastructure specifications prevent production incidents.
```

---

### Slide 4-13: Scenario I: API Versioning — Backward Compatibility Spec

**Plan ref:** Line 285

```markdown
---

## Section 4.3: Other Scenarios

# Scenario I: API Versioning — Backward Compatibility

v1 → v2 migration with 200 existing consumers:

- **Shim layer** — v1 requests translated to v2 internally
- **Deprecation timeline** — v1 sunset date communicated 6 months ahead
- **`410 Gone`** — after sunset, v1 endpoints return 410 (not 404)
- Monitoring: track v1 usage to know when it's safe to remove

> SDD lesson: **200 consumers depend on v1 — compatibility is a spec requirement.**
> Breaking changes without a migration spec → customer churn.
```

---

## Section 4.4: Intermediate–Advanced Summary (3 slides)

### Slide 4-14: Intermediate vs Intermediate–Advanced — What Changed?

**Plan ref:** Line 291

```markdown
---

## Section 4.4: Summary

# Intermediate vs Intermediate–Advanced — What Changed?

| Axis | ⭐⭐ Intermediate | ⭐⭐⭐ Int–Advanced |
|---|---|---|
| **External services** | None | Stripe / IdP / Terraform |
| **Stakes** | UI bugs | Real money / security |
| **Constitution** | 6 principles | 11 principles |
| **Consistency** | Not needed | Eventual consistency |
| **Testing** | Contract tests | Chaos testing |
```

---

### Slide 4-15: "Missing Specs Cause Real Damage" — Case Studies

**Plan ref:** Line 292

```markdown
---

## Section 4.4: Summary

# "Missing Specs Cause Real Damage" — Case Studies

1. 💸 **Double billing** — missing idempotency spec (Scenario D)
2. 🔓 **Cross-tenant data leak** — missing fail-closed principle (Scenario C)
3. 📱 **Offline data loss** — missing sync spec (Scenario B)
4. 💔 **Sudden API shutdown** — missing migration spec (Scenario I)
5. 🔥 **Infrastructure drift** — missing IaC spec (Scenario G)

> **All preventable with Clarify.**
> The cost of writing specs << the cost of these failures.
```

---

### Slide 4-16: Bridge to Advanced

**Plan ref:** Line 293

```markdown
---

## Section 4.4: Summary

# Bridge to Advanced

**Intermediate–Advanced:** external service integrations

**Advanced:** distributed systems — failure is the default state

- Safety invariants vs liveness goals
- Compensating transactions (Sagas)
- Consistency models (CRDT, OT, authoritative server)
- "Timeout = unknown" paradigm

> Specs must define the **failure model** — not just the happy path → **Chapter 5**
```

---

## ✅ Chapter 4 Quality Checks

- [ ] Section divider for Chapter 4 present
- [ ] 16 numbered slides (4-1 through 4-16)
- [ ] Stripe walkthrough covers: integer cents, state machine, webhooks, idempotency, clarify moment, constitution density (7 slides)
- [ ] "Aha moment" — `0.1 + 0.2 !== 0.3` billing bug (slide 4-4)
- [ ] Floating-point code example present
- [ ] State machine shows 8+ states with ASCII diagram
- [ ] Webhook "at least once" delivery explained with 4 requirements
- [ ] Each scenario (B, C, G, I) has its own slide
- [ ] Constitution density comparison table (slide 4-9)
- [ ] "Real damage" case studies with emoji icons (slide 4-15)
- [ ] Bridge to Chapter 5 mentions failure models (slide 4-16)
- [ ] All h2 labels correct
- [ ] No Japanese text
