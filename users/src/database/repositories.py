"""  User repository file """
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from database.abstract_repo import Repository

from .models import User


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
        self,
        email: str,
        hashed_password: str = None,
        first_name: str = None,
        second_name: str = None,
        buy_volume: Decimal = 0,
        sell_volume: Decimal = 0,
        is_verified: bool = False,
    ) -> None:

        new_user = await self.session.merge(
            self.type_model(
                email=email,
                hashed_password=hashed_password,
                first_name=first_name,
                second_name=second_name,
                buy_volume=buy_volume,
                sell_volume=sell_volume,
                is_verified=is_verified
            )
        )
        return new_user
