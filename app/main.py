# app/main.py

from fastapi import FastAPI, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/users/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    users = crud.user.get(db)
    return users

@app.post("/users/", response_model=schemas.User)
def create_user(create_schema: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.user.create(db, create_schema)