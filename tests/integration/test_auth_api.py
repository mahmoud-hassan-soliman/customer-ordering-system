"""Failing-first FastAPI integration tests for auth contracts."""

import pytest


pytestmark = [pytest.mark.integration, pytest.mark.tdd]


def test_fr_01_register_success_returns_201(client, customer_payload):
    """FR-01, NFR-02: POST /auth/register creates a customer."""

    response = client.post("/auth/register", json=customer_payload)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == customer_payload["email"]
    assert body["role"] == "customer"
    assert "password" not in body


def test_fr_14_kitchen_register_rejects_non_ejust_email(client, kitchen_payload):
    """FR-14: kitchen staff registration requires @ejust.edu.eg email."""

    response = client.post(
        "/auth/register",
        json={**kitchen_payload, "email": "salma.kitchen@gmail.com"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Kitchen staff email must end with @ejust.edu.eg"
    }


def test_fr_14_kitchen_register_allows_ejust_email(client, kitchen_payload):
    """FR-14: kitchen staff registration allows EJUST domain staff email."""

    response = client.post("/auth/register", json=kitchen_payload)

    assert response.status_code == 201
    assert response.json()["email"].endswith("@ejust.edu.eg")
    assert response.json()["role"] == "kitchen"


def test_fr_01_duplicate_register_returns_400_structured_error(client, customer_payload):
    """FR-01: duplicate email follows the API contract error response."""

    first = client.post("/auth/register", json=customer_payload)
    second = client.post("/auth/register", json=customer_payload)

    assert first.status_code == 201
    assert second.status_code == 400
    assert second.json() == {"detail": "Email already registered"}


def test_fr_02_login_success_returns_token(client, customer_payload):
    """FR-02: POST /auth/login returns access_token for valid credentials."""

    client.post("/auth/register", json=customer_payload)

    response = client.post(
        "/auth/login",
        json={
            "email": customer_payload["email"],
            "password": customer_payload["password"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_fr_03_invalid_login_returns_401_structured_error(client, customer_payload):
    """FR-03, EC-06: invalid login returns 401 with structured detail."""

    client.post("/auth/register", json=customer_payload)

    response = client.post(
        "/auth/login",
        json={"email": customer_payload["email"], "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
