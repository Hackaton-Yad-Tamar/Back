# Database connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DB_CONFIG

host = DB_CONFIG['host']
port = DB_CONFIG['port']
db_name = DB_CONFIG['dbname']
user = DB_CONFIG['user']
password = DB_CONFIG['password']

DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()