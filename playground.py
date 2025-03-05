from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
from datetime import datetime

# PostgreSQL Database Configuration
POSTGRES_IP = "20.50.143.29"
POSTGRES_USER = "yad-tamar"
POSTGRES_PASSWORD = "kingshoval!123"
POSTGRES_DATABASE = "yad-tamar"

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_IP}/{POSTGRES_DATABASE}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model for requests
class Request(Base):
    __tablename__ = "requests"

    id = Column(String, primary_key=True, index=True)
    family_id = Column(String, nullable=False)
    request_type = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    city = Column(Integer, nullable=False)
    status = Column(Integer, default=1)
    is_urgent = Column(Boolean, default=False)
    assigned_volunteer_id = Column(String, nullable=True)
    expected_completion = Column(DateTime, nullable=True)
    preferred_datetime = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Pydantic Model for a new request data
class RequestCreate(BaseModel):
    id: str
    family_id: str
    request_type: int
    description: Optional[str] = None
    city: int
    status: Optional[int] = 1
    is_urgent: Optional[bool] = False
    assigned_volunteer_id: Optional[str] = None
    expected_completion: Optional[datetime] = None
    preferred_datetime: Optional[datetime] = None

# Pydantic Model for response that includes request data
class RequestResponse(BaseModel):
    id: str
    family_id: str
    request_type: int
    description: Optional[str]
    city: int
    status: int
    is_urgent: bool
    assigned_volunteer_id: Optional[str]
    expected_completion: Optional[datetime]
    preferred_datetime: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

# Read All Requests or by ID
@app.get("/request", response_model=list[RequestResponse])
def read_all_requests(id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if id:
        results = db.query(Request).filter(Request.id == id).all()
    else:
        results = db.query(Request).all()
    return results

# Create a New Request
@app.post("/request", response_model=dict)
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    new_request = Request(**request.model_dump())
    db.add(new_request)
    try:
        db.commit()
        db.refresh(new_request)
        return {"id": new_request.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    