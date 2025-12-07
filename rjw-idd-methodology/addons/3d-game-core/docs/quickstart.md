# DOC-3D-QUICKSTART-0001 — 3D Game Core Quickstart

## 1. Sprint Zero Checklist
1. Confirm opt-in intention with `DEC-3D-ADOPTION-0001`.
2. Validate repository cleanliness and capture baseline metrics.
3. Run `python scripts/addons/enable_3d_game_core.py` (no effect if already enabled).
4. Choose a profile via `python scripts/addons/set_3d_profile.py --profile <profile>`.
5. Record the chosen profile in `DEC-3D-PROFILE-0001` and cite this document.

## 2. Artefact Flow
| Phase | Artefact | Prompt | Spec |
| --- | --- | --- | --- |
| Research | `REQ-3D-*` | `PROMPT-3D-0001` | — |
| Design | `GDD`, `Engineering Spec` | `PROMPT-3D-0002` | `SPEC-3D-GDD-0001`, `SPEC-3D-ENGINE-0001` |
| Verification | Test Navigator | `PROMPT-3D-0003` | `SPEC-3D-PERF-0001`, `SPEC-3D-AI-0001`, `SPEC-3D-NET-0001` |
| Operations | Pact drafting | `PROMPT-3D-0004` | `docs/pacts_examples.md` |
| Governance | Doc reconciler | `PROMPT-3D-0005` | All specs |

## 3. Tool Wiring
- Determinism Harness: provide a `--tape` file exported from your engine (start with `ci_samples/determinism_tape.json`).
- Tolerant Replay Runner: map engine snapshot dumps to the schema described in `docs/metrics_schema.md` under `snapshots`.
- Rollback Harness: duplicate predicted vs. authoritative streams, referencing profile rollback thresholds.
- Asset Linter: point `--assets` to your asset root; customise rules via profile overlays.
- Performance Gate: export metrics JSON and validate locally before pushing to CI.

## 4. Metrics Integration
1. Review adapter stubs in `addons/3d-game-core/tools/engine_adapters/`.
2. Implement non-invasive exporters that save artefacts under `BuildArtifacts/`.
3. Update `scripts/addons/verify_3d_game_core.py` configuration if additional required fields are introduced.
4. Attach metrics JSON and tapes as CI artefacts for reproducibility.

## 5. Disable / Rollback
- Run `python scripts/addons/disable_3d_game_core.py` to remove docs/CI links and reset the feature flag.
- Delete project-only artefacts (build outputs, tapes) manually if they were generated outside repo scope.

> Capture every deviation in a `DEC-3D-*` record to preserve traceability when toggling profiles or disabling the add-in.
