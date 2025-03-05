from fastapi import FastAPI
from .api.endpoints.users import users_router

app = FastAPI()
app.include_router(users_router, prefix="/users")


@app.get("/")
def health_check():
    return "hello world"
