# Scenario R: Feature Flag & Experimentation — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Bucketing Algorithm Reference

```javascript
// Deterministic bucketing (pseudocode)
function getBucket(flagKey, userId) {
  const hash = murmurHash3(`${flagKey}:${userId}`);
  return hash % 10000; // 0-9999
}

function evaluateFlag(flag, userId) {
  // 1. Kill switch (highest priority)
  if (flag.killSwitchVariant !== null) return flag.killSwitchVariant;
  
  // 2. Targeting rules (priority order)
  for (const rule of flag.rules.sortBy('priority')) {
    if (matchesConditions(rule.conditions, userId, attributes)) {
      return rule.variant;
    }
  }
  
  // 3. Percentage rollout
  const bucket = getBucket(flag.key, userId);
  let cumulative = 0;
  for (const [variant, percentage] of flag.trafficSplit) {
    cumulative += percentage * 100; // percentage as 0-100 → buckets as 0-10000
    if (bucket < cumulative) return variant;
  }
  
  // 4. Default
  return flag.defaultVariant;
}
```

**Monotonic expansion:** When rollout goes from 25% to 50%, buckets 0-2499 stay in treatment. Buckets 2500-4999 are ADDED to treatment. No existing user moves OUT. This is critical for experiment integrity.

## SRM Detection Reference

```
Chi-squared goodness-of-fit test:
- Expected: 500 control, 500 treatment (50/50 split, 1000 exposures)
- Observed: 600 control, 400 treatment
- χ² = (600-500)²/500 + (400-500)²/500 = 20 + 20 = 40
- p-value for χ²=40 with df=1 → p ≈ 0 (far below 0.01 threshold)
- Result: SRM DETECTED — randomization is broken
```

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Assignment unit | userId (required); anonymous sessions are Stretch | userId is stable and cross-session; anonymous bucketing has identity problems |
| 2 | Sticky assignment lifetime | Stable for the duration of the experiment; reset only on experiment restart | Mid-experiment rebucketing corrupts results |
| 3 | Exposure logging frequency | Log on every evaluation (not just first) | Multiple exposures per user are normal (page reloads); dedup by evaluationId in analysis |
| 4 | Missing userId | Return default variant (control); log as "unidentified" | Random bucketing for missing IDs creates inconsistency across services |
| 5 | Kill switch semantics | Immediate override for ALL evaluations (cached and new) | Kill switch is an emergency mechanism; cached values must be invalidated |
| 6 | Mutual exclusion | Core feature (not Stretch); needed for any platform running >1 experiment | Without it, experiment contamination is silent and undetectable |
| 7 | Bot filtering | Configurable userId pattern exclusion list; bots are excluded from analysis, not from evaluation | Blocking evaluation might break bot-facing features; exclusion in analysis is cleaner |
| 8 | Event retention | Exposure events: 90 days. Conversion events: 90 days. Audit log: 1 year. | 90 days covers most experiment durations; audit log needs longer retention |
| 9 | Rebucketing on rollout change | Monotonic expansion only — users only ENTER treatment, never LEAVE | Moving users out of treatment mid-experiment corrupts statistical analysis |
| 10 | SRM action | Detection + warning in results; auto-pause is Stretch | Auto-pause needs confidence; v1 flags and lets humans decide |

## Data Quality Checklist

| Issue | Behavior |
|---|---|
| Duplicate exposure (same evaluationId) | Deduplicated on insert (UNIQUE constraint) |
| Late conversion (>7 days after experiment end) | Ignored in analysis |
| Missing conversion | Expected (most users don't convert); analysis handles this |
| Bot traffic | Excluded from analysis via configurable pattern list |
| SRM detected | Warning in results; experiment NOT auto-paused in v1 |

## Facilitator Notes

- **After Constitution**: "Ask: why is exposure logging 'not optional'? Because without it, you can't compute conversion RATES — you'd have conversions without knowing the denominator."
- **After Specify**: "The deterministic bucketing algorithm is the core contract. Write `hash('new-checkout:user123') % 10000 = 4821` on the board. Ask: what variant does this user see at 25% rollout? At 50%? (Answer: control at 25%, treatment at 50% — monotonic expansion.)"
- **After Clarify**: "SRM detection is the statistical 'aha' moment. Show the chi-squared calculation. Ask: what causes SRM? (Answers: buggy hash function, bot traffic, redirect before logging, client-side filtering.)"
- **After Plan**: "Check: is the hash function the SAME across all services? If the web app uses MurmurHash3 and the API uses FNV-1a, users get different variants — catastrophic."
- **Common mistake**: Teams use `Math.random()` instead of a deterministic hash. This means the same user gets different variants on page reload.
- **Common mistake**: Teams log exposure BEFORE evaluation returns. If evaluation fails, you've logged a phantom exposure.
