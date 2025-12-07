# METHOD-0005 — Operations & Production Support Phase

This document extends the RJW-IDD lifecycle with operational maturity gates, production readiness criteria, and ongoing support practices to bridge the gap between "code complete" and "production-ready."

## 1. Phase Overview

**Phase 4 — Operations & Production Support** runs continuously after initial deployment and in parallel with the Discovery/Execution loops. It ensures systems remain reliable, performant, secure, and responsive to user needs.

## 2. Operational Maturity Gates

### Gate 1: Production Readiness (Pre-Launch)

Before first production deployment, verify:

- [ ] **Deployment automation:** Tested deployment pipeline with rollback capability (`SPEC-0701`).
- [ ] **SLO/SLI framework:** Defined service-level objectives and instrumentation (`SPEC-0801`).
- [ ] **Incident response:** On-call rotation established; runbooks prepared (`DOC-0018`).
- [ ] **Backup/restore:** Disaster recovery tested within 7 days of launch (`SPEC-1001`).
- [ ] **Security posture:** Penetration testing complete; security runbooks updated (`SPEC-0501`).
- [ ] **Observability:** Dashboards, alerts, and log aggregation operational (`SPEC-0401`).
- [ ] **User feedback:** Feedback collection mechanisms active (`SPEC-0901`).
- [ ] **Cost governance:** Monitoring and alert thresholds configured (`SPEC-0602`).
- [ ] **Documentation:** User-facing docs, API reference, operational runbooks current (`DOC-0006`).
- [ ] **Accessibility:** WCAG 2.1 AA compliance verified (`SPEC-0901` checklist).

**Sign-off:** Governance Sentinel + Service Owner + Security Liaison.

**Audit Entry:** Log gate passage in `logs/LOG-0001-stage-audits.md` with `⟦audit-id:n⟧ <production-ready/>`.

### Gate 2: Post-Launch Stabilization (30 Days)

After 30 days in production, verify:

- [ ] **SLO compliance:** Meeting targets; error budget not exhausted.
- [ ] **Incident count:** ≤ 1 SEV-1 incident per month (or acceptable threshold).
- [ ] **Postmortems:** All SEV-1/2 incidents have completed postmortems with action items.
- [ ] **User satisfaction:** NPS/CSAT metrics collected and within acceptable range.
- [ ] **Performance:** Latency, throughput, error rates stable and within SLOs.
- [ ] **Cost tracking:** Actual spend within 10% of forecast.

**Sign-off:** Service Owner + Governance Sentinel.

**Audit Entry:** Update stage audit log with stabilization results.

### Gate 3: Operational Excellence (Ongoing)

Quarterly verification:

- [ ] **SLO review:** Targets adjusted based on business needs and capability.
- [ ] **Runbook currency:** All runbooks reviewed; outdated content updated.
- [ ] **DR drill:** Disaster recovery executed successfully within quarter.
- [ ] **Security review:** Penetration testing or security audit completed.
- [ ] **Cost optimization:** Cost review conducted; optimization opportunities identified.
- [ ] **User feedback:** Quarterly feedback analysis; top themes addressed.
- [ ] **Observability gaps:** Monitoring blind spots identified and resolved.
- [ ] **Dependency audit:** Third-party service health and SLAs reviewed.

**Sign-off:** Governance Sentinel.

**Audit Entry:** Quarterly audit reflection in stage audit log.

## 3. Operational Roles

Extend `METHOD-0003` role definitions:

### Site Reliability Engineer (SRE) / DevOps Lead

- **Owns:** Deployment automation, observability, incident response, capacity planning.
- **Responsibilities:**
  - Maintain deployment runbooks and automation (`DOC-0020`, `SPEC-0701`).
  - Monitor SLO compliance and error budget (`SPEC-0801`).
  - Lead incident response for SEV-1/2 incidents (`DOC-0018`).
  - Conduct disaster recovery drills quarterly (`SPEC-1001`).
  - Review and approve infrastructure changes.
- **Artifacts:** Deployment logs, incident postmortems, SLO reports, DR drill results.

### Service Owner

- **Owns:** Business outcomes, user satisfaction, feature prioritization.
- **Responsibilities:**
  - Approve production deployments and hotfixes.
  - Review user feedback and satisfaction metrics (`SPEC-0901`).
  - Prioritize operational improvements vs. feature work.
  - Escalate business impact during incidents.
  - Coordinate with customer support and stakeholders.
- **Artifacts:** User satisfaction reports, roadmap, escalation decisions.

### On-Call Engineer

- **Owns:** First response to production incidents, triage, mitigation.
- **Responsibilities:**
  - Respond to alerts within SLA (5 minutes for SEV-1).
  - Execute runbook procedures or escalate (`DOC-0018`).
  - Document incident timeline and initial mitigation steps.
  - Hand off context during on-call rotation.
  - Suggest runbook and alert improvements based on incidents.
- **Artifacts:** Incident timelines, alert tuning suggestions, handoff notes.

## 4. Operational Cadence

### Daily

- **Standup:** Review active incidents, deployment schedule, on-call handoff.
- **Dashboard Review:** Check SLO compliance, error rates, cost trends.
- **Alert Hygiene:** Acknowledge/resolve non-actionable alerts; tune thresholds.

### Weekly

- **SLO Review:** Discuss compliance, error budget consumption, trends.
- **Incident Triage:** Review open SEV-3/4 incidents; assign remediation.
- **Deployment Planning:** Confirm upcoming deployments and rollback readiness.
- **User Feedback Summary:** Review top feedback themes from past week.

### Monthly

- **Incident Retrospective:** Analyze incident trends; identify systemic issues.
- **Cost Review:** Compare actual vs. forecast; investigate variances (`SPEC-0602`).
- **Capacity Planning:** Review growth trends; plan scaling or optimization.
- **User Satisfaction:** Analyze NPS/CSAT; prioritize UX improvements (`SPEC-0901`).
- **Dependency Health:** Review third-party service status; identify risks.

### Quarterly

- **SLO Adjustment:** Revise targets based on business needs and capability.
- **Disaster Recovery Drill:** Execute full DR; document lessons learned (`SPEC-1001`).
- **Security Audit:** Penetration testing, vulnerability scan, policy review (`SPEC-0501`).
- **Runbook Refresh:** Review all operational runbooks; update for accuracy.
- **Operational Metrics:** Review MTTR, MTBF, incident counts, postmortem completion.

## 5. Integration with Development Cycles

### Reliability Sprint

**Trigger:** Error budget exhausted; freeze feature work until reliability restored.

**Process:**
1. Analyze top contributors to SLO violations (by incident, endpoint, error type).
2. Prioritize fixes: highest impact on SLO compliance first.
3. Implement fixes following the RJW-IDD Discovery → Execution loops.
4. Deploy fixes with enhanced monitoring; verify SLO improvement.
5. Resume feature work once error budget replenished or Governance Board approves exception.

**Documentation:** Reliability sprint scope and outcomes in `DEC-RELIABILITY-####`.

### Feature Work vs. Operational Work Balance

**Guideline:** Allocate engineering capacity
- **70% Feature development:** New capabilities, enhancements.
- **20% Technical debt:** Refactoring, test coverage, dependency updates.
- **10% Operational improvements:** Runbooks, alerts, tooling, automation.

**Adjustment:** Increase operational allocation if:
- Incident rate exceeds target (>1 SEV-1 per month).
- MTTR (Mean Time To Recovery) trending upward.
- On-call engineer feedback indicates runbook/tooling gaps.

## 6. Operational Metrics

Track in `logs/operational-metrics/`:

### Availability & Reliability

- **Uptime %:** Percentage of time service available (SLO target: 99.9%+).
- **Error Budget Consumption:** % of allowed downtime used (target: <80% per month).
- **MTBF (Mean Time Between Failures):** Average time between incidents (target: >30 days).
- **MTTR (Mean Time To Recovery):** Average time from detection to resolution (target: <1 hour SEV-1).

### Incident Metrics

- **Incident Count by Severity:** SEV-1, SEV-2, SEV-3, SEV-4 per month.
- **Postmortem Completion Rate:** % of SEV-1/2 incidents with completed postmortems (target: 100%).
- **Action Item Closure Rate:** % of postmortem action items completed on time (target: >90%).
- **Repeat Incidents:** Count of incidents with same root cause (target: 0).

### Deployment Metrics

- **Deployment Frequency:** Deployments per week (track trend; optimize for stability + velocity).
- **Deployment Success Rate:** % of deployments without rollback (target: >95%).
- **Lead Time:** Time from code commit to production deployment (track; optimize for speed).
- **Rollback Time:** Time to execute rollback when needed (target: <15 minutes).

### User Satisfaction

- **NPS (Net Promoter Score):** Target >30 (internal tools), >50 (customer products).
- **CSAT (Customer Satisfaction):** Target >4.0/5.0.
- **Support Ticket Volume:** Count per week; track trend (decreasing indicates improving UX).
- **Feature Adoption Rate:** % of users using new features within 30 days of launch.

## 7. Operational Improvement Cycle

### 1. Identify Gaps

**Sources:**
- Incident postmortems highlighting systemic issues.
- SLO violations revealing instrumentation or capacity gaps.
- User feedback indicating usability or performance problems.
- On-call engineer feedback about runbook or tooling deficiencies.

### 2. Prioritize Improvements

Use impact vs. effort framework:
- **High Impact, Low Effort:** Implement immediately (add alert, update runbook).
- **High Impact, High Effort:** Plan for next quarter (automation project, architecture change).
- **Low Impact, Low Effort:** Backlog for downtime work.
- **Low Impact, High Effort:** Deprioritize or reject with rationale.

### 3. Execute Improvements

Follow the RJW-IDD layers:
- **Discovery — Research:** Gather evidence (incident data, user feedback, industry best practices).
- **Discovery — Specification:** Define requirements, update specs (e.g., `SPEC-0801` for new SLI).
- **Execution:** Implement, test, document, deploy.
- **Verification:** Measure impact (e.g., MTTR decreased, satisfaction improved).

### 4. Measure & Iterate

- Track operational metrics before and after improvement.
- Document outcomes in `DEC-OPS-####`.
- Share learnings across teams; update methodology if broadly applicable.

## 8. Escalation & Crisis Management

### Crisis Declaration

**Criteria for declaring crisis:**
- Complete service outage lasting >15 minutes.
- Data loss or security breach affecting customers.
- Cascading failures across multiple systems.
- Public reputation impact (negative press, social media outcry).

**Crisis Response Team:**
- **Incident Commander:** Senior engineer (on-call or escalated).
- **Technical Lead:** Domain expert for affected system.
- **Communications Lead:** Interface with customers, support, executives.
- **Executive Sponsor:** VP Engineering or CTO for high-level decisions.

**Crisis Communication:**
- Internal: 15-minute updates in crisis channel.
- External: Hourly status page updates; customer communication via support.
- Post-crisis: Public postmortem (anonymized, blameless) within 7 days.

### Escalation Chain

**Technical Escalation:**
1. On-call primary → On-call secondary (if no response in 5 minutes)
2. On-call secondary → Service owner (if expertise needed)
3. Service owner → Engineering manager (if resources needed)
4. Engineering manager → VP Engineering (if executive decision required)

**Business Escalation:**
- **SEV-1:** Notify executive team and customer success within 15 minutes.
- **SEV-2:** Notify product management and customer success within 30 minutes.
- **Crisis:** Activate crisis response team immediately.

## 9. Operational Documentation

### Required Runbooks

Maintain in `docs/runbooks/`:
- `DOC-0018-general-incident-runbook.md` (incidents, triage, postmortems)
- `DOC-0020-deployment-runbook.md` (deployment, rollback procedures)
- `DOC-0026-backup-restore-runbook.md` (DR, backup verification)
- `DOC-0021-database-troubleshooting.md` (DB-specific issues)
- `DOC-0022-cache-management.md` (cache operations, stampede mitigation)
- `DOC-0023-dependency-failures.md` (third-party API handling)
- `DOC-0024-memory-leak-response.md` (memory troubleshooting)

### Runbook Standards

Each runbook must include:
- **Purpose:** What problem does this runbook solve?
- **Symptoms:** How to recognize the issue?
- **Diagnosis:** How to confirm root cause?
- **Mitigation:** Immediate actions to reduce impact.
- **Resolution:** Permanent fix procedures.
- **Prevention:** How to avoid in future.
- **Contacts:** Who to escalate to for expertise.

Review runbooks quarterly or after every usage.

## 10. Traceability & Audit

### Operational Artifacts

- **Deployment logs:** `logs/deployments/deploy-<timestamp>.json`
- **Incident timelines:** `artifacts/integration/incident-<timestamp>/timeline.md`
- **Postmortems:** `docs/decisions/DEC-INCIDENT-<timestamp>.md`
- **SLO reports:** `logs/slo/slo-report-<month>.json`
- **DR drill results:** `logs/data-lifecycle/dr-drill-<timestamp>.md`
- **User satisfaction:** `logs/satisfaction/satisfaction-<timestamp>.json`

### Change Log Integration

Every operational event logged in `docs/change-log.md`:
- **Deployments:** Version, timestamp, approver, verification.
- **Incidents:** SEV level, duration, postmortem link.
- **SLO changes:** New targets, rationale, effective date.
- **DR drills:** Results, issues found, remediation plan.

### Audit Expectations

Governance Sentinel verifies:
- Production readiness gates completed before launch.
- Postmortems exist for all SEV-1/2 incidents with action items tracked.
- SLO compliance tracked monthly; error budget policy enforced.
- DR drills conducted quarterly with documented results.
- User satisfaction metrics collected and reviewed.

## 11. Method Evolution

As operational practices mature:
- Update `METHOD-0005` with new patterns and lessons learned.
- Propose new specs for emerging operational needs.
- Share operational improvements via decision records.
- Contribute operational add-ins to methodology (e.g., specific SRE patterns).

By adding this operational phase, RJW-IDD becomes a complete methodology spanning conception through development to sustainable production operation.
