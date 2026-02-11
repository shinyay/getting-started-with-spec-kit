# Scenario M: URL Shortener with Analytics API

| | |
|---|---|
| **Level** | ⭐⭐ Intermediate |
| **Duration** | ~100 min |
| **Key SDD themes** | API contract design, HTTP redirect semantics, cursor pagination, error handling |
| **Why it tests SDD** | HTTP status codes, redirect caching, and error formats have precise semantics that "just return a redirect" hand-waves away — vague API contracts break every client |
| **Best for** | Developers learning REST API design and HTTP contract specification |

---

## The Concept

You are building a URL shortener — users submit a long URL, get a short link back, and visitors to the short link are redirected to the original. Simple, right?

Except:
- Should the redirect be 301 (permanent, browsers cache) or 302 (temporary, trackable)? The choice changes analytics accuracy.
- What does a deleted short link return — 404 (not found) or 410 (gone)? The distinction matters for SEO and user experience.
- If someone shortens the same URL twice, do they get the same link or a new one? The answer defines your idempotency model.
- When the redirect route `/:slug` conflicts with `/api/links`, which wins? Express route ordering is a real bug.

This scenario teaches that **API contracts are the product** — the exact status codes, response shapes, and error formats ARE what consumers depend on. Without a spec, the AI will make confident but arbitrary choices for each of these.

This is the same skill that appears at higher difficulty in:
- Scenario I (⭐⭐⭐): API v2 response contracts must be precisely defined and backward-compatible
- Scenario C (⭐⭐⭐): Auth API endpoints have security-sensitive contract requirements

**Tech stack:** Node.js + Express + SQLite (see [Intermediate Baseline Contract](#intermediate-baseline-contract) in WORKSHOP.md)

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a URL shortener API service. Prioritize: API contracts are the product (request/response shapes and status codes must be specified before implementation), redirect correctness (HTTP redirect status 301 vs 302 must be explicit and testable), no silent failures (every API error returns the standard JSON error envelope; browser redirect routes return deterministic human-readable HTML error pages), idempotency by design (same normalized URL returns the same active short link), privacy by default (never store IP addresses or full user-agent strings in analytics), and testability (contract tests for every endpoint).
```

**Checkpoint** — verify the generated constitution includes:
- [ ] API-first / contract-first principle
- [ ] Redirect correctness with specific HTTP semantics
- [ ] Error handling split: JSON for API, HTML for browser routes
- [ ] Idempotency rule
- [ ] Privacy constraints for analytics
- [ ] Testing requirements

---

### Specification

```
/speckit.specify Build ShortLink — a URL shortener API with click analytics.

API endpoints:
- POST /api/shorten — create short link. Normalizes URL, checks for existing active link for same normalized URL. If exists → return existing (200). If new → create (201). Returns { id, slug, shortUrl, originalUrl, createdAt }.
- GET /:slug — redirect to original URL. This IS the product.
- GET /api/links/:id — get link details + click count.
- GET /api/links/:id/stats — analytics: clicks per day (last 30 days), top 10 referrer domains.
- GET /api/links — list all links with cursor-based pagination.
- DELETE /api/links/:id — soft-delete. Returns 200 with { deletedAt }. Deleting already-deleted link returns 200 (idempotent).

Route safety:
- GET /:slug only matches slugs satisfying ^[A-Za-z0-9-]{3,30}$
- Reserved paths that must never match as slugs: api, assets, health, favicon.ico
- Implementation note: mount /api/* routes BEFORE the slug catch-all.

URL normalization rules (v1):
- Trim whitespace. Require scheme: only http and https (reject javascript:, data:, etc.). Lowercase scheme and hostname. Remove default ports (:80 for http, :443 for https). Preserve path + query as-is (no query param sorting in v1).

Redirect behavior (301 vs 302 only — no 307/308 in v1):
- Default: 302 Found (temporary — allows analytics on every visit, no browser caching).
- Optional permanent: true on creation → 301 Moved Permanently (browsers cache; fewer analytics hits).
- Only GET and HEAD methods are redirected; other methods → 405 Method Not Allowed.
- HEAD requests: redirect with Location header but no body. Do NOT record analytics for HEAD (only GET).
- Deleted links → 410 Gone. Expired links (if expiry enabled) → 410 Gone with expiry info.

Error behavior split:
- GET /:slug errors (browser route): return HTML error page. 404 = "Link not found." 410 = "This link has been removed."
- /api/* errors: always return JSON error envelope { error: { code, message, suggestion } }.

Idempotency:
- POST /api/shorten: same normalized URL returns the same ACTIVE short link (200). If the previous link for that URL was deleted, create a new link with a new slug (201). Old slug remains 410 forever.
- Principle: "Same normalized URL returns the same active short link."

ID generation:
- Base62 slugs (a-z, A-Z, 0-9), 7 characters default.
- Collision: UNIQUE constraint on slug column. If violated, retry with new slug (up to 3 attempts, then 8-char slug).
- Vanity slugs: user-provided custom slug matching ^[A-Za-z0-9-]{3,30}$. If collision with existing → 409 Conflict.

Pagination (cursor-based):
- Query: ?limit=20&cursor=<opaque>. Default limit: 20, max: 100.
- Ordering: createdAt DESC.
- Cursor: opaque base64-encoded string referencing last item's createdAt + id.
- Response: { data: [...], pagination: { cursor: "...", hasMore: true } }. When hasMore is false, cursor is null.
- Invalid cursor → 400 with code INVALID_CURSOR.

Analytics:
- Record on GET redirect only (not HEAD).
- Store: timestamp (UTC), referrerDomain (parsed host or null from Referer header).
- Never store: IP address, full user-agent, full referrer URL, cookies.
- Analytics insert failure must NOT block redirect — redirect succeeds, failure logged server-side.
- Stats endpoint: clicks per day for last 30 days + top 10 referrer domains.

Rate limiting:
- 100 requests/min per IP for POST /api/shorten.
- No rate limit on GET redirects.
- Headers: X-RateLimit-Remaining, X-RateLimit-Reset (Unix epoch).
- Over limit: 429 Too Many Requests with Retry-After header.

Delete semantics:
- Soft-delete: link stays in DB with deletedAt timestamp.
- GET /api/links/:id after deletion → 200 with full resource including deletedAt field.
- GET /:slug after deletion → 410 Gone (HTML).
- Deleted slugs cannot be reused for new links (tombstoned).

Sample data:
- 3 pre-created short links (one with 50+ clicks for stats demo, one expired, one active with zero clicks)
- 5 pre-recorded clicks with varied timestamps and referrer domains

Scope tiers:
- MVP (required): POST shorten + GET redirect (302) + GET link details + contract tests (API-only; test with curl)
- Core (recommended): + List (paginated) + DELETE (410 Gone) + click tracking + stats endpoint + minimal admin UI
- Stretch (optional): + Vanity slugs + rate limiting (429 + headers) + link expiry + bot detection
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: Should creating a short link for an already-shortened URL return the existing link (200) or always create a new one (201)?
2. Decision needed: What redirect status code should be the default — 302 or 301? What are the analytics tradeoffs?
3. Decision needed: Should deleted links return 404 (not found) or 410 (gone)? Why does the HTTP distinction matter?
4. Decision needed: How long should click analytics be retained — 30 days, 90 days, or indefinitely?
5. Decision needed: Should vanity slugs be case-sensitive ("MyLink" ≠ "mylink")?
6. Decision needed: What happens if a vanity slug collides with an existing random slug?
7. Decision needed: Should we detect redirect chains (our short link → another short link on our service)?
8. Decision needed: Should HEAD requests count as analytics clicks?
9. Decision needed: What does `GET /:slug` return on error — HTML page, JSON, or plain text?
10. Decision needed: If URL X was shortened then deleted, what does POST shorten return for URL X later?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/M-url-shortener-answers.md`](_answers/M-url-shortener-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] API endpoint table with methods, paths, and response shapes
- [ ] Redirect behavior with explicit HTTP status codes
- [ ] Error format split (JSON for API, HTML for browser)
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguities above
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify
```

Review the questions surfaced by Spec Kit. Use the deliberate ambiguity list above as a checklist — did the AI catch all 10? If not, add the missed ones manually.

**Manual refinement** — add details the AI missed:

```
For sample data: one short link should have 50+ recorded clicks spread over 10 days so the stats endpoint has meaningful data to demonstrate. Include at least 3 different referrer domains. The expired link should have expired yesterday.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] All 10 decision questions resolved
- [ ] Redirect semantics are unambiguous (301 vs 302, GET vs HEAD, deleted vs expired)
- [ ] Route safety rules are explicit
- [ ] Error format per route type is defined

---

### Plan

```
/speckit.plan Use Node.js with Express and better-sqlite3. Follow the Intermediate Baseline Contract: standard error envelope, cursor pagination, ISO 8601 dates, PRAGMA foreign_keys = ON, createdAt/updatedAt on all tables. Mount /api/* routes before the /:slug catch-all. Slug route uses a regex parameter constraint. Analytics recording is fire-and-forget (try/catch around insert, never blocks redirect). Contract tests use supertest.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Architecture with route mounting strategy |
| `data-model.md` | links table, clicks table, schema |
| `research.md` | HTTP redirect caching, Base62 encoding, cursor pagination |
| `quickstart.md` | Contract test scenarios |

**Validate the plan:**

```
Review the plan and check: (1) Are /api routes mounted before /:slug? (2) Is the slug route constrained by regex? (3) Does analytics use fire-and-forget (never blocks redirect)? (4) Are contract tests defined for each endpoint? (5) Is URL normalization a pure function?
```

**Checkpoint:**
- [ ] Route mounting order is explicit
- [ ] Redirect and API error handling are separate middleware
- [ ] Analytics is isolated from redirect path
- [ ] URL normalization is a testable pure function

---

### Tasks

```
/speckit.tasks
```

**What to observe:**
- URL normalization + slug generation are early pure-function tasks
- Route mounting order is a specific task, not implicit
- Contract tests are written alongside each endpoint (not deferred)
- Analytics is decoupled from redirect handler
- MVP / Core / Stretch ordering respected

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Especially valuable here — verify every HTTP status code in the spec has a corresponding contract test in the tasks.

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- `/api/*` routes mounted before `/:slug`
- Slug route uses regex constraint
- 302 is the default redirect (not 301)
- Analytics insert is wrapped in try/catch (never throws to the redirect handler)
- DELETE is idempotent (second delete returns same response)
- Pagination cursor is opaque (not a raw ID)
- No PII in the clicks table

---

## Extension Activities

### Add a Feature: Custom Domains

```
/speckit.specify Add custom domain support to ShortLink. Users can register a domain (e.g., short.myco.com) and links created under that domain use its namespace. The same slug can exist on different domains. The API needs a domain parameter on creation, and the redirect route must resolve the correct link based on the Host header.
```

Then continue through `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test: Add Authentication

What if links are user-owned and private? How do redirect semantics change when auth is required? Does a private link redirect unauthenticated users or show an error?

```
/speckit.specify Add authentication to ShortLink. Users sign up, log in, and own their links. Links can be public (anyone can use the redirect) or private (only the creator can view analytics). How does this change the redirect route? Does GET /:slug for a private link still redirect, or require auth?
```

This bridges directly to Scenario C (OIDC SSO + RBAC).
