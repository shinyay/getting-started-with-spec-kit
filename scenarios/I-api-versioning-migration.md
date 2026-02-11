# Scenario I: API Versioning Migration (v1 → v2)

| | |
|---|---|
| **Level** | ⭐⭐⭐ Intermediate–Advanced |
| **Duration** | ~110 min |
| **Key SDD themes** | Backward compatibility, deprecation governance, API contracts, client migration paths, dual-version coexistence |
| **Why it tests SDD** | API migrations affect every consumer simultaneously — vague deprecation timelines, undefined compatibility windows, or untested shims break third-party integrations in production |
| **Best for** | Backend developers, API platform teams, anyone maintaining public or partner-facing APIs |

---

## The Concept

You are migrating a public REST API from v1 (inconsistent naming, ad-hoc pagination, unstructured errors) to v2 (standardized conventions). Both versions must coexist during a compatibility window. Clients need a clear migration path with guides, response headers signaling deprecation, and telemetry tracking adoption.

This scenario stress-tests SDD because:
- **Every API consumer is a stakeholder** — breaking changes affect partners, integrations, and mobile apps simultaneously with no ability to force-update
- **The compatibility window is a contract** — "supported for a defined period" without dates and enforcement rules is a lawsuit waiting to happen
- **Dual-version coexistence creates subtle bugs** — shared business logic serving two response shapes can silently drift if not tested
- **Deprecation is a process, not an event** — headers, documentation, usage tracking, communication cadence, and sunset enforcement must all be specified
- **API contracts are machine-verifiable** — unlike UI specs, API specs can be validated automatically via contract tests, making SDD particularly powerful here

This is the same skill that appears at higher difficulty in:
- Scenario Q (⭐⭐⭐⭐): Plugin API contracts must be backward-compatible across versions while third-party developers build against them
- Scenario R (⭐⭐⭐⭐): Feature lifecycle governance with kill switches applies the same "deprecation as a governed process" to feature rollouts

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create a constitution for an API versioning and migration project.

Non-negotiables:
- Backward compatibility window must be explicit: define the exact duration (in months), the start date trigger, and what "supported" means (bug fixes only? security patches only? feature parity?).
- Deprecation is a governed process, not an informal notice: every deprecated endpoint must have a documented migration path, a Sunset response header (RFC 8594) with the retirement date, and measurable adoption tracking.
- No breaking changes without a safe rollout: feature flags, dual-write/dual-read if data models change, and a rollback plan if adoption stalls.
- Strong API contracts: every endpoint must have an OpenAPI specification. Contract tests validate responses against the spec on every CI run. No undocumented fields or behaviors.
- Semantic versioning for the API: v2 is a new major version because it contains breaking changes from v1. Within v2, all changes must be backward-compatible (additive only).
- Response stability: once a v2 endpoint is GA, its response shape (field names, types, nesting) must not change without a v3. New optional fields may be added.
- Observability: track usage per endpoint, per version, per client (API key). Alert when a deprecated v1 endpoint usage increases (possible new integration). Alert when v1 usage drops below threshold (sunset candidate).
- Client communication: deprecation notices must be sent to all registered API consumers at defined milestones (announcement, 50% window, 30 days before sunset, sunset).
- Testing: contract tests for both versions, backward-compatibility regression tests for v1, integration tests that verify v1 and v2 return equivalent data for the same underlying resources.
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Explicit compatibility window with duration and support level
- [ ] Deprecation governance (Sunset header, migration path, tracking)
- [ ] No breaking changes without rollout plan
- [ ] OpenAPI contract requirement with CI-enforced contract tests
- [ ] Response stability guarantee for GA endpoints
- [ ] Per-version, per-client usage tracking
- [ ] Client communication milestones
- [ ] Dual-version equivalence testing

---

### Specification

```
/speckit.specify Migrate our public REST API from v1 to v2.

Context:
- The API serves 200+ third-party integrations (partners, mobile apps, internal services).
- v1 has been in production for 3 years. It has inconsistent field names (camelCase and snake_case mixed), three different pagination approaches across endpoints, and unstructured error responses (plain text in some, JSON in others).
- Clients authenticate via API keys. Each key is associated with a client organization.

Motivation:
- Standardize naming, pagination, error format, and resource identifiers for v2.
- Reduce support burden from confused integrators.
- Enable future API expansion on a clean foundation.

v2 standards (all endpoints must conform):
- Naming: all field names use snake_case. No abbreviations (e.g., "organization" not "org").
- Resource identifiers: all resources use a prefixed string ID (e.g., "usr_abc123", "ord_xyz789") instead of v1's mixed integer/UUID IDs. v1 IDs remain valid as aliases in v2 for the compatibility window.
- Pagination: cursor-based pagination on all list endpoints. Response shape: { "data": [...], "pagination": { "next_cursor": "...", "has_more": true } }. v1 used offset/limit on some endpoints and page/per_page on others.
- Error format: all errors return { "error": { "code": "invalid_parameter", "message": "Human-readable message", "details": [...], "request_id": "req_..." } }. HTTP status codes follow RFC 7231 strictly.
- Timestamps: all timestamps are ISO 8601 in UTC with timezone designator (e.g., "2025-01-15T10:30:00Z"). v1 had some Unix timestamps and some ISO without timezone.
- Envelope: all successful responses use { "data": ... } for single resources and { "data": [...], "pagination": {...} } for lists. v1 returned bare objects/arrays.

Endpoints to migrate (representative set — not exhaustive):
- GET /v2/users, GET /v2/users/{id} (v1: /v1/users, mixed camelCase fields, integer IDs, offset pagination)
- GET /v2/orders, GET /v2/orders/{id}, POST /v2/orders (v1: /v1/orders, bare array response, Unix timestamps, unstructured errors)
- GET /v2/products, PATCH /v2/products/{id} (v1: /v1/products, page/per_page pagination, abbreviations like "desc" instead of "description")

Compatibility layer:
- A translation shim that allows v1 clients to continue working without code changes during the compatibility window.
- Approach: v1 endpoints internally call v2 logic, then transform the response back to v1 shape. This ensures a single source of truth (v2 logic) while maintaining v1 contracts.
- The shim must be transparent to v1 clients: identical response shapes, status codes, and pagination behavior to pre-migration v1.

Deprecation and sunset:
- Compatibility window: 12 months from v2 GA date.
- v1 support during window: security patches and critical bug fixes only. No new features on v1.
- Deprecation headers: all v1 responses include Deprecation: true and Sunset: <date> headers (RFC 8594).
- Documentation: v1 API docs show a deprecation banner with a link to the migration guide.
- Communication cadence: email to all API key holders at: v2 GA announcement, 6 months remaining, 3 months remaining, 30 days remaining, sunset day.
- Post-sunset: v1 endpoints return 410 Gone with a JSON body containing the migration guide URL. Not a silent 404.

Migration guide for clients:
- Per-endpoint mapping: v1 request/response → v2 request/response with field-by-field diff.
- ID migration: document how v1 integer/UUID IDs map to v2 prefixed IDs. Provide a lookup endpoint: GET /v2/id-map?v1_id=<old_id>&type=user → { "v2_id": "usr_abc123" }.
- Pagination migration: show how to convert offset/limit or page/per_page calls to cursor-based pagination.
- Error handling migration: show how to parse the new error envelope.
- SDK updates: if SDKs exist, provide updated versions with changelog.

Acceptance criteria:
- v2 endpoints conform to all v2 standards (validated by contract tests against OpenAPI spec).
- v1 responses remain byte-for-byte identical during the compatibility window (validated by snapshot/golden tests against pre-migration recordings).
- The v1→v2 translation shim produces responses that pass v1's existing contract tests.
- Usage telemetry shows per-client v1 vs v2 adoption over time.
- Deprecation headers are present on all v1 responses.
- Migration guide covers every v1 endpoint with request/response examples.
- Post-sunset, v1 endpoints return 410 Gone (not 404 or 500).

Edge cases to explicitly cover:
- Client sends v1-style integer ID to a v2 endpoint: accept it as an alias and return the v2 prefixed ID in the response. Log a "legacy ID usage" metric.
- Client sends a v2 request to a v1 endpoint (e.g., cursor pagination to an offset endpoint): return a clear error with a hint to use the v2 endpoint.
- v1 endpoint has a bug that clients depend on ("bug compatibility"): document the behavior difference in the migration guide. If the bug is relied upon, consider preserving it in the shim with a code comment explaining why.
- Rate limits differ between v1 and v2: v2 has higher rate limits as an incentive to migrate.
- Webhook payloads (if any) also need versioning: v1 webhooks continue in v1 format during the window; new webhook registrations default to v2 format.
- Client's API key is used for both v1 and v2 simultaneously during migration (same key, both versions).

Non-goals (explicitly out of scope):
- GraphQL API (REST only).
- WebSocket/streaming endpoints (future).
- New v2-only features (this migration is about parity + standardization, not new functionality).

Scope tiers:
- MVP (required): v2 OpenAPI spec (contract-first) + 3 v2 endpoint groups (users, orders, products) with v2 standards (snake_case, cursor pagination, error envelope) + contract tests validating responses against OpenAPI spec
- Core (recommended): + v1 translation shim (per-endpoint transformer modules) + v2 prefixed ID system with v1 alias support + deprecation headers on all v1 responses (Sunset + Deprecation) + v1 snapshot/golden tests for backward compatibility
- Stretch (optional): + Per-client v1/v2 usage telemetry dashboard + post-sunset 410 Gone enforcement with per-endpoint feature flags + migration guide with per-endpoint field-by-field mapping + webhook versioning (v1 ↔ v2 format switching)
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: How is the translation shim implemented — Express middleware, separate controllers, or a reverse proxy layer?
2. Decision needed: What happens to v1 API documentation after sunset — archived at a stable URL, removed entirely, or redirected to v2 docs?
3. Decision needed: What is the acceptable performance overhead of the v1 shim — and how is latency monitored per-endpoint?
4. Decision needed: How are v2 contract tests structured — per-endpoint, per-standard (e.g., "all lists use cursor pagination"), or both?
5. Decision needed: Who approves the sunset date, and can it be extended? What is the maximum number of extensions?
6. Decision needed: What happens to in-flight v1 requests at the exact moment of sunset cutover — complete normally, or reject with 410?
7. Decision needed: Is the v2 ID backfill migration performed online (zero-downtime, progressive) or offline (maintenance window)?
8. Decision needed: Are rate limits different between v1 and v2 — and if v2 has higher limits as a migration incentive, how is this communicated?
9. Decision needed: What happens if a client's integration tests break after the shim is deployed but before they've migrated to v2?
10. Decision needed: Can a client request a per-client sunset extension, and if so, what is the technical mechanism (per-API-key feature flag)?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/I-api-versioning-migration-answers.md`](_answers/I-api-versioning-migration-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] User stories with acceptance criteria
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguities above
- [ ] v2 standards defined (naming, pagination, errors, timestamps, envelope)
- [ ] Compatibility window duration and support level
- [ ] Communication cadence for deprecation notices
- [ ] Migration guide requirements
- [ ] A review and acceptance checklist
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify Review the API v1→v2 migration spec and ask me about every ambiguity, unstated assumption, and gap — especially around: shim implementation strategy, v1 documentation post-sunset, shim performance overhead, contract test structure, sunset date governance, webhook versioning details, and any API migration edge cases you can identify.
```

Review the questions surfaced by Spec Kit. Use the deliberate ambiguity list above as a checklist — did the AI catch all 10? If not, add the missed ones manually.

**Manual refinement:**

```
For testing and documentation: create sample request/response pairs for each of the 3 endpoint groups (users, orders, products) in both v1 and v2 format. These serve as: (1) golden test fixtures, (2) migration guide examples, and (3) shim test cases. Include one example showing how a v1 integer ID maps to a v2 prefixed ID.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] v2 standards are fully defined and testable
- [ ] Translation shim approach is decided with performance budget
- [ ] Deprecation timeline has concrete milestones and communication plan
- [ ] Post-sunset behavior is defined (410 Gone, not 404)
- [ ] ID aliasing rules are specified (accept v1 IDs, return v2 IDs)
- [ ] Every edge case has a defined behavior (bug compatibility, webhook versioning, rate limit incentive)
- [ ] All 10 deliberate ambiguities have documented resolutions

---

### Plan

```
/speckit.plan Create a technical plan for delivering API v2 alongside v1.

Tech stack context (existing app):
- Backend: Node.js + Express, PostgreSQL, Knex.js for migrations.
- API documentation: existing Swagger/OpenAPI spec for v1.
- Authentication: API key middleware (already shared).
- Deployment: Docker, CI/CD via GitHub Actions.
- Use dredd or Prism for contract testing against OpenAPI specs.

The plan must include:
- Versioning strategy: URL-path versioning (/v1/..., /v2/...). Document why URL-path over Accept header (simpler for clients, cache-friendly, unambiguous in logs).
- OpenAPI contract definition: v2 spec written first (contract-first development). v1 spec codified from existing behavior (snapshot of current responses). Both specs are the source of truth for contract tests.
- Architecture: shared business logic layer (services) → v2 controllers (native) + v1 controllers (shim that calls v2 services + transforms responses). v1 controllers do NOT contain business logic — they are pure translators.
- Translation shim design: per-endpoint transformer modules. Each transformer has: requestV1toV2(req) and responseV2toV1(res) functions. Transformers are unit-tested with golden fixtures.
- ID migration: add a v2_id column (prefixed string) to primary tables. Backfill existing rows. Create a unique index. v2 uses v2_id as the primary external identifier. v1 IDs are aliases resolved via database lookup.
- Pagination migration: v2 uses cursor-based pagination (cursor = opaque base64-encoded token). v1 shim translates offset/limit and page/per_page to cursor internally and translates back in responses.
- Telemetry: middleware that logs { version, endpoint, client_id, latency, status_code } for every request. Grafana dashboard showing v1 vs v2 usage per client over time. Alert if any client increases v1 usage after receiving deprecation notice.
- Deprecation headers: middleware that adds Deprecation: true, Sunset: <date>, and Link: <migration-guide-url>; rel="sunset" to all v1 responses.
- Post-sunset enforcement: feature flag that switches v1 from "deprecated" to "sunset" mode. In sunset mode, all v1 endpoints return 410 Gone with migration guide URL. Flag is per-endpoint to allow phased sunset if needed.
- Contract test strategy: (1) v2 contract tests via Prism (validate responses against OpenAPI spec). (2) v1 snapshot tests (compare current responses to pre-migration recordings — byte-for-byte). (3) Equivalence tests (call v1 and v2 for the same resource, verify data consistency).
- Rollout plan: Phase 1 — v2 beta (invite 5 partner clients, gather feedback). Phase 2 — v2 GA (announce to all clients, start 12-month clock). Phase 3 — active migration support (office hours, migration tooling). Phase 4 — sunset (410 Gone for v1).
- Risk analysis: top risks and mitigations (shim introduces bugs, clients don't migrate, performance regression, ID backfill data integrity).
- Documentation plan: v2 OpenAPI spec (auto-generated docs), migration guide (per-endpoint mapping with examples), changelog, SDK update guide.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Architecture, rollout phases, risk analysis |
| `data-model.md` | v2_id column additions, ID mapping table, pagination cursor encoding |
| `research.md` | URL-path vs header versioning, contract testing tools (Prism vs Dredd), cursor pagination approaches |
| `contracts/` | OpenAPI specs for v1 (codified) and v2 (designed), sample request/response pairs |
| `quickstart.md` | Key validation scenarios |

**Validate the plan:**

```
Review the implementation plan and check: (1) Does the shim architecture ensure v1 controllers have zero business logic? (2) Are contract tests running in CI for both versions? (3) Is the ID backfill migration reversible? (4) Does the rollout plan include a feedback phase before GA? (5) Is there a rollback plan if v2 has critical bugs at GA?
```

**Checkpoint:**
- [ ] Versioning strategy chosen with rationale (URL-path)
- [ ] Contract-first: v2 OpenAPI spec exists before implementation
- [ ] Shim is a pure translator (no business logic in v1 controllers)
- [ ] ID migration has a backfill plan with data integrity checks
- [ ] Telemetry tracks usage per version per client
- [ ] Deprecation headers include Sunset date (RFC 8594)
- [ ] Post-sunset returns 410 (not 404) with migration guide
- [ ] Rollout has phased approach (beta → GA → migration → sunset)

---

### Tasks

```
/speckit.tasks Break down tasks to implement API v2 and run the v1→v2 migration.

Task preferences:
- Start with contracts: write the v2 OpenAPI spec first, then codify the v1 spec from current behavior. These are the source of truth.
- Then implement v2 endpoints (contract-first: write contract tests, then implement to pass them).
- Then build the v1 translation shim (per-endpoint transformers with golden tests).
- Then add ID migration (v2_id column, backfill, alias resolution).
- Then add telemetry (version/endpoint/client tracking, dashboard).
- Then add deprecation headers and post-sunset enforcement (feature flag).
- Then write documentation (migration guide, changelog, SDK update guide).
- Include explicit tasks for: v1 backward-compatibility regression tests (snapshot tests against pre-migration recordings), v1↔v2 equivalence tests, shim performance benchmarks, beta client onboarding, and deprecation email drafts.
- Include a "smoke test the migration guide" task: follow the guide yourself as if you were a v1 client and verify every example works.
- Each task must have a "done when" check.
```

**What to observe in `tasks.md`:**
- OpenAPI spec creation is the very first task (contract-first)
- v2 implementation follows contract tests (write test → implement → pass)
- v1 shim is built after v2 is working (shim calls v2 logic)
- v1 snapshot tests are recorded from the live v1 before any changes
- ID backfill has a verification step (count check, no nulls, no duplicates)
- Telemetry and deprecation headers are separate tasks
- Documentation includes a "smoke test the guide" validation task
- Tasks are ordered: contracts → v2 implementation → shim → migration → telemetry → docs

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Run `/speckit.analyze` after tasks to check cross-artifact consistency. It validates that every spec requirement has a corresponding task, and every task traces back to the spec. Particularly valuable for API migrations where a missed endpoint, an inconsistent response shape, or a missing contract test means broken client integrations in production.

---

### Implement

```
/speckit.implement Execute all tasks in order. Before modifying any v1 code, record v1 response snapshots for all endpoints (these become the golden regression fixtures). After implementing v2 endpoints, run the v2 contract tests. After building the shim, run the v1 snapshot tests to verify byte-for-byte compatibility. Run equivalence tests to verify v1 and v2 return consistent data.
```

**What to watch for:**
- The AI follows the task order from `tasks.md`
- v2 OpenAPI spec is written before any v2 controller code
- v1 response snapshots are recorded BEFORE any code changes
- v1 controllers contain only translation logic (no business logic)
- ID aliasing is implemented (v1 integer IDs accepted by v2 endpoints)
- Deprecation and Sunset headers appear on v1 responses
- Post-sunset mode returns 410 Gone (not 404)
- Contract tests run in CI for both versions

---

## Extension Activities

### Add a Feature: API Key Scoping by Version

Extend the API key system to support version-specific access:

```
/speckit.specify Add the ability for clients to create API keys scoped to a specific API version. A "v2-only" key cannot call v1 endpoints (returns 403 with migration guide link). A "v1+v2" key works on both versions (default during migration). After sunset, "v1+v2" keys automatically become "v2-only". Include admin UI for key management and telemetry showing which keys are v1-only, v2-only, and dual. Consider: how does this interact with webhook versioning?
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test the Spec: Emergency Sunset Extension

Force a governance decision through the SDD process:

```
A major partner (30% of API traffic) has informed you 45 days before sunset that they cannot complete their v1→v2 migration in time. Their contract includes API access SLAs. Update the spec to define the sunset extension procedure. Consider: do you extend for all clients or just this partner? How does a per-client extension work technically (feature flag per API key)? What is the communication to other clients who already migrated? How does this affect the deprecation timeline and Sunset headers? What if the partner requests a second extension?
```

This demonstrates how SDD handles governance conflicts — the spec forces you to define the decision framework before the crisis, not during it.
