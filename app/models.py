# app/models.py

from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
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
    materials: Mapped[List["Material"]] = relationship(back_populates='topic')
    flashcards: Mapped[List["Flashcard"]] = relationship(back_populates='topic')


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    type = Column(String, nullable=False)
    file_name = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    content = Column(String, nullable=False)

    topic: Mapped["Topic"] = relationship(back_populates='materials')


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    question = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=True)
    review_criteria = Column(String, nullable=False)

    topic: Mapped["Topic"] = relationship(back_populates='flashcards')
    flashcard_reviews: Mapped[List['FlashcardReview']] = relationship(back_populates='flashcard')



class FlashcardReview(Base):
    __tablename__ = "flashcard_reviews"

    id = Column(Integer, primary_key=True, index=True)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id"))
    date = Column(DateTime, nullable=False)
    answer = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    review = Column(String, nullable=False)

    flashcard: Mapped['Flashcard'] = relationship(back_populates='flashcard_reviews')

