"""Failing-first unit tests for authentication service behavior."""

import pytest


pytestmark = [pytest.mark.unit, pytest.mark.tdd]


def test_fr_01_registration_success_creates_customer(service_modules, customer_payload):
    """FR-01, NFR-02: valid registration creates exactly one customer."""

    auth_service = service_modules["auth_service"]

    user = auth_service.register_user(customer_payload)

    assert user.email == customer_payload["email"]
    assert user.role == "customer"
    assert getattr(user, "password_hash", None) != customer_payload["password"]


def test_fr_01_duplicate_registration_rejected(service_modules, customer_payload):
    """FR-01: duplicate email registration is rejected."""

    auth_service = service_modules["auth_service"]
    auth_service.register_user(customer_payload)

    with pytest.raises(ValueError, match="Email already registered"):
        auth_service.register_user(customer_payload)


def test_nfr_02_registration_rejects_password_shorter_than_8_chars(
    service_modules, customer_payload
):
    """NFR-02 boundary: password length must be at least 8 characters."""

    auth_service = service_modules["auth_service"]
    weak_payload = {**customer_payload, "password": "1234567"}

    with pytest.raises(ValueError, match="password"):
        auth_service.register_user(weak_payload)


def test_fr_02_login_success_returns_access_token(service_modules, customer_payload):
    """FR-02: valid login returns a bearer-style access token."""

    auth_service = service_modules["auth_service"]
    auth_service.register_user(customer_payload)

    token = auth_service.login_user(
        customer_payload["email"], customer_payload["password"]
    )

    assert token.access_token
    assert token.token_type == "bearer"
    assert token.role == "customer"


def test_fr_03_invalid_login_rejected_without_token(service_modules, customer_payload):
    """FR-03, EC-06: invalid credentials do not issue an access token."""

    auth_service = service_modules["auth_service"]
    auth_service.register_user(customer_payload)

    with pytest.raises(ValueError, match="Invalid credentials"):
        auth_service.login_user(customer_payload["email"], "wrong-password")


def test_fr_13_invalid_token_rejected_before_protected_action(
    service_modules, invalid_token
):
    """FR-13, EC-08: malformed or expired tokens are rejected by auth boundary."""

    auth_service = service_modules["auth_service"]

    with pytest.raises(PermissionError, match="Unauthorized"):
        auth_service.require_valid_token(invalid_token)
