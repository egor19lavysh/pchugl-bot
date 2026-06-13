from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from src.config import settings


DATABASE_URL = settings.DB_URL


engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

def get_async_session():
    return async_session_maker()

# Базовый класс для всех моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True