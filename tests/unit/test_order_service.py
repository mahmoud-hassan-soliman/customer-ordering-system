"""Failing-first unit tests for order and kitchen service rules."""

import pytest

from tests.utils.seed_data import DUPLICATE_CLIENT_ORDER_KEY, empty_order_payload, order_payload


pytestmark = [pytest.mark.unit, pytest.mark.tdd]


@pytest.mark.parametrize("quantity", [0, -1, 11])
def test_fr_05_quantity_validation_rejects_boundary_violations(
    service_modules, quantity
):
    """FR-05, EC-02: quantity must be between 1 and 10 inclusive."""

    order_service = service_modules["order_service"]

    with pytest.raises(ValueError, match="quantity"):
        order_service.validate_order_items(order_payload(quantity=quantity)["items"])


def test_fr_06_valid_order_placement_creates_pending_order(
    service_modules, customer_payload
):
    """FR-06: valid order creates a pending order with a calculated total."""

    order_service = service_modules["order_service"]

    order = order_service.create_order(
        customer_email=customer_payload["email"],
        payload=order_payload(quantity=2),
    )

    assert order.status == "pending"
    assert order.total > 0
    assert len(order.items) == 1


def test_fr_07_empty_cart_rejected(service_modules, customer_payload):
    """FR-07, EC-03: empty order items are rejected and create no order."""

    order_service = service_modules["order_service"]

    with pytest.raises(ValueError, match="at least one item"):
        order_service.create_order(
            customer_email=customer_payload["email"],
            payload=empty_order_payload(),
        )


def test_fr_08_duplicate_client_order_key_prevents_duplicate_order(
    service_modules, customer_payload
):
    """FR-08, EC-01: duplicate client_order_key cannot create two orders."""

    order_service = service_modules["order_service"]
    payload = order_payload(client_order_key=DUPLICATE_CLIENT_ORDER_KEY, quantity=1)

    first_order = order_service.create_order(
        customer_email=customer_payload["email"], payload=payload
    )

    with pytest.raises(ValueError, match="duplicate"):
        order_service.create_order(customer_email=customer_payload["email"], payload=payload)

    assert first_order.client_order_key == DUPLICATE_CLIENT_ORDER_KEY


def test_fr_09_kitchen_dashboard_lists_active_orders(
    service_modules, customer_payload
):
    """FR-09: kitchen dashboard returns active submitted orders."""

    order_service = service_modules["order_service"]
    created = order_service.create_order(
        customer_email=customer_payload["email"],
        payload=order_payload(client_order_key="client-order-key-dashboard", quantity=1),
    )

    orders = order_service.list_kitchen_orders()

    assert any(order.id == created.id for order in orders)


def test_fr_10_status_update_success_changes_order_status(
    service_modules, customer_payload
):
    """FR-10: kitchen staff can update status from pending to preparing."""

    order_service = service_modules["order_service"]
    created = order_service.create_order(
        customer_email=customer_payload["email"],
        payload=order_payload(client_order_key="client-order-key-status", quantity=1),
    )

    updated = order_service.update_order_status(created.id, "preparing")

    assert updated.status == "preparing"


def test_fr_12_invalid_status_transition_rejected_and_original_status_kept(
    service_modules, customer_payload
):
    """FR-12, EC-07: invalid status archived is rejected."""

    order_service = service_modules["order_service"]
    created = order_service.create_order(
        customer_email=customer_payload["email"],
        payload=order_payload(client_order_key="client-order-key-invalid-status", quantity=1),
    )

    with pytest.raises(ValueError, match="Invalid order status"):
        order_service.update_order_status(created.id, "archived")

    unchanged = order_service.get_order(created.id)
    assert unchanged.status == "pending"

