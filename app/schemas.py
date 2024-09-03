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
    type: str
    file_name: Optional[str]
    file_path: Optional[str]
    content: str

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
    question: str
    due_date: datetime
    review_criteria: str

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(FlashcardBase):
    pass

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
    
class FlashcardReviewCreate(FlashcardReviewBase):
    pass

class FlashcardReviewUpdate(FlashcardReviewBase):
    pass

class FlashcardReview(FlashcardReviewBase):
    id: int

    class Config:
        orm_mode = True



