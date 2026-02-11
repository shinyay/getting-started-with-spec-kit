# Scenario B — Facilitator Answer Key: Offline-first Field Inspection PWA

> **This file is for facilitators only.** Do not distribute to participants before the workshop — it removes the learning value of the clarification phase.

---

## Expected Domain Output: Sync Conflict Resolution Matrix

When `/speckit.clarify` resolves the sync and conflict decisions, the specification should produce a conflict resolution strategy covering these field types:

| Conflict Type | Local State | Remote State | Resolution Strategy |
|---|---|---|---|
| Text field (notes) | Edited offline | Edited by another inspector | Show diff, let user merge or pick one |
| Checklist item (pass/fail/NA) | Changed offline | Changed remotely | Last-write-wins by server timestamp; flag for review |
| Photo attachment | Added offline | Same item has different photo remotely | Keep both; surface duplicate for manual review |
| Inspection status | Submitted offline | Already submitted remotely | Reject duplicate (idempotency key); notify user |
| Template structure | Cached v1 | Updated to v2 on server | Complete with cached v1; banner suggests re-sync |

### Offline Storage Quota Strategy

| Threshold | Behavior |
|---|---|
| < 80% | Normal operation |
| 80–95% | Warning banner: "Storage filling up — submit completed inspections" |
| 95–100% | Block new photo attachments; text entry and checklist continue; never lose existing draft data |
| Write failure | Show "Storage full" error; retry once; if still failing, offer to export draft as JSON |

### Sync Queue Prioritization

The sync engine should process queued items in this order:
1. **Submitted inspections** (highest priority — business value)
2. **Photo uploads** for submitted inspections (complete the submission)
3. **Auto-saved drafts** (background, lowest priority)

Within each priority tier, process FIFO (oldest first).

---

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Completed inspection lifecycle | After supervisor approval → archived. Local cache purged after confirmed server receipt. Server retains 7 years (compliance). | Compliance-driven retention; local cleanup prevents storage exhaustion. |
| 2 | Supervisor notifications | Badge count on dashboard + optional daily email digest. No push in v1. | Low implementation cost; push notifications add complexity without critical value in v1. |
| 3 | Local data after server receipt | Purge from IndexedDB after server confirms receipt with 200 + receipt ID. Keep for 24h as buffer. | Balance storage pressure against "just submitted but need to reference" use case. |
| 4 | Supervisor rejection | Reject with comments → inspection returns as draft with rejection notes. Inspector sees a "Returned for rework" badge. | Common field workflow; prevents lost context from starting over. |
| 5 | Template versioning | Inspection keeps the template version it started with. Non-blocking banner if newer version exists. No forced migration mid-inspection. | Mid-inspection migration risks data loss; banner informs without disrupting. |
| 6 | Concurrent inspections | Max 3 concurrent in-progress inspections per inspector. Warn at 3, block at limit. | Prevents storage exhaustion on low-end devices; 3 covers realistic field scenarios. |
| 7 | Photo metadata (GPS/EXIF) | Keep GPS for compliance (location proof); strip camera model/serial. Configurable per template. | GPS proves "inspector was at site"; camera metadata is privacy-sensitive and unnecessary. |
| 8 | Supervisor reviews during offline edit | Supervisor sees a read-only snapshot of last-synced state. Banner: "Inspector may have unsaved changes." | Prevents edit conflicts between roles; snapshot is always consistent. |
| 9 | Past inspection reference | Yes, inspectors can view their own completed inspections (last 30 days). Cached offline if viewed within 7 days. | Field reference is common (re-inspecting same site); bounded cache prevents bloat. |
| 10 | Sync queue priority | FIFO within priority tiers: submitted inspections > photos for submitted > draft auto-saves. | Business value ordering — completed work reaches server first. |

---

## Facilitator Notes

### Constitution Phase
> Watch for participants who skip "offline-first as non-negotiable." If the constitution doesn't make offline the default mode, the entire spec will drift toward "online with offline fallback" — which is a fundamentally different architecture.

### Specification Phase
> The scope tiers are critical here. MVP must be genuinely offline-capable (checklist + auto-save + sync). Participants who put "photo attachments" in MVP are over-scoping — photos need upload queues, retry logic, and compression, which is Core complexity.

### Clarification Phase
> Questions 7 (photo metadata) and 8 (supervisor reviews during offline) are the most commonly missed. Push participants to think about the physical context — inspectors are in basements with no signal, supervisors are in offices with full connectivity. These different contexts create asymmetric assumptions.

### Plan Phase
> The #1 mistake is choosing a sync library without understanding the conflict model first. The sync strategy must be derived from the conflict resolution matrix, not the other way around. Ask: "What happens when two people edit the same checklist item?" before "Which library handles sync?"

### Implement Phase
> Watch for IndexedDB schema design. Participants often store everything in one object store. The schema should separate: timer state (hot, written every transition), inspection drafts (warm, written on auto-save), and completed inspections (cold, read-only cache). This maps to different sync and storage strategies.
