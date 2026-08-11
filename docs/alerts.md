# Alert Runbook

Mỗi alert bên dưới dựa trên triệu chứng người dùng hoặc SLO. Khi alert kích hoạt, điều tra theo thứ tự Metrics -> Traces -> Logs để đi từ triệu chứng tổng quan tới request cụ thể và root cause có bằng chứng.

## Alert 1

- Tên: `high_latency_p95`
- Severity: warning
- SLI/SLO liên quan: `latency_p95_ms <= 3000`, target 99.5% trong cửa sổ 28 ngày.
- Điều kiện và thời gian duy trì: `latency_p95_ms > 3000` trong 5 phút.
- Ảnh hưởng tới người dùng: phần lớn request vẫn có thể thành công, nhưng nhóm 5% request chậm nhất vượt 3 giây làm trải nghiệm chat bị trễ, dễ timeout ở client hoặc demo.
- Ba bước kiểm tra đầu tiên:
  1. Metrics: mở dashboard panel Latency, xác nhận P95/P99 tăng từ thời điểm nào và có trùng với Traffic spike không.
  2. Traces: lọc Langfuse traces trong khoảng thời gian P95 tăng, mở trace chậm nhất và xem span `run`, `retrieve`, `generate` nếu có.
  3. Logs: lấy `correlation_id` từ trace/response, lọc `data/logs.jsonl` để xem request có feature/session/prompt nào gây chậm.
- Mitigation tạm thời: giảm concurrency load test, tắt incident practice nếu đang bật, chuyển feature bị chậm sang fallback đơn giản, hoặc rollback prompt/version nếu prompt mới làm output quá dài.
- Owner: on-call-engineer

## Alert 2

- Tên: `elevated_error_rate`
- Severity: critical
- SLI/SLO liên quan: `error_rate_pct <= 2`, target 99.0% trong cửa sổ 28 ngày.
- Điều kiện và thời gian duy trì: `error_rate_pct > 5` trong 3 phút.
- Ảnh hưởng tới người dùng: nhiều request trả 500 hoặc không có câu trả lời, ảnh hưởng trực tiếp tới khả năng demo và chất lượng API.
- Ba bước kiểm tra đầu tiên:
  1. Metrics: mở panel Error Rate and Breakdown, xác định error rate hiện tại và `error_type` chiếm đa số.
  2. Traces: mở trace lỗi tương ứng trong Langfuse, kiểm tra span nào báo lỗi và metadata `feature`, `session_id`, `model`, `prompt_label`.
  3. Logs: lọc log theo `correlation_id`, tìm event `request_failed` và đọc `error_type`/`payload.detail` đã được PII scrub.
- Mitigation tạm thời: tắt incident hoặc feature gây lỗi, retry request nếu lỗi transient, rollback prompt/config mới, hoặc chuyển traffic sang fallback response an toàn.
- Owner: on-call-engineer

## Alert 3

- Tên: `cost_budget_exceeded`
- Severity: warning
- SLI/SLO liên quan: `daily_cost_usd <= 2.5`, target 100.0% trong cửa sổ 28 ngày.
- Điều kiện và thời gian duy trì: `daily_cost_usd > 2.5`.
- Ảnh hưởng tới người dùng: hệ thống vẫn có thể trả lời bình thường, nhưng chi phí vượt ngân sách; thường đi kèm output token tăng hoặc prompt/retrieval context quá dài.
- Ba bước kiểm tra đầu tiên:
  1. Metrics: mở panel Cost và Tokens, xác nhận cost tăng do `tokens_in`, `tokens_out` hay số request tăng.
  2. Traces: lọc trace có cost/tokens cao, so sánh prompt label/version và feature liên quan.
  3. Logs: dùng `correlation_id` để xem event `response_sent`, đối chiếu `tokens_in`, `tokens_out`, `cost_usd`, `quality_score`.
- Mitigation tạm thời: giảm max output token, dùng prompt ngắn hơn, tắt feature sinh câu trả lời dài, rollback prompt candidate nếu cost spike xuất hiện sau đổi label.
- Owner: team-lead
