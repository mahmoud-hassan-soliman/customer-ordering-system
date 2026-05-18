"""Order request and response schemas."""

from pydantic import BaseModel


class OrderItemRequest(BaseModel):
    menu_item_id: int
    quantity: int


class CreateOrderRequest(BaseModel):
    client_order_key: str
    items: list[OrderItemRequest]
    payment_method: str = "cash"
    payment_status: str = "unpaid"


class OrderItemResponse(BaseModel):
    menu_item_id: int
    quantity: int
    line_total: float


class OrderResponse(BaseModel):
    id: int
    status: str
    items: list[OrderItemResponse]
    total: float
    payment_method: str
    payment_status: str


class KitchenOrderItemResponse(BaseModel):
    name: str
    quantity: int


class KitchenOrderResponse(BaseModel):
    id: int
    customer_email: str
    status: str
    total: float
    payment_method: str
    payment_status: str
    items: list[KitchenOrderItemResponse]


class CustomerOrderItemResponse(BaseModel):
    name: str
    quantity: int
    line_total: float


class CustomerOrderResponse(BaseModel):
    id: int
    status: str
    total: float
    payment_method: str
    payment_status: str
    items: list[CustomerOrderItemResponse]


class StatusUpdateRequest(BaseModel):
    status: str


class StatusUpdateResponse(BaseModel):
    id: int
    status: str
