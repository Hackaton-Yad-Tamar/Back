from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.models.request import RequestStatus
request_status_router = APIRouter()


@request_status_router.get("/request_status")
def request_status( db: Session = Depends(get_db)):
    results = db.query(RequestStatus).all()
    return results