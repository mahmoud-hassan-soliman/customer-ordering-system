"""Authentication routes."""

from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, RegisterRequest
from app.services import auth_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest):
    try:
        user = auth_service.register_user(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }


@router.post("/login")
def login(payload: LoginRequest):
    try:
        token = auth_service.login_user(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return {
        "access_token": token.access_token,
        "token_type": token.token_type,
        "role": token.role,
    }
