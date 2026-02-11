# Scenario F: High-throughput Event Ingestion Pipeline

| | |
|---|---|
| **Level** | ⭐⭐⭐⭐ Advanced |
| **Duration** | ~120 min |
| **Key SDD themes** | Data quality, schema evolution, backpressure, SLOs, cost-aware architecture |
| **Why it tests SDD** | Throughput targets, retention policies, schema evolution, and failure modes must be specified precisely — vague specs produce pipelines that silently drop data |
| **Best for** | Backend / data / platform engineers; anyone building event-driven or IoT systems |

---

## The Concept

IoT devices send telemetry events (metrics, diagnostics) at high throughput. The pipeline must ingest, validate, route, aggregate, and store these events — serving both near-real-time dashboards and long-term historical analytics. Schemas evolve over time as new device firmware adds new metrics, and the pipeline must handle this without breaking existing consumers.

This scenario stress-tests SDD because:
- **Throughput targets force concrete architecture** — "high throughput" without numbers is meaningless; the spec must define baselines and peaks
- **Schema evolution is an ongoing challenge** — adding new fields, deprecating old ones, and handling mixed-version device fleets simultaneously
- **Silent data loss is the worst failure mode** — vague error handling specs produce pipelines that quietly drop events under pressure
- **Cost is a first-class constraint** — unbounded retention or uncontrolled fan-out can make a pipeline economically unviable
- **Backpressure design must be explicit** — what happens when downstream is slower than upstream?

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create a constitution for a production-grade event ingestion pipeline.

Non-negotiables:
- No silent data loss: every ingested event must be either successfully processed or explicitly routed to a dead-letter queue with diagnostic context. Silent drops are never acceptable.
- Data quality: schema validation at the edge (ingestion point), explicit handling of unknown fields (preserve, don't discard), and a versioned schema strategy with forward and backward compatibility rules.
- At-least-once ingestion with idempotent processing: duplicates are safe to process; every unique event is processed at least once.
- Backpressure is a design choice, not an afterthought: define explicit behavior when each downstream component is slow or unavailable (buffer, shed load with 429, degrade gracefully).
- Cost awareness: all storage must have explicit retention/lifecycle policies. Compute must have autoscaling with defined min/max bounds. Architectural decisions must document their cost implications.
- Observability: structured metrics (ingestion rate, error rate, lag, queue depth), structured logs (no secrets, no PII), distributed tracing for event lifecycle, and alerting with defined thresholds.
- Security: TLS for all data in transit, encryption at rest for stored events, least-privilege IAM, API key authentication for device ingestion, and audit logs for administrative access.
- Idempotency keys: every event must carry a unique event_id; deduplication happens at the processing layer.
- Testing: include replay tests, schema evolution tests, load/stress tests, failure injection tests, and cost projection validation.
```

**Checkpoint** — verify the generated constitution includes:
- [ ] No-silent-data-loss guarantee
- [ ] Schema validation and evolution strategy
- [ ] At-least-once with idempotent processing
- [ ] Explicit backpressure behavior defined
- [ ] Cost awareness with retention policies
- [ ] Observability with specific metric types
- [ ] Security (TLS, encryption at rest, API keys)
- [ ] Idempotency key requirement

---

### Specification

```
/speckit.specify Build an event ingestion pipeline for IoT devices sending telemetry.

Context:
- 50,000 IoT devices deployed in industrial facilities send telemetry events.
- Devices send events every 10 seconds during active operation (12–16 hours/day).
- Events are JSON containing: event_id (UUID), device_id, device_firmware_version, timestamp (ISO 8601), metrics (object with named numeric values), and optional diagnostics (freeform object).
- Throughput baseline: ~5,000 events/second sustained. Peak (all devices active + burst): ~15,000 events/second for up to 30 minutes.

Functional requirements:

Ingestion:
- HTTP POST endpoint accepting single events or batches (up to 100 events per request).
- API key authentication per device fleet (not per device). Keys are rotatable without downtime.
- Events are validated against a versioned JSON Schema before processing.
- Valid events are acknowledged with 202 Accepted; invalid events return 400 with specific validation errors per event in the batch.
- If the pipeline is under pressure, respond with 429 Too Many Requests with a Retry-After header. Devices will back off and retry.

Schema strategy:
- Schemas are versioned (v1, v2, v3...). The schema version is determined by device_firmware_version.
- New schema versions may add optional metrics fields. Existing fields must not change type or be removed (backward compatible).
- Unknown fields (from newer firmware than the schema registry knows about) are preserved in raw storage but excluded from aggregation until the schema is updated.
- A schema registry stores all versions. Consumers declare which schema version(s) they support.

Storage (dual-layer):
- Raw event store: all validated events stored as-is for 90 days. Queryable by device_id, time range, and metric name. Partitioned by date for efficient lifecycle management.
- Aggregated metric store: 1-minute, 1-hour, and 1-day rollups of numeric metrics per device. Retained for 2 years. Powers dashboards and long-term analytics.
- Dead-letter store: invalid events and processing failures stored with error context for 30 days for investigation.

Processing:
- Stream processing layer consumes from a message queue, deduplicates by event_id, and fans out to: raw store writer, aggregation engine, and anomaly detector.
- Aggregation engine computes rollups (min, max, avg, p50, p95, count) per metric per device per time window.
- Anomaly detection: configurable per-metric thresholds (static) and z-score-based spike detection (dynamic). When an anomaly is detected, emit an alert event to a notification channel.

Query / dashboards:
- Near-real-time dashboard: displays the last 5 minutes of metrics for a selected device or device group. Data freshness target: <30 seconds from event ingestion to dashboard visibility.
- Historical analytics API: query aggregated metrics by device, metric name, and time range. Support for device groups and fleet-wide aggregations.

Replay:
- Support replaying raw events for a time range and/or specific device_ids from raw storage back into the processing pipeline.
- Replay must be idempotent: re-processing replayed events must not create duplicate aggregations (use event_id deduplication).
- Replay is triggered via an admin API and is audited.

Operational requirements:
- Backpressure: if the message queue depth exceeds a threshold, the ingestion endpoint begins returning 429. If a downstream store is unavailable, events buffer in the queue up to a configured retention limit (e.g., 4 hours). If the buffer fills, the oldest unprocessed events are moved to the dead-letter store (never silently dropped).
- Graceful degradation: if the aggregation engine is down, raw ingestion continues. If the anomaly detector is down, aggregation continues. Each component fails independently.
- Autoscaling: ingestion workers scale horizontally based on queue depth. Aggregation workers scale based on processing lag. Define min/max instance counts.

Acceptance criteria:
- Sustained 5,000 events/second with <500ms end-to-end ingestion latency (p99) under normal operation.
- Peak 15,000 events/second for 30 minutes without data loss (events may be buffered).
- If the aggregated store is unavailable for 1 hour, raw ingestion continues with zero loss; aggregation catches up after recovery.
- Schema v2 devices and v1 devices can coexist in the same fleet without pipeline errors.
- Dashboard shows data <30 seconds old under normal operation.
- Replay of 1 hour of data for 1,000 devices completes within 15 minutes.

Edge cases to explicitly cover:
- Device sends events with a future timestamp (clock drift): accept but flag; use server-received-time for ordering.
- Device sends a batch with some valid and some invalid events: accept valid, reject invalid, return per-event status.
- Message queue is full: dead-letter the oldest events (not the newest) and alert.
- Network partition between ingestion and processing: events buffer; no loss on recovery.
- Schema registry is unavailable: cache last-known schemas locally; reject events from completely unknown firmware versions.
- Device sends duplicate events (same event_id): deduplicate silently; count duplicates in metrics.
- Aggregation reprocessing after a bug fix: replay affected time range with corrected logic.

Non-goals (explicitly out of scope):
- Device management (provisioning, firmware updates, fleet grouping) — separate system.
- User-facing alerting UI — alerts are emitted to a notification channel (Slack/PagerDuty webhook); the UI is out of scope.
- Machine learning anomaly detection — use static thresholds and z-score only for v1.

Failure model (must be specified):
- Requests may time out and be retried by devices (at-least-once delivery).
- Messages may be delivered out of order across partitions.
- Processing consumers may crash after reading from queue but before writing to store.
- Downstream stores (S3, TimescaleDB) may become temporarily unavailable.
- Schema registry may be unreachable (cache fallback required).
- Device clocks may drift (events with future/past timestamps).

Safety invariants:
- No silent data loss — every event is either processed or dead-lettered with diagnostic context.
- Deduplication by event_id — duplicate processing never creates duplicate aggregations.
- Schema validation at ingestion — invalid events never reach the processing pipeline.
- Dead-letter store captures ALL failures with enough context to investigate and replay.

Liveness goals:
- If all components are healthy, events flow from ingestion to dashboard within 30 seconds.
- If a downstream store recovers, buffered events are eventually processed.
- Aggregation catches up after outage without manual intervention.

Scope tiers:
- MVP (required): HTTP ingestion endpoint + schema validation + Kafka producer + single consumer + raw S3 writer. Validates happy-path pipeline end-to-end.
- Core (recommended): + Deduplication + dead-letter routing + backpressure (429) + aggregation engine (1-min rollups) + dashboard query API + API key auth.
- Stretch (optional): + Anomaly detection + alerting + replay mechanism + autoscaling + cost validation + load testing (5K/15K events/sec) + failure injection.
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: What is the batch acknowledgment semantics when a batch is partially valid — 202 with per-event status, or 207 Multi-Status?
2. Decision needed: How are device groups defined and managed — in this pipeline or in an external system?
3. Decision needed: What happens to aggregations when a schema version adds a new metric — backfill from raw, or forward-only?
4. Decision needed: What is the cost budget or cloud spend constraint?
5. Decision needed: How are API keys provisioned and distributed to device fleets?
6. Decision needed: What ordering guarantees do we provide — per-device, global, or none?
7. Decision needed: How are late-arriving events (>1 hour old) handled — included in aggregations or stored raw only?
8. Decision needed: When the message queue is full, which events are dead-lettered — oldest (FIFO shed) or newest (backpressure)?
9. Decision needed: Should the schema registry be an external service (Confluent) or a lightweight custom implementation?
10. Decision needed: What is the data retention lifecycle — can admins override the 90-day raw retention for compliance?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/F-event-ingestion-pipeline-answers.md`](_answers/F-event-ingestion-pipeline-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] User stories / system stories with acceptance criteria
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguous areas
- [ ] Concrete throughput numbers (5K sustained, 15K peak)
- [ ] Dual-layer storage with retention policies
- [ ] Schema versioning with compatibility rules
- [ ] Backpressure behavior defined at each layer
- [ ] Failure model and safety invariants
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify Review the event ingestion pipeline spec and ask me about every ambiguity, unstated assumption, and gap — especially around: batch response semantics, device group management, new-metric aggregation backfill, cost constraints, API key provisioning, event ordering guarantees, and any distributed systems edge cases you can identify.
```

Review the questions surfaced. Use the 10 decision questions above as a checklist — did the AI catch all of them?

**Manual refinement:**

```
For sample data and testing: define 3 device firmware versions (v1 with 3 metrics, v2 adds 2 optional metrics, v3 adds 1 metric and deprecates-but-preserves one from v1). Create sample event payloads for each version. Include one malformed event (missing required field) and one with an unknown firmware version.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] Throughput and latency SLOs are concrete and measurable
- [ ] Backpressure behavior defined for every component boundary
- [ ] Schema evolution rules are explicit (add optional fields, never remove, preserve unknown)
- [ ] Dead-letter path exists for every failure mode (no silent drops)
- [ ] Late-arriving event handling is defined
- [ ] All edge cases have defined behaviors

---

### Plan

```
/speckit.plan Create a technical plan for the IoT event ingestion pipeline.

Tech stack:
- Ingestion API: Node.js + Fastify (high-throughput HTTP), deployed in Docker containers with horizontal autoscaling.
- Message queue: Apache Kafka (partitioned by device_id for ordering; configurable retention for buffering).
- Stream processing: Node.js consumers (or Apache Flink if justified — document tradeoff). Kafka consumer groups for parallel processing.
- Schema registry: Confluent Schema Registry (or a lightweight custom registry using PostgreSQL — document tradeoff).
- Raw event store: Amazon S3 (Parquet files, partitioned by date) with Athena for ad-hoc queries. 90-day lifecycle policy.
- Aggregated metric store: TimescaleDB (PostgreSQL extension for time-series). Continuous aggregation for rollups. 2-year retention with automatic downsampling.
- Dead-letter store: S3 bucket with 30-day lifecycle.
- Dashboard data: TimescaleDB for near-real-time queries. Materialized views refreshed on new data.
- Caching: Redis for schema cache, API key validation cache, and dashboard query cache (short TTL).
- Monitoring: Prometheus + Grafana for metrics and dashboards. PagerDuty for alerting.
- Deployment: Docker + Kubernetes, CI/CD via GitHub Actions.

The plan must include:
- Ingestion architecture: HTTP → validate → produce to Kafka. Backpressure: monitor Kafka lag; return 429 when lag exceeds threshold.
- Kafka topic design: raw-events topic (partitioned by device_id, 30 partitions baseline), dead-letter topic, alert-events topic. Retention: 4 hours for raw-events (buffer), 30 days for dead-letter.
- Schema validation: validate at ingestion against cached schemas from registry. Unknown firmware versions → reject with error. Unknown fields from known versions → preserve in raw event, strip from aggregation input.
- Processing pipeline: Kafka consumer group → deduplicate by event_id (Redis set with 1-hour TTL) → fan-out to: (1) S3 raw writer (batched, write Parquet every 60 seconds or 10,000 events), (2) aggregation engine (update TimescaleDB continuous aggregates), (3) anomaly detector (compare against thresholds, emit to alert-events topic).
- Aggregation strategy: TimescaleDB continuous aggregates for 1-min rollups; scheduled jobs for 1-hour and 1-day rollups. Pre-compute min, max, avg, p50, p95, count per metric per device.
- Anomaly detection: static thresholds (configurable per metric per device type) + z-score spike detection (rolling 1-hour window, alert if z-score > 3). Emit alert events to Kafka alert-events topic → consumed by notification service.
- Replay mechanism: admin API triggers a Kafka producer that reads raw events from S3 for a specified time range / device filter and re-publishes to a replay-events topic. Processing consumers handle replay-events identically to raw-events (idempotent — event_id deduplication prevents duplicate aggregation).
- API key management: keys stored in PostgreSQL (hashed), cached in Redis (5-min TTL). Rotation supports dual-active keys.
- Query API: REST endpoints for dashboard (latest metrics, last 5 min) and analytics (aggregated metrics by time range). Rate-limited. Results paginated.
- SLO/SLA definitions: ingestion latency p99 < 500ms, dashboard freshness < 30s, availability 99.9%, zero silent data loss. Alert thresholds for each.
- Autoscaling: ingestion pods scale on CPU + request rate (min 3, max 20). Processing consumers scale on Kafka consumer lag (min 3, max 15). Aggregation workers scale on processing lag (min 2, max 10).
- Cost analysis: estimate monthly cost breakdown (compute, Kafka, S3, TimescaleDB, Redis) at baseline and peak. Identify top cost drivers and optimization levers.
- Test plan: load tests at 5K and 15K events/second sustained, replay correctness tests, schema evolution tests (add v2 metrics while v1 devices are active), failure injection (kill processing consumers, make S3 unavailable, partition Kafka), and cost projection tests (verify retention policies actually delete data on schedule).
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Architecture, data flow, SLOs, and cost analysis |
| `data-model.md` | Event schema versions, Kafka topics, S3 layout, TimescaleDB schema, Redis key patterns |
| `research.md` | Kafka vs alternatives, Flink vs Node consumers, TimescaleDB vs InfluxDB, schema registry options |
| `contracts/` | Ingestion API contract (OpenAPI), event schema (JSON Schema v1/v2/v3), query API contract |
| `quickstart.md` | Key validation scenarios |

**Validate the plan:**

```
Review the implementation plan and check: (1) Is there a clear data loss path analysis — for every failure mode, where do events go? (2) Is the cost estimate realistic for the throughput targets? (3) Does the replay mechanism correctly handle idempotency? (4) Are SLOs defined with concrete numbers and alerting thresholds?
```

**Checkpoint:**
- [ ] Data flow is traceable: HTTP → Kafka → consumers → S3 / TimescaleDB / alerts
- [ ] Backpressure behavior is defined at each boundary (HTTP→Kafka, Kafka→consumers, consumers→stores)
- [ ] Schema validation happens at ingestion (not downstream)
- [ ] Dead-letter path exists for every failure mode
- [ ] SLOs have concrete numbers (latency, freshness, availability)
- [ ] Cost estimate exists with breakdown by component
- [ ] Autoscaling has min/max bounds

---

### Tasks

```
/speckit.tasks Generate tasks for implementing the ingestion pipeline.

Task preferences:
- Start with "happy path" ingestion first: schema definition → HTTP endpoint → Kafka producer → consumer → raw S3 writer. Validate end-to-end before adding resilience.
- Then add resilience: deduplication, dead-letter routing, backpressure (429 responses), retry logic.
- Then add analytics: aggregation engine, TimescaleDB continuous aggregates, rollup jobs.
- Then add anomaly detection and alerting.
- Then add replay mechanism.
- Then add monitoring dashboards and alert rules.
- Include explicit tasks for: schema registry setup and evolution tests, API key management, load testing at baseline and peak, cost validation (verify retention policies), and failure injection testing.
- Each task must have a "done when" check.
- Identify parallelizable tasks (e.g., S3 writer and aggregation engine can be built in parallel once the Kafka consumer framework exists).
```

**What to observe in `tasks.md`:**
- Happy path is completed and validated before resilience is added
- Schema definition and event contracts appear as the very first tasks
- Kafka topic creation and consumer framework are early foundational tasks
- Load testing tasks specify concrete throughput targets (5K, 15K events/sec)
- Cost validation task verifies S3 lifecycle policies actually delete data
- Failure injection tasks exist (kill consumers, make stores unavailable)
- Parallelizable tasks are marked

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Focus on the failure model — for every failure mode, trace where events end up. Is there a dead-letter path for each? Are there test cases for every backpressure trigger?

---

### Implement

```
/speckit.implement Execute all tasks in order. After completing the happy-path ingestion (HTTP → Kafka → S3), run a load test at baseline throughput (5,000 events/sec) to validate the pipeline before adding resilience features. After adding resilience, run failure injection tests before proceeding to analytics.
```

**What to watch for:**
- The AI follows the task order from `tasks.md`
- Schema validation rejects invalid events with specific error messages (not generic 400)
- Kafka producer uses device_id as partition key
- Event deduplication uses event_id with a bounded TTL (not unbounded storage)
- S3 writer batches events into Parquet files (not one file per event)
- Dead-letter routing includes diagnostic context (why the event failed)
- Backpressure returns 429 with Retry-After header (not 503)
- No secrets or PII in log output

---

## Extension Activities

### Add a Feature: Device-level Anomaly Baselines

Extend anomaly detection with per-device learned baselines:

```
/speckit.specify Add per-device anomaly baselines to the event pipeline. Instead of fleet-wide static thresholds, compute a rolling 7-day baseline for each metric on each device. Alert when a device's current metric deviates more than 3 standard deviations from its own baseline. Store baselines in TimescaleDB, recompute daily. Include a "learning mode" for new devices (suppress alerts for the first 7 days). Consider: how does this interact with device firmware updates that legitimately change metric behavior?
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test the Spec: Schema Breaking Change

Force a non-backward-compatible schema change and trace the consequences:

```
A new requirement has emerged: firmware v4 renames the metric "cpu_temp" to "processor_temperature" and changes the unit from Celsius to Kelvin. This is a breaking change. Update the spec, plan, and tasks to handle this. Consider: how do you maintain dashboard continuity (same graph, different field name)? How does replay work for historical data with the old field name? What does the schema registry compatibility check report? Can v3 and v4 devices coexist?
```

This demonstrates how SDD handles breaking changes in data contracts — the spec forces you to trace the impact across every consumer before making the change.
