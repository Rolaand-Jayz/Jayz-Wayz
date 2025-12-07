# SPEC-VIDEO-LATENCY-0003 — Latency Budget Specification

## Targets
- Glass-to-glass: `<ms>`
- Pipeline: `<ms>`
- Encode buffer: `<ms>`
- Queue depth: `<frames>`

## Measurement Strategy
- Telemetry tap points per stage (timestamps, counters).
- Sample window size and percentile reporting cadence.
- Alert thresholds and automated responses.

## Drill Procedures
- Synthetic load scenarios to validate guard variance.
- Failover tests (model fallback, GPU switchover).
- Reporting format for retrofits.
