from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.adminview_db import city_count, status_count, type_count, request_completion_time
from app.core.database import get_db

dashboard_router = APIRouter()


@dashboard_router.get("/city-count")
def get_city_count(start_date: str, end_date: str, status: str = None, request_type: str = None,
                   db: Session = Depends(get_db)):
    return city_count(db, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date), status, request_type)


@dashboard_router.get("/status-count")
def get_status_count(start_date: str, end_date: str, city: str = None, request_type: str = None,
                     db: Session = Depends(get_db)):
    return status_count(db, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date), city, request_type)


@dashboard_router.get("/type-count")
def get_type_count(start_date: str, end_date: str, city: str = None,
                   db: Session = Depends(get_db)):
    return type_count(db, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date), city)


@dashboard_router.get("/request-completion-time")
def get_request_completion_time(start_date: str, end_date: str, city: str = None, request_type: str = None,
                                db: Session = Depends(get_db)):
    return request_completion_time(db, datetime.fromisoformat(start_date), datetime.fromisoformat(end_date), city,
                                   request_type)
