#define the table user schema using sqlalchemy

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, TIMESTAMP, CHAR
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class UserType(Base):
    __tablename__ = 'user_types'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(20), unique=True, nullable=False)
    
    users = relationship("User", back_populates="user_type_relation")

class City(Base):
    __tablename__ = 'cities'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(50), unique=True, nullable=False)
    
    users = relationship("User", back_populates="city_relation")
    volunteers = relationship("Volunteer", back_populates="preferred_city_relation")
    requests = relationship("Request", back_populates="city_relation")

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
    is_approved = Column(Boolean, default=False)
    approved_by = Column(CHAR(9), ForeignKey('users.id'), nullable=True)
    approved_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default='NOW()')
    
    city_relation = relationship("City", back_populates="users")
    user_type_relation = relationship("UserType", back_populates="users")
    authentication = relationship("Authentication", uselist=False, back_populates="user")
    families = relationship("Family", uselist=False, back_populates="user")
    volunteers = relationship("Volunteer", uselist=False, back_populates="user")

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

class RequestType(Base):
    __tablename__ = 'request_types'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(50), unique=True, nullable=False)
    
    requests = relationship("Request", back_populates="request_type_relation")
    volunteers = relationship("Volunteer", back_populates="preferred_skill_relation")

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

