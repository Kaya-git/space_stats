import asyncio
import pytest
from src.routers import add_api, delete_api, show_my_api
from src.database.base_model import Base, engine
from src.database.db import Database, async_session_maker
from src.database.models import User, ApiKey


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
async def fill_db():
    async with async_session_maker as session:
        db = Database(session)
        user = await db.user.new()
        db.session.add(user)
        await db.session.flush()
        api_keys = [
            await db.api_key.new(key_name="qwerty", hashed_key="qwerty", user_id=user.id),
            await db.api_key.new(key_name="asdf", hashed_key="asdf", user_id=user.id)
        ]
        db.session.add_all(api_keys)
        await db.session.commit()


@pytest.mark.usefixtures("fill_db")
@pytest.mark.asyncio
class Test_User_routers:

    async def test_add_api():
        ...

    async def test_delete_api():
        ...

    async def test_show_my_api():
        ...
