"""Database initialization and small menu seed."""

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import Base, engine
from app.models.menu import MenuItem


SEEDED_MENU = [
    {"name": "Chicken Sandwich", "price": 80.0, "available": True},
    {"name": "Pasta Bowl", "price": 95.0, "available": True},
    {"name": "Fresh Juice", "price": 35.0, "available": True},
]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_order_payment_columns()
    db = Session(bind=engine)
    try:
        seed_menu(db)
    finally:
        db.close()


def seed_menu(db: Session) -> None:
    if db.query(MenuItem).count() >= len(SEEDED_MENU):
        return
    existing_names = {item.name for item in db.query(MenuItem).all()}
    for item in SEEDED_MENU:
        if item["name"] not in existing_names:
            db.add(MenuItem(**item))
    db.commit()


def reset_db() -> None:
    Base.metadata.drop_all(bind=engine)
    init_db()


def ensure_order_payment_columns() -> None:
    with engine.begin() as connection:
        columns = {
            row[1]
            for row in connection.execute(text("PRAGMA table_info(orders)")).fetchall()
        }
        if columns and "payment_method" not in columns:
            connection.execute(
                text("ALTER TABLE orders ADD COLUMN payment_method VARCHAR NOT NULL DEFAULT 'cash'")
            )
        if columns and "payment_status" not in columns:
            connection.execute(
                text("ALTER TABLE orders ADD COLUMN payment_status VARCHAR NOT NULL DEFAULT 'unpaid'")
            )
