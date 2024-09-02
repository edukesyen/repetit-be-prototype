# app/models.py

from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from .database import Base  # Ensure this is correctly imported


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    diamond = Column(Integer)
    star = Column(Integer)

    topics: Mapped[List["Topic"]] = relationship(back_populates="user")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates='topics')
