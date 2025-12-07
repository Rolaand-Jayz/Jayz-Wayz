# PROMPT-3D-0003 — Test Navigator (3D)

**Goal:**
Produce a risk-driven test plan aligning with determinism, tolerant replay, rollback, asset, and perf gates for the active profile.

**Assistant Inputs:**
- GDD + Engine + Perf specs (`SPEC-3D-*`).
- Merged config/profile budgets & tolerances.

**Requested Output:**
1. Laddered test suites (unit, integration, soak, CI gates) referencing `TEST-3D-*` IDs.
2. Mapping of each suite to tooling (`determinism_harness.py`, `tolerant_replay_runner.py`, `rollback_sim_harness.py`, `asset_linter_3d.py`, `perf_budget_gate_3d.py`).
3. Matrix linking risks → mitigations → evidence targets.
4. Highlight automation gaps requiring new harness adapters or metrics exporters.

**Format:**
- Markdown with sections per risk area and tables capturing traceability from `REQ-####` to `TEST-####` and `INTEG-####`.
