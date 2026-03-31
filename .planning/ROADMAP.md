# Roadmap: Smart WTP

## Overview

V1 is sequenced as a safe operator platform. The roadmap establishes canonical plant contracts, telemetry semantics, and access boundaries first; lands reliable telemetry and current-state monitoring next; adds history, ML visibility, and alarm workflows on top of that state; and only then exposes audited manual control. AI auto-control remains v2 and must reuse the bounded command path rather than bypass it.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions after planning

- [ ] **Phase 1: Plant Contract, Safety Envelope, and Access Foundation** - Establish canonical plant semantics and role boundaries before downstream features.
- [ ] **Phase 2: Telemetry Backbone and Current-State Monitoring** - Materialize trustworthy real-time plant state for operators.
- [ ] **Phase 3: History, Trends, and ML Visibility** - Expose historical context, aggregated views, and prediction results.
- [ ] **Phase 4: Alarm Operations** - Deliver actionable abnormal-state handling on top of trustworthy current and historical state.
- [ ] **Phase 5: Manual Control and Command Audit** - Ship bounded manual control with status tracking and forensic evidence.

## Phase Details

### Phase 1: Plant Contract, Safety Envelope, and Access Foundation
**Goal**: The platform has authoritative plant and point contracts, safety metadata, and role boundaries that downstream telemetry, monitoring, alarms, and control workflows can trust.
**Depends on**: Nothing (first phase)
**Requirements**: TELM-02, ACCS-01
**Success Criteria** (what must be TRUE):
  1. Authorized operators and field workers can reach only the routes and actions permitted for their role.
  2. Configured assets and points expose canonical asset, tag, unit, timestamp, and quality semantics that downstream APIs and jobs use consistently.
**Plans**: TBD

### Phase 2: Telemetry Backbone and Current-State Monitoring
**Goal**: The platform can ingest required plant telemetry and turn it into trustworthy current-state monitoring for operators.
**Depends on**: Phase 1
**Requirements**: TELM-01, MON-01, MON-02, MON-03
**Success Criteria** (what must be TRUE):
  1. New sensor and PLC readings for configured assets appear in the platform and are available for monitoring workflows.
  2. User can open a monitoring dashboard showing current status for configured plant assets and sensor points.
  3. User can inspect a selected asset or device and see its latest value, engineering unit, timestamp, data-quality status, and current operating state.
**Plans**: TBD
**UI hint**: yes

### Phase 3: History, Trends, and ML Visibility
**Goal**: Users can analyze plant behavior over time and view ML prediction results in operational context.
**Depends on**: Phase 2
**Requirements**: ANLY-01, ANLY-02, ANLY-03
**Success Criteria** (what must be TRUE):
  1. User can view aggregated operational charts for configured time windows.
  2. User can query historical telemetry and device-state data for troubleshooting and comparison.
  3. User can view machine learning prediction results associated with the relevant asset or process.
**Plans**: TBD
**UI hint**: yes

### Phase 4: Alarm Operations
**Goal**: Users can detect, acknowledge, and review abnormal plant conditions from trustworthy current and historical state.
**Depends on**: Phase 3
**Requirements**: ALRM-01, ALRM-02, ALRM-03
**Success Criteria** (what must be TRUE):
  1. User can view active alarms with severity, source asset, start time, and current status.
  2. User can acknowledge an alarm and later see who acknowledged it and when.
  3. User can review alarm and event history for a selected period.
**Plans**: TBD
**UI hint**: yes

### Phase 5: Manual Control and Command Audit
**Goal**: Authorized users can issue bounded manual commands through an audited command path that future guarded automation can reuse.
**Depends on**: Phase 4
**Requirements**: ACCS-02, CTRL-01, CTRL-02, CTRL-03
**Success Criteria** (what must be TRUE):
  1. Authorized user can submit a manual control command only for permitted devices and actions from the control screen.
  2. User can track each control command through pending, accepted, rejected, completed, or failed states.
  3. User can review an audit trail tying together the control request, execution result, and device response.
**Plans**: TBD
**UI hint**: yes

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Plant Contract, Safety Envelope, and Access Foundation | 0/TBD | Not started | - |
| 2. Telemetry Backbone and Current-State Monitoring | 0/TBD | Not started | - |
| 3. History, Trends, and ML Visibility | 0/TBD | Not started | - |
| 4. Alarm Operations | 0/TBD | Not started | - |
| 5. Manual Control and Command Audit | 0/TBD | Not started | - |
