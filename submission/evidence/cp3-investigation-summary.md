# CP3 Incident Investigation Summary

## Challenge

- Challenge ID: `day13-k4-observability-v1`
- Cohort: `K4`
- Incident: `rag_slow`
- Affected feature: `monitoring`
- Challenge latency threshold: `2000ms`

## Metrics

Baseline metrics from `submission/evidence/cp2-metrics-baseline.json`:

```json
{"traffic":10,"latency_p50":150.0,"latency_p95":1156.0,"latency_p99":1156.0,"avg_cost_usd":0.0019,"total_cost_usd":0.019,"tokens_in_total":407,"tokens_out_total":1183,"error_breakdown":{},"quality_avg":0.88}
```

Incident metrics from `submission/evidence/cp3-incident-metrics.json`:

```json
{"traffic":15,"latency_p50":150.0,"latency_p95":2651.0,"latency_p99":2651.0,"avg_cost_usd":0.0019,"total_cost_usd":0.0283,"tokens_in_total":621,"tokens_out_total":1761,"error_breakdown":{},"quality_avg":0.8667}
```

Symptom: `latency_p95` increased to `2651ms`, exceeding the challenge threshold `2000ms`.

## Logs

Root-cause log evidence is stored in `submission/evidence/cp3-root-cause-log.jsonl`.

Relevant correlation IDs:

- `req-58ac4178`
- `req-df325ea4`
- `req-8a82de74`
- `req-ef109b09`
- `req-b6a80ffa`

All affected requests have `feature="monitoring"` and server-side `latency_ms` around `2650-2651ms`.

## Root Cause

The official challenge enables `rag_slow`, so the RAG retrieval path adds latency for the affected `monitoring` feature. Metrics show latency P95 above threshold, traces in Langfuse show `run` observations during the incident window, and logs prove affected `monitoring` requests share high `latency_ms`.

## Fix Action

Disable the incident/fault injection and restore normal RAG retrieval latency:

```powershell
.\.venv\Scripts\python.exe scripts\inject_incident.py --disable
```

For production, temporarily route `monitoring` requests to a cached or simpler retrieval path while investigating the slow dependency.

## Preventive Measure

Add symptom-based alerting on `latency_p95_ms`, keep trace spans around retrieval/generation, and use correlation IDs to connect slow traces with structured logs.
