import uuid
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from beanie import PydanticObjectId


class ItemType(str, Enum):
    owner = "owner"
    admin = "admin"
    operator = "operator"


class UserRegisterRequest(BaseModel):
    username: str = Field(...)
    password: str
    role: ItemType = ItemType.operator
    # model_config
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "username": "admin",
                "password": "Atsjsc123",
                "role": "admin"
            }
        }
    )


class UserItemResponse(BaseModel):
    id: PydanticObjectId
    username: str
    role: ItemType = ItemType.operator
    managed_projects: list[PydanticObjectId]


class LoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    # model_config
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "username": "admin",
                "password": "Atsjsc123",
            }
        }
    )


class Token(BaseModel):
    access_token: str
    refresh_token: str
    versionId: PydanticObjectId


class TokenData(BaseModel):
    username: str | None = None


class RefreshToken(BaseModel):
    refresh_token: str = Field(...)
