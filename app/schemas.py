# app/schemas.py

from pydantic import BaseModel


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