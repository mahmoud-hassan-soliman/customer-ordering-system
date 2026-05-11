"""Menu service functions.

Requirement coverage: FR-04.
"""

from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.menu import MenuItem


def list_menu_items() -> list[MenuItem]:
    init_db()
    db = SessionLocal()
    try:
        items = db.query(MenuItem).filter(MenuItem.available.is_(True)).all()
        for item in items:
            db.expunge(item)
        return items
    finally:
        db.close()

