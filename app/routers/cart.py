from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter()

def get_or_create_cart(session_id: str, db: Session):
    """Get existing cart or create new one for session"""
    cart = db.query(models.Cart).filter(models.Cart.session_id == session_id).first()
    if not cart:
        cart = models.Cart(session_id=session_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def calculate_cart_total(cart: models.Cart):
    """Calculate total amount for cart"""
    total = 0
    for item in cart.cart_items:
        total += item.menu_item.price * item.quantity
    return total

@router.post("/cart/{session_id}/items", response_model=schemas.CartSummary)
async def add_to_cart(
    session_id: str, 
    cart_item: schemas.CartItemCreate, 
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    # Verify menu item exists
    menu_item = db.query(models.MenuItem).filter(
        models.MenuItem.id == cart_item.menu_item_id
    ).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Get or create cart
    cart = get_or_create_cart(session_id, db)
    
    # Check if item already exists in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.menu_item_id == cart_item.menu_item_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += cart_item.quantity
    else:
        # Add new item
        new_cart_item = models.CartItem(
            cart_id=cart.id,
            menu_item_id=cart_item.menu_item_id,
            quantity=cart_item.quantity
        )
        db.add(new_cart_item)
    
    db.commit()
    db.refresh(cart)
    
    total_amount = calculate_cart_total(cart)
    total_items = sum(item.quantity for item in cart.cart_items)
    
    return schemas.CartSummary(
        cart=cart,
        total_amount=total_amount,
        total_items=total_items
    )

@router.get("/cart/{session_id}", response_model=schemas.CartSummary)
async def get_cart(session_id: str, db: Session = Depends(get_db)):
    """Get cart contents"""
    cart = get_or_create_cart(session_id, db)
    
    total_amount = calculate_cart_total(cart)
    total_items = sum(item.quantity for item in cart.cart_items)
    
    return schemas.CartSummary(
        cart=cart,
        total_amount=total_amount,
        total_items=total_items
    )

@router.put("/cart/{session_id}/items/{item_id}", response_model=schemas.CartSummary)
async def update_cart_item(
    session_id: str,
    item_id: int,
    cart_item_update: schemas.CartItemUpdate,
    db: Session = Depends(get_db)
):
    """Update item quantity in cart"""
    cart = get_or_create_cart(session_id, db)
    
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.id == item_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    cart_item.quantity = cart_item_update.quantity
    db.commit()
    db.refresh(cart)
    
    total_amount = calculate_cart_total(cart)
    total_items = sum(item.quantity for item in cart.cart_items)
    
    return schemas.CartSummary(
        cart=cart,
        total_amount=total_amount,
        total_items=total_items
    )

@router.delete("/cart/{session_id}/items/{item_id}", response_model=schemas.CartSummary)
async def remove_from_cart(
    session_id: str,
    item_id: int,
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart = get_or_create_cart(session_id, db)
    
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.id == item_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    db.refresh(cart)
    
    total_amount = calculate_cart_total(cart)
    total_items = sum(item.quantity for item in cart.cart_items)
    
    return schemas.CartSummary(
        cart=cart,
        total_amount=total_amount,
        total_items=total_items
    )

@router.delete("/cart/{session_id}", response_model=dict)
async def clear_cart(session_id: str, db: Session = Depends(get_db)):
    """Clear all items from cart"""
    cart = db.query(models.Cart).filter(models.Cart.session_id == session_id).first()
    if cart:
        db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()
        db.commit()
    
    return {"message": "Cart cleared successfully"}