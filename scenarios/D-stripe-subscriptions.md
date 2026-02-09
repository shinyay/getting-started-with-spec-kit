# Scenario D: Stripe Subscriptions + Webhooks + Dunning

| | |
|---|---|
| **Level** | ⭐⭐⭐ Intermediate–Advanced |
| **Duration** | ~120 min |
| **Key SDD themes** | Money correctness, idempotency, state machines, webhook reliability, eventual consistency |
| **Why it tests SDD** | Billing ambiguity = real money lost; every edge case has financial consequences |
| **Best for** | Developers building SaaS billing; anyone who wants to see how SDD handles financial correctness |

---

## The Concept

You are adding subscription billing to a SaaS product using Stripe. Users can start trials, upgrade/downgrade, cancel, and manage payment methods. Failed payments trigger a dunning flow (notify → grace period → restrict → suspend). Webhooks from Stripe drive state changes in your app.

This scenario stress-tests SDD because:
- **Money correctness is non-negotiable** — a billing bug that overcharges customers destroys trust
- **Subscription state machines are complex** — trial → active → past_due → canceled → suspended with many edge cases at each transition
- **Idempotency is mandatory** — Stripe delivers webhooks at-least-once; duplicate processing = duplicate charges or state corruption
- **Eventual consistency** — your app and Stripe will temporarily disagree; the spec must define reconciliation
- **Proration math** — mid-cycle upgrades/downgrades involve non-obvious financial calculations

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create a constitution for implementing subscription billing using Stripe.

Non-negotiables:
- Correctness over speed: no ambiguous billing states; every subscription must be in a well-defined state at all times.
- Monetary precision: all monetary calculations must use integer cents (not floating point). Currency formatting is a display concern only.
- Idempotency everywhere: webhooks, checkout, upgrade, downgrade — all billing operations must be idempotent using idempotency keys or event deduplication.
- Eventual consistency by design: the app and Stripe may be temporarily inconsistent. Design for reconciliation, not synchronous certainty.
- Fail-safe access: when in doubt about a user's billing state, err on the side of granting access. A brief period of free access is better than incorrectly blocking a paying customer.
- Webhooks must be verified (signature validation) and processed idempotently. Unprocessable webhooks must be dead-lettered for investigation, never silently dropped.
- Never store raw card data; follow PCI best practices (use Stripe-hosted flows only).
- Clear separation between "Stripe state" and "app state" with periodic reconciliation.
- All billing-impacting changes must be logged and traceable (who/what/when).
- Testing: include webhook simulation tests, billing lifecycle integration tests, and proration correctness tests.
- Observability: dashboards/alerts for failed payments, webhook processing lag, and Stripe-vs-app state drift.
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Correctness-over-speed principle
- [ ] Monetary precision (integer cents, no floating point)
- [ ] Idempotency for all billing operations
- [ ] Eventual consistency / reconciliation principle
- [ ] Fail-safe access (grant access when uncertain)
- [ ] PCI compliance (no raw card data)
- [ ] Audit logging for billing changes
- [ ] Observability requirements

---

### Specification

```
/speckit.specify Add subscription billing to our SaaS product with monthly and annual plans.

Business goals:
- Monetize via subscriptions, support free trial, and reduce churn via dunning.
- Provide self-serve upgrades/downgrades and cancellation.
- Invoice and receipt access for finance/accounting needs.

Users:
- Account Owner (billing admin): manages plan, payment method, seats, and invoices.
- Member (non-billing user): sees their plan tier but cannot modify billing.
- Finance/Support (internal): views billing status and audit log without seeing sensitive payment details.

Requirements:

Plans:
- Free, Pro ($29/mo or $290/yr), Business ($99/mo or $990/yr).
- Optional add-on: extra seats beyond included (Free: 1 seat, Pro: 5, Business: 25).
- Trial: 14-day trial for Pro/Business. Trial starts without a payment method. User must add a payment method before trial ends or trial expires to Free.

Subscription state machine (valid states and transitions):
- trialing → active (payment method added, trial ends successfully)
- trialing → expired (trial ends without payment method → revert to Free)
- active → past_due (payment fails)
- past_due → active (retry succeeds or user updates payment method)
- past_due → suspended (grace period exhausted — 7 days, 3 retry attempts)
- active → canceled_pending (user cancels, access continues until period end)
- canceled_pending → expired (period ends)
- suspended → active (user updates payment method and pays outstanding balance)
- Any state → canceled_immediately (user chooses immediate cancellation)

Billing flows:
- Start trial → prompt to add payment method before trial ends → auto-convert to paid on trial end.
- Upgrade mid-cycle: charge prorated difference immediately. New features available instantly.
- Downgrade mid-cycle: apply credit for unused time to next invoice. Reduced features apply at next billing cycle.
- Cancel (end of period): access continues until period end, then features revert to Free tier.
- Cancel (immediate): access reverts to Free tier immediately; no refund for remaining time.
- Payment method update: Stripe-hosted Customer Portal or Stripe Elements checkout.
- Invoices and receipts accessible in-app, downloadable as PDF.

Failed payment / dunning:
- Day 0: payment fails → status becomes past_due. Notify Account Owner via email + in-app banner.
- Day 3: second retry + email reminder.
- Day 5: third retry + urgent email.
- Day 7: grace period ends → status becomes suspended. Access restricted to read-only (can view data but not create/edit). Email notification of suspension.
- During suspension: in-app prompt to update payment method. On successful payment, immediately restore to active.

Seat management:
- Seats are per-user. Adding a user consumes a seat.
- Adding seats beyond the plan's included count triggers an add-on charge (prorated to current billing cycle).
- Removing a user frees the seat immediately but no refund is issued until next invoice (credit applied).
- If seat count drops below current user count after a downgrade, Account Owner must remove users before downgrade completes.

Admin UX:
- Billing portal section: current plan, renewal date, seat count (used/total), invoices list, payment method (last 4 digits only), upgrade/downgrade/cancel buttons.
- Audit log of all billing changes (plan changes, seat changes, payment method updates) visible to Account Owner and Finance/Support.

Acceptance criteria:
- Duplicate webhook deliveries do not cause duplicate charges or state changes.
- Plan change always results in correct entitlement changes (features and seats) at the correct time.
- Billing emails contain correct, localized amounts and dates.
- Support can view billing status without seeing full card numbers or Stripe secret keys.
- A user in a trial who does not add a payment method is gracefully reverted to Free with no data loss.
- Proration calculations match Stripe's calculations exactly (do not reimplement; use Stripe's proration).

Edge cases to explicitly cover:
- Card expires between renewal dates.
- User upgrades during grace period (past_due).
- Trial expires at exactly midnight in different time zones.
- Double-click on checkout/upgrade button.
- Stripe webhook arrives before the checkout callback returns to the app.
- User cancels and immediately wants to resubscribe.
- Account has credit from previous downgrade proration.
- Webhook signature validation fails (reject and alert, do not process).

Non-goals (explicitly out of scope):
- Multi-currency support (USD only for v1).
- Tax calculation (will use Stripe Tax in a future iteration).
- Coupon/discount codes (future iteration).
- Refund self-service (handled manually by Support for now).
```

**Deliberate ambiguities to watch for:**
- What happens to data when an account is suspended? (read-only vs. full lockout)
- Can a Member see the billing portal at all, or is it completely hidden?
- What is the email sender name/address and template style?
- How long are invoices retained and accessible?
- Can an Account Owner transfer billing ownership to another user?

**Checkpoint** — verify the generated spec contains:
- [ ] User stories with acceptance criteria
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguous areas
- [ ] A review and acceptance checklist
- [ ] The subscription state machine is captured in the spec

---

### Clarification

```
/speckit.clarify Review the Stripe billing spec and ask me about every ambiguity, unstated assumption, and gap — especially around: suspended account data access, member visibility into billing, email templates, invoice retention, billing ownership transfer, Stripe Checkout vs custom checkout flow, and any financial edge cases you can identify.
```

Suggested answers for the workshop:

| Question Theme | Suggested Answer |
|---|---|
| Suspended account data access | Read-only: users can view and export their data but cannot create, edit, or delete anything. API returns 403 for mutating operations with a clear error message. |
| Member visibility into billing | Members see their current plan tier and renewal date on a settings page, but cannot see payment details, invoices, or billing controls. |
| Email sender and templates | Sender: "Billing <billing@ourapp.com>". Templates needed: trial starting, trial expiring (3 days before), payment succeeded, payment failed (x3 retries), account suspended, account reactivated. |
| Invoice retention | Invoices are retained indefinitely in Stripe and cached in-app for 2 years. Older invoices are fetched on-demand from Stripe. |
| Billing ownership transfer | Account Owner can transfer billing admin role to another user in the same account. Transfer is audit-logged. New owner must confirm via email. |
| Checkout flow | Use Stripe Checkout (hosted) for initial subscription creation and Stripe Customer Portal for payment method updates. Do not build custom card forms. |
| Annual plan cancellation mid-year | End-of-period cancellation: access continues until the annual renewal date. No partial refund. Immediate cancellation: no refund for remaining months (documented in cancellation confirmation dialog). |

**Manual refinement:**

```
For sample data: create 3 accounts — "Acme Corp" (Business annual, 20/25 seats used, active), "Startup Inc" (Pro monthly, in trial with 3 days remaining, no payment method), and "Old Co" (Pro monthly, past_due since 2 days ago). Include sample invoices and a billing audit log with plan changes.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] Subscription state machine is fully defined with all transitions
- [ ] Proration behavior is explicit for upgrades and downgrades
- [ ] Dunning timeline is specified (Day 0, 3, 5, 7)
- [ ] Every listed edge case has a defined behavior
- [ ] Checkout flow decision is made (Stripe Checkout vs custom)

---

### Plan

```
/speckit.plan Create a technical plan for Stripe subscription billing per the spec and constitution.

Tech stack context (existing app):
- Backend: Node.js + Express, PostgreSQL, Knex.js for migrations.
- Frontend: React SPA, communicating via REST API.
- Email: SendGrid for transactional email.
- Deployment: Docker, CI/CD via GitHub Actions.
- Use Stripe API (latest version), stripe Node.js SDK, and Stripe CLI for local webhook testing.

The plan must include:
- Stripe objects to use: Customers, Subscriptions, Prices (with lookup_keys), Products, Checkout Sessions, Customer Portal, and why each is needed.
- Checkout flow: Stripe Checkout for initial subscription + Stripe Customer Portal for self-serve payment method and plan changes.
- Webhook design: signature verification with stripe SDK, event deduplication (store processed event IDs), async processing via a job queue (not synchronous in HTTP handler), retry strategy, ordering considerations (use event timestamp, not delivery order).
- Subscription state machine: how app state maps to Stripe subscription statuses, and which webhooks trigger which transitions.
- Data model: accounts, subscriptions (app-side mirror), invoices (cached), entitlements, seat counts, dunning state, webhook event log, billing audit log.
- Entitlement enforcement: Express middleware that checks account subscription state + plan tier on every API request. Cache entitlements in Redis with a short TTL (60s). Invalidate on webhook-triggered state change.
- Email notification: SendGrid templates for each dunning stage and billing event. Include unsubscribe compliance.
- Reconciliation job: periodic (hourly) job that fetches active subscriptions from Stripe and compares to app state. Log discrepancies, auto-fix safe cases (e.g., subscription active in Stripe but past_due in app), alert on unsafe cases.
- Idempotency: Stripe idempotency keys for all mutating Stripe API calls; event ID deduplication for webhooks.
- Testing plan: Stripe CLI for local webhook testing, Stripe test-mode for integration tests, mock Stripe API for unit tests, specific tests for each state machine transition, and a "chaos" test that delivers webhooks out of order.
- Rollout plan: feature flag per account ("billing_enabled"), start with internal accounts, then 10% canary, then GA. "Billing disabled" fallback keeps all features accessible.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Implementation plan with phases and architecture |
| `data-model.md` | Tables: accounts, subscriptions, invoices, entitlements, webhook events, audit log |
| `research.md` | Stripe API patterns, webhook reliability, proration behavior |
| `contracts/` | API contracts for billing endpoints, webhook payload handling |
| `quickstart.md` | Key validation scenarios |

**Validate the plan:**

```
Review the implementation plan and check: (1) Does the webhook processing handle out-of-order delivery safely? (2) Is the entitlement cache invalidation strategy robust? (3) Does the reconciliation job handle all discrepancy types? (4) Are all Stripe API calls using idempotency keys?
```

**Checkpoint:**
- [ ] Stripe objects are correctly chosen and justified
- [ ] Webhook processing is async (queued, not synchronous in HTTP handler)
- [ ] Event deduplication prevents duplicate state changes
- [ ] State machine mapping between Stripe statuses and app states is documented
- [ ] Reconciliation job exists for drift detection and repair
- [ ] Entitlement enforcement is centralized in middleware
- [ ] Rollout uses feature flags with a canary phase

---

### Tasks

```
/speckit.tasks Produce tasks that implement billing end-to-end.

Task constraints:
- Include separate tasks for: schema + migrations, Stripe product/price setup, Stripe Checkout flow, webhook handler (with async queue), subscription state machine, entitlement enforcement middleware, billing UI (portal section), email notifications (dunning + lifecycle), seat management, reconciliation job, monitoring/alerts, and test suites.
- Include explicit tasks for edge cases: proration math verification, cancellation timing (immediate vs end-of-period), payment failure grace period transitions, duplicate webhook events, webhook signature failures, checkout double-click protection, and resubscription after cancellation.
- Include a "financial correctness" task: verify that proration calculations in the app match Stripe's proration exactly for upgrade, downgrade, and seat changes.
- Include a "reconciliation verification" task: introduce deliberate Stripe/app drift and verify the reconciliation job detects and repairs it.
- Include docs tasks: Account Owner billing guide + Support troubleshooting playbook.
```

**What to observe in `tasks.md`:**
- State machine implementation appears early (before UI or webhook handling)
- Webhook handler uses async processing (queue), not synchronous
- Edge case tasks are separate, not buried in "implement webhook handler"
- Financial correctness task explicitly compares app calculations to Stripe
- Reconciliation job includes both drift detection and repair verification
- Monitoring/alerting task exists for failed payments and webhook lag

---

### Implement

```
/speckit.implement Execute all tasks in order. After completing the state machine and webhook handler, run the billing lifecycle integration tests before proceeding to UI tasks. Verify financial correctness tests pass before moving to the rollout phase.
```

**What to watch for:**
- The AI follows the task order from `tasks.md`
- Stripe API calls include idempotency keys
- Webhook handler stores processed event IDs for deduplication
- Monetary values are stored as integer cents, never floating point
- Entitlement middleware is applied globally, not per-route
- No raw card data appears anywhere in the codebase
- Feature flags gate billing functionality per account

---

## Extension Activities

### Add a Feature: Coupon and Discount Codes

Extend billing with promotional pricing:

```
/speckit.specify Add coupon and discount code support to the billing system. Account Owners can apply a coupon code during checkout or from the billing portal. Coupons can be percentage-based (e.g., 20% off for 3 months) or fixed-amount (e.g., $10 off per month for 6 months). Coupons can be restricted to specific plans or available for all plans. Include a Support-facing admin UI to create and manage coupons. Track coupon usage and redemption limits.
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test the Spec: Mid-billing-cycle Price Change

Add a new business requirement and see how it ripples:

```
A new requirement has emerged: the business wants to increase Pro plan pricing from $29/mo to $39/mo, effective next month. Existing subscribers should be grandfathered at $29/mo for 6 months, then migrated to $39/mo with 30 days notice via email. New subscribers immediately pay $39/mo. Update the spec, plan, and tasks to handle this. Consider: how does this interact with annual plans already purchased at the old price? What about users currently in trial?
```

This demonstrates how SDD handles business-critical pricing changes systematically rather than as ad-hoc code patches.
