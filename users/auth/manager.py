from typing import Optional
import uuid

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, UUIDIDMixin, exceptions, models,
                           schemas)

from config import conf
from enums import Role
from sevices import services
from users.models import User

from .db import get_user_db


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = conf.auth.user_menager
    verification_token_secret = conf.auth.user_menager

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None
    ):

        await services.mail.send_token(
            recepient_email=user.email,
            generated_token=user.verification_token
        )
        return f"User {user.id} has registered."

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None
    ):
        return {
            "user": user.id,
            "token": token
        }

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None
    ):
        return {
            "user": user.id,
            "token": token
        }

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role"] = Role.Клиент
        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
