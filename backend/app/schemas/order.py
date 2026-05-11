"""Order request and response schemas."""

from pydantic import BaseModel


class OrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int


class CreateOrderRequest(BaseModel):
    client_order_key: str
    items: list[OrderItemRequest]


class OrderItemResponse(BaseModel):
    menu_item_id: int
    quantity: int
    line_total: float


class OrderResponse(BaseModel):
    id: int
    status: str
    items: list[OrderItemResponse]
    total: float


class KitchenOrderItemResponse(BaseModel):
    name: str
    quantity: int


class KitchenOrderResponse(BaseModel):
    id: int
    customer_email: str
    status: str
    total: float
    items: list[KitchenOrderItemResponse]


class StatusUpdateRequest(BaseModel):
    status: str


class StatusUpdateResponse(BaseModel):
    id: int
    status: str

