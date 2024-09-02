# # app/crud.py

# from sqlalchemy.orm import Session
# from sqlalchemy.future import select
# from . import models, schemas


# class CRUDBase():
#     def __init__(self):
#         pass

#     def get(self, db: Session):
#         pass

#     def create(self):
#         pass

#     def update(self):
#         pass

#     def delete(self):
#         pass


# class CRUDUser(CRUDBase):
#     def get(self, db: Session):
#         result = db.execute(select(models.User))
#         return result.scalars().all()
    
#     def create(self, db: Session, create_schema: schemas.UserCreate):
#         db_data = models.User(**create_schema.dict())
#         db.add(db_data)
#         db.commit()
#         db.refresh(db_data)
#         return db_data
    
# user = CRUDUser()




# app/crud.py

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from . import models, schemas


class CRUDBase:
    def __init__(self, model):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        self.model = model

    def get(self, db: Session):
        return db.execute(select(self.model)).scalars().all()

    def get_by_id(self, db: Session, id: int):
        return db.execute(select(self.model).where(self.model.id == id)).scalar_one_or_none()

    def create(self, db: Session, obj_in):
        db_obj = self.model(**obj_in.dict())  # Convert Pydantic model to dictionary
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj, obj_in):
        obj_data = obj_in.dict(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        obj = db.execute(select(self.model).where(self.model.id == id)).scalar_one_or_none()
        if obj:
            db.delete(obj)
            db.commit()
        return obj


class CRUDUser(CRUDBase):
    def __init__(self):
        super().__init__(models.User)


# Initialize CRUDUser instance
user = CRUDUser()
