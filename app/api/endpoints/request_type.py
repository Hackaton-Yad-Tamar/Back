from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from typing import Optional
from app.models.request import RequestType
request_type_router = APIRouter()


@request_type_router.get("/request_type")
def read_all_requests( db: Session = Depends(get_db)):
    results = db.query(RequestType).all()
    return results