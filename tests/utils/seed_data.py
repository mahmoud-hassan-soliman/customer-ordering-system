"""Seeded payloads shared by failing-first tests."""

CUSTOMER_USER = {
    "name": "Mina Customer",
    "email": "mina.customer@example.com",
    "password": "password123",
    "role": "customer",
}

KITCHEN_USER = {
    "name": "Salma Kitchen",
    "email": "salma.kitchen@example.com",
    "password": "kitchen123",
    "role": "kitchen",
}

MENU_ITEMS = [
    {"id": 1, "name": "Chicken Sandwich", "price": 80.0, "available": True},
    {"id": 2, "name": "Pasta Bowl", "price": 95.0, "available": True},
    {"id": 3, "name": "Fresh Juice", "price": 35.0, "available": True},
]

VALID_CLIENT_ORDER_KEY = "client-order-key-001"
DUPLICATE_CLIENT_ORDER_KEY = "client-order-key-duplicate"
INVALID_TOKEN = "expired-or-invalid-token"


def order_payload(client_order_key: str = VALID_CLIENT_ORDER_KEY, quantity: int = 1) -> dict:
    return {
        "client_order_key": client_order_key,
        "items": [{"menu_item_id": 1, "quantity": quantity}],
    }


def empty_order_payload(client_order_key: str = "client-order-key-empty") -> dict:
    return {"client_order_key": client_order_key, "items": []}

