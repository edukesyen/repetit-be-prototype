# app/crud.py

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from .models import Item
from .schemas import ItemCreate

async def get_items(db: Session):
    result = await db.execute(select(Item))
    return result.scalars().all()

async def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item
