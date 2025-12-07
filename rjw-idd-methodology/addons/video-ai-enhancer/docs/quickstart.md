# DOC-VIDEO-QUICKSTART-0001 — Video AI Enhancer Quickstart

## 1. Decide Activation Scope
- Confirm real-time enhancement/upscale is in scope and project can tolerate optional telemetry additions.
- Choose a starter profile (`baseline`, `live_stream`, `broadcast_mastering`, `mobile_edge`, `remote_collaboration`).

## 2. Enable Feature Flag
```bash
python scripts/addons/enable_video_ai_enhancer.py
python scripts/addons/set_video_ai_profile.py --profile live_stream
```

## 3. Wire Quality & Latency Guards
- Add the snippets from `ci/includes.yml` (or include `addons/video-ai-enhancer/ci/snippets/*.yml`).
- Feed telemetry samples using the schemas in `docs/samples/`.
- Run locally:
  ```bash
  python addons/video-ai-enhancer/tools/quality_gate_video.py --metrics addons/video-ai-enhancer/docs/samples/quality_metrics_baseline.json
  python addons/video-ai-enhancer/tools/latency_guard_video.py --trace addons/video-ai-enhancer/docs/samples/latency_trace_sample.json
  python addons/video-ai-enhancer/tools/storage_capture_validator.py --report addons/video-ai-enhancer/docs/samples/storage_report_sample.json
  ```

## 4. Align Prompts & Specs
- Prompts live under `addons/video-ai-enhancer/prompts/` and map to research, design, QA, ops, and reconciliation anchors.
- Specs templates live in `addons/video-ai-enhancer/specs/templates/`; copy into project docs using RJW-IDD IDs.

## 5. Exit Cleanly if Needed
```bash
python scripts/addons/verify_video_ai_enhancer.py --mode full
python scripts/addons/disable_video_ai_enhancer.py
```
This removes CI hooks and README entries while keeping artefacts for archival.
