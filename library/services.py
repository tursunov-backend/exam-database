from datetime import datetime
from .db import SessionLocal, get_session
from .models import Author, Book, Student, Borrow


def create_author(name: str, bio: str = None) -> Author:
    session = get_session()

    author = Author(name=name, bio=bio)
    session.add(author)
    session.commit()
    session.refresh(author)

    session.close()
    return author


def get_author_by_id(author_id: int) -> Author | None:
    session = get_session()

    author = session.query(Author).filter_by(id=author_id).first()

    session.close()
    return author


def get_all_authors() -> list[Author]:
    session = SessionLocal()

    authors = session.query(Author).all()

    session.close()
    return authors


def update_author(author_id: int, name: str = None, bio: str = None) -> Author | None:
    session = SessionLocal()

    existing_author = session.query(Author).filter_by(id=author_id).first()

    if existing_author:
        if name:
            existing_author.name = name
        if bio:
            existing_author.bio = bio

        session.commit()
        session.refresh(existing_author)

        session.close()
        return existing_author

    session.close()
    return None


def delete_author(author_id: int) -> bool:
    session = SessionLocal()

    existing_author = session.query(Author).filter_by(id=author_id).first()

    if not existing_author:
        session.close()
        return False

    session.delete(existing_author)
    session.commit()

    session.close()
    return True


def create_book(title: str, author_id: int, published_year: int, isbn: str = None) -> Book:
    session = SessionLocal()

    book = Book(
        title=title,
        author_id=author_id,
        published_year=published_year,
        isbn=isbn,
    )

    session.add(book)
    session.commit()
    session.refresh(book)

    session.close()
    return book


def get_book_by_id(book_id: int) -> Book | None:
    session = SessionLocal()

    book = session.query(Book).filter_by(id=book_id).first()

    session.close()
    return book


def get_all_books() -> list[Book]:
    session = SessionLocal()

    books = session.query(Book).all()

    session.close()
    return books


def search_books_by_title(title: str) -> list[Book]:
    session = SessionLocal()

    books = session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

    session.close()
    return books


def delete_book(book_id: int) -> bool:
    session = SessionLocal()

    existing_book = session.query(Book).filter_by(id=book_id).first()

    if not existing_book:
        session.close()
        return False

    session.delete(existing_book)
    session.commit()

    session.close()
    return True


def create_student(full_name: str, email: str, grade: str = None) -> Student:
    session = get_session()

    student = Student(full_name=full_name, email=email, grade=grade)

    session.add(student)
    session.commit()
    session.refresh(student)

    session.close()
    return student


def get_student_by_id(student_id: int) -> Student | None:
    session = SessionLocal()

    student = session.query(Student).filter_by(id=student_id).first()

    session.close()
    return student


def get_all_students() -> list[Student]:
    session = SessionLocal()

    students = session.query(Student).all()

    session.close()
    return students


def update_student_grade(student_id: int, grade: str) -> Student | None:
    session = SessionLocal()

    student = session.get(Student, student_id)

    if not student:
        session.close()
        return None

    student.grade = grade
    session.commit()
    session.refresh(student)

    session.close()
    return student


def borrow_book(student_id: int, book_id: int) -> Borrow | None:
    session = get_session()

    student = session.get(Student, student_id)
    book = session.get(Book, book_id)

    if not student or not book:
        session.close()
        return None

    if not book.is_available:
        session.close()
        return None

    borrow_books = (
        session.query(Borrow)
        .filter(Borrow.student_id == student_id)
        .filter(Borrow.returned_at.is_(None))
        .count()
    )

    if borrow_books >= 3:
        session.close()
        return None

    borrow = Borrow(student_id=student_id, book_id=book_id)
    book.is_available = False

    session.add(borrow)
    session.commit()
    session.refresh(borrow)

    _ = borrow.book
    _ = borrow.student

    session.close()
    return borrow


def return_book(borrow_id: int) -> bool:
    session = get_session()

    borrow = session.query(Borrow).filter(Borrow.id == borrow_id).first()

    if not borrow:
        session.close()
        return False

    if borrow.returned_at:
        session.close()
        return False

    borrow.returned_at = datetime.now()
    borrow.book.is_available = True

    session.commit()

    session.close()
    return True


def get_student_borrow_count(student_id: int) -> int:
    session = get_session()

    count = (
        session.query(Borrow)
        .filter(Borrow.student_id == student_id)
        .filter(Borrow.returned_at.is_(None))
        .count()
    )

    session.close()
    return count


def get_currently_borrowed_books() -> list[tuple[Book, Student, datetime]]:
    session = get_session()

    borrow_records = session.query(Borrow).filter(Borrow.returned_at.is_(None)).all()

    result = [
        (borrow.book, borrow.student, borrow.borrowed_at)
        for borrow in borrow_records
    ]

    session.close()
    return result


def get_books_by_author(author_id: int) -> list[Book]:
    session = get_session()

    author = session.get(Author, author_id)

    if not author:
        session.close()
        return []

    books = author.books

    session.close()
    return books


def get_overdue_borrows() -> list[tuple[Borrow, Student, Book, int]]:
    session = get_session()

    now = datetime.now()

    overdue_records = (
        session.query(Borrow)
        .filter(Borrow.returned_at.is_(None))
        .filter(Borrow.due_date < now)
        .all()
    )

    result = []

    for borrow in overdue_records:
        student = borrow.student
        book = borrow.book
        days_overdue = (now - borrow.due_date).days
        result.append((borrow, student, book, days_overdue))

    session.close()
    return result