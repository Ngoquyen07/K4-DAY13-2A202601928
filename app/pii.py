from __future__ import annotations

import hashlib
import re

# Street/administrative keywords that turn a "so <number>" prefix into an address.
_ADDRESS_UNIT_VN = (
    r"(?:đường|duong|phố|pho|ngõ|ngo|ngách|ngach|tổ|to|thôn|thon|ấp|ap"
    r"|phường|phuong|xã|xa|quận|quan|huyện|huyen|thị trấn|thi tran"
    r"|thành phố|thanh pho|tỉnh|tinh|tp)"
)

PII_PATTERNS: dict[str, str] = {
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
    "phone_vn": r"(?<!\d)(?:\+84|0)(?:[ .-]?\d){9}(?!\d)",
    "cccd": r"\b\d{12}\b",
    "credit_card": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
    # Vietnamese passport: one uppercase letter + 7 digits (B1234567).
    # Uppercase only on purpose: correlation IDs are lowercase hex ("req-a1234567")
    # and must stay readable as investigation evidence.
    "passport": r"\b[A-Z]\d{7}\b",
    # Street address: "So <number> ...," followed by at least one street/admin unit.
    # Both units are required so ordinary prose is not redacted.
    "address_vn": rf"(?i)\bs(?:ố|o)\s*\d+[^,\n]{{0,60}}(?:,\s*{_ADDRESS_UNIT_VN}\b[^,\n]{{0,60}})+",
}


def scrub_text(text: str) -> str:
    safe = text
    for name, pattern in PII_PATTERNS.items():
        safe = re.sub(pattern, f"[REDACTED_{name.upper()}]", safe)
    return safe


def summarize_text(text: str, max_len: int = 80) -> str:
    safe = scrub_text(text).strip().replace("\n", " ")
    return safe[:max_len] + ("..." if len(safe) > max_len else "")


def hash_user_id(user_id: str) -> str:
    return hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:12]
