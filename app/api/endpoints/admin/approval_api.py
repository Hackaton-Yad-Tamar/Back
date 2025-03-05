from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.admin_approval import unapproved_users, do_approve_user, do_reject_user
from app.core.database import get_db
from app.models.user import User

approve_users = APIRouter()


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    address: Optional[str]
    profile_picture: Optional[str]
    city_id: int
    user_type_id: int
    status_id: Optional[int]
    approved_at: Optional[datetime]
    created_at: datetime

    @staticmethod
    def from_alchemy(user: User):
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            address=user.address,
            profile_picture=user.profile_picture,
            city_id=user.city,
            user_type_id=user.user_type,
            status_id=user.user_status,
            approved_at=user.approved_at,
            created_at=user.created_at
        )


@approve_users.get("/all_users")
def get_all_users(db: Session = Depends(get_db)):
    users = User.get_users(db)
    return [UserResponse.from_alchemy(user) for user in users]


@approve_users.get("/unapproved")
def get_unapproved_users(db: Session = Depends(get_db)):
    users = unapproved_users(db)
    return [UserResponse.from_alchemy(user) for user in users]


@approve_users.post("/{user_id}/approve", response_model=UserResponse)
def approve_user(user_id: str, db: Session = Depends(get_db)):
    user = do_approve_user(db, user_id)
    if user:
        return UserResponse.from_alchemy(user)
    raise HTTPException(status_code=404, detail="User not found")


@approve_users.post("/{user_id}/reject", response_model=UserResponse)
def reject_user(user_id: str, db: Session = Depends(get_db)):
    user = do_reject_user(db, user_id)
    if user:
        return UserResponse.from_alchemy(user)
    raise HTTPException(status_code=404, detail="User not found")
