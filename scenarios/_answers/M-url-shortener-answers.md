# Scenario M: URL Shortener — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## API Contract Summary (Expected Output)

| Method | Path | Success | Error |
|---|---|---|---|
| POST | `/api/shorten` | 200 (existing) or 201 (new) | 400 (invalid URL), 409 (vanity collision) |
| GET | `/:slug` | 302 (redirect) | 404 HTML, 410 HTML, 405 (non-GET/HEAD) |
| GET | `/api/links/:id` | 200 (with deletedAt if soft-deleted) | 404 JSON |
| GET | `/api/links/:id/stats` | 200 | 404 JSON |
| GET | `/api/links` | 200 (paginated) | 400 (invalid cursor) |
| DELETE | `/api/links/:id` | 200 (idempotent) | 404 JSON |

Key implementation details:
- **Route order:** `/api/*` routes MUST be registered before `/:slug` catch-all
- **Slug regex:** Express param constraint `[A-Za-z0-9-]{3,30}` prevents swallowing reserved paths
- **Analytics isolation:** Click recording in try/catch — never throws to redirect handler
- **URL normalization:** Pure function — trim, lowercase scheme+host, remove default ports, validate scheme

## Idempotency + Deletion Edge Case

If URL X was shortened → slug `abc1234` created → link deleted:
1. `GET /abc1234` → 410 Gone (forever)
2. POST `/api/shorten` with URL X again → creates NEW link with NEW slug `xyz5678` (201)
3. Principle: "Same normalized URL returns the same **active** short link"

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Same URL → existing or new? | Return existing active link (200); if deleted, create new (201) | Idempotency without Idempotency-Key headers |
| 2 | Default redirect status | 302 Found (temporary) | Allows analytics on every visit; 301 caches in browsers |
| 3 | Deleted links: 404 or 410? | 410 Gone | HTTP spec: 410 = "was here, intentionally removed"; 404 = "never existed" |
| 4 | Analytics retention | 90 days detailed, then aggregate monthly | Balances storage with usefulness |
| 5 | Vanity case-sensitive? | Yes — "MyLink" ≠ "mylink" | Maximizes slug space; matches URL convention |
| 6 | Vanity collision | 409 Conflict with error envelope suggesting alternatives | Clear feedback; no silent override |
| 7 | Redirect chains | Detect if target URL matches our own domain; warn on creation, don't block | Prevents infinite loops without restricting legitimate use |
| 8 | HEAD analytics | Do NOT record — HEAD is often bots/health checks | Keeps stats meaningful |
| 9 | Error format for /:slug | HTML for browser routes; JSON for /api/* | Different consumers, different formats — great teaching moment |
| 10 | Shorten after delete | New slug, old slug stays 410 | Preserves tombstone; idempotency applies to active links only |

## Facilitator Notes

- **After Constitution**: "Notice principle #3 splits error handling: JSON for API, HTML for browser. This is real-world — your redirect route serves browsers, your API serves code."
- **After Specify**: "Ask: what happens if you swap the route mounting order? This is a real Express bug that a spec prevents."
- **After Clarify**: "The 301 vs 302 question teaches that HTTP semantics are a spec concern, not an implementation detail. 301 caches in browsers — your analytics will silently disappear."
- **After Plan**: "Is URL normalization a pure function or embedded in the route handler? The answer reveals plan quality."
