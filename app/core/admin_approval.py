from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..models.user import User

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

import random
import string
import hashlib

import requests
import json

def send_email(user_email, subject, message):
    # API URL
    url = "https://virtserver.swaggerhub.com/liorshwartz/alert_service/1.0.0/api/send-email"

    # Email data
    email_data = {
        "to_email": user_email,
        "subject": subject,
        "body": message
    }

    # Headers to define content type
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Make the POST request
    response = requests.post(url, json=email_data, headers=headers)

    # Check if the email was sent successfully
    if response.status_code == 200:
        print("Email sent successfully!")
        print(response.json())  # Print the response from the server
    else:
        print("Failed to send email.")
        print(f"Error: {response.status_code}")
        print(response.json())  # Print error details


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    address: Optional[str]
    profile_picture: Optional[str]
    city_id: int
    user_type_id: int
    status_id: int
    approved_at: Optional[datetime]
    created_at: datetime




def unapproved_users(session: Session):
    try:
        print(session.query(User).filter(User.status_id == 2))
        users = session.query(User).filter(User.status_id == 2).all() #TODO: replace status with requested
        user_responses = [UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            address=user.address,
            profile_picture=user.profile_picture,
            city_id=user.city_id,
            user_type_id=user.user_type_id,
            status_id=user.status_id,
            approved_at=user.approved_at,
            created_at=user.created_at
        ) for user in users]
        return user_responses
    finally:
        session.close()




def do_approve_user(session: Session, user_id: string):
    '''
    Approve or reject a user based on the user_id
    if approved:
    - generate new password
    - send email with password
    - update user status to approved
    - update manager user that approved the user
    if rejected:
    - update user status to rejected
    - send email to user that he/she got rejected (optional)
    
    '''
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.status = 1 # TODO: replace status with approved
            # generate new password
            characters = string.ascii_letters + string.digits  # Letters (uppercase + lowercase) and digits
            password = ''.join(random.choice(characters) for _ in range(12))  # Randomly choose characters
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            user.hashed_password = hashed_password #TODO: check hashed_password field
            send_email(user.email, "successfully connection to Yad-Tamar", password)
            
            session.commit()
            session.refresh(user)
        return None
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def do_reject_user(session: Session, user_id: string):
    try:
        print("try1")
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.status_id = 0 # TODO: replace status with rejected
            session.commit()
            session.refresh(user)
            return None
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
