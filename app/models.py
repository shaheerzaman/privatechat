from sqlalchemy import Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String, DateTime, UUID
from datetime import datetime
import uuid

from .db import Base
from .schemas import UserLevel


class User(Base):
    __tablename__ = "users"
    # id = Column(Integer, primary_key=True, index=True)
    id = Column(String, primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    age = Column(Integer)
    level = Column(SQLEnum(UserLevel))
    created_at = Column(DateTime, default=datetime.utcnow)
