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
    firstName: str
    lastName: str
    phoneNumber: Optional[str]
    address: Optional[str]
    profilePicture: Optional[str]
    city: str
    userType: str
    status: str
    approvedAt: Optional[datetime]
    createdAt: datetime

    @staticmethod
    def from_alchemy(user: User):
        return UserResponse(
            id=user.id,
            firstName=user.first_name,
            lastName=user.last_name,
            phoneNumber=user.phone_number,
            address=user.address,
            profilePicture=user.profile_picture,
            city=user.city_relation.city_name,
            userType=user.user_type_relation.type_name,
            status=user.user_status_relation.name if user.user_status_relation is not None else 'PENDING',
            approvedAt=user.approved_at,
            createdAt=user.created_at
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
