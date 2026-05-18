"""Order service functions.

Requirement coverage: FR-05, FR-06, FR-07, FR-08, FR-09, FR-10, FR-12, FR-15, FR-16.
"""

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.menu import MenuItem
from app.models.order import Order, OrderItem


ALLOWED_STATUSES = {"pending", "preparing", "ready", "completed"}
PAYMENT_METHODS = {"cash", "card", "wallet"}
PAYMENT_STATUSES = {"paid", "unpaid"}


def validate_order_items(items: list[dict]) -> None:
    if not items:
        raise ValueError("Order must contain at least one item")
    for item in items:
        quantity = item["quantity"]
        if not isinstance(quantity, int) or quantity < 1 or quantity > 10:
            raise ValueError("quantity must be between 1 and 10")


def create_order(customer_email: str, payload: dict) -> Order:
    init_db()
    items = payload["items"]
    validate_order_items(items)
    payment_method = payload.get("payment_method", "cash")
    payment_status = payload.get("payment_status", "unpaid")
    if payment_method not in PAYMENT_METHODS:
        raise ValueError("Invalid payment method")
    if payment_status not in PAYMENT_STATUSES:
        raise ValueError("Invalid payment status")

    db = SessionLocal()
    try:
        existing = (
            db.query(Order)
            .filter(Order.client_order_key == payload["client_order_key"])
            .first()
        )
        if existing:
            raise ValueError("duplicate client_order_key")

        order = Order(
            customer_email=customer_email,
            status="pending",
            client_order_key=payload["client_order_key"],
            total=0.0,
            payment_method=payment_method,
            payment_status=payment_status,
        )
        db.add(order)
        db.flush()

        total = 0.0
        for item in items:
            menu_item = (
                db.query(MenuItem)
                .filter(
                    MenuItem.id == item["menu_item_id"],
                    MenuItem.available.is_(True),
                )
                .first()
            )
            if menu_item is None:
                raise ValueError("Menu item not found")
            line_total = menu_item.price * item["quantity"]
            total += line_total
            db.add(
                OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item.id,
                    quantity=item["quantity"],
                    line_total=line_total,
                )
            )

        order.total = total
        db.commit()
        db.refresh(order)
        _load_order_items(db, order)
        db.expunge(order)
        return order
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def list_kitchen_orders() -> list[Order]:
    init_db()
    db = SessionLocal()
    try:
        orders = (
            db.query(Order)
            .filter(Order.status.in_(["pending", "preparing", "ready"]))
            .order_by(Order.id)
            .all()
        )
        for order in orders:
            _load_order_items(db, order)
            db.expunge(order)
        return orders
    finally:
        db.close()


def list_customer_orders(customer_email: str) -> list[Order]:
    init_db()
    db = SessionLocal()
    try:
        orders = (
            db.query(Order)
            .filter(Order.customer_email == customer_email)
            .order_by(Order.id.desc())
            .all()
        )
        for order in orders:
            _load_order_items(db, order)
            db.expunge(order)
        return orders
    finally:
        db.close()


def get_order(order_id: int) -> Order:
    init_db()
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order is None:
            raise LookupError("Order not found")
        _load_order_items(db, order)
        db.expunge(order)
        return order
    finally:
        db.close()


def update_order_status(order_id: int, status: str) -> Order:
    init_db()
    if status not in ALLOWED_STATUSES:
        raise ValueError("Invalid order status")

    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order is None:
            raise LookupError("Order not found")
        order.status = status
        db.commit()
        db.refresh(order)
        _load_order_items(db, order)
        db.expunge(order)
        return order
    finally:
        db.close()


def _load_order_items(db, order: Order) -> None:
    for item in order.items:
        _ = item.menu_item.name
