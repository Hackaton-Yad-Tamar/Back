#define the table request schema using sqlalchemy

from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, TIMESTAMP, CHAR
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class RequestStatus(Base):
    __tablename__ = 'request_status'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String(50), unique=True, nullable=False)
    
    requests = relationship("Request", back_populates="status_relation")
    request_processes = relationship("RequestProcess", back_populates="status_relation")

class Request(Base):
    __tablename__ = 'requests'
    
    id = Column(CHAR(9), primary_key=True)
    family_id = Column(CHAR(9), ForeignKey('families.user_id'), nullable=False)
    request_type = Column(Integer, ForeignKey('request_types.id'), nullable=False)
    description = Column(Text, nullable=True)
    city = Column(Integer, ForeignKey('cities.id'), nullable=False)
    status = Column(Integer, ForeignKey('request_status.id'), default=1)
    is_urgent = Column(Boolean, default=False)
    assigned_volunteer_id = Column(CHAR(9), ForeignKey('volunteers.user_id'), nullable=True)
    expected_completion = Column(TIMESTAMP, nullable=True)
    preferred_datetime = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default='NOW()')
    
    family_relation = relationship("Family", back_populates="requests")
    request_type_relation = relationship("RequestType", back_populates="requests")
    city_relation = relationship("City", back_populates="requests")
    status_relation = relationship("RequestStatus", back_populates="requests")
    assigned_volunteer_relation = relationship("Volunteer", back_populates="requests")
    request_processes = relationship("RequestProcess", back_populates="request_relation")

class RequestProcess(Base):
    __tablename__ = 'request_process'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(CHAR(9), ForeignKey('requests.id'), nullable=False)
    volunteer_id = Column(CHAR(9), ForeignKey('volunteers.user_id'), nullable=False)
    status = Column(Integer, ForeignKey('request_status.id'), default=1)
    volunteer_approval = Column(Boolean, default=False)
    estimated_arrival = Column(TIMESTAMP, nullable=True)
    completed_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default='NOW()')
    
    request_relation = relationship("Request", back_populates="request_processes")
    volunteer_relation = relationship("Volunteer", back_populates="request_processes")
    status_relation = relationship("RequestStatus", back_populates="request_processes")
