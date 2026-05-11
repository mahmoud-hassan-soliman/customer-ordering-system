"""Failing-first FastAPI integration tests for kitchen contracts."""

import pytest

from tests.utils.seed_data import order_payload


pytestmark = [pytest.mark.integration, pytest.mark.tdd]


def test_fr_09_kitchen_dashboard_returns_orders(
    client, auth_headers, kitchen_headers
):
    """FR-09: kitchen staff can view active submitted orders."""

    created = client.post(
        "/orders",
        headers=auth_headers,
        json=order_payload(client_order_key="kitchen-dashboard-order", quantity=1),
    )

    response = client.get("/orders/kitchen", headers=kitchen_headers)

    assert created.status_code == 201
    assert response.status_code == 200
    assert any(order["id"] == created.json()["id"] for order in response.json())


def test_fr_10_kitchen_status_update_success(
    client, auth_headers, kitchen_headers
):
    """FR-10: kitchen staff can update order status."""

    created = client.post(
        "/orders",
        headers=auth_headers,
        json=order_payload(client_order_key="kitchen-status-order", quantity=1),
    )
    order_id = created.json()["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        headers=kitchen_headers,
        json={"status": "preparing"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "preparing"


def test_fr_11_customer_cannot_access_kitchen_dashboard(client, auth_headers):
    """FR-11, EC-04: customer token is rejected from kitchen dashboard."""

    response = client.get("/orders/kitchen", headers=auth_headers)

    assert response.status_code == 403
    assert response.json() == {"detail": "Kitchen role required"}


def test_fr_12_invalid_status_archived_returns_400_and_keeps_status(
    client, auth_headers, kitchen_headers
):
    """FR-12, EC-07: archived is not an allowed status."""

    created = client.post(
        "/orders",
        headers=auth_headers,
        json=order_payload(client_order_key="invalid-status-order", quantity=1),
    )
    order_id = created.json()["id"]

    response = client.patch(
        f"/orders/{order_id}/status",
        headers=kitchen_headers,
        json={"status": "archived"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid order status"}

    dashboard = client.get("/orders/kitchen", headers=kitchen_headers)
    stored = next(order for order in dashboard.json() if order["id"] == order_id)
    assert stored["status"] == "pending"


def test_fr_13_invalid_token_rejected_from_kitchen_endpoint(client):
    """FR-13, EC-08: invalid token blocks protected kitchen access."""

    response = client.get(
        "/orders/kitchen",
        headers={"Authorization": "Bearer expired-or-invalid-token"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized access"}

