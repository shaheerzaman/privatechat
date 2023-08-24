from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


class Base(DeclarativeBase):
    pass
