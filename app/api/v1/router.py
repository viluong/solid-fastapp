from fastapi import APIRouter

from app.api.v1.endpoints import users, auth

router = APIRouter()
router.include_router(users.router, prefix="/auth", tags=["auth"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
