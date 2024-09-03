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





@app.get("/materials/", response_model=list[schemas.Material])
def read_materials(
    db: Session = Depends(get_db)
):
    return crud.material.get(db)

@app.post("/materials/", response_model=schemas.Material)
def create_material(
    material_in: schemas.MaterialCreate, 
    db: Session = Depends(get_db)
):
    return crud.material.create(db, material_in)

@app.get("/materials/{material_id}", response_model=schemas.Material)
def read_material(
    material_id: int, 
    db: Session = Depends(get_db)
):
    db_material = crud.material.get_by_id(db, material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

@app.put("/materials/{material_id}", response_model=schemas.Material)
def update_material(
    material_id: int, 
    material_in: schemas.MaterialUpdate, 
    db: Session = Depends(get_db)
):
    db_material = crud.material.get_by_id(db, material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return crud.material.update(db, db_material, material_in)

@app.delete("/materials/{material_id}", response_model=schemas.Material)
def delete_material(
    material_id: int, 
    db: Session = Depends(get_db)
):
    db_material = crud.material.delete(db, material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

# Endpoint to get materials by topic_id
@app.get("/materials/topic/{topic_id}", response_model=list[schemas.Material])
def read_materials_by_topic(
    topic_id: int, 
    db: Session = Depends(get_db)
):
    db_topic = crud.topic.get_by_id(db, topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return crud.material.get_by_topic_id(db, topic_id)






@app.get("/flashcards/", response_model=list[schemas.Flashcard])
def read_flashcards(
    db: Session = Depends(get_db)
):
    return crud.flashcard.get(db)

@app.post("/flashcards/", response_model=schemas.Flashcard)
def create_flashcard(
    flashcard_in: schemas.FlashcardCreate, 
    db: Session = Depends(get_db)
):
    return crud.flashcard.create(db, flashcard_in)

@app.get("/flashcards/{flashcard_id}", response_model=schemas.Flashcard)
def read_flashcard(
    flashcard_id: int, 
    db: Session = Depends(get_db)
):
    db_flashcard = crud.flashcard.get_by_id(db, flashcard_id)
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return db_flashcard

@app.put("/flashcards/{flashcard_id}", response_model=schemas.Flashcard)
def update_flashcard(
    flashcard_id: int, 
    flashcard_in: schemas.FlashcardUpdate, 
    db: Session = Depends(get_db)
):
    db_flashcard = crud.flashcard.get_by_id(db, flashcard_id)
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return crud.flashcard.update(db, db_flashcard, flashcard_in)

@app.delete("/flashcards/{flashcard_id}", response_model=schemas.Flashcard)
def delete_flashcard(
    flashcard_id: int, 
    db: Session = Depends(get_db)
):
    db_flashcard = crud.flashcard.delete(db, flashcard_id)
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return db_flashcard

# Endpoint to get flashcards by topic_id
@app.get("/topics/{topic_id}/flashcards/", response_model=list[schemas.Flashcard])
def read_flashcards_by_topic(
    topic_id: int, 
    db: Session = Depends(get_db)
):
    db_topic = crud.topic.get_by_id(db, topic_id)
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    return crud.flashcard.get_by_topic_id(db, topic_id)




# FlashcardReview endpoints
@app.get("/flashcard-reviews/", response_model=list[schemas.FlashcardReview])
def read_flashcard_reviews(
    db: Session = Depends(get_db)
):
    return crud.flashcard_review.get(db)

@app.post("/flashcard-reviews/", response_model=schemas.FlashcardReview)
def create_flashcard_review(
    flashcard_review_in: schemas.FlashcardReviewCreate, 
    db: Session = Depends(get_db)
):
    return crud.flashcard_review.create(db, flashcard_review_in)

@app.get("/flashcard-reviews/{flashcard_review_id}", response_model=schemas.FlashcardReview)
def read_flashcard_review(
    flashcard_review_id: int, 
    db: Session = Depends(get_db)
):
    db_flashcard_review = crud.flashcard_review.get_by_id(db, flashcard_review_id)
    if db_flashcard_review is None:
        raise HTTPException(status_code=404, detail="Flashcard review not found")
    return db_flashcard_review

@app.put("/flashcard-reviews/{flashcard_review_id}", response_model=schemas.FlashcardReview)
def update_flashcard_review(
    flashcard_review_id: int, 
    flashcard_review_in: schemas.FlashcardReviewUpdate, 
    db: Session = Depends(get_db)
):
    db_flashcard_review = crud.flashcard_review.get_by_id(db, flashcard_review_id)
    if db_flashcard_review is None:
        raise HTTPException(status_code=404, detail="Flashcard review not found")
    return crud.flashcard_review.update(db, db_flashcard_review, flashcard_review_in)

@app.delete("/flashcard-reviews/{flashcard_review_id}", response_model=schemas.FlashcardReview)
def delete_flashcard_review(
    flashcard_review_id: int, 
    db: Session = Depends(get_db)
):
    db_flashcard_review = crud.flashcard_review.delete(db, flashcard_review_id)
    if db_flashcard_review is None:
        raise HTTPException(status_code=404, detail="Flashcard review not found")
    return db_flashcard_review

# Endpoint to get flashcard reviews by flashcard_id
@app.get("/flashcards/{flashcard_id}/reviews/", response_model=list[schemas.FlashcardReview])
def read_flashcard_reviews_by_flashcard(
    flashcard_id: int, 
    db: Session = Depends(get_db)
):
    db_flashcard = crud.flashcard.get_by_id(db, flashcard_id)
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    return crud.flashcard_review.get_by_flashcard_id(db, flashcard_id)