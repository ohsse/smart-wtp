# Pitfalls Research

**Domain:** Real-time monitoring and control backend for a smart water treatment plant with AI-assisted control paths
**Researched:** 2026-03-31
**Confidence:** HIGH

Phase mapping below is an inference from the project context and current OT, alarm-management, data-quality, and AI-governance guidance.

## Recommended Prevention Phases

These phase labels are referenced throughout the pitfalls section so roadmap planning can attach each risk to a concrete milestone.

| Phase | Purpose |
|-------|---------|
| Phase 1: OT Safety Envelope and Telemetry Contract | Define assets, tags, units, timestamps, quality flags, safe ranges, interlocks, and authoritative control constraints. |
| Phase 2: Command and Mode Orchestration | Implement AI/manual/maintenance mode state machines, command IDs, acknowledgements, and edge-vs-backend control boundaries. |
| Phase 3: Alarm Management and Operator Workflow | Rationalize alarms, separate alarms from events, and design operator response flows that survive upset conditions. |
| Phase 4: Historian, Observability, and Forensics | Build end-to-end traces for telemetry, model inference, operator actions, control commands, and PLC acknowledgements. |
| Phase 5: AI Governance, Drift Monitoring, and Change Control | Start in shadow mode, monitor drift and performance, gate autonomous control, and version control models and configuration changes. |
| Phase 6: OT Security Hardening and Commissioning | Enforce zoning/DMZ, remote access controls, recovery drills, site acceptance, and final readiness checks before wider rollout. |

## Critical Pitfalls

### Pitfall 1: Letting AI outputs bypass the independent safety envelope

**What goes wrong:**
The backend turns model output directly into actuator commands or setpoint changes without an independent check against interlocks, safe operating ranges, rate-of-change limits, or fallback rules. A model can be statistically "good" and still unsafe for the current plant state.

**Why it happens:**
Teams collapse optimization, prediction, and actuation into one service and treat AI confidence as permission to control. They also confuse supervisory optimization with the deterministic logic that belongs in PLC or safety layers.

**How to avoid:**
Keep hard real-time and safety-critical logic at or near the physical process. The backend should issue only bounded supervisory commands that pass an explicit policy engine: current mode, current interlock state, safe envelope, max delta, command cooldown, and fallback action. Start AI in advisory or shadow mode, then enable closed-loop control only after replay, simulation, and operator sign-off.

**Warning signs:**
- A model score maps 1:1 to a device command.
- No document defines safe operating envelopes per controllable asset.
- Loss of the backend or network would stop automatic control rather than degrade gracefully.
- There is no kill switch, no command hold state, and no replay test pack for control logic.

**Phase to address:**
Phase 1: OT Safety Envelope and Telemetry Contract

---

### Pitfall 2: Blurring AI mode, manual mode, and maintenance bypass into one command path

**What goes wrong:**
Manual approvals are bypassed by retries, scheduler jobs, or background services because the system uses one generic "send command" path with a mode flag. Operators cannot trust whether a command came from AI, a person, or maintenance work.

**Why it happens:**
Mode is implemented as a UI label or a loose device attribute instead of a server-enforced state machine with transition rules, ownership, and command authorization.

**How to avoid:**
Model mode as an authoritative backend state with explicit transitions, required confirmations, timeout rules, and per-mode permissions. Separate event types for AI recommendation, AI actuation, manual request, manual approval, maintenance override, and PLC acknowledgement. Every command should be rejected if the current confirmed mode does not permit it.

**Warning signs:**
- The same endpoint accepts both AI and manual commands with an optional flag.
- Operators can issue commands while AI mode is active without a clear precedence rule.
- Maintenance or commissioning bypass is handled outside the platform in spreadsheets or verbal procedure.
- Incident review cannot answer who or what had control authority at a specific time.

**Phase to address:**
Phase 2: Command and Mode Orchestration

---

### Pitfall 3: Treating raw telemetry as trustworthy instead of quality-scored plant evidence

**What goes wrong:**
The platform stores and acts on sensor and PLC data without validating timestamps, units, calibration state, staleness, stuck values, impossible rates of change, or quality flags. Bad data leaks into dashboards, alarms, aggregates, and AI control.

**Why it happens:**
Greenfield teams optimize ingestion throughput first and postpone quality logic. OT point metadata lives in PLC tags, vendor docs, or operator knowledge rather than in one canonical contract the backend can enforce.

**How to avoid:**
Create a tag and asset registry that defines engineering units, sampling cadence, timezone, source timestamp, calibration interval, expected range, quality bit semantics, and substitution rules. Run automatic QC checks at ingest, preserve source quality flags, and quarantine suspect data from control decisions until reviewed. Use duplicate sensors and historian reconciliation where the process warrants it.

**Warning signs:**
- Flatlined or repeated values are treated as normal plant stability.
- The same point appears with conflicting units or scale in different screens.
- Daylight saving, timezone, or clock skew issues change event order.
- Operators say the data "looks wrong" but the backend has no quality indicator to explain why.

**Phase to address:**
Phase 1: OT Safety Envelope and Telemetry Contract

---

### Pitfall 4: Building a control backend that behaves like an alarm spammer

**What goes wrong:**
Every threshold breach becomes an alarm, events and alarms are mixed together, and upset conditions produce floods that operators cannot act on. The result is alarm blindness, shelving abuse, and missed real abnormalities.

**Why it happens:**
The team implements notifications before it defines an alarm philosophy, rationalization process, priority rules, and KPIs for alarm health.

**How to avoid:**
Adopt an ISA-18.2-style alarm lifecycle early. Separate alarms from events, warnings, and diagnostics. Rationalize each alarm with cause, operator response, consequence, priority, and suppression logic. Track alarm rates, standing alarms, chattering alarms, shelved alarms, and alarm flood windows as first-class operational metrics.

**Warning signs:**
- Operators mute, ignore, or work around alarms.
- One process upset generates cascades of near-duplicate alarms.
- There is no list of "top bad actors" by alarm volume or standing duration.
- Alarms exist without defined operator action or response time.

**Phase to address:**
Phase 3: Alarm Management and Operator Workflow

---

### Pitfall 5: Missing end-to-end observability for control decisions and plant response

**What goes wrong:**
After a bad command or missed action, nobody can reconstruct the exact chain: source telemetry, model version, feature window, operator input, command payload, PLC acknowledgement, resulting process values, and elapsed time between each step.

**Why it happens:**
Application logs, telemetry history, and OT events are implemented as separate concerns. Teams collect debugging logs but not immutable operational evidence.

**How to avoid:**
Make every control-relevant event traceable with shared correlation IDs and synchronized clocks. Persist an immutable decision record for recommendations, approvals, commands, acknowledgements, rejects, and overrides. Retain enough context to replay a control decision offline, including input features, model version, rule checks, and plant state snapshots.

**Warning signs:**
- Incident review depends on screenshots or operator memory.
- Different systems disagree on the order or time of the same event.
- There is no single query that answers "why did this device move?"
- Model outputs are logged only when debugging is manually enabled.

**Phase to address:**
Phase 4: Historian, Observability, and Forensics

---

### Pitfall 6: Pushing tight control loops through general-purpose backend and messaging layers

**What goes wrong:**
Round trips through REST, Kafka, schedulers, or cloud-hosted inference sit in the critical path for time-sensitive control. Normal latency variance, retries, or outages then become process risk instead of just software inconvenience.

**Why it happens:**
Teams prefer one centralized architecture for everything and defer the hard distinction between supervisory control and deterministic local control. "Real-time" is treated as "fast enough on average" instead of "bounded and predictable."

**How to avoid:**
Allocate each control function to the layer that matches its timing and safety needs. Keep deterministic loops in PLC or edge control. Use the backend for optimization, advisory logic, setpoint proposals, schedule changes, and longer-horizon coordination. Define explicit latency budgets and degraded-operation behavior before implementation.

**Warning signs:**
- Automatic control stops when Kafka backs up or the API is unavailable.
- No one can state the acceptable end-to-end latency budget for each control path.
- PLC logic waits on backend acknowledgements to continue a process.
- Pilot testing only measures average latency, not worst-case timing and packet loss behavior.

**Phase to address:**
Phase 2: Command and Mode Orchestration

---

### Pitfall 7: Treating OT connectivity and remote control like a normal web application

**What goes wrong:**
HMIs, APIs, engineering workstations, or vendor tunnels end up too exposed. Flat connectivity makes it easy for the wrong user, the wrong workstation, or the wrong network segment to reach control functions.

**Why it happens:**
The project inherits enterprise IT defaults and convenience-driven remote access patterns instead of designing an OT-specific zone model, jump points, and control-path restrictions.

**How to avoid:**
Design the network and trust boundaries with OT zoning and a DMZ from the start. Inventory every path that can read or write control data. Use strong identity for remote commands, time-bounded remote sessions, least privilege, and the ability to quickly disable remote control paths. Do not expose control HMIs or PLC-adjacent services directly to the internet.

**Warning signs:**
- The network map is incomplete or out of date.
- Shared service accounts are used for plant commands.
- Corporate VPN access reaches OT services without an additional controlled boundary.
- The team cannot enumerate all remote access methods into the plant.

**Phase to address:**
Phase 6: OT Security Hardening and Commissioning

---

### Pitfall 8: Shipping models, tag maps, and control parameters without formal change control

**What goes wrong:**
Seemingly small config or model updates silently change plant behavior. A tag remap, scaling factor change, feature definition tweak, or retrained model can alter commands more than an application code release would.

**Why it happens:**
Control configuration and ML artifacts are treated as data, not as safety-relevant releases. Spreadsheets, database rows, and ad hoc scripts become the true control surface outside version control and approval flow.

**How to avoid:**
Version and review tag maps, feature definitions, setpoints, model artifacts, and decision rules exactly like code. Require offline replay, impact analysis, rollback plans, and operations sign-off for control-relevant changes. Keep previous approved baselines and make current-vs-approved diffs easy to inspect.

**Warning signs:**
- "We only changed config" is used to explain behavior drift.
- Current plant mappings cannot be compared to the last approved baseline.
- Model performance is reported from training data, not current production behavior.
- There is no controlled shadow period before enabling a new model for actuation.

**Phase to address:**
Phase 5: AI Governance, Drift Monitoring, and Change Control

## Technical Debt Patterns

Shortcuts that look efficient in an MVP but are expensive in plant operations.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Single generic `POST /commands` endpoint with a `mode` field | Fastest way to demo control | Mode leakage, weak auditability, unsafe retries | Never for production control |
| Inferring units and scale from tag names | Low setup effort | Silent mis-scaling, wrong thresholds, broken analytics | Never |
| Using the primary OLTP schema as the raw historian | Fewer moving parts | Query contention, retention pain, poor replay support | Only for very small pilot loads with short retention and no closed-loop control |
| Letting the model service call PLC adapters directly | Fewer services | AI bypasses policy checks and mode gates | Never |
| Logging model inputs only on error | Lower storage cost | No forensic replay, no drift analysis, blind postmortems | Never once any recommendation can influence operator action |
| Treating maintenance bypass as an undocumented operator convention | Faster commissioning | Hidden authority changes and unsafe state transitions | Never |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| PLC/SCADA tag ingestion | Assuming tag names, scaling, and quality bits are stable across sites or firmware changes | Version a canonical tag registry with units, ranges, quality semantics, and per-site mappings |
| Kafka-backed processing | Driving direct actuation off at-least-once events without dedupe or command identity | Use explicit command IDs, acknowledgement states, idempotency rules, and policy checks before actuation |
| Python ML outputs | Passing only a score or setpoint with no feature window, model version, or data-quality context | Define a strict inference contract: model version, feature timestamps, confidence, quality summary, and intended use mode |
| PostgreSQL + JPA/MyBatis | Mixing high-frequency telemetry writes, control transactions, and dashboard queries in the same access path | Partition telemetry, isolate control transactions, and keep read models separate from command-critical writes |
| Operator UI / REST API | Relying on the client to enforce manual approvals or control authority | Enforce approvals, mode rules, and authority checks on the server side with immutable audit events |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Persisting every sample through ORM-managed entities | Rising write latency, GC pressure, lock contention | Use bulk ingestion paths, partitioning, and telemetry-specific schemas | Usually breaks once high-frequency points and history retention both grow |
| Computing dashboards from raw telemetry tables | Slow trend screens and aggregate queries during plant load | Pre-aggregate, materialize read models, and separate raw from presentation queries | Breaks early when dashboards, alarms, and reports hit the same tables |
| Running model inference inline on control request paths | Command latency spikes during model load or Python runtime issues | Decouple inference from hard command timing, cache noncritical results, and precompute where possible | Breaks during upset conditions, deploys, or model cold starts |
| Polling PLCs too aggressively from multiple services | Network saturation, stale reads, inconsistent timestamps | Centralize polling responsibility and distribute normalized streams downstream | Breaks as more features or teams add their own pollers |
| Replaying historical events without time-bounded tooling | Recovery jobs overload live systems | Build dedicated replay pipelines with rate controls and isolation | Breaks during incident recovery and backfill operations |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Internet-reachable HMI or control API | Unauthorized viewing or control changes | Keep control-plane services behind OT boundaries, managed access paths, and strong authentication |
| Flat IT/OT network | Lateral movement into plant systems | Use zones, conduits, and a DMZ with least-privilege traffic flows |
| Shared operator, service, or vendor accounts | No accountability for control actions | Use individual identities, scoped service accounts, and session-based access for remote work |
| Remote vendor tunnel left permanently enabled | Persistent hidden control path | Inventory every remote path, time-box access, and require explicit enable/disable controls |
| Uncontrolled active scanning or agent deployment in OT | Unexpected device instability | Validate tooling in representative environments and use OT-aware discovery methods |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Control mode is not always visible and current | Operators act on stale assumptions about who has authority | Show authoritative mode, owning actor, last change time, and pending transitions on every control screen |
| AI recommendations are opaque | Operators either distrust them or follow them blindly | Show key inputs, constraints checked, confidence, expected effect, and why the system refused or proposed a change |
| Alarm list mixes alarms, events, and diagnostics | Operators cannot prioritize response under stress | Use separate views and strong visual distinctions for alarms vs informational events |
| Data freshness and quality are hidden | Operators mistake stale or suspect data for live truth | Display source timestamp, latency, quality flag, and fallback status beside every critical value |
| Manual approvals do not show downstream state | Operators are unsure whether a command was requested, sent, acknowledged, or applied | Make command lifecycle states explicit from request through PLC acknowledgement and observed process response |

## "Looks Done But Isn't" Checklist

- [ ] **AI mode:** Has a kill switch, shadow period, safe envelope checks, and fallback behavior when telemetry quality drops.
- [ ] **Manual mode:** Server-side authority and approval rules are enforced even if the UI is bypassed.
- [ ] **Telemetry ingestion:** Every critical point has units, ranges, quality bits, source timestamp, and calibration metadata.
- [ ] **Audit trail:** A command can be traced from plant state and model input through operator action, issuance, acknowledgement, and resulting plant response.
- [ ] **Alarming:** Alarm priorities, suppression rules, flood KPIs, and standing-alarm reviews are defined.
- [ ] **Security:** OT zone map, DMZ, remote access inventory, and control-path identity model exist and have been reviewed.
- [ ] **Release process:** Model, rule, and tag-map changes require replay testing, sign-off, and rollback plans.

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| AI bypassed safety envelope | HIGH | Disable autonomous actuation, revert to manual or bounded advisory mode, restore last approved ruleset, review commands issued, and replay the incident with preserved evidence |
| Mode separation failure | HIGH | Freeze command issuance, reconcile authoritative device modes from PLC state, invalidate stale sessions, review recent commands, and patch transition rules before re-enabling control |
| Data quality corruption | MEDIUM to HIGH | Mark affected intervals as suspect, stop control decisions that depend on those points, backfill from trusted history if possible, and recalibrate or remap the affected sensors |
| Alarm flood | MEDIUM | Temporarily suppress nonactionable nuisance alarms, stabilize the process upset, identify flood sources, and rationalize bad-actor alarms before returning to normal thresholds |
| Missing observability | HIGH | Switch to conservative operation, preserve all available logs and historian data, add temporary correlation and decision capture, and do not resume autonomous mode until forensic gaps are closed |
| Unsafe config or model release | HIGH | Roll back to the previous approved baseline, compare current-vs-approved mappings and model versions, rerun replay tests, and require formal sign-off for the next attempt |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| AI outputs bypass safety envelope | Phase 1: OT Safety Envelope and Telemetry Contract | Every autonomous command is blocked unless safe-range, interlock, and quality predicates pass in replay and integration tests |
| AI/manual/maintenance mode leakage | Phase 2: Command and Mode Orchestration | Invalid mode transitions and wrong-mode commands are rejected and fully audited in automated tests |
| Bad telemetry enters control path | Phase 1: OT Safety Envelope and Telemetry Contract | Stale, stuck, out-of-range, and wrong-unit samples are flagged or quarantined before reaching dashboards or control logic |
| Alarm spam replaces alarm management | Phase 3: Alarm Management and Operator Workflow | Alarm KPIs stay within agreed thresholds during simulation and pilot operation |
| No forensic trail for decisions | Phase 4: Historian, Observability, and Forensics | A sample incident can be reconstructed end to end from one correlation ID and synchronized timestamps |
| General-purpose backend in tight loop | Phase 2: Command and Mode Orchestration | Latency budgets and degraded-mode behavior are documented and validated under fault injection |
| OT network exposed like IT | Phase 6: OT Security Hardening and Commissioning | Network review confirms zoning, DMZ boundaries, approved remote paths, and no direct internet exposure for control-plane assets |
| Config and model releases bypass MOC | Phase 5: AI Governance, Drift Monitoring, and Change Control | Every control-relevant config and model change has versioning, replay evidence, approval, and rollback data |

## Sources

- NIST SP 800-82 Rev. 3, *Guide to Operational Technology (OT) Security* (official, HIGH): https://doi.org/10.6028/NIST.SP.800-82r3
- NIST, *Artificial Intelligence Risk Management Framework (AI RMF 1.0)* and Playbook resources (official, HIGH): https://www.nist.gov/itl/ai-risk-management-framework
- ISA, *ISA-18.2 Alarm Management* overview and lifecycle references (official, HIGH): https://isaeurope.com/alarm-management/
- ISA, *Open Process Automation Forum Launches New Use Cases in Cloud OT and AI* (official, MEDIUM-HIGH). Used for the current industry direction that real-time closed-loop control should remain local to the physical process: https://www.isa.org/about-isa/press-room/press-releases/2025/open-process-automation-forum-launches-new-use-cases-in-cloud-ot-and-ai
- US EPA, *Smart Sewers* and real-time decision support material (official, MEDIUM-HIGH): https://www.epa.gov/npdes/smart-sewers
- US EPA, *Quality Assurance for Air Sensors* and *ContDataQC* resources. Used as current official guidance for continuous sensor QC patterns such as timestamp checks, calibration, stuck values, and anomaly review (official, MEDIUM): https://www.epa.gov/air-sensor-toolbox/quality-assurance-air-sensors and https://assessments.epa.gov/risk/document/%26deid%3D365551
- CISA, *Recommended Practices for Securing Industrial Control Systems* and OT asset inventory guidance (official, HIGH): https://www.cisa.gov/resources-tools/resources/recommended-practices-securing-industrial-control-systems and https://www.cisa.gov/resources-tools/resources/foundations-ot-cybersecurity-asset-inventory-guidance-owners-and-operators
- CISA advisory on internet-accessible HMIs and insecure OT remote access patterns (official, HIGH): https://www.cisa.gov/news-events/cybersecurity-advisories/aa22-103a
- Microsoft Learn, *Azure Machine Learning model monitoring* (official vendor documentation, MEDIUM). Used to confirm current production monitoring patterns for drift, data quality, and performance thresholds: https://learn.microsoft.com/en-us/azure/machine-learning/concept-model-monitoring?view=azureml-api-2

---
*Pitfalls research for: smart water treatment plant operations backend*
*Researched: 2026-03-31*
