from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db

users_router = APIRouter()

#דוגמה ליצירת ראוט וראוטר
@users_router.get("/")
def read_user(db: Session = Depends(get_db)):
    # db_user = crud.get_user(db, user_id=user_id)
    # if db_user is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return "אני רק דוגמהההה"