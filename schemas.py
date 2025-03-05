from pydantic import BaseModel, Field, field_validator, EmailStr
import re

HASH_REGEX = re.compile(r"^[a-fA-F0-9]{32,64}$")


class UserDTO_for_managers(BaseModel):
    #data to send on each vulenteer
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    phone_number: str = Field(..., min_length=2, max_length=20)
    address: str
    profile_pic: str
    is_approved: bool
    pref_city: int
    license_type: int
    skill_type: int


class UserDTO_for_vul_signup(BaseModel):
    #data to get from each user when vulenteer when trying to sign up
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    phone_number: str = Field(..., min_length=2, max_length=20)
    address: str
    profile_pic: str
    email: EmailStr
    pref_city: int
    license_type: int
    skill_type: int


class UserDTO_for_signin(BaseModel):
    #data to get from users when signing in
    email: EmailStr
    password: str = Field(..., regex=HASH_REGEX.pattern)
    first_sign_in: bool