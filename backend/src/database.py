from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncAttrs
)
from sqlalchemy.orm import (
    DeclarativeBase, Mapped, mapped_column, declared_attr
)
from sqlalchemy import func

from typing import Annotated
from datetime import datetime

from .config import Config


DATABASE_URL = Config.get_db_url()


engine = create_async_engine(DATABASE_URL)


SessionLocal = async_sessionmaker(autoflush=False, bind=engine)


created_at = Annotated[
    datetime, mapped_column(default=func.now(), nullable=False)
]

updated_at = Annotated[
    datetime, mapped_column(default=func.now(), onupdate=func.now(), nullable=False)
]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
