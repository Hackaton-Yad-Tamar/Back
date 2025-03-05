from sqlalchemy import func

from app.models.request import Request, RequestProcess

'''
    The function below is used to get the count of requests based on the city, status and type of request.
    The function takes in the following parameters:
    session: the session object
    start_date: the start date of the request
    end_date: the end date of the request
    status: the status of the request
    type: the type of request
    The function returns the count of requests based on the city, status and type of request.
'''


def city_count(session, start_date, end_date, status=None, type=None):
    filters = [Request.created_at.between(start_date, end_date)]

    if status:
        filters.append(Request.status == status)
    if type:
        filters.append(Request.request_type == type)

    return session.query(Request.city, func.count(Request.city)).filter(*filters).group_by(Request.city).all()


'''
    The function below is used to get the count of status (open and closed) requests based on the city, and type of request.
    The function takes in the following parameters:
    session: the session object
    start_date: the start date of the request
    end_date: the end date of the request
    city: the city of the request
    type: the type of request
    The function returns the count of status (open and closed) requests based on the city, and type of request.
'''


def status_count(session, start_date, end_date, city=None, type=None):
    filters = [Request.created_at.between(start_date, end_date)]

    if city:
        filters.append(Request.city == city)
    if type:
        filters.append(Request.request_type == type)

    return session.query(Request.status, func.count(Request.status)).filter(*filters).group_by(Request.status).all()


'''
    The function below is used to get the count of requests based on the type of request.
    The function takes in the following parameters:
    session: the session object
    start_date: the start date of the request
    end_date: the end date of the request
    city: the city of the request
    type: the type of request
    The function returns the count of requests based on the type of request.
'''


def type_count(session, start_date, end_date, city=None, type=None):
    filters = [Request.created_at.between(start_date, end_date)]

    if city:
        filters.append(Request.city == city)
    if type:
        filters.append(Request.request_type == type)

    return session.query(Request.request_type, func.count(Request.request_type)).filter(*filters).group_by(
        Request.request_type).all()


'''
    The function below is used to get the time taken to close a request based on the city, and type of request.
    The function takes in the following parameters:
    session: the session object
    start_date: the start date of the request
    end_date: the end date of the request
    city: the city of the request
    type: the type of request
    The function returns the time taken to close a request based on the city, and type of request.
'''


def time_taken(session, start_date, end_date, city=None, type=None):
    filters = [Request.created_at.between(start_date, end_date), Request.status == 'closed']

    if city:
        filters.append(Request.city == city)
    if type:
        filters.append(Request.request_type == type)

    return session.query(Request.city, func.avg(func.date_diff(Request.created_at, Request.updated_at))).filter(
        *filters).group_by(Request.city).all()


'''
    The function below is used to get the time taken to close a request based on the city, and type of request.
    The function takes in the following parameters:
    session: the session object
    start_date: the start date of the request
    end_date: the end date of the request
    city: the city of the request
    request_type: the type of request
    The function returns the time taken to close a request based on the city, and type of request.
'''


def request_completion_time(session, start_date, end_date, city=None, request_type=None):
    filters = [Request.created_at.between(start_date, end_date)]

    if city:
        filters.append(Request.city == city)
    if request_type:
        filters.append(Request.request_type == request_type)

    return session.query(
        RequestProcess.request_id,
        (func.extract('epoch', RequestProcess.completed_at) - func.extract('epoch', Request.created_at)).label(
            "completion_time")
    ).join(RequestProcess, Request.id == RequestProcess.request_id).filter(*filters).all()
