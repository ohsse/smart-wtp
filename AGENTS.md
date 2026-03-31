## Project

**Smart WTP**

Smart WTP is a Gradle multi-module backend platform for water treatment plant operations. It collects real-time sensor and PLC data, aggregates plant data for dashboards and history views, surfaces Python machine learning results, and controls equipment in either AI or manual mode for operators and field workers.

**Core Value:** Improve water treatment plant operating efficiency by turning real-time operational data and ML output into safe, actionable control decisions.

### Constraints

- **Architecture**: Gradle multi-module project with `common`, `api`, and `scheduler` modules.
- **Common Module**: Shared domain models, DTOs, enums, utilities, exceptions, and common response models live in `common`.
- **API Module**: `api` handles synchronous REST requests and should not absorb scheduler concerns.
- **Scheduler Module**: `scheduler` owns scheduling, batch jobs, async work, Kafka-connected processing, and control dispatch pipelines.
- **Runtime Stack**: Spring Boot 4.0.5 and Java 21.
- **Data Stack**: PostgreSQL with both JPA and MyBatis.
- **Control Safety**: Manual and AI-originated control must stay mode-aware, auditable, and bounded by safety rules.

## Technology Stack

- Use Spring MVC on Spring Boot 4.0.5 for both executable modules.
- Keep PostgreSQL as the v1 system of record.
- Use JPA for write-owned aggregates and MyBatis for read-heavy or bulk SQL paths.
- Use Kafka for asynchronous ingest and integration events.
- Use Spring Batch for restartable background jobs in `scheduler`.
- Treat Flyway, Actuator, metrics, tracing, Testcontainers, and architecture tests as day-one requirements.

## Workflow Enforcement

Before changing files, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
