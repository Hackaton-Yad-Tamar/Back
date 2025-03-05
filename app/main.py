from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Import CORS middleware

from .api.endpoints.admin.dashboard import dashboard_router
from .api.endpoints.users import users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (you can restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PATCH, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(users_router, prefix="/users")
app.include_router(dashboard_router, prefix="/admin/dashboard")


@app.get("/")
def health_check():
    return "hello world"
