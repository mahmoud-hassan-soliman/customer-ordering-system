"""Order and kitchen routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from app.routers.dependencies import require_customer, require_kitchen
from app.schemas.order import CreateOrderRequest, StatusUpdateRequest
from app.services import order_service


router = APIRouter(tags=["orders"])


@router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(payload: CreateOrderRequest, current_user=Depends(require_customer)):
    try:
        order = order_service.create_order(
            customer_email=current_user.email,
            payload=payload.model_dump(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return _order_response(order)


@router.get("/orders/kitchen")
def kitchen_orders(current_user=Depends(require_kitchen)):
    return [_kitchen_order_response(order) for order in order_service.list_kitchen_orders()]


@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    payload: StatusUpdateRequest,
    current_user=Depends(require_kitchen),
):
    try:
        order = order_service.update_order_status(order_id, payload.status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"id": order.id, "status": order.status}


def _order_response(order):
    return {
        "id": order.id,
        "status": order.status,
        "items": [
            {
                "menu_item_id": item.menu_item_id,
                "quantity": item.quantity,
                "line_total": item.line_total,
            }
            for item in order.items
        ],
        "total": order.total,
    }


def _kitchen_order_response(order):
    return {
        "id": order.id,
        "customer_email": order.customer_email,
        "status": order.status,
        "total": order.total,
        "items": [
            {"name": item.menu_item.name, "quantity": item.quantity}
            for item in order.items
        ],
    }
