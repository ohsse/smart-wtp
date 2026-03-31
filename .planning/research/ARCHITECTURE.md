# Architecture Research

**Domain:** Smart water treatment plant operations platform
**Researched:** 2026-03-31
**Confidence:** MEDIUM

**Note:** The component split is grounded in current industrial IoT, alarm-management, Kafka, PostgreSQL, and Spring guidance. The exact build order is an inference from those dependencies and from this project's `common` / `api` / `scheduler` constraints.

## Standard Architecture

### System Overview

```text
+---------------------------- Operator Web UI -----------------------------+
| Real-time dashboard | history/charts | alarms | ML results | control UI |
+----------------------------------+--------------------------------------+
                                   |
                                   v
+------------------------------- API Runtime ------------------------------+
| Auth | query endpoints | dashboard reads | alarm/history reads           |
| ML result reads | manual command intake | mode changes | status polling  |
+-------------------+----------------------+-------------------------------+
                    | SQL reads / transactional writes
                    v
+---------------------------- PostgreSQL Core -----------------------------+
| asset/point registry | control mode state | telemetry_raw                |
| asset_current_state  | agg_1m / agg_1h    | alarm_state / alarm_event    |
| ml_result            | command_request    | command_execution | audit     |
| outbox               | scheduler metadata | user acknowledgements         |
+----------^------------------^-------------------^------------------------+
           |                  |                   |
           | writes / reads   | batch refresh     | command/audit updates
           |                  |                   |
+---------------------------- Scheduler Runtime ---------------------------+
| Kafka consumers | telemetry normalization | current-state materializer   |
| aggregation jobs | alarm evaluator | ML result ingester                 |
| AI decision engine | policy/interlock gate | command dispatcher          |
| retries/reconciliation | notification hooks | scheduled maintenance jobs  |
+-----------^--------------------^---------------------^-------------------+
            |                    |                     |
            | telemetry          | ML outputs          | command ack/nack
            v                    v                     |
+-------------------------- Integration Layer -----------------------------+
| Edge/site gateway | OPC UA / PLC adapters | protocol mapping            |
| Python ML producer | command transport | health/status monitoring       |
+----------------------------^-----------------------------^---------------+
                             |                             |
                             +------ plant sensors / PLCs -+
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Asset and point registry | Own the canonical plant, process, asset, and point hierarchy plus tag mappings, engineering units, control modes, and alarm definitions. | PostgreSQL master tables, shared IDs/enums in `common`, admin CRUD later. |
| Edge connectivity layer | Speak plant protocols, normalize raw tags into canonical identifiers, and execute writes close to the PLC boundary. | OPC UA or vendor-specific adapters at the site edge; command acknowledgement channel back to Kafka or DB. |
| Event backbone | Decouple ingestion, ML, alarms, and control so API latency is not tied to background work. | Kafka topics keyed by plant or asset (`telemetry.raw`, `telemetry.normalized`, `ml.result`, `control.requested`, `control.result`). |
| Ingestion and normalization workers | Validate telemetry quality, enrich with asset context, persist immutable raw samples, and emit normalized events. | `scheduler` Kafka consumers and idempotent writers. |
| Operational read-model materializer | Maintain fast latest-state tables for dashboard and control screens. | `scheduler` upserts into `asset_current_state` and related status tables. |
| Aggregation and history pipeline | Build minute/hour rollups and query-optimized history views without forcing UI queries over raw telemetry. | Scheduled jobs, stream processors, PostgreSQL partitioned tables, optional materialized views. |
| Alarm lifecycle engine | Evaluate alarm rules, manage active vs cleared state, record acknowledgement history, and prevent alarm floods from becoming just another notification list. | `scheduler` evaluators plus `alarm_state` and `alarm_event` tables. |
| ML result ingestion | Accept Python model output, validate timestamp and asset alignment, store confidence and model version, and expose results to operators. | Kafka or landing-table ingestion in `scheduler`, persisted to `ml_result`. |
| Control orchestration | Validate command intent, enforce AI/manual mode, run policy and interlock checks, dispatch to edge adapters, and persist execution outcomes. | `api` for command intake, `scheduler` for policy gate, dispatch, retry, and reconciliation. |
| Query API | Serve dashboards, charts, alarm/history screens, ML result views, mode status, and command execution status. | Spring Boot app in `api`, MyBatis-heavy reads, JPA for transactional writes. |

## Recommended Project Structure

```text
smart-wtp/
|-- common/
|   `-- src/main/java/.../
|       |-- asset/       # asset, plant, point, topology contracts
|       |-- telemetry/   # telemetry events, quality, units, DTOs
|       |-- alarm/       # alarm definitions, state enums, DTOs
|       |-- ml/          # ML result and recommendation contracts
|       |-- control/     # mode, command, result, policy contracts
|       `-- shared/      # errors, response models, utilities
|-- api/
|   `-- src/main/java/.../
|       |-- dashboard/   # real-time read endpoints
|       |-- history/     # chart/history query endpoints
|       |-- alarm/       # alarm read + acknowledgement endpoints
|       |-- ml/          # prediction/result endpoints
|       |-- control/     # manual command intake, mode changes, status
|       |-- query/       # MyBatis mappers and query services
|       `-- config/      # web, security, serialization, API wiring
`-- scheduler/
    `-- src/main/java/.../
        |-- ingest/      # Kafka consumers, protocol payload normalization
        |-- materialize/ # current-state upserts
        |-- aggregate/   # rollups, retention, refresh jobs
        |-- alarm/       # rule evaluation and lifecycle processing
        |-- ml/          # ML result ingestion and recommendation staging
        |-- control/     # policy gate, dispatch, retries, reconciliation
        |-- integration/ # Kafka, edge adapter clients, command result intake
        `-- jobs/        # scheduled jobs, batch runners, maintenance
```

### Structure Rationale

- **`common/`:** No runtime responsibilities. It is the canonical contract jar for shared domain models, events, enums, validation rules, and errors. Treat it as the source of truth for plant IDs, point IDs, alarm types, control modes, and command/result schemas.
- **`api/`:** The synchronous application boundary. It owns REST, authentication, operator-facing reads, manual command submission, acknowledgements, and mode changes. It should not run ingestion consumers, heavy aggregation, or direct PLC dispatch.
- **`scheduler/`:** The asynchronous and control pipeline boundary. It owns Kafka consumption, normalization, materialized read models, alarms, ML result ingestion, and all device command dispatch. This keeps long-running work and failure handling out of the REST runtime.

### Module to Runtime Mapping

| Module | Deployable | Runtime Responsibility |
|--------|------------|------------------------|
| `common` | No | Shared contracts only. No background jobs, no controllers, no direct infrastructure ownership. |
| `api` | Yes | Request-response reads, manual writes that create intent records, acknowledgement endpoints, mode changes, status retrieval, user-facing validation. |
| `scheduler` | Yes | Background ingestion, batch jobs, Kafka processing, read-model materialization, alarm evaluation, ML ingestion, command policy checks, PLC dispatch, retry and audit completion. |

## Architectural Patterns

### Pattern 1: Immutable Telemetry Event + Mutable Read Model

**What:** Persist immutable telemetry/history separately from dashboard-oriented current-state and aggregate tables.
**When to use:** Always. Real-time dashboards, historical charts, and control screens have different latency and query-shape needs.
**Trade-offs:** You duplicate data intentionally and accept eventual consistency between raw telemetry and UI read models. In return, operator reads stay fast and predictable.

**Example:**
```java
public record TelemetrySample(
    String plantId,
    String assetId,
    String pointId,
    Instant observedAt,
    BigDecimal value,
    QualityCode quality,
    String sourceProtocol
) {}
```

### Pattern 2: One Command Pipeline, Two Intent Sources

**What:** Manual and AI-originated commands share the same request, validation, dispatch, and audit path. The only difference is who created the intent.
**When to use:** Always for mixed AI/manual operations. Separate executors drift and create safety holes.
**Trade-offs:** Slightly more up-front modeling, but much safer and easier to audit than parallel code paths.

**Example:**
```java
public enum ControlSource { MANUAL, AI }
public enum ControlMode { MANUAL, AI }

public record ControlCommandRequest(
    UUID requestId,
    String plantId,
    String assetId,
    String pointId,
    ControlSource source,
    ControlMode expectedMode,
    String commandType,
    String payloadJson,
    Instant requestedAt
) {}
```

### Pattern 3: Transactional Intent Capture, Async Dispatch

**What:** The API stores the operator's command request and an outbox record in one transaction. The scheduler later dispatches the command and records the physical result.
**When to use:** Any time the action leaves the REST process and must survive retries, PLC downtime, or broker restarts.
**Trade-offs:** The initial API response is usually "accepted" rather than "completed". That is the correct trade for reliable plant-side execution.

**Example:**
```java
@Transactional
public UUID submitManualCommand(ManualCommandDto dto, UserPrincipal user) {
    var request = commandRequestRepository.save(
        ControlCommandRequestEntity.manual(dto, user.userId())
    );
    outboxRepository.save(
        OutboxEvent.controlRequested(request.getRequestId())
    );
    return request.getRequestId();
}
```

## Data Flow

### Online Request Flow

```text
Operator UI
  -> API controller
  -> query service / command service

Read path:
  -> MyBatis query
  -> asset_current_state / agg_* / alarm_* / ml_result
  -> DTO response
  -> Operator UI

Write path (manual control or alarm acknowledgement):
  -> JPA transaction
  -> command_request / acknowledgement / outbox
  -> HTTP 202 or 200 with tracking ID
```

### Background Processing Flow

```text
Sensors / PLCs
  -> edge gateway / adapter
  -> Kafka telemetry.raw
  -> scheduler.ingest normalize + validate
  -> telemetry_raw
  -> scheduler.materialize upsert current state
  -> asset_current_state
  -> scheduler.aggregate rollups
  -> agg_1m / agg_1h / history views
  -> scheduler.alarm evaluate lifecycle
  -> alarm_state / alarm_event
  -> API reads for dashboard, history, and alarms
```

### ML Result Flow

```text
Python ML job / service
  -> Kafka ml.result or controlled landing table
  -> scheduler.ml ingest + validation
  -> ml_result (+ recommendation metadata, confidence, model version)
  -> API read endpoints
  -> UI renders advisory result or recommended action
```

### Control Pipeline

```text
Manual mode:
Operator UI
  -> API command intake
  -> command_request(source=MANUAL) + outbox
  -> scheduler.control policy gate
  -> edge command adapter
  -> PLC write
  -> command_result ack/nack
  -> command_execution + audit
  -> API status endpoint / push update

AI mode:
telemetry + alarm state + ml_result
  -> scheduler.decision engine
  -> command_request(source=AI)
  -> same policy gate
  -> same edge adapter
  -> same command_execution + audit path
```

### Key Data Flows

1. **Ingestion:** OT protocols become canonical telemetry events before they touch dashboard queries, alarm logic, or ML presentation.
2. **Operational reads:** The API reads from current-state and aggregate tables, not from raw telemetry streams.
3. **Alarm lifecycle:** Normalized telemetry drives alarm state transitions, acknowledgement tracking, and alarm history independently from UI refresh timing.
4. **ML presentation:** Python outputs are stored as versioned, timestamped result records and shown to users as read-only information unless promoted into the AI decision pipeline.
5. **Manual control:** The operator creates intent through the API, but actual dispatch is asynchronous and always audited.
6. **AI control:** AI mode produces intents automatically, but the downstream executor is identical to manual mode and still enforces policy, interlocks, dedupe, and cooldown rules.

## Suggested Build Order

**This order is an inference from runtime dependencies.** Every later step assumes the earlier ones already exist and are trustworthy.

1. **Asset context and shared contracts**
   - Build plant, asset, point, alarm-definition, control-mode, and command/result schemas in `common`.
   - Create PostgreSQL master tables for topology, tag mappings, and control mode state.
   - Why first: ingestion, alarms, ML attribution, and control auditing all need canonical IDs.

2. **Telemetry ingestion backbone**
   - Stand up Kafka topics, edge-to-platform mappings, scheduler consumers, normalization, and raw telemetry persistence.
   - Why second: everything operator-facing depends on trustworthy telemetry landing correctly.

3. **Current-state materialization and dashboard reads**
   - Maintain `asset_current_state` and expose real-time dashboard endpoints from `api`.
   - Why third: this is the first operator-valuable slice and becomes the base for control screens.

4. **Aggregation and history pipeline**
   - Add minute/hour rollups, retention policies, and chart/history endpoints.
   - Why now: charts and trend views depend on stable raw ingestion but not yet on alarms or control.

5. **Alarm lifecycle and acknowledgement**
   - Evaluate alarm rules, store active and cleared history, and add acknowledgement endpoints.
   - Why before control: operators need trusted abnormal-state visibility before automated decisions are allowed to act.

6. **ML result ingestion and presentation**
   - Ingest Python outputs, persist model/version/confidence metadata, and surface predictions and recommendations in the UI.
   - Why after alarms/history: model outputs need context, and users need the ability to compare prediction with actual state.

7. **Manual control pipeline**
   - Build command intent capture, mode checks, outbox, scheduler dispatch, PLC acknowledgements, and audit history.
   - Why before AI control: prove the physical command path safely with a human in the loop first.

8. **AI decisioning and automatic control**
   - Add scheduler-side decision policies that create AI-originated command intents.
   - Reuse the exact same dispatcher, policy gate, and audit path from manual control.
   - Why last: this depends on telemetry, alarms, history, ML results, and a proven manual execution path.

### Phase Ordering Implications

- The first roadmap phases should build a reliable telemetry-to-read-model loop before any advanced analytics or control work.
- Manual control must ship before AI control so the command executor, acknowledgement handling, and audit trail are already proven.
- Alarm lifecycle should precede automatic control because it becomes a key policy input and operator trust mechanism.
- ML should land as presentation and recommendation first. Direct AI actuation is a later phase, not an initial integration shortcut.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| Pilot or single plant | One `api` instance, one `scheduler` instance, one PostgreSQL instance, Kafka sized for modest telemetry volume. This is enough if reads come from current-state and aggregate tables. |
| Multi-plant regional rollout | Partition Kafka topics by plant or asset group, run multiple scheduler consumers by function, and partition PostgreSQL telemetry/history tables by date and plant. |
| Large fleet / high tag volume | Split scheduler functions into separate worker groups for ingest, aggregation, and control dispatch. Consider a dedicated historical analytics store later, but keep v1 on PostgreSQL until evidence says otherwise. |

### Scaling Priorities

1. **First bottleneck:** Dashboard reads against large telemetry tables. Fix with current-state tables, pre-aggregation, and MyBatis query tuning.
2. **Second bottleneck:** History retention and rollup refresh cost. Fix with PostgreSQL partitioning, retention windows, and incremental aggregation instead of recomputing from raw every time.

## Anti-Patterns

### Anti-Pattern 1: Direct API-to-PLC Control

**What people do:** Let the REST app write directly to a PLC or OPC UA server during the HTTP request.
**Why it's wrong:** It couples user latency to device latency, makes retries unsafe, and turns API outages into plant-control outages.
**Do this instead:** Persist command intent in `api`, dispatch asynchronously from `scheduler`, and record a formal execution result.

### Anti-Pattern 2: Separate Manual and AI Executors

**What people do:** Build one code path for operator commands and another for AI commands.
**Why it's wrong:** Policy checks, cooldowns, interlocks, and audit behavior drift apart.
**Do this instead:** Use one command schema and one dispatcher. Differentiate only by `source` and required gating.

### Anti-Pattern 3: Query Raw Telemetry for Every Screen

**What people do:** Point dashboard and history queries directly at high-volume sample tables.
**Why it's wrong:** Real-time screens become slow, expensive, and brittle as data volume grows.
**Do this instead:** Store raw telemetry for history, but read operational screens from current-state and pre-aggregated tables.

### Anti-Pattern 4: Treat ML Output as a Command

**What people do:** Accept model output as if it were already an executable control instruction.
**Why it's wrong:** It removes human context, hides model confidence, and bypasses mode and interlock checks.
**Do this instead:** Store ML output as versioned results first; only the AI decision engine may promote a recommendation into a command intent, and only in AI mode.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| PLC / SCADA / OPC UA servers | Edge or site adapter normalizes telemetry and executes control writes close to the plant boundary. | Keep device writes near the edge when possible; do not depend on browser-to-PLC round trips. |
| Kafka | Topics for telemetry, ML results, command requests, and command results. | Key by plant or asset for ordering where needed; consumers must be idempotent. |
| Python ML runtime | Emit versioned inference results through Kafka or a controlled landing store consumed by `scheduler`. | Include asset scope, time window, model version, confidence, and optional explanation payload. |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| `common` -> `api` / `scheduler` | Compile-time dependency only | `common` must stay infrastructure-light so contracts remain stable. |
| `api` -> PostgreSQL | Direct SQL/JPA | `api` owns synchronous reads and intent creation, not background materialization. |
| `api` -> `scheduler` | Database outbox and Kafka, not synchronous RPC | This is the critical separation that keeps the API thin and reliable. |
| `scheduler` -> PostgreSQL | Direct writes and scheduled jobs | `scheduler` owns read-model mutation, alarm state, ML persistence, and control execution status. |
| `scheduler` -> edge adapter | Async command/result exchange | The scheduler waits for ack/nack and persists the outcome for operator visibility. |

## Sources

- Microsoft Learn, "What is the connector for OPC UA?" https://learn.microsoft.com/en-us/azure/iot-operations/discover-manage-assets/overview-opc-ua-connector
- Microsoft Learn, "How to control OPC UA assets." https://learn.microsoft.com/en-us/azure/iot-operations/discover-manage-assets/howto-control-opc-ua
- Microsoft Learn, "Asset and Device Management." https://learn.microsoft.com/en-us/azure/iot-operations/discover-manage-assets/overview-manage-assets
- Microsoft Learn, "Introduction to the Azure Internet of Things (IoT)." https://learn.microsoft.com/en-us/azure/architecture/guide/iiot-guidance/iiot-architecture
- Microsoft Fabric reference architecture, "Connected factory." https://learn.microsoft.com/en-us/fabric/real-time-intelligence/architectures/connected-factory
- AWS IoT SiteWise documentation, "What is AWS IoT SiteWise?" https://docs.aws.amazon.com/iot-sitewise/latest/userguide/what-is-sitewise.html
- AWS IoT SiteWise documentation, "Manage alarms in AWS IoT SiteWise." https://docs.aws.amazon.com/iot-sitewise/latest/userguide/define-iot-events-alarms.html
- Confluent documentation, "Materialized Views in ksqlDB for Confluent Platform." https://docs.confluent.io/platform/current/ksqldb/concepts/materialized-views.html
- PostgreSQL documentation, "CREATE MATERIALIZED VIEW." https://www.postgresql.org/docs/current/sql-creatematerializedview.html
- PostgreSQL documentation, "Table Partitioning." https://www.postgresql.org/docs/current/ddl-partitioning.html
- Spring Batch reference, "Spring Batch Introduction." https://docs.spring.io/spring-batch/reference/spring-batch-intro.html
- ISA, "ISA-18 Series of Standards." https://www.isa.org/standards-and-publications/isa-standards/isa-18-series-of-standards

---
*Architecture research for: smart water treatment plant operations platform*
*Researched: 2026-03-31*
