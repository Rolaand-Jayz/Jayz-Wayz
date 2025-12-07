# DOC-VIDEO-METRIC-0001 — Video AI Enhancer Metrics Schema

| Field | Type | Description |
| --- | --- | --- |
| `metrics.vmaf` | float | VMAF score computed on the enhanced output. |
| `metrics.psnr` | float | PSNR (dB) vs. source. |
| `metrics.ssim` | float | SSIM across full frame. |
| `metrics.lpips` | float | LPIPS perceptual distance (lower is better). |
| `frame_consistency.jitter_ratio` | float | Ratio of frame-to-frame timing variance. |
| `frame_consistency.frame_drop_pct` | float | Percentage of dropped frames in the window. |
| `frame_consistency.actual_fps` | float | Observed output framerate. |
| `artifact_budget.hallucination_pct` | float | Percentage of frames with hallucinated detail or texture pops. |
| `artifact_budget.color_shift_delta_e` | float | Mean Delta-E colour shift against ground truth. |
| `latency.glass_to_glass_ms` | float | Optional aggregated glass-to-glass figure for context (used by latency guard). |
| `storage.average_bitrate_mbps` | float | Optional average bitrate across capture segments. |

Payloads should follow the sample in `docs/samples/quality_metrics_baseline.json` and may include project-specific annotations under `context.*`.
