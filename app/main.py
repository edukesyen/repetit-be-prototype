# app/main.py

from fastapi import FastAPI, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/items/", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = await crud.get_items(db)
    return items

@app.post("/items/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return await crud.create_item(db, item)
