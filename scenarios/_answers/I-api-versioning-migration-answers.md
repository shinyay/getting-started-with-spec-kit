# Scenario I — Facilitator Answer Key: API Versioning Migration (v1 → v2)

> **This file is for facilitators only.** Do not distribute to participants before the workshop — it removes the learning value of the clarification phase.

---

## Expected Domain Output: v1 → v2 Field Mapping Table

When `/speckit.specify` produces the v2 standards, the specification should include field-by-field mappings for each endpoint group:

### Users Endpoint

| v1 Field | v2 Field | Change Type |
|---|---|---|
| `id` (integer: 42) | `id` (prefixed: `"usr_abc123"`) | ID format change |
| `firstName` | `first_name` | camelCase → snake_case |
| `lastName` | `last_name` | camelCase → snake_case |
| `emailAddr` | `email_address` | abbreviation expanded |
| `createdAt` (Unix: 1704067200) | `created_at` (`"2025-01-01T00:00:00Z"`) | timestamp format change |
| (bare object response) | `{ "data": { ... } }` | response envelope added |
| `offset` + `limit` params | `cursor` param | pagination model change |

### ID Format Migration

| Entity | v1 Format | v2 Format | Alias Behavior |
|---|---|---|---|
| User | Integer (42) | `usr_abc123` | v2 accepts `42` as alias, returns `usr_abc123` |
| Order | UUID (`550e8400-...`) | `ord_xyz789` | v2 accepts UUID as alias, returns `ord_xyz789` |
| Product | Integer (7) | `prd_def456` | v2 accepts `7` as alias, returns `prd_def456` |

### Deprecation Timeline Milestones

| Milestone | Timing | Action |
|---|---|---|
| v2 Beta | T-14 months | Invite 5 partners; gather feedback; iterate on contracts |
| v2 GA | T+0 (start of 12-month clock) | Email all API key holders; publish migration guide; add Sunset headers to v1 |
| 50% window | T+6 months | Email reminder; publish adoption dashboard showing per-client v1/v2 split |
| 75% window | T+9 months | Email "3 months remaining"; offer migration office hours |
| 30 days before sunset | T+11 months | Urgent email; contact top v1 consumers directly |
| Sunset | T+12 months | v1 returns 410 Gone; v1 docs archived; extension window closed |
| Post-sunset archive | T+12 to T+36 months | v1 docs kept at /v1-archive with deprecation banner |

---

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Shim implementation | Express middleware: intercepts v1 routes → transforms request to v2 format → calls v2 handler → transforms v2 response back to v1 shape. Separate transformer module per endpoint. | Single source of truth (v2 logic); shim is pure translation; per-endpoint modules are independently testable. |
| 2 | v1 docs post-sunset | Archive at `/v1-archive` URL with deprecation banner. Main docs redirect to v2. Keep archive for 2 years. | Clients may need reference during cleanup; eventual removal keeps docs current. |
| 3 | Shim performance overhead | Accept up to 20ms additional latency for v1 requests. Monitor with `v1_shim_latency_ms` metric per endpoint. If any endpoint exceeds 20ms p95, optimize transformer. | JSON transform overhead is measurable; explicit budget prevents unbounded degradation. |
| 4 | Contract test structure | Two layers: (1) Per-standard tests ("all lists use cursor pagination", "all errors use error envelope") applied to every v2 endpoint. (2) Per-endpoint tests (specific field names, types, business logic). Both run in CI. | Per-standard tests catch systemic violations; per-endpoint tests catch business logic regressions. |
| 5 | Sunset governance | Engineering VP approves sunset date. Maximum one extension of 3 months. Extension requires written justification. Proceed when v1 < 5% of total requests. | Clear authority prevents indefinite postponement; usage threshold makes the decision data-driven. |
| 6 | In-flight v1 requests at sunset cutover | Deploy with a 60-second grace period: new v1 requests get 410, but requests started before cutover complete normally. Implemented via a "sunset timestamp" check at request start, not connection close. | Prevents mid-request failures; 60s is generous for any REST call. Grace period is invisible to most clients. |
| 7 | v2 ID backfill | Online migration: add nullable `v2_id` column → backfill in batches (1000 rows/batch, 100ms sleep between) → set NOT NULL → create unique index. Zero downtime. Estimated: <10 min for 1M rows. | Online is safer; batch approach prevents table locks; nullable-then-not-null pattern is standard for zero-downtime migrations. |
| 8 | Rate limits v1 vs v2 | v2 gets 2× the rate limit of v1 (incentive to migrate). Both versions share the same rate limit counter per API key. Communicated in migration guide + Changelog + rate limit response headers. | Migration incentive without punishing v1 clients; shared counter prevents abuse of dual access. |
| 9 | Client's tests break after shim | Shim must be byte-for-byte compatible with pre-migration v1. If a client's tests break, it's a shim bug — file a P1 issue. Maintain v1 golden test fixtures (recorded pre-migration) as regression suite. | The shim contract is "v1 clients see no change." Any deviation is a bug, not a migration issue. |
| 10 | Per-client sunset extension | Yes, via per-API-key feature flag: `v1_sunset_override: true`. Maximum 3-month extension. Requires written justification + executive approval. Extended clients are listed in an internal dashboard. Communication to other clients: "Some partners have a limited extension; the v1 archive remains available." | Per-key granularity is simple (middleware checks flag before returning 410). Transparency prevents perception of unfairness. |

---

## Facilitator Notes

### Constitution Phase
> The key principle is "response stability." Once v2 is GA, its response shape is frozen. Participants who don't include this will discover mid-migration that they want to change a v2 field name — which is exactly the problem v2 was supposed to solve.

### Specification Phase
> The scope tiers are critical. MVP is "v2 endpoints exist and pass contract tests." The shim, ID aliasing, and deprecation headers are Core. Participants who put "migration guide" or "telemetry dashboard" in MVP are over-scoping — you need working v2 endpoints before you can measure migration.

### Clarification Phase
> Questions 6 (in-flight requests at sunset) and 9 (client tests break after shim) are the most commonly missed. Both are "what happens at the boundary?" questions. The sunset cutover and the shim deployment are the two highest-risk moments in the migration — they need explicit behaviors.

### Plan Phase
> The #1 mistake is implementing v2 controllers with business logic AND v1 controllers with business logic — duplicating logic across versions. The correct architecture: shared service layer → v2 controllers (native) → v1 controllers (pure translators calling v2 services). If a participant's plan has business logic in v1 controllers, the shim will drift from v2.

### Implement Phase
> Watch for the ID backfill. Participants often try to do a single `UPDATE ... SET v2_id = generate_prefix_id()` on millions of rows — which locks the table. The batch approach (1000 rows at a time with sleep intervals) is essential for zero-downtime migration. Also watch for v1 golden tests — they must be recorded BEFORE any code changes, not written by hand afterward.
