# Scenario L: Recipe Collection — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Fraction System (Expected Output)

The scaling algorithm a good SDD process should produce:

1. `scaleFactor = desiredServings / baseServings` (represented as a fraction)
2. Multiply ingredient quantity × scaleFactor (fraction × fraction arithmetic)
3. Simplify result (reduce to lowest terms)
4. Find nearest representable fraction with allowed denominators (2, 3, 4, 8)
5. If best-fit error > 0.05, fall back to decimal with 1 digit
6. If within 0.02 of integer, display as integer

### Scaling Examples

| Original | Scale Factor | Raw Result | Display |
|---|---|---|---|
| ⅓ cup | ×2 | ⅔ | ⅔ cup |
| ½ cup | ×3 | 1.5 | 1 ½ cups |
| ¼ tsp | ×2 | 0.5 | ½ tsp |
| ¼ tsp | ×0.5 | 0.125 | ⅛ tsp |
| 2 eggs (piece) | ×1.5 | 3.0 | 3 eggs |
| 2 eggs (piece) | ×0.75 | 1.5 | 2 eggs (rounded from 1.5) |
| 1 egg (piece) | ×0.25 | 0.25 | 1 egg (recipe calls for ¼ — use beaten egg, measure approx) |
| to taste | ×any | — | to taste (not scaled) |
| ⅓ cup | ×1.2 | 0.4 | 0.4 cups (not representable as allowed fraction) |

## Shopping List Merge Examples

| Items to Merge | Same Dimension? | Result |
|---|---|---|
| 500g chicken breast + 300g chicken breast | Yes (g + g) | 800 g chicken breast |
| 1 cup flour + 2 cups flour | Yes (cup + cup) | 720 mL → 720 mL flour (or 3 cups) |
| 2 cups flour + 100g flour | No (volume + weight) | 2 cups flour, 100 g flour (separate lines) |
| 500g chicken breast + 300g chicken thigh | Names differ | 500 g chicken breast, 300 g chicken thigh (separate) |
| 2 tbsp olive oil + 1 cup olive oil | Yes (volume + volume) | 270 mL olive oil |

Display thresholds: volume ≥ 1000 mL → show as L (1 decimal); weight ≥ 1000 g → show as kg (2 decimals).

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Allowed denominators | 2, 3, 4, 8 — not 16 (too precise for kitchen use) | Kitchen measures rarely go below ⅛ practically |
| 2 | ¼ egg scaling down | Round UP to 1 egg with explanatory note | You can't use a quarter egg; the note teaches the user |
| 3 | Non-numeric display | Unchanged text + "(not scaled)" badge | Visual clarity that scaling didn't forget this item |
| 4 | Cup conversion constant | 240 mL (kitchen standard) | Exact 236.588 is impractical; cookbooks use 240 |
| 5 | Name matching | Exact only (case-insensitive, trimmed) | Fuzzy matching produces surprising/incorrect merges |
| 6 | Mixed-unit merge | Same dimension: convert to base + sum. Different dimensions: separate lines | Can't meaningfully merge volume + weight for same ingredient |
| 7 | Duplicate names | Allowed; distinguished by creation date in recipe list | Forcing unique names frustrates users with recipe variations |
| 8 | Minimum recipe | ≥1 ingredient OR ≥1 step total; empty sections are allowed | "How to boil water" = steps only = valid recipe |
| 9 | Week boundary | Monday; local time at page load; stored as YYYY-MM-DD | Consistent with ISO 8601 week standard |
| 10 | Non-representable fraction | Decimal with 1 digit: "0.4 cups" | "Approx" text adds uncertainty without practical value |

## Data Model Detail

```
Ingredient (numeric):
  quantity: { numerator: int, denominator: int }  // e.g., { 1, 3 } = ⅓
  unit: "cup" | "tbsp" | "tsp" | "fl oz" | "oz" | "lb" | "g" | "kg" | "mL" | "L" | "piece"
  name: string
  preparation: string | null

Ingredient (non-numeric):
  quantity: null
  unit: null
  quantityText: "to taste" | "a pinch" | "as needed"
  name: string
  preparation: string | null
```

The `quantityText` field resolves the model inconsistency: `quantity:null` + `unit:null` signals non-numeric, and `quantityText` provides the display value. Non-numeric ingredients are never passed to the scaling engine.

## Facilitator Notes

- **After Constitution**: "'Sensible kitchen defaults' sounds simple. But what IS practical precision for ⅜ cup? This is why even cooking apps need constitutional guidance."
- **After Clarify**: "'1.5 eggs' always gets a laugh. But it's the same class of problem as splitting $10.00 three ways in a billing system. Calculation correctness specs prevent real bugs."
- **After Plan**: "Ask: where does fraction arithmetic live? In the UI? In the data model? In a utility module? The answer reveals whether the plan has clean separation of concerns — fraction math is pure logic that should never touch the DOM."
