from .config import SessionLocal
from .models import Author


def create_author(name: str, bio: str = None) -> Author:
    """Yangi muallif yaratish"""
    db = SessionLocal()

    author = Author(name=name, bio=bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    db.close()

    return author


def get_author_by_id(author_id: int) -> Author | None:
    """ID bo'yicha muallifni olish"""
    db = SessionLocal()

    author = db.query(Author).filter_by(id=author_id).first()
    db.close()

    return author


def get_all_authors() -> list[Author]:
    """Barcha mualliflar ro'yxatini olish"""
    db = SessionLocal()

    authors = db.query(Author).all()
    db.close()

    return authors


def update_author(author_id: int, name: str = None, bio: str = None) -> Author | None:
    """Muallif ma'lumotlarini yangilash"""
    db = SessionLocal()

    existing_author = db.query(Author).filter_by(id=author_id).first()

    if existing_author:
        if name:
            existing_author.name = name
        if bio:
            existing_author.bio = bio

        db.commit()
        db.refresh(existing_author)
        db.close()

        return existing_author

    db.close()
    return Author


def delete_author(author_id: int) -> bool:
    """Muallifni o'chirish"""
    db = SessionLocal()

    existing_author = db.query(Author).filter_by(id=author_id).first()

    if not existing_author:
        db.close()
        return False

    db.delete(existing_author)
    db.commit()
    db.close()

    return True
