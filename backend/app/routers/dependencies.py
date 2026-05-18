"""Router dependencies for token and role checks.

Requirement coverage: FR-11, FR-13, FR-14.
"""

from fastapi import Header, HTTPException

from app.services.auth_service import KITCHEN_EMAIL_DOMAIN, require_valid_token


def _extract_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized access")
    return authorization.removeprefix("Bearer ").strip()


def get_current_user(authorization: str | None = Header(default=None)):
    try:
        return require_valid_token(_extract_token(authorization))
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


def require_customer(current_user=Header(default=None, alias="Authorization")):
    try:
        user = require_valid_token(_extract_token(current_user))
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    if user.role != "customer":
        raise HTTPException(status_code=403, detail="Customer role required")
    return user


def require_kitchen(current_user=Header(default=None, alias="Authorization")):
    try:
        user = require_valid_token(_extract_token(current_user))
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    if user.role != "kitchen":
        raise HTTPException(status_code=403, detail="Kitchen role required")
    if not user.email.lower().endswith(KITCHEN_EMAIL_DOMAIN):
        raise HTTPException(status_code=403, detail="Kitchen staff email domain required")
    return user
