from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from config import Settings

Base = declarative_base()
async_engine = create_async_engine(Settings.DB_URL)
async_session_factory = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession | None]:
    async with async_session_factory() as session:
        yield session
