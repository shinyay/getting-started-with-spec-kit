# Scenario L: Recipe Collection & Meal Planner

| | |
|---|---|
| **Level** | ⭐ Beginner |
| **Duration** | ~90 min |
| **Key SDD themes** | Structured nested data modeling, calculation correctness, fraction arithmetic |
| **Why it tests SDD** | Recipe scaling has hidden math rules (fractions, rounding, unit conversion) that the AI will resolve arbitrarily without explicit specs |
| **Best for** | Developers learning that algorithms need correctness specifications |

---

## The Concept

You are building a recipe collection app with serving-size scaling. Everyone has followed a recipe, so the domain is immediately familiar. But recipe math is surprisingly tricky:

- `1/3 cup × 1.5 = 1/2 cup` — fraction arithmetic, not floating point
- `1 egg × 1.5 = ???` — you can't use 1.5 eggs practically; round to 2?
- `"A pinch of salt" × 2 = ???` — non-numeric quantities don't scale
- `2 cups + 2 cups = ???` — 4 cups, or should it consolidate to 1 quart?

And the data model is nested — Recipe → Sections → Ingredients + Steps — which is the first data modeling challenge.

This scenario teaches that **calculation correctness requires explicit rules for fractions, rounding, edge cases, and display**. Without them, the AI will make arbitrary choices — and every choice produces a different user experience.

This is the same skill that appears at higher difficulty in:
- Scenario D (⭐⭐⭐): Money must be tracked in integer cents; proration has precise rounding rules
- Scenario F (⭐⭐⭐⭐): Data aggregation across millions of events requires defined precision

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a personal recipe management application. Prioritize calculation correctness (scaling must produce sensible, human-readable amounts — never display "0.333333 cups"), data integrity (validate input but never silently corrupt user recipes), accessible measurements (screen reader announces "one third cup olive oil" not "0.33 cup"), sensible kitchen defaults (prefer common units; round to practical precision), simplicity (no build tools, no frameworks, localStorage only), and no data loss (confirm before deletion; persist all data across sessions).
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Calculation correctness principle
- [ ] Data integrity
- [ ] Accessibility for measurements
- [ ] Sensible rounding / kitchen defaults
- [ ] Simplicity constraints

---

### Specification

```
/speckit.specify Build RecipeBox — a personal recipe collection with serving-size scaling and meal planning.

Recipe data model (nested hierarchy):
- Recipe: title (string, required; duplicates allowed — distinguished by creation date in list), description (optional), servings (integer ≥ 1, the base serving count), prepTime (minutes, optional), cookTime (minutes, optional), category (Breakfast | Lunch | Dinner | Dessert | Snack), imageUrl (optional, URL reference only).
- A recipe has 1 or more Sections (e.g., "For the sauce", "For the dough").
- Each Section has ingredients[] (may be empty — allows instruction-only sections like "Plating") and steps[] (may be empty — allows ingredient-list-only sections).
- Validation: a recipe must have at least one ingredient OR one step in total.

Ingredient model:
- Numeric ingredients: quantity as a fraction { numerator, denominator } (NOT floating point), unit (from predefined list), name (string), preparation (optional, e.g., "diced", "room temperature").
- Non-numeric ingredients: quantityText field ("to taste" | "a pinch" | "as needed"), name (string), preparation (optional). Non-numeric ingredients are never scaled and display with a "(not scaled)" badge.

Predefined units: cup, tbsp, tsp, fl oz, oz, lb, g, kg, mL, L, piece. No custom units in v1.

Fraction system:
- Allowed denominators: 2, 3, 4, 8. Always reduce to simplest form.
- Internal representation: { numerator: int, denominator: int }.
- Scaling: scaleFactor = desiredServings / baseServings. Multiply ingredient fraction by scaleFactor using fraction arithmetic. Convert result to nearest representable fraction (allowed denominators). If best-fit error > 0.05, show decimal with 1 digit instead. If result is within 0.02 of an integer, display as integer.
- Display using vulgar fraction characters: ½, ⅓, ⅔, ¼, ¾, ⅛, ⅜, ⅝, ⅞. Mixed numbers as "1 ½ cups".

Scaling rules for special cases:
- Unit "piece": always round UP to nearest whole number. Show note if rounded: "2 eggs (rounded from 1.5)". If scaled piece < 1, round to 1 and show: "1 egg (recipe calls for {fraction} — use beaten egg, measure approx)".
- Non-numeric (quantityText): display unchanged with "(not scaled)" badge.
- Very small results near zero: floor to minimum ⅛; below that show "(trace amount)".

Unit conversion (toggle button switches imperial ↔ metric):
- Conversion constants (kitchen-standard): 1 cup = 240 mL, 1 tbsp = 15 mL, 1 tsp = 5 mL, 1 fl oz = 30 mL, 1 oz = 28 g, 1 lb = 454 g, 1 kg = 1000 g, 1 L = 1000 mL.
- Rounding: mL to nearest 5 mL, g to nearest 1 g, kg to 0.01 kg.
- Display: "240 mL (1 cup)" — converted value with original in parentheses.
- Conversion happens AFTER scaling (scale first, convert second).
- "piece" and non-numeric ingredients are never converted.

Shopping list (generated from meal planner):
- Merge algorithm: merge only when normalized ingredient name matches EXACTLY (case-insensitive, trimmed whitespace). No semantic merging ("chicken breast" ≠ "chicken thigh" — separate lines).
- Merge only if units are convertible within the same dimension: volume ↔ volume (convert to mL, sum, then display), weight ↔ weight (convert to g, sum, then display).
- If units are different dimensions (cups of flour + grams of flour): keep as separate lines.
- Display thresholds: volume ≥ 1000 mL → show as L (1 decimal); weight ≥ 1000 g → show as kg (2 decimals).
- Items can be checked off. Manual freeform items can be added.

Meal planner:
- Weekly grid: Monday–Sunday × Breakfast / Lunch / Dinner.
- Week starts Monday. Keyed by week start date (YYYY-MM-DD in local time).
- "This week" computed from local time at page load.
- Assign recipes to slots via dropdown.
- "Generate Shopping List" button aggregates all ingredients from planned recipes.

Search: filter recipes by name OR by ingredient name. Case-insensitive substring match. Instant client-side.

Sample data: 5 recipes:
- Classic Pancakes (Breakfast): ½ cup milk, ¼ tsp salt — demonstrates fractions
- Pasta Bolognese (Dinner): 2 sections ("For the sauce" / "For the pasta") — demonstrates nesting
- Caesar Salad (Lunch): "salt to taste", "pepper to taste" — demonstrates non-scalable
- Chocolate Chip Cookies (Dessert): "2 eggs" — demonstrates piece rounding on 1.5× scaling
- Overnight Oats (Breakfast): 200g oats, 300 mL milk — demonstrates metric + conversion

Scope tiers:
- MVP (required): Recipe CRUD + sections/ingredients/steps + scaling with fraction display
- Core (recommended): + Unit conversion toggle + recipe search (name + ingredient)
- Stretch (optional): + Meal planner grid + shopping list aggregation + checkoff
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: What denominators are allowed for fraction display? Should 16 be included (for ¹⁄₁₆)?
2. Decision needed: When rounding pieces UP from scaling, what about scaling down — does ¼ egg round to 1 egg?
3. Decision needed: For "a pinch" / "to taste" items, show unchanged text only, or display a visual "(not scaled)" badge?
4. Decision needed: Unit conversion constants — 1 cup = 236.588 mL (exact) or 240 mL (kitchen standard)?
5. Decision needed: When merging shopping list ingredients, how strict is name matching — exact only, or fuzzy/stemmed?
6. Decision needed: If two recipes use different units for the same ingredient (cups of flour + grams of flour), convert and merge, or keep as separate lines?
7. Decision needed: Are duplicate recipe names allowed? If yes, how are they distinguished in the UI?
8. Decision needed: Can a section be completely empty (no ingredients AND no steps)? What is the minimum valid recipe?
9. Decision needed: Meal plan week boundary — Monday or Sunday? How does timezone or travel affect "this week"?
10. Decision needed: When scaling produces a non-representable fraction (e.g., 0.4 cups), show decimal "0.4" or approximate as "⅜ (approx)"?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/L-recipe-collection-answers.md`](_answers/L-recipe-collection-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] Nested data model (recipe → sections → ingredients + steps)
- [ ] Scaling rules with explicit fraction arithmetic
- [ ] Non-numeric ingredient handling
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
For the sample data: Pancakes should use ½ and ¼ fractions so scaling is visually obvious. Chocolate Chip Cookies should use "2 eggs" so scaling to 1.5× demonstrates piece-rounding (3 eggs, rounded). Caesar Salad must have at least 2 "to taste" items. Pasta Bolognese must have at least 2 sections with different ingredients in each.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec. Check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] All 10 deliberate ambiguities have documented resolutions
- [ ] Fraction rules are unambiguous (denominators, rounding, display)
- [ ] Non-numeric ingredient handling is explicit
- [ ] Shopping list merge rules are deterministic

---

### Plan

```
/speckit.plan Use vanilla HTML, CSS, and JavaScript. Store all data in localStorage. Implement a Fraction utility module ({ numerator, denominator } representation with add, multiply, simplify, and toDisplay methods) — this is the core algorithmic component and must be pure functions with no DOM dependencies. The scaling engine is a pure function: (recipe, targetServings) → scaledRecipe. Unit conversion uses a lookup table of conversion constants. No build tools or frameworks.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Architecture with fraction module design |
| `data-model.md` | Recipe, section, ingredient, shopping list models |
| `research.md` | Fraction arithmetic, vulgar fraction Unicode characters, conversion constants |
| `quickstart.md` | Validation scenarios for scaling edge cases |

**Validate the plan:**

```
Review the implementation plan and check: (1) Is the fraction module a pure utility with no DOM dependencies? (2) Is scaling a pure function that takes a recipe and target servings and returns a new scaled recipe? (3) Are conversion constants explicitly defined with specific values? (4) Is the shopping list merge algorithm deterministic and documented?
```

**Checkpoint:**
- [ ] Fraction utility is isolated pure logic
- [ ] Scaling is a pure function
- [ ] Conversion constants are explicit (240 mL/cup, 15 mL/tbsp, etc.)
- [ ] No unnecessary dependencies

---

### Tasks

```
/speckit.tasks
```

**What to observe in `tasks.md`:**
- Fraction utility module is one of the FIRST tasks (it's the algorithmic foundation)
- Scaling engine task depends on fraction module
- UI tasks come AFTER data model and algorithms
- MVP / Core / Stretch ordering is respected
- Shopping list aggregation comes last (Stretch tier)

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Especially useful for this scenario — verify every scaling rule and edge case in the spec has a corresponding test case in the task breakdown.

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- Fractions stored as `{ numerator, denominator }`, NOT as floats
- Scaling uses fraction arithmetic (multiply), not `parseFloat` → `*` → `toFixed`
- Non-numeric ingredients display unchanged with "(not scaled)" badge
- Piece items round UP to whole number with a note when rounded
- Conversion constants match the spec values (240 mL per cup, not 236.588)
- Shopping list merges by exact name match + compatible dimension only
- No features outside the specified scope tier

---

## Extension Activities

### Add a Feature: Nutritional Estimates

Add nutritional data using the full SDD workflow:

```
/speckit.specify Add nutritional estimates to RecipeBox. Each ingredient can optionally have calories, protein (g), carbs (g), and fat (g) per unit quantity. The recipe detail view shows per-serving totals that scale with serving size. Display as: "Estimated per serving: 450 cal | 25g protein | 55g carbs | 15g fat". Values are estimates — show a disclaimer: "Nutritional values are approximate."
```

Then continue through `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test: Recipe Import from URL

What if we need to parse recipes from web pages? This challenges the "local-only, user-entered data" constitution assumption:

```
/speckit.specify Add recipe import from URL to RecipeBox. The user pastes a URL and the app attempts to extract recipe data using schema.org/Recipe structured data (JSON-LD). If no structured data is found, show an error with a message to add the recipe manually. Imported recipes enter a "Review" state where the user can edit all fields before saving.
```

Re-run `/speckit.clarify` to discover new ambiguities: What if the schema data is malformed? What about sites that require JavaScript rendering? How do you map external ingredient formats to your fraction model? This demonstrates how external data sources cascade complexity through the spec.
