#define APIRouter() instance for requests
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.models.request import Request, RequestStatus, RequestType
from app.schemas.request import RequestModel
from app.core.database import get_db
from sqlalchemy.orm import Session, joinedload
from app.models.user import *
from sqlalchemy.sql import case, func

request_router = APIRouter()

@request_router.get("/ai_button")
def get_requests(user_id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    """
    Returns a list of requests with volunteer details and a calculated match percentage.
    
    The match percentage is computed as:
      - 100 if both the request's city and request_type match the volunteer's preferred city and skill.
      - 50 if either the city or the skill matches.
      - 0 otherwise.
    
    Filters:
      - Only include users whose related user_type has an id equal to 2.
      - Only include users that have been approved (approved_by_id is not null).
      - Only include requests with a status of 1.
    """
    # Define the match_percentage expression.
    match_percentage_expr = case(
        (
            (Request.city == Volunteer.preferred_city) &
            (Request.request_type == Volunteer.preferred_skill),
            100
        ),
        (
            (Request.city == Volunteer.preferred_city) |
            (Request.request_type == Volunteer.preferred_skill),
            50
        ),
        else_=0
    ).label("match_percentage")

    # Build the query with joins and filters.
    query = (
        db.query(
            Request.id.label("request_id"),
            Request.request_type,
            Request.description,
            Request.city,
            Request.status,
            Request.is_urgent,
            # Concatenate first_name and last_name from the User model.
            func.concat(User.first_name, " ", User.last_name).label("vol_name"),
            match_percentage_expr
        )
        .join(Family, Family.user_id == Request.family_id)
        .join(User, User.id == Family.user_id)
        .join(Volunteer, Volunteer.user_id == User.id)
        .filter(
            # Filter using the relationship’s criteria.
            User.user_type.has(id=2),
            User.approved_by_id.isnot(None),
            User.id == user_id
        )
    )

    results = query.all()
    # Convert each result row to a dictionary.
    return [dict(row._mapping) for row in results]

@request_router.get("/request")
def read_all_requests(id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if id:
        results = db.query(Request).options(joinedload(Request.request_type_relation).filter(Request.id == id)).all()
    else:
        results = db.query(Request).options(joinedload(Request.request_type_relation)).all()
    return results

# Create a New Request
@request_router.post("/request", response_model=dict)
def create_request(request, db: Session = Depends(get_db)):
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