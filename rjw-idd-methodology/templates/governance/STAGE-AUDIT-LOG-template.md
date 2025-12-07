# LOG-XXXX — Stage Audit Reflections

> Copy this file into your project workspace (for example `logs/LOG-0001-stage-audits.md`). Do not edit the template in-place.

| audit_tag | date (UTC) | stage | summary | owners | follow_up |
|-----------|------------|-------|---------|--------|-----------|
| ⟦audit-id:1⟧ \<reflect/\> | YYYY-MM-DD | Stage name | Brief summary of audit findings. | Role names | Action items or `cleared` |

## Guidelines

### Audit Tag Format

- Use `⟦audit-id:n⟧` where `n` increments sequentially starting from 1.
- Append `<reflect/>` for standard reflections.
- Append `<production-ready/>` for production readiness gates.
- Append `<exit/>` for phase exit audits.

### Stage Names

- `Phase 0 — Governance Setup`
- `Discovery Research`
- `Discovery Specification`
- `Discovery→Execution`
- `Execution Readiness`
- `Execution→Release`
- `Production Readiness`
- `Post-Launch Stabilization`
- `Operational Excellence`

### Follow-Up Tracking

- Record concrete actions or mark `cleared` once work is complete.
- Reference related decision records (`DEC-####`) for significant findings.
- Link to change log entries (`change-YYYYMMDD-##`) when actions are completed.

### Sign-Off Requirements

Each audit should include sign-off from the responsible roles:

- **Discovery audits:** Evidence Lead, Spec Architect
- **Execution audits:** Execution Wrangler, Security Liaison
- **Production audits:** Governance Sentinel, Service Owner

## Cross-References

- Change Log: `docs/change-log.md`
- Phase Checklists: `METHOD-0002-phase-driver-checklists.md`
- Role Handbook: `METHOD-0003-role-handbook.md`
