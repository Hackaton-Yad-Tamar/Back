from datetime import datetime
from typing import Optional

from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.models.request import Request, RequestProcess, RequestStatus, RequestType
from app.models.user import City


def city_count(session: Session, start_date: datetime, end_date: datetime, status: Optional[int] = None,
               request_type: Optional[str] = None, city: Optional[str] = None):
    """
        The function below is used to get the count of requests based on the city, status and type of request.
        The function takes in the following parameters:
        session: the session object
        start_date: the start date of the request
        end_date: the end date of the request
        status: the status of the request
        request_type: the type of request
        The function returns the count of requests based on the city, status and type of request.
    """
    filters = [Request.created_at.between(start_date, end_date)]

    query = session.query(City.city_name, func.count(Request.id))

    if status is not None:
        query = query.join(RequestStatus, Request.status == RequestStatus.id)
        filters.append(RequestStatus.status_name == status)
    if request_type is not None:
        query = query.join(RequestType, Request.request_type == RequestType.id)
        filters.append(RequestType.type_name == request_type)
    if city is not None:
        filters.append(City.city_name == city)

    query = (
        query
        .join(City, Request.city == City.id)
        .filter(*filters)
        .group_by(City.city_name)
    )

    print(query)

    res = query.all()

    return {city: count for city, count in res}


def status_count(session: Session, start_date: datetime, end_date: datetime, status: Optional[int] = None,
                 request_type: Optional[str] = None, city: Optional[str] = None):
    """
        The function below is used to get the count of status (open and closed) requests based on the city, and type of request.
        The function takes in the following parameters:
        session: the session object
        start_date: the start date of the request
        end_date: the end date of the request
        city: the city of the request
        request_type: the type of request
        The function returns the count of status (open and closed) requests based on the city, and type of request.
    """
    filters = [Request.created_at.between(start_date, end_date)]

    query = session.query(RequestStatus.status_name, func.count(Request.id))

    if city is not None:
        query = query.join(City, Request.city == City.id)
        filters.append(City.city_name == city)
    if request_type is not None:
        query = query.join(RequestType, Request.request_type == RequestType.id)
        filters.append(RequestType.type_name == request_type)
    if status is not None:
        filters.append(RequestStatus.status_name == status)

    query = (
        query
        .join(RequestStatus, Request.status == RequestStatus.id)
        .filter(*filters)
        .group_by(RequestStatus.status_name)
    )

    res = query.all()

    return {status: count for status, count in res}


def type_count(session: Session, start_date: datetime, end_date: datetime, status: Optional[int] = None,
               request_type: Optional[str] = None, city: Optional[str] = None):
    """
        The function below is used to get the count of requests based on the type of request.
        The function takes in the following parameters:
        session: the session object
        start_date: the start date of the request
        end_date: the end date of the request
        city: the city of the request
        The function returns the count of requests based on the type of request.
    """
    filters = [Request.created_at.between(start_date, end_date)]

    query = session.query(RequestType.type_name, func.count(Request.id))

    if city is not None:
        query = query.join(City, Request.city == City.id)
        filters.append(City.city_name == city)
    if status is not None:
        query = query.join(RequestStatus, Request.status == RequestStatus.id)
        filters.append(RequestStatus.status_name == status)
    if request_type is not None:
        filters.append(RequestType.type_name == request_type)

    query = (
        query
        .join(RequestType, Request.request_type == RequestType.id)
        .filter(*filters)
        .group_by(RequestType.type_name)
    )

    res = query.all()

    return {type_name: count for type_name, count in res}


def request_completion_time(session: Session, start_date: datetime, end_date: datetime, city: Optional[int] = None,
                            request_type: Optional[str] = None):
    """
        The function below is used to get the time taken to close a request based on the city, and type of request.
        The function takes in the following parameters:
        session: the session object
        start_date: the start date of the request
        end_date: the end date of the request
        city: the city of the request
        request_type: the type of request
        The function returns the time taken to close a request based on the city, and type of request.
    """
    filters = [Request.created_at.between(start_date, end_date), RequestStatus.status_name == RequestStatus.COMPLETED]

    query = session.query(
        Request.id,
        (func.extract('epoch', RequestProcess.completed_at) - func.extract('epoch', Request.created_at)).label(
            "completion_time")
    )

    if city is not None:
        query = query.join(City, Request.city == City.id)
        filters.append(City.city_name == city)
    if request_type is not None:
        query = query.join(RequestType, Request.status == RequestType.id)
        filters.append(RequestType.type_name == request_type)

    query = (
        query
        .join(RequestProcess, Request.id == RequestProcess.request_id)
        .join(RequestStatus, RequestProcess.status == RequestStatus.id)
        .filter(*filters)
    )

    res = query.all()

    return {request_id: completion_time for request_id, completion_time in res}


def custom_query(session: Session, query: str):
    """
        The function below is used to run a RAW SQL query.
        The function takes in the following parameters:
        session: the session object
        query: the RAW SQL query
        The function returns the result of the RAW SQL query.
    """
    res = session.execute(text(query))
    fetchall = res.fetchall()
    return fetchall

