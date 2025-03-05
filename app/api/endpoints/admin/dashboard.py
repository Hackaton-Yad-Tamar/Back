from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.adminview_db import city_count, status_count, type_count, time_taken, request_completion_time
from app.core.database import get_db

dashboard_router = APIRouter()


@dashboard_router.get("/city-count")
def get_city_count(start_date: str, end_date: str, status: str = None, request_type: str = None,
                   db: Session = Depends(get_db)):
    return city_count(db, start_date, end_date, status, request_type)


@dashboard_router.get("/status-count")
def get_status_count(start_date: str, end_date: str, city: str = None, request_type: str = None,
                     db: Session = Depends(get_db)):
    return status_count(db, start_date, end_date, city, request_type)


@dashboard_router.get("/type-count")
def get_type_count(start_date: str, end_date: str, city: str = None, request_type: str = None,
                   db: Session = Depends(get_db)):
    return type_count(db, start_date, end_date, city, request_type)


@dashboard_router.get("/time-taken")
def get_time_taken(start_date: str, end_date: str, city: str = None, request_type: str = None,
                   db: Session = Depends(get_db)):
    return time_taken(db, start_date, end_date, city, request_type)


@dashboard_router.get("/request-completion-time")
def get_request_completion_time(start_date: str, end_date: str, city: str = None, request_type: str = None,
                                db: Session = Depends(get_db)):
    return request_completion_time(db, start_date, end_date, city, request_type)
