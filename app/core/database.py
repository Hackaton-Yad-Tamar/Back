import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

load_dotenv()

DB_IP = os.getenv("DB_IP", "localhost")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres") 
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres") 

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_IP}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()