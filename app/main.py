from fastapi import FastAPI

from .api.endpoints.admin.dashboard import dashboard_router
from .api.endpoints.users import users_router

app = FastAPI()
app.include_router(users_router, prefix="/users")
app.include_router(dashboard_router, prefix="/admin/dashboard")


@app.get("/")
def health_check():
    return "hello world"
