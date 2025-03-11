from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .database import SessionLocal
from src.projects.dao import ProjectDAO


class TestProjectDao(ProjectDAO):
    session_maker: async_sessionmaker[AsyncSession] = SessionLocal


@pytest_asyncio.fixture
async def new_project():
    project_data = {
        "name": "Project",
        "description": "Description",
        "user_id": 1
    }
    return await TestProjectDao.create_project(project_data=project_data)


@pytest.mark.asyncio
async def test_list_all_projects():
    result = await TestProjectDao.list_all_projects(1)
    assert result is not None


@pytest.mark.asyncio
async def test_get_by_id(new_project):
    result = await TestProjectDao.get_project_by_id(new_project)
    assert result is not None


@pytest.mark.asyncio
async def test_get_by_id_result_none():
    result = await TestProjectDao.get_project_by_id(project_id=uuid4().hex)
    assert result is None
