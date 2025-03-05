from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.adminview_db import city_count, status_count, type_count, time_taken, request_completion_time
from fastapi import FastAPI

class DBManager:
    def __init__(self, db_url, app: FastAPI):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.app = app  # Store FastAPI instance
        self.register_routes()

    def execute_query(self, query_func, *args, **kwargs):
        """Helper method to manage session lifecycle and execute queries."""
        with self.Session() as session:
            try:
                return query_func(session, *args, **kwargs)
            except Exception as e:
                session.rollback()
                print(f"Database query error: {e}")  # Replace with proper logging
                return None
    
    def city_count(self, start_date, end_date, status=None, type=None):
        return self.execute_query(city_count, start_date, end_date, status, type)
    
    def status_count(self, start_date, end_date, city=None, type=None):
        return self.execute_query(status_count, start_date, end_date, city, type)

    def type_count(self, start_date, end_date, city=None, type=None):
        return self.execute_query(type_count, start_date, end_date, city, type)
    
    def time_taken(self, start_date, end_date, city=None, type=None):
        return self.execute_query(time_taken, start_date, end_date, city, type)
    
    def request_completion_time(self, start_date, end_date, city=None, request_type=None):
        return self.execute_query(request_completion_time, start_date, end_date, city, request_type)

    def register_routes(self):
        """Registers API routes related to this manager."""
        @self.app.post("/city-count")
        def get_city_count(start_date: str, end_date: str, status: str = None, request_type: str = None):
            return self.city_count(start_date, end_date, status, request_type)

        @self.app.post("/status-count")
        def get_status_count(start_date: str, end_date: str, city: str = None, request_type: str = None):
            return self.status_count(start_date, end_date, city, request_type)

        @self.app.post("/type-count")
        def get_type_count(start_date: str, end_date: str, city: str = None, request_type: str = None):
            return self.type_count(start_date, end_date, city, request_type)
        
        @self.app.post("/time-taken")
        def get_time_taken(start_date: str, end_date: str, city: str = None, request_type: str = None):
            return self.time_taken(start_date, end_date, city, request_type)
        
        @self.app.post("/request-completion-time")
        def get_request_completion_time(start_date: str, end_date: str, city: str = None, request_type: str = None):
            return self.request_completion_time(start_date, end_date, city, request_type)
