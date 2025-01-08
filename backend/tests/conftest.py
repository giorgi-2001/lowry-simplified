import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from .database import engine, SessionLocal, DB_PATH
from src.database import Base
from src.users.models import User
from src.users.users_dao import UserDao
from src.main import app

import os


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await conn.run_sync(Base.metadata.drop_all)
        os.remove(DB_PATH)


@pytest_asyncio.fixture
async def session():
    async with SessionLocal() as session:
        async with session.begin() as transaction:
            yield session
            await session.rollback()


@pytest_asyncio.fixture
async def user_factory(session: AsyncSession):
    async def get_user(
        username: str, email: str, password: str
    ):
        user = User(
            username=username,
            email=email,
            password=password
        )
        session.add(user)
        await session.flush()
        return user

    return get_user


@pytest_asyncio.fixture()
async def test_user(user_factory):
    user = await user_factory("TestUser", "test@test.com", "testuser123")
    return user


@pytest_asyncio.fixture
async def client():
    class TestUserDao(UserDao):
        session_maker = SessionLocal

    app.dependency_overrides[UserDao] = TestUserDao

    yield TestClient(app)
    
    app.dependency_overrides[TestUserDao] = UserDao