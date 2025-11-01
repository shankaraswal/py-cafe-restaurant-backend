from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.get("/menu", response_model=List[schemas.MenuItem])
async def get_menu_items(db: Session = Depends(get_db)):
    """Get all menu items"""
    menu_items = db.query(models.MenuItem).all()
    return menu_items

@router.get("/menu/{item_id}", response_model=schemas.MenuItem)
async def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific menu item by ID"""
    menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return menu_item

@router.post("/menu", response_model=schemas.MenuItem)
async def create_menu_item(menu_item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    """Create a new menu item (for admin use)"""
    db_menu_item = models.MenuItem(**menu_item.dict())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item