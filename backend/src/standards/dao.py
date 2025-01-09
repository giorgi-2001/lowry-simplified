from sqlalchemy import select, delete, update, desc
from sqlalchemy.exc import SQLAlchemyError
from ..database import SessionLocal
from .models import Standard


class StandardDao:
    session_maker = SessionLocal
    model = Standard

    @classmethod
    async def list_all_standards(cls):
        async with cls.session_maker() as session:
            statement = select(cls.model).order_by(desc(cls.model.created_at))
            result = await session.execute(statement)
            return result.scalars().all()
        
    @classmethod
    async def get_standards_by_user_id(cls, user_id: int):
        async with cls.session_maker() as session:
            statement = (
                select(cls.model)
                .where(cls.model.user_id == user_id)
                .order_by(desc(cls.model.created_at))
            )
            result = await session.execute(statement)
            return result.scalars().all()
    
    @classmethod
    async def get_standard_by_id(cls, id: int):
        async with cls.session_maker() as session:
            statement = select(cls.model).where(cls.model.id == id)
            result = await session.execute(statement)
            return result.scalar_one_or_none()
        
    @classmethod
    async def create_standard(cls, data):
        async with cls.session_maker() as session:
            async with session.begin():
                standard = cls.model(**data)
                session.add(standard)

                try:
                    await session.flush()
                except SQLAlchemyError:
                    session.rollback()
                    raise

                await session.commit()
            
            await session.refresh(standard)
            return standard.id
        
    @classmethod
    async def delete_standrd_by_id(cls, id: int):
        async with cls.session_maker() as session:
            async with session.begin():
                statement = delete(cls.model).where(cls.model.id == id)
                await session.execute(statement)
                await session.commit()
            
            return id