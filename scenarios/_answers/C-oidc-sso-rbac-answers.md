# Scenario C — Facilitator Answer Key: Brownfield OIDC SSO + RBAC

> **This file is for facilitators only.** Do not distribute to participants before the workshop — it removes the learning value of the clarification phase.

---

## Expected Domain Output: OIDC Authorization Code Flow with PKCE

When `/speckit.specify` and `/speckit.clarify` produce the auth flow, the specification should define this sequence:

```
1. User clicks "Continue with SSO"
2. App determines tenant from email domain (or tenant picker)
3. App redirects to OIDC provider's /authorize endpoint:
   - response_type=code
   - scope=openid email profile
   - redirect_uri=https://app.example.com/auth/callback
   - state=<CSRF token>
   - code_challenge=<PKCE challenge>
   - code_challenge_method=S256
4. User authenticates at OIDC provider
5. Provider redirects to /auth/callback with ?code=...&state=...
6. App validates state (CSRF), exchanges code for tokens at /token endpoint
7. App validates ID token (signature, issuer, audience, expiry, nonce)
8. App performs JIT provisioning or account linking (see below)
9. App creates session (express-session, server-side token storage)
10. User is redirected to dashboard
```

### Tenant Isolation Invariants

These invariants must hold at ALL times — violation of any one is a security incident:

| Invariant | Enforcement Point |
|---|---|
| User in Tenant A cannot see Tenant B's data | Every database query includes `WHERE tenant_id = ?` |
| OIDC misconfiguration in Tenant A cannot affect Tenant B | OIDC config is per-tenant; validation errors are tenant-scoped |
| Role in Tenant A does not grant access in Tenant B | RBAC middleware checks `(user_id, tenant_id, role)` tuple |
| Audit logs for Tenant A are not visible to Tenant B | Audit log queries scoped by `tenant_id` |
| SSO enforcement in Tenant A does not disable password login in Tenant B | Enforcement flag is per-tenant; login page checks tenant config |

### JIT Provisioning Decision Tree

```
SSO login → email matches existing user in same tenant?
  ├─ YES → prompt "Link accounts?" (require explicit confirmation)
  │         ├─ Confirmed → link OIDC subject to existing user
  │         └─ Declined → create new user with OIDC identity
  └─ NO  → create new user with tenant's default role
```

---

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Active sessions on role change | Re-check permissions on every request (middleware). No cached permissions. No session invalidation needed. | Simplest correct approach; avoids race conditions from cache invalidation. |
| 2 | Admin visibility into login failures | Tenant Admin sees failure reason (e.g., "claim 'email' missing") but never tokens/secrets. Support sees same + request correlation IDs. | Balanced: admins can self-troubleshoot; secrets never exposed. |
| 3 | Audit log retention | 90 days hot (queryable), 2 years cold (archive). Configurable per tenant for compliance. | Meets common compliance requirements (SOC 2, GDPR). |
| 4 | Support impersonation | Explicit "impersonation mode" with audit log entry containing support agent's identity. Banner shown. Auto-expires after 1 hour. | Essential for debugging; time limit + audit trail prevent abuse. |
| 5 | OIDC secret rotation | Dual active secrets (old + new) during rotation window. Tenant Admin adds new before revoking old. Both validated during overlap. | Zero-downtime rotation; standard practice for OIDC client credentials. |
| 6 | SSO enforcement + existing password users | 30-day grace period. During grace: both SSO and password work. After grace: password disabled, forced SSO. Email warning at 14 days and 3 days. | Prevents lockouts; gives users time to link accounts. |
| 7 | Multi-tenant membership | Yes, a user can belong to multiple tenants with different roles. Tenant is selected at login (domain mapping or picker). Session is single-tenant. | Enterprise users often have accounts across subsidiaries. |
| 8 | Idle session timeout | Default 30 min, configurable per tenant (15 min–8 hours). Token refresh extends the session. | Balances security (short timeout) vs. usability (long timeout). Per-tenant for compliance. |
| 9 | OIDC config test connection | Yes — "Test Connection" button validates: (a) issuer URL is reachable, (b) client ID/secret are valid, (c) required claims are available. New config is not saved until test passes. | Prevents lockouts from misconfiguration. Critical safety mechanism. |
| 10 | Session termination on IdP deactivation | On next token refresh (typically within 1 hour). No proactive session kill. If immediate is needed, use "revoke all sessions" admin action. | Proactive kill requires webhook from IdP (not standard OIDC). Refresh-based is reliable and simple. |

---

## Facilitator Notes

### Constitution Phase
> Watch for "fail closed" principle. Many participants default to "fail open" for usability. In auth systems, ambiguity must deny access — a momentary lockout is recoverable; an auth bypass is a security incident.

### Specification Phase
> The scope tiers prevent participants from trying to build everything. MVP is "SSO login works alongside password" — that's already complex. Account linking, enforcement mode, and impersonation are Core/Stretch. If a participant puts "dual secret rotation" in MVP, they're over-scoping.

### Clarification Phase
> Questions 6 (SSO enforcement + existing users) and 9 (test connection) are the most commonly missed. Both are "what happens when the admin makes a mistake?" scenarios — participants focus on the happy path and forget that misconfiguration is the most common failure mode.

### Plan Phase
> The #1 mistake is building custom OIDC flows instead of using a certified library (openid-client). The plan should reference the library explicitly. Ask: "Are you implementing OIDC, or are you using a library that implements OIDC?" Only the second answer is correct.

### Implement Phase
> Watch for tenant isolation. The most dangerous bug is a missing `WHERE tenant_id = ?` in a single query. Every database access must be scoped. Suggest a repository pattern that enforces tenant scoping at the data access layer, not per-query.
