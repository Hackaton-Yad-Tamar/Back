from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserDTO_for_signin

users_router = APIRouter()

@users_router.post("/signin")
def signIn(
    userDetails: UserDTO_for_signin,
    db: Session = Depends(get_db)):
    user = db.query(User).first()
    print(user.authentication)
    return "אני רק דוגמהההה"