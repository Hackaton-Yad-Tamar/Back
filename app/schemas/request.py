# Pydantic schemas for request# Unified Pydantic model for creating and returning requests
# Enum for request types

from sqlalchemy import (
    create_engine, Column, String, Integer, Boolean, DateTime, func, ForeignKey, Enum, Text
)
import uuid
import enum
from pydantic import BaseModel, Field
from sqlalchemy.orm import relationship, sessionmaker, Session, declarative_base
from typing import Optional
from datetime import datetime
Base = declarative_base()

class RequestType(enum.Enum):
    FOOD = "food"
    MEDICAL = "medical"
    TRANSPORT = "transport"
    OTHER = "other"

# Cities table
class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    requests = relationship("Request", back_populates="city")

# Families table
class Family(Base):
    __tablename__ = 'families'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    requests = relationship("Request", back_populates="family")

# Volunteers table
class Volunteer(Base):
    __tablename__ = 'volunteers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    assigned_requests = relationship("Request", back_populates="assigned_volunteer")

# Request statuses table
class RequestStatus(Base):
    __tablename__ = 'request_statuses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(50), unique=True, nullable=False)
    requests = relationship("Request", back_populates="status")

class RequestModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique request ID")
    family_id: int
    request_type: RequestType
    description: Optional[str] = None
    city: int
    status: Optional[int] = 1
    is_urgent: Optional[bool] = False
    assigned_volunteer_id: Optional[int] = None
    expected_completion: Optional[datetime] = None
    preferred_datetime: Optional[datetime] = None
    created_at: Optional[datetime] = None  # Only set when returning a request

    class Config:
        from_attributes = True  # Enables automatic conversion from ORM models