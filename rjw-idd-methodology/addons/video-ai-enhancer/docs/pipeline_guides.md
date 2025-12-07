# DOC-VIDEO-GUIDE-0001 — Pipeline Integration Guide

## Streaming Stack Checklist
- Confirm encoder exposes stage timings for `detector`, `enhancer`, `encoder`, `muxer`.
- Emit JSON traces compatible with `latency_guard_video.py` (see `docs/samples/latency_trace_sample.json`).
- Export quality metrics every N frames via offline evaluation or on-the-fly model.

## Recording & Storage
- Keep rolling capture windows aligned with `storage_pipeline.capture_window_minutes`.
- Report aggregate write rate in MB to validate retention and parallel writer limits.
- For high bitrate mastering, adjust `broadcast_mastering` profile and commit to the feature registry via `set_video_ai_profile.py`.

## Observability
- Forward snapshots (raw + enhanced) for manual spot checks when variance spikes.
- Tag logs with `video-ai` and profile id for quick filtering.
- Extend `metrics_export` in config if OTLP is not available (JSON schema recommended).
