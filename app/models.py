# app/models.py

from sqlalchemy import Column, Integer, String
from .database import Base  # Ensure this is correctly imported

class Item(Base):  # Make sure to inherit from Base
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    # qty = Column(Integer, index=True)