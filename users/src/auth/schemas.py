from typing import Optional
import uuid
from fastapi_users import schemas


class UserGetDTO(schemas.BaseUser[uuid.UUID]):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserPostDTO(schemas.BaseUserCreate):
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserPatchDTO(schemas.BaseUserUpdate):
    pass
