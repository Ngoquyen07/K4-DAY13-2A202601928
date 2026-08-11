# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: 2A202601928
- Repository URL: [TODO](https://github.com/Ngoquyen07/K4-DAY13-2A202601928)
- Commit SHA cuối: d7266913a8c861b5856701aac77745e0ea55cc91
- Thành viên và vai trò:
  - Người 1 - Ngô Ngọc Quyền - 2A202601928 Tech Lead / Backend Observability: correlation ID middleware, enrich logs, trace/span extension nếu có.
  - Người 2 - Nguyễn Kỳ Anh - 2A202601558 Security & SRE Engineer: PII scrubbing, SLO, alert rules, alert runbook.
  - Người 3 - Nguyễn Hà Bách - 2A202601592 QA / Metrics / Chief Investigator: load test sau CP1, dashboard spec, Langfuse evidence, incident investigation, tổng hợp report.

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100
- Tổng số traces: >= 10 traces theo ảnh Langfuse `submission/evidence/cp2-langfuse-traces-list.jpg`
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: `docs/dashboard-spec.md`, `config/dashboard.yaml`; ảnh dashboard runtime chờ chụp sau khi chạy load test.
- Kết quả `validate_dashboard.py`: `HỢP LỆ: 6/6 panel có trong dashboard contract.`

## 3. Logging và tracing

- Evidence correlation ID: `submission/evidence/cp1-log-samples.txt`
- Evidence PII redaction: `submission/evidence/cp1-log-samples.txt`, `submission/evidence/cp1-validate-logs.txt`
- Evidence trace waterfall: chờ ảnh chi tiết một trace, ví dụ `submission/evidence/cp2-langfuse-waterfall.png`
- Giải thích một span đáng chú ý:
  - Trace ID: TODO
  - Span đáng chú ý: TODO, ví dụ `run`, `retrieve`, hoặc `generate`
  - Nhận xét: TODO, nêu latency/error/cost/metadata liên quan và correlation ID dùng để nối sang logs.

## 4. Prompt versioning

- Prompt name: TODO
- Version/label baseline: TODO
- Version/label candidate: TODO
- Trace ID của mỗi version:
  - Baseline trace ID: TODO
  - Candidate trace ID: TODO
- Bằng chứng đổi label hoặc rollback prompt: TODO, ví dụ `submission/evidence/cp2-prompt-label-rollback.png`

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: `HỢP LỆ: 6/6 panel có trong dashboard contract.`
- Evidence dashboard: TODO, ví dụ `submission/evidence/cp2-dashboard-6-panels.png`
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

- Challenge ID: TODO, hoặc ghi `Practice scenario: rag_slow/tool_fail/cost_spike` nếu Coach chưa release challenge chính thức.
- Triệu chứng từ metrics:
  - Panel bất thường: TODO
  - Giá trị trước incident: TODO
  - Giá trị trong incident: TODO
  - Threshold bị vượt: TODO
- Trace ID liên quan:
  - Trace ID: TODO
  - Span liên quan: TODO
  - Metadata quan trọng: TODO, ví dụ `feature`, `session_id`, `model`, `prompt_label`
- Log line/correlation ID liên quan:
  - Correlation ID: TODO
  - File/log evidence: TODO, ví dụ `submission/evidence/cp3-root-cause-log.png`
  - Event log chính: TODO, ví dụ `request_failed` hoặc `response_sent`
- Root cause: TODO
- Fix action: TODO
- Preventive measure: TODO

### Mẫu kết luận CP3

Metrics cho thấy TODO vượt threshold vào khoảng TODO. Trace TODO trong Langfuse khoanh vùng vấn đề ở span TODO. Log có cùng `correlation_id=TODO` ghi nhận TODO, vì vậy root cause là TODO. Nếu đây là production, hành động xử lý tạm thời là TODO; phòng ngừa lâu dài bằng TODO.

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Người 1 | Correlation ID middleware, enrich log context, response headers, trace/span extension nếu có | Chờ dán commit SHA/PR | Correlation ID giúp nối request từ client -> trace -> log để điều tra nhanh hơn. |
| Người 2 | PII scrubbing, SLO, alert rules, alert runbook | Chờ dán commit SHA/PR | Alert nên dựa trên triệu chứng người dùng thấy thay vì tên implementation nội bộ. |
| Người 3 | Dashboard spec, evidence checklist, validate dashboard, incident report template, tổng hợp report | Chờ dán commit SHA/PR | Metrics phát hiện triệu chứng, traces khoanh vùng vị trí, logs chứng minh root cause. |

## 8. Evidence checklist

| Evidence | Trạng thái | Đường dẫn |
|---|---|---|
| Kết quả cuối của `validate_logs.py` | Done | `submission/evidence/cp1-validate-logs.txt` |
| Danh sách có tối thiểu 10 traces | Done | `submission/evidence/cp2-langfuse-traces-list.jpg` |
| Một trace waterfall đầy đủ | TODO | Cần mở một trace cụ thể và chụp waterfall |
| Hai prompt version và trace đúng name/label/version | TODO | TODO |
| Bằng chứng đổi label hoặc rollback prompt | TODO | TODO |
| Log JSON có correlation ID và metadata | Done | `submission/evidence/cp1-log-samples.txt` |
| Log chứng minh PII đã được redact | Done | `submission/evidence/cp1-log-samples.txt`, `submission/evidence/cp1-validate-logs.txt` |
| Kết quả `python scripts/validate_dashboard.py` hợp lệ | Done | `submission/evidence/cp2-validate-dashboard.txt` |
| Dashboard đủ 6 nhóm chỉ số | TODO | TODO |
| Alert rules và runbook hoàn thiện | Done | `config/alert_rules.yaml`, `docs/alerts.md` |
| Evidence điều tra challenge: metric, trace ID, log line | TODO | TODO |
