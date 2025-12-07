# DOC-3D-METRICS-SCHEMA-0001 — Performance Metrics Schema

## Top-Level Structure
```json
{
  "metadata": {
    "schema_version": "1.0.0",
    "profile": "third_person",
    "build_id": "<CI_BUILD_ID>",
    "timestamp": "2024-01-01T12:00:00Z",
    "scene": "RJW_PERF_SANDBOX"
  },
  "frame": {
    "cpu_ms": 15.8,
    "gpu_ms": 14.2,
    "dropped_frames": 0
  },
  "memory": {
    "system_ram_mb": 8500,
    "vram_mb": 5500,
    "texture_pool_mb": 1800
  },
  "subsystems": {
    "render": {
      "draw_calls": 2100,
      "material_switches": 320,
      "lights": 65
    },
    "animation": {
      "active_graphs": 48,
      "blend_time_avg_ms": 1.3
    },
    "physics": {
      "step_ms": 3.8,
      "constraints": 420
    },
    "ai": {
      "agents_active": 32,
      "decision_time_ms": 0.7
    }
  },
  "network": {
    "rtt_ms": 48,
    "packet_loss_pct": 0.6,
    "misprediction_rate": 0.04,
    "rollback_depth": 3
  },
  "snapshots": {
    "tolerant_replay": "BuildArtifacts/replays/snapshots.json",
    "deterministic_tape": "BuildArtifacts/replays/deterministic.tape"
  },
  "custom": {}
}
```

## Required Fields
Align with `perf_metrics_inputs.required_fields` in the merged config/profile.

| Field | Type | Description |
| --- | --- | --- |
| `frame.cpu_ms` | number | Average CPU frame time. |
| `frame.gpu_ms` | number | Average GPU frame time. |
| `frame.dropped_frames` | integer | Total dropped frames in capture. |
| `subsystems.render.draw_calls` | integer | Unique draw calls in capture. |
| `subsystems.render.material_switches` | integer | Distinct material binds. |
| `subsystems.animation.active_graphs` | integer | Active animation state machines. |
| `subsystems.physics.step_ms` | number | Average physics step budget. |
| `memory.vram_mb` | number | Peak VRAM usage. |
| `memory.texture_pool_mb` | number | Texture pool allocation. |

## Extensions
- Introduce additional keys under `custom.*` to avoid schema conflicts.
- Document any new fields in project decision logs and update `scripts/addons/verify_3d_game_core.py` checks if they become required.

## Validation
- Use `python addons/3d-game-core/tools/perf_budget_gate_3d.py --metrics <file> --profile <profile>`.
- JSON must be UTF-8 encoded and deterministic (sorted keys recommended but not required).
