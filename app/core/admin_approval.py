import hashlib
import random
import string
from typing import List

import requests
from sqlalchemy.orm import Session

from ..models.user import User, UserStatus


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


def unapproved_users(session: Session) -> List[User]:
    users = User.get_users(session,
                           filters=[User.user_status == UserStatus.PENDING])  # TODO: replace status with requested

    return users


def do_approve_user(session: Session, user_id: str):
    """
    Approve or reject a user based on the user_id
    if approved:
    - generate new password
    - send email with password
    - update user status to approved
    - update manager user that approved the user
    if rejected:
    - update user status to rejected
    - send email to user that he/she got rejected (optional)

    """
    user = User.get_user(session, user_id)
    if user:
        user.user_status = UserStatus.APPROVED
        # generate new password
        characters = string.ascii_letters + string.digits  # Letters (uppercase + lowercase) and digits
        password = ''.join(random.choice(characters) for _ in range(12))  # Randomly choose characters
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user.hashed_password = hashed_password  # TODO: check hashed_password field
        send_email(user.email, "Successful connection to Yad-Tamar: ", password)

        session.commit()
        session.refresh(user)
        return user
    return None


def do_reject_user(session: Session, user_id: str):
    user = User.get_user(session, user_id)
    if user:
        user.status_id = UserStatus.REJECTED
        session.commit()
        session.refresh(user)
        return user
    return None
