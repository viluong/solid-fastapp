from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class DuplicateEmailException(Exception):
    pass

def add_exception_handlers(app: FastAPI):
    @app.exception_handler(DuplicateEmailException)
    async def duplicate_email_handler(request: Request, exc: DuplicateEmailException):
        return JSONResponse(
            status_code=400,
            content={"message": "Email already registered"},
        )