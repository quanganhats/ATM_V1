from datetime import datetime

from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from app.helpers.exception_handler import CustomException

from app.schemas.sche_user import Token, RefreshToken, UserItemResponse
from app.services.srv_user import UserService
from datetime import datetime, timedelta, timezone
from app.core.security import create_token
from fastapi.encoders import jsonable_encoder
from jose import jwt, JWTError
from app.helpers.login_manager import login_required, PermissionRequired
from app.models import User
from typing import Annotated

from app.core.config import settings
router = APIRouter()


@router.post('/token', response_model=Token)
async def refreshToken(form_data: RefreshToken = Body(...), user_service: UserService = Depends()):

    user = await user_service.get_current_user(form_data.refresh_token)
    if not user:
        raise CustomException(http_code=status.HTTP_401_UNAUTHORIZE, code='401', message=str(
            "jwt refresh token expired"))
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(
        data={"sub": user.username, "role": user.role},  expires_delta=access_token_expires
    )
    return Token(access_token=access_token, refresh_token=form_data.refresh_token)


@router.post('/logout',  dependencies=[Depends(login_required)])
async def logout():
    return


@router.get('/user/active',  dependencies=[Depends(login_required)])
async def getUserActive(current_user: Annotated[User, Depends(login_required)]) -> UserItemResponse:
    return current_user


@router.put('/user/active',  dependencies=[Depends(login_required)])
async def getUserActive(current_user: Annotated[User, Depends(login_required)], form_data: str = Body(...), user_service: UserService = Depends()) -> dict:
    update_bool = await user_service.update_user(current_user.id, form_data)
    if update_bool:
        return {"message": "Update success"}
    else:
        raise CustomException(http_code=status.HTTP_404_NOT_FOUND, code='404', message=str(
            "update error"))


@router.get('/users')
async def getUserList(user_service: UserService = Depends()) -> list[UserItemResponse]:
    list_user = await user_service.get_list_user()
    return list_user


@router.put('/user/{user_id}')
async def updateUser(user_id, form_data: str = Body(...), user_service: UserService = Depends()) -> dict:
    update_bool = await user_service.update_user(user_id, form_data)
    if update_bool:
        return {"message": "Update success"}
    else:
        raise CustomException(http_code=status.HTTP_404_NOT_FOUND, code='404', message=str(
            "update error"))


@router.delete('/user/{user_id}')
async def deleteUser(user_id, user_service: UserService = Depends()) -> dict:
    delete_bool = await user_service.delete_user(user_id)
    if delete_bool:
        return {"message": "Delete success"}
