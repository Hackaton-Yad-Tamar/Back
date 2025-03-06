import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.request import RequestType
from app.models.user import City, Family, License, Volunteer
from app.models.user import User
from app.schemas.user import DTO_for_family_signup, DTO_for_vulenteer_signup, UserDTO_for_signin

users_router = APIRouter()


@users_router.post("/signin")
def signIn(
        userDetails: UserDTO_for_signin,
        db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=userDetails.email, password_hash=userDetails.password).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User '{userDetails.email}' not found")
    return user
    
    


@users_router.post("/signup/vulenteer")
def signUpVulenteer(
        userDetails: DTO_for_vulenteer_signup,
        db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == userDetails.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_id = str(uuid.uuid4())[:9]
    db_user = User(id=user_id, first_name=userDetails.first_name, last_name=userDetails.last_name,
                   phone_number=userDetails.phone_number, address=userDetails.address,
                   profile_picture=userDetails.profile_picture, email=userDetails.email, user_type=2,
                   city=userDetails.city)
    vol_user = Volunteer(user_id=user_id, preferred_city=userDetails.preferred_city,
                         preferred_skill=userDetails.preferred_skill, license_level=userDetails.license_level)
    db.add(db_user)
    db.add(vol_user)
    db.commit()
    db.refresh(db_user)

    return "user created successfully"


@users_router.post("/signup/family")
def signUpVulenteer(
        userDetails: DTO_for_family_signup,
        db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == userDetails.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_id = str(uuid.uuid4())[:9]
    db_user = User(id=user_id, first_name=userDetails.first_name, last_name=userDetails.last_name,
                   phone_number=userDetails.phone_number, address=userDetails.address,
                   profile_picture=userDetails.profile_picture, email=userDetails.email, user_type=1,
                   city=userDetails.city)
    fam_user = Family(user_id=user_id, building_type=userDetails.building_type, floor_number=userDetails.floor_number,
                      has_parking=userDetails.has_parking, has_elevator=userDetails.has_elevator,
                      is_private_house=userDetails.is_private_house)
    db.add(db_user)
    db.add(fam_user)
    db.commit()
    db.refresh(db_user)

    return "user created successfully"


@users_router.get("/cities")
def getCities(
        db: Session = Depends(get_db)):
    cities = db.query(City).all()
    return cities


@users_router.get("/licenses")
def getLicenses(
        db: Session = Depends(get_db)):
    licenses = db.query(License).all()
    return licenses


@users_router.get("/skills")
def getLicenses(
        db: Session = Depends(get_db)):
    skills = db.query(RequestType).all()
    return skills

@users_router.post("/update-password")
def update_user_first_name(    
    userDetails: UserDTO_for_signin,
    db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == userDetails.email).first()

    if user:
        user.password_hash = userDetails.password
        if user.first_sign_in:
            user.first_sign_in = False
        db.commit()
        db.refresh(user)

        return user
    else:
        return None
