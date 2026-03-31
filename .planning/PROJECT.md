# Smart WTP

## What This Is

Smart WTP is a Gradle multi-module backend platform for water treatment plant operations. It collects real-time sensor and PLC data, aggregates plant data for dashboards and history views, surfaces Python machine learning results, and controls equipment in either AI or manual mode for operators and field workers.

## Core Value

Improve water treatment plant operating efficiency by turning real-time operational data and ML output into safe, actionable control decisions.

## Requirements

### Validated

(None yet - ship to validate)

### Active

- [ ] Operators and field workers can monitor real-time plant status from a dashboard.
- [ ] The system can collect and store real-time sensor and PLC data for operational use.
- [ ] The system can surface aggregated charts, alarm and history data, and ML prediction results.
- [ ] The system can execute equipment control automatically in AI mode and after user interaction in manual mode.
- [ ] The backend is structured as a Gradle multi-module system with shared common code, REST APIs, and scheduler or batch processing.

### Out of Scope

- Mobile application - initial release is web and backend focused.
- Additional client channels beyond the operator-facing operational system - keep v1 focused on plant monitoring and control.

## Context

- This is a greenfield project for a smart water treatment plant system.
- Primary users are operators and field workers.
- The core operational flow is real-time collection, persistence, aggregation, dashboard viewing, ML result viewing, and control command execution.
- Control behavior changes by mode:
  - AI mode executes device control automatically.
  - Manual mode executes control after explicit user interaction.
- Planned v1 screens or capabilities include a real-time monitoring dashboard, aggregated charts, ML prediction results, device control screens, and alarm or history views.
- External integration points currently identified are sensor or PLC ingestion and Kafka-connected processing.
- Python-based machine learning outputs will be displayed inside the operational system.

## Constraints

- **Architecture**: Gradle multi-module project with `common`, `api`, and `scheduler` modules - keep responsibilities separated from the start.
- **Common Module**: Shared domain models, DTOs, enums, utilities, exceptions, and common response models live in `common` - all modules depend on the same shared contracts.
- **API Module**: `api` serves as the REST application entry point - it must handle external requests cleanly without absorbing scheduler concerns.
- **Scheduler Module**: `scheduler` owns scheduling, batch jobs, async work, and Kafka-connected processing - long-running and offline work stays outside the API app.
- **Runtime Stack**: Spring Boot 4.0.5 and Java 21 - implementation choices should stay compatible with the selected platform.
- **Data Stack**: PostgreSQL with both JPA and MyBatis - design must support ORM and query-driven access patterns.
- **Control Safety**: Device control must respect AI mode and manual mode behavior - the system cannot blur automatic and user-confirmed control paths.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use a Gradle multi-module structure | The project has distinct shared, API, and background processing responsibilities | Pending |
| Split modules into `common`, `api`, and `scheduler` | Shared contracts and batch or async workflows should not be mixed into the REST application | Pending |
| Use PostgreSQL with both JPA and MyBatis | The system needs standard entity persistence and query-oriented data access for operational views and aggregation | Pending |
| Support both AI and manual control modes | Plant operation needs both automated control and operator-driven intervention paths | Pending |
| Focus v1 on monitoring, analysis visibility, and control | The first release should prove operational value before expanding channels such as mobile | Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `$gsd-transition`):
1. Requirements invalidated? - Move to Out of Scope with reason
2. Requirements validated? - Move to Validated with phase reference
3. New requirements emerged? - Add to Active
4. Decisions to log? - Add to Key Decisions
5. "What This Is" still accurate? - Update if drifted

**After each milestone** (via `$gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check - still the right priority?
3. Audit Out of Scope - reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-31 after initialization*
