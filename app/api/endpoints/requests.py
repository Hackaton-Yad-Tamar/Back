#define APIRouter() instance for requests
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.models.request import Request
from app.schemas.request import RequestModel
from app.core.database import get_db
from sqlalchemy.orm import Session, joinedload
from app.models.user import *

request_router = APIRouter()

@request_router.get("/request")
def read_all_requests(id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if id:
        results = db.query(Request).options(joinedload(Request.request_type_relation).filter(Request.id == id)).all()
    else:
        results = db.query(Request).options(joinedload(Request.request_type_relation)).all()
    return results

# Create a New Request
@request_router.post("/request", response_model=dict)
def create_request(request: RequestModel, db: Session = Depends(get_db)):
    new_request = Request(**request.model_dump())
    db.add(new_request)
    try:
        db.commit()
        db.refresh(new_request)
        return {"id": new_request.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@request_router.put("/request/{request_id}", response_model=RequestModel)
def update_request(request_id: str, updated_request: RequestModel, db: Session = Depends(get_db)):
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    for key, value in updated_request.dict(exclude_unset=True, exclude={"id", "created_at"}).items():
        setattr(db_request, key, value)

    db.commit()
    db.refresh(db_request)
    return db_request

# Delete a request
@request_router.delete("/request/{request_id}", response_model=dict)
def delete_request(request_id: str, db: Session = Depends(get_db)):
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    db.delete(db_request)
    db.commit()
    return {"message": "Request deleted successfully"}