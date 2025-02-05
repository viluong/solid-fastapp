from fastapi import FastAPI

from app.api.v1.router import router
from app.core.exceptions import add_exception_handlers

app = FastAPI()

add_exception_handlers(app)

app.include_router(router, prefix="/api/v1")