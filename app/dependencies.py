from sqlalchemy.orm import Session
from app.database import SessionLocal


def get_db() -> Session:
    """
    Получить сессию базы данных.

    :return: Объект Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
