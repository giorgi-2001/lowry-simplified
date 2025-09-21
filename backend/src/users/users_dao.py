from sqlalchemy import select, delete

from ..database import SessionLocal
from .models import User


class UserDao:
    session_maker = SessionLocal
    model = User

    @classmethod
    async def list_all_users(cls):
        async with cls.session_maker() as session:
            statement = select(cls.model).order_by(cls.model.created_at)
            result = await session.execute(statement)
            users = result.scalars().all()
            return users

    @classmethod
    async def get_user_by_username(cls, username: str):
        async with cls.session_maker() as session:
            statement = select(cls.model).where(cls.model.username == username)
            result = await session.execute(statement)
            user = result.scalar_one_or_none()
            return user

    @classmethod
    async def register_user(cls, userdata: dict):
        async with cls.session_maker() as session:
            async with session.begin():
                user = cls.model(**userdata)
                session.add(user)
                await session.commit()

            await session.refresh(user)
            return user.username

    @classmethod
    async def delete_user(cls, id: int):
        async with cls.session_maker() as session:
            async with session.begin():
                statement = select(cls.model).where(cls.model.id == id)
                result = await session.execute(statement)
                user = result.scalar_one_or_none()

                if not user:
                    return None

                statement = delete(cls.model).where(cls.model.id == id)
                await session.execute(statement)
                await session.commit()

            return user.username
