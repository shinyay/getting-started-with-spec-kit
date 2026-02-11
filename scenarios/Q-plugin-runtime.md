# Scenario Q: Plugin Runtime with Sandboxed Execution

| | |
|---|---|
| **Level** | ⭐⭐⭐⭐ Advanced |
| **Duration** | ~120 min |
| **Key SDD themes** | Public API contract stability, sandboxed execution, capability-based permissions, resource limits, lifecycle management |
| **Why it tests SDD** | "Just load and run the plugin" breaks on the first infinite loop, memory leak, or API change — the spec must define isolation guarantees, resource limits, and a compatibility contract that external developers can trust |
| **Best for** | Developers building extensible platforms; anyone who wants to understand why public API contracts require a fundamentally different spec mindset |

---

## The Concept

You are building a plugin system — third-party developers write small extensions that hook into your platform, transform data, or react to events. Users install plugins from a registry. Simple, right?

Except:
- A plugin enters an infinite loop. Does it hang your entire server? The spec must define execution timeouts and isolation.
- A plugin tries to read files from disk or make network calls. Should it be allowed? The spec must define a capability model.
- You release platform v2 with a changed API. Every installed plugin breaks. The spec must define a versioning contract that prevents this.
- A plugin crashes during execution. Does it take down other plugins? Does the user see an error? Does the platform retry? The spec must define failure isolation.

This scenario teaches that **your spec IS the product** — when external developers build against your API, the spec defines what they can rely on. Breaking the spec breaks THEIR code, not yours. And that **running untrusted code requires explicit security contracts** — what a plugin CAN access, what it MUST NOT access, and what happens when it misbehaves.

This is the same skill that appears at a simpler scale in:
- Scenario H (⭐⭐): CLI output contracts as a public interface
- Scenario I (⭐⭐⭐): API versioning and backward compatibility
- Scenario K (⭐): Whitelist-based security thinking (allowed vs not-allowed)

**Tech stack:** Node.js + Worker Threads (sandboxed execution) + Express + PostgreSQL

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create principles for a plugin runtime platform. Prioritize: the API contract is the product (external developers build against it — breaking changes break THEIR code), defense in depth (plugins are untrusted code; isolate execution, enforce resource limits, restrict capabilities), fail-closed security (if permission check fails or is ambiguous, deny access), graceful degradation (a crashing plugin must never take down the host or other plugins), deterministic execution (same input produces same output within resource limits; no hidden state between invocations unless explicitly allowed), auditability (every plugin execution, permission check, and failure is logged with enough context to investigate), and compatibility by contract (plugins declare their required apiVersion; the host refuses to load incompatible plugins rather than silently breaking).
```

**Checkpoint** — verify the generated constitution includes:
- [ ] API contract as product principle
- [ ] Defense in depth / untrusted code
- [ ] Fail-closed security model
- [ ] Plugin crash isolation
- [ ] Deterministic execution
- [ ] Audit logging
- [ ] Compatibility contract

---

### Specification

```
/speckit.specify Build PlugKit — a platform plugin runtime with sandboxed execution.

Plugin manifest (JSON):
- name: unique identifier (lowercase, alphanumeric + hyphens, 3-50 chars)
- version: semver (e.g., "1.2.3")
- apiVersion: integer (e.g., 1). The platform API version this plugin targets.
- permissions: array of capability strings the plugin requires
- entryPoint: path to main module (relative to plugin root)
- hooks: object mapping hook names to exported function names

Available hooks:
- onLoad(): called when plugin is enabled. Setup logic. No return value.
- onUnload(): called when plugin is disabled. Cleanup logic. No return value.
- onEvent(event): called when a platform event occurs. Receives event object. Returns void or { action, data } to modify platform behavior.
- transform(input): called to transform data. Receives input object. Must return transformed output object. Pure function (no side effects expected).

Capability-based permissions:
- "read:data" — read platform data via provided API
- "write:data" — create/update/delete platform data
- "log" — write to plugin log (always granted; cannot be denied)
- "storage:read" — read from plugin-scoped key-value storage
- "storage:write" — write to plugin-scoped key-value storage (max 1MB per plugin)
- "fetch:http" — make outbound HTTP requests (Stretch)

Permission model:
- Default deny: plugins can ONLY access APIs for their declared permissions.
- On install: user sees permission list and must approve.
- If a plugin calls an API without permission: call fails with PermissionDenied error; execution continues (not terminated); incident logged.
- Plugins cannot escalate permissions at runtime — must be declared in manifest.

Sandbox execution model:
- Each plugin runs in a Node.js Worker Thread (separate V8 isolate).
- Communication between host and plugin: structured message passing only (serializable JSON).
- Plugin has NO access to: filesystem, network (unless fetch:http granted), process env, other plugins' state, host internals.
- Resource limits per plugin execution:
  - CPU timeout: 200ms per hook invocation (configurable). Exceeding → execution terminated, error returned to host.
  - Memory: 64MB heap per worker (configurable). Exceeding → worker killed, plugin marked as "crashed."
  - Output size: max 1MB response per hook invocation.
- Worker lifecycle: one worker per enabled plugin. Worker is reused across invocations (for onLoad state). Worker is killed and recreated on crash.

Failure isolation:
- Plugin crash (unhandled exception): caught by host. Error logged with plugin name, hook, input (sanitized), and stack trace. Plugin marked as "error" state. Host continues normally.
- Plugin timeout: worker terminated. Plugin invocation returns timeout error to host. Plugin stays enabled (transient failure). After 5 consecutive timeouts → plugin auto-disabled.
- Plugin out-of-memory: worker killed. Plugin auto-disabled. Admin notified.
- Host never crashes due to plugin failure.

Plugin lifecycle:
- AVAILABLE → INSTALLED → ENABLED → DISABLED → UNINSTALLED
- Install: download plugin, validate manifest, check apiVersion compatibility, store in DB.
- Enable: spawn worker, call onLoad(), start receiving events.
- Disable: call onUnload(), terminate worker, stop receiving events.
- Uninstall: must be disabled first. Removes plugin storage. Cannot uninstall an enabled plugin.
- Upgrade: disable → uninstall old → install new → enable. Plugin storage preserved across upgrades of the same plugin name.

API versioning:
- Host declares supported apiVersions (e.g., [1]).
- Plugin declares required apiVersion (e.g., 1).
- Install-time check: if plugin's apiVersion is not in host's supported list → reject installation with clear error.
- Host guarantees: all APIs available in apiVersion N remain available and backward-compatible in apiVersion N. Breaking changes require apiVersion N+1.
- Deprecation: APIs can be deprecated (logged warning on use) but not removed within the same apiVersion.

Plugin-scoped storage:
- Key-value store scoped to plugin name.
- Keys: string (max 256 chars). Values: JSON (max 100KB per value).
- Total storage per plugin: max 1MB.
- Storage persists across enable/disable cycles and upgrades.
- Storage deleted on uninstall.

Threat model (v1):
- Defend against: infinite loops (timeout), memory exhaustion (heap limit), excessive output (size limit), unauthorized data access (capability check), noisy logging (rate limit on log API: 100 entries/min).
- Do NOT defend against: kernel-level VM escapes, timing side-channel attacks, Worker Thread sandbox bypasses. Document these as known limitations.

Data model:
- plugins: id, name (UNIQUE), version, apiVersion, permissions (JSON), status (available/installed/enabled/disabled/error), installedAt, enabledAt, errorCount, lastError
- plugin_storage: pluginName, key, value (JSON), updatedAt. PRIMARY KEY (pluginName, key).
- plugin_executions: id, pluginName, hook, status (success/error/timeout/oom), durationMs, inputSize, outputSize, error, createdAt
- plugin_audit: id, pluginName, action (install/enable/disable/uninstall/upgrade/permission_denied/crash), actor, details (JSON), createdAt

Observability:
- Every hook invocation logged with: plugin, hook, duration, status, input/output size.
- Permission denied events logged with: plugin, attempted API, declared permissions.
- Metrics: invocations/sec per plugin, error rate, p50/p95 duration, storage usage.
- Alert: plugin crash rate > 3/hour, any plugin auto-disabled.

Sample data:
- 2 installed plugins: "data-formatter" (transform hook, read:data + log permissions, healthy) and "event-logger" (onEvent hook, log + storage:write, healthy).
- 1 test plugin: "crash-test" (always throws, for failure isolation testing).
- Pre-populated plugin_storage for data-formatter (2 config keys).

Scope tiers:
- MVP (required): Plugin manifest validation + load plugin in Worker Thread + run transform hook + isolate failure (plugin throws → host continues) + permission check on API calls. No registry — plugins loaded from local folder.
- Core (recommended): + All hooks + timeout enforcement + memory limit + plugin lifecycle (install/enable/disable/uninstall) + scoped storage + audit log + apiVersion compatibility check.
- Stretch (optional): + Plugin marketplace/registry + hot reload + signed plugin verification + fetch:http capability + execution metrics dashboard + rate limiting on log API.
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: Sandbox mechanism — Worker Thread, subprocess, or vm module?
2. Decision needed: Do plugins get async APIs (Promises) or must hooks be synchronous/pure?
3. Decision needed: Permission model — default deny with explicit grant, or full access with restrictions?
4. Decision needed: Plugin distribution — local folder only, or install from a remote registry?
5. Decision needed: Can plugins have npm dependencies, or must they be self-contained?
6. Decision needed: Can plugins persist state between invocations (via storage API), or must they be stateless?
7. Decision needed: Plugin crash policy — disable immediately, or allow N consecutive failures before disabling?
8. Decision needed: Plugin logging — allowed? Rate-limited? How to prevent log spam or secret leakage?
9. Decision needed: API versioning — strict match only, or compatibility ranges (e.g., "works with apiVersion 1-3")?
10. Decision needed: Should the host support hot-reload (update plugin without disabling)?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/Q-plugin-runtime-answers.md`](_answers/Q-plugin-runtime-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] Plugin manifest schema with all fields
- [ ] Capability-based permission model
- [ ] Sandbox execution model with resource limits
- [ ] Failure isolation rules (crash, timeout, OOM)
- [ ] Plugin lifecycle state machine
- [ ] API versioning contract
- [ ] Threat model (v1)
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
For sample data: the "crash-test" plugin should throw different errors in different hooks — unhandled exception in transform, infinite loop in onEvent, and memory exhaustion in onLoad — to test all three failure isolation paths.
```

**Checkpoint:**
- [ ] All 10 decision questions resolved
- [ ] Resource limits are concrete (200ms timeout, 64MB memory, 1MB output)
- [ ] Permission denied behavior is explicit (fail call, continue execution, log)
- [ ] Auto-disable threshold is defined (5 consecutive timeouts, or 3 crashes)
- [ ] Storage limits and lifecycle are clear

---

### Plan

```
/speckit.plan Use Node.js with Express and PostgreSQL. Plugin sandbox uses Worker Threads (one worker per enabled plugin). Communication via structured message passing (postMessage). Host exposes a capability-checked API surface to plugins via message protocol. Resource limits enforced by worker timeout and V8 heap limit flag. Plugin storage in PostgreSQL (plugin_storage table). Audit log in PostgreSQL.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Plugin runtime architecture, worker lifecycle, message protocol |
| `data-model.md` | plugins, plugin_storage, plugin_executions, plugin_audit tables |
| `research.md` | Worker Threads vs vm vs subprocess, V8 isolate limits, message serialization |
| `quickstart.md` | Test scenarios for each failure mode |

**Validate the plan:**

```
Review the plan and check: (1) Is the message protocol between host and worker fully defined? (2) Does the capability check happen in the host (not in the worker)? (3) Is worker crash recovery automatic? (4) Is apiVersion compatibility checked at install time? (5) Are there test plugins for each failure mode?
```

**Checkpoint:**
- [ ] Worker lifecycle: spawn → onLoad → serve invocations → onUnload → terminate
- [ ] Capability check is in the host (worker never has direct API access)
- [ ] Crash recovery: worker killed → respawned → plugin retains state via storage
- [ ] Message protocol: invoke(hook, input) → result/error with timeout
- [ ] apiVersion compatibility is install-time rejection (not runtime error)

---

### Tasks

```
/speckit.tasks
```

**What to observe:**
- Plugin manifest validation is an early pure-function task
- Worker Thread spawning and message protocol are foundational tasks
- Capability check middleware comes before any hook execution
- Failure isolation tests (crash, timeout, OOM) are separate explicit tasks
- Plugin lifecycle (install → enable → disable → uninstall) is a complete flow
- MVP / Core / Stretch ordering respected

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Focus on the threat model — for every threat listed, is there a corresponding defense in the plan and a test in the tasks? Is there a test for "plugin calls API without permission"?

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- Worker Thread is created with `{ workerData }`, not `eval` or `vm.runInContext`
- Capability check happens in the HOST's message handler (plugin never has direct access)
- Timeout enforced by `setTimeout` + worker termination (not just a flag)
- Plugin crash does NOT propagate to host (try/catch + worker error event)
- apiVersion check happens at install time (rejected before any code loads)
- Audit log records every lifecycle event and permission denial
- Plugin storage is scoped (one plugin cannot read another's storage)

---

## Extension Activities

### Add a Feature: Plugin Marketplace

Plugins are distributed via a remote registry. Users browse, install, and rate plugins. The platform verifies plugin signatures (code hasn't been tampered with). How does the install flow change? What about plugin updates — can the marketplace push updates, or must users opt in?

```
/speckit.specify Add a plugin marketplace to PlugKit. Plugins are published to a central registry with metadata (name, description, author, version, permissions, download count, rating). Users browse and install from the marketplace. Published plugins must be signed by the author (Ed25519 signature of plugin bundle). The platform verifies the signature before installation. How do you handle: (1) a plugin update that adds new permissions? (2) a plugin removed from the marketplace but still installed by users? (3) a malicious plugin that passes signature verification but contains harmful code?
```

### Stress-test: Breaking API Change

You need to release apiVersion 2 with a breaking change to the transform hook signature. How do you migrate? What happens to existing plugins? How long do you support apiVersion 1?

```
/speckit.specify Release apiVersion 2 of the PlugKit platform API. The transform hook now receives { input, context } instead of just input. Existing apiVersion 1 plugins must continue working for 6 months (deprecation window). New plugins should target apiVersion 2. How do you: (1) run v1 and v2 plugins simultaneously? (2) warn v1 plugin authors about deprecation? (3) prevent new v1 plugins from being published after the deprecation date? (4) handle a plugin that declares apiVersion 1 but accidentally uses v2 APIs?
```

This bridges directly to Scenario I (API versioning migration).
