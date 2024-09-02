# # app/database.py

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql+psycopg2://postgres.cajmnyodyzccgsxcibcc:C2vcdM79EZbT@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

# # Use synchronous SQLAlchemy engine
# engine = create_engine(DATABASE_URL, echo=True)

# # Use synchronous sessionmaker
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# # Dependency to get a session for each request
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()





from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Use synchronous SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Use synchronous sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get a session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
