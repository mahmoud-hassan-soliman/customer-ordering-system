"""Failing-first FastAPI integration tests for menu and order contracts."""

import pytest

from tests.utils.seed_data import DUPLICATE_CLIENT_ORDER_KEY, empty_order_payload, order_payload


pytestmark = [pytest.mark.integration, pytest.mark.tdd]


def test_fr_04_menu_retrieval_returns_at_least_three_items(client):
    """FR-04, NFR-01: GET /menu returns seeded menu items."""

    response = client.get("/menu")

    assert response.status_code == 200
    body = response.json()
    assert len(body) >= 3
    assert {"id", "name", "price", "available"} <= set(body[0])


@pytest.mark.parametrize("quantity", [0, -1, 11])
def test_fr_05_order_endpoint_rejects_invalid_quantities(
    client, auth_headers, quantity
):
    """FR-05, EC-02: API rejects quantity boundary violations."""

    response = client.post(
        "/orders",
        headers=auth_headers,
        json=order_payload(client_order_key=f"invalid-quantity-{quantity}", quantity=quantity),
    )

    assert response.status_code == 400
    assert "quantity" in response.json()["detail"].lower()


def test_fr_06_valid_order_placement_returns_201(client, auth_headers):
    """FR-06: POST /orders creates a pending order."""

    response = client.post(
        "/orders",
        headers=auth_headers,
        json=order_payload(client_order_key="client-order-key-api-valid", quantity=2),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "pending"
    assert body["total"] > 0


def test_fr_07_empty_cart_returns_400_structured_error(client, auth_headers):
    """FR-07, EC-03: empty items cannot create an order."""

    response = client.post(
        "/orders", headers=auth_headers, json=empty_order_payload()
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Order must contain at least one item"}


def test_fr_08_duplicate_client_order_key_returns_400(client, auth_headers):
    """FR-08, EC-01: duplicate client_order_key prevents duplicate order."""

    payload = order_payload(client_order_key=DUPLICATE_CLIENT_ORDER_KEY, quantity=1)

    first = client.post("/orders", headers=auth_headers, json=payload)
    second = client.post("/orders", headers=auth_headers, json=payload)

    assert first.status_code == 201
    assert second.status_code == 400
    assert "duplicate" in second.json()["detail"].lower()


def test_fr_13_invalid_token_rejected_before_order_creation(client):
    """FR-13, EC-08: invalid token returns 401 before order creation."""

    response = client.post(
        "/orders",
        headers={"Authorization": "Bearer expired-or-invalid-token"},
        json=order_payload(client_order_key="invalid-token-order", quantity=1),
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized access"}

