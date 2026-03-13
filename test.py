# test.py
from library.services import (
    create_author,
    create_book,
    create_student,
    borrow_book,
    return_book,
    get_student_borrow_count,
    get_currently_borrowed_books,
    get_overdue_borrows,
)

from library.models import Base
from library.db import engine

Base.metadata.create_all(bind=engine)


def main():
    print("=== Demo Data Test ===")

    # Muallif yaratish
    author1 = create_author("J.K. Rowling", "Famous fantasy author")
    author2 = create_author("George Orwell", "Dystopian fiction author")
    author3 = create_author("Abdulla Qodiriy", "O'zbek yozuvchi")
    author4 = create_author("Cho'lpon", "Shoir")
    author5 = create_author("Ernest Hemingway", "American author")
    print(
        f"Created Authors: {author1.name}, {author2.name}, {author3.name}, {author4.name}, {author5.name}"
    )

    # Kitoblar yaratish
    book1 = create_book("Harry Potter 1", author1.id, 1997)
    book2 = create_book("Harry Potter 2", author1.id, 1998)
    book3 = create_book("1984", author2.id, 1949)
    book4 = create_book("O'tkan kunlar", author3.id, 1926)
    book5 = create_book("The Old Man and the Sea", author5.id, 1952)
    print(
        f"Created Books: {book1.title}, {book2.title}, {book3.title}, {book4.title}, {book5.title}"
    )

    # Talabalar yaratish
    student1 = create_student("Alice Smith", "alice@example.com", "10th")
    student2 = create_student("Bob Johnson", "bob@example.com", "11th")
    student3 = create_student("Ali", "ali@gmail.com", "10-A")
    student4 = create_student("Vali", "vali@gmail.com", "11-B")
    student5 = create_student("Bek", "bek@gmail.com", "9-A")
    print(
        f"Created Students: {student1.full_name}, {student2.full_name}, {student3.full_name}, {student4.full_name}, {student5.full_name}"
    )

    # Kitob berish
    borrow1 = borrow_book(student1.id, book1.id)
    borrow2 = borrow_book(student2.id, book2.id)
    borrow3 = borrow_book(student3.id, book3.id)
    borrow4 = borrow_book(student4.id, book4.id)
    borrow5 = borrow_book(student5.id, book5.id)

    print(f"{student1.full_name} borrowed: {borrow1.book.title}")
    print(f"{student2.full_name} borrowed: {borrow2.book.title}")
    print(f"{student3.full_name} borrowed: {borrow3.book.title}")
    print(f"{student4.full_name} borrowed: {borrow4.book.title}")
    print(f"{student5.full_name} borrowed: {borrow5.book.title}")

    # Talabaning olgan kitoblari soni
    print(
        f"{student1.full_name} currently has {get_student_borrow_count(student1.id)} books borrowed"
    )
    print(
        f"{student2.full_name} currently has {get_student_borrow_count(student2.id)} books borrowed"
    )
    print(
        f"{student3.full_name} currently has {get_student_borrow_count(student3.id)} books borrowed"
    )
    print(
        f"{student4.full_name} currently has {get_student_borrow_count(student4.id)} books borrowed"
    )
    print(
        f"{student5.full_name} currently has {get_student_borrow_count(student5.id)} books borrowed"
    )

    # Hozirda band bo'lgan kitoblar
    borrowed_books = get_currently_borrowed_books()
    print("Currently borrowed books:")
    for book, student, borrowed_at in borrowed_books:
        print(f"- {book.title} borrowed by {student.full_name} at {borrowed_at}")

    # Kitobni qaytarish
    return_book(borrow1.id)
    print(f"{borrow1.book.title} returned by {student1.full_name}")

    # Kechikkan kitoblar
    overdue = get_overdue_borrows()
    print("Overdue borrows:")
    for borrow, student, book, days_overdue in overdue:
        print(
            f"- {book.title} borrowed by {student.full_name}, overdue by {days_overdue} days"
        )


if __name__ == "__main__":
    main()
