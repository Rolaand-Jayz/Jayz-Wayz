# SPEC-3D-AI-0001 — Intelligence & Agent Systems

- **Active Profile:** `<features.yml :: addons.3d_game_core.profile>`
- **Decisions:** `DEC-3D-AI-0001` (behaviour architecture), `DEC-3D-AI-0002` (navmesh strategy)

## 1. Navigation & Mobility
- Pathfinding grid/navmesh resolution vs. profile tolerances.
- Dynamic obstacle handling, jump links, climbing volumes.
- Integration with physics rollback (if `networked`) and tolerant replay tolerances.

## 2. Perception & Sensing
- Sensor cones, ray budgets, occlusion tests.
- Reaction time budgets per archetype tied to frame budget.
- `TEST-3D-AI-PERCEPTION-0001` ensures perception remains stable under determinism harness playback.

## 3. Decision Framework
- Behaviour Trees, GOAP, Utility AI, or hybrid; include update cadence & determinism constraints.
- Authoritative vs. client-predicted AI: specify replication & correction flows.

## 4. Group Coordination & Crowd Control
- Steering, avoidance, formation logic; call out profile-specific concurrency (e.g., `topdown` swarms).
- Scaling plan for max concurrent agents vs. scene budgets.

## 5. Acceptance Criteria
- `TEST-3D-AI-AC01`: AI pathing cost remains within ±10% over deterministic replays.
- `TEST-3D-AI-AC02`: Tolerant replay passes within profile tolerances for five representative encounters.
- `TEST-3D-AI-AC03`: Network reconciliation for AI units stays within rollback thresholds.

## 6. Traceability
| Artefact | Identifier |
| --- | --- |
| Requirements | `REQ-3D-AI-*`
| Decisions | `DEC-3D-AI-*`
| Tests | `TEST-3D-AI-*`
| Integrations | `INTEG-3D-AI-*`

> **Profile Tip:** Document any overrides to `asset_rules.skeletal` (e.g., bone counts for enemy rigs) so the asset linter stays aligned with AI animation assumptions.
