from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import (
    create_engine, Column, String, Integer, Boolean, DateTime, func, ForeignKey, Enum, Text
)
from sqlalchemy.orm import relationship, sessionmaker, Session, declarative_base
from typing import Optional
from datetime import datetime
import uuid
import enum

# PostgreSQL Database Configuration
POSTGRES_IP = "20.50.143.29"
POSTGRES_USER = "yad-tamar"
POSTGRES_PASSWORD = "kingshoval!123"
POSTGRES_DATABASE = "yad-tamar"

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_IP}/{POSTGRES_DATABASE}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enum for request types to restrict allowed values
class RequestType(enum.Enum):
    FOOD = "food"
    MEDICAL = "medical"
    TRANSPORT = "transport"
    OTHER = "other"

# Cities table to enforce valid city references
class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    requests = relationship("Request", back_populates="city")

# Families table to ensure valid family references
class Family(Base):
    __tablename__ = 'families'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    requests = relationship("Request", back_populates="family")

# Volunteers table for tracking assigned volunteers
class Volunteer(Base):
    __tablename__ = 'volunteers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    assigned_requests = relationship("Request", back_populates="assigned_volunteer")

# Request statuses to enforce valid statuses
class RequestStatus(Base):
    __tablename__ = 'request_statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(50), unique=True, nullable=False)

    requests = relationship("Request", back_populates="status")

# Requests table with foreign key constraints
class Request(Base):
    __tablename__ = "requests"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))  # UUID for unique request IDs
    family_id = Column(Integer, ForeignKey('families.id'), nullable=False)
    request_type = Column(Enum(RequestType), nullable=False)  # Enum-enforced request type
    description = Column(Text, nullable=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    status_id = Column(Integer, ForeignKey('request_statuses.id'), default=1, nullable=False)
    is_urgent = Column(Boolean, default=False, nullable=False)
    assigned_volunteer_id = Column(Integer, ForeignKey('volunteers.id'), nullable=True)
    expected_completion = Column(DateTime, nullable=True)
    preferred_datetime = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Define relationships
    family = relationship("Family", back_populates="requests")
    city = relationship("City", back_populates="requests")
    status = relationship("RequestStatus", back_populates="requests")
    assigned_volunteer = relationship("Volunteer", back_populates="assigned_requests")

# Create all tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Pydantic Model for creating a new request
class RequestCreate(BaseModel):
    id: str
    family_id: int
    request_type: RequestType
    description: Optional[str] = None
    city_id: int
    status_id: Optional[int] = 1
    is_urgent: Optional[bool] = False
    assigned_volunteer_id: Optional[int] = None
    expected_completion: Optional[datetime] = None
    preferred_datetime: Optional[datetime] = None

# Pydantic Model for returning request details
class RequestResponse(BaseModel):
    id: str
    family_id: int
    request_type: RequestType
    description: Optional[str]
    city_id: int
    status_id: int
    is_urgent: bool
    assigned_volunteer_id: Optional[int]
    expected_completion: Optional[datetime]
    preferred_datetime: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

# Read All Requests or Filter by ID
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

# Update an Existing Request
@app.put("/request/{request_id}", response_model=RequestResponse)
def update_request(request_id: str, updated_request: RequestCreate, db: Session = Depends(get_db)):
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    for key, value in updated_request.dict(exclude_unset=True).items():
        setattr(db_request, key, value)

    db.commit()
    db.refresh(db_request)
    return db_request

# Delete a Request
@app.delete("/request/{request_id}", response_model=dict)
def delete_request(request_id: str, db: Session = Depends(get_db)):
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    db.delete(db_request)
    db.commit()
    return {"message": "Request deleted successfully"}
