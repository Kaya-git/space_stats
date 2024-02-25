"""  User repository file """
from sqlalchemy.ext.asyncio import AsyncSession

from database.abstract_repo import Repository
from .db import async_session_maker
from .models import User, ApiKey


class UserRepo(Repository[User]):
    """
    User repository for CRUD
    and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize User
        repository as for all User
        or only for one
        """
        super().__init__(type_model=User, session=session)

    async def new(
        self
    ) -> None:
        async with async_session_maker() as session:
            user = await session.merge(
                self.type_model(
                    email="admin",
                    hashed_password="admin",
                    is_active=True,
                    is_superuser=False,
                    is_verified=False
                )
            )
            return user


class ApiRepo(Repository[ApiKey]):
    """
    User repository for CRUD
    and other SQL queries
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize User
        repository as for all User
        or only for one
        """
        super().__init__(type_model=ApiKey, session=session)

    async def new(
        self,
        key_name,
        hashed_key,
        user_id,
    ) -> None:
        async with async_session_maker() as session:
            api_key = await session.merge(
                self.type_model(
                    key_name=key_name,
                    hashed_key=hashed_key,
                    user_id=user_id
                )
            )
            return api_key

    async def update_key(
        self
    ):
        ...
