from library.models import Base
from library.config import engine
from library.services import create_author

from library.services import create_book, get_all_books

Base.metadata.create_all(bind=engine)

author = create_author("Ali", "Python muallifi")

book = create_book("Python", 1, 2024, "1234567890123")

books = get_all_books()

for b in books:
    print(b.title)
