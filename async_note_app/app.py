from fastapi import FastAPI, status
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from db import engine
import crud
from schemas import NoteModel, NoteCreateModel
from http import HTTPStatus
from typing import List
from models import Note
import uuid
from doc_router import router

app = FastAPI(
    title="Noted API", description="This is a simple note taking service", docs_url="/"
)
app.include_router(router)
# create an async session object for CRUD
session: AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)


@app.get("/notes", response_model=List[NoteModel])
async def get_all_notes():
    """API endpoint for listing all note resources"""
    notes = await crud.get_all(session)

    return notes


@app.post("/notes", status_code=HTTPStatus.CREATED, response_model=NoteCreateModel)
async def create_note(note_data: NoteCreateModel):
    new_note = Note(
        id=str(uuid.uuid4()), title=note_data.title, content=note_data.content
    )

    note = await crud.add(session, new_note)

    return note


@app.get("/note/{note_id}")
async def get_note_by_id(note_id):
    """API endpoint for retrieving a note by its ID

    Args:
        note_id (str): the ID of the note to retrieve

    Returns:
        dict: The retrieved note
    """
    note = await crud.get_by_id(session, note_id)

    return note


@app.put("/note/{note_id}")
async def update_note(note_id: str, data: NoteCreateModel):
    note = await crud.update(session, note_id, data=data)

    return note


@app.delete("/note/{note_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_note(note_id):
    """Delete note by id

    Args:
        note_id (str): ID of note to delete

    """
    note = await crud.get_by_id(session, note_id)

    result = await crud.delete(session, note)

    return result
