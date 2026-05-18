"""Authentication service functions.

Requirement coverage: FR-01, FR-02, FR-03, FR-13, FR-14, NFR-02.
"""

from dataclasses import dataclass

from app.auth.security import (
    create_access_token,
    get_token_record,
    hash_password,
    verify_password,
)
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.user import User


KITCHEN_EMAIL_DOMAIN = "@ejust.edu.eg"


@dataclass
class TokenDTO:
    access_token: str
    token_type: str
    role: str


def register_user(payload: dict) -> User:
    init_db()
    password = payload["password"]
    if len(password) < 8:
        raise ValueError("password must be at least 8 characters")

    role = payload.get("role", "customer")
    if role not in {"customer", "kitchen"}:
        raise ValueError("role must be customer or kitchen")
    if role == "kitchen" and not payload["email"].lower().endswith(KITCHEN_EMAIL_DOMAIN):
        raise ValueError("Kitchen staff email must end with @ejust.edu.eg")

    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == payload["email"]).first()
        if existing:
            raise ValueError("Email already registered")

        user = User(
            name=payload["name"],
            email=payload["email"],
            password_hash=hash_password(password),
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def login_user(email: str, password: str) -> TokenDTO:
    init_db()
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")
        token = create_access_token(user.email, user.role)
        return TokenDTO(access_token=token, token_type="bearer", role=user.role)
    finally:
        db.close()


def require_valid_token(token: str):
    record = get_token_record(token)
    if record is None:
        raise PermissionError("Unauthorized access")
    return record
