# Phan chia cong viec Lab 13 - Observability cho he thong AI

## Muc tieu chung

Hoan thanh Lab 13 tu Block 1 theo dung flow: structured logging -> correlation ID & PII redaction -> metrics/traces/dashboard/SLO/alerts -> incident investigation -> report va evidence nop bai.

Nhom 3 nguoi lam song song, moi nguoi co vai tro ro rang, co commit rieng theo tung round de dam bao vua xong phan ky thuat nhom, vua co bang chung dong gop ca nhan.

## Vai tro 3 thanh vien

| Thanh vien | Vai tro | Muc tieu chinh | File/phan viec phu trach |
| --- | --- | --- | --- |
| Nguoi 1 | Tech Lead / Backend Observability | Lam CP1: middleware correlation ID, enrich log context, dam bao API tra x-request-id | `app/middleware.py`, `app/main.py`, mot phan `scripts/load_test.py` neu lam extension loi 500 |
| Nguoi 2 | Security & SRE Engineer | Lam CP1 PII + CP2 SLO/alerts: scrub PII, cau hinh alert rules, viet runbook | `app/logging_config.py`, `app/pii.py`, `config/slo.yaml`, `config/alert_rules.yaml`, `docs/alerts.md` |
| Nguoi 3 | QA / Metrics / Chief Investigator | Chay load test sau CP1, dashboard spec, Langfuse evidence, dieu tra incident, tong hop report | `docs/dashboard-spec.md`, `submission/REPORT.md`, `submission/evidence/`, log/metrics/trace evidence |

## Nguyen tac lam viec

- Lam tren branch rieng cho tung round hoac tung nguoi, vi du: `codex/person1-cp1-logging`, `codex/person2-alerts`, `codex/person3-report-evidence`.
- Moi commit nen nho, co noi dung ro rang, de khi ghi bao cao ca nhan co the dan commit/PR chinh xac.
- Khong commit `.env`, API key, `.venv/`, cache, log co PII chua redact, hoac `config/challenge.json` neu Coach yeu cau khong dua vao repo.
- Sau moi round can chay lai: `python -m pytest -q`, `python scripts/validate_logs.py`, va `git status --short`.
- Evidence dat trong `submission/evidence/`, ten file nen co tien to ro: `cp1-`, `cp2-`, `cp3-`.

## Round 1 - Block 1 / CP1 Logging, Correlation ID & PII

Thoi gian goi y: 0:30 - 1:30

### Nguoi 1 - Backend Observability

Viec chinh:

- Hoan thanh `CorrelationIdMiddleware.dispatch()` trong `app/middleware.py`.
- Dau moi request phai `clear_contextvars()`.
- Lay `x-request-id` tu header neu co, neu khong thi tao `req-<8hex>`.
- `bind_contextvars(correlation_id=correlation_id)`.
- Gan `request.state.correlation_id`.
- Tra response headers `x-request-id` va `x-response-time-ms`.
- Trong `app/main.py`, enrich log context trong endpoint `/chat`: `user_id_hash`, `session_id`, `feature`, `model`, `env`.
- Neu con thoi gian: them generic exception handler de response loi 500 van co `x-request-id`.

Output:

- Log moi request co `correlation_id`.
- Response cua `/chat` co header `x-request-id`.
- Log co metadata de dieu tra: `user_id_hash`, `session_id`, `feature`, `model`, `env`.

Commit goi y:

- `feat: add correlation id middleware`
- `feat: enrich chat logs with request metadata`

### Nguoi 2 - PII & Security

Viec chinh:

- Bat processor scrub PII trong `app/logging_config.py`.
- Bo sung pattern trong `app/pii.py` cho cac loai PII thuong gap:
  - Email
  - So dien thoai Viet Nam
  - Credit card test, dac biet mau `4111`
  - CCCD/CMND neu starter repo chua co
  - Dia chi hoac thong tin nhay cam neu validator/guide yeu cau
- Kiem tra log khong con email, phone, credit card raw.

Output:

- `validate_logs.py` tang diem, muc tieu toi thieu >= 80/100 sau CP1, ly tuong 100/100.
- Co evidence log PII da bi redact.

Commit goi y:

- `fix: enable pii scrubbing for structured logs`
- `feat: extend vietnamese pii redaction patterns`

### Nguoi 3 - QA

Viec chinh:

- Chay API + load test sau khi Nguoi 1 va 2 merge.
- Xoa log cu truoc khi test lai neu can.
- Chay `python scripts/validate_logs.py`.
- Luu evidence:
  - Log JSON co `correlation_id`
  - Log co `user_id_hash`, `session_id`, `feature`
  - Log co PII da redact
  - Score validator cuoi CP1
- Cap nhat `submission/REPORT.md` muc logging/correlation/PII.

Output:

- CP1 dat acceptance criteria.
- Evidence san sang cho bao cao.

Commit goi y:

- `docs: add cp1 logging evidence to report`

## Round 2 - Block 2 / CP2 Metrics, Traces, Dashboard, SLO & Alerts

Thoi gian goi y: 1:30 - 2:30

### Nguoi 1 - Trace Extension neu kip

Viec chinh:

- Kiem tra Langfuse trace da sinh sau load test.
- Neu co thoi gian, them span con cho RAG/LLM:
  - `app/mock_rag.py`: decorate `retrieve()` bang `@observe(as_type="span")`.
  - `app/mock_llm.py`: decorate `generate()` bang `@observe(as_type="span")`.
- Dam bao app van chay va trace waterfall co `run`, co the co `retrieve`, `generate`.

Output:

- Trace co metadata va waterfall de phuc vu CP3.

Commit goi y:

- `feat: add rag and llm subcomponent spans`

### Nguoi 2 - SLO & Alerting

Viec chinh:

- Cap nhat `config/slo.yaml` voi SLI/SLO phu hop:
  - `latency_p95_ms`: objective 3000, target 99.5
  - `error_rate_pct`: objective 2, target 99.0
  - `daily_cost_usd`: objective 2.5, target 100.0
  - `quality_score_avg`: objective 0.75, target 95.0
- Dien 3 alert trong `config/alert_rules.yaml`:
  - High latency P95
  - Elevated error rate
  - Cost budget exceeded
- Viet `docs/alerts.md` cho 3 runbook, moi alert co:
  - Severity
  - SLI/SLO lien quan
  - Dieu kien kich hoat
  - Anh huong toi nguoi dung
  - 3 buoc kiem tra dau tien theo Metrics -> Traces -> Logs
  - Mitigation tam thoi
  - Owner

Output:

- Alert rules va runbook day du, symptom-based.

Commit goi y:

- `feat: define slo and alert rules`
- `docs: add incident alert runbooks`

### Nguoi 3 - Dashboard & Evidence

Viec chinh:

- Goi `/metrics`, ghi lai cac chi so hien co.
- Hoan thien `docs/dashboard-spec.md` voi 6 nhom panel:
  - Latency: P50/P95/P99
  - Traffic: total requests/QPS
  - Error: error rate + breakdown
  - Cost: total/average cost
  - Tokens: input/output tokens
  - Quality: average quality score
- Chay load test de tao toi thieu 10 traces.
- Luu screenshot/evidence Langfuse:
  - Danh sach >= 10 traces
  - Mot trace waterfall day du
  - Dashboard spec hoac anh dashboard neu co
- Cap nhat `submission/REPORT.md` muc CP2.

Output:

- CP2 co du dashboard spec, trace evidence, alert evidence.

Commit goi y:

- `docs: complete dashboard specification`
- `docs: add cp2 trace and dashboard evidence`

## Round 3 - Block 3 / CP3 Incident Investigation

Thoi gian goi y: 2:30 - 3:30

### Phan cong khi Coach release challenge

| Nguoi | Viec can lam | Evidence can lay |
| --- | --- | --- |
| Nguoi 1 | Kiem tra he thong chay on dinh, bat incident bang `scripts/inject_incident.py`, ho tro doc code khi can | Command output, log server neu co loi |
| Nguoi 2 | Doc metrics, xac dinh trieu chung bat thuong so voi baseline | Screenshot/JSON metrics: latency, error rate, cost, quality |
| Nguoi 3 | Mo Langfuse trace, lay correlation ID, loc logs, viet ket luan root cause | Trace ID, waterfall screenshot, log line/correlation ID |

### Flow dieu tra bat buoc

1. Metrics: chi so nao bat thuong?
2. Traces: request/span nao bi cham hoac loi?
3. Logs: correlation ID nao chung minh root cause?
4. Ket luan: root cause, fix action, preventive measure.

### Neu chua co challenge.json

Dung practice scenario de luyen va lam fallback evidence:

- `rag_slow`: latency tang, trace/span bi keo dai.
- `tool_fail`: error rate tang, log co request failed.
- `cost_spike`: cost/tokens tang bat thuong.

Ghi ro trong report: `Practice scenario: <ten_scenario>`.

### Commit goi y

- `docs: add incident investigation evidence`
- `docs: complete challenge root cause report`

Nguoi commit chinh: Nguoi 3, nhung moi thanh vien nen co commit evidence/phan viec rieng neu co thay doi file.

## Round 4 - Block 4 / Final Report, Review & Submission

Thoi gian goi y: 3:30 - 4:00

### Nguoi 1

- Review code trong `app/`.
- Dam bao khong log raw `user_id`.
- Chay public tests.
- Ghi contribution ca nhan vao `submission/REPORT.md`.

### Nguoi 2

- Review `config/slo.yaml`, `config/alert_rules.yaml`, `docs/alerts.md`.
- Dam bao alert la symptom-based, khong phu thuoc ten ham noi bo.
- Ghi contribution ca nhan vao `submission/REPORT.md`.

### Nguoi 3

- Tong hop `submission/REPORT.md`.
- Kiem tra du evidence trong `submission/evidence/`.
- Chay final checklist.
- Lay commit SHA cuoi va repo URL de nop.

### Final checklist

```bash
python -m pytest -q
python scripts/validate_logs.py
git status --short
```

Can dam bao:

- Tests pass.
- `validate_logs.py` dat muc tieu cua lab, ly tuong 100/100.
- `submission/REPORT.md` day du thong tin nhom, repo URL, commit SHA, vai tro, evidence.
- `submission/evidence/` co du anh/log can thiet.
- Khong co secret/API key trong git diff.
- Khong commit `.env`, `.venv/`, cache, log co PII raw.

Commit goi y:

- `docs: finalize submission report`
- `chore: prepare final lab submission`

## Lich commit de de chia diem ca nhan

| Round | Commit | Nguoi phu trach | Noi dung |
| --- | --- | --- | --- |
| R1.1 | `feat: add correlation id middleware` | Nguoi 1 | Middleware, response headers |
| R1.2 | `feat: enrich chat logs with request metadata` | Nguoi 1 | Log metadata trong `/chat` |
| R1.3 | `fix: enable pii scrubbing for structured logs` | Nguoi 2 | Bat scrubber |
| R1.4 | `feat: extend vietnamese pii redaction patterns` | Nguoi 2 | Regex PII |
| R1.5 | `docs: add cp1 logging evidence to report` | Nguoi 3 | Evidence CP1 |
| R2.1 | `feat: define slo and alert rules` | Nguoi 2 | SLO + alert rules |
| R2.2 | `docs: add incident alert runbooks` | Nguoi 2 | Runbook |
| R2.3 | `docs: complete dashboard specification` | Nguoi 3 | Dashboard 6 nhom chi so |
| R2.4 | `feat: add rag and llm subcomponent spans` | Nguoi 1 | Optional trace spans |
| R2.5 | `docs: add cp2 trace and dashboard evidence` | Nguoi 3 | Trace/dashboard evidence |
| R3.1 | `docs: add incident investigation evidence` | Nguoi 3 | Metrics/trace/log evidence |
| R3.2 | `docs: complete challenge root cause report` | Nguoi 3 | Root cause + fix/preventive |
| R4 | `docs: finalize submission report` | Ca nhom | Bao cao cuoi |

## Mau ghi dong gop ca nhan trong REPORT.md

### Nguoi 1 - Tech Lead / Backend Observability

- Hoan thanh correlation ID middleware va response headers.
- Enrich structured logs voi `user_id_hash`, `session_id`, `feature`, `model`, `env`.
- Kiem tra API va ho tro trace/span extension.
- Commit lien quan: `<dan link commit hoac SHA>`.

### Nguoi 2 - Security & SRE Engineer

- Bat va mo rong PII scrubbing cho structured logs.
- Hoan thien SLO, alert rules va alert runbook.
- Kiem tra alert theo huong symptom-based.
- Commit lien quan: `<dan link commit hoac SHA>`.

### Nguoi 3 - QA / Metrics / Chief Investigator

- Chay load test sau CP1, validate logs.
- Hoan thien dashboard spec 6 nhom chi so.
- Thu thap evidence Langfuse/logs/metrics.
- Chu tri incident investigation va tong hop `submission/REPORT.md`.
- Commit lien quan: `<dan link commit hoac SHA>`.
