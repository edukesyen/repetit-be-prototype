# app/models.py

from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, relationship
from .database import Base  # Ensure this is correctly imported


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    diamond = Column(Integer, nullable=True)
    star = Column(Integer, nullable=True)
    streak = Column(Integer, nullable=True)
    target = Column(Integer, nullable=True)

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
    name = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # type = Column(String, nullable=False)
    # file_name = Column(String, nullable=True)
    # file_path = Column(String, nullable=True)

    topic: Mapped["Topic"] = relationship(back_populates='materials')


class Flashcard(Base):
    __tablename__ = "flashcards"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=True)
    question = Column(String, nullable=False)
    expected_answer = Column(String, nullable=True)
    answer_criteria_1 = Column(String, nullable=True)
    answer_criteria_2 = Column(String, nullable=True)
    answer_criteria_3 = Column(String, nullable=True)

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
    passed_criteria_1 = Column(Boolean, nullable=True)
    passed_criteria_2 = Column(Boolean, nullable=True)
    passed_criteria_3 = Column(Boolean, nullable=True)

    flashcard: Mapped['Flashcard'] = relationship(back_populates='flashcard_reviews')


