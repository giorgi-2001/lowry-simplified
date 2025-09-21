import uuid

from typing import Literal
from ..database import SessionLocal
from .models import Experiment

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, desc, delete


class ExperimentDAO:
    model = Experiment
    session_maker: async_sessionmaker[AsyncSession] = SessionLocal

    @classmethod
    async def get_experiments_by_project_id(cls, project_id: str):
        project_id = uuid.UUID(project_id)
        async with cls.session_maker() as session:
            statement = select(cls.model).where(
                cls.model.project_id == project_id
            ).order_by(desc(cls.model.created_at))
            result = await session.execute(statement)
            return result.scalars().all()

    @classmethod
    async def get_experiments_by_id(cls, experiment_id: int):
        async with cls.session_maker() as session:
            statement = select(cls.model).where(
                cls.model.id == experiment_id
            )
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    @classmethod
    async def create_experiment(cls, experiment_data: dict):
        experiment_data["project_id"] = uuid.UUID(experiment_data["project_id"])
        async with cls.session_maker() as session:
            async with session.begin():
                new_experiment = cls.model(**experiment_data)
                session.add(new_experiment)
                await session.commit()
            await session.refresh(new_experiment)
            return new_experiment.id

    @classmethod
    async def delete_experiment(cls, experiment_id: int):
        async with cls.session_maker() as session:
            async with session.begin():
                statement = delete(cls.model).where(
                    cls.model.id == experiment_id
                )
                await session.execute(statement)
                await session.commit()
            return experiment_id

    @classmethod
    async def update_file(
        cls, experiment_id: int,
        file_name: str,
        file_type: Literal["csv", "img"]
    ):
        async with cls.session_maker() as session:
            async with session.begin():
                statement = select(cls.model).where(cls.model.id == experiment_id)
                result = await session.execute(statement)
                experiment = result.scalar_one_or_none()

                if not experiment:
                    return None

                if file_type == "csv":
                    experiment.csv = file_name
                elif file_type == "img":
                    experiment.image = file_name
                else:
                    raise ValueError("Unsupported file type was provided")

                await session.commit()
            await session.refresh(experiment)
            return experiment
