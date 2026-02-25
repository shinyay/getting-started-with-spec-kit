# Task 06: Chapter 3 — Intermediate Scenarios (16 slides)

> **Purpose:** Introduce server-side development. Learn to specify API contracts, HTTP semantics, and data validation.
> **Target Level:** ⭐⭐ Intermediate (Node.js fundamentals required)
> **Plan reference:** `slides/SLIDE-PLAN-EN.md` lines 209–250
> **JP reference:** `slides/spec-kit-presentation.md` lines 1600–1900
> **Scenarios:** `scenarios/H-cross-platform-cli.md`, `scenarios/M-url-shortener.md`, `scenarios/N-kanban-board.md`, `scenarios/O-csv-importer.md`

---

## Section 3.1: Intermediate Scenario Introduction (3 slides)

### Slide 3-1: Chapter 3 Section Divider

**Plan ref:** Line 219

```markdown
---

<!-- _paginate: false -->
<!-- _header: "" -->

# Chapter 3: Intermediate — Server-Side & API Contracts
```

---

### Slide 3-2: Intermediate Scenarios

**Plan ref:** Line 220

```markdown
---

## Section 3.1: Introduction

# Intermediate Scenarios

| Scenario | Build | SDD Skills |
|---|---|---|
| **H: CLI** | Cross-platform CLI tool | Output contract, exit codes |
| **M: ShortLink** | URL shortener + analytics | API contract, HTTP semantics |
| **N: KanbanFlow** | Kanban board | Ordering algorithms, intent-based API |
| **O: MoneyTrail** | CSV expense importer | Data validation pipeline |

> Add a server. **API contracts become the center of your specs.**
```

---

### Slide 3-3: Baseline Contract

**Plan ref:** Line 221

```markdown
---

## Section 3.1: Introduction

# Baseline Contract — Shared by All ⭐⭐ Scenarios

All intermediate scenarios share these conventions:

- **Standard error envelope** — JSON `{ error: { code, message } }`
- **Cursor pagination** — `?cursor=<token>&limit=20`
- **ISO 8601 dates** — `2026-02-25T21:36:37Z`
- **DB conventions** — `PRAGMA foreign_keys = ON`, `id` / `createdAt` / `updatedAt`
- **Standard scripts** — `npm start` / `npm test`

> **A shared baseline means each scenario focuses on its unique SDD lesson**
```

---

## Section 3.2: Scenario M — ShortLink: API Contract Design (7 slides)

### Slide 3-4: Scenario M: ShortLink

**Plan ref:** Line 227

```markdown
---

## Section 3.2: ShortLink Walkthrough

# Scenario M: ShortLink — URL Shortener + Analytics

Looks simple. But when you write the spec, questions emerge:

- 301 vs 302 redirect?
- Route ordering in Express?
- What happens to deleted short URLs?
- Shorten the same URL twice — new slug or existing?

> SDD lesson: **The API contract IS the product**
```

---

### Slide 3-5: HTTP Status Codes Are Part of the Spec

**Plan ref:** Line 228

```markdown
---

## Section 3.2: ShortLink Walkthrough

# HTTP Status Codes Are Part of the Spec

| | 301 Permanent | 302 Temporary |
|---|---|---|
| **Browser behavior** | Caches redirect | Hits server each time |
| **Analytics** | ❌ Stops counting | ✅ Every click recorded |
| **SEO** | Transfers link equity | Preserves original URL |

> **Status code selection is a business decision, not a technical one.**
> Without specs, AI picks one — your analytics may break silently.
```

**Notes:**
- This is Chapter 3's "aha moment" — `301 vs 302 breaks your analytics!`

---

### Slide 3-6: Route Safety — Express Mount Order

**Plan ref:** Line 229

```markdown
---

## Section 3.2: ShortLink Walkthrough

# Route Safety — Express Mount Order

```javascript
// ❌ Wrong order — /:slug catches EVERYTHING
app.get('/:slug', redirectHandler);
app.get('/api/health', healthHandler);   // Never reached!

// ✅ Correct order — mount /api/* first
app.get('/api/health', healthHandler);
app.get('/api/shorten', shortenHandler);
app.get('/:slug', redirectHandler);      // Last = catch-all
```

> **Route ordering must be explicitly specified in the API contract**
```

---

### Slide 3-7: Idempotency — Shorten the Same URL Twice?

**Plan ref:** Line 230

```markdown
---

## Section 3.2: ShortLink Walkthrough

# Idempotency — Shorten the Same URL Twice?

### Option A: Generate a new slug
- Response: `201 Created` with a new short URL
- Same long URL → multiple short URLs

### Option B: Return existing active link
- Response: `200 OK` with the existing short URL
- Same long URL → always the same short URL

> **SDD resolves this in Clarify.**
> Without specs, AI picks one arbitrarily.
```

---

### Slide 3-8: Deletion Semantics — 404 vs 410

**Plan ref:** Line 231

```markdown
---

## Section 3.2: ShortLink Walkthrough

# Deletion Semantics — 404 vs 410

| | 404 Not Found | 410 Gone |
|---|---|---|
| **Meaning** | "Never existed" | "Once existed, now deleted" |
| **Slug reuse** | Slug can be reused | Slug permanently reserved |
| **Guarantee** | None | Slug permanence |

**Recommended:** `410 Gone` + tombstone record

> **Deletion semantics are business rules, not HTTP defaults.**
> The slug `abc123` was shared on Twitter — it must never point somewhere else.
```

---

### Slide 3-9: Error Format Split

**Plan ref:** Line 232

```markdown
---

## Section 3.2: ShortLink Walkthrough

# Error Format Split

| Consumer | Endpoint | Error Format |
|---|---|---|
| **Browser** | `GET /:slug` | HTML error page |
| **API client** | `POST /api/shorten` | JSON error envelope |
| **API client** | `GET /api/stats/:slug` | JSON error envelope |

> **Same app, different consumers = different error formats.**
> The spec must define error format per endpoint, not globally.
```

---

### Slide 3-10: ShortLink Takeaways

**Plan ref:** Line 233

```markdown
---

## Section 3.2: ShortLink Walkthrough

# ShortLink Takeaways

1. **HTTP status codes are part of the spec** — 301 vs 302 is a business decision
2. **Route ordering must be specified** — `/:slug` catches everything
3. **Idempotency is resolved in Clarify** — not left to AI
4. **Deletion semantics are business rules** — 404 vs 410
5. **Error format varies by consumer** — HTML for browsers, JSON for APIs

> What looks "simple" has at least **5 specification decisions** hiding beneath the surface
```

---

## Section 3.3: Other Intermediate Scenarios (3 slides)

### Slide 3-11: Scenario H: CLI — Output Contract

**Plan ref:** Line 239

```markdown
---

## Section 3.3: Other Intermediate Scenarios

# Scenario H: CLI — Output Contract

The CLI's "screen" is **stdout** — output itself IS the contract

- **stderr / stdout separation** — errors go to stderr, data to stdout
- **Exit codes** — `0` success, `1` general error, `2` usage error
- **JSON output mode** — `--json` flag for machine-readable output
- Piping: `mycli list | jq '.[] | .name'` must work

> SDD lesson: **Non-web software has contracts too.**
> Every output format decision belongs in the spec.
```

---

### Slide 3-12: Scenario N: KanbanFlow — Fractional Indexing

**Plan ref:** Line 240

```markdown
---

## Section 3.3: Other Intermediate Scenarios

# Scenario N: KanbanFlow — Fractional Indexing

Card ordering is **data** — not just UI presentation

- **Fractional indexing:** assign numeric positions between existing cards
- **Intent-based API:** client says "move card between A and B" → server calculates position
- No sequential integer IDs for order (reordering becomes expensive)

> SDD lesson: **Ordering algorithms are part of the spec.**
> Without specs, AI picks array splice or sequential IDs — both break at scale.
```

---

### Slide 3-13: Scenario O: MoneyTrail — Data Validation Pipeline

**Plan ref:** Line 241

```markdown
---

## Section 3.3: Other Intermediate Scenarios

# Scenario O: MoneyTrail — Data Validation Pipeline

Each CSV row gets a **verdict**: success / warning / error / skipped

```javascript
// ❌ The parseFloat trap
Math.round(parseFloat('1.005') * 100) // → 100, not 101!

// ✅ parseCents() — string splitting
'1.005'.split('.') → parse integer parts → 1005 cents
```

> SDD lesson: **Data quality specs design the validation pipeline.**
> Every row verdict must be defined in the spec.
```

---

## Section 3.4: Intermediate Summary (3 slides)

### Slide 3-14: Intermediate Progression

**Plan ref:** Line 247

```markdown
---

## Section 3.4: Intermediate Summary

# Intermediate Progression

| Order | Scenario | New Server-Side SDD Skill |
|---|---|---|
| 1st | **H: CLI** | Output contract (stdout/stderr/exit codes) |
| 2nd | **M: ShortLink** | API contract (HTTP semantics) |
| 3rd | **N: KanbanFlow** | Ordering algorithm specification |
| 4th | **O: MoneyTrail** | Data validation pipeline |

> Each step adds a new **server-side specification skill**
```

---

### Slide 3-15: Beginner vs Intermediate — What Changed?

**Plan ref:** Line 248

```markdown
---

## Section 3.4: Intermediate Summary

# Beginner vs Intermediate — What Changed?

| Axis | ⭐ Beginner | ⭐⭐ Intermediate |
|---|---|---|
| **Tech stack** | localStorage | SQLite + Express |
| **Spec center** | UI behavior | API contract |
| **Testing** | Manual | supertest + automated |
| **Constitution** | 4–5 principles | 6 principles |
| **Consumer** | Self (browser) | External clients |

> The spec focus shifts from **UI behavior** to **API contracts**
```

---

### Slide 3-16: Bridge to Intermediate–Advanced

**Plan ref:** Line 249

```markdown
---

## Section 3.4: Intermediate Summary

# Bridge to Intermediate–Advanced

**Intermediate:** single service + own database

**Intermediate–Advanced:** external service integrations enter the picture

- OAuth / OIDC authentication providers
- Payment processors (Stripe)
- Infrastructure as Code (Terraform)
- API versioning for existing consumers

> Where missing specs cause **real damage** — real money, real security breaches → **Chapter 4**
```

---

## ✅ Chapter 3 Quality Checks

- [ ] Section divider for Chapter 3 present
- [ ] 16 numbered slides (3-1 through 3-16)
- [ ] ShortLink walkthrough covers 301 vs 302, route safety, idempotency, deletion, error format (5 deep slides)
- [ ] "Aha moment" — 301 vs 302 breaks analytics (slide 3-5)
- [ ] Route ordering code example present (slide 3-6)
- [ ] CLI output contract covered (slide 3-11)
- [ ] Fractional indexing concept explained (slide 3-12)
- [ ] parseCents() vs parseFloat trap shown (slide 3-13)
- [ ] Beginner vs Intermediate comparison table (slide 3-15)
- [ ] Bridge to Chapter 4 emphasizes "real damage" (slide 3-16)
- [ ] All h2 labels correct
- [ ] No Japanese text
