# SPEC-3D-BUILD-0001 — Build, Toolchain & Deployment

- **Active Profile:** `<features.yml :: addons.3d_game_core.profile>`
- **Decisions:** `DEC-3D-BUILD-0001` (CI lane strategy), `DEC-3D-BUILD-0002` (platform coverage)

## 1. Targets & Outputs
- Enumerate supported platforms, architectures, and distribution storefronts.
- Map each to build flavours (debug, profile, release, certification) and pipeline steps.

## 2. Toolchain Stack
- Engine versioning/branch map, compiler toolsets, SDK dependencies.
- Automated validation: asset linter, perf gate, determinism & rollback harness runs.
- Packaging & patching flow with rollback capability.

## 3. Build Farm Operations
- Queue sizing, parallelism, caching, artifact retention.
- Integration with scripts under `scripts/addons/` for toggling add-in features in CI.

## 4. Observability & Reporting
- Logging & artifact capture for each lane (tap metrics schema, harness outputs).
- Escalation path when budgets or deterministic checks fail.

## 5. Acceptance Criteria
- `TEST-3D-BUILD-AC01`: CI lanes include add-in tools only when feature flag enabled.
- `TEST-3D-BUILD-AC02`: Re-running `enable_3d_game_core.py` after successful build is a no-op.
- `TEST-3D-BUILD-AC03`: Build outputs attach perf metrics JSON & replay artefacts for audit.

## 6. Traceability
| Artefact | Identifier |
| --- | --- |
| Requirements | `REQ-3D-BUILD-*` |
| Decisions | `DEC-3D-BUILD-*` |
| Tests | `TEST-3D-BUILD-*` |
| Integrations | `INTEG-3D-BUILD-*`, `INTEG-3D-CI-*` |

> **Profile Hint:** Document any platform-specific constraints (e.g., console TRCs) and map them back to profile budgets so the enable script can warn when switching between profiles with different targets.
