#define APIRouter() instance for requests
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.models.request import Request, RequestType, RequestStatus
from app.models.user import City
from app.schemas.request import RequestModel
from app.core.database import get_db
from sqlalchemy.orm import Session, joinedload, contains_eager
from app.models.user import *
from sqlalchemy.sql import case, func
import re

request_router = APIRouter()

@request_router.get("/ai_button")
def ai_requests(user_id: Optional[str] = Query(None), db: Session = Depends(get_db)):
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

@request_router.get("/request") #add status object, 
def get_all_requests(id: Optional[str] = Query(None), db: Session = Depends(get_db)):
    if id:
        results = db.query(Request).options(joinedload(Request.request_type_relation).filter(Request.id == id)).all()
    else:
        results = (
    db.query(Request, City, RequestStatus, RequestType, User)
      .filter(City.id == Request.city)
      .filter(RequestStatus.id == Request.status)
      .filter(RequestType.id == Request.request_type)
      .filter(User.id == Request.family_id)
      .all()
    )

    results_parsed = [
        {
            "request": vars(request),
            "city": vars(city),
            "status": vars(status),
            "request_type": vars(req_type),
            "user": vars(user)
        }
        for request, city, status, req_type, user in results
    ]  

    return results_parsed

def to_camel_case(snake_str: str) -> str:
    """Converts snake_case to camelCase."""
    parts = snake_str.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

def convert_keys_to_camel_case(data):
    """Recursively converts dictionary keys from snake_case to camelCase."""
    if isinstance(data, list):
        return [convert_keys_to_camel_case(item) for item in data]
    elif isinstance(data, dict):
        return {to_camel_case(key): convert_keys_to_camel_case(value) for key, value in data.items()}
    return data  # If it's neither list nor dict, return as is

@request_router.get("/request/{family_id}")
def get_family_requests(family_id: str, db: Session = Depends(get_db)):
    results = (
        db.query(Request)
        # .options(joinedload(Request.request_type_relation))
        .filter(Request.family_id == family_id)  # Filter by user_id
        .all()
    )

    # Convert to dict format before applying camelCase conversion
    results_dict = [row.__dict__ for row in results]

    # Remove SQLAlchemy internal metadata
    for row in results_dict:
        row.pop("_sa_instance_state", None)

    # Convert snake_case to camelCase
    camel_case_results = convert_keys_to_camel_case(results_dict)

    return camel_case_results

# Create a New Request
@request_router.post("/request", response_model=dict)
def create_request(request: RequestModel, db: Session = Depends(get_db)):
    data = request.model_dump()
    data["request_type"] = data["request_type"].value  # Convert enum to string
    new_request = Request(**data)
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

# @request_router.get("/request/statuses", response_model=List[RequestStatus])
# def get_all_statuses(db: Session = Depends(get_db)):
#     statuses = db.query(RequestStatus).all()
#     if statuses is None:
#         raise HTTPException(status_code=404, detail="No statuses found")
#     return statuses
#
# @request_router.get("/request/request_types", response_model=List[RequestType])
# def get_all_request_types(db: Session = Depends(get_db)):
#     types = db.query(RequestType).all()
#     if not types:
#         raise HTTPException(status_code=404, detail="No request types found")
#     return types