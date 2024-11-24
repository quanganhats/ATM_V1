from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.encoders import jsonable_encoder

from app.schemas.sche_user import UserItemResponse, UserRegisterRequest
from app.services.srv_user import UserService
from app.helpers.login_manager import login_required, PermissionRequired

router = APIRouter()


@router.post('', response_model=UserItemResponse)
async def register(register_data: UserRegisterRequest, user_service: UserService = Depends()) -> Any:
    try:
        return await user_service.register_user(register_data)
        # return UserItemResponse(id=register_user.id,
        #                         username=register_user.username,
        #                         role=register_user.role)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
# dependencies=[Depends(PermissionRequired('admin'))],
