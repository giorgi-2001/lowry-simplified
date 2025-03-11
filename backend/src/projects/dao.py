from ..database import SessionLocal
from .models import Project

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, desc, delete, update

from uuid import UUID


class ProjectDAO:
    model = Project
    session_maker: async_sessionmaker[AsyncSession] = SessionLocal

    @classmethod
    async def list_all_projects(cls, user_id):
        async with cls.session_maker() as session:
            statement = (
                select(cls.model)
                .where(cls.model.user_id == user_id)
                .order_by(desc(cls.model.created_at))
            )
            result = await session.execute(statement)
            return result.scalars().all()

    @classmethod
    async def get_project_by_id(cls, project_id: str):
        project_id = UUID(project_id)
        async with cls.session_maker() as session:
            statement = select(cls.model).where(cls.model.id == project_id)
            result = await session.execute(statement)
            project = result.scalar_one_or_none()
            return project

    @classmethod
    async def create_project(cls, project_data: dict):
        async with cls.session_maker() as session:
            async with session.begin():
                new_project = Project(**project_data)
                session.add(new_project)
                await session.commit()

            await session.refresh(new_project)
            return new_project.id.hex

    @classmethod
    async def delete_project(cls, project_id: str):
        project_id = UUID(project_id)
        async with cls.session_maker() as session:
            async with session.begin():
                statement = delete(cls.model).where(cls.model.id == project_id)
                await session.execute(statement)
                await session.commit()

            return project_id

    @classmethod
    async def update_project(cls, project_id: int, project_data: dict):
        project_id = UUID(project_id)
        async with cls.session_maker() as session:
            async with session.begin():
                statement = (
                    update(cls.model)
                    .where(cls.model.id == project_id)
                    .values(**project_data)
                )
                await session.execute(statement)
                await session.commit()
            return project_id
