# Feature Research

**Domain:** Smart water treatment plant monitoring and control platform (backend + operator workflows)
**Researched:** 2026-03-31
**Confidence:** MEDIUM

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these means the product does not feel like a real operations platform.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Real-time plant and asset monitoring | Every SCADA and operations-center product leads with system-wide monitoring across plant and remote assets. | MEDIUM | Requires PLC and sensor ingestion, asset and tag hierarchy, stale or bad-quality indicators, unit-aware values, and drill-down from plant to process to device. |
| Alarm and event management | Alarm handling is core process-operations functionality, not an add-on. Operators expect prioritization, acknowledgement, and historical review. | HIGH | Needs severity and priority rules, acknowledgements, notifications, alarm journal, nuisance-alarm controls, and correlation to equipment state and operator actions. |
| Historian, trends, and event-correlated history | Vendors consistently pair monitoring with historian, charting, and root-cause review. Without history, operators cannot explain process drift or verify changes. | MEDIUM | Store raw and aggregated time-series data, overlay alarms and commands on trends, retain sufficient history for troubleshooting and reporting, and support fast ad hoc queries. |
| Secure manual control with mode awareness | Plants buy these systems to operate equipment, not just watch it. Safe command execution is table stakes for real control software. | HIGH | Needs role-based access, security zones, command confirmation, setpoint bounds, read-back verification, manual vs AI mode separation, and a full command audit trail. |
| Operational reporting and compliance evidence | Treatment plants need daily and shift reports, alarm summaries, and traceable operational records for internal review and compliance workflows. | MEDIUM | Build scheduled and ad hoc reports from historian and alarm data; include interventions, deviations, water-quality context, and operator annotations. |
| Shift logbook and handover | Industrial operations suites consistently include logbook and handover functions because paper and spreadsheet handoffs create operational risk. | MEDIUM | Start with a web logbook: event timeline, operator notes, outstanding issues, standing orders, and shift summary generation. Full knowledge-management workflow can come later. |
| Field inspection rounds and maintenance handoff | Critical observations still happen in the field. Modern operations platforms increasingly digitize rounds and route issues into maintenance workflows. | MEDIUM | For v1, keep this browser and tablet friendly rather than building a native mobile app. Capture inspections and observations, then hand off to an existing CMMS instead of building full work-order management. |

### Differentiators (Competitive Advantage)

These are the features that can make Smart WTP meaningfully better than a generic SCADA dashboard.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| AI-assisted decision support and prediction | Predicts excursions, energy or chemical usage, and likely process instability before alarms become incidents. Gives operators recommended actions instead of just more charts. | HIGH | Best initial form is recommendation-first: show predicted outcomes, suggested setpoint changes, and confidence context alongside live process state and history. |
| Guardrailed AI automatic control for selected units | Reduces routine operator tuning effort and creates measurable efficiency gains when automation stays inside engineered limits. | HIGH | Only enable per process unit or equipment class after manual control is stable. Requires safe envelopes, mode transitions, fallback behavior, operator-visible reason codes, and complete auditability. |
| Sensor-health and data-quality analytics | Prevents the system from making decisions off fouled analyzers, stuck instruments, or implausible sensor values. This materially improves trust in alerts, trends, and ML output. | HIGH | Needs data-quality scoring, missing-data handling, plausibility rules, and separation of instrument faults from real process upsets. |
| Guided procedures and contextual work instructions | Makes less-experienced operators and field workers more consistent during abnormal conditions, startup, shutdown, and maintenance preparation. | MEDIUM | Attach standing orders, SOPs, and troubleshooting steps to alarms, assets, and operating modes after the logbook and handover foundation exists. |
| What-if simulation and digital-twin style optimization | Lets operators and engineers test proposed changes before applying them to the plant, improving confidence in optimization and control changes. | HIGH | Valuable later, but depends on mature historian data, stable tag models, and trustworthy process models. Strong v2 candidate, not a launch feature. |

### Anti-Features (Commonly Requested, Often Problematic)

These are the features that sound attractive but should be excluded from v1 to keep scope safe and defensible.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Full CMMS, ERP, LIMS, GIS, and enterprise-suite replacement in v1 | Stakeholders want a single pane of glass and fewer systems. | This explodes scope, duplicates systems of record, and delays the core operator product. It also creates heavy master-data and workflow ownership problems. | Ingest the minimum reference data needed for operations, and integrate outward to existing CMMS, LIMS, or ERP systems through APIs, events, and report exports. |
| Unrestricted remote control from any browser or network | It sounds convenient for supervisors and field staff. | Water-sector guidance and recent incidents show exposed HMIs and PLC paths materially increase operational risk. Broad remote actuation also conflicts with network zoning and approval discipline. | Launch with secure remote visibility first. Add tightly scoped remote control later behind MFA, network segmentation, role checks, and explicit approval rules. |
| Black-box AI autonomy across the whole plant | It promises labor savings and aggressive optimization. | Operators will not trust it, and unsafe behavior is hard to bound when instrumentation or model quality drifts. In a treatment plant, opaque automatic dosing or actuator changes are a rewrite-grade mistake. | Start with recommendation-first AI and then enable bounded auto mode only for selected loops with clear guardrails, fallbacks, and audit trails. |
| 3D or AR digital twin as the primary operator interface | It demos well and looks modern. | It slows delivery, adds heavy data-modeling overhead, and can reduce situational awareness compared with a clear high-performance HMI. Fancy graphics do not replace alarm clarity, trends, or command safety. | Use an ISA-101-style high-performance 2D HMI first. Add specialized 3D views or simulation only where they prove operational value. |

## Feature Dependencies

```text
[PLC and sensor ingestion + asset/tag model]
  -> [Real-time plant and asset monitoring]
  -> [Alarm and event management]
  -> [Historian, trends, and event-correlated history]

[Historian, trends, and event-correlated history]
  -> [Operational reporting and compliance evidence]
  -> [AI-assisted decision support and prediction]

[Role-based access + security zones + audit trail]
  -> [Secure manual control with mode awareness]

[Secure manual control with mode awareness]
  -> [Guardrailed AI automatic control for selected units]

[Shift logbook and handover]
  -> [Guided procedures and contextual work instructions]

[Field inspection rounds and maintenance handoff]
  -> [Existing CMMS integration]

[Sensor-health and data-quality analytics]
  -> [Higher-trust alarms]
  -> [Higher-trust AI predictions and automatic control]

[Unrestricted remote control]
  conflicts with [Control safety and cybersecurity baseline]
```

### Dependency Notes

- **Real-time monitoring, alarms, and historian all depend on the same asset and tag model:** if the plant model is inconsistent, every downstream feature becomes noisy or misleading.
- **Reporting depends on history, not just live dashboards:** compliance and operations review need stored process values, alarms, commands, and operator notes.
- **AI automatic control should never precede safe manual control:** the platform must first prove it can execute and audit human-approved commands correctly.
- **Guided procedures are much more effective after digital handover exists:** otherwise procedures and shift context remain disconnected.
- **Field workflows should hand off to maintenance systems, not replace them:** v1 should create actionable maintenance requests, not reimplement enterprise maintenance planning.
- **Broad remote control conflicts with water-sector safety guidance:** remote visibility is lower-risk and should precede remote actuation.

## MVP Definition

### Launch With (v1)

- [x] Real-time plant and asset monitoring - baseline operator visibility across process units and critical equipment.
- [x] Alarm and event management with acknowledgement, notification, and alarm journal - baseline response loop.
- [x] Historian, trends, and operational reporting - enables troubleshooting, performance review, and compliance evidence.
- [x] Secure manual control with AI/manual mode awareness, RBAC, confirmations, and audit trail - safe actuation path.
- [x] Shift logbook and handover - required for 24/7 operations continuity.
- [x] Browser-based field inspection capture and maintenance handoff - minimal field workflow without expanding into native mobile.
- [x] ML result visibility and recommendation display - validates the product's core value before broad autonomous control.

### Add After Validation (v1.x)

- [ ] Guardrailed AI automatic control for selected loops or units - add only after manual control and auditing are proven stable.
- [ ] Sensor-health and data-quality analytics - add once enough history exists to train and validate models.
- [ ] Guided procedures, standing orders, and contextual troubleshooting - add when the operator logbook is in regular use.
- [ ] CMMS work-request integration and closure feedback - add when field-to-maintenance handoff volume justifies tighter automation.

### Future Consideration (v2+)

- [ ] What-if simulation and digital-twin optimization - defer until the plant model and historian quality are mature.
- [ ] Multi-site benchmarking and fleet operations center - defer until the product serves more than one site or plant.
- [ ] Native mobile and offline-first field workflow - defer because the project explicitly avoids mobile in the initial release.
- [ ] Rich 3D visualization or AR overlays - defer unless there is a proven training or engineering use case.

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Real-time plant and asset monitoring | HIGH | MEDIUM | P1 |
| Alarm and event management | HIGH | HIGH | P1 |
| Historian, trends, and operational reporting | HIGH | MEDIUM | P1 |
| Secure manual control with mode awareness | HIGH | HIGH | P1 |
| Shift logbook and handover | HIGH | MEDIUM | P1 |
| Field inspection capture and maintenance handoff | MEDIUM | MEDIUM | P1 |
| ML result visibility and recommendation display | HIGH | MEDIUM | P1 |
| Guardrailed AI automatic control | HIGH | HIGH | P2 |
| Sensor-health and data-quality analytics | HIGH | HIGH | P2 |
| What-if simulation and digital-twin optimization | MEDIUM | HIGH | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have after the core platform proves operational value
- P3: Nice to have, future consideration

## Competitor Feature Analysis

| Feature | Competitor A | Competitor B | Our Approach |
|---------|--------------|--------------|--------------|
| Real-time monitoring and control | Rockwell Smart Water SCADA centers on system-wide monitoring and control, historian, reporting, CMMS linkage, and secure network foundations. | Ignition Water/Wastewater emphasizes connecting remote sites and monitoring performance from anywhere. | Build plant-first web monitoring with strong asset context and remote visibility, but do not default to broad remote actuation. |
| Alarm, history, and reporting | AVEVA Operations Control pairs SCADA with historian and purpose-built reports for compliance and troubleshooting. | Ignition ships historian and alarm journal capabilities as first-class platform modules. | Treat historian and alarm journal as core domain services, not optional reporting add-ons. |
| Shift handover and field workflows | Hexagon j5 offers shift handover, logbook, rounds, work instructions, and action management. | AVEVA Teamwork focuses on worker support and knowledge-sharing from workstations and portable devices. | Deliver the minimum digital logbook and browser-based rounds in v1; add richer connected-worker knowledge flows only after adoption. |
| Optimization and prediction | Xylem Plant Management for wastewater offers predictions, operational suggestions, automatic process adjustment, alarms, and work-order generation. | Rockwell Smart Water optimization pages emphasize predictive models for setpoints, process values, energy, and AI-led optimization. | Start with explainable prediction and recommendation views, then add bounded auto mode for selected units once safety controls are proven. |

## Sources

- Project context: `.planning/PROJECT.md`
- Rockwell Automation Smart Water Ecosystem, SCADA and Operations Center: https://interact.rockwellautomation.com/smart-water-ecosystem/scada.html
- Rockwell Automation Smart Water Ecosystem, Energy Consumption / Prediction and Process Optimization: https://interact.rockwellautomation.com/smart-water-ecosystem/energy-consumption.html
- Inductive Automation, Ignition SCADA for the Water and Wastewater Industry: https://page.inductiveautomation.com/industry/water-wastewater
- Inductive Automation docs, Historian Core Module: https://docs.inductiveautomation.com/docs/8.3/getting-started/modules-overview/core-modules/tag-historian-module
- Inductive Automation docs, Alarm Journal: https://www.docs.inductiveautomation.com/docs/8.3/platform/alarming/alarm-journal
- Inductive Automation docs, Security Level Rules: https://www.docs.inductiveautomation.com/docs/8.3/platform/security/identity-provider-authentication-strategy/security-level-rules
- AVEVA Operations Control and HMI: https://www.aveva.com/en/solutions/operations/operations-control-hmi/
- Hexagon j5 Operations Management Solutions: https://hexagon.com/products/j5-operations-management-solutions
- Hexagon j5 Shift Handover: https://hexagon.com/es/products/j5-shift-handover
- Hexagon j5 Operations Logbook Overview: https://aliresources.hexagon.com/all-resources/j5-operations-logbook-overview
- Hexagon j5 Operator Rounds and Routine Duties: https://hexagon.com/it/products/j5-operator-rounds-routine-duties
- Xylem Vue powered by GoAigua: https://www.xylem.com/it-it/brands/xylem-vue/xylem-vue-powered-by-goaigua/
- Xylem Vue Plant Management Application for Wastewater: https://www.xylem.com/en-sg/catalog/products--services/digital-water/xylem-vue/plant-management-application-for-wastewater/
- ISA101 committee scope for HMIs: https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa101
- ISA18 committee scope for alarm systems: https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa18
- CISA and EPA fact sheet on internet-exposed HMIs in water and wastewater systems: https://www.cisa.gov/resources-tools/resources/internet-exposed-hmis-pose-cybersecurity-risks-water-and-wastewater-systems
- CISA advisory on exploitation of Unitronics PLCs used in water and wastewater systems: https://www.cisa.gov/news-events/alerts/2023/11/28/exploitation-unitronics-plcs-used-water-and-wastewater-systems
- CISA advisory on compromise of a U.S. water treatment facility: https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-042a

---
*Feature research for: smart water treatment plant monitoring and control platform*
*Researched: 2026-03-31*
