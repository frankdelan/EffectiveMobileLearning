import asyncio
import enum
from typing import Optional
import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, async_engine


class Genre(Base):
    __tablename__ = 'genre'

    genre_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name_genre: Mapped[str]


class Author(Base):
    __tablename__ = 'author'

    author_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name_author: Mapped[str]


class Book(Base):
    __tablename__ = 'book'

    book_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey('genre.genre_id'))
    author_id: Mapped[int] = mapped_column(ForeignKey('author.author_id'))
    title: Mapped[str]
    price: Mapped[float]
    amount: Mapped[int]


class City(Base):
    __tablename__ = 'city'

    city_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name_city: Mapped[str]
    days_delivery: Mapped[datetime.date]


class Client(Base):
    __tablename__ = 'client'

    client_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name_client: Mapped[str]
    email: Mapped[str]
    city_id: Mapped[int] = mapped_column(ForeignKey('city.city_id'))


class Buy(Base):
    __tablename__ = 'buy'

    buy_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    buy_description: Mapped[Optional[str]]
    client_id: Mapped[int] = mapped_column(ForeignKey('client.client_id'))


class BuyBook(Base):
    __tablename__ = 'buy_book'

    buy_book_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('client.client_id'))
    book_id: Mapped[int] = mapped_column(ForeignKey('book.book_id'))
    amount: Mapped[int]


class Stage(enum.Enum):
    INACTIVE = 'На складе'
    IN_TRANSIT = 'В пути'
    DELIVERED = 'Доставлен'


class Step(Base):
    __tablename__ = 'step'

    step_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name_step: Mapped[Stage]


class BuyStep(Base):
    __tablename__ = 'buy_step'

    buy_step_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    buy_id: Mapped[int] = mapped_column(ForeignKey('buy.buy_id'))
    step_id: Mapped[int] = mapped_column(ForeignKey('step.step_id'))
    date_step_beg: Mapped[datetime.date] = mapped_column(server_default=func.current_date(),
                                                         default=func.current_date())
    date_step_end: Mapped[Optional[datetime.date]]


# async def create_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
# asyncio.run(create_tables())
