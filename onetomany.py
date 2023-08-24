import asyncio

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True,
)


# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


Base = declarative_base()


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    data = Column(String)
    create_date = Column(DateTime, server_default=func.now())
    bs = relationship("B")

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)
    a_id = Column(ForeignKey("a.id"))
    data = Column(String)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    A(bs=[B(), B()], data="a1"),
                    A(bs=[B()], data="a2"),
                ]
            )

    async with async_session() as session:
        result = await session.execute(
            select(A).order_by(A.id).options(selectinload(A.bs))
        )
        a1 = result.scalars().first()

        # no issue:
        print(a1.name, a1.data)
        print(a1.bs)

        # await session.refresh(a1, attribute_names=["bs"])
        # print(a1.bs)


asyncio.run(main())
