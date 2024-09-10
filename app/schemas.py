# app/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: str
    password: str
    diamond: int
    star: int

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True




class TopicBase(BaseModel):
    name: str
    tag: str
    user_id: int

class TopicCreate(TopicBase):
    pass

class TopicUpdate(TopicBase):
    pass

class Topic(TopicBase):
    id: int

    class Config:
        orm_mode = True




class MaterialBase(BaseModel):
    topic_id: int
    name: str
    content: str
    # type: str
    # file_name: Optional[str]
    # file_path: Optional[str]

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int

    class Config:
        orm_mode = True


class FlashcardBase(BaseModel):
    topic_id: int
    due_date: datetime
    created_at: datetime
    question: str
    expected_answer: str
    answer_criteria_1: str
    answer_criteria_2: str
    answer_criteria_3: str
    

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(FlashcardBase):
    topic_id: Optional[int] = None
    due_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    question: Optional[str] = None
    expected_answer: Optional[str] = None
    answer_criteria_1: Optional[str] = None
    answer_criteria_2: Optional[str] = None
    answer_criteria_3: Optional[str] = None

    class Config:
        orm_mode = True

class Flashcard(FlashcardBase):
    id: int

    class Config:
        orm_mode = True




class FlashcardReviewBase(BaseModel):
    flashcard_id: int
    date: datetime
    answer: str
    score: int
    review: str
    passed_criteria_1: bool
    passed_criteria_2: bool
    passed_criteria_3: bool

class FlashcardReviewCreate(FlashcardReviewBase):
    pass

class FlashcardReviewUpdate(FlashcardReviewBase):
    pass

class FlashcardReview(FlashcardReviewBase):
    id: int

    class Config:
        orm_mode = True



