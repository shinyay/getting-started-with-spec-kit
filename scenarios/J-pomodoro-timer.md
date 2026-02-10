# Scenario J: Pomodoro Timer + Task Board

| | |
|---|---|
| **Level** | ⭐ Beginner |
| **Duration** | ~90 min |
| **Key SDD themes** | State machine specification, time-based logic, persistence |
| **Why it tests SDD** | Timer behavior has hidden state transitions that must be explicitly specified — without a state machine spec, the AI will confidently make wrong assumptions about every transition |
| **Best for** | Developers learning that "simple" features need precise behavioral specs |

---

## The Concept

You are building a Pomodoro timer — the classic productivity technique of 25-minute focus sessions followed by short breaks. Everyone thinks they can "just code a timer." Then they discover:

- Timers have **states** (idle, focus, break, paused)
- States have **transitions** with rules (can you pause a break? does skip work during focus?)
- Transitions have **persistence implications** (what if the tab closes mid-session?)
- Time logic has **platform traps** (`setInterval` drifts; background tabs throttle timers)

This scenario teaches that **behavioral correctness requires a state machine spec**. Without one, the AI will assume answers to questions you never asked — and many of those assumptions will be wrong.

This is the same skill that appears at higher difficulty in:
- Scenario D (⭐⭐⭐): Subscription billing has 8+ state transitions where ambiguity = real money lost
- Scenario E (⭐⭐⭐⭐): Collaborative whiteboard has per-object states with concurrent updates

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a personal productivity timer application. Prioritize predictable behavior (no surprising state transitions), data persistence (never lose task or session data), accessibility (screen reader announces timer state), simplicity (no frameworks, no build tools, localStorage only), and visual clarity (current state is always obvious at a glance). The constitution should be short — proportional to the project's low risk profile.
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Predictable behavior / no surprising state transitions
- [ ] Data persistence across browser sessions
- [ ] Accessibility requirements
- [ ] Simplicity constraints (no frameworks)
- [ ] Visual clarity principle

---

### Specification

```
/speckit.specify Build a Pomodoro Timer with Task Board — a personal productivity web app.

Timer behavior:
- States: Idle, Focus, Short Break, Long Break, Paused.
- Paused state remembers which state was paused (focus or break) so Resume returns to the correct state.
- Default durations: Focus = 25 min, Short Break = 5 min, Long Break = 15 min, Long Break every 4 focus sessions. All configurable in settings (Focus: 1–60 min, Short Break: 1–30 min, Long Break: 1–60 min, Cycle length: 2–8).
- Controls: Start, Pause, Resume, Skip, Cancel.
- Timer display: large countdown (MM:SS), circular progress ring, current state label.
- Breaks begin automatically after focus completes. Next focus does NOT auto-start after breaks — user must click Start.

Timer implementation:
- Use wall-clock comparison (Date.now() vs stored endTime), NOT setInterval tick counting.
- Persist timer state to localStorage on every transition: { state, endTime, pausedRemainingMs, pausedFrom, cycleCount }.
- On page load: if endTime is in the past, repeatedly apply Complete transitions until caught up (computing each next endTime from the previous endTime, not from "now"). This prevents stale states after extended absence.
- Timer runtime state is always prioritized over history in storage; if quota is near, prune history first so timer state can still be written.

Task board:
- Add task (text input + Enter), mark complete (checkbox), delete (× button), reorder (up/down arrows).
- When starting a Focus session, optionally link a task from a dropdown.

Statistics:
- Each completed focus session stores localDateCompleted as YYYY-MM-DD in local time at completion. This date never changes even if timezone changes later.
- Display: today's completed pomodoros, total focus time today, current streak (consecutive days with ≥1 completed focus), weekly bar chart (last 7 days).
- History retention: keep detailed records for 90 days; older data stored as daily aggregates only ({ date, count, totalMinutes }).
- If localStorage write fails: show "Storage full" banner and stop recording history; timer continues operating.

Notifications:
- Only guaranteed while app is open in a browser tab. No Service Worker or background alarms.
- Tier 1: Browser Notification API (if permission granted). Tier 2: Audio chime (HTML5 Audio). Tier 3: Visual flash (border pulse + state change).
- If Notification permission denied: fall back silently, no re-prompt.

Keyboard shortcuts:
- Space = Start/Pause/Resume (context-dependent), S = Skip (breaks only), Esc = Cancel, N = New task.
- All shortcuts DISABLED when focus is inside any text input, settings field, or editable element.

Settings changes apply to the NEXT session, not mid-timer.

Sample data:
- 3 pre-loaded tasks: "Write project proposal", "Review pull requests", "Update documentation"
- 1 completed pomodoro session from "today" linked to first task
- Statistics showing 1 completed pomodoro, streak of 1 day

Scope tiers:
- MVP (required): Timer states + controls + wall-clock persistence + basic display
- Core (recommended): + Task list CRUD + session-task linking + session history list
- Stretch (optional): + Weekly bar chart + streak logic + Notification API + keyboard shortcuts
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: Can you pause during breaks, or only during focus sessions?
2. Decision needed: Is "Skip" allowed during a focus session, or only during breaks? If during focus, does it count as a completed session?
3. Decision needed: Does "Cancel" discard the current session entirely, or record it as "abandoned" in history?
4. Decision needed: Can tasks be added/edited/completed while a pomodoro is running?
5. Decision needed: Can completed pomodoro history records be manually deleted by the user?
6. Decision needed: How is the cycle counter affected by Cancel — stay at current value or reset?
7. Decision needed: When the cycle counter is at 3/4 and the user skips the break, does the next focus count toward the same cycle or start a new one?
8. Decision needed: If the app is reopened after a very long absence and the catch-up loop processes Focus → Break → Idle, should the completed focus be recorded in history?
9. Decision needed: What happens if the user rapidly clicks Start multiple times — is there protection against duplicate timers?
10. Decision needed: If a break is skipped, is it recorded in history as "skipped" or simply not recorded?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/J-pomodoro-answers.md`](_answers/J-pomodoro-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] State descriptions with transition rules
- [ ] `[NEEDS CLARIFICATION]` markers for the ambiguities above
- [ ] Acceptance criteria that reference specific state transitions
- [ ] Timer persistence and recovery behavior
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify
```

Review the questions surfaced by Spec Kit. Use the deliberate ambiguity list above as a checklist — did the AI catch all 10? If not, add the missed ones manually.

**Manual refinement** — add details the AI missed:

```
For the sample data: ensure the completed pomodoro shows in the statistics (1 completed, streak of 1 day). Pre-loaded tasks should have varied states — first task linked to the completed pomodoro, second and third in "to-do" state.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] All 10 deliberate ambiguities have documented resolutions
- [ ] State transition rules are unambiguous
- [ ] Timer recovery behavior (catch-up loop) is explicitly defined

---

### Plan

```
/speckit.plan Use vanilla HTML, CSS, and JavaScript with no build tools or frameworks. Store all data in localStorage. The app should have a single index.html with linked CSS and JS files. Timer must use wall-clock comparison (Date.now() vs stored endTime). State machine should be implemented as an explicit state object with transition functions — no ad-hoc if/else chains.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Architecture with state machine design |
| `data-model.md` | State object, task model, session history |
| `research.md` | Timer accuracy (setInterval vs wall-clock), Notification API |
| `quickstart.md` | Key validation scenarios |

**Validate the plan:**

```
Review the implementation plan and check: (1) Is the state machine implemented as explicit transitions, not scattered if/else? (2) Does the timer use wall-clock comparison, not tick counting? (3) Is localStorage persistence on every state transition, not just on tab close? (4) Are keyboard shortcuts disabled inside input fields?
```

**Checkpoint:**
- [ ] Timer uses wall-clock, not `setInterval` for time tracking
- [ ] State machine is explicit (transition table or state/event handler)
- [ ] Persistence happens on every transition
- [ ] No unnecessary dependencies

---

### Tasks

```
/speckit.tasks
```

**What to observe in `tasks.md`:**
- State machine logic tasks come before UI tasks
- Timer persistence and recovery is an early task (not bolted on later)
- Wall-clock timekeeping is specified, not `setInterval`
- MVP / Core / Stretch tiers are respected in task ordering
- Notification fallback chain is a single task, not scattered

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Run `/speckit.analyze` after tasks to check cross-artifact consistency. It validates that every spec requirement has a corresponding task, and every task traces back to the spec. Optional but especially valuable for beginners learning to trust the SDD process.

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- The AI follows the task order from `tasks.md`
- State transitions are implemented as an explicit table/map, not ad-hoc conditionals
- `Date.now()` is used for time tracking, not `setInterval` ticks
- Timer state is persisted to localStorage on every transition
- Reopen catch-up loop processes multiple transitions if needed
- Keyboard shortcuts check `document.activeElement` before firing
- No features outside the specified scope tier

---

## Extension Activities

### Add a Feature: Focus Mode

Add a "Focus Mode" using the full SDD workflow:

```
/speckit.specify Add a "Focus Mode" to the Pomodoro Timer. When enabled, Focus Mode hides the task list and shows only the timer display and current linked task name. Focus Mode activates automatically when a focus session starts (if enabled in settings) and deactivates when the session ends. The user can also toggle it manually. The setting persists across sessions.
```

Then continue through `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Rebuild with Web Workers

Same spec, different plan — demonstrates SDD's tech-independence:

```
/speckit.plan Rebuild the Pomodoro Timer using a Web Worker for the timer logic. The main thread handles UI only. The Web Worker tracks time and sends messages to the main thread for display updates and state transitions. This ensures the timer runs accurately even when the browser tab is in the background.
```
