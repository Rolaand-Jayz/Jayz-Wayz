# SPEC-3D-PERF-0001 — Performance & Budget Charter

- **Active Profile:** `<features.yml :: addons.3d_game_core.profile>`
- **Reference Config:** `addons/3d-game-core/config/3d-game-core.yml`
- **Decisions:** `DEC-3D-PERF-0001` (baseline budgets), `DEC-3D-PERF-0002` (profiling cadence)

## 1. Target Hardware Envelope
- Enumerate min/spec/elite hardware targets with CPU/GPU/VRAM specs.
- Map each target to the expected frame budget and resolution scaling matrix.

## 2. Budget Breakdown
Replicate the table below with profile-specific numbers pulled from the merged config.

| Subsystem | Budget Source | Budget Value | Notes |
| --- | --- | --- | --- |
| CPU (frame) | `performance_budgets.frame.cpu_ms` | `<value>` | `TEST-3D-PERF-CPU-0001` |
| GPU (frame) | `performance_budgets.frame.gpu_ms` | `<value>` | `TEST-3D-PERF-GPU-0002` |
| Draw Calls | `performance_budgets.scene.draw_calls` | `<value>` | `TEST-3D-PERF-SCENE-0003` |
| Materials | `performance_budgets.scene.materials` | `<value>` | `TEST-3D-PERF-SCENE-0004` |
| Lights | `performance_budgets.scene.lights` | `<value>` | `TEST-3D-PERF-LIGHTS-0005` |
| VRAM | `performance_budgets.memory.vram_mb` | `<value>` | `TEST-3D-PERF-MEM-0006` |
| Texture Pool | `performance_budgets.memory.texture_pool_mb` | `<value>` | `TEST-3D-PERF-TEX-0007` |

## 3. Instrumentation Plan
- Hook metrics export (Unity, Unreal, Godot, custom) to `perf_metrics_inputs.required_fields`.
- Define sample capture cadence per build lane and environment (dev, qa, certification).

## 4. Acceptance Criteria
- `TEST-3D-PERF-AC01`: Automation fails build when any subsystem exceeds budgets by >5% for three consecutive captures.
- `TEST-3D-PERF-AC02`: Engineers can reproduce perf metrics locally using engine adapters.
- `TEST-3D-PERF-AC03`: Perf dashboard surfaces at least five profile-specific insights per sprint.

## 5. Traceability
| Artefact | Identifier |
| --- | --- |
| Requirements | `REQ-3D-PERF-*`
| Decisions | `DEC-3D-PERF-*`
| Tests | `TEST-3D-PERF-*`
| Integrations | `INTEG-3D-PERF-*`

> **Profile Check:** Refer to `scripts/addons/verify_3d_game_core.py` output to confirm the merged budget values recorded here stay in sync with the active profile.
