from fastapi import APIRouter
from app.api.v1.endpoints import users

router = APIRouter()
router.include_router(users.router, prefix="/auth", tags=["auth"])