from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
