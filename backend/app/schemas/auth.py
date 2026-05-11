"""Authentication request and response schemas."""

from pydantic import BaseModel, ConfigDict


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "customer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
