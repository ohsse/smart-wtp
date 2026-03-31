# Requirements: Smart WTP

**Defined:** 2026-03-31
**Core Value:** Improve water treatment plant operating efficiency by turning real-time operational data and ML output into safe, actionable control decisions.

## v1 Requirements

### Telemetry

- [ ] **TELM-01**: System can ingest real-time sensor and PLC telemetry required for monitoring, alarms, history, and control workflows.
- [ ] **TELM-02**: System can normalize incoming telemetry into canonical asset, tag, unit, timestamp, and quality semantics before downstream use.

### Access

- [ ] **ACCS-01**: Authorized operators and field workers can access only the operational views and actions permitted for their role.
- [ ] **ACCS-02**: Only authorized users can submit manual control commands for permitted devices and actions.

### Monitoring

- [ ] **MON-01**: User can view current real-time status of configured plant assets and sensor points from a monitoring dashboard.
- [ ] **MON-02**: User can see the latest value, engineering unit, timestamp, and data-quality status for each monitored point.
- [ ] **MON-03**: User can inspect the current operating state of a selected asset or device in detail.

### Analytics

- [ ] **ANLY-01**: User can view aggregated operational charts for configured time windows.
- [ ] **ANLY-02**: User can view historical telemetry and device-state data for troubleshooting and comparison.
- [ ] **ANLY-03**: User can view machine learning prediction results associated with the relevant asset or process.

### Alarms

- [ ] **ALRM-01**: User can view active alarms with severity, source asset, start time, and current status.
- [ ] **ALRM-02**: User can acknowledge an alarm and see who acknowledged it and when.
- [ ] **ALRM-03**: User can review alarm and event history for a selected period.

### Control

- [ ] **CTRL-01**: Authorized user can submit a manual control command for a permitted device from the control screen.
- [ ] **CTRL-02**: User can see whether a control command is pending, accepted, rejected, completed, or failed.
- [ ] **CTRL-03**: User can review an audit trail of control requests, control results, and device responses.

## v2 Requirements

### Control

- **CTRL-04**: System can execute bounded equipment control automatically in AI mode within approved safety envelopes.

### Operations

- **OPER-01**: User can record shift handover notes and review recent operator logbook entries.

### Field

- **FIELD-01**: Field worker can record inspection findings and hand off maintenance follow-up work.

### Analytics

- **ANLY-04**: User can view sensor-health analytics and model-confidence context that explain whether recommendations are trustworthy.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Mobile application | Initial release is web and backend focused for plant operations. |
| Unrestricted plant-wide AI auto-control | Deferred until manual control, auditability, and safety envelopes are proven. |
| Full CMMS, ERP, or LIMS replacement | Outside the first release goal of operational monitoring and control. |
| Native offline field workflow | Deferred unless browser-based operational workflows prove insufficient. |
| 3D or AR-style plant visualization | Not required to validate the core operational value of v1. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|

**Coverage:**
- v1 requirements: 16 total
- Mapped to phases: 0
- Unmapped: 16

---
*Requirements defined: 2026-03-31*
*Last updated: 2026-03-31 after initial definition*
