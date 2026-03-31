<!-- GSD:project-start source:PROJECT.md -->
## Project

**Smart WTP**

Smart WTP is a Gradle multi-module backend platform for water treatment plant operations. It collects real-time sensor and PLC data, aggregates plant data for dashboards and history views, surfaces Python machine learning results, and controls equipment in either AI or manual mode for operators and field workers.

**Core Value:** Improve water treatment plant operating efficiency by turning real-time operational data and ML output into safe, actionable control decisions.

### Constraints

- **Architecture**: Gradle multi-module project with `common`, `api`, and `scheduler` modules - keep responsibilities separated from the start.
- **Common Module**: Shared domain models, DTOs, enums, utilities, exceptions, and common response models live in `common` - all modules depend on the same shared contracts.
- **API Module**: `api` serves as the REST application entry point - it must handle external requests cleanly without absorbing scheduler concerns.
- **Scheduler Module**: `scheduler` owns scheduling, batch jobs, async work, and Kafka-connected processing - long-running and offline work stays outside the API app.
- **Runtime Stack**: Spring Boot 4.0.5 and Java 21 - implementation choices should stay compatible with the selected platform.
- **Data Stack**: PostgreSQL with both JPA and MyBatis - design must support ORM and query-driven access patterns.
- **Control Safety**: Device control must respect AI mode and manual mode behavior - the system cannot blur automatic and user-confirmed control paths.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:research/STACK.md -->
## Technology Stack

## Baseline Assessment
- letting `common` become a dumping ground for business logic
- letting JPA and MyBatis both write the same aggregate
- letting controllers, Kafka consumers, and schedulers all trigger control logic differently
- adding extra infrastructure too early, especially reactive data access, Redis, Quartz, or a second database
## Recommended Stack
### Core Technologies
| Technology | Version | Purpose | Why Recommended | Confidence |
|------------|---------|---------|-----------------|------------|
| Spring Boot 4.0.5 with Spring MVC, Security, and Actuator | 4.0.5 | Primary runtime for `api` and `scheduler` apps | Servlet MVC matches a blocking JDBC stack, integrates cleanly with JPA/MyBatis/Kafka, and gives built-in health checks, metrics, tracing hooks, structured logging, and `ProblemDetail` support without extra frameworks. | HIGH |
| PostgreSQL | 17.x preferred | System of record for commands, configuration, alarms, history, outbox, and batch metadata | PostgreSQL gives strong transactional semantics, JSONB when needed, mature partitioning, and one operational surface for both OLTP and plant history in v1. | HIGH |
| JPA via Spring Data JPA / Hibernate | Boot-managed 4.0.x / 7.x line | Transactional writes and aggregate persistence | Use JPA for control commands, device configuration, users/roles, thresholds, alarm rules, and other write-owned aggregates where optimistic locking and entity lifecycle matter. | HIGH |
| MyBatis Spring Boot Starter | 4.0.0 | SQL-first access for dashboards, history, aggregation, bulk ingest, and reporting queries | MyBatis is the right complement to JPA for plant telemetry and operational views because those queries are explicit, join-heavy, windowed, and often performance-sensitive. | HIGH |
| Spring for Apache Kafka | 4.0.x | Telemetry ingest, asynchronous processing, integration events | Kafka is already in scope. Spring Kafka gives listener containers, DLT/retry tooling, transactions where appropriate, and observability support on the Boot 4 line. | HIGH |
| Spring Batch | 6.0.x | Restartable batch jobs, reconciliation, aggregation, backfill, retention, and ML sync workflows in `scheduler` | Batch is a better fit than ad hoc cron code for long-running plant jobs because it gives restartability, job metadata, chunking, recovery, and controlled concurrency. | HIGH |
### Supporting Libraries
| Library | Version | Purpose | When to Use | Confidence |
|---------|---------|---------|-------------|------------|
| `org.flywaydb:flyway-core` | Boot-managed | Schema migrations | Mandatory from day 1. Use SQL migrations for schema, indexes, partitions, and seed reference data. Do not rely on Hibernate schema generation outside local dev. | HIGH |
| `org.springframework.boot:spring-boot-starter-validation` | Boot-managed | Bean validation for request DTOs and config | Always. Validate command payloads, scheduler configuration, and integration settings before they reach domain logic. | HIGH |
| `org.springframework.boot:spring-boot-starter-security` | Boot-managed | Authentication and authorization foundation | Always. Even internal operator systems need role-based protection and endpoint hardening. | HIGH |
| `org.springframework.boot:spring-boot-starter-oauth2-resource-server` | Boot-managed | JWT/OIDC resource server integration | Default choice if the plant or enterprise already has an IdP. Prefer external identity and treat this backend as a resource server, not an authorization server. | HIGH |
| `org.springframework.boot:spring-boot-starter-actuator` | Boot-managed | Health, liveness/readiness, metrics, and operational endpoints | Always. Required for safe operations and deployment diagnostics. | HIGH |
| `io.micrometer:micrometer-registry-prometheus` | Boot-managed | Metrics export | Use for Prometheus/Grafana or any scraper-based monitoring. Meter API latency, batch duration, Kafka lag, DB pool pressure, command outcomes, and integration failures. | HIGH |
| `org.springframework.boot:spring-boot-starter-opentelemetry` | Boot-managed | Trace export over OTLP | Strongly recommended when `api`, `scheduler`, Kafka, and external adapters must be correlated during incidents. | HIGH |
| `org.springdoc:springdoc-openapi-starter-webmvc-ui` | 3.0.1 | OpenAPI generation and Swagger UI | Use in `api` for frontend integration and internal testing. Keep docs enabled in non-prod by default; production exposure depends on security policy. | HIGH |
| `net.javacrumbs.shedlock:shedlock-spring` + `shedlock-provider-jdbc-template` | 7.2.2 | Cluster-safe scheduling lock | Add only when `scheduler` runs more than one replica. Use JDBC provider on PostgreSQL and `usingDbTime()` to avoid clock skew issues. | HIGH |
| `org.springframework.boot:spring-boot-starter-cache` + `com.github.ben-manes.caffeine:caffeine` | Boot-managed | Local in-memory cache | Optional. Use only for slow-changing reference data such as plant hierarchy, code tables, and permission lookups. Do not cache live telemetry or device state. | HIGH |
### Development Tools
| Tool | Purpose | Notes | Confidence |
|------|---------|-------|------------|
| Gradle version catalog + dependency locking | Version consistency across modules | Keep versions centralized. Apply the Boot plugin only to executable modules, not `common`. Prefer Boot BOM-managed versions over pinning every Spring/Micrometer dependency manually. | HIGH |
| `org.springframework.boot:spring-boot-testcontainers` + Testcontainers | Real integration tests against PostgreSQL and Kafka | Use Boot service connections for local and CI integration tests. This is the fastest way to catch JPA/MyBatis SQL, migration, and Kafka wiring issues before deployment. | HIGH |
| `org.mybatis.spring.boot:mybatis-spring-boot-starter-test` | Focused MyBatis slice tests | Use `@MybatisTest` for mapper SQL and result-map verification. | HIGH |
| `org.springframework.kafka:spring-kafka-test` | Kafka listener and producer tests | Use for listener error handling, serializer compatibility, and topic-level test support. | HIGH |
| `org.springframework.batch:spring-batch-test` | Batch job and step tests | Use for restartability, job parameter, and step outcome verification in `scheduler`. | HIGH |
| `com.tngtech.archunit:archunit` | Architecture enforcement tests | Use to lock module boundaries: `api` must not depend on `scheduler`, `common` must not depend on Spring Boot runtime concerns, and persistence packages should not cross feature boundaries. | HIGH |
## Module and Integration Guardrails
### Required module boundaries
- `common` is a shared kernel only.
- Put shared DTOs, enums, error codes, common response models, time abstractions, and security abstractions here.
- Do not put repositories, services, Kafka listeners, scheduler code, entities with rich lifecycle, or feature-specific business rules in `common`.
- `api` is the synchronous edge.
- It owns REST controllers, request validation, security, application services, query facades, and transaction boundaries for user-initiated commands.
- It should persist command intent and outbox records, but it should not run long jobs, Kafka listeners, polling loops, or retry daemons.
- `scheduler` owns asynchronous and offline work.
- It owns `@Scheduled`, Spring Batch, Kafka consumers, outbox publishing, aggregation, reconciliation, data retention, ML polling, and replay/recovery jobs.
- All jobs here must be idempotent and restart-safe.
### Required persistence split
- JPA owns write-side aggregates.
- MyBatis owns read-heavy operational queries and bulk SQL paths.
- Do not let both write the same business aggregate.
- If a table is JPA-owned, MyBatis may read it for reporting but should not become a second write path.
- If MyBatis is used for bulk ingest or projection tables, keep that ownership explicit.
### Required integration patterns
- Use a PostgreSQL outbox table for integration events and command dispatch records.
- Publish Kafka messages from `scheduler`, not directly from controller code.
- Do not try to make PostgreSQL and Kafka one atomic transaction. Use transactional outbox plus idempotent consumers instead.
- Persist every device control command before dispatch.
- A command record should include mode (`AI` or `MANUAL`), operator or actor, target device, requested action, correlation id, timestamps, and final outcome.
- Field-side retries must be explicit and domain-aware. Automatic blind retries on control actions are unsafe.
- Use `RestClient` or HTTP interface clients for Python ML integration and other blocking HTTP calls.
- Do not pull in Feign or reactive HTTP clients by default when the rest of the stack is blocking.
## Installation
## Alternatives Considered
| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Spring MVC on Boot 4 | Spring WebFlux + R2DBC | Only if you intentionally rebuild the whole persistence and integration model around non-blocking I/O. That is not compatible with a JPA/MyBatis baseline. |
| Flyway | Liquibase | Use Liquibase only if the team strongly prefers XML/YAML changelogs and already has operational standards around it. For this project, SQL-first Flyway is the simpler fit. |
| `@Scheduled` + Spring Batch + ShedLock | Quartz | Use Quartz only if you need persistent calendars, misfire semantics, or complex trigger orchestration that cannot be expressed as batch jobs plus simple schedules. |
| External IdP + Spring Security resource server | Spring Authorization Server | Use Authorization Server only if this platform must issue tokens to other systems. Do not make the WTP backend its own IdP by default. |
| Native PostgreSQL partitioning first | TimescaleDB from day 1 | Add TimescaleDB only after ingest and query benchmarks prove PostgreSQL native partitioning is insufficient and platform operations accept extension-specific complexity. |
## What NOT to Use
| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Spring WebFlux / R2DBC | It fights the chosen blocking persistence stack and creates two programming models, two transaction models, and harder debugging. | Spring MVC + JDBC/JPA/MyBatis |
| A third persistence abstraction such as jOOQ, QueryDSL, or Spring Data JDBC | `JPA + MyBatis` already covers write-side and SQL-first needs. A third abstraction increases cognitive load and ownership ambiguity. | Keep a strict two-lane model: JPA for writes, MyBatis for operational SQL |
| `hibernate.hbm2ddl.auto` outside local throwaway environments | Hidden schema drift is unacceptable in plant operations. | Flyway migrations |
| `spring.jpa.open-in-view=true` | It hides query behavior in the web layer and encourages lazy-loading surprises and N+1 problems. | Set `spring.jpa.open-in-view=false` and map DTOs inside service transactions |
| Quartz as the default scheduler | It adds stateful scheduling infrastructure before the project has proven it needs it. | Spring Batch for real jobs, `@Scheduled` for simple triggers, ShedLock only when clustered |
| Redis for sessions, distributed cache, or live plant state in v1 | It introduces another state system and stale-state risk without clear early value. | PostgreSQL as source of truth; optional Caffeine for local reference-data caching |
| Custom JWT parsing or homegrown auth filters | Security bugs here are expensive and unnecessary. | Spring Security resource server with an external IdP |
| TimescaleDB at kickoff | It adds extension lock-in and operational overhead before volume is known. | PostgreSQL native partitioning first |
| Global virtual-thread enablement on day 1 | It does not remove DB bottlenecks and can complicate operational reasoning in control and scheduling paths before load testing. | Tuned platform thread pools first; revisit after profiling |
| Infinite Kafka retries or relying on default behavior | Poison messages can stall pipelines or create repeated unsafe side effects. | Explicit `DefaultErrorHandler`, finite backoff, DLT, and idempotent consumers |
## Stack Patterns by Variant
- Use Spring Batch for restartable jobs.
- Use plain `@Scheduled` for simple periodic triggers.
- Do not add ShedLock yet.
- Add ShedLock with JDBC provider on PostgreSQL.
- Use `usingDbTime()`.
- Keep jobs idempotent because ShedLock skips overlapping runs; it is a lock, not a distributed scheduler.
- Put Kafka consumers and publishers in `scheduler`.
- Keep controller flows synchronous and short.
- Use outbox plus idempotent consumer logic rather than direct controller-to-Kafka publishing.
- Isolate that adapter behind a dedicated integration package in `scheduler`.
- Never let protocol libraries leak into controllers or shared `common` contracts.
- Treat control dispatch as audited infrastructure, not casual service-to-service I/O.
- First add partitioning, retention jobs, and projection tables.
- Benchmark before adding TimescaleDB or another specialized store.
- Only split storage after actual ingestion and query evidence, not forecasted scale.
## Version Compatibility
| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| `org.springframework.boot:4.0.5` | Java 21, Spring Framework 7, Security 7, Data 4 line | Chosen baseline is aligned with the current Spring 7 generation. |
| `org.mybatis.spring.boot:mybatis-spring-boot-starter:4.0.0` | Spring Boot 4.0+, Java 17+ | Official MyBatis starter line for Boot 4. |
| Spring Batch `6.0.x` | Spring Framework 7, Spring Data 4, Spring Kafka 4 | Do not use the default resourceless repository for real jobs; configure JDBC batch metadata tables in PostgreSQL. |
| Spring Kafka `4.0.x` | Apache Kafka 4 clients, KRaft mode | Kafka 4 removes ZooKeeper-era assumptions; plan clusters accordingly. |
| `net.javacrumbs.shedlock:7.2.2` | Spring Boot 4.x, Java 17+ | Official compatibility matrix lists Boot 4.x and Spring 7. |
| `org.springdoc:springdoc-openapi-starter-webmvc-ui:3.0.1` | Spring Boot 4.0.x | `3.0.1` explicitly upgraded to Spring Boot `4.0.1`, so it is the right springdoc line for Boot 4. |
| `com.tngtech.archunit:archunit:1.4.1` | Java 21+ | Current release supports modern class file versions and is suitable for boundary tests in this codebase. |
| Testcontainers `2.0.x` | Java 21+, Spring Boot test service connections | Prefer Boot-managed service connections and official PostgreSQL/Kafka modules in CI. |
## Sources
- [Spring Boot logging and structured logging docs](https://docs.spring.io/spring-boot/reference/features/logging.html) - verified Boot 4 built-in structured logging support and default Logback stance. HIGH
- [Spring Boot caching docs](https://docs.spring.io/spring-boot/reference/io/caching.html) - verified Caffeine support and cache-provider guidance. HIGH
- [Spring Boot observability docs](https://docs.spring.io/spring-boot/reference/actuator/observability.html) - verified Micrometer Observation and OpenTelemetry support. HIGH
- [Spring Boot tracing docs](https://docs.spring.io/spring-boot/reference/actuator/tracing.html) - verified `spring-boot-starter-opentelemetry` and OTLP tracing support. HIGH
- [Spring Boot Testcontainers docs](https://docs.spring.io/spring-boot/reference/testing/testcontainers.html) - verified Boot service-connection support for containerized integration tests. HIGH
- [Spring Security OAuth2 resource server docs](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/jwt.html) - verified JWT resource-server configuration and external IdP model. HIGH
- [Spring Security OAuth2 overview](https://docs.spring.io/spring-security/reference/servlet/oauth2/) - verified Boot starter for resource server usage. HIGH
- [Spring Framework REST client docs](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html) - verified `RestClient` and HTTP interface client model for blocking HTTP integration. HIGH
- [Spring Batch 6 "What's new"](https://docs.spring.io/spring-batch/reference/whatsnew.html) - verified Batch 6 feature set, dependency line, and new infrastructure model. HIGH
- [Spring Kafka reference](https://docs.spring.io/spring-kafka/reference/) - verified current Spring Kafka 4.0.x line. HIGH
- [Spring Kafka error handling docs](https://docs.spring.io/spring-kafka/reference/kafka/annotation-error-handling.html) - verified `DefaultErrorHandler`, finite retries, and DLT pattern support. HIGH
- [Spring Boot SQL database docs](https://docs.spring.io/spring-boot/reference/data/sql.html) - verified `spring.jpa.open-in-view`, JPA DDL guidance, and that jOOQ/R2DBC remain optional alternatives rather than required additions. HIGH
- [Spring Boot Quartz docs](https://docs.spring.io/spring-boot/reference/io/quartz.html) - verified Quartz support exists but is an optional add-on, not a required scheduler baseline. HIGH
- [MyBatis Spring Boot Starter reference](https://mybatis.org/spring-boot-starter/mybatis-spring-boot-autoconfigure/) - verified `4.0.0` compatibility with Spring Boot `4.0+`. HIGH
- [MyBatis Spring Boot Starter releases](https://github.com/mybatis/spring-boot-starter/releases) - verified `4.0.0` release for Boot 4 line. HIGH
- [MyBatis Spring Boot Starter Test reference](https://mybatis.org/spring-boot-starter/mybatis-spring-boot-test-autoconfigure/) - verified `@MybatisTest` support on Boot 4 line. HIGH
- [ShedLock README and compatibility matrix](https://github.com/lukas-krecan/ShedLock) - verified JDBC provider guidance, `usingDbTime()`, and Boot 4 compatibility. HIGH
- [springdoc-openapi releases](https://github.com/springdoc/springdoc-openapi/releases) - verified `3.0.1` as the Boot 4.x line and `3.0.0/3.0.1` Boot 4 upgrade notes. HIGH
- [ArchUnit repository and docs](https://github.com/TNG/ArchUnit) - verified `1.4.1` usage and architecture-test focus. HIGH
- [Testcontainers Java repository](https://github.com/testcontainers/testcontainers-java) - verified current `2.0.2` release line. MEDIUM
- [Flyway getting started](https://documentation.red-gate.com/fd/getting-started-212140421.html) - verified Flyway current product direction and SQL migration workflow. HIGH
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
