from library.models import Base
from library.config import engine
from library.services import create_author

Base.metadata.create_all(bind=engine)

author = create_author("Ali", "Python muallifi")
