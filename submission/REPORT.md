# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: 2A202601928
- Repository URL: https://github.com/Ngoquyen07/K4-DAY13-2A202601928
- Commit SHA cuối: 2cad59070236f1ff4fbf3f3cff841893137746de
- Thành viên và vai trò:
  - Người 1 - Ngô Ngọc Quyền - 2A202601928 Tech Lead / Backend Observability: correlation ID middleware, enrich logs, trace/span extension nếu có.
  - Người 2 - Nguyễn Kỳ Anh - 2A202601558 Security & SRE Engineer: PII scrubbing, SLO, alert rules, alert runbook.
  - Người 3 - Nguyễn Hà Bách - 2A202601592 QA / Metrics / Chief Investigator: load test sau CP1, dashboard spec, Langfuse evidence, incident investigation, tổng hợp report.

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100
- Tổng số traces: >= 10 traces theo ảnh Langfuse `submission/evidence/cp2-langfuse-traces-list.jpg`
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: `docs/dashboard-spec.md`, `config/dashboard.yaml`; runtime metrics baseline nằm ở `submission/evidence/cp2-metrics-baseline.json`.
- Kết quả `validate_dashboard.py`: `HỢP LỆ: 6/6 panel có trong dashboard contract.`

## 3. Logging và tracing

- Evidence correlation ID: `submission/evidence/cp1-log-samples.txt`
- Evidence PII redaction: `submission/evidence/cp1-log-samples.txt`, `submission/evidence/cp1-validate-logs.txt`
- Evidence trace waterfall: `submission/evidence/cp2-langfuse-waterfall.png`
- Giải thích một span đáng chú ý:
  - Trace evidence: `submission/evidence/cp2-langfuse-waterfall.png`, `submission/evidence/cp2-trace-metadata.png`
  - Span đáng chú ý: `run`
  - Nhận xét: span `run` đại diện cho request xử lý chat. Metadata cho thấy session, user hash, env, tags `lab`, `qa`, model `claude-sonnet-4-5`, giúp nối trace với log qua cùng khoảng thời gian/session/feature.

## 4. Prompt versioning

- Prompt name: `day13-chat`
- Version/label baseline: version `#1`, labels `production` và `baseline`
- Version/label candidate: version `#2`, labels `latest` và `candidate`
- Trace ID của mỗi version:
  - Baseline trace evidence: `submission/evidence/cp2-prompt-versions.png`
  - Candidate trace evidence: `submission/evidence/cp2-prompt-versions.png`
- Bằng chứng đổi label hoặc rollback prompt: `submission/evidence/cp2-prompt-versions.png`

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: `HỢP LỆ: 6/6 panel có trong dashboard contract.`
- Evidence dashboard: `docs/dashboard-spec.md`, `config/dashboard.yaml`, `submission/evidence/cp2-validate-dashboard.png`, `submission/evidence/cp2-metrics-baseline.json`
- Evidence validator dashboard: `submission/evidence/cp2-validate-dashboard.txt`
- Dashboard spec:
  - File spec: `docs/dashboard-spec.md`
  - Contract: `config/dashboard.yaml`
  - Time range: 60 phút
  - Refresh: 30 giây
  - Data source: `data/logs.jsonl`
  - Số panel: 6
- Sáu panel chính:
  - Latency percentiles: P50/P95/P99 từ `response_sent.latency_ms`, threshold P95 <= 3000 ms.
  - Request traffic: count và request/phút từ `request_received`, threshold >= 1 request/phút khi load test.
  - Error rate and breakdown: error rate và breakdown `error_type`, threshold <= 2%.
  - Cost over time: tổng `cost_usd` theo phút và toàn cửa sổ, threshold <= 2.5 USD.
  - Input and output tokens: tổng `tokens_in` và `tokens_out`, threshold <= 50000 tokens.
  - Quality proxy: trung bình `quality_score`, threshold >= 0.75.
- SLO đã chọn và lý do:
  - `latency_p95_ms <= 3000`: bám yêu cầu trải nghiệm người dùng, P95 thể hiện tail latency tốt hơn average.
  - `error_rate_pct <= 2`: giữ lỗi user-facing ở mức thấp, giúp alert không phụ thuộc tên hàm nội bộ.
  - `daily_cost_usd <= 2.5`: kiểm soát cost spike khi output token tăng bất thường.
  - `quality_score_avg >= 0.75`: đảm bảo chất lượng phản hồi không giảm trong lúc tối ưu latency/cost.
- Alert rules và runbook:
  - Config: `config/alert_rules.yaml`
  - Runbook: `docs/alerts.md`
  - Alert 1: `high_latency_p95`, warning, `latency_p95_ms > 3000 for 5 minutes`.
  - Alert 2: `elevated_error_rate`, critical, `error_rate_pct > 5 for 3 minutes`.
  - Alert 3: `cost_budget_exceeded`, warning, `daily_cost_usd > 2.5`.
  - Ghi chú: alert rules và runbook đã được ghép vào report; evidence dashboard runtime vẫn cần chụp sau load test.

## 6. Điều tra challenge

- Challenge ID: `day13-k4-observability-v1`
- Triệu chứng từ metrics:
  - Panel bất thường: Latency P95/P99
  - Giá trị trước incident: `latency_p95=1156ms` trong `submission/evidence/cp2-metrics-baseline.json`
  - Giá trị trong incident: `latency_p95=2651ms`, `latency_p99=2651ms` trong `submission/evidence/cp3-incident-metrics.json`
  - Threshold bị vượt: challenge threshold `latency_threshold_ms=2000`
- Trace ID liên quan:
  - Trace evidence: `submission/evidence/cp2-langfuse-traces-list.jpg`, `submission/evidence/cp2-langfuse-waterfall.png`
  - Span liên quan: `run`
  - Metadata quan trọng: affected feature `monitoring`, env `default/dev`, model `claude-sonnet-4-5`, session IDs `k4-challenge-s01` to `k4-challenge-s05`
- Log line/correlation ID liên quan:
  - Correlation ID: `req-58ac4178`, `req-df325ea4`, `req-8a82de74`, `req-ef109b09`, `req-b6a80ffa`
  - File/log evidence: `submission/evidence/cp3-root-cause-log.jsonl`
  - Event log chính: `response_sent` với `feature="monitoring"` và `latency_ms` khoảng `2650-2651`
- Root cause: official challenge bật incident `rag_slow`, làm RAG retrieval path chậm cho feature `monitoring`.
- Fix action: tắt incident bằng `.\.venv\Scripts\python.exe scripts\inject_incident.py --disable`; trong production, route tạm sang cached/simple retrieval path và kiểm tra dependency RAG.
- Preventive measure: alert symptom-based trên `latency_p95_ms`, thêm/giữ trace spans quanh retrieval/generation, và dùng correlation ID để nối slow traces với structured logs.

### Mẫu kết luận CP3

Metrics cho thấy `latency_p95=2651ms` vượt threshold `2000ms` sau khi chạy challenge `day13-k4-observability-v1`. Trace evidence trong Langfuse khoanh vùng vấn đề ở span `run` trong khoảng thời gian incident. Log có các `correlation_id` như `req-8a82de74` ghi nhận `feature="monitoring"` và `latency_ms=2650`, vì vậy root cause là incident `rag_slow` làm retrieval path chậm. Nếu đây là production, hành động xử lý tạm thời là route sang cached/simple retrieval path hoặc rollback thay đổi liên quan; phòng ngừa lâu dài bằng latency P95 alert, retrieval/generation spans và correlation ID đầy đủ.

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Người 1 | Correlation ID middleware, enrich log context, response headers, trace/span extension nếu có | `d7266913a8c861b5856701aac77745e0ea55cc91` và commit trước của nhóm | Correlation ID giúp nối request từ client -> trace -> log để điều tra nhanh hơn. |
| Người 2 | PII scrubbing, SLO, alert rules, alert runbook | `d7266913a8c861b5856701aac77745e0ea55cc91` và commit trước của nhóm | Alert nên dựa trên triệu chứng người dùng thấy thay vì tên implementation nội bộ. |
| Người 3 | Dashboard spec, evidence checklist, validate dashboard, incident report template, tổng hợp report | `d7266913a8c861b5856701aac77745e0ea55cc91` | Metrics phát hiện triệu chứng, traces khoanh vùng vị trí, logs chứng minh root cause. |

## 8. Evidence checklist

| Evidence | Trạng thái | Đường dẫn |
|---|---|---|
| Kết quả cuối của `validate_logs.py` | Done | `submission/evidence/cp1-validate-logs.txt` |
| Danh sách có tối thiểu 10 traces | Done | `submission/evidence/cp2-langfuse-traces-list.jpg` |
| Một trace waterfall đầy đủ | Done | `submission/evidence/cp2-langfuse-waterfall.png` |
| Hai prompt version và trace đúng name/label/version | Done | `submission/evidence/cp2-prompt-versions.png` |
| Bằng chứng đổi label hoặc rollback prompt | Done | `submission/evidence/cp2-prompt-versions.png` |
| Log JSON có correlation ID và metadata | Done | `submission/evidence/cp1-log-samples.txt` |
| Log chứng minh PII đã được redact | Done | `submission/evidence/cp1-log-samples.txt`, `submission/evidence/cp1-validate-logs.txt` |
| Kết quả `python scripts/validate_dashboard.py` hợp lệ | Done | `submission/evidence/cp2-validate-dashboard.txt` |
| Dashboard đủ 6 nhóm chỉ số | Done | `docs/dashboard-spec.md`, `config/dashboard.yaml`, `submission/evidence/cp2-validate-dashboard.png` |
| Alert rules và runbook hoàn thiện | Done | `config/alert_rules.yaml`, `docs/alerts.md` |
| Evidence điều tra challenge: metric, trace ID, log line | Done | `submission/evidence/cp3-incident-metrics.json`, `submission/evidence/cp3-root-cause-log.jsonl`, `submission/evidence/cp3-investigation-summary.md` |
