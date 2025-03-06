from dateutil import parser

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.adminview_db import city_count, status_count, type_count, request_completion_time, filtered_data
from app.core.database import get_db

dashboard_router = APIRouter()


@dashboard_router.get("/city-count")
def get_city_count(start_date: str, end_date: str, status: str = None, request_type: str = None, city: str = None,
                   db: Session = Depends(get_db)):
    return city_count(db, parser.parse(start_date), parser.parse(end_date), status, request_type, city)


@dashboard_router.get("/status-count")
def get_status_count(start_date: str, end_date: str, status: str = None, request_type: str = None, city: str = None,
                     db: Session = Depends(get_db)):
    return status_count(db, parser.parse(start_date), parser.parse(end_date), status, request_type, city)


@dashboard_router.get("/type-count")
def get_type_count(start_date: str, end_date: str, status: str = None, request_type: str = None, city: str = None,
                   db: Session = Depends(get_db)):
    return type_count(db, parser.parse(start_date), parser.parse(end_date), status, request_type, city)


@dashboard_router.get("/request-completion-time")
def get_request_completion_time(start_date: str, end_date: str, city: str = None, request_type: str = None,
                                db: Session = Depends(get_db)):
    return request_completion_time(db, parser.parse(start_date), parser.parse(end_date), city,
                                   request_type)
    

@dashboard_router.get("/filtered-table")
def get_filtered_data(start_date: str, end_date: str, status: str = None, request_type: str = None, city: str = None,
                   db: Session = Depends(get_db)):
    return filtered_data(db, parser.parse(start_date), parser.parse(end_date), status, request_type, city)
