# Project Research Summary

**Project:** Smart WTP
**Domain:** Smart water treatment plant monitoring and control backend
**Researched:** 2026-03-31
**Confidence:** MEDIUM

## Executive Summary

Smart WTP is not a generic SaaS dashboard. It is an industrial operations backend that has to ingest OT telemetry, maintain operator-grade read models, surface alarms and history, present ML recommendations, and execute plant control with auditability and mode-aware safety. The research consistently points to a conservative architecture: Java 21, Spring Boot 4, PostgreSQL, Kafka-backed async processing, synchronous REST for operator intent, and a strict split between `common`, `api`, and `scheduler`.

The recommended approach is to build the platform in the same order experts build control-adjacent systems: define the plant contract and safety envelope first, then land trustworthy telemetry, materialize current state and history, add alarm and workflow foundations, prove manual command orchestration, and only then expose ML recommendations. Automatic AI control is not a launch feature. It should be enabled only after the manual command path, observability, change control, and site-specific safety constraints are proven in production-like conditions.

The dominant risks are control-path drift and false trust: AI bypassing hard constraints, manual and AI modes leaking into each other, raw telemetry being treated as truth, alarm floods overwhelming operators, and missing forensic evidence when something goes wrong. The mitigation pattern is consistent across the research: authoritative server-side mode state, quality-scored telemetry contracts, transactional intent capture with async dispatch, one audited command pipeline for both manual and AI sources, and OT-specific security boundaries that treat remote actuation as high risk.

## Key Findings

### Recommended Stack

Detailed stack guidance is in [STACK.md](./STACK.md). The research strongly favors a deliberately boring stack because auditability, restartability, and operational clarity matter more than framework novelty in this domain. The non-negotiable guardrails are as important as the tooling choices: `common` stays a shared-kernel contract jar only, `api` stays the synchronous operator edge, and `scheduler` owns ingest, Kafka consumers, batch jobs, outbox publishing, read-model updates, and device dispatch. JPA owns write-side aggregates, MyBatis owns read-heavy and bulk SQL paths, and neither should become a second write path for the other.

**Core technologies:**
- Java 21 + Spring Boot 4.0.5: stable servlet-based runtime for `api` and `scheduler`, aligned with JPA, MyBatis, Spring Kafka, and Spring Batch.
- PostgreSQL 17.x preferred: single system of record for commands, alarms, history, outbox, and batch metadata in v1.
- Spring Data JPA / Hibernate 7.x: write-side ownership for commands, configuration, thresholds, users, and other transactional aggregates.
- MyBatis Spring Boot Starter 4.0.0: SQL-first read path for dashboards, history, aggregates, reporting, and bulk telemetry workflows.
- Spring for Apache Kafka 4.0.x: decoupled ingest, ML result flow, integration events, and command/result messaging.
- Spring Batch 6.0.x: restartable aggregation, reconciliation, retention, and scheduled offline jobs in `scheduler`.
- Flyway + Actuator + Micrometer + OpenTelemetry: mandatory migration, health, metrics, and trace foundations from day one.

**Module and integration guardrails:**
- `common` contains shared DTOs, enums, error codes, and contracts only. No repositories, listeners, schedulers, or feature business logic.
- `api` accepts operator requests, validates input, persists command intent and outbox records, and serves read APIs. It does not dispatch directly to PLCs or own long-running work.
- `scheduler` owns Kafka consumption, read-model materialization, alarms, ML ingestion, outbox publishing, retries, reconciliation, and all device command dispatch.
- Use PostgreSQL outbox plus idempotent consumers. Do not try to make PostgreSQL and Kafka one atomic transaction.
- Publish Kafka messages and dispatch control from `scheduler`, not directly from controllers.
- Avoid WebFlux/R2DBC, Redis, Quartz, TimescaleDB, extra persistence abstractions, and direct API-to-device control in v1.

### Expected Features

Detailed feature analysis is in [FEATURES.md](./FEATURES.md). The v1 line is clear: operators need a credible operations platform before they will trust optimization or autonomy. That means live visibility, history, alarms, safe manual action, and continuity workflows. ML earns its place in v1 only as visible recommendations and predictions, not as authority to move equipment.

**Must have (table stakes for v1):**
- Real-time plant and asset monitoring with canonical asset and tag hierarchy.
- Alarm and event management with acknowledgement, prioritization, and historical journal.
- Historian, trends, and operational reporting for troubleshooting and compliance evidence.
- Secure manual control with server-enforced mode awareness, confirmation, and full audit trail.
- Shift logbook and handover for 24/7 operations continuity.
- Browser-based field inspection capture with maintenance handoff, not full CMMS replacement.
- ML result visibility and recommendation display so operators can compare predictions to real plant state.

**Should have after core validation (v1.x):**
- Guardrailed AI automatic control for selected loops or units only.
- Sensor-health and data-quality analytics to improve trust in alarms, trends, and recommendations.
- Guided procedures and contextual work instructions tied to alarms, assets, and modes.
- Tighter CMMS integration once handoff volume justifies it.

**Defer beyond v1:**
- What-if simulation and digital-twin optimization.
- Multi-site benchmarking or fleet operations center features.
- Native mobile and offline-first field workflows.
- Rich 3D or AR views.
- Full CMMS, ERP, LIMS, or GIS replacement.
- Unrestricted remote control from broad browser or network access.
- Black-box plant-wide AI autonomy.

### Architecture Approach

Detailed architecture guidance is in [ARCHITECTURE.md](./ARCHITECTURE.md). The recommended design is an immutable-telemetry plus mutable-read-model architecture. Raw telemetry lands through edge and Kafka integration into PostgreSQL history tables. `scheduler` then materializes fast current-state tables, aggregates history, evaluates alarms, ingests ML results, and runs the control pipeline. `api` reads from current-state and aggregate tables and writes only operator intent, acknowledgements, and mode changes.

**Major components:**
1. Asset and point registry: canonical plant, asset, tag, unit, alarm, and control-mode metadata that every downstream feature depends on.
2. Edge and event backbone: protocol adapters plus Kafka topics for telemetry, ML results, control requests, and control results.
3. Scheduler runtime: normalization, quality checks, materialized read models, aggregation, alarm lifecycle, ML ingestion, policy checks, dispatch, and reconciliation.
4. PostgreSQL core: master data, telemetry history, current state, aggregates, alarms, commands, audit, outbox, and batch metadata.
5. API runtime: authenticated dashboards, history queries, alarm acknowledgement, ML result reads, manual command intake, and mode/status endpoints.

**Key patterns to follow:**
- Persist immutable telemetry separately from dashboard-oriented current-state and aggregate tables.
- Use one command schema and one audited execution pipeline for both manual and AI intent sources.
- Capture command intent transactionally in `api`, then dispatch asynchronously from `scheduler`.
- Keep deterministic or safety-critical control loops at PLC or edge level; the backend issues bounded supervisory commands only.

### Critical Pitfalls

The full risk catalog is in [PITFALLS.md](./PITFALLS.md). These are the pitfalls that must actively shape roadmap sequencing, not just implementation details.

1. **AI bypassing the safety envelope:** never map model output directly to a device command; require independent safe-range, interlock, cooldown, and fallback checks before any actuation.
2. **Mode leakage between AI, manual, and maintenance:** model control mode as an authoritative backend state machine with explicit transitions, permissions, and audit events.
3. **Treating raw telemetry as trustworthy evidence:** define units, ranges, timestamps, quality bits, staleness rules, and quarantine logic before telemetry drives alarms, ML, or control.
4. **Alarm spam replacing alarm management:** separate alarms from events and diagnostics, rationalize priorities and operator actions, and track flood and standing-alarm KPIs early.
5. **Missing end-to-end observability and forensics:** every recommendation, approval, command, acknowledgement, reject, and plant response needs shared correlation IDs and replayable evidence.
6. **Treating OT control paths like normal web access:** remote visibility is lower risk than remote actuation; production rollout needs zoning, DMZ boundaries, strong identity, and explicit remote-control restrictions.

## Implications for Roadmap

Based on the combined research, the roadmap should treat v1 as a safe operator platform, not as an autonomy project. Build order has to follow dependency order and control-risk order.

### Phase 1: Plant Contract and Safety Envelope

**Rationale:** Every downstream feature depends on canonical plant IDs, tag mappings, units, quality semantics, and safe operating constraints. If this contract is loose, dashboards, alarms, ML, and control all become untrustworthy.
**Delivers:** Shared `common` contracts, asset and point registry, engineering units, quality flags, safe ranges, initial interlock metadata, Flyway baseline schema, and architecture tests that lock module boundaries.
**Addresses:** Telemetry collection foundation, real-time monitoring foundation, control-safety baseline.
**Avoids:** AI bypassing hard constraints, telemetry-quality corruption, `common` becoming a dumping ground.

### Phase 2: Telemetry Backbone, Current State, and History

**Rationale:** The first user-visible slice should come from a reliable telemetry-to-read-model loop, not from querying raw streams ad hoc.
**Delivers:** Kafka topics and consumers, telemetry normalization, raw history persistence, `asset_current_state`, rollups and retention jobs, dashboard endpoints, trend/history APIs, and baseline reporting queries.
**Uses:** PostgreSQL partitioning, MyBatis read models, Spring Kafka, Spring Batch, Actuator, and observability hooks.
**Implements:** Ingestion pipeline, materialized read models, historian, and reporting substrate.
**Addresses:** Real-time monitoring, historian, trends, and operational reporting.
**Avoids:** ORM-heavy ingest bottlenecks, raw-table dashboard queries, premature extra storage systems.

### Phase 3: Alarming and Operator Workflow

**Rationale:** Operators need actionable abnormal-state handling and shift continuity before they will trust optimization or remote workflows.
**Delivers:** Alarm lifecycle engine, acknowledgement APIs, alarm journal, flood metrics, shift logbook, handover workflow, and browser-based field inspection capture with maintenance handoff records.
**Addresses:** Alarm and event management, shift handover, field inspection workflow, richer reporting context.
**Avoids:** Alarm spam, mixed alarm/event UX, paper or spreadsheet handoff gaps.

### Phase 4: Manual Control, Mode Orchestration, and Audit

**Rationale:** Safe manual control has to exist and be proven before any automatic AI actuation is even considered.
**Delivers:** Authoritative server-side mode state machine, command intent capture, outbox records, async dispatch via `scheduler`, PLC ack/nack handling, command status views, and immutable audit history.
**Uses:** JPA for command and mode writes, PostgreSQL outbox, Kafka or async integration events, and scheduler-owned dispatch and reconciliation.
**Implements:** Single command pipeline for manual commands and future AI commands.
**Addresses:** Secure manual control with mode awareness and auditability.
**Avoids:** Direct API-to-PLC control, mode leakage, unsafe retries, and command ownership drift.

### Phase 5: ML Advisory, Forensics, and Rollout Hardening

**Rationale:** v1 should validate ML value without granting control authority. At the same time, rollout needs enough observability and security hardening to support incident reconstruction and safe commissioning.
**Delivers:** ML result ingestion, recommendation display with confidence and model version, shared correlation IDs across telemetry and command flows, decision and command traces, OT access-path review, and production readiness checks for remote visibility and control restrictions.
**Addresses:** ML result visibility, operator trust, incident forensics, and pre-launch hardening.
**Avoids:** Treating ML output as a command, missing forensic evidence, uncontrolled remote-access exposure.

### Phase 6: Post-v1 Guardrailed Auto Control and Change Governance

**Rationale:** Automatic AI control is a post-v1 capability because it depends on stable telemetry quality, proven manual dispatch, trusted alarms, audited ML outputs, and formal change control.
**Delivers:** Shadow mode, replay validation, kill switch, bounded auto-actuation for selected units, drift monitoring, versioned model and config release flow, and rollback evidence.
**Addresses:** Guardrailed AI automatic control, sensor-health analytics, and model-governance workflows.
**Avoids:** Black-box autonomy, unsafe config changes, and plant-wide auto-control rollout before evidence exists.

### Phase Ordering Rationale

- Canonical asset, tag, and safety metadata must exist before ingest, alarms, ML attribution, or control auditing can be correct.
- Telemetry, current state, and history come before alarms and operator workflows because those workflows depend on trustworthy state and history.
- Alarm lifecycle must precede AI actuation because alarms and abnormal-state handling are part of the operator trust model and future policy gating.
- Manual control must ship before auto control so the physical command path, acknowledgements, retries, and audit trail are already proven with a human in the loop.
- ML should enter as recommendation-first. The same researched evidence argues against broad autonomous control in v1.
- OT security and commissioning constraints are cross-cutting from phase 1, but they still need a dedicated hardening gate before production rollout.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 1:** Site-specific tag registry, unit normalization, safe envelopes, and interlock ownership are plant-specific and need direct domain validation.
- **Phase 4:** Control dispatch, PLC or OPC UA integration, latency budgets, ack semantics, and degraded-mode behavior need implementation-phase research.
- **Phase 5:** ML inference contract, recommendation UX, OT remote-access model, and evidence retention policies need focused design work.
- **Phase 6:** Auto-control gating, replay tooling, drift thresholds, and management-of-change workflow need dedicated research before execution.

Phases with standard patterns (can likely skip `research-phase`):
- **Phase 2:** Spring Boot + Kafka + PostgreSQL ingestion, read-model materialization, Flyway migrations, and MyBatis query APIs are well-documented patterns.
- **Phase 3:** Logbook, handover, reporting, and browser-based inspection CRUD are standard once the domain schema and alarm philosophy are defined.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Based mostly on official Spring, PostgreSQL, MyBatis, and Testcontainers documentation, with clear fit to the module constraints in this project. |
| Features | MEDIUM | Table stakes are clear from industrial competitors and standards, but exact workflow scope still depends on site needs and operator adoption. |
| Architecture | MEDIUM | Strongly supported by industrial IoT and platform patterns, but exact edge-integration and deployment topology are still project-specific. |
| Pitfalls | HIGH | Grounded in official OT security, alarm-management, and AI governance guidance, with direct relevance to water and wastewater operations. |

**Overall confidence:** MEDIUM

### Gaps to Address

- **Edge integration choice:** confirm whether plant connectivity is OPC UA, vendor gateway, direct PLC integration, or a mixed model before planning command dispatch details.
- **Telemetry volume and retention targets:** validate sample rates, retention windows, and reporting expectations to confirm PostgreSQL partitioning and aggregation strategy.
- **Identity and OT network model:** confirm external IdP, remote access paths, zone and DMZ boundaries, and whether any remote actuation is allowed in v1.
- **Alarm philosophy and operating envelopes:** define per-asset priorities, operator actions, suppression rules, and safe command envelopes with plant stakeholders.
- **ML contract and ownership:** define inference schema, confidence and explanation fields, recommendation approval rules, and who approves model and config changes.

## Sources

### Primary (HIGH confidence)
- Project context: [PROJECT.md](../PROJECT.md)
- Spring Boot, Spring Security, Spring Kafka, Spring Batch, MyBatis, Flyway, PostgreSQL, and Testcontainers official documentation used in [STACK.md](./STACK.md)
- NIST SP 800-82 Rev. 3 and NIST AI RMF resources used in [PITFALLS.md](./PITFALLS.md)
- CISA OT security and water-sector advisories used in [FEATURES.md](./FEATURES.md) and [PITFALLS.md](./PITFALLS.md)
- ISA-18 and ISA-101 references used for alarm-management and HMI/operator workflow framing

### Secondary (MEDIUM confidence)
- Microsoft Azure IIoT and OPC UA architecture references used in [ARCHITECTURE.md](./ARCHITECTURE.md)
- AWS IoT SiteWise architectural references used in [ARCHITECTURE.md](./ARCHITECTURE.md)
- Rockwell, Ignition, AVEVA, Hexagon, and Xylem product materials used in [FEATURES.md](./FEATURES.md) to identify category table stakes and differentiators

### Tertiary (LOW confidence)
- None relied on directly for roadmap-critical conclusions

---
*Research completed: 2026-03-31*
*Ready for roadmap: yes*
