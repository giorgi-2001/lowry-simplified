import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from httpx import AsyncClient, ASGITransport

from .database import engine, SessionLocal, DB_PATH
from .test_project_dao import TestProjectDao
from src.database import Base
from src.users.models import User
from src.standards.models import Standard
from src.projects.models import Project
from src.users.users_dao import UserDao
from src.standards.dao import StandardDao
from src.projects.dao import ProjectDAO
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
        async with session.begin():
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


@pytest_asyncio.fixture
async def test_user(user_factory):
    user = await user_factory("TestUser", "test@test.com", "testuser123")
    return user


@pytest_asyncio.fixture
async def standard_factory(session: AsyncSession, test_user):
    async def create_standard(
        name, description, image, correlation,
        slope, y_intercept, user_id=test_user.id,
    ):
        standard = Standard(
            name=name, description=description, image=image,
            correlation=correlation, slope=slope,
            y_intercept=y_intercept, user_id=user_id
        )

        session.add(standard)
        await session.flush()

        return standard
    return create_standard


@pytest_asyncio.fixture
async def project_factory(test_user, session: AsyncSession):
    async def create_standard(
        name="name", description="description",
        user_id=test_user.id
    ):
        project = Project(
            name=name, description=description, user_id=user_id
        )
        session.add(project)
        await session.flush()
        return project
    return create_standard


@pytest_asyncio.fixture(scope="module")
async def client():
    class TestUserDao(UserDao):
        session_maker = SessionLocal

    class TestStandardDao(StandardDao):
        session_maker = SessionLocal

    app.dependency_overrides[UserDao] = TestUserDao
    app.dependency_overrides[StandardDao] = TestStandardDao
    app.dependency_overrides[ProjectDAO] = TestProjectDao

    base_url = "http://localhost:8000/api/v1"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=base_url
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def login_user(client: AsyncClient):
    user_data = {
        "username": "random_user",
        "password": "password123",
        "email": "random@random.com"
    }
    await client.post("/users/register", json=user_data)
    response = await client.post("/users/login", json=user_data)
    token = response.json().get("access_token")
    client.headers["Authorization"] = f"Bearer {token}"
    yield
    client.headers.pop("Authorization")
