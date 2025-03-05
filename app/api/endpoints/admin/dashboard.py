from dateutil import parser

import requests

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.adminview_db import city_count, status_count, type_count, request_completion_time, custom_query
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

@dashboard_router.get("/custom-query")
def get_custom_query(query: str, db: Session = Depends(get_db)):
    url = "http://localhost:5000/translate"
    data = {"question": query}
    response = requests.post(url, json=data)
    query = response.json()["sql_query"]
    if "UPDATE" in query or "DELETE" in query or "INSERT" in query:
        raise ValueError("This query is not allowed.")
    # turn the column names included in the SELECT statement into a list
    columns = response.json()["sql_query"].split("SELECT")[1].split("FROM")[0].strip().split(",")
    columns = [col.strip() for col in columns]
    fetched_data = custom_query(db, response.json()["sql_query"])
    print(fetched_data)
    dictio = [dict(zip(columns, row)) for row in fetched_data]
    return dictio
