# Scenario B: Offline-first Field Inspection PWA

| | |
|---|---|
| **Level** | ⭐⭐⭐ Intermediate–Advanced |
| **Duration** | ~120 min |
| **Key SDD themes** | Offline-first, sync conflicts, media uploads, UX edge cases |
| **Why it tests SDD** | Offline + sync + conflict resolution cannot be vibe-coded |
| **Best for** | Developers who want a production-grade challenge |

---

## The Concept

Inspectors perform safety/compliance checks at physical sites — basements, industrial areas, places with poor connectivity. They need to complete checklists, attach photos, add notes, and submit when back online. Supervisors review the submissions remotely.

This scenario stress-tests SDD because:
- **Offline-first** forces extremely precise state management specs
- **Sync conflicts** are inherently ambiguous — the spec MUST address them
- **Media uploads** on flaky connections add async/failure-mode complexity
- **Two user roles** with different capabilities test permission modeling

This is the same skill that appears at higher difficulty in:
- Scenario E (⭐⭐⭐⭐): Conflict resolution escalates from offline sync to real-time collaborative editing with CRDTs
- Scenario F (⭐⭐⭐⭐): Data ingestion from devices scales to millions of events/sec with schema evolution and backpressure

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create a constitution for an offline-first field inspection PWA that will be used on-site with unstable connectivity.

Non-negotiables:
- Offline-first is mandatory: core flows must work with no network.
- Never lose user-entered data: drafts, photos, notes must be durable.
- Conflict handling must be explicit (no "last write wins" without user awareness).
- Progressive enhancement: core inspection completion must work on limited browsers; PWA-specific features (background sync, push notifications) are enhancements, not requirements.
- Graceful degradation for hardware APIs: if camera access or storage is unavailable, offer an alternative path or clear explanation — never a silent failure.
- Data lifecycle: define explicit retention and cleanup rules; submitted inspections may be purged from local storage after confirmed server receipt.
- Accessibility: keyboard navigation + screen-reader-friendly forms; clear error messages.
- Performance: fast launch; avoid heavy bundles; keep memory usage reasonable.
- Security/privacy: treat photos and notes as sensitive; no sensitive data in logs; sanitize analytics.
- Testing: require automated tests for sync/conflict logic and critical UI flows; include regression tests for bug fixes.
- Documentation: include a "How offline sync works" doc and a troubleshooting section for support.
```

**Checkpoint** — verify the generated `.specify/memory/constitution.md` includes:
- [ ] Code quality and simplicity guidelines
- [ ] Testing expectations
- [ ] Architectural constraints
- [ ] UI/UX and accessibility principles
- [ ] Offline-first stated as non-negotiable
- [ ] Data durability principle
- [ ] Conflict handling rules are explicit

---

### Specification

```
/speckit.specify Build an offline-first "Field Inspection" web app for inspectors performing safety/compliance checks at physical sites.

Context & goals:
- Inspectors work in basements/industrial areas with poor connectivity.
- They need to complete checklists, attach photos, add notes, and submit when back online.
- Reduce time-to-complete and reduce rework due to lost data.

Users:
- Inspector (primary): logs in with email/password; session persists offline once authenticated.
- Supervisor (reviews submitted inspections).

Core flows:
1) Inspector selects a site + inspection template (checklist) and starts an inspection.
2) App saves progress continuously (auto-save).
3) Inspector can attach multiple photos per checklist item, add notes, and mark pass/fail/NA.
4) Inspector can complete inspection offline and "Submit" later when online.
5) Supervisor can review submitted inspections, leave comments, and export a PDF summary.

Functional requirements:
- Inspection templates: grouped sections, required vs optional items. Templates are managed by admins and synced to devices; inspectors cannot modify templates.
- Draft state: list drafts, search by site, show last-edited time, resume draft.
- Attachments: capture from camera + upload from device; max 10 photos per checklist item; JPEG/PNG only, max 10 MB each; no video in v1. Show upload status; allow delete/replace.
- Sync:
  - Automatic background sync when connectivity returns.
  - Clear status UI (Offline / Syncing / Synced / Needs Attention).
  - If the same inspection draft was edited on two devices, show a conflict resolution UI.

Non-goals (explicitly out of scope):
- No real-time collaboration on the same draft.
- No complex permissions beyond Inspector vs Supervisor.
- No video capture.

Acceptance criteria (examples):
- If the app crashes or the tab closes, reopening restores the latest draft state.
- Submitting offline queues the submission; when online, submission completes without user re-entering data.
- Conflict resolution shows the differing fields and lets the user choose per-field or per-section.
- Supervisor export includes checklist results, notes, and photo thumbnails/links.

Edge cases to explicitly cover:
- Large photo uploads on slow connections, retries, and partial failures.
- Duplicate submissions (user taps Submit multiple times).
- Time drift between devices.
- Template updates while an inspection is in progress.
- Storage full on device while inspection is in progress.

Scope tiers:
- MVP (required): Inspector completes offline checklist + auto-save to IndexedDB + basic sync on reconnect + inspector login with offline session persistence
- Core (recommended): + Photo attachments with upload queue + conflict resolution UI (per-field choice) + supervisor review dashboard + PDF export
- Stretch (optional): + Background sync via service worker + push notifications for submission status + template version management with migration banner + storage quota management with progressive warnings
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: What is the completed inspection lifecycle after supervisor approval — archive, delete, or retain with a defined retention period?
2. Decision needed: How is the supervisor notified of new submissions — push notification, email digest, dashboard badge, or a combination?
3. Decision needed: What happens to local data after confirmed server receipt — immediate purge, deferred cleanup, or manual user action?
4. Decision needed: Can a supervisor reject an inspection and send it back for rework? If so, does it reopen as a draft on the inspector's device?
5. Decision needed: How are template versions managed when inspectors have cached old versions — force update, allow completion with old version, or show a migration banner?
6. Decision needed: What is the maximum number of concurrent in-progress inspections per inspector — unlimited, or capped to prevent storage exhaustion?
7. Decision needed: How should photo metadata (GPS coordinates, EXIF timestamps) be handled — strip for privacy, keep for compliance, or make configurable per template?
8. Decision needed: What happens if a supervisor opens an inspection for review while the inspector is still editing it offline — read-only snapshot, or block review until submission finalizes?
9. Decision needed: Can inspectors access and reference their own past completed inspections while on-site, and if so, are those cached offline?
10. Decision needed: How does the sync queue prioritize when multiple inspections are queued for upload — FIFO, by submission urgency, or by payload size (smallest first)?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/B-field-inspection-pwa-answers.md`](_answers/B-field-inspection-pwa-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] User stories with acceptance criteria
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguities above
- [ ] A review and acceptance checklist
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify Review the Field Inspection spec and ask me about every ambiguity, unstated assumption, and gap — especially around: authentication flow, completed inspection lifecycle, supervisor notification mechanism, data retention policy, template versioning, and the specific behavior for each listed edge case.
```

Review the questions surfaced by Spec Kit. Use the deliberate ambiguity list above as a checklist — did the AI catch all 10? If not, add the missed ones manually.

**Manual refinement** — add details the AI missed:

```
For sample data: create 2 inspection templates — "Fire Safety Quarterly" (3 sections, 12 items) and "Electrical Compliance" (2 sections, 8 items). Pre-load 1 completed inspection and 1 in-draft state. Include at least one item with multiple photo attachments and one with a detailed note.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] Clear user stories with testable acceptance criteria
- [ ] Sample data requirements defined
- [ ] Edge cases explicitly addressed
- [ ] Sync behavior fully specified (online → offline → online transitions)
- [ ] Conflict resolution UX described (per-field or per-section choice)
- [ ] Every listed edge case has a defined behavior
- [ ] All 10 deliberate ambiguities have documented resolutions

---

### Plan

```
/speckit.plan Create a technical plan for the Field Inspection PWA, adhering to the constitution.

Tech stack:
- Frontend: TypeScript + React, built with Vite, Workbox for service worker management.
- Local storage: IndexedDB via Dexie.js for structured data; Cache API for static assets.
- Backend: Node.js + Fastify, PostgreSQL for persistent storage.
- File storage: S3-compatible object store for photo uploads.
- Deployment: containerized (Docker), deployed via CI/CD.

The plan must include:
- Architecture overview (frontend, backend, storage, sync strategy).
- PWA strategy: service worker lifecycle, cache-first vs network-first decisions per resource type, app install prompt, update notification UX.
- Offline storage approach: what data goes where, durability guarantees, IndexedDB schema versioning/migration.
- Sync protocol: identifiers, idempotency, retries, conflict detection strategy, and conflict resolution UX design.
- Data model: inspection templates, inspections, checklist items, attachments, submission status, supervisor review comments.
- API design: endpoints/contracts for templates, drafts, submissions, exports, and attachment upload (including multipart + resumable upload for large photos).
- Attachment strategy: client-side compression/thumbnail generation before storage in IndexedDB, upload queue with retry, server-side thumbnail generation for PDF export.
- Observability: event logging (non-sensitive), error tracking, sync failure diagnostics.
- Testing plan: unit tests for sync/conflict engine, integration tests for offline-to-online flows, e2e tests for critical paths (complete inspection offline → submit online → supervisor review).
- Rollout plan: feature flags for sync and offline features, safe IndexedDB schema migration strategy.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | High-level implementation plan with phases |
| `data-model.md` | Data structures for all entities |
| `research.md` | Technical research and library evaluations |
| `quickstart.md` | Key validation scenarios |
| `contracts/` | API specifications |

**Validate the plan:**

```
Review the implementation plan and check: (1) Are there any over-engineered components that violate our constitution's simplicity principle? (2) Does every technical choice trace back to a requirement in the spec? (3) Is the phase ordering logical — can each phase be validated independently?
```

**Checkpoint:**
- [ ] Tech stack matches what you specified
- [ ] No unnecessary dependencies or abstractions
- [ ] Data model covers all entities from the spec
- [ ] Sync protocol described with conflict detection and resolution steps
- [ ] Service worker strategy documented (cache-first vs network-first per resource)
- [ ] Attachment lifecycle clear (capture → compress → IndexedDB → upload queue → S3)

---

### Tasks

```
/speckit.tasks Break down the plan into small, ordered tasks.

Task breakdown rules:
- Each task should have a clear objective, explicit inputs/outputs, and "done when" checks.
- Prefer tasks that touch 1–2 files/components/modules at a time.
- Identify tasks that can be parallelized safely.
- Include dedicated tasks for tests (unit/integration/e2e) and documentation.
- Include tasks for edge cases (conflicts, retries, duplicate submissions, large attachments).
- Include integration checkpoint tasks where independently-built components are wired together and validated.
- Include an early end-to-end "golden path" task: Inspector logs in → starts inspection → fills checklist → attaches photo → goes offline → completes inspection → comes back online → submits → Supervisor reviews. This validates the full flow before edge cases are implemented.
```

**What to observe in `tasks.md`:**
- Tasks grouped by user story
- Dependency ordering — data models before services, services before UI
- `[P]` markers for tasks that can run in parallel
- File paths for each task
- Checkpoints between phases
- The golden-path task appears early in the sequence
- Integration checkpoint tasks exist between major components

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Run `/speckit.analyze` after tasks to check cross-artifact consistency. It validates that every spec requirement has a corresponding task, and every task traces back to the spec. Particularly valuable for complex offline-first apps where sync and conflict requirements can easily get lost between the plan and implementation.

---

### Implement

```
/speckit.implement
```

**What to watch for:**
- The AI follows the task order from `tasks.md`, not its own improvised order
- Generated code references back to spec requirements
- The data model matches `data-model.md`
- No features are added that weren't in the specification
- Service worker registration happens early
- IndexedDB schema setup matches the data model
- Sync engine is implemented before UI features that depend on it

---

## Extension Activities

### Add a Feature: Real-time Supervisor Notifications

```
/speckit.specify Add a real-time notification system for supervisors. When an inspector submits an inspection, the supervisor's dashboard shows a toast notification and updates the badge count without a page refresh. Use Server-Sent Events (SSE) for push — not WebSockets — to keep complexity low. Include a notification history page showing the last 50 events.
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test the Spec: Mid-inspection Handoff

Add a new requirement and see how it ripples through the plan and tasks:

```
A new requirement has emerged: inspectors may now hand off an in-progress inspection to a different inspector mid-visit (shift change). Update the spec, plan, and tasks to handle this. Consider: what happens to the original inspector's locally cached data? Does the new inspector's device need to pull the partial draft? How does this interact with conflict resolution?
```

This demonstrates SDD's iterative enhancement — specs evolve, and the toolchain propagates changes.
