# Scenario F: Event Ingestion Pipeline — Facilitator Answer Key

> **This file is for facilitators only.** Do not share with participants before the `/speckit.clarify` phase.

## Pipeline Data Flow

```
Device → HTTP POST → Schema Validate → Kafka → Consumer Group
                                                    ├── Raw S3 Writer (Parquet, batched)
                                                    ├── Aggregation Engine (TimescaleDB)
                                                    └── Anomaly Detector → Alert Topic
                                          Failures → Dead-Letter (S3, 30 days)
```

## SLO Summary

| Metric | Target | Alert Threshold |
|---|---|---|
| Ingestion latency (p99) | <500ms | >1s for 5 min |
| Dashboard freshness | <30s | >60s for 5 min |
| Availability | 99.9% | Any 5xx spike >1% |
| Silent data loss | Zero | Any event unaccounted for |
| Replay (1hr, 1K devices) | <15 min | >30 min |

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Batch response semantics | 207 Multi-Status with per-event array: `{ event_id, status: "accepted"/"rejected", error? }`. Batch is NOT atomic. | Devices need per-event feedback; partial acceptance is standard |
| 2 | Device groups | External system manages groups; pipeline queries on dashboard requests | Separation of concerns; pipeline focuses on ingestion, not device management |
| 3 | New metric aggregation | Forward-only from schema registration; backfill via admin-triggered replay | Automatic backfill is expensive and risky; manual replay is intentional |
| 4 | Cost budget | <$5,000/month at baseline; storage lifecycle is primary lever; compute autoscaling capped at 20 instances | Forces architectural cost awareness; prevents unbounded scaling |
| 5 | API key provisioning | Admin API creates keys scoped to fleet; rotation with 7-day dual-active overlap window | Zero-downtime rotation; fleet-level (not per-device) keeps key count manageable |
| 6 | Event ordering | No global ordering; approximate order within device_id partition; aggregation uses event timestamps | Global ordering is prohibitively expensive; timestamp-based aggregation is sufficient |
| 7 | Late-arriving events | Raw storage with `late_arrival` flag; excluded from real-time aggregation; includable via replay | Prevents dashboard instability; replay is the correct mechanism for corrections |
| 8 | Queue full policy | Dead-letter OLDEST events (FIFO shed); never drop newest | Newest events are more valuable for real-time; oldest are already in raw storage or recoverable |
| 9 | Schema registry | Lightweight custom (PostgreSQL table) for workshop; Confluent for production | Workshop simplicity; production would use Confluent for compatibility checking |
| 10 | Retention override | Configurable per-fleet; admin API to extend/reduce; audit-logged changes | Compliance may require longer retention; audit prevents silent policy changes |

## Backpressure Reference

| Boundary | Trigger | Behavior |
|---|---|---|
| HTTP → Kafka | Kafka producer queue full or lag > threshold | Return 429 + Retry-After header |
| Kafka → Consumers | Consumer lag > threshold | Scale consumers (up to max) |
| Consumers → S3 | S3 unavailable | Buffer in Kafka (up to 4hr retention) |
| Consumers → TimescaleDB | DB unavailable | Buffer; raw ingestion continues; aggregation catches up |
| Buffer overflow | Kafka retention exceeded | Dead-letter oldest events; alert ops |

## Facilitator Notes

- **After Constitution**: "Ask: what does 'no silent data loss' mean concretely? It means every event has a known final destination — processed, dead-lettered, or buffered. Name the destination for each failure mode."
- **After Specify**: "The throughput numbers (5K/15K) force real architecture. Ask: can a single Node.js process handle 5K events/sec? (Answer: yes for validation + Kafka produce; no for full processing.)"
- **After Clarify**: "The cost constraint ($5K/month) forces storage lifecycle decisions. Ask: what's the monthly S3 cost for 5K events/sec × 90 days? This makes retention policy concrete."
- **After Plan**: "Check: for every failure mode in the failure model, is there a dead-letter path? If a team's plan has any path that ends in 'log the error', that's a silent drop."
- **Common mistake**: Teams compute file hash or schema validation AFTER queueing (should be at ingestion, before Kafka).
- **Common mistake**: Deduplication uses unbounded storage (should be Redis with 1hr TTL, scoped to event_id).
