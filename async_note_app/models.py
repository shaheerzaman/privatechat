from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Table, ForeignKey, Column, String
from datetime import datetime
from db import Base


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    date_created: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Note {self.title} at {self.date_created}>"


doc_user = Table(
    "doc_user",
    Base.metadata,
    Column("user_id", String, ForeignKey("users.id"), primary_key=True),
    Column("doc_id", String, ForeignKey("documents.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    documents = relationship(
        "Document", secondary="doc_user", back_populates="users", lazy="joined"
    )


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    doc_type: Mapped[str] = mapped_column(default="text")
    doc_source: Mapped[str] = mapped_column(default="enterprise")
    users = relationship(
        "User", secondary="doc_user", back_populates="documents", lazy="joined"
    )
