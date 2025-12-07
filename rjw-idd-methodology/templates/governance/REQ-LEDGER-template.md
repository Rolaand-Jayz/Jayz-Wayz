# Requirement Ledger

> Copy this file into your project workspace (for example `artifacts/ledgers/requirement-ledger.md`). Do not edit the template in-place.

Track all requirements, their implementation status, and traceability to specifications, tests, and evidence.

## Active Requirements

| req_id | title | status | priority | spec_ids | test_ids | evidence_ids | owner | due_date |
|--------|-------|--------|----------|----------|----------|--------------|-------|----------|
| `REQ-0001` | Requirement title | Draft/Review/Approved/Done | Critical/High/Medium/Low | `SPEC-####` | `TEST-####` | `EVD-####` | Role | YYYY-MM-DD |

## Status Definitions

| Status | Description |
|--------|-------------|
| **Draft** | Requirement identified but not yet reviewed |
| **Review** | Under stakeholder review |
| **Approved** | Accepted for implementation |
| **In Progress** | Implementation underway |
| **Done** | Implemented and verified |
| **Deprecated** | No longer applicable |
| **Blocked** | Awaiting dependency resolution |

## Coverage Summary

| Category | Total | Draft | Review | Approved | In Progress | Done | Deprecated |
|----------|-------|-------|--------|----------|-------------|------|------------|
| Functional | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Quality | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Security | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Observability | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Integration | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Cost | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Traceability Gaps

List requirements missing specifications, tests, or evidence links:

| req_id | missing_artefact_type | action_required | owner | due_date |
|--------|----------------------|-----------------|-------|----------|
| `REQ-####` | Specification | Create SPEC | Role | YYYY-MM-DD |

## Guidelines

1. **Unique IDs:** Use `REQ-####` format, incrementing sequentially.
2. **Traceability:** Every requirement should link to at least one specification and one test.
3. **Evidence:** High-priority requirements should link to supporting evidence.
4. **Review Cadence:** Review ledger weekly during active development phases.
5. **Gap Resolution:** Address traceability gaps before phase transitions.

## Cross-References

- Specifications: `specs/SPEC-####.md`
- Tests: `tests/TEST-####.md`
- Evidence: `research/evidence/EVD-####.md`
- Change Log: `docs/change-log.md`
