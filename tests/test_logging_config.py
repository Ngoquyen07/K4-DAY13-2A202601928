from __future__ import annotations

import json
from pathlib import Path

import structlog

from app import logging_config


def _log_one_record(monkeypatch, tmp_path: Path, **fields) -> dict:
    log_path = tmp_path / "logs.jsonl"
    monkeypatch.setattr(logging_config, "LOG_PATH", log_path)
    logging_config.configure_logging()

    log = structlog.get_logger().bind(correlation_id="req-client01")
    log.info("request_received", service="api", **fields)

    lines = [line for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) == 1
    return json.loads(lines[0])


def test_configured_pipeline_scrubs_pii_in_payload(monkeypatch, tmp_path: Path) -> None:
    record = _log_one_record(
        monkeypatch,
        tmp_path,
        payload={"message_preview": "mail student@vinuni.edu.vn phone 0987654321"},
    )

    preview = record["payload"]["message_preview"]
    assert "student@vinuni.edu.vn" not in preview
    assert "0987654321" not in preview
    assert "REDACTED_EMAIL" in preview
    assert "REDACTED_PHONE_VN" in preview


def test_configured_pipeline_scrubs_pii_outside_payload(monkeypatch, tmp_path: Path) -> None:
    record = _log_one_record(
        monkeypatch,
        tmp_path,
        error_detail="card 4111 1111 1111 1111 rejected",
        payload={"docs": ["contact student@vinuni.edu.vn"]},
    )

    assert "4111 1111 1111 1111" not in record["error_detail"]
    assert "REDACTED_CREDIT_CARD" in record["error_detail"]
    assert "student@vinuni.edu.vn" not in record["payload"]["docs"][0]


def test_configured_pipeline_keeps_correlation_id_and_structure(
    monkeypatch, tmp_path: Path
) -> None:
    record = _log_one_record(monkeypatch, tmp_path, payload={"message_preview": "hello"})

    assert record["correlation_id"] == "req-client01"
    assert record["service"] == "api"
    assert record["event"] == "request_received"
    assert record["payload"]["message_preview"] == "hello"
