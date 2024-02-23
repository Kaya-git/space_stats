from fastapi import APIRouter, Depends
from database.db import get_async_session, Database
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from auth.users import current_active_user
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database import User


LOGGER = logging.getLogger(__name__)


user_router = APIRouter(
    prefix="/api/users",
    tags=["Роутер Users"]
)


@user_router.post("/add_api")
async def add_api(
    api_name,
    api_key,
    user: "User" = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):

    db = Database(session)
    try:
        new_api_key = await db.api_key.new(
            key_name=api_name,
            hashed_key=api_key,
            user_id=user.id
        )
        db.session.add(new_api_key)
        await db.session.flush()
    except Exception as exc:
        LOGGER.error(exc)
        raise
    await db.session.commit()
    return {
        "status": f"{new_api_key.id}"
    }
