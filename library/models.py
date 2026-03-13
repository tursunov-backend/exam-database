from datetime import datetime, timedelta

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase,
)
from sqlalchemy import (
    TIMESTAMP,
    func,
    Integer,
    String,
    ForeignKey,
    Boolean,
    DateTime,
    Text,
)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    create_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    update_ad: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Author(Base, TimestampMixin):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="authors")


class Book(Base, TimestampMixin):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    published_year: Mapped[int] = mapped_column(Integer)
    isbn: Mapped[str] = mapped_column(String(13), unique=True, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    authors: Mapped["Author"] = relationship("Author", back_populates="books")
    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="books")


class Student(Base, TimestampMixin):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    grade: Mapped[str | None] = mapped_column(String(20), nullable=True)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    borrows: Mapped[list["Borrow"]] = relationship("Borrow", back_populates="students")


class Borrow(Base, TimestampMixin):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    borrowed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    due_date: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now() + timedelta(days=14)
    )

    returned_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    students: Mapped["Student"] = relationship("Student", back_populates="borrows")
    books: Mapped["Book"] = relationship("Book", back_populates="borrows")
