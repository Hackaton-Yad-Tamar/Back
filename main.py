from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
from datetime import datetime
from app.api.endpoints.requests import request_router
from app.core.database import engine
Base = declarative_base()

app = FastAPI()

app.include_router(request_router, prefix="/api")

    # Create tables in the database
Base.metadata.create_all(bind=engine)