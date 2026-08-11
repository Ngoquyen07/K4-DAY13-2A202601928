# Evidence Checklist

Luu anh chup, output lenh va log evidence trong thu muc nay. Trong `submission/REPORT.md`, dan lai bang duong dan tuong doi.

## CP1 - Logging, Correlation ID, PII

| Evidence | Ten file goi y | Trang thai |
| --- | --- | --- |
| Log JSON co `correlation_id` | `cp1-correlation-id-log.png` | TODO |
| Log co metadata `user_id_hash`, `session_id`, `feature`, `model`, `env` | `cp1-log-metadata.png` | TODO |
| Log chung minh PII da redact | `cp1-pii-redaction-log.png` | TODO |
| Ket qua `validate_logs.py` | `cp1-validate-logs.txt` | TODO |

## CP2 - Traces, Prompt Version, Dashboard

| Evidence | Ten file goi y | Trang thai |
| --- | --- | --- |
| Danh sach toi thieu 10 traces tren Langfuse | `cp2-langfuse-traces-list.jpg` | Done |
| Mot trace waterfall day du | `cp2-langfuse-waterfall.png` | TODO |
| Trace prompt baseline | `cp2-prompt-baseline-trace.png` | TODO |
| Trace prompt candidate | `cp2-prompt-candidate-trace.png` | TODO |
| Bang chung doi label hoac rollback prompt | `cp2-prompt-label-rollback.png` | TODO |
| Dashboard du 6 panel | `cp2-dashboard-6-panels.png` | TODO |
| Ket qua `validate_dashboard.py` | `cp2-validate-dashboard.txt` | TODO |
| Metrics baseline tu `/metrics` | `cp2-metrics-baseline.json` | TODO |

## CP3 - Incident Investigation

| Evidence | Ten file goi y | Trang thai |
| --- | --- | --- |
| Metrics luc incident, panel vuot threshold | `cp3-incident-metrics.png` | TODO |
| Trace lien quan den incident | `cp3-incident-trace-waterfall.png` | TODO |
| Log co cung correlation ID va root cause | `cp3-root-cause-log.png` | TODO |
| Ket luan root cause/fix/prevention | `cp3-investigation-summary.md` | TODO |

