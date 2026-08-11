# Evidence Checklist

Luu anh chup, output lenh va log evidence trong thu muc nay. Trong `submission/REPORT.md`, dan lai bang duong dan tuong doi.

## CP1 - Logging, Correlation ID, PII

| Evidence | Ten file goi y | Trang thai |
| --- | --- | --- |
| Log JSON co `correlation_id` | `cp1-correlation-id-log.png`, `cp1-log-samples.txt` | Done |
| Log co metadata `user_id_hash`, `session_id`, `feature`, `model`, `env` | `cp1-log-metadata.png`, `cp1-log-samples.txt` | Done |
| Log chung minh PII da redact | `cp1-pii-redaction-log.png`, `cp1-log-samples.txt` | Done |
| Ket qua `validate_logs.py` | `cp1-validate-logs.txt` | Done |

## CP2 - Traces, Prompt Version, Dashboard

| Evidence | Ten file goi y | Trang thai |
| --- | --- | --- |
| Danh sach toi thieu 10 traces tren Langfuse | `cp2-langfuse-traces-list.jpg` | Done |
| Mot trace waterfall day du | `cp2-langfuse-waterfall.png` | Done |
| Trace prompt baseline | `cp2-prompt-versions.png` | Done |
| Trace prompt candidate | `cp2-prompt-versions.png` | Done |
| Bang chung doi label hoac rollback prompt | `cp2-prompt-versions.png` | Done |
| Dashboard du 6 panel | `cp2-validate-dashboard.png`, `../docs/dashboard-spec.md`, `../config/dashboard.yaml` | Done |
| Ket qua `validate_dashboard.py` | `cp2-validate-dashboard.txt`, `cp2-validate-dashboard.png` | Done |
| Metrics baseline tu `/metrics` | `cp2-metrics-baseline.json` | Done |

## CP3 - Incident Investigation

| Evidence | Ten file goi y | Trang thai |
| --- | --- | --- |
| Metrics luc incident, panel vuot threshold | `cp3-incident-metrics.json` | Done |
| Trace lien quan den incident | `cp2-langfuse-waterfall.png`, `cp2-trace-metadata.png` | Done |
| Log co cung correlation ID va root cause | `cp3-root-cause-log.jsonl` | Done |
| Ket luan root cause/fix/prevention | `cp3-investigation-summary.md` | Done |

