# Scenario P: Order Fulfillment Saga — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Saga State Machine

```
CREATED → VALIDATING → PAYMENT_AUTHORIZED → INVENTORY_RESERVED
                                                    ↓
                                          CAPTURING_AND_SHIPPING
                                            ↙             ↘
                                    (capture)         (shipment)
                                            ↘             ↙
                                            FULFILLED

Any step failure → COMPENSATING → COMPENSATED
                                   or → COMPENSATION_FAILED → REQUIRES_MANUAL_REVIEW
Timeout → retry (×3) → REQUIRES_MANUAL_REVIEW
```

## Compensation Pairs

| Step | Forward | Compensation | Cost of Compensation |
|---|---|---|---|
| 2 | Authorize payment | Void authorization | Free, instant |
| 3 | Reserve inventory | Release reservation | Free, instant |
| 4 | Capture payment | Refund | Fees + 5-10 day delay |
| 5 | Create shipment | Cancel shipment | Only before carrier pickup |
| 6 | Send confirmation | Send cancellation email | Cannot unsend original |

**Key insight:** Compensation cost increases with each step. Void (free) → Release (free) → Refund (fees) → Cancel shipment (time-limited). This is why step ordering matters.

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Orchestration vs choreography | Orchestration (central orchestrator) | Easier to reason about, audit, and test; saga state machine is explicit |
| 2 | Auth then capture, or capture immediately | Authorize first, capture after inventory confirmed | Separates "can they pay?" from "charge them" — enables void (free) vs refund (costly) |
| 3 | Payment timeout handling | Query payment status FIRST, then decide | Blind retry risks double-charge; status query is safe and idempotent |
| 4 | Insufficient inventory | Fail the order; backorder is Stretch | Workshop simplicity; backorder adds partial-fulfillment complexity |
| 5 | Partial fulfillment | All-or-nothing in v1; partial is Stretch | Reduces compensation complexity by half |
| 6 | Compensation failure policy | Retry 3 times with exponential backoff, then REQUIRES_MANUAL_REVIEW | Bounded retries prevent infinite loops; human escalation is the safety net |
| 7 | Event delivery guarantee | At-least-once with idempotent handlers | Exactly-once is not achievable; at-least-once + idempotency key gives the same result |
| 8 | Order cancellation states | Allowed in: CREATED, VALIDATING, PAYMENT_AUTHORIZED, INVENTORY_RESERVED. Denied after CAPTURING_AND_SHIPPING. | Once capture/shipment starts, cancellation is too late (requires refund + cancel shipment, which is a different flow) |
| 9 | Idempotency key structure | `{orderId}-{stepName}-{attemptNumber}` | Deterministic, collision-free, debuggable; attempt number handles retries |
| 10 | Source of truth | Saga table is authoritative; order table reflects saga outcome | Saga tracks the process; order tracks the result. Saga is the source of truth during execution. |

## Facilitator Notes

- **After Constitution**: "Ask: what's the difference between a safety invariant and a liveness goal? 'Never ship unpaid' is safety. 'Eventually ship if paid' is liveness. Both must be in the spec."
- **After Specify**: "Draw the compensation pairs on the board. Ask: what happens if step 5 compensation (cancel shipment) fails because the carrier already picked up? This is why compensation failure needs a spec."
- **After Clarify**: "The timeout=unknown question is the 'aha' moment. Write on the board: 'Payment capture timed out. Did it charge the customer?' The answer is: you don't know. That's why you query status."
- **After Plan**: "Check: does the plan persist saga state BEFORE executing each step? If the worker crashes between step execution and state write, the saga is in an unknown state."
- **Common mistake**: Teams treat timeout as failure (retry immediately). This risks double-charge on payment capture.
- **Common mistake**: Compensation runs in forward order instead of reverse. Step 3 compensation (release inventory) should happen BEFORE step 2 compensation (void auth).
