# Scenario G — Facilitator Answer Key: Terraform + GitHub Actions Multi-Environment Infrastructure

> **This file is for facilitators only.** Do not distribute to participants before the workshop — it removes the learning value of the clarification phase.

---

## Expected Domain Output: Module Dependency Graph

When `/speckit.plan` produces the architecture, the module structure should follow this dependency order:

```
bootstrap/          (manual, local state — creates: S3 bucket, DynamoDB lock, OIDC provider, ECR)
    ↓
modules/networking  (VPC, subnets, NAT, security groups, VPC flow logs)
    ↓
modules/database    (RDS PostgreSQL, Secrets Manager, subnet group, security group)
    ↓
modules/compute     (ECS cluster, task definition, ALB, auto-scaling, ECR image reference)
    ↓
modules/observability (CloudWatch logs, metrics, alarms, dashboards, X-Ray)
    ↓
modules/cost-controls (AWS Budgets, tagging policy, scheduled scaling rules)
```

### Environment Sizing Matrix

| Parameter | dev | staging | prod |
|---|---|---|---|
| AZs | 1 | 2 | 3 |
| NAT Gateway | Single | Single | HA (one per AZ) |
| ECS tasks (min/max) | 1/2 | 2/4 | 3/10 |
| RDS instance | db.t3.micro | db.t3.small | db.r6g.large (or Aurora Serverless v2) |
| RDS backups | 7 days | 14 days | 30 days |
| CloudWatch log retention | 7 days | 30 days | 90 days |
| X-Ray tracing | Off | On | On |
| SSH/SSM access | SSH (wider SG) | SSM only | SSM only |
| Auto-destroy idle | Yes (72h) | No | No |
| Budget | $200/mo | $500/mo | $3,000/mo |

### CI Pipeline Stages

```
PR opened/updated:
  ├─ terraform fmt -check
  ├─ terraform validate
  ├─ tfsec (security scan)
  ├─ terraform plan → save as artifact + comment on PR
  └─ infracost → comment cost diff on PR

Merge to main:
  ├─ terraform apply (dev) ← automatic, uses saved plan artifact
  ├─ terraform apply (staging) ← requires 1 reviewer approval (GitHub Environment)
  └─ terraform apply (prod) ← requires 1 of 2 designated approvers + 5-min wait timer

Scheduled (daily):
  └─ terraform plan per environment → alert on non-zero changes (drift detection)
```

---

## Reference Answers

| # | Question | Recommended Answer | Rationale |
|---|---|---|---|
| 1 | Directory/module structure | Monorepo: `modules/` (networking, compute, database, observability, cost-controls), `environments/` (dev/, staging/, prod/ — each with main.tf, tfvars, backend.tf), `bootstrap/` (one-time setup). | Reusable modules + per-environment tfvars = add new env without module changes. |
| 2 | ECR bootstrap | Separate `bootstrap/` Terraform config applied manually once. Creates S3 state bucket, DynamoDB lock table, OIDC provider, and ECR repo. Uses local state (the only exception). | Solves chicken-and-egg: state bucket must exist before Terraform can use remote state. |
| 3 | OIDC trust policy | Trust policy scoped to specific GitHub org/repo. Main branch for apply; any branch for plan (read-only). Each environment's IAM role trusts only its own workflow. | Prevents cross-environment access; branch scoping prevents unauthorized applies. |
| 4 | Database credentials | `manage_master_user_password = true` on RDS (Terraform never sees password). App retrieves from Secrets Manager at runtime. Auto-rotation every 30 days. | Password never in state file; auto-rotation reduces credential exposure window. |
| 5 | Alerting destinations | CloudWatch → SNS → Slack (#infra-alerts) for all environments. Prod critical (service down, budget exceeded) also pages via PagerDuty. | Slack for awareness, PagerDuty for action. No alert fatigue from dev/staging paging. |
| 6 | Terraform version pinning | `required_version = "~> 1.6"` in terraform block. CI uses exact version in workflow YAML. Developers use tfenv or mise. Upgrade process: bump in dev first, validate, then staging/prod. | Prevents version drift; patch-level flexibility with `~>` avoids unnecessary churn. |
| 7 | Module update with resource replacement (stateful) | Stateful resource replacement (RDS) requires explicit approval + maintenance window. CI detects destroy+create in plan output and adds a "⚠️ DESTRUCTIVE" label to the PR. No auto-apply for destructive changes in prod. | RDS replacement = data loss without backup/restore. Must be a deliberate, planned event. |
| 8 | Shared cross-environment resources | Bootstrap state (ECR, OIDC provider, state bucket) is separate from environment state. Each environment's state is fully independent. Shared IAM policies reference resources by tag, not by ARN. | Environment isolation: a bad apply in dev cannot corrupt prod's state or resources. |
| 9 | Destroy in prod approval | Different from normal apply: requires BOTH designated approvers (not just one). Plan output must be reviewed line-by-line. CI comments include resource names being destroyed. | Two-person rule for destructive prod changes. Visibility into exactly what's being destroyed. |
| 10 | Plan artifact validity | Plan artifact is valid for the duration of the PR review (no hard timeout). Apply step re-validates the plan hash. If infrastructure changed between plan and apply, the apply fails safely and requires re-plan. | Terraform's built-in plan validation catches drift. No stale plan can be applied silently. |

---

## Facilitator Notes

### Constitution Phase
> The critical principle is "no manual changes." Watch for participants who skip drift detection. Without it, "no manual changes" is unenforceable — someone will click in the console during an incident, and without drift detection, the code and reality silently diverge.

### Specification Phase
> The scope tiers matter greatly for infrastructure. MVP is a single environment (dev) with remote state. Participants who try to build 3 environments + CI + drift detection in MVP will run out of time. The key insight: get one environment working end-to-end, then parameterize.

### Clarification Phase
> Questions 7 (stateful resource replacement) and 10 (plan artifact validity) are the most missed. Both are "what happens when things go wrong?" scenarios. Participants focus on the happy path (plan → apply → done) and forget that plans can become stale and replacements can destroy data.

### Plan Phase
> The #1 mistake is not separating bootstrap from ongoing operations. If the state bucket is in the same Terraform config as the infrastructure, you can't bootstrap — you need the bucket to exist before Terraform can use it. The bootstrap/ongoing split is essential.

### Implement Phase
> Watch for hardcoded values in modules. Every environment difference must come from variables (tfvars). If a participant hardcodes `us-east-1` or `db.t3.micro` in a module, adding a new environment will require module changes — violating the acceptance criteria.
