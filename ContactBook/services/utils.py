import re

from ContactBook.database.database import SessionLocal, engine
from ContactBook.models import models


def create_database():
    return models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check_email(email: str):
    return True if re.fullmatch(email_regex, email) else False
