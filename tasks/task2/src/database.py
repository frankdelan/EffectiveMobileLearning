from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from tasks.task2.src.config import DB_PASS, DB_PORT, DB_HOST, DB_NAME, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

Base = declarative_base()

async_engine = create_async_engine(DATABASE_URL)

async_session_factory = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
