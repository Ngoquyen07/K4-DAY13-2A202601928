from app.pii import scrub_text


def test_scrub_email() -> None:
    out = scrub_text("Email me at student@vinuni.edu.vn")
    assert "student@" not in out
    assert "REDACTED_EMAIL" in out


def test_scrub_common_vietnamese_phone_formats() -> None:
    phone_numbers = (
        "0901234567",
        "090 123 4567",
        "090.123.4567",
        "090-123-4567",
        "+84 90 123 4567",
    )

    for phone_number in phone_numbers:
        out = scrub_text(f"Contact: {phone_number}")
        assert phone_number not in out
        assert "REDACTED_PHONE_VN" in out


def test_scrub_test_credit_card_formats() -> None:
    cards = ("4111 1111 1111 1111", "4111-1111-1111-1111", "4111111111111111")

    for card in cards:
        out = scrub_text(f"Card: {card}")
        assert card not in out
        assert "REDACTED_CREDIT_CARD" in out


def test_scrub_cccd_number() -> None:
    out = scrub_text("CCCD cua toi la 001204012345")
    assert "001204012345" not in out
    assert "REDACTED_CCCD" in out


def test_scrub_vietnamese_passport_number() -> None:
    out = scrub_text("Passport number B1234567 issued in 2024")
    assert "B1234567" not in out
    assert "REDACTED_PASSPORT" in out


def test_scrub_vietnamese_street_address() -> None:
    out = scrub_text("Giao hang toi So 12 Duong Lang, Quan Dong Da, Ha Noi")
    assert "Duong Lang" not in out
    assert "REDACTED_ADDRESS_VN" in out


def test_scrub_keeps_correlation_id_and_ordinary_text_intact() -> None:
    text = "req-a1234567 latency 4111 ms for model claude-sonnet-4-5 at 2026-08-11T15:30:00.123456Z"
    assert scrub_text(text) == text
