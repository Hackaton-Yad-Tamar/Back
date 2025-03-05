#define the table request schema using sqlalchemy#define APIRouter() instance for requests

from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
from datetime import datetime


Base = declarative_base()

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