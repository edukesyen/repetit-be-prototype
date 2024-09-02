# app/crud.py

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from . import models, schemas


class CRUDBase():
    def __init__(self):
        pass

    def get(self, db: Session):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class CRUDUser(CRUDBase):
    def get(self, db: Session):
        result = db.execute(select(models.User))
        return result.scalars().all()
    
    def create(self, db: Session, create_schema: schemas.UserCreate):
        db_data = models.User(**create_schema.dict())
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data
    
user = CRUDUser()