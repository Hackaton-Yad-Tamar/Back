from fastapi import FastAPI

from .api.endpoints.admin.dashboard import dashboard_router
from .api.endpoints.users import users_router

app = FastAPI()
app.add_middleware(
    allow_origins=["*"],         # Allows specific origins
    allow_credentials=True,        # Allows cookies
    allow_methods=["*"],           # Allows all HTTP methods
    allow_headers=["*"],           # Allows all headers
)
app.include_router(users_router, prefix="/users")
app.include_router(dashboard_router, prefix="/admin/dashboard")


@app.get("/")
def health_check():
    return "hello world"
