# Scenario R: Feature Flag & Experimentation Platform

| | |
|---|---|
| **Level** | ⭐⭐⭐⭐ Advanced |
| **Duration** | ~120 min |
| **Key SDD themes** | Deterministic bucketing, consistent distributed evaluation, exposure logging, statistical correctness, emergency rollback |
| **Why it tests SDD** | "Just check a flag" hides a distributed consistency problem — the same user must see the same variant everywhere, exposure logging must be correct for analysis, and a kill switch must propagate in seconds, not minutes |
| **Best for** | Developers building experimentation or gradual rollout systems; anyone who wants to understand why "feature flags" require distributed systems + statistical rigor specs |

---

## The Concept

You are building a feature flag and experimentation platform — teams create flags, configure rollout percentages, run A/B tests, and analyze results. Services evaluate flags at runtime to decide what users see. Simple, right?

Except:
- User X sees the new checkout flow on the web, but the old flow in the mobile API. Same user, different variant — because the two services computed bucketing differently. The spec must define deterministic assignment.
- Your experiment shows a 5% lift in conversion — but 60% of users are in the control group and 40% in treatment. Sample ratio mismatch (SRM) means your randomization is broken. The spec must define how to detect this.
- A critical bug is found in the new feature. You flip the kill switch. But services cache flags for 5 minutes. Users see the broken feature for another 5 minutes. The spec must define a propagation SLO.
- Two experiments both modify the checkout page. A user is in both. The results are contaminated. The spec must define mutual exclusion.

This scenario teaches that **correctness here is both statistical AND distributed** — getting either wrong produces decisions based on bad data. And that **the flag evaluation contract must be identical across all services** — any inconsistency corrupts experiment results.

This is the same skill that appears at a simpler scale in:
- Scenario M (⭐⭐): API analytics correctness (counting clicks accurately)
- Scenario O (⭐⭐): Aggregation correctness and traceability (money-as-cents)
- Scenario D (⭐⭐⭐): Financial correctness mindset applied to different domain

**Tech stack:** Node.js + Express + PostgreSQL + Redis (flag cache + pub/sub propagation)

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a feature flag and experimentation platform. Prioritize: deterministic evaluation (same user + same flag = same result, always, across all services), exposure logging is not optional (every flag evaluation that affects user experience must be logged — missing exposure events corrupt experiment analysis), statistical rigor (experiment conclusions must be traceable to data; sample ratio mismatch detection is mandatory), propagation speed (flag changes must reach all services within a defined SLO; kill switches are the fastest path), no experiment contamination (users in one experiment must not be affected by another experiment on the same surface unless explicitly allowed), auditability (every flag change, experiment start/stop, and override is logged with who/what/when), and testability (deterministic bucketing is testable with known inputs; exposure logging is verifiable end-to-end).
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Deterministic evaluation principle
- [ ] Mandatory exposure logging
- [ ] Statistical rigor / SRM detection
- [ ] Propagation SLO for flag changes
- [ ] Experiment isolation / mutual exclusion
- [ ] Audit trail
- [ ] Testability of bucketing

---

### Specification

```
/speckit.specify Build FlagShip — a feature flag and experimentation platform.

Core concepts:
- Flag: a named toggle with variants. Simplest: boolean (on/off). Advanced: multivariate (control, treatment_a, treatment_b).
- Experiment: a flag with traffic allocation, start/end dates, and a primary metric. Experiment = "flag + measurement."
- Targeting rule: conditions that determine which users see which variant (e.g., country = US, plan = pro, userId in allowlist).
- Kill switch: immediately force a flag to a specific variant for all users, bypassing all rules.

Deterministic bucketing algorithm:
- Unit of assignment: userId (required). If userId is missing, flag returns default variant (control).
- Hash: stable hash of "{flagKey}:{userId}" → integer in range [0, 9999].
- Bucket mapping: rollout percentage maps to bucket range. E.g., 25% rollout → buckets 0-2499 = treatment, 2500-9999 = control.
- Stickiness: assignment is stable for a given (flagKey, userId) pair. Changing rollout percentage from 25% to 50% means buckets 0-4999 = treatment. Users already in treatment (0-2499) stay. New users (2500-4999) enter treatment. No existing user moves from treatment to control.
- Multivariate: traffic split defined per variant. E.g., control=50%, treatment_a=25%, treatment_b=25% → buckets 0-4999=control, 5000-7499=treatment_a, 7500-9999=treatment_b.

Flag evaluation API:
- POST /api/flags/evaluate — body: { flagKey, userId, attributes? }. Returns: { variant, flagKey, userId, evaluationId }.
- Evaluation logic (in order): (1) kill switch active → return forced variant. (2) targeting rules (evaluate in priority order, first match wins). (3) percentage rollout via bucketing. (4) no match → default variant.
- evaluationId is a unique ID for this evaluation event (used in exposure logging).

Targeting rules:
- Rules are ordered by priority (lower number = higher priority).
- Rule structure: { priority, conditions: [{ attribute, operator, value }], variant }.
- Supported operators: equals, not_equals, in (list), not_in, greater_than, less_than, contains, starts_with.
- Conditions within a rule are AND-ed. Rules are evaluated top-to-bottom; first matching rule wins.
- Built-in attributes: userId, country, plan, platform. Custom attributes passed in evaluate request.

Exposure logging:
- Every flag evaluation that returns a variant MUST log an exposure event.
- Exposure event schema: { evaluationId, flagKey, userId, variant, timestamp (UTC), attributes (subset), source (service name) }.
- Exposure logging is fire-and-forget: logging failure must NOT block flag evaluation. Failed events are buffered and retried.
- Idempotency: same evaluationId logged twice → deduplicated in analysis.
- Exposure events are written to an append-only events table.

Conversion events:
- Services send conversion events: POST /api/events/conversion — body: { userId, eventName, value?, timestamp?, properties? }.
- Conversion event schema: { id, userId, eventName, value (optional numeric), timestamp (UTC), properties (JSON) }.
- Conversion events are independent of flags — analysis joins them by userId + time window.

Experiment analysis:
- GET /api/experiments/:id/results — returns per-variant metrics.
- For each variant: exposures count, conversions count, conversion rate, absolute lift vs control.
- Sample ratio mismatch (SRM) detection: compare actual exposure counts per variant to expected ratio. If chi-squared test p-value < 0.01, flag SRM warning. SRM means randomization is broken — results are unreliable.
- v1: report conversion rate + absolute lift + SRM detection. Stretch: confidence intervals, sequential testing warnings.

Kill switch:
- POST /api/flags/:key/kill — body: { variant }. Immediately overrides all rules.
- POST /api/flags/:key/kill/release — removes kill switch, resumes normal evaluation.
- Kill switch propagation SLO: all services must evaluate the new variant within 30 seconds.
- Propagation mechanism: Redis pub/sub notifies all connected services; services invalidate local cache immediately.

Flag change propagation:
- Normal flag changes (rule updates, rollout %, new experiments): propagated via Redis pub/sub.
- Services maintain a local cache of flag configurations.
- Cache TTL: 60 seconds (normal). Kill switch: immediate invalidation via pub/sub.
- If Redis pub/sub is down: services fall back to polling every 60 seconds. Kill switch degrades to poll-based (60s worst case — acceptable degradation).

Mutual exclusion (experiment isolation):
- Experiments can be assigned to "layers." Each layer gets an independent hash salt.
- Users are bucketed independently per layer: being in experiment A (layer 1) does not affect bucketing in experiment B (layer 2).
- Within the same layer: experiments are mutually exclusive (a user can only be in one experiment per layer).
- Default: each experiment is in its own layer (no mutual exclusion needed). Explicit layer assignment is required for isolation.

Failure model:
- Flag evaluation service unavailable: calling service uses last cached variant. If no cache, return default variant (control).
- Exposure logging fails: buffer locally, retry with exponential backoff. Accept data loss for exposure events (analysis accuracy degrades gracefully).
- Redis pub/sub down: degrade to polling (60s TTL). Kill switch propagation degrades from 30s to 60s.
- Database unavailable: serve from Redis cache. No new experiments can be created.

Safety invariants:
- Same (flagKey, userId) ALWAYS returns the same variant within one flag configuration version.
- Kill switch overrides ALL other evaluation logic (no exceptions).
- A user is never in two mutually exclusive experiments in the same layer.

Liveness goals:
- Flag changes eventually propagate to all services (within 60s normal, 30s kill switch).
- Exposure events are eventually logged (buffered and retried on failure).

Data model:
- flags: id, key (UNIQUE), name, description, variants (JSON array), defaultVariant, killSwitchVariant (NULL if inactive), status (active/archived), createdAt, updatedAt
- targeting_rules: id, flagId (FK), priority (INTEGER), conditions (JSON), variant, createdAt
- experiments: id, flagId (FK), name, primaryMetric, trafficPercent, status (draft/running/paused/completed), startedAt, endedAt, layer (TEXT, default: experimentId)
- exposures: id, evaluationId (UNIQUE), flagKey, userId, variant, source, timestamp, createdAt
- conversions: id, userId, eventName, value (NUMERIC), properties (JSON), timestamp, createdAt
- flag_audit: id, flagKey, action, actor, details (JSON), createdAt

Data quality:
- Duplicate exposure events (same evaluationId): deduplicated on insert (UNIQUE constraint).
- Late-arriving conversions: accepted if within 7 days of experiment end. Later arrivals ignored.
- Missing conversions: expected (not all exposed users convert). Analysis handles this.
- Bot traffic: exclude userId patterns matching known bots (configurable exclusion list).

Sample data:
- 2 flags: "new-checkout" (boolean, 50% rollout, running experiment) and "dark-mode" (boolean, 100% rollout, no experiment).
- 1 experiment on "new-checkout" with 1000 pre-generated exposure events (500 control, 500 treatment) and 120 conversion events (50 control, 70 treatment).
- Targeting rule: "new-checkout" → variant=treatment for userId in internal-testers allowlist (overrides rollout).

Scope tiers:
- MVP (required): Flag CRUD + deterministic bucketing + evaluate endpoint + exposure logging. Verify: same userId always gets same variant. API-only.
- Core (recommended): + Targeting rules + kill switch with Redis pub/sub propagation + conversion events + experiment results (conversion rate + SRM detection) + audit log.
- Stretch (optional): + Mutual exclusion layers + confidence intervals + sequential testing warnings + bot filtering + flag change history + metrics dashboard.
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: Assignment unit — userId, deviceId, or anonymous session ID?
2. Decision needed: Sticky assignment lifetime — forever, or until experiment is reset?
3. Decision needed: Exposure logging — on every evaluation, or only on first evaluation per (user, flag) pair?
4. Decision needed: If userId is missing from the request, return default variant or random bucket?
5. Decision needed: Kill switch semantics — immediate override for all users, or only new evaluations?
6. Decision needed: Mutually exclusive experiments — needed for v1, or Stretch?
7. Decision needed: Bot filtering — how to detect and exclude bot traffic?
8. Decision needed: Exposure event retention — how long are events kept?
9. Decision needed: Rebucketing — when rollout percentage changes mid-experiment, can users move between variants?
10. Decision needed: Sample ratio mismatch — detection only, or auto-pause the experiment?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/R-feature-flag-experimentation-answers.md`](_answers/R-feature-flag-experimentation-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] Deterministic bucketing algorithm with hash function and bucket ranges
- [ ] Flag evaluation logic with priority order
- [ ] Exposure logging schema and semantics
- [ ] Kill switch with propagation SLO
- [ ] Failure model and safety invariants
- [ ] SRM detection mechanism
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
For sample data: the 1000 exposure events should be spread across 7 days with realistic timestamps. The conversion events should have a higher rate in treatment (70/500 = 14%) vs control (50/500 = 10%) — this is a realistic 4% absolute lift. Include one day with anomalous exposure counts (SRM signal) to test detection.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] All 10 decision questions resolved
- [ ] Bucketing algorithm is fully deterministic and testable with known inputs
- [ ] Exposure deduplication strategy is clear
- [ ] Kill switch propagation path is defined (pub/sub → cache invalidation)
- [ ] SRM detection uses chi-squared test with explicit p-value threshold

---

### Plan

```
/speckit.plan Use Node.js with Express and PostgreSQL. Redis for flag configuration cache and pub/sub propagation. Deterministic bucketing uses a stable hash function (e.g., MurmurHash3 or FNV-1a of "{flagKey}:{userId}" modulo 10000). Exposure events in PostgreSQL with evaluationId UNIQUE constraint for deduplication. Kill switch uses Redis pub/sub for immediate invalidation + Redis cache override. Experiment analysis queries PostgreSQL (JOIN exposures and conversions by userId + time window). SRM detection: chi-squared goodness-of-fit test comparing observed vs expected variant counts.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Evaluation engine, propagation architecture, analysis pipeline |
| `data-model.md` | flags, targeting_rules, experiments, exposures, conversions, flag_audit |
| `research.md` | Hash functions for bucketing, SRM detection math, pub/sub patterns |
| `quickstart.md` | Test scenarios: deterministic bucketing, kill switch propagation, SRM |

**Validate the plan:**

```
Review the plan and check: (1) Is the hash function deterministic and stable across services? (2) Does the kill switch bypass all caches? (3) Is exposure logging fire-and-forget (never blocks evaluation)? (4) Does SRM detection use a proper statistical test? (5) Are there test cases for: same user across services, rollout percentage change, kill switch timing?
```

**Checkpoint:**
- [ ] Hash function is deterministic, stable, and uniform
- [ ] Kill switch propagation: pub/sub → immediate cache invalidation → 30s SLO
- [ ] Exposure logging is async (fire-and-forget with retry)
- [ ] SRM detection has a concrete test (expected vs observed counts)
- [ ] Evaluation order: kill switch → targeting rules → percentage rollout → default

---

### Tasks

```
/speckit.tasks
```

**What to observe:**
- Deterministic bucketing function is an early, independently-testable pure function
- Flag evaluation engine comes before any API endpoint
- Exposure logging is a separate concern (not embedded in evaluation)
- Kill switch is tested with timing assertions (propagation SLO)
- SRM detection is a separate analysis task with known test data
- MVP / Core / Stretch ordering respected

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Focus on the determinism contract — is there a test that evaluates the same (flagKey, userId) on two different "services" (or two calls) and verifies identical results? Is there a test for the SRM detection with the pre-loaded anomalous data?

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- Hash function produces the same result for the same input (test with known values)
- Rollout percentage change does not move existing users OUT of treatment (monotonic expansion)
- Kill switch evaluation happens BEFORE targeting rules and rollout
- Exposure event is logged AFTER evaluation returns (non-blocking)
- evaluationId is unique per evaluation (UUID or similar)
- Conversion events are independent of flags (no flagKey in conversion schema)
- SRM detection correctly flags the anomalous day in sample data

---

## Extension Activities

### Add a Feature: Server-Side SDK

External services need to evaluate flags locally (not via HTTP API) for performance. Build a server-side SDK that syncs flag configurations and evaluates locally. The SDK must produce identical results to the API.

```
/speckit.specify Build a server-side SDK for FlagShip. The SDK connects to the flag service, syncs configurations, and evaluates flags locally (no HTTP call per evaluation). Requirements: (1) evaluation results must be IDENTICAL to the API for the same inputs, (2) SDK maintains a local cache of flag configs, updated via streaming connection or polling, (3) kill switch propagation works via the streaming connection, (4) exposure events are buffered and batch-sent every 10 seconds. How do you test that SDK evaluation matches API evaluation exactly?
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test: Multi-Surface Experimentation

What if you need to run experiments across web, mobile, email, and push notifications? Each surface has different evaluation timing, different user identification, and different conversion tracking. How does the spec change?

```
/speckit.specify Extend FlagShip for multi-surface experimentation. An experiment can span web (userId), mobile app (deviceId), and email (emailHash). The same user might have different IDs on different surfaces. How do you: (1) ensure consistent bucketing across surfaces? (2) attribute conversions to the correct experiment exposure? (3) handle the case where a user sees treatment on web but isn't exposed on mobile? Define an identity resolution strategy and a cross-surface attribution model.
```

This bridges to the identity resolution problem in Scenario C (OIDC SSO — user identity across systems).
