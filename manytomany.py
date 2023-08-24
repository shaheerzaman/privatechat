import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.util import await_only, greenlet_spawn

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

Base = declarative_base()

user_tag = Table(
    "user_tag",
    Base.metadata,
    Column("user_id", INTEGER, ForeignKey("users.id")),
    Column("tag_id", INTEGER, ForeignKey("tags.id")),
)


class User(Base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=True)
    tags = relationship(
        "Tag", secondary=user_tag, back_populates="users", lazy="joined"
    )


class Tag(Base):
    __tablename__ = "tags"
    id = Column(INTEGER, primary_key=True)
    tag = Column(VARCHAR(255), nullable=False, unique=True)
    users = relationship(
        "User", secondary=user_tag, back_populates="tags", lazy="joined"
    )


async def main():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:pgs12345@localhost/test",
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    users = [User(name="p1"), User(name="p2"), User(name="p3")]
    tags = [Tag(tag="tag1"), Tag(tag="tag2"), Tag(tag="tag3")]

    async with AsyncSession(engine) as session:
        async with session.begin():
            session.add_all(users)
            session.add_all(tags)

        for user in users:
            await session.refresh(user)
        for tag in tags:
            await session.refresh(tag)

        for user in users:
            for i in range(3, user.id - 1, -1):
                await session.execute(
                    user_tag.insert().values(user_id=user.id, tag_id=i)
                )
        await session.commit()

        for user in users:
            await session.refresh(user)
        for tag in tags:
            await session.refresh(tag)

        tags = await greenlet_spawn(users[0].tags)
        print(tags)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
