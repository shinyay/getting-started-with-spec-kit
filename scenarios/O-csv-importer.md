# Scenario O: CSV Data Importer + Reporting Dashboard

| | |
|---|---|
| **Level** | ⭐⭐ Intermediate |
| **Duration** | ~100 min |
| **Key SDD themes** | Data import/validation pipeline, aggregation correctness, money handling |
| **Why it tests SDD** | "Just parse the CSV" produces code that silently drops rows, miscounts money, and cannot explain its results — the import pipeline and validation rules must be specified as contracts |
| **Best for** | Developers learning to specify data quality rules, validation pipelines, and financial correctness |

---

## The Concept

You are building a CSV importer for personal finance — users upload a CSV of bank transactions, the system validates each row, imports valid data, and generates monthly spending reports.

Except:
- A CSV row has the amount `12.345` — do you round to `12.35` or reject? The spec must define rounding rules.
- The amount is `-50.00` with type "credit" — the sign conflicts with the type. Is that an error or auto-correctable?
- Someone uploads the same file twice — do you create duplicate transactions, or detect and block it?
- Monthly report says total expenses are `$1,234.56` — can you trace that back to which rows produced it?

This scenario teaches that **validation rules are spec, not code** — every field, every edge case, every verdict must be defined before implementation. And that **aggregation correctness is intentional** — summing formatted strings instead of integer cents produces wrong answers at scale.

This is the same skill that appears at higher difficulty in:
- Scenario D (⭐⭐⭐): Financial reporting with multi-currency, exchange rates, and regulatory constraints
- Scenario F (⭐⭐⭐): Data ingestion pipelines with schema evolution and quality scoring
- Scenario L (⭐): Calculation correctness at a simpler scale (recipe scaling)

**Tech stack:** Node.js + Express + SQLite (see [Intermediate Baseline Contract](#intermediate-baseline-contract) in WORKSHOP.md)

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a CSV data importer with financial reporting. Prioritize: never corrupt source data (original CSV is never modified; all transformations create new data), every row gets a verdict (each row is explicitly "success", "warning", or "error" — never silently skipped), validation rules are spec not code (field validation is defined before implementation), aggregation correctness (report values must be traceable to source rows; rounding strategy defined), file-level idempotency (importing the same file twice must not create duplicates; detected via file hash), and testability (include test CSVs with known edge cases; validation rules have test cases).
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Source data immutability
- [ ] Explicit row verdict system (success/warning/error)
- [ ] Validation-as-spec principle
- [ ] Aggregation correctness + rounding
- [ ] Idempotency via file hash
- [ ] Test CSV requirements

---

### Specification

```
/speckit.specify Build MoneyTrail — a CSV transaction importer with monthly spending reports.

Import pipeline (staged):
1. Upload: POST /api/import/upload (multipart file). Server receives CSV, computes importHash = SHA-256(file bytes), checks if hash already exists.
2. If importHash exists: return 200 with { message: "This file was already imported on {date}. {N} transactions were imported.", existingImportId }.
3. If new: parse CSV, validate every row, return preview: { importId, filename, totalRows, summary: { success, warnings, errors, skipped }, rows: [{ rowNum, verdict, fields, issues }] }.
4. User reviews preview in UI.
5. Confirm: POST /api/import/:importId/confirm — imports only rows with verdict "success" or "warning". Returns { imported, warned, rejected, skipped }.
6. After confirm: import is sealed. Re-uploading the same file returns the sealed import info.

Required CSV columns (case-insensitive, whitespace-trimmed):
- date: transaction date
- description: text description of the transaction
- amount: numeric amount
- type: "credit" or "debit"

Header validation:
- Case-insensitive match to required field names.
- Trim whitespace from header names.
- Extra columns beyond the 4 required: silently ignored.
- Missing required column: file-level error "Missing required column: {name}. Expected: date, description, amount, type."
- Duplicate header names: file-level error "Duplicate column: {name}."

Row verdict definitions:
- success: row passes all validation, imported normally.
- warning: row imported but with a noted issue (e.g., amount rounded, sign-type mismatch auto-corrected).
- error: row fails required validation, NOT imported.
- skipped: row is empty (all fields blank) or user excluded in preview (Stretch).

Date parsing (v1):
- Accept ONLY ISO format: YYYY-MM-DD.
- Non-ISO date → error verdict: "Date format not recognized. Expected YYYY-MM-DD."
- Stretch: configurable date format selector with re-parse.

Amount parsing:
- Must be a valid number (decimal or integer).
- Non-numeric → error: "Invalid amount: not a number."
- Implement parseCents() WITHOUT floating point multiplication. Parse by string splitting on decimal point: integer part × 100 + decimal part (padded/truncated to 2 digits). This avoids IEEE 754 issues like parseFloat("1.005") * 100 = 100.49999...
- Amount > 2 decimal places → round half-away-from-zero, attach warning: "Amount rounded from {original} to {rounded}."
- Negative amounts with type field present:
  - Sign matches type (negative + debit) → store as positive cents with type debit, attach warning: "Negative amount converted to positive debit."
  - Sign conflicts with type (negative + credit) → error: "Negative amount conflicts with credit type."
- Negative amount with type missing → error: "Amount must be positive; use type field for debit/credit."
- Description > 200 characters → truncate, attach warning: "Description truncated from {original length} to 200 characters."

Money storage:
- Store as integer cents. Display with 2 decimal places + currency symbol.
- Aggregation: sum integer cents, format for display last (never sum formatted strings).
- Single currency per import in v1 (no multi-currency).

Traceability fields:
- transactions.importId (FK → imports.id) — which import produced this transaction.
- transactions.sourceRowNum (integer) — original CSV row number (1-based, excluding header).

Data model:
- imports: id, importHash (SHA-256), filename, status ("preview" | "confirmed"), totalRows, successCount, warningCount, errorCount, skippedCount, createdAt, updatedAt.
- transactions: id, importId (FK), sourceRowNum, date (TEXT, YYYY-MM-DD), description (TEXT, max 200), amountCents (INTEGER), type ("credit" | "debit"), category (TEXT), createdAt, updatedAt.
- categories: id, name (TEXT, UNIQUE). Predefined: Housing, Food, Transport, Shopping, Entertainment, Health, Income, Other.
- auto_rules: id, pattern (TEXT, case-insensitive substring), categoryId (FK), priority (INTEGER, lower = higher priority). First matching rule wins; no match → "Other."

Auto-categorization:
- Ordered list of { pattern, category } rules.
- Pattern is case-insensitive substring match on description.
- First matching rule wins; no match → "Other."
- Manual category override on any transaction persists — auto-rules do NOT override manual changes on re-categorize.

Reporting:
- GET /api/reports/monthly?year=2025&month=1 — monthly summary: total income (sum credit cents), total expenses (sum debit cents), net (income - expenses), breakdown by category.
- GET /api/reports/trend?months=12 — last N months: monthly totals for income, expenses, net.
- Reports assigned by transaction date (not import date).
- Months with no transactions: show as $0.00 for all values (not omitted from response).

File-level idempotency:
- v1: If importHash already exists → block re-import with informational 200 response.
- Stretch: "Import again anyway" override via POST /api/import/upload with field force=true, which creates a new import record even if hash exists.
- Row-level duplicate detection (same date + description + amount + type across imports) is a Stretch warning-only feature, never auto-skip.

Sample data:
- 1 confirmed import with 20 transactions across 3 months (varied categories).
- 1 test CSV file with known edge cases: rounded amount, empty row, negative amount, missing date.
- 3 auto-categorization rules pre-configured.

Scope tiers:
- MVP (required): CSV upload + parse + validate + preview + confirm + transaction list. API-first; minimal upload page.
- Core (recommended): + Auto-categorization rules + manual category edit + monthly report endpoint.
- Stretch (optional): + Trend chart + row-level duplicate warnings + date format selector + "import again anyway" override + large file streaming.
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: Date format — accept only ISO YYYY-MM-DD, or auto-detect multiple formats?
2. Decision needed: Extra CSV columns not in schema — ignore silently, or show a warning?
3. Decision needed: Character encoding — assume UTF-8 only, or attempt BOM/heuristic detection?
4. Decision needed: Negative amounts — convert based on sign, or reject as invalid?
5. Decision needed: Can users edit a transaction's amount/date after import, or only category?
6. Decision needed: Reports assigned by transaction date or import date?
7. Decision needed: If a user manually set a category, should auto-rules override on a bulk re-categorize?
8. Decision needed: Large CSV (50K+ rows) — import all at once or batch with progress?
9. Decision needed: Months with no transactions in reports — show $0.00 or omit?
10. Decision needed: Rounding direction for amounts with more than 2 decimal places?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/O-csv-importer-answers.md`](_answers/O-csv-importer-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] Import pipeline with all 6 stages
- [ ] Row verdict system with all 4 types
- [ ] Amount parsing rules including parseCents() note
- [ ] File-level idempotency via SHA-256
- [ ] Traceability: importId + sourceRowNum on transactions
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguities above
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify
```

Review the questions surfaced. Use the 10 decision questions above as a checklist — did the AI catch all of them?

**Manual refinement:**

```
For sample data: the test CSV must include at least these edge cases in specific rows: (1) an amount with 3 decimal places that gets rounded, (2) a completely empty row, (3) a negative amount with type "debit" (auto-correct case), (4) a negative amount with type "credit" (error case), (5) a missing date field, (6) a description with 250+ characters. The 20 confirmed transactions should span January through March 2025 with at least 3 different categories.
```

**Checkpoint:**
- [ ] All 10 decision questions resolved
- [ ] parseCents() approach documented (string splitting, not float multiplication)
- [ ] File-level vs row-level idempotency clearly separated
- [ ] Report aggregation uses transaction date, not import date

---

### Plan

```
/speckit.plan Use Node.js with Express, better-sqlite3, and multer for file upload. Follow the Intermediate Baseline Contract. CSV parsing with a streaming parser (csv-parse). Money stored as integer cents — implement parseCents() by string splitting on decimal point (no floating-point multiplication). File hash with crypto.createHash('sha256'). Traceability: every transaction row stores importId and sourceRowNum. Reports sum integer cents, format for display last.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Import pipeline architecture, validation engine design |
| `data-model.md` | imports, transactions, categories, auto_rules tables |
| `research.md` | CSV edge cases, money-as-cents pattern, SHA-256 hashing |
| `quickstart.md` | Test CSV files with expected verdicts |

**Validate the plan:**

```
Review the plan and check: (1) Does parseCents() use string splitting, not parseFloat * 100? (2) Is file hash computed before any row processing? (3) Are row verdicts assigned during validation, not during import? (4) Does the preview response include every row with its verdict? (5) Are reports aggregating integer cents, not formatted strings?
```

**Checkpoint:**
- [ ] parseCents() is a pure function using string operations
- [ ] Import pipeline is staged (upload → preview → confirm)
- [ ] File hash checked before row-level processing
- [ ] Traceability fields in data model

---

### Tasks

```
/speckit.tasks
```

**What to observe:**
- parseCents() and date validation are early, independently-testable pure functions
- CSV parsing produces row objects before validation (separation of concerns)
- Validation engine processes rows and assigns verdicts (separate from import)
- Preview is generated and returned before any database writes
- Confirm step does the actual INSERT
- Report queries sum amountCents, not formatted values
- MVP / Core / Stretch ordering respected

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Check: does every row verdict have a corresponding test case? Is there a test for the "same file uploaded twice" idempotency path?

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- `parseCents("1.005")` returns `101` (correct), not `100` (float bug)
- File hash is SHA-256 of raw bytes (not parsed content)
- Preview returns ALL rows with verdicts (not just errors)
- Confirm only imports success + warning rows
- Reports use `SUM(amountCents)` in SQL (not application-layer string sums)
- Empty rows are "skipped", not "error"
- Manual category edits survive re-categorization runs
- Months with no data return `$0.00` (not omitted)

---

## Extension Activities

### Add a Feature: CSV Export

Export filtered transactions back to CSV, matching the original input format. How do you handle the fact that amounts are stored as cents but need to display as dollars? What about transactions whose descriptions were truncated on import?

```
/speckit.specify Add CSV export to MoneyTrail. Users can export filtered transactions (by date range, category, import) back to a CSV file. The exported CSV must use the same column format as the import (date, description, amount, type). How do you convert integer cents back to decimal amounts without floating-point drift? What about truncated descriptions — do you export the truncated version or flag it?
```

### Stress-test: Multi-Currency

What if the CSV contains transactions in different currencies (USD, EUR, GBP)? Aggregation across currencies requires exchange rates. Monthly reports need per-currency subtotals AND a converted total.

```
/speckit.specify Add multi-currency support to MoneyTrail. CSVs may include a "currency" column (ISO 4217 codes). If present: store currency per transaction, aggregate per currency in reports, and provide a "converted total" using configurable exchange rates. If the currency column is missing, default to USD. How do you handle exchange rate updates — fixed at import time, or live at report time?
```

This bridges directly to Scenario D (financial dashboard with multi-currency).
