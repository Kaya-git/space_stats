from fastapi import FastAPI
import logging
from auth import UserRead, UserCreate, auth_backend, fastapi_users
from routers import user_router


LOGGER = logging.getLogger(__name__)


users_app = FastAPI(
    title="Users"
)

users_app.include_router(user_router)
users_app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/api/auth/jwt",
    tags=["auth"],
)
users_app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)
users_app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/api/auth",
    tags=["auth"],
)
users_app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/api/auth",
    tags=["auth"],
)
