# app/main.py

import datetime
# from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import engine, get_db
from .fsrs_scheduler import FSRSScheduler

from .flashcard import Flashcard

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://repetit.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/flashcards/generate", response_model=None)
def generate_flashcard(
    # topic_id: int,
    obj_in: dict = {"topic_id": 0, "datetime_today": "datetime_iso"},
    db: Session = Depends(get_db),
):
    topic_id = obj_in["topic_id"]
    
    materials = crud.material.get_by_topic_id(db, topic_id)
    materials = [material.content for material in materials]
    material = " __[divider]__ ".join(materials)
    # print(material)    
    flashcard = Flashcard(material)
    questions_df = flashcard.generate()
    flashcards = questions_df.to_dict(orient="records")
    
    for flashcard in flashcards:
        print(flashcard)
        # today = datetime.datetime.now(datetime.timezone.utc)
        today = obj_in["datetime_today"]
        today = datetime.datetime.strptime(today,  "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
        data = {
            "topic_id": topic_id,
            "due_date": today + datetime.timedelta(hours=1),
            "created_at": today,
            "question": flashcard["question"], 
            "expected_answer": flashcard["expected_answer"],
            "answer_criteria_1": flashcard["answer_criteria_1"],
            "answer_criteria_2": flashcard["answer_criteria_2"],
            "answer_criteria_3": flashcard["answer_criteria_3"],
        }
        flashcard_create = schemas.FlashcardCreate(**data)
        crud.flashcard.create(db, flashcard_create)
    
    return jsonable_encoder(flashcards)


@app.post("/flashcards/evaluate", response_model=None)
def evaluate_flashcard(
    obj_in: dict = {"flashcard_id": 0,"answer": "string", "datetime_today": "datetime_iso"},
    db: Session = Depends(get_db),
):
    flashcard_id = obj_in["flashcard_id"]
    fc = crud.flashcard.get_by_id(db, flashcard_id)
    topic_id = fc.topic_id
    print(obj_in["answer"])

    materials = crud.material.get_by_topic_id(db, topic_id)
    materials = [material.content for material in materials]
    material = " __[divider]__ ".join(materials)  

    flashcard = Flashcard(material)
    
    evaluation_df = flashcard.evaluate(
        question=fc.question,
        answer=obj_in["answer"],
        expected_answer=fc.expected_answer,
        answer_criteria_1=fc.answer_criteria_1,
        answer_criteria_2=fc.answer_criteria_2,
        answer_criteria_3=fc.answer_criteria_3,
    )
    evaluations = evaluation_df.to_dict(orient="records")  

    for evaluation in evaluations:
        score = int(evaluation["passed_criteria_1"]) + int(evaluation["passed_criteria_2"]) + int(evaluation["passed_criteria_3"])  

        # today = datetime.datetime.now(datetime.timezone.utc)
        today = obj_in["datetime_today"]
        today = datetime.datetime.strptime(today, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
        today = today + datetime.timedelta(hours=1)
        print(evaluation)
        data = {
            "flashcard_id": flashcard_id,
            "date": today,
            "answer": obj_in["answer"], 
            "score": score, 
            "review": "null",
            "passed_criteria_1": bool(evaluation["passed_criteria_1"]),
            "passed_criteria_2": bool(evaluation["passed_criteria_2"]),
            "passed_criteria_3": bool(evaluation["passed_criteria_3"]),
        }
        print(data)
        evaluation_create = schemas.FlashcardReviewCreate(**data)
        crud.flashcard_review.create(db, evaluation_create)

        # first_review = (
        #     db.query(models.FlashcardReview)
        #     .filter(models.FlashcardReview.flashcard_id == flashcard_id)
        #     .order_by(models.FlashcardReview.date.asc())
        #     .first()
        # )

        # if first_review:
        #     first_review_date = first_review.date
        # else:
        #     first_review_date = datetime.datetime.now(datetime.timezone.utc)
        
        # first_review_date = first_review_date.replace(tzinfo=datetime.timezone.utc)

        # fc_created_at = datetime.datetime.strptime(fc.created_at, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
        fc_created_at = fc.created_at
        fc_created_at = fc_created_at.isoformat()
        # fc_created_at = datetime.datetime.strptime(fc_created_at, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)
        fc_created_at = datetime.datetime.strptime(fc_created_at, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=datetime.timezone.utc)
        fc_created_at = fc_created_at + datetime.timedelta(hours=1)

        fsrs_scheduler = FSRSScheduler(
            flashcard_id=flashcard_id, 
            first_review_date=fc_created_at
        )

        review_history = (
            db.query(models.FlashcardReview)
            .filter(models.FlashcardReview.flashcard_id == flashcard_id)
            .order_by(models.FlashcardReview.date.asc()).all()
        )
        for review in review_history:
            fsrs_scheduler.add_review(review.score)

        fsrs_scheduler.add_review(score)
        fc_upd_data = {
            "due_date": fsrs_scheduler.get_next_review()
        }
        flashcard_update = schemas.FlashcardUpdate(**fc_upd_data)
        db_flashcard = crud.flashcard.get_by_id(db, flashcard_id)
        if db_flashcard is None:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        crud.flashcard.update(db, db_flashcard, flashcard_update)

    return jsonable_encoder(evaluations)



@app.get("/flashcards/last-review/{flashcard_id}", response_model=None)
def get_flashcard_last_review(
    flashcard_id: int,
    db: Session = Depends(get_db)
):
    flaschcard_detail = (
        db.query(models.Flashcard)
        .filter(models.Flashcard.id == flashcard_id)
        .first()
    )
    last_review = (
        db.query(models.FlashcardReview)
        .filter(models.FlashcardReview.flashcard_id == flashcard_id)
        .order_by(models.FlashcardReview.id.desc())
        .first()
    )
    topic_id = (
        db.query(models.Flashcard)
        .filter(models.Flashcard.id == flashcard_id)
        .first()
        .topic_id
    )
    topic_name = (
        db.query(models.Topic)
        .filter(models.Topic.id == topic_id)
        .first()
        .name
    )

    response = {
        "topic": topic_name,
        "question": flaschcard_detail.question,
        "answer": last_review.answer,
        "score": last_review.score,
        "next_review_date": datetime.datetime.fromisoformat(str(flaschcard_detail.due_date)).strftime("%d %B %Y %H:%M:%S"),
        "next_review_date_iso": flaschcard_detail.due_date,
        "criteria": [
            {
                "passed": int(last_review.passed_criteria_1),
                "name": flaschcard_detail.answer_criteria_1,
            },
            {
                "passed": int(last_review.passed_criteria_2),
                "name": flaschcard_detail.answer_criteria_2,
            },
            {
                "passed": int(last_review.passed_criteria_3),
                "name": flaschcard_detail.answer_criteria_3,
            },
        ]
    }

    return jsonable_encoder(response)


@app.get("/flashcards/todays-review/{topic_id}", response_model=None)
def get_todays_review(
    topic_id: int,
    db: Session = Depends(get_db),
):
    topic = crud.topic.get_by_id(db, topic_id)
    print('TOPIC',topic)

    flashcards = crud.flashcard.get_by_topic_id(db, topic_id)
    flashcards_due_today = []
    for flashcard in flashcards:
        if flashcard.due_date.date() ==  datetime.datetime.now().date():
            flashcards_due_today.append(flashcard)

    review_score_count = {
        "easy": 0,
        "good": 0,
        "hard": 0,
    }

    for flashcard in flashcards_due_today:
        print("FC_ID",flashcard.id)
        reviews = crud.flashcard_review.get_by_flashcard_id(db, flashcard.id)

        print("REVIEWS",reviews)

        if len(reviews) > 0:
            review = reviews[-1]
            print(review.score)
            if review.score == 3:
                review_score_count['easy'] += 1
            elif review.score == 2:
                review_score_count["good"] += 1
            elif review.score == 1:
                review_score_count["hard"] += 1

    flashcard_list = [{"flashcard_id": fcdt.id, "topic_id": fcdt.topic_id} for fcdt in flashcards_due_today]
    flashcard_list = sorted(flashcard_list, key=lambda k: k["flashcard_id"])

    response = {
        "topic_name": topic.name,
        "topic_tag": topic.tag,
        "flashcard_count": len(flashcards_due_today),
        "flashcard_list": flashcard_list,
        "last_review": {
            "easy": review_score_count['easy'],
            "good": review_score_count['good'],
            "hard": review_score_count['hard'],
        }
    }
    return jsonable_encoder(response)
    

# @app.post("/materials", response_model=None)
# def add_material(
#     obj_in: dict = {"topic_id": 0,"content": "string"},
#     db: Session = Depends(get_db)
# ):
#     pass



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
@app.get("/flashcards/topic/{topic_id}", response_model=list[schemas.Flashcard])
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
@app.get("/flashcard-reviews/flashcard/{flashcard_id}", response_model=list[schemas.FlashcardReview])
def read_flashcard_reviews_by_flashcard(
    flashcard_id: int, 
    db: Session = Depends(get_db)
):
    db_flashcard = crud.flashcard.get_by_id(db, flashcard_id)
    if db_flashcard is None:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    return crud.flashcard_review.get_by_flashcard_id(db, flashcard_id)
