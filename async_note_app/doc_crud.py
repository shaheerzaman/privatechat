from models import Document
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from schemas import DocumentIn


async def get_all(async_session: AsyncSession):
    async with async_session() as session:
        statement = (
            select(Document).order_by(Document.id).options(selectinload(Document.users))
        )
        result = await session.execute(statement)
        return result.scalars()


async def add(asyn_session: AsyncSession, document: Document):
    async with asyn_session() as session:
        session.add(document)
        await session.commit()

    return document


async def get_by_id(async_session: AsyncSession, document_id: str):
    async with async_session() as session:
        statement = (
            select(Document)
            .options(selectinload(Document.users))
            .filter(Document.id == document_id)
        )
        result = await session.execute(statement)
        return result.scalars().one()


async def update(async_session: AsyncSession, document_id: str, doc_dict: dict):
    async with async_session() as session:
        document = await get_by_id(async_session, document_id)
        for key, val in doc_dict.items():
            setattr(document, key, val)
        await session.commit()
        return document


async def delete(async_session: AsyncSession, doc: Document):
    async with async_session() as session:
        await session.delete(doc)
        await session.commit()
