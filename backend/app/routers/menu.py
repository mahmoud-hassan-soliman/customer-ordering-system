"""Menu routes."""

from fastapi import APIRouter

from app.services.menu_service import list_menu_items


router = APIRouter(tags=["menu"])


@router.get("/menu")
def get_menu():
    return [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "available": item.available,
        }
        for item in list_menu_items()
    ]

