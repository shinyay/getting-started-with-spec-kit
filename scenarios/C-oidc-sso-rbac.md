# Scenario C: Brownfield OIDC SSO + Role-Based Access Control

| | |
|---|---|
| **Level** | ⭐⭐⭐ Intermediate–Advanced |
| **Duration** | ~120 min |
| **Key SDD themes** | Brownfield constraints, security/auth, backward compatibility, multi-tenancy |
| **Why it tests SDD** | Security + backward compatibility + multi-tenant isolation cannot be vibe-coded safely |
| **Best for** | Developers working on enterprise SaaS; anyone who wants to see SDD in a brownfield context |

---

## The Concept

You are adding OIDC Single Sign-On and role-based access control to an **existing multi-tenant SaaS application** that currently uses email/password authentication. Tenants can opt-in to SSO, and access is controlled by roles. Existing password login must keep working.

This scenario stress-tests SDD because:
- **Brownfield constraints** force the spec to address backward compatibility and migration paths
- **Security is the domain where ambiguity = vulnerability** — vague specs lead to auth bypass
- **Multi-tenancy** adds a tenant isolation dimension that must be specified explicitly
- **OIDC is standards-based** — the spec must handle real protocol edge cases (clock skew, expired secrets, missing claims)
- **Incremental rollout** means the plan must handle partial deployment states where some tenants have SSO and others don't

This is the same skill that appears at higher difficulty in:
- Scenario Q (⭐⭐⭐⭐): Capability-based permissions for a plugin runtime where third-party code runs inside your security boundary
- Scenario R (⭐⭐⭐⭐): Targeting rules and audience segmentation function as fine-grained access control for experimentation

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create a constitution for adding OIDC SSO and RBAC to an existing SaaS codebase.

Non-negotiables:
- Backward compatibility: existing password login must keep working until explicitly deprecated.
- Security first: follow least privilege, secure defaults, and protect against auth bypass.
- Tenant isolation is a security boundary: a user in Tenant A must never access Tenant B's data, even through OIDC misconfiguration, role bypass, or identity-linking bugs.
- Fail closed: if the auth system cannot determine a user's identity or permissions, deny access. Never fail open.
- Secrets management: OIDC client secrets, tokens, and credentials must never appear in logs, error messages, API responses, or client-side code. Use encrypted storage.
- Standards adherence: OIDC implementation must follow the OpenID Connect Core specification; do not invent custom auth flows.
- Auditability: security-sensitive actions must be audit logged (role changes, SSO config changes, login failures) without leaking secrets.
- Incremental rollout: feature flags + staged rollout; do not force all tenants at once.
- No breaking DB migrations without a rollback strategy.
- Testing: add automated tests for auth flows, role enforcement, and tenant isolation.
- Documentation: admin-facing docs for enabling SSO and troubleshooting login issues.
```

**Checkpoint** — verify the generated constitution includes:
- [ ] Backward compatibility principle
- [ ] Security-first / fail-closed stance
- [ ] Tenant isolation as a security boundary
- [ ] Secrets management rules
- [ ] Audit logging requirements
- [ ] Incremental rollout strategy
- [ ] Migration rollback requirement

---

### Specification

```
/speckit.specify Add OIDC Single Sign-On (SSO) and role-based access control (RBAC) to our existing multi-tenant SaaS app.

Goals:
- Tenants can enable OIDC SSO for their organization.
- Users can log in via SSO, and access is controlled by roles.
- Reduce support load from password resets and improve enterprise readiness.

Users:
- Tenant Admin: configures SSO, manages roles within their tenant.
- Standard User: logs in and uses the app.
- Support/Admin (internal): can troubleshoot safely without seeing sensitive data.

Requirements:

SSO:
- Tenant Admin can enable OIDC SSO by entering issuer URL / client ID / client secret and selecting required claims.
- Login page supports both "Email + Password" and "Continue with SSO" (tenant-aware).
- Support multiple tenants; tenant selection is determined by email domain or a tenant picker.
- A tenant may have multiple email domains (e.g., company.com and company.co.uk → same tenant).
- SSO enforcement mode: Tenant Admin can optionally force SSO-only login, disabling password login for their tenant's users.
- Handle common failure modes: wrong issuer, expired secret, missing claims, clock skew, OIDC provider outage.

Identity linking / Just-In-Time (JIT) provisioning:
- When a user logs in via SSO for the first time, create a local account linked to the OIDC subject.
- If the SSO email matches an existing password-based user in the same tenant, prompt the user to link accounts (do not auto-link silently — require confirmation).
- If no match, create a new user with the tenant's configured default role.

Logout:
- Logging out of the app clears the local session.
- RP-initiated logout: redirect to the OIDC provider's end-session endpoint if supported.
- "Logout from all devices" invalidates all sessions for that user.

Token lifecycle:
- Access tokens have a configurable expiry (default 1 hour).
- Refresh tokens are used to extend sessions silently.
- If the OIDC provider revokes access (e.g., user removed from IdP), the next token refresh fails and the user is logged out.

RBAC:
- Roles: Viewer, Editor, Admin (minimum).
- Admin can assign roles to users within their tenant.
- Roles affect access to specific routes/actions (define a few concrete examples: e.g., Viewer cannot create/delete resources; Editor cannot manage users; Admin has full access within their tenant).
- Default role for new SSO users is configurable per tenant.
- Role changes take effect immediately (no cached stale permissions).

Acceptance criteria:
- A tenant can enable SSO without disrupting existing users.
- A user logging in through SSO is created/linked correctly and placed in the correct tenant.
- Access control is enforced consistently across UI and API (no "hidden button" security).
- Audit logs exist for: enabling/disabling SSO, role changes, and login failures (without leaking secrets).
- Existing password login continues to work for tenants that have not enabled SSO.

Edge cases to explicitly cover:
- OIDC provider is down: SSO users cannot log in; show a clear error. If password login is not disabled, offer it as fallback.
- Tenant Admin misconfigures SSO (wrong issuer URL): no users are locked out; previous working config is preserved until new config is validated.
- User exists in multiple tenants via different email domains.
- Clock skew beyond tolerance between app server and OIDC provider.
- Tenant Admin accidentally disables SSO after users are already SSO-only.

Non-goals (explicitly out of scope):
- SAML support (only OIDC for this iteration).
- SCIM provisioning (later iteration).
- Social login (Google, GitHub, etc.) — only enterprise OIDC IdPs.

Scope tiers:
- MVP (required): Tenant Admin configures OIDC (issuer URL + client ID + secret) + SSO login works alongside existing password login + basic role assignment (Viewer, Editor, Admin) per tenant
- Core (recommended): + JIT provisioning for new SSO users + account linking confirmation flow + RBAC enforcement middleware on all routes + audit logging for security-sensitive actions
- Stretch (optional): + SSO enforcement mode (disable password per tenant) + dual OIDC secret rotation (old + new overlap) + Support impersonation with audit trail + login rate limiting + per-tenant feature flags for staged rollout
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: What happens to a user's active sessions when their role changes — immediate invalidation, grace period, or re-check on next request?
2. Decision needed: Should Tenant Admin be able to see login failure details (e.g., which claim was missing), or is that restricted to Support?
3. Decision needed: What is the audit log retention policy — how long in hot storage vs. cold archive, and is it configurable per tenant?
4. Decision needed: Can a Support/Admin impersonate a user for debugging? If so, how is that audited and is there a time limit?
5. Decision needed: How is the OIDC client secret rotated without downtime — dual active secrets during a rotation window?
6. Decision needed: What happens to existing password-only users when a Tenant Admin enables SSO enforcement mode — are they locked out, given a grace period, or force-linked?
7. Decision needed: Can a user belong to multiple tenants with different roles in each — and if so, how is the "current tenant" determined at login?
8. Decision needed: What is the idle session timeout, and is it configurable per tenant for compliance reasons?
9. Decision needed: Is there a "test connection" step to validate OIDC configuration before it goes live — preventing misconfiguration lockouts?
10. Decision needed: How quickly is an active session terminated when a user is deactivated in the OIDC provider — on next token refresh, or proactively?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/C-oidc-sso-rbac-answers.md`](_answers/C-oidc-sso-rbac-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] User stories with acceptance criteria
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguities above
- [ ] A review and acceptance checklist
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify Review the OIDC SSO + RBAC spec and ask me about every ambiguity, unstated assumption, and gap — especially around: session behavior on role change, admin visibility into login failures, audit log retention, support/admin impersonation, OIDC secret rotation, rate limiting on login, and any security edge cases you can identify.
```

Review the questions surfaced by Spec Kit. Use the deliberate ambiguity list above as a checklist — did the AI catch all 10? If not, add the missed ones manually.

**Manual refinement:**

```
For sample data: create 3 tenants — "Acme Corp" (SSO enabled, 2 domains), "Globex Inc" (password-only), and "Initech" (SSO enabled, enforcement mode on). Pre-load 5 users across these tenants with varied roles. Include one user who exists in both Acme Corp and Globex Inc via different email addresses.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] Clear user stories with testable acceptance criteria
- [ ] All edge cases have defined behavior
- [ ] Logout flow is fully specified (local session + OIDC provider + all-devices)
- [ ] JIT provisioning rules are explicit (new user vs. existing user linking)
- [ ] SSO enforcement mode behavior is documented (including accidental disable recovery)
- [ ] All 10 deliberate ambiguities have documented resolutions

---

### Plan

```
/speckit.plan Produce a technical plan to implement OIDC SSO + RBAC in the existing multi-tenant SaaS app.

Tech stack context (existing app):
- Backend: Node.js + Express, PostgreSQL database, Knex.js for migrations.
- Frontend: React SPA, communicating via REST API.
- Auth (current): email/password with bcrypt, express-session with connect-pg-simple, CSRF tokens.
- Deployment: Docker containers, CI/CD via GitHub Actions.

For OIDC, use the openid-client library (certified RP implementation). Do not build custom OIDC flows.

The plan must include:
- How to detect/select tenant at login (domain mapping vs tenant picker; pros/cons of each).
- Auth flow details: OIDC authorization code flow with PKCE, redirects, callback handling, session creation, CSRF protections.
- Session management: extend existing express-session; store OIDC tokens server-side; cookie security (httpOnly, secure, SameSite=Lax).
- User identity linking: how to map OIDC subject/email to existing users safely; the confirmation flow for linking existing password accounts.
- Secret storage: OIDC client secrets encrypted at rest in PostgreSQL; how secrets are redacted in logs/telemetry.
- Redirect URI and CORS security: strict redirect URI validation; no open redirects.
- RBAC enforcement strategy: shared authorization middleware (Express middleware), policy definitions, and how to avoid scattered permission checks. Include concrete route-level examples.
- Database changes: new tables/columns for OIDC config, user identity providers, roles, audit logs — with Knex migration + rollback strategy.
- Threat model: identify top 5 attack vectors (token theft, CSRF, tenant confusion, privilege escalation, open redirect) and how the plan mitigates each.
- Test strategy: unit tests for auth middleware, integration tests for OIDC flows (with mock IdP), e2e tests for login/logout, negative tests for role bypass, and tenant isolation tests.
- Rollout plan: feature flags (per-tenant SSO enablement), canary deployment, and rollback procedure.
- Operational playbook: what to check on login failures, what logs exist, what NOT to log, how to help a tenant who misconfigured SSO.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Implementation plan with phases and architecture |
| `data-model.md` | New tables: OIDC configs, identity providers, roles, audit logs |
| `research.md` | OIDC library evaluation, session management research |
| `contracts/` | API contracts for SSO config, login, role management |
| `quickstart.md` | Key validation scenarios |

**Validate the plan:**

```
Review the implementation plan and check: (1) Does the threat model cover the top 5 auth attack vectors? (2) Are there any security shortcuts that violate the constitution? (3) Is the migration strategy truly reversible? (4) Does the rollout plan allow tenant-by-tenant enablement?
```

**Checkpoint:**
- [ ] Tech stack matches the existing app (Node/Express, PostgreSQL, React)
- [ ] OIDC flow uses authorization code + PKCE (not implicit flow)
- [ ] Secrets are encrypted at rest and redacted in logs
- [ ] RBAC enforcement is centralized in middleware, not scattered
- [ ] Threat model exists with specific mitigations
- [ ] Migration includes rollback strategy
- [ ] Feature flag strategy enables per-tenant rollout

---

### Tasks

```
/speckit.tasks Generate a task list to implement the plan.

Constraints for tasks:
- Separate tasks for: data model/migrations, OIDC configuration UI, login flow (SSO + password coexistence), identity linking/JIT provisioning, logout flow, RBAC middleware, UI permission gating, audit logging, and tests.
- Include at least one "attack mindset" task: validate no role bypass via direct API calls, no tenant cross-contamination via OIDC misconfiguration.
- Include a regression task: run the existing test suite after each major change to ensure no breakage.
- Include a "canary tenant" task: deploy SSO to a single test tenant and validate the full flow before broader rollout.
- Include docs tasks: tenant admin guide for enabling SSO + support troubleshooting checklist.
- Each task should have a clear "done when" check.
```

**What to observe in `tasks.md`:**
- Tasks grouped by concern (data model → OIDC flow → RBAC → audit → tests → docs)
- Existing test suite regression checks appear after major changes
- "Attack mindset" task(s) validate security from an adversarial perspective
- Canary tenant deployment before production rollout
- Migration tasks have explicit rollback steps

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Run `/speckit.analyze` after tasks to check cross-artifact consistency. It validates that every spec requirement has a corresponding task, and every task traces back to the spec. Particularly valuable for security-sensitive systems where a missed auth check or tenant isolation gap can become a vulnerability.

---

### Implement

```
/speckit.implement Execute all tasks in order. After completing each group of related tasks, run the existing test suite to check for regressions before proceeding.
```

**What to watch for:**
- The AI follows the task order from `tasks.md`
- Database migrations are created with rollback support
- OIDC client secrets are never logged or exposed in API responses
- RBAC middleware is applied consistently, not ad-hoc per route
- Existing password login flow is not broken
- Feature flags gate SSO functionality per tenant

---

## Extension Activities

### Add a Feature: SCIM Provisioning

Extend the SSO integration with automated user provisioning:

```
/speckit.specify Add SCIM 2.0 provisioning support so that enterprise IdPs can automatically create, update, and deactivate users in our app. When a user is deactivated in the IdP, their account should be suspended (not deleted) in our app within 15 minutes. Include a SCIM API endpoint that the IdP calls, with bearer token authentication and rate limiting.
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test the Spec: Emergency SSO Bypass

Add a new requirement and see how it ripples through the plan:

```
A new requirement has emerged: if a tenant's OIDC provider has a prolonged outage (>1 hour), a Support/Admin must be able to temporarily enable "emergency password login" for that tenant's users, even if SSO enforcement was on. This bypass must be heavily audit-logged and auto-expire after 24 hours. Update the spec, plan, and tasks to handle this.
```

This demonstrates SDD's ability to handle security-critical requirement changes systematically rather than as panicked hotfixes.
