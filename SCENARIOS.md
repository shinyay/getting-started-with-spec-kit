# 🎯 Workshop Scenarios

> **Pick a scenario. Learn Spec-Driven Development by building something real.**

Every scenario walks you through the full SDD lifecycle — from defining principles to generating working code. You'll use the same `/speckit.*` commands, but each scenario teaches a different aspect of specification writing.

**New to SDD?** Start with a ⭐ scenario. **Already comfortable?** Jump to ⭐⭐ or higher.

👉 Open a scenario, then follow along with the [Workshop Guide](WORKSHOP.md).

---

## ⭐ Beginner — Start Here

No server, no database. Pure frontend or single-file apps. Focus on learning the SDD workflow itself.

| | Scenario | What You Build | What You Learn | Duration |
|---|---|---|---|---|
| **A** | [QuickRetro](scenarios/A-quick-retro.md) | Team retrospective board | Data modeling, CRUD specs, permissions | ~90 min |
| **J** | [Pomodoro Timer](scenarios/J-pomodoro-timer.md) | Focus timer + task tracker | State machine specification, time-based logic | ~90 min |
| **K** | [MarkdownPad](scenarios/K-markdown-notes.md) | Note-taking app with preview | Rendering correctness, feature whitelist, XSS prevention | ~90 min |
| **L** | [RecipeBox](scenarios/L-recipe-collection.md) | Recipe collection + meal planner | Fraction arithmetic, calculation correctness, unit conversion | ~90 min |

**Which one?**
- 🟢 **A (QuickRetro)** — Best first scenario. Simplest domain, teaches the full workflow.
- 🟡 **J (Pomodoro)** — Best for "how do I spec behavior?" State machines are a universal pattern.
- 🟡 **K (MarkdownPad)** — Best for "how do I spec output?" Teaches whitelisting and security.
- 🟡 **L (RecipeBox)** — Best for "how do I spec calculations?" Teaches algorithmic correctness.

---

## ⭐⭐ Intermediate — Add a Server

Node.js + Express + SQLite. Real API endpoints, real database, real HTTP semantics. You'll learn to specify contracts that clients actually depend on.

All ⭐⭐ scenarios share a [baseline contract](WORKSHOP.md#intermediate-baseline-contract) (error format, pagination, dates, DB conventions) so you focus on the SDD lesson, not boilerplate.

| | Scenario | What You Build | What You Learn | Duration |
|---|---|---|---|---|
| **H** | [Log Analysis CLI](scenarios/H-cross-platform-cli.md) | Cross-platform log parser | CLI output contracts, deterministic output, streaming | ~100 min |
| **M** | [ShortLink](scenarios/M-url-shortener.md) | URL shortener + analytics API | API contract design, HTTP redirect semantics, cursor pagination | ~100 min |
| **N** | [KanbanFlow](scenarios/N-kanban-board.md) | Task board with drag-and-drop | Multi-entity relationships, fractional indexing, cascade operations | ~100 min |
| **O** | [MoneyTrail](scenarios/O-csv-importer.md) | CSV importer + spending reports | Data validation pipelines, money-as-cents, aggregation correctness | ~100 min |

**Which one?**
- 🟢 **M (ShortLink)** — Best first intermediate. "Make a short link" sounds simple, but 301 vs 302, route ordering, and idempotency reveal why specs matter.
- 🟡 **N (KanbanFlow)** — Best for "how do I spec relationships?" Card ordering is an invisible spec problem that breaks without a contract.
- 🟡 **O (MoneyTrail)** — Best for "how do I spec data quality?" Every CSV row gets a verdict — success, warning, error, or skipped.
- 🟡 **H (CLI)** — Best for "how do I spec non-web software?" CLI output IS the contract.

---

## ⭐⭐⭐ Intermediate–Advanced — Real-World Complexity

External services, auth, multi-tenancy, financial correctness. These mirror production challenges where a missing spec causes real damage.

| | Scenario | What You Build | What You Learn | Duration |
|---|---|---|---|---|
| **B** | [Field Inspection PWA](scenarios/B-field-inspection-pwa.md) | Offline-first mobile app | Offline sync, conflict resolution, media uploads | ~120 min |
| **C** | [OIDC SSO + RBAC](scenarios/C-oidc-sso-rbac.md) | Enterprise auth system | Security contracts, multi-tenancy, secret rotation | ~120 min |
| **D** | [Stripe Subscriptions + Dunning](scenarios/D-stripe-subscriptions.md) | Subscription + dunning flow | Money correctness, idempotency, webhook state machines | ~120 min |
| **G** | [Terraform + GitHub Actions](scenarios/G-terraform-github-actions.md) | Infrastructure-as-Code pipeline | Drift detection, blast radius, governance | ~120 min |
| **I** | [API Versioning Migration (v1→v2)](scenarios/I-api-versioning-migration.md) | API migration with shim layer | Backward compatibility, deprecation governance | ~110 min |

**Which one?**
- 🟢 **D (Stripe Subscriptions)** — The "money must be exact" constraint shows why SDD prevents real-world damage.
- 🟡 **B (Field Inspection)** — The "what happens offline?" question teaches sync conflict specification.
- 🟡 **C (OIDC SSO)** — The "who can access what?" question teaches security-first specification.
- 🟡 **I (API Versioning)** — The "200 consumers depend on v1" constraint teaches backward-compatible specification.
- 🟡 **G (Terraform)** — The "infrastructure IS the spec" lesson applies SDD to ops, not just apps.

---

## ⭐⭐⭐⭐ Advanced — Distributed Systems

Concurrency, real-time collaboration, high-throughput pipelines, distributed workflows, platform extensibility. These push SDD to its limits — the spec must define failure models, safety invariants, and quantitative SLOs.

All ⭐⭐⭐⭐ scenarios require specifying a [failure model, safety invariants, and observability requirements](WORKSHOP.md#advanced-baseline-contract).

| | Scenario | What You Build | What You Learn | Duration |
|---|---|---|---|---|
| **E** | [Collaborative Whiteboard](scenarios/E-collaborative-whiteboard.md) | Real-time drawing canvas | Consistency models, client prediction, conflict resolution | ~120 min |
| **F** | [Event Ingestion Pipeline](scenarios/F-event-ingestion-pipeline.md) | IoT data pipeline | Schema evolution, backpressure, SLOs, data quality | ~120 min |
| **P** | [OrderFlow Saga](scenarios/P-order-fulfillment-saga.md) | Multi-step order fulfillment | Compensating transactions, timeout semantics, exactly-once | ~120 min |
| **Q** | [PlugKit Runtime](scenarios/Q-plugin-runtime.md) | Plugin platform + sandbox | Public API contracts, sandboxed execution, capability permissions | ~120 min |
| **R** | [FlagShip Experimentation](scenarios/R-feature-flag-experimentation.md) | Feature flags + A/B testing | Deterministic bucketing, statistical correctness, kill switches | ~120 min |

**Which one?**
- 🟢 **P (OrderFlow)** — Best first advanced. "Payment timed out — did it charge?" teaches that distributed failure is the default state.
- 🟡 **E (Whiteboard)** — Best for "how do I spec real-time?" Consistency model is the fundamental architectural choice.
- 🟡 **F (Pipeline)** — Best for "how do I spec throughput?" Forces concrete SLOs, not vague "high performance."
- 🟡 **Q (PlugKit)** — Best for "how do I spec a platform?" Your spec IS the product — external developers build against it.
- 🟡 **R (FlagShip)** — Best for "how do I spec correctness that's both statistical AND distributed?" Bucketing + SRM detection.

---

## Suggested Learning Paths

### 🚀 "I have 90 minutes"
→ Pick **one beginner** scenario (A is the safest bet)

### 📚 "I have a half day"
→ **A** (learn the workflow) → **M** or **N** (add a server)

### 🎓 "I have a full day"
→ **A** → **J** or **K** → **M** → **N** → choose one ⭐⭐⭐

### 🧠 "I want the advanced track"
→ **M** (API contracts) → **D** (Stripe billing) → **P** (saga) → **R** (experimentation)

### 🏢 "Team training — mixed levels"
→ Everyone does **A** together, then self-selects by level

### 🎤 "Conference talk (60 min)"
→ **A** or **J**, MVP tier only — demo the SDD workflow live

---

## How Each Scenario Works

Every scenario follows the same structure:

```
1. /speckit.constitution   → Define project principles
2. /speckit.specify        → Describe what to build (with deliberate ambiguities)
3. /speckit.clarify        → Resolve the ambiguities (this is where SDD pays off)
4. /speckit.plan           → Choose technology and architecture
5. /speckit.tasks          → Break into executable tasks
6. /speckit.analyze        → (Optional) Cross-check spec ↔ tasks alignment
7. /speckit.implement      → Generate code from specifications
```

Each scenario includes:
- **Phase prompts** — copy-paste into Copilot Chat
- **Checkpoints** — verify the AI produced the right artifacts
- **Decision questions** — deliberate ambiguities you must resolve
- **Extension activities** — go deeper after the core workshop

⭐⭐+ scenarios also include **facilitator answer keys** in [`scenarios/_answers/`](scenarios/_answers/).

---

## Getting Started

```bash
# 1. Launch environment
# Click "Open in GitHub Codespaces" on the README, or:
git clone https://github.com/shinyay/getting-started-with-spec-kit.git
# Open in VS Code → "Reopen in Container"

# 2. Initialize Spec Kit
specify init . --ai copilot --force
specify check

# 3. Pick a scenario from the tables above and open its file
# 4. Follow the phase prompts in order
```

For detailed facilitator guidance, timing tables, and teaching tips, see the [Workshop Guide](WORKSHOP.md).
