# DOC-3D-PACT-EXAMPLES-0001 — Cross-Team Pact Examples

## PACT-3D-0001 — Input ↔ Controller Systems
- **Objective:** Guarantee low-latency translation of player input into deterministic actions.
- **Profile Alignment:** `first_person`, `third_person`, `platformer`.
- **Contract:**
  - Input team ensures device sampling at ≥ 250 Hz; controller system buffers 120 ticks.
  - Shared seed table for randomised assists stored in `INTEG-3D-ENGINE-0001` bundle.
- **Budgets:** Round-trip latency < 40 ms (profile dependent).
- **Verification:** `TEST-3D-ENGINE-AC01`, determinism harness tapes.

## PACT-3D-0002 — Physics ↔ ECS
- **Objective:** Maintain reproducible physics across determinism/rollback flows.
- **Profile Alignment:** All.
- **Contract:**
  - ECS publishes authoritative state snapshots per tick for physics to consume.
  - Physics returns resolved transforms before ECS finalises render components.
- **Budgets:** Divergence tolerance per profile `tolerant_replay` settings.
- **Verification:** `TEST-3D-AI-AC02`, `rollback_sim_harness.py` misprediction logs.

## PACT-3D-0003 — ECS ↔ Renderer
- **Objective:** Keep draw call/material counts within perf budgets while retaining fidelity.
- **Profile Alignment:** `third_person`, `isometric`, `topdown`.
- **Contract:**
  - ECS tags renderables with LOD hints; renderer enforces `performance_budgets.scene`.
  - Renderer reports aggregate metrics each frame for perf gate ingestion.
- **Verification:** `TEST-3D-PERF-SCENE-0003`, perf budget gate.

## PACT-3D-0004 — Build ↔ Importer
- **Objective:** Ensure asset validation occurs pre-build following `asset_rules`.
- **Profile Alignment:** All.
- **Contract:**
  - Importer runs `asset_linter_3d.py` on ingest; build rejects packages without lint receipts.
  - Build system injects profile ID into packaging metadata.
- **Verification:** `TEST-3D-BUILD-AC01`, asset linter CI step.

## PACT-3D-0005 — Animation ↔ NetSync
- **Objective:** Maintain animation coherence across network prediction & rollback.
- **Profile Alignment:** `networked`, `third_person`.
- **Contract:**
  - Animation exports normalised state vectors tracked by tolerant replay runner.
  - NetSync sends animation delta every `rollback.max_prediction_ticks/2` ticks.
- **Budgets:** Animation error <= `animation_normalised_error` from profile.
- **Verification:** Tolerant replay diff tables, `TEST-3D-NET-AC02`.

## PACT-3D-0006 — Audio ↔ Mix Engineering
- **Objective:** Keep loudness/peaks within profile audio rules during rapid gameplay.
- **Profile Alignment:** All.
- **Contract:**
  - Audio content team maintains LUFS values per `asset_rules.audio`.
  - Mix engineers provide real-time meters feeding telemetry.
- **Verification:** `asset_linter_3d.py` audio checks, `TEST-3D-OBS-AC01`.
