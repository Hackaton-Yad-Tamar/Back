from datetime import datetime
from typing import List, Optional, Callable

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, TIMESTAMP, CHAR, DateTime
from sqlalchemy.orm import relationship, declarative_base, Mapped, Session

from app.models.request import Base


class UserType(Base):
    __tablename__ = 'user_types'

    id: str = Column(Integer, primary_key=True, autoincrement=True)  # Primary key for UserTypes
    name: str = Column(String(20), unique=True, nullable=False)  # Type name (e.g., 'family', 'volunteer', 'admin')

    users: Mapped[List['User']] = relationship("User",
                                               back_populates="user_type")  # Relationship to User table


class UserStatus(Base):
    __tablename__ = 'user_status'

    id: str = Column(Integer, primary_key=True)  # Primary key for UserStatus
    name: str = Column(String(50), nullable=False)  # Status name (e.g., 'pending', 'approved', 'rejected')

    users: Mapped[List['User']] = relationship("User", back_populates="status")  # Relationship to User table


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key for Cities
    city_name = Column(String(50), unique=True,
                       nullable=False)  # City name (e.g., 'Istanbul', 'Ankara', 'Izmir')

    users = relationship("User", back_populates="city")  # Relationship to User table
    volunteers = relationship("Volunteer", back_populates="preferred_city_relation")  # Relationship to Volunteer table
    requests = relationship("Request", back_populates="city_relation")  # Relationship to Request table


class User(Base):
    __tablename__ = 'users'  # Table name in the database

    # Define columns for the User table
    id: str = Column(String(9), primary_key=True)  # Unique identifier for the user

    first_name: str = Column(String(50), nullable=False)  # User's first name
    last_name: str = Column(String(50), nullable=False)  # User's last name

    phone_number: Optional[str] = Column(String(20), nullable=True)  # User's phone number (optional)
    address: Optional[str] = Column(Text, nullable=True)  # User's address (optional)
    profile_picture: Optional[str] = Column(Text, nullable=True)  # User's profile picture (optional)

    city: Mapped[City] = relationship("City", back_populates="users")  # User's city
    user_type: Mapped[UserType] = relationship("UserType", back_populates="users")  # User's type
    status: Mapped[UserStatus] = relationship("UserStatus", back_populates="users")  # User's status

    approved_at: Optional[datetime] = Column(DateTime,
                                             nullable=True)  # Timestamp for when the user was approved (optional)
    created_at: datetime = Column(DateTime, default=datetime.now)  # Timestamp for when the user record was created

    city_id: int = Column("city", Integer, ForeignKey("cities.id"),
                          nullable=False)  # Foreign key reference to Cities table
    user_type_id: int = Column("user_type", Integer, ForeignKey("user_types.id"),
                               nullable=False)  # Foreign key reference to User_Types table
    status_id: int = Column("status", Integer, ForeignKey("user_status.id"),
                            nullable=False)  # Foreign key reference to User_Status table
    approved_by_id: Optional[str] = Column(String(9), ForeignKey("users.id"),
                                           nullable=True)  # Foreign key reference to the approving user (optional)
    authentication = relationship("Authentication", uselist=False, back_populates="user")
    families = relationship("Family", uselist=False, back_populates="user")
    volunteers = relationship("Volunteer", uselist=False, back_populates="user")

    @classmethod
    def update_user(cls, session: Session, user_id: str, **kwargs: dict) -> Optional['User']:
        """
        Update an existing user in the database with the provided attributes.
        :param session: SQLAlchemy database session
        :param user_id: Identifier for the user to update
        :param kwargs: Attributes to update for the user
        :return: The updated user if found, None otherwise
        """
        raise NotImplementedError

    @classmethod
    def get_users(cls, session: Session, order_by: Optional[List[Callable]] = None, filters: dict = None) \
            -> List['User']:
        """
        Retrieve a list of users from the database based on the provided filters.
        :param session: SQLAlchemy database session
        :param order_by: List of functions to order the results. Look at asc() and desc() from sqlalchemy
        :param filters: Filters to apply to the query
        :return: List of users matching the filters
        """
        raise NotImplementedError

    @classmethod
    def get_user(cls, session: Session, user_id: str) -> Optional['User']:
        """
        Retrieve a user from the database based on the provided identifier.
        :param session: SQLAlchemy database session
        :param user_id: Identifier for the user to retrieve
        :return: The user if found, None otherwise
        """
        raise NotImplementedError


class Authentication(Base):
    __tablename__ = 'authentication'

    user_id = Column(CHAR(9), ForeignKey('users.id'), primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)

    user = relationship("User", back_populates="authentication")


class Family(Base):
    __tablename__ = 'families'

    user_id = Column(CHAR(9), ForeignKey('users.id'), primary_key=True)
    building_type = Column(String(50))
    floor_number = Column(Integer)
    has_parking = Column(Boolean, default=False)
    has_elevator = Column(Boolean, default=False)
    is_private_house = Column(Boolean, default=False)

    user = relationship("User", back_populates="families")
    requests = relationship("Request", back_populates="family_relation")


class License(Base):
    __tablename__ = 'licenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    license_name = Column(String(50), unique=True, nullable=False)

    volunteers = relationship("Volunteer", back_populates="license_level_relation")


class Volunteer(Base):
    __tablename__ = 'volunteers'

    user_id = Column(CHAR(9), ForeignKey('users.id'), primary_key=True)
    preferred_city = Column(Integer, ForeignKey('cities.id'), nullable=False)
    preferred_skill = Column(Integer, ForeignKey('request_types.id'), nullable=False)
    license_level = Column(Integer, ForeignKey('licenses.id'), nullable=False)

    user = relationship("User", back_populates="volunteers")
    preferred_city_relation = relationship("City", back_populates="volunteers")
    preferred_skill_relation = relationship("RequestType", back_populates="volunteers")
    license_level_relation = relationship("License", back_populates="volunteers")
    requests = relationship("Request", back_populates="assigned_volunteer_relation")
    request_processes = relationship("RequestProcess", back_populates="volunteer_relation")
