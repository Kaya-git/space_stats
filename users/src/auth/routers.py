from fastapi_users import FastAPIUsers
import uuid
from .auth import auth_backend
from .db import User
from .manager import get_user_manager

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(
    active=True
)