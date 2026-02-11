# Scenario D — Facilitator Answer Key: Stripe Subscriptions + Webhooks + Dunning

> **This file is for facilitators only.** Do not distribute to participants before the workshop — it removes the learning value of the clarification phase.

---

## Expected Domain Output: Subscription State Machine with Stripe Webhook Mapping

When `/speckit.specify` and `/speckit.clarify` resolve the state machine, the specification should produce this transition table:

| From State | To State | Trigger | Stripe Webhook | App Action |
|---|---|---|---|---|
| (none) | trialing | User starts trial | `customer.subscription.created` (status: trialing) | Create local subscription record; start trial timer |
| trialing | active | Trial ends + payment method present | `customer.subscription.updated` (status: active) | Update state; enable paid features |
| trialing | expired | Trial ends, no payment method | `customer.subscription.updated` (status: canceled) | Revert to Free tier; notify user |
| active | past_due | Payment fails | `invoice.payment_failed` | Set past_due; start dunning timer (Day 0) |
| past_due | active | Retry succeeds or payment method updated | `invoice.payment_succeeded` | Restore active; clear dunning state |
| past_due | suspended | Grace period exhausted (Day 7) | `customer.subscription.updated` (status: past_due, 3 retries failed) | Restrict to read-only; notify user |
| active | canceled_pending | User cancels (end of period) | `customer.subscription.updated` (cancel_at_period_end: true) | Mark as canceling; show "access until [date]" |
| canceled_pending | expired | Period ends | `customer.subscription.deleted` | Revert to Free tier |
| suspended | active | Payment method updated + outstanding paid | `invoice.payment_succeeded` | Restore full access immediately |
| Any | canceled_immediately | User cancels (immediate) | `customer.subscription.deleted` | Revert to Free tier now; no refund |

### Dunning Timeline

| Day | Event | Email | App UI |
|---|---|---|---|
| 0 | Payment fails | "Payment failed — update payment method" | Banner: "Payment failed" |
| 3 | 2nd retry + reminder | "Action required — 2nd attempt failed" | Banner persists |
| 5 | 3rd retry + urgent email | "Urgent: account at risk of suspension" | Banner turns red |
| 7 | Grace period ends | "Account suspended — update payment to restore" | Read-only mode; prominent "Restore" button |

### Idempotency Strategy

| Operation | Idempotency Mechanism |
|---|---|
| Webhook processing | Store `event.id` in `webhook_events` table; skip if already processed |
| Stripe Checkout creation | Stripe idempotency key = `checkout_{account_id}_{plan_id}_{timestamp_minute}` |
| Plan change (upgrade/downgrade) | Stripe idempotency key = `plan_change_{subscription_id}_{target_plan}_{timestamp_minute}` |
| UI double-click protection | Disable button after first click; re-enable after response or 10s timeout |

---

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Suspended account data access | Read-only: view and export data, but cannot create/edit/delete. API returns 403 for mutations with `subscription_suspended` error code. | Preserves data access (builds trust) while enforcing payment obligation. |
| 2 | Member visibility into billing | Members see plan tier + renewal date on settings. No payment details, invoices, or billing controls visible. | Reduces confusion; billing is Account Owner's responsibility. |
| 3 | Email sender and templates | Sender: "Billing \<billing@ourapp.com\>". Templates: trial starting, trial expiring (3 days before), payment succeeded, payment failed (×3), suspended, reactivated. | Standard dunning communication cadence; sender identity builds trust. |
| 4 | Invoice retention | Indefinite in Stripe; cached in-app for 2 years. Older invoices fetched on-demand from Stripe API. | Stripe is the source of truth; local cache improves UX for common queries. |
| 5 | Billing ownership transfer | Account Owner can transfer to another user in same account. New owner confirms via email. Transfer is audit-logged. | Prevents orphaned billing when employees leave. Email confirmation prevents unauthorized transfer. |
| 6 | In-flight requests during state change | Complete the current request; apply new state on next request. Middleware re-checks entitlements per-request (no cached state). | Avoids mid-request errors; eventual consistency is acceptable for sub-second windows. |
| 7 | Trial expiry timezone | Always UTC. Trial starts at creation timestamp; ends 14×24h later. Display local time to user but calculate in UTC. | Eliminates timezone ambiguity; consistent behavior across all accounts. |
| 8 | Plan change during past_due | Allowed for upgrades (may fix payment issue with higher-tier card authorization). Blocked for downgrades until payment resolves. | Upgrades often succeed because of higher charge authorization; downgrades during past_due add complexity with no value. |
| 9 | Grace period + downgrade | Downgrade blocked during past_due. If somehow processed, grace period continues unchanged — clock does not reset. | Prevents gaming (downgrade to reset grace period). Simplifies state machine. |
| 10 | Seat credits on cancellation | Unused seat credits applied to final invoice. If cancellation is immediate, credits are forfeited (documented in cancellation dialog). | End-of-period: credits offset final charge. Immediate: user chose to forfeit by selecting "cancel now." |

---

## Facilitator Notes

### Constitution Phase
> The key principle is "correctness over speed." Watch for participants who skip "monetary precision: integer cents only." Floating point in billing is a bug — `0.1 + 0.2 !== 0.3` in JavaScript. This is not theoretical; it causes real invoice discrepancies.

### Specification Phase
> The state machine is the heart of this scenario. If participants produce a spec without an explicit state transition table, the AI will invent transitions. Push them to enumerate every From → To → Trigger combination. The most commonly missed transitions: `past_due → suspended` and `canceled_pending → expired`.

### Clarification Phase
> Questions 6 (in-flight requests) and 9 (grace period + downgrade) are the sneakiest. Both involve timing edge cases where two events happen "at the same time." Participants who answer these well understand eventual consistency; those who struggle reveal an assumption that state changes are instantaneous.

### Plan Phase
> The #1 mistake is processing webhooks synchronously in the HTTP handler. Stripe has a 20-second timeout. If webhook processing involves database writes + entitlement cache invalidation + email sending, it will time out. The plan must include an async job queue for webhook processing.

### Implement Phase
> Watch for Stripe API calls without idempotency keys. Every mutating Stripe call needs one. Also watch for `parseFloat` or `Number` on monetary values — all calculations must use integer cents. The reconciliation job (Stretch) is where participants discover that their app and Stripe can disagree — this is the most valuable learning moment.
