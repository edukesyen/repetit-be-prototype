# app/main.py

# from typing import List
from fastapi import FastAPI, Depends, HTTPException
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

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    db_user = crud.user.get_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/", response_model=schemas.User)
def create_user(
    user_in: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    return crud.user.create(db, user_in)

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







@app.get("/topics/", response_model=list[schemas.Topic])
def read_topics(
    db: Session = Depends(get_db)
):
    return crud.topic.get(db)

@app.get("/topics/{topic_id}", response_model=schemas.Topic)
def read_topic(
    topic_id: int, 
    db: Session = Depends(get_db)
):
    db_topic = crud.topic.get_by_id(db, topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return db_topic

@app.get("/topics/user/{user_id}", response_model=list[schemas.Topic])
def read_topics_by_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    db_user = crud.user.get_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud.topic.get_by_user_id(db, user_id)

@app.post("/topics/", response_model=schemas.Topic)
def create_topic(
    topic_in: schemas.TopicCreate, 
    db: Session = Depends(get_db)
):
    return crud.topic.create(db, topic_in)

@app.put("/topics/{topic_id}", response_model=schemas.Topic)
def update_topic(
    topic_id: int, 
    topic_in: schemas.TopicUpdate, 
    db: Session = Depends(get_db)
):
    db_topic = crud.topic.get_by_id(db, topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return crud.topic.update(db, db_topic, topic_in)

@app.delete("/topics/{topic_id}", response_model=schemas.Topic)
def delete_topic(
    topic_id: int, 
    db: Session = Depends(get_db)
):
    db_topic = crud.topic.delete(db, topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return db_topic