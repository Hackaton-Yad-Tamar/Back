from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import City, User, Volunteer
from app.schemas.user import DTO_for_vulenteer_signup, UserDTO_for_signin
import uuid

users_router = APIRouter()

@users_router.post("/signin")
def signIn(
    userDetails: UserDTO_for_signin,
    db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=userDetails.email, password_hash=userDetails.password).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User '{userDetails.email}' not found")
    return {"isFirstTime": False}

@users_router.post("/signup/vulenteer")
def signUp(
    userDetails: DTO_for_vulenteer_signup,
    db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == userDetails.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_id = str(uuid.uuid4())[:9]
    db_user = User(id = user_id, first_name=userDetails.first_name,last_name=userDetails.last_name, phone_number=userDetails.phone_number,address = userDetails.address,profile_picture = userDetails.profile_pic,email = userDetails.email,user_type = 2, city = userDetails.pref_city )
    vol_user = Volunteer(user_id = user_id, preferred_city = userDetails.pref_city, preferred_skill = userDetails.skill_type, license_level = userDetails.license_type )
    db.add(db_user)
    db.add(vol_user)
    db.commit()
    db.refresh(db_user)

    
    return {"isFirstTime": False}
@users_router.get("/cities")
def signUp(
    db: Session = Depends(get_db)):
    cities = db.query(City).all()
    return cities