---
title: Scholarships Data Product Charter
status: local-source-pilot
created: 2026-08-08
updated: 2026-08-08
tags: [template, data-engineering, data-product, governance]
description: Outcome, consumers, ownership, contract, quality, privacy, and operating boundary for a data product.
---

# Data Product Charter

## Document control

| Field | Value |
|---|---|
| Data product ID/version | book-scholarship-data / scholarship.v1 demo and scholarship.v2 source pilot |
| Product owner | bookchaowalit |
| Data owner/steward | bookchaowalit |
| Producer team | Domain repository |
| Status/review date | Local source pilot / 2026-09-07 |
| Evidence boundary | schema.json, schema-v2.json, demo.json, source policies, capture adapter and tests in this repository |

## Product contract

- Decision or user outcome: Find education funding by degree and applicant eligibility.
- Consumers and use cases: Discovery applications; integration planned.
- Source systems and lake layers: Chevening Thailand and four GOV.UK Content API pages (undergraduate finance, 16-19 bursary, free courses for jobs, university scholarships) → landing → Bronze through the shared local runtime; synthetic fixtures remain for offline contract tests.
- In scope/out of scope: Degree and tuition awards; research project budgets belong to grant.
- Freshness, availability, and volume expectation: Target source review every 24h; open filter rejects checks older than 72h; no live SLA.
- Data classification, residency, retention, and access: Public program metadata and synthetic fixtures; no user profile; raw source bytes stay in the private local operational archive with no automatic deletion, per each source policy.
- Quality thresholds and incident route: All contract tests pass; live quality/replay gates pending; owner handles source failures.
- Cost/capacity guardrail: Offline only, zero provider calls; max 10,000 records per envelope.
- Versioning, deprecation, and migration policy: Draft v1; breaking changes version separately; no legacy migration or live consumer yet.

## Acceptance and ownership

| Gate | Evidence | Owner | Result/status |
|---|---|---|---|
| Contract | Versioned schema and compatibility rules |  |  |
| Quality | Checks and threshold report |  |  |
| Lineage | Source-to-consumer map |  |  |
| Access/privacy | Classification and access review |  |  |
| Operations | Runbook, alert, replay, and recovery |  |  |

## Approval

| Role | Name/date | Decision |
|---|---|---|
| Product/data owner |  | Approve charter / revise |
| Producer owner |  | Accept delivery boundary |
| Consumer representative |  | Accept use and SLA |
