# SPEC-3D-NET-0001 — Network & Rollback Blueprint

- **Active Profile:** `<features.yml :: addons.3d_game_core.profile>`
- **Decisions:** `DEC-3D-NET-0001` (topology), `DEC-3D-NET-0002` (transport, quality settings)

## 1. Topology & Authority
- Enumerate supported models: authoritative server, lockstep, rollback peer-to-peer.
- Map ownership of actors/components per model.
- Latency tiers and quality-of-service fallback plans.

## 2. Prediction & Rollback
- Input prediction pipeline, state buffering strategy, reconciliation flows.
- Maximum rollback depth and tick window tied to profile `rollback` thresholds.
- Integration checkpoints for `rollback_sim_harness.py` including instrumentation IDs `INTEG-3D-NET-ROLLBACK-*`.

## 3. Replication Schema
- Delta compression, relevancy culling, frequency scaling under load.
- Sensitive data handling (anti-cheat, tamper detection) with `DEC-3D-NET-SECURITY-*` references.

## 4. Monitoring & Observability
- Event hooks for net metrics (RTT, packet loss, misprediction rate) exported to telemetry spec.
- Alert thresholds matching `rollback.misprediction_rate_threshold`.

## 5. Acceptance Criteria
- `TEST-3D-NET-AC01`: Rollback harness reports rollback depth < profile threshold during stress tape.
- `TEST-3D-NET-AC02`: Tolerant replay drift remains within tolerances after reconciliation bursts.
- `TEST-3D-NET-AC03`: Network metrics feed into perf budget gate checks without schema violations.

## 6. Traceability
| Artefact | Identifier |
| --- | --- |
| Requirements | `REQ-3D-NET-*` |
| Decisions | `DEC-3D-NET-*` |
| Tests | `TEST-3D-NET-*`, `TEST-3D-ROLLBACK-*` |
| Integrations | `INTEG-3D-NET-*` |

> **Profile Note:** When `addons.3d_game_core.profile == networked`, treat these acceptance criteria as go/no-go gates; other profiles can downscope but must document deviations in `DEC-3D-NET-0003`.
