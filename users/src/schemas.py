from pydantic import BaseModel
from auth.schemas import UserGetDTO
import uuid


class ApiKeyPostDTO(BaseModel):
    key_name: str
    hashed_key: str


class ApiKeyGetDTO(ApiKeyPostDTO):
    id: uuid.UUID
    user_id: uuid.UUID

    class Config:
        from_attributes = True


class ApiKeyRelDTO(ApiKeyGetDTO):
    user: "UserGetDTO"


class UserRelDTO(UserGetDTO):
    api_keys: list["ApiKeyGetDTO"]
