import uuid
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from beanie import Document, Indexed, init_beanie
from app.schemas.sche_user import ItemType
from beanie import PydanticObjectId


class User(Document):
    # id: PydanticObjectId = Field(alias="_id")
    username: str = Field(...)
    role: ItemType = ItemType.operator
    password: str = Field(...)
    managed_projects: list[PydanticObjectId] = []
