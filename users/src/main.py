from fastapi import FastAPI, Depends
import logging
from auth.schemas import UserRead, UserCreate, UserUpdate
from auth.users import auth_backend, fastapi_users, current_active_user
from routers import user_router
from database.models import User


LOGGER = logging.getLogger(__name__)


users_app = FastAPI(
    title="Users"
)


users_app.include_router(user_router)
users_app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt", tags=["auth"]
)
users_app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
users_app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
users_app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
users_app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@users_app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
