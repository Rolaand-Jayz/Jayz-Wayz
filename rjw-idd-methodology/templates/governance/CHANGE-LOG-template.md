# RJW-IDD Method Change Log

> Copy this file into your project workspace (for example `docs/change-log.md`). Track every change with a unique `change-YYYYMMDD-##` identifier. Do not edit the template in-place.

Track every methodology or project update with a unique `change-YYYYMMDD-##` identifier. Each row binds decisions, evidence, and audit artefacts so teams can replay the history.

| change_id | date (UTC) | description | impacted_ids | operator | verification |
|-----------|------------|-------------|--------------|----------|--------------|
| change-YYYYMMDD-01 | YYYY-MM-DD | Description of the change. | SPEC-####;REQ-####;DEC-#### | Role/Name | validator:status; audit:⟦audit-id:n⟧ |

## Guidelines

1. **Unique Identifiers:** Use `change-YYYYMMDD-##` format, incrementing the suffix for multiple changes on the same day.
2. **Impacted IDs:** List all artefacts affected by this change using semicolon separators.
3. **Verification:** Reference validator outputs and audit tags to demonstrate the change was properly reviewed.
4. **Operator:** Record who made the change and their role.
5. **Description:** Keep descriptions concise but sufficient to understand the scope of the change.

## Cross-References

- Stage audits: `logs/LOG-0001-stage-audits.md`
- Decisions: `docs/decisions/DEC-####.md`
- Specifications: `specs/SPEC-####.md`
