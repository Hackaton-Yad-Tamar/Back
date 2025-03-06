from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.api.endpoints.requests import request_router
from app.api.endpoints.request_type import request_type_router
from app.core.database import engine
from fastapi.middleware.cors import CORSMiddleware  
Base = declarative_base()



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PATCH, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(request_router, prefix="/api")
app.include_router(request_type_router, prefix="/api")
    # Create tables in the database
Base.metadata.create_all(bind=engine)