# from jose import JWTError, jwt

from typing import Optional
from fastapi import APIRouter, Body, Request, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from starlette import status
from jose import JWTError, jwt

from app.models import User
from app.core.config import settings
from app.schemas.sche_user import UserRegisterRequest, LoginRequest, RefreshToken
from app.core.security import get_password_hash, verify_password
from app.core.config import settings


class UserService(object):
    __instance = None

    def __init__(self) -> None:
        pass

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )

    @staticmethod
    async def register_user(data: UserRegisterRequest):
        try:

            exist_user = await User.find_one({"username": data.username})
            if exist_user:
                raise Exception('Username already exists')
            hash_password = get_password_hash(data.password)
            new_user = User(username=data.username,
                            role=data.role, password=hash_password)
            insert_user = await new_user.create()
            return insert_user
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def authenticate(data: LoginRequest) -> Optional[User]:
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        user = await User.find_one(User.username == data.username)

        if not user:
            return False
        if not verify_password(data.password, user.password):
            return False
        return user

    @staticmethod
    async def refreshToken(username: str) -> Optional[User]:
        user = await User.find_one(
            {"username": username},
        )
        if not user:
            return False
        return user

    @staticmethod
    async def get_current_user(http_authorization_credentials: str) -> User:
        """
        Decode JWT token to get user_id => return User info from DB query
        """
        try:
            payload = jwt.decode(
                http_authorization_credentials, settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")

        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"jwt expired",
            )
        user = await User.find_one(
            {"username": username},
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def get_list_user() -> list[User]:
        try:
            list_user = await User.find().to_list()
            return list_user
        except Exception as e:
            raise HTTPException(status_code=404, detail=e)

    @staticmethod
    async def update_user(param: str, data: str):
        hash_password = get_password_hash(data)
        try:
            result = await User.find_one(User.id == param).update({"$set": {User.password: hash_password}})
            if result.modified_count == 1:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail=e)

    @staticmethod
    async def delete_user(param: str) -> bool:
        try:
            await User.find_one(User.id == param).delete()
            return True
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail=e)
