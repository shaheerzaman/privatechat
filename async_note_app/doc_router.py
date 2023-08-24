from fastapi import status, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from db import engine
import doc_crud
from schemas import DocumentIn, DocumentOut
from typing import List
from models import Document, User
import uuid

router = APIRouter()

# create an async session object for CRUD
session: AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)

user = User(id=str(uuid.uuid4()), username="shaheer", hashed_password="shaheer")


@router.get(
    "/documents", response_model=List[DocumentOut], status_code=status.HTTP_200_OK
)
async def get_all_notes():
    """API endpoint for listing all note resources"""
    documents = await doc_crud.get_all(session)
    return documents


@router.post(
    "/documents",
    status_code=status.HTTP_201_CREATED,
    response_model=DocumentOut,
)
async def create_document(doc: DocumentIn):
    # user = User(
    #     id=str(uuid.uuid4()), username="shaheerzaman", hashed_password="shaheer"
    # )
    document = Document(
        id=str(uuid.uuid4()), **doc.model_dump(exclude_none=True), users=[user]
    )
    document = await doc_crud.add(session, document)
    return document


@router.get("/documents/{doc_id}", response_model=DocumentOut)
async def get_document_by_id(doc_id: str):
    document = await doc_crud.get_by_id(session, doc_id)
    return document


@router.put("/documents/{doc_id}", response_model=DocumentOut)
async def update_document(doc_id: str, doc: DocumentIn):
    doc_dict = doc.model_dump(exclude_none=True)
    document = await doc_crud.update(session, doc_id, doc_dict)
    return document


@router.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    doc = await doc_crud.get_by_id(session, doc_id)
    if doc is None:
        raise HTTPException(status_code=400, detail="Document not found")

    await doc_crud.delete(session, doc)

    return {"response": "successfully deleted"}


@router.get("/document_ids/{usename}", response_model=List[str])
async def get_user_document_ids(username: str):
    doc_ids = await doc_crud.get_user_documents(session, username)
    return doc_ids
