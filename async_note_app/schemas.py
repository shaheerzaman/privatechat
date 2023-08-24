from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List


# schema for returning a note
class NoteModel(BaseModel):
    id: str
    title: str
    content: str
    date_created: datetime

    model_config = ConfigDict(from_attributes=True)


# schema for creating a note
class NoteCreateModel(BaseModel):
    title: str
    content: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"title": "Sample title", "content": "Sample content"}
        },
    )


class DocumentIn(BaseModel):
    title: str
    content: str
    doc_type: Optional[str] = None
    doc_source: Optional[str] = None


class DocumentBase(BaseModel):
    id: str
    title: str
    content: str
    doc_type: str
    doc_source: str
    created_at: datetime

    class Cofing:
        orm_mode = True


class UserIn(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    id: str
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class DocumentOut(DocumentBase):
    users: Optional[List[UserBase]] = []


class UserOut(UserBase):
    documents: Optional[List[DocumentBase]] = []
