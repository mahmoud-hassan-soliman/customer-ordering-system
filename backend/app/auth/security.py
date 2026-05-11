"""Small bearer-token and password helpers for the academic demo."""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


TOKEN_TTL_MINUTES = 60
_TOKENS: dict[str, "TokenRecord"] = {}


@dataclass
class TokenRecord:
    email: str
    role: str
    expires_at: datetime


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return secrets.compare_digest(hash_password(password), password_hash)


def create_access_token(email: str, role: str) -> str:
    token = secrets.token_urlsafe(24)
    _TOKENS[token] = TokenRecord(
        email=email,
        role=role,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=TOKEN_TTL_MINUTES),
    )
    return token


def get_token_record(token: str) -> TokenRecord | None:
    record = _TOKENS.get(token)
    if record is None:
        return None
    if record.expires_at <= datetime.now(timezone.utc):
        _TOKENS.pop(token, None)
        return None
    return record

