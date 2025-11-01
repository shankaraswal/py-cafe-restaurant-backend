from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# Menu Item Schemas
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    image_url: Optional[str] = None

class MenuItemCreate(MenuItemBase):
    pass

class MenuItem(MenuItemBase):
    id: int
    
    class Config:
        from_attributes = True

# Cart Schemas
class CartItemBase(BaseModel):
    menu_item_id: int
    quantity: int = Field(..., gt=0)

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)

class CartItem(CartItemBase):
    id: int
    menu_item: MenuItem
    
    class Config:
        from_attributes = True

class CartBase(BaseModel):
    session_id: str

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int
    created_at: datetime
    cart_items: List[CartItem] = []
    
    class Config:
        from_attributes = True

# Order Schemas
class OrderBase(BaseModel):
    cart_id: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    status: OrderStatus
    total_amount: float
    created_at: datetime
    cart: Cart
    
    class Config:
        from_attributes = True

# Response Schemas
class CartSummary(BaseModel):
    cart: Cart
    total_amount: float
    total_items: int

class OrderConfirmation(BaseModel):
    order: Order
    message: str