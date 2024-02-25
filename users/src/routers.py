from fastapi import APIRouter, Depends, HTTPException, status
from database.db import get_async_session, Database
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from auth.users import current_active_user
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from database.models import User
from database.models import ApiKey
from schemas import ApiKeyPostDTO, ApiKeyRelDTO
import uuid


LOGGER = logging.getLogger(__name__)


user_router = APIRouter(
    prefix="/api/users",
    tags=["users api keys"]
)


@user_router.post("/add_api")
async def add_api(
    api_key: ApiKeyPostDTO,
    user: "User" = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> bool:

    db = Database(session)

    new_api_key = await db.api_key.new(
        key_name=api_key.key_name,
        hashed_key=api_key.hashed_key,
        user_id=user.id
    )
    db.session.add(new_api_key)
    await db.session.flush()
    LOGGER.info(f"Добавили новый ключ с id:{new_api_key.id}")
    await db.session.commit()
    return True


@user_router.post("/delete_api")
async def delete_api(
    api_id: uuid.UUID,
    user: "User" = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> bool:
    db = Database(session)
    await db.api_key.delete(
        ApiKey.id == api_id
    )

    if await db.api_key.get(api_id):
        LOGGER.error(f"Ошибка с удаление api ключа: id{api_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка с удалением из бд"
        )
    else:
        return True


@user_router.get("/show_my_api")
async def show_my_api(
    user: "User" = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
) -> List[ApiKeyRelDTO] | None:
    db = Database(session)
    api_keys = await db.api_key.get_many_where(
        ApiKey.user_id == user.id
    )
    if api_keys:
        LOGGER.info(f"Запрошены ключи пользователя. user_id: {user.id}")
        result_api_keys = [
            ApiKeyRelDTO.model_validate(
                row, from_attributes=True
            ) for row in api_keys
        ]
        return result_api_keys
    else:
        LOGGER.info(f"Ключи пользователя не найдены. user_id:{user.id}")
        return None
