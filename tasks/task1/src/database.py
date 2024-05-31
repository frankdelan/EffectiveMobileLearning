from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from config import DB_PASS, DB_PORT, DB_HOST, DB_NAME, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

Base = declarative_base()

async_engine = create_async_engine(DATABASE_URL)
