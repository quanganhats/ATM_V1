from fastapi import APIRouter

from app.api import api_login, api_register, api_auth

router = APIRouter()
router.include_router(api_register.router, tags=[
                      "register"], prefix="/register")
router.include_router(api_login.router, tags=["login"], prefix="/login")

router.include_router(api_auth.router, tags=["Auth"], prefix="/auth")
# router.include_router(api_DSA.router, tags=["DSA"], prefix="/dsa")

