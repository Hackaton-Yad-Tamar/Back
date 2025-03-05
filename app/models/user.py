from typing import List, Optional, Callable

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, CHAR, SQLColumnExpression, TIMESTAMP
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import relationship, Mapped, Session

from app.models.request import Base


class UserType(Base):
    __tablename__ = 'user_types'

    id: str = Column(Integer, primary_key=True, autoincrement=True)  # Primary key for UserTypes
    name: str = Column(String(20), unique=True, nullable=False)  # Type name (e.g., 'family', 'volunteer', 'admin')

    users: Mapped[List['User']] = relationship("User",
                                               back_populates="user_type_relation")  # Relationship to User table


class UserStatus(Base):
    __tablename__ = 'user_status'

    PENDING = 0
    APPROVED = 1
    REJECTED = 2

    id: str = Column(Integer, primary_key=True)  # Primary key for UserStatus
    name: str = Column(String(50), nullable=False)  # Status name (e.g., 'pending', 'approved', 'rejected')

    users: Mapped[List['User']] = relationship("User", back_populates="user_status_relation")  # Relationship to User table


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Primary key for Cities
    city_name = Column(String(50), unique=True,
                       nullable=False)  # City name (e.g., 'Istanbul', 'Ankara', 'Izmir')

    users = relationship("User", back_populates="city_relation")  # Relationship to User table
    volunteers = relationship("Volunteer", back_populates="preferred_city_relation")  # Relationship to Volunteer table
    requests = relationship("Request", back_populates="city_relation")  # Relationship to Request table


class User(Base):
    __tablename__ = 'users'
    
    id = Column(CHAR(9), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone_number = Column(String(20))
    address = Column(Text)
    city = Column(Integer, ForeignKey('cities.id'), nullable=False)
    user_type = Column(Integer, ForeignKey('user_types.id'), nullable=False)
    profile_picture = Column(Text, nullable=True)
    user_status = Column(Integer, ForeignKey('user_status.id'), nullable=True)
    approved_by = Column(CHAR(9), ForeignKey('users.id'), nullable=True)
    approved_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default='NOW()')
    first_sign_in = Column(Boolean, default=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    
    city_relation = relationship("City", back_populates="users")
    user_type_relation = relationship("UserType", back_populates="users")
    user_status_relation = relationship("UserStatus", back_populates="users")
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
        try:
            # Fetch the user by ID
            user = User.get_user(session, user_id)
            # If user does not exist, return None
            if not user:
                return None

            # Update user attributes
            for key, value in kwargs.items():
                if hasattr(user, key):  # Ensure the attribute exists
                    setattr(user, key, value)

            # Commit changes
            session.commit()
            session.refresh(user)  # Refresh to get updated data from the database

            return user

        except SQLAlchemyError as e:
            session.rollback()  # Rollback on error
            print(f"Error updating user: {e}")
            return None

    @classmethod
    def get_users(cls, session: Session, order_by: Optional[List[Callable]] = None,
                  filters: Optional[List[SQLColumnExpression]] = None) \
            -> List['User']:
        """
        Retrieve a list of users from the database based on the provided filters.
        :param session: SQLAlchemy database session
        :param order_by: List of functions to order the results. Look at asc() and desc() from sqlalchemy
        :param filters: Filters to apply to the query
        :return: List of users matching the filters
        """

        query = session.query(cls)

        # Apply filters if provided
        if filters is not None:
            query = query.filter(*filters)

        # Apply ordering if provided
        if order_by is not None:
            query = query.order_by(*order_by)

        return query.all()

    @classmethod
    def get_user(cls, session: Session, user_id: str) -> Optional['User']:
        """
        Retrieve a user from the database based on the provided identifier.
        :param session: SQLAlchemy database session
        :param user_id: Identifier for the user to retrieve
        :return: The user if found, None otherwise
        """
        return session.query(User).filter_by(id=user_id).first()


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
