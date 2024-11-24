from datetime import datetime

from fastapi import APIRouter, Body, Request, HTTPException, status, Depends

from app.schemas.sche_user import Token, LoginRequest
from app.services.srv_user import UserService
from datetime import datetime, timedelta, timezone
from app.core.security import create_token
from app.core.config import settings
from app.helpers.exception_handler import CustomException


router = APIRouter()


@router.post('', response_model=Token)
async def login_access_token(form_data: LoginRequest = Body(...), user_service: UserService = Depends()):
    user = await user_service.authenticate(form_data)
    if not user:
        # raise CustomException(http_code=status.HTTP_401_UNAUTHORIZE, code='401', message=str(
        #     "Incorrect username or password"))
        raise HTTPException(status_code=401,
                            detail='Incorrect username or password')
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.username, "role": user.role},  expires_delta=access_token_expires
    )
    refresh_token = create_token(
        data={"sub": user.username, "role": user.role},  expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, versionId=user.id)
