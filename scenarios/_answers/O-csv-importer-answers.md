# Scenario O: CSV Importer — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Import Pipeline Summary

| Stage | Endpoint | What Happens |
|---|---|---|
| 1. Upload | POST `/api/import/upload` | Receive CSV, compute SHA-256, check idempotency |
| 2. Idempotency check | — | If hash exists → return 200 with existing import info |
| 3. Parse + Validate | — | Parse rows, assign verdicts, return preview |
| 4. Preview | Response from upload | `{ importId, totalRows, summary, rows }` |
| 5. Confirm | POST `/api/import/:importId/confirm` | Insert success + warning rows into transactions |
| 6. Sealed | — | Re-upload same file → returns sealed import info |

## parseCents() — Correct Implementation

```javascript
// ✅ CORRECT: String splitting (no floating-point multiplication)
function parseCents(amountStr) {
  const str = amountStr.trim();
  const negative = str.startsWith('-');
  const abs = negative ? str.slice(1) : str;
  const [intPart, decPart = ''] = abs.split('.');
  const paddedDec = (decPart + '00').slice(0, 2);
  const extraDec = decPart.length > 2 ? decPart[2] : null;
  let cents = parseInt(intPart, 10) * 100 + parseInt(paddedDec, 10);
  // Round half-away-from-zero for >2 decimal places
  if (extraDec !== null && parseInt(extraDec, 10) >= 5) cents += 1;
  return { cents, rounded: decPart.length > 2, negative };
}

// ❌ WRONG: Float multiplication
// Math.round(parseFloat("1.005") * 100) === 100 (not 101!)
```

## Row Verdict Examples

| Row | date | description | amount | type | Verdict | Issue |
|---|---|---|---|---|---|---|
| 1 | 2025-01-15 | Grocery store | 42.50 | debit | ✅ success | — |
| 2 | 2025-01-16 | Salary | 3000.00 | credit | ✅ success | — |
| 3 | 2025-01-17 | Coffee | 4.999 | debit | ⚠️ warning | "Amount rounded from 4.999 to 5.00" |
| 4 | | | | | ⏭️ skipped | Empty row |
| 5 | 2025-01-18 | Refund | -25.00 | debit | ⚠️ warning | "Negative amount converted to positive debit" |
| 6 | 2025-01-19 | Return | -10.00 | credit | ❌ error | "Negative amount conflicts with credit type" |
| 7 | 01/20/2025 | Electric bill | 85.00 | debit | ❌ error | "Date format not recognized. Expected YYYY-MM-DD." |

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Date format | ISO YYYY-MM-DD only in v1 | Avoids ambiguity (01/02 = Jan 2 or Feb 1?); multi-format is Stretch |
| 2 | Extra columns | Ignore silently | Standard CSV practice; showing warnings creates noise |
| 3 | Character encoding | UTF-8 only; reject with error if BOM detected for other encoding | Workshop simplicity; encoding detection is ⭐⭐⭐ |
| 4 | Negative amounts | Auto-correct if sign matches type (warning); error if conflicts | Teaches warning vs error distinction |
| 5 | Edit after import | Only category (v1); amount/date editing is Stretch | Preserves source data integrity |
| 6 | Report date basis | Transaction date | "When did I spend?" not "When did I import?" |
| 7 | Manual override persists | Yes — auto-rules never override manual edits | Principle: user intent takes precedence |
| 8 | Large CSV handling | All-at-once in v1; streaming is Stretch | Workshop CSVs are small; streaming adds complexity |
| 9 | Empty months | Show $0.00 | Charts need continuous data; omitting months creates misleading gaps |
| 10 | Rounding direction | Half-away-from-zero (standard financial rounding) | 4.995 → 5.00; 4.994 → 4.99 |

## Facilitator Notes

- **After Constitution**: "Principle #4 'aggregation correctness' is the sleeper lesson. Ask: what does `0.1 + 0.2` equal in JavaScript? (0.30000000000000004). This is why we store cents as integers."
- **After Specify**: "The staged import pipeline (upload → preview → confirm) is a teaching moment about separation of concerns. Validation is not import. Preview is not commitment."
- **After Clarify**: "The parseCents() question is a great 'aha' moment. Write `Math.round(parseFloat('1.005') * 100)` on the board and ask what it returns. Answer: 100, not 101."
- **After Plan**: "Check if traceability fields (importId, sourceRowNum) are in the data model. If not, reports can't trace back to source rows — violates principle #4."
- **Common mistake**: Teams compute file hash AFTER parsing (instead of on raw bytes), which means reformatted files that parse identically get different hashes.
- **Common mistake**: Reports aggregate in application code using formatted strings instead of SQL SUM(amountCents).
