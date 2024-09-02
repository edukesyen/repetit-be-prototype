# app/main.py

# from typing import List
from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.get("/users/", response_model=list[schemas.User])
def read_users(
    db: Session = Depends(get_db)
):
    return crud.user.get(db)

@app.post("/users/", response_model=schemas.User)
def create_user(
    user_in: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    return crud.user.create(db, user_in)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    db_user = crud.user.get_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, 
    user_in: schemas.UserUpdate, 
    db: Session = Depends(get_db)
):
    db_user = crud.user.get_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.user.update(db, db_user, user_in)

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    db_user = crud.user.delete(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user