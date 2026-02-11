# Scenario Q: Plugin Runtime — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Plugin Lifecycle State Machine

```
AVAILABLE → INSTALLED → ENABLED ⇄ DISABLED → UNINSTALLED
                           ↓
                        ERROR (auto-disabled after threshold)
```

## Threat Model Summary

| Threat | Defense | Enforcement |
|---|---|---|
| Infinite loop | 200ms execution timeout | Worker thread timeout + termination |
| Memory exhaustion | 64MB V8 heap limit | `--max-old-space-size=64` on worker |
| Unauthorized data access | Capability check in host | Message handler validates permissions |
| Excessive output | 1MB response limit | Host checks response size |
| Log spam | 100 entries/min rate limit | Host-side rate limiter on log API |
| Cross-plugin data access | Scoped storage (pluginName key) | DB query scoped to plugin name |

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Sandbox mechanism | Worker Thread (separate V8 isolate) | Better isolation than vm; lighter than subprocess; real V8 heap limits |
| 2 | Async APIs | Hooks return Promises; host awaits with timeout | Plugins need async for storage API; timeout prevents hangs |
| 3 | Permission model | Default deny; explicit grant per manifest | Fail-closed security; users see permissions before install |
| 4 | Plugin distribution | Local folder for v1; registry is Stretch | Workshop simplicity; registry adds auth, signing, networking |
| 5 | Plugin dependencies | Self-contained bundles only; no npm install at runtime | Security: npm install can run arbitrary scripts; bundling is safer |
| 6 | Plugin state | Stateless between invocations; use storage API for persistence | Deterministic execution; state via storage is explicit and auditable |
| 7 | Crash policy | 5 consecutive failures → auto-disable; admin re-enable | Prevents runaway crash loops; threshold catches persistent bugs |
| 8 | Plugin logging | Allowed via "log" capability (always granted); rate-limited to 100/min; sanitized (no secrets in output) | Debugging needs logs; rate limit prevents abuse |
| 9 | API versioning | Strict match only (plugin declares exactly one apiVersion) | Simpler than ranges; compatibility ranges create testing combinatorics |
| 10 | Hot reload | Stretch feature; v1 requires disable → uninstall → install → enable | Hot reload needs careful state migration; too complex for v1 |

## Message Protocol (Host ↔ Worker)

```json
// Host → Worker: invoke hook
{ "type": "invoke", "hook": "transform", "input": { ... }, "requestId": "abc123" }

// Worker → Host: result
{ "type": "result", "requestId": "abc123", "output": { ... } }

// Worker → Host: error
{ "type": "error", "requestId": "abc123", "message": "...", "stack": "..." }

// Worker → Host: API call (capability-checked)
{ "type": "api", "requestId": "def456", "method": "read:data", "args": { ... } }

// Host → Worker: API response
{ "type": "api_response", "requestId": "def456", "result": { ... } }

// Host → Worker: API denied
{ "type": "api_denied", "requestId": "def456", "permission": "write:data" }
```

## Facilitator Notes

- **After Constitution**: "Ask: what does 'fail-closed' mean for a plugin system? If the permission check crashes, does the plugin get access or not? Answer: NO — fail-closed means deny on ambiguity."
- **After Specify**: "The threat model section is THE advanced lesson. Ask: what attacks does this NOT defend against? (Answer: V8 sandbox escapes.) Acknowledging limitations IS the spec."
- **After Clarify**: "The 'can plugins have dependencies' question reveals scope instincts. npm install at runtime is a supply-chain attack vector. Self-contained bundles are the safe choice."
- **After Plan**: "Check: does the capability check happen in the HOST or in the WORKER? If it's in the worker, a malicious plugin can bypass it. The host is the trust boundary."
- **Common mistake**: Teams put permission checks inside the plugin code (untrusted). Checks must be in the host message handler.
- **Common mistake**: Teams use `vm` module instead of Worker Threads. `vm` shares the same V8 isolate and is NOT a security boundary.
