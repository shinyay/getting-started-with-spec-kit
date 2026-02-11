# Scenario G: Terraform + GitHub Actions Multi-Environment Infrastructure

| | |
|---|---|
| **Level** | ⭐⭐⭐ Intermediate–Advanced |
| **Duration** | ~120 min |
| **Key SDD themes** | Infrastructure governance, drift prevention, environment parity, secrets management, cost control |
| **Why it tests SDD** | Infrastructure specs demand precision — a vague network rule or missing IAM policy is a security incident or an outage, not just a bug |
| **Best for** | Platform / DevOps / SRE engineers; developers who manage their own infrastructure |

---

## The Concept

You are building Infrastructure-as-Code (Terraform) with a CI/CD pipeline (GitHub Actions) to provision a standard platform for a web service across dev, staging, and prod environments. All changes go through PR review, CI validates plans, and applies require approval for production. No manual console changes allowed.

This scenario stress-tests SDD because:
- **Infrastructure ambiguity = outages and security incidents** — a vague security group rule or missing IAM boundary isn't a UI bug, it's a production incident
- **Environment parity is deceptively hard** — "consistent baseline but different sizing" requires precise parameterization; copy-paste between environments is the #1 source of drift
- **Secrets management in CI is a security-critical design decision** — one wrong step and credentials are in logs or state files
- **Drift detection is an ongoing operational concern** — the spec must define what happens when reality diverges from code
- **Cost control requires governance, not just monitoring** — without guardrails, a typo in instance sizing costs thousands

This is the same skill that appears at higher difficulty in:
- Scenario R (⭐⭐⭐⭐): Progressive rollout governance with kill switches — the same "change governance" problem applied to feature releases instead of infrastructure
- Scenario P (⭐⭐⭐⭐): Multi-step orchestration with rollback/compensation — the same "apply-then-verify-then-rollback" pattern applied to distributed business workflows

---

## Phase Prompts

### Constitution

```
/speckit.constitution Create a constitution for Infrastructure-as-Code (Terraform) with CI/CD via GitHub Actions.

Non-negotiables:
- No manual changes: all managed resources must be provisioned and modified exclusively through Terraform. Manual console changes are forbidden and must be detected via drift detection.
- Drift detection and remediation: run scheduled drift detection (terraform plan with no changes expected). Alert on any drift. Document the remediation process (re-apply from code, or import + codify the manual change if justified).
- Least privilege IAM: each environment has its own IAM roles with minimal permissions. CI/CD service accounts have apply permissions only for their target environment. No cross-environment access.
- Environment isolation: dev, staging, and prod are fully isolated — separate accounts/projects, separate state files, separate credentials. A misconfiguration in dev must not affect prod.
- Remote state with locking: state is stored remotely (S3 + DynamoDB or equivalent) with locking to prevent concurrent applies. State access is audited and restricted to authorized principals.
- Secrets hygiene: secrets must never be committed to Git, appear in Terraform plan output, or be stored in state unencrypted. Use approved secret storage (AWS Secrets Manager, GitHub Actions OIDC, or equivalent). Rotate credentials on a defined schedule.
- Change governance: all changes go through PR review. CI must run fmt, validate, and plan checks on every PR. Apply requires explicit approval for staging and prod (GitHub Environments with protection rules).
- Blast radius control: changes to shared/foundational resources (networking, IAM) require additional review. Use Terraform workspaces or directory separation to limit the blast radius of a single apply.
- Rollback strategy: every apply must be reversible. Document the rollback procedure for each resource type (re-apply previous commit vs. manual intervention for stateful resources).
- Tagging: all resources must be tagged with environment, service, owner, cost-center, and managed-by=terraform. Untagged resources are flagged for remediation.
- Testing: include plan validation, security scanning (tfsec/checkov), cost estimation (infracost), and post-apply smoke tests.
```

**Checkpoint** — verify the generated constitution includes:
- [ ] No-manual-changes principle with drift detection
- [ ] Least privilege IAM per environment
- [ ] Environment isolation (separate accounts/state/credentials)
- [ ] Remote state with locking and audit
- [ ] Secrets hygiene rules
- [ ] Change governance (PR review, CI checks, apply approval)
- [ ] Blast radius control
- [ ] Rollback strategy requirement
- [ ] Mandatory tagging policy

---

### Specification

```
/speckit.specify Create Infrastructure-as-Code to provision a standard platform for a web service across dev, staging, and prod.

Context:
- A team is deploying a containerized REST API service. The infrastructure must be consistent across environments but right-sized per environment.
- Cloud provider: AWS (adaptable to others, but specify AWS-native services for concreteness).
- The team has 5 engineers. Two are designated "infrastructure approvers" for prod changes.

Requirements:

Environments:
- dev: smallest sizing, relaxed security (wider SSH access for debugging), single-AZ, auto-destroy idle resources after 72 hours.
- staging: mirrors prod topology at reduced scale. Used for integration testing and pre-prod validation.
- prod: full sizing, multi-AZ, hardened security, no SSH access (use SSM Session Manager), auto-scaling enabled.
- All environments share the same Terraform modules but are parameterized via tfvars files.
- Adding a new environment (e.g., "demo") should require only a new tfvars file and GitHub Actions workflow — no module changes.

Networking:
- VPC per environment with public and private subnets across 2 AZs (3 AZs in prod).
- NAT Gateway for outbound from private subnets. Single NAT in dev (cost), HA NAT in prod (reliability).
- Security groups: allow inbound HTTPS (443) to load balancer only. All other inbound blocked. Outbound restricted to known dependencies (database, external APIs) — no unrestricted 0.0.0.0/0 egress in prod.
- VPC Flow Logs enabled in all environments.

Compute:
- ECS Fargate for container orchestration (no EC2 instance management).
- Application Load Balancer (ALB) in front of ECS service.
- Auto-scaling: min 1 / max 2 tasks in dev, min 2 / max 4 in staging, min 3 / max 10 in prod.
- Health checks: ALB health check on /healthz endpoint. ECS task health check with configurable interval.
- Container image from ECR. Image tag is a deployment parameter (not hardcoded).

Database:
- RDS PostgreSQL (or Aurora Serverless v2 in prod if justified — document tradeoff).
- Private subnet only. No public accessibility.
- Automated backups: daily, 7-day retention in dev, 30-day in prod.
- Encryption at rest enabled in all environments.

Observability:
- CloudWatch Logs for ECS task logs. Log retention: 7 days (dev), 30 days (staging), 90 days (prod).
- CloudWatch Metrics + alarms: CPU, memory, request count, error rate, latency p99.
- X-Ray tracing enabled in staging and prod.
- CloudWatch dashboard per environment showing key metrics.

CI/CD pipeline (GitHub Actions):
- On PR: terraform fmt check, terraform validate, terraform plan (output as PR comment), tfsec security scan, infracost cost estimate (comment on PR).
- On merge to main: terraform apply to dev automatically. Staging and prod require manual approval via GitHub Environments with protection rules.
- Environment promotion: dev → staging → prod. Each apply is a separate workflow job with its own credentials and state.
- Plan artifacts: the plan file from the PR check is saved and used for the apply (plan-and-apply consistency — never apply a different plan than what was reviewed).

Access control:
- CI/CD credentials: use GitHub Actions OIDC federation with AWS IAM roles (no long-lived access keys). Each environment has its own IAM role with permissions scoped to that environment's resources only.
- Human access: developers have read-only access to all environments via AWS SSO. Infrastructure approvers have apply permissions for staging/prod only through a break-glass procedure (documented, audit-logged).
- Terraform state: accessible only to the CI/CD role and the two infrastructure approvers. State bucket has versioning enabled for recovery.

Cost controls:
- AWS Budgets: alert at 80% and 100% of monthly budget per environment. Budget: $200/mo dev, $500/mo staging, $3,000/mo prod.
- Cost tagging: all resources tagged with cost-center and environment.
- Infracost on every PR to show cost impact before apply.
- Dev environment auto-destroy: non-essential resources (ECS tasks, NAT Gateway) are scaled to zero outside business hours (8am–6pm weekdays) via scheduled Lambda or EventBridge rules.
- Guardrails: Terraform provider constraints to prevent creation of expensive resource types (e.g., no GPU instances, no provisioned IOPS unless explicitly approved).

Acceptance criteria:
- A new environment can be bootstrapped by adding a tfvars file and a GitHub Actions workflow — no module changes required.
- terraform plan on a clean environment produces zero changes after initial apply (deterministic).
- CI pipeline catches formatting errors, validation failures, security issues, and cost overruns before apply.
- Prod apply requires explicit approval from one of the two infrastructure approvers.
- Drift detection runs daily and alerts on any unplanned changes.
- All resources are tagged; untagged resources are flagged within 24 hours.
- Rotating CI credentials (OIDC) requires no code changes.

Edge cases to explicitly cover:
- Terraform state lock is stuck (previous apply crashed): document how to safely force-unlock.
- A resource was manually created in the console: drift detection flags it; runbook explains import-or-delete decision.
- Terraform provider or module update introduces a breaking change: pin versions, test upgrades in dev first.
- RDS instance requires downtime for a major version upgrade: schedule maintenance window, document the process.
- ECR image referenced in Terraform doesn't exist yet (first deploy chicken-and-egg): document the bootstrap sequence.
- Cost alert fires: document the triage process (identify the resource, scale down, or accept with justification).

Non-goals (explicitly out of scope):
- Application code deployment (CI/CD for the app itself is separate; this is infrastructure only).
- Multi-region deployment (single region for v1).
- Kubernetes (using ECS Fargate, not EKS).
- DNS / domain management (handled separately).

Scope tiers:
- MVP (required): VPC + ECS Fargate + ALB + RDS in dev environment with remote state (S3 + DynamoDB locking) + basic GitHub Actions workflow (plan on PR, apply on merge)
- Core (recommended): + Staging and prod environments via tfvars + OIDC federation (no static keys) + GitHub Environment protection rules (approval gates) + CI pipeline (fmt → validate → plan → tfsec → apply) + cost budgets per environment
- Stretch (optional): + Scheduled drift detection with alerting + Infracost on PRs + dev auto-stop (EventBridge scheduled scaling) + tagging enforcement + security scanning (tfsec/Checkov) + operational runbooks (rollback, drift remediation, secret rotation)
```

**Deliberate ambiguities — decisions that `/speckit.clarify` should surface:**

1. Decision needed: What is the Terraform directory/module structure — flat vs. nested modules, monorepo vs. multi-repo?
2. Decision needed: How is the ECR repository provisioned — same Terraform config or separate bootstrap that runs once?
3. Decision needed: What is the exact OIDC trust policy for GitHub Actions → AWS — scoped to repo + branch, or broader?
4. Decision needed: How are database credentials managed — Secrets Manager with automatic rotation, or manual rotation with a runbook?
5. Decision needed: What monitoring/alerting goes to whom — PagerDuty for prod, Slack for dev/staging, email for budget alerts?
6. Decision needed: How is the Terraform version pinned and upgraded consistently across all environments — tfenv, mise, or CI-enforced constraint?
7. Decision needed: What happens when a module update requires a resource replacement (destroy + create) on a stateful resource in production — auto-approve, or require manual confirmation?
8. Decision needed: How are shared cross-environment resources (ECR repos, IAM policies, OIDC provider) managed — same state file, separate bootstrap state, or per-environment duplication?
9. Decision needed: What is the approval process when `terraform plan` shows resources being destroyed in production — different from normal apply approval?
10. Decision needed: How long is the saved plan artifact valid before it must be regenerated — and what prevents a stale plan from being applied after the infrastructure has changed?

> [!NOTE]
> Reference answers for facilitators are in [`_answers/G-terraform-github-actions-answers.md`](_answers/G-terraform-github-actions-answers.md).

**Checkpoint** — verify the generated spec contains:
- [ ] User stories / operator stories with acceptance criteria
- [ ] `[NEEDS CLARIFICATION]` markers for ambiguities above
- [ ] Environment sizing table (dev/staging/prod)
- [ ] CI/CD pipeline stages defined
- [ ] Cost budgets per environment
- [ ] A review and acceptance checklist
- [ ] MVP / Core / Stretch scope tiers

---

### Clarification

```
/speckit.clarify Review the Terraform + GitHub Actions infrastructure spec and ask me about every ambiguity, unstated assumption, and gap — especially around: Terraform directory structure, ECR bootstrap, OIDC trust policy details, database credential management, alerting destinations, state bucket bootstrap (chicken-and-egg), and any operational gaps you can identify.
```

Review the questions surfaced by Spec Kit. Use the deliberate ambiguity list above as a checklist — did the AI catch all 10? If not, add the missed ones manually.

**Manual refinement:**

```
For the initial deployment: the REST API service is a simple health-check-only container (nginx returning 200 on /healthz). This validates the full infrastructure before the application team deploys their actual service. Include this "placeholder service" in the spec.
```

**Validate the checklist:**

```
Read the review and acceptance checklist in the spec, and check off each item that the specification now satisfies. Leave unchecked any that still need work.
```

**Checkpoint:**
- [ ] No remaining `[NEEDS CLARIFICATION]` markers (or documented decisions for each)
- [ ] Environment parameterization is defined (tfvars, not copy-paste)
- [ ] CI/CD pipeline stages are specified with approval gates
- [ ] OIDC federation is chosen over long-lived keys
- [ ] Cost budgets are concrete per environment
- [ ] Bootstrap sequence is documented (state bucket, ECR, OIDC)
- [ ] All edge cases have defined runbook procedures
- [ ] All 10 deliberate ambiguities have documented resolutions

---

### Plan

```
/speckit.plan Create a technical plan for the Terraform + GitHub Actions infrastructure.

Tech stack:
- Terraform >= 1.6 with AWS provider.
- GitHub Actions for CI/CD. GitHub Environments for protection rules.
- AWS services: VPC, ECS Fargate, ALB, RDS PostgreSQL, ECR, CloudWatch, X-Ray, Secrets Manager, S3 (state), DynamoDB (lock), IAM, AWS Budgets, SNS.
- Security scanning: tfsec (or Checkov) in CI.
- Cost estimation: Infracost in CI.
- State: S3 + DynamoDB lock per environment (separate state files).

The plan must include:
- Terraform module structure: reusable modules for networking (VPC, subnets, NAT, security groups), compute (ECS, ALB, auto-scaling), database (RDS, Secrets Manager), observability (CloudWatch, X-Ray, dashboards), and cost-controls (budgets, tagging). Environment directories consume modules with tfvars.
- Bootstrap sequence: state bucket + lock table + OIDC provider + ECR repo. Applied once manually with local state. Document the exact steps.
- Remote state configuration: S3 backend with DynamoDB locking. Separate state file per environment. State bucket versioning enabled for recovery. State access restricted via bucket policy.
- CI pipeline design: PR workflow (fmt → validate → tfsec → plan → infracost → comment on PR). Apply workflow (triggered on merge to main → apply dev auto → staging manual approval → prod manual approval). Plan file is passed as an artifact from plan step to apply step for consistency.
- GitHub Environments: dev (no protection), staging (require 1 reviewer), prod (require 1 of 2 designated approvers + wait timer of 5 minutes).
- OIDC federation: GitHub Actions assumes AWS IAM role per environment. Role trust policy scoped to repo + branch. Role permissions scoped to environment-specific resources via resource tags.
- Secret management: no secrets in code or state. RDS passwords via Secrets Manager with automatic rotation. CI credentials via OIDC (no stored keys). Application secrets via Secrets Manager referenced by ECS task definition.
- Drift detection: scheduled GitHub Actions workflow (daily) runs terraform plan per environment and alerts on non-zero changes. Runbook for common drift scenarios.
- Tagging enforcement: default_tags in AWS provider config. tag-policy guardrail via AWS Organizations (or tfsec rule) to flag untagged resources.
- Cost controls: AWS Budgets per environment, infracost on every PR, dev environment auto-stop (EventBridge scheduled rule), provider constraints (disallow expensive instance types).
- Rollback strategy: for stateless resources (ECS tasks, ALB rules), re-apply previous commit. For stateful resources (RDS), document the manual rollback process (point-in-time recovery). For networking changes, warn about potential downtime.
- Documentation deliverables: Getting Started runbook (bootstrap + first deploy), Operational Playbook (apply, rollback, drift remediation, secret rotation, cost triage), Architecture Decision Records (ADRs) for key choices (ECS vs EKS, Aurora vs RDS, OIDC vs static keys).
- Testing: plan validation in CI, tfsec/checkov security scanning, infracost threshold check (fail PR if cost increase > $500/mo), post-apply smoke test (curl /healthz on the ALB), and a monthly disaster recovery drill document.
```

**Expected artifacts:**

| File | Purpose |
|---|---|
| `plan.md` | Module structure, CI pipeline, rollback strategy |
| `data-model.md` | Resource inventory per environment, tagging schema, state file layout |
| `research.md` | ECS vs EKS, Aurora vs RDS, OIDC federation setup, tfsec vs Checkov |
| `contracts/` | CI workflow definitions (YAML structure), module input/output interfaces |
| `quickstart.md` | Bootstrap sequence and first-deploy steps |

**Validate the plan:**

```
Review the implementation plan and check: (1) Can a new environment be added with only a tfvars file and workflow — no module changes? (2) Is the blast radius of a single apply limited to one environment? (3) Does the CI pipeline prevent applying a plan that wasn't reviewed? (4) Is there a clear rollback procedure for both stateless and stateful resources?
```

**Checkpoint:**
- [ ] Module structure is reusable (networking, compute, database, observability, cost-controls)
- [ ] Bootstrap sequence is documented and separated from ongoing operations
- [ ] CI pipeline enforces plan-then-apply with artifact passing
- [ ] GitHub Environments have appropriate protection rules per environment
- [ ] OIDC is used instead of static credentials
- [ ] Drift detection is scheduled with alerting
- [ ] Rollback is documented per resource type (stateless vs stateful)
- [ ] Cost controls include both preventive (guardrails) and detective (budgets/infracost)

---

### Tasks

```
/speckit.tasks Break down the infrastructure work into tasks.

Task preferences:
- Start with bootstrap (state bucket, lock table, OIDC provider, ECR) — this unblocks everything else.
- Then build modules environment-agnostic (networking → compute → database → observability → cost-controls).
- Then set up the CI pipeline early (so every subsequent change is validated automatically).
- Then instantiate dev environment first (fastest feedback loop).
- Then staging, then prod (each with its own tfvars and workflow).
- Include separate tasks for: drift detection setup, tagging enforcement, dev auto-stop scheduling, cost budget alerts, security scanning configuration, and post-apply smoke tests.
- Include documentation tasks: Getting Started runbook, Operational Playbook (apply, rollback, drift remediation, secret rotation, cost triage), and Architecture Decision Records.
- Include a security review task: validate IAM policies follow least privilege, verify no public accessibility for database, verify security group rules.
- Each task must have a "done when" check (e.g., "done when terraform plan on dev shows 0 changes after apply").
```

**What to observe in `tasks.md`:**
- Bootstrap is the very first task (unblocks state, OIDC, ECR)
- Modules are built before environment instantiation
- CI pipeline is set up early (not at the end)
- Dev is instantiated first, then staging, then prod
- Security review and cost validation are explicit tasks, not afterthoughts
- Documentation tasks exist alongside implementation tasks
- Each task has a concrete "done when" check

---

### Analyze (Optional)

```
/speckit.analyze
```

> [!TIP]
> Run `/speckit.analyze` after tasks to check cross-artifact consistency. It validates that every spec requirement has a corresponding task, and every task traces back to the spec. Particularly valuable for infrastructure projects where a missed security group rule or IAM policy gap becomes a production security incident.

---

### Implement

```
/speckit.implement Execute all tasks in order. After completing the bootstrap and CI pipeline, verify that the CI pipeline catches a deliberate formatting error before proceeding. After applying to dev, run the smoke test (curl /healthz) before building staging and prod.
```

**What to watch for:**
- The AI follows the task order from `tasks.md`
- Bootstrap creates state bucket + lock table + OIDC provider + ECR
- Modules use variables and outputs (not hardcoded values)
- CI pipeline comments the plan on the PR (not just logs it)
- Dev environment apply is automatic; staging and prod require approval
- Security groups don't have 0.0.0.0/0 egress in prod
- All resources are tagged
- RDS password is not stored in Terraform state
- No long-lived AWS access keys appear anywhere

---

## Extension Activities

### Add a Feature: Multi-Region Disaster Recovery

Extend the infrastructure for regional failover:

```
/speckit.specify Add multi-region disaster recovery to the prod environment. Deploy a standby RDS read replica and ECS service in a secondary AWS region (us-west-2, primary is us-east-1). Use Route 53 health-check-based failover for DNS routing. Define RPO (Recovery Point Objective) and RTO (Recovery Time Objective) targets. Active-passive: the secondary region only receives traffic during failover. Consider: how does Terraform manage resources across two regions? How does the state file structure change? How is failover triggered and tested?
```

Then continue through `/speckit.clarify`, `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement`.

### Stress-test the Spec: Emergency Production Hotfix

Simulate an urgent production change that bypasses the normal workflow:

```
A critical production issue requires an immediate security group change (block a specific IP range that is actively attacking the service). The normal PR → review → approve → apply cycle takes too long. Update the spec to define a "break-glass" emergency change procedure. Consider: who is authorized? How is the change made (Terraform still, or manual + import)? What audit trail is required? How is the change reconciled back into the codebase? What prevents abuse of the break-glass procedure?
```

This demonstrates how SDD handles operational governance — the spec must define not just the happy path but the emergency procedures that prevent ad-hoc firefighting from becoming technical debt.
