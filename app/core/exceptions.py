from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class DuplicateEmailException(Exception):
    pass


class AuthenticationFailException(Exception):
    pass


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(DuplicateEmailException)
    async def duplicate_email_handler(request: Request, exc: DuplicateEmailException):
        return JSONResponse(
            status_code=400,
            content={"message": "Email already registered."},
        )

    @app.exception_handler(AuthenticationFailException)
    async def authentication_fail_handler(
        request: Request, exc: AuthenticationFailException
    ):
        return JSONResponse(
            status_code=401,
            content={
                "message": "Authentication failed. Please check your credentials."
            },
        )
