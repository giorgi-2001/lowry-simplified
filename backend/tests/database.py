from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from pathlib import Path


DB_PATH = Path(__file__).parent.joinpath("test_database.db").resolve()

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"


engine = create_async_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False},
    future=True
)


SessionLocal = async_sessionmaker(autoflush=False, bind=engine)