#define APIRouter() instance for requests
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from sqlalchemy import update

from app.models.request import Request, RequestStatus
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


@request_router.patch("/request/update_status/{request_id}/{status_id}", response_model=RequestModel)
def update_status(
        request_id: str,
        status_id: int,
        db: Session = Depends(get_db)
):
    # Retrieve the Request record
    db_request = db.query(Request).filter(Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    # Determine the toggled status:
    # If provided status_id is 1, then new_status becomes 2; if it's 2, then new_status becomes 1.
    if status_id == 1:
        new_status = 2
    elif status_id == 2:
        new_status = 1
    else:
        raise HTTPException(status_code=400, detail="Invalid status_id provided; must be 1 or 2.")

    # Validate that the new status exists in RequestStatus table
    status_record = db.query(RequestStatus).filter(RequestStatus.id == new_status).first()
    if not status_record:
        raise HTTPException(status_code=404, detail="Status not found")

    # Update the Request record's status_integer field to the new status
    db_request.status_integer = new_status
    db.commit()
    db.refresh(db_request)

    # Optionally, if you want to include the status name in your response,
    # ensure your RequestModel includes a field for it and populate it accordingly.
    return db_request
