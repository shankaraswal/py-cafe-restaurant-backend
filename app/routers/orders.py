from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db
from app.routers.cart import calculate_cart_total

router = APIRouter()

@router.post("/orders", response_model=schemas.OrderConfirmation)
async def create_order(session_id: str, db: Session = Depends(get_db)):
    """Create order from cart"""
    # Get cart
    cart = db.query(models.Cart).filter(models.Cart.session_id == session_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    if not cart.cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total
    total_amount = calculate_cart_total(cart)
    
    # Create order
    order = models.Order(
        cart_id=cart.id,
        total_amount=total_amount,
        status=models.OrderStatus.PENDING
    )
    
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Generate greeting message
    total_items = sum(item.quantity for item in cart.cart_items)
    greeting_message = f"Thank you for your order! Your order #{order.id} has been placed successfully. Total: ${total_amount:.2f} for {total_items} items. We'll have it ready soon!"
    
    return schemas.OrderConfirmation(
        order=order,
        message=greeting_message
    )

@router.get("/orders/{order_id}", response_model=schemas.Order)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order details"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/orders", response_model=List[schemas.Order])
async def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all orders (for admin use)"""
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return orders

@router.put("/orders/{order_id}", response_model=schemas.Order)
async def update_order_status(
    order_id: int, 
    status: str = Query(..., description="Order status: pending, completed, or cancelled"), 
    db: Session = Depends(get_db)
):
    """Update order status (for admin use)"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Validate and convert string to enum
    try:
        status_enum = models.OrderStatus(status.lower())
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid status. Must be one of: {[s.value for s in models.OrderStatus]}"
        )
    
    order.status = status_enum
    db.commit()
    db.refresh(order)
    return order