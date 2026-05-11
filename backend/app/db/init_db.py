"""Database initialization and small menu seed."""

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
