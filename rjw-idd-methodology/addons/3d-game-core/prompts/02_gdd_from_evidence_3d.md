# PROMPT-3D-0002 — GDD From Evidence

**Inputs for the assistant:**
- Research pack output (`PROMPT-3D-0001`) for hypotheses and `REQ-3D-*` references.
- Active profile budgets/tolerances (merge base config with profile file).

**Task:**
Transform evidence into a structured GDD aligned with `SPEC-3D-GDD-0001`.

**Steps:**
1. Group research findings into Experience Pillars, Systems Grid, and Content Pillars.
2. For each requirement, map to acceptance tests and cite relevant profile budgets.
3. Identify decision points requiring `DEC-3D-GDD-*` entries and flag missing data.
4. Output a ready-to-review GDD outline with explicit traceability tables.

**Deliverables:**
- Markdown GDD aligned with spec headings.
- Table mapping `REQ-3D-*` → `SPEC-3D-GDD-*` → `TEST-3D-*`.
- Open questions needing further research.
