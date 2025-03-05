# Pydantic schemas for user
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import re

HASH_REGEX = re.compile(r"^[a-fA-F0-9]{32,64}$")


class DTO_users_for_post_signup(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)


class DTO_users_for_signup(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    phone_number: str = Field(..., min_length=2, max_length=20)
    address: str
    city: int
    profile_picture: Optional[str] = None
    email: EmailStr


class DTO_for_vulenteer_signup(DTO_users_for_signup):
    #data to get from each user when vulenteer when trying to sign up
    preferred_city: int
    license_level: int
    preferred_skill: int


class DTO_for_family_signup(DTO_users_for_signup):
    building_type: str = Field(..., min_length=2, max_length=50)
    floor_number: Optional[int]
    has_parking: bool
    has_elevator: Optional[bool]
    is_private_house: bool

class UserDTO_for_signin(BaseModel):
    #data to get from users when signing in
    email: EmailStr
    password: str = Field(..., pattern=HASH_REGEX.pattern)
