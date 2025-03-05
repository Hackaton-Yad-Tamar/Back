from typing import List
from fastapi import FastAPI, HTTPException
from app.core.admin_approval import UserResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.core.admin_approval import unapproved_users, do_approve_user, do_reject_user


approve_users = APIRouter()

@approve_users.get("/unapproved", response_model=List[UserResponse])
def get_unapproved_users(db: Session = Depends(get_db)):
    users = unapproved_users(db)
    return users

@approve_users.post("/{user_id}/approve", response_model=UserResponse)
def approve_user(user_id: str, db: Session = Depends(get_db)):
    user = do_approve_user(db, user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")
    
@approve_users.post("/{user_id}/reject", response_model=UserResponse)
def reject_user(user_id: str, db: Session = Depends(get_db)):
    user = do_reject_user(db, user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")
