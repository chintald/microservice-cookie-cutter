from datetime import datetime

from pydantic import Field
from fastapi_utils.api_model import APIMessage, APIModel


class User(APIModel):
    id: int = Field(None, description="ID")
    password: str = Field(None, description="Password")
    email: str = Field(None, description="Email")
    nickname: str = Field(None, description="Nickname")
    is_admin: bool = Field(None, description="Is admin")
    created_at: datetime = Field(None, description="Create Time")
    updated_at: datetime = Field(None, description="Update Time")
