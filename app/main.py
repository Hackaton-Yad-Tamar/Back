from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints.admin.dashboard import dashboard_router
from .api.endpoints.users import users_router
from .api.endpoints.admin.approval_api import approve_users
from .api.endpoints.requests import request_router
from .api.endpoints.request_type import request_type_router
from .api.endpoints.request_status import request_status_router
app = FastAPI()

app.include_router(users_router, prefix="/users")
app.include_router(dashboard_router, prefix="/admin/dashboard")
app.include_router(approve_users, prefix="/admin/approval")
app.include_router(request_router, prefix="/api")
app.include_router(request_type_router, prefix="/api")
app.include_router(request_status_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PATCH, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def health_check():
    return "hello world"
