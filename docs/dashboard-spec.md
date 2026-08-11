# Dashboard Spec - Day 13 AI Observability

Dashboard theo doi he thong AI trong cua so mac dinh 60 phut, refresh 30 giay. Nguon du lieu chuan la `data/logs.jsonl`; contract may cham nam trong `config/dashboard.yaml`.

Muc tieu cua dashboard la phat hien trieu chung bang metrics truoc, sau do dung Langfuse traces va structured logs de khoanh vung request/correlation ID lien quan.

## Cau hinh chung

| Thuoc tinh | Gia tri |
| --- | --- |
| Title | Day 13 AI Observability |
| Time range mac dinh | 60 phut |
| Refresh | 30 giay |
| Data source | `data/logs.jsonl` |
| So panel lop chinh | 6 |
| Contract validation | `python scripts/validate_dashboard.py` |

## Panel 1 - Latency Percentiles

| Muc | Gia tri |
| --- | --- |
| Panel ID | `latency` |
| Muc dich | Theo doi tail latency cua API `/chat` |
| Event/field | `response_sent.latency_ms` |
| Aggregations | P50, P95, P99 |
| Don vi | ms |
| Query logic | `event == "response_sent" | percentile(latency_ms, [50, 95, 99])` |
| Threshold/SLO line | P95 <= 3000 ms |
| Kieu hien thi | Line chart theo thoi gian + single value P95 hien tai |
| Dieu tra khi bat thuong | Mo traces trong khoang thoi gian latency cao, tim request/span cham, sau do loc log theo `correlation_id` |

## Panel 2 - Request Traffic

| Muc | Gia tri |
| --- | --- |
| Panel ID | `traffic` |
| Muc dich | Theo doi luu luong request va phat hien drop/spike bat thuong |
| Event/field | `request_received.event` |
| Aggregations | Count, rate per minute |
| Don vi | requests/minute |
| Query logic | `event == "request_received" | count() by 1m` |
| Threshold/SLO line | Rate >= 1 request/minute trong luc load test |
| Kieu hien thi | Bar/line chart theo tung phut |
| Dieu tra khi bat thuong | So sanh voi load test dang chay, kiem tra API/server co nhan request hay khong |

## Panel 3 - Error Rate And Breakdown

| Muc | Gia tri |
| --- | --- |
| Panel ID | `errors` |
| Muc dich | Phat hien loi user-facing va nhom loi theo `error_type` |
| Event/field | `request_received`, `request_failed`, `error_type` |
| Aggregations | Error rate percentage, count by error type |
| Don vi | percent |
| Query logic | `count(event == "request_failed") / count(event == "request_received") * 100; count_by(error_type)` |
| Threshold/SLO line | Error rate <= 2% |
| Kieu hien thi | Single value error rate + table breakdown |
| Dieu tra khi bat thuong | Mo trace loi, lay `correlation_id`, loc log `request_failed` de xem root cause |

## Panel 4 - Cost Over Time

| Muc | Gia tri |
| --- | --- |
| Panel ID | `cost` |
| Muc dich | Theo doi cost tich luy va phat hien cost spike |
| Event/field | `response_sent.cost_usd` |
| Aggregations | Sum by minute, total |
| Don vi | USD |
| Query logic | `event == "response_sent" | sum(cost_usd) by 1m; sum(cost_usd)` |
| Threshold/SLO line | Total cost <= 2.5 USD trong cua so theo doi |
| Kieu hien thi | Line/area chart + total cost |
| Dieu tra khi bat thuong | Kiem tra panel tokens, mo trace co output dai bat thuong, doi chieu log prompt/feature |

## Panel 5 - Input And Output Tokens

| Muc | Gia tri |
| --- | --- |
| Panel ID | `tokens` |
| Muc dich | Theo doi tong token input/output de giai thich cost va latency |
| Event/field | `response_sent.tokens_in`, `response_sent.tokens_out` |
| Aggregations | Sum by field |
| Don vi | tokens |
| Query logic | `event == "response_sent" | sum(tokens_in), sum(tokens_out)` |
| Threshold/SLO line | Tong token <= 50000 trong cua so theo doi |
| Kieu hien thi | Stacked bar hoac two-line chart input/output |
| Dieu tra khi bat thuong | Tim feature/session co token out cao, mo trace va log cung `correlation_id` |

## Panel 6 - Quality Proxy

| Muc | Gia tri |
| --- | --- |
| Panel ID | `quality` |
| Muc dich | Theo doi chat luong phan hoi bang proxy score |
| Event/field | `response_sent.quality_score` |
| Aggregations | Mean |
| Don vi | score 0..1 |
| Query logic | `event == "response_sent" | mean(quality_score)` |
| Threshold/SLO line | Mean quality >= 0.75 |
| Kieu hien thi | Single value + trend line |
| Dieu tra khi bat thuong | Kiem tra prompt version, feature, trace metadata va sample response lien quan |

## Evidence Can Thu Thap

Luu tat ca anh trong `submission/evidence/` va dan lai trong `submission/REPORT.md`.

| Evidence | Ten file goi y | Ghi chu |
| --- | --- | --- |
| Dashboard du 6 panel | `cp2-dashboard-6-panels.png` | Anh phai thay title panel, time range, don vi va threshold |
| Validator dashboard pass | `cp2-validate-dashboard.txt` hoac screenshot terminal | Ket qua can co dong `HOP LE: 6/6 panel` hoac ban tieng Viet co dau |
| Metrics baseline sau load test | `cp2-metrics-baseline.json` | Lay tu endpoint `/metrics` neu app dang chay |
| Danh sach >= 10 traces | `cp2-langfuse-traces-list.png` | Langfuse trace list |
| Mot trace waterfall | `cp2-langfuse-waterfall.png` | Can thay span `run`, neu co them `retrieve`/`generate` cang tot |

## Runtime Check

Chay theo thu tu sau khi Block 1 da merge:

```bash
python scripts/load_test.py --concurrency 5
python scripts/validate_logs.py
python scripts/validate_dashboard.py
```

Neu API dang chay local, lay metrics hien tai:

```bash
curl http://localhost:8000/metrics
```

Khi co incident, workflow dieu tra tren dashboard:

1. Xac dinh panel bat thuong: latency, errors, cost, tokens hoac quality.
2. Ghi lai timestamp va chi so vuot threshold.
3. Mo Langfuse trong cung khoang thoi gian.
4. Chon trace lien quan, lay trace ID va `correlation_id`.
5. Loc `data/logs.jsonl` theo `correlation_id` de tim log root cause.
