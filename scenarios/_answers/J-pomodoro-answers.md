# Scenario J: Pomodoro Timer — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Transition Table (Expected Output)

A well-run SDD process should produce a state transition table similar to this:

| From | Event | Guard | Action | To |
|---|---|---|---|---|
| Idle | Start | — | init focus endTime; record startTime | Focus |
| Focus | Tick | remainingMs > 0 | update display | Focus |
| Focus | Complete | remainingMs ≤ 0 | record session; increment cycle; notify | ShortBreak (cycle < 4) or LongBreak (cycle = 4) |
| Focus | Pause | — | store remainingMs + pausedFrom="focus" | Paused |
| Focus | Cancel | — | discard (not recorded); cycle unchanged | Idle |
| ShortBreak | Tick | remainingMs > 0 | update display | ShortBreak |
| ShortBreak | Complete | remainingMs ≤ 0 | notify | Idle |
| ShortBreak | Skip | — | — | Idle |
| ShortBreak | Pause | — | store remainingMs + pausedFrom="shortBreak" | Paused |
| LongBreak | Tick | remainingMs > 0 | update display | LongBreak |
| LongBreak | Complete | remainingMs ≤ 0 | reset cycle to 0; notify | Idle |
| LongBreak | Skip | — | reset cycle to 0 | Idle |
| LongBreak | Pause | — | store remainingMs + pausedFrom="longBreak" | Paused |
| Paused | Resume | — | restore remainingMs; recompute endTime | {pausedFrom} |
| Paused | Skip | pausedFrom is break | skip the paused-from period | Idle |
| Paused | Cancel | — | discard session | Idle |

Key decisions embedded in this table:
- **Breaks auto-start** after focus completes (Focus → Complete → ShortBreak/LongBreak)
- **Focus does NOT auto-start** after breaks (Break → Complete → Idle)
- **Skip is allowed during breaks and paused-from-break**, but NOT during focus
- **Cancel does NOT record** the session in history
- **Cycle counter** increments only on focus Complete; resets on long break Complete/Skip

## Catch-Up Loop Rule

On page load, if `endTime` is in the past:
1. Apply the `Complete` transition
2. Compute the next state's `endTime` from the **previous `endTime`** (not from "now")
3. If the new `endTime` is still in the past, repeat
4. Continue until the current state is `Idle` or the `endTime` is in the future

Example: Focus ended at 10:00, break should end at 10:05. User reopens at 10:20. The loop processes Focus → Complete → ShortBreak (endTime 10:05) → Complete → Idle. Final state: Idle. The completed focus IS recorded in history.

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Pause during breaks? | Yes — pausing is allowed in any running state | Restricting pause to focus only is surprising UX |
| 2 | Skip during focus? | No — use Pause + Cancel instead | Prevents accidental loss of focus progress |
| 3 | Cancel records session? | No — Cancel discards entirely | Clean semantics: only Complete records |
| 4 | Task editing during focus? | Yes — tasks are independent of timer state | Restricting adds UX friction without benefit |
| 5 | Delete history records? | No manual deletion; auto-pruning at 90 days only | Prevents stat manipulation; simpler implementation |
| 6 | Cancel affects cycle counter? | No — counter stays at current value | Only Complete increments the counter |
| 7 | Skip break + cycle counter? | Counter is unchanged; next focus still counts toward current cycle | Skipping a break doesn't "earn" a long break faster |
| 8 | Catch-up records history? | Yes — if focus Complete fires during catch-up, record it | Wall-clock recovery should match real-time behavior |
| 9 | Rapid double-click? | Start only valid from Idle; second click is no-op | Transition table enforces: Start has no effect in Focus state |
| 10 | Skipped break in history? | Not recorded — only completed focus sessions are entries | Simplifies history model |

## Storage Priority Rule

Timer runtime state (`{ state, endTime, pausedRemainingMs, pausedFrom, cycleCount }`) is always prioritized over history. If localStorage quota is reached:
1. Prune history records older than 90 days (convert to aggregates)
2. If still full, prune aggregate records oldest-first
3. Show "Storage full" banner
4. Timer state can always be written

## Facilitator Notes

- **After Constitution**: "This constitution is 5 principles. Scenario D (billing) has 12. A constitution should match the project's risk profile."
- **After Specify**: "Did the generated spec produce a transition table, or just prose? If prose only, does it cover all state combinations? The transition table is what makes the spec truly unambiguous."
- **After Clarify**: "The pause/resume question seems trivial, but imagine the AI assumed 'reset' instead of 'resume.' That's a production bug a spec prevents."
- **After Plan**: "Check: does the plan use `setInterval` or wall-clock? If `setInterval`, ask: what happens after 25 min of `setInterval(1000)` drift?"
