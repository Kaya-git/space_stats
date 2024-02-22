from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from config import conf
from .repositories import UserRepo

from .base_model import Base

engine = _create_async_engine(
    url=conf.db.build_connection_str(),
    echo=conf.debug,
    pool_pre_ping=True
)


async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()


class Database:
    """
    Database class is the highest abstraction level of database
    and can be used in the handlers or any other bot-side functions
    """

    user: UserRepo
    """ User repository """

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession = None,
        user: UserRepo = None
    ) -> None:

        self.session = session
        self.user = user or UserRepo(session=session)
