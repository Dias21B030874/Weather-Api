from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL базы данных.
DATABASE_URL = "sqlite:///./test.db"

# Создание движка SQLAlchemy
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создание сессии
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False
)

# Базовый класс для моделей
Base = declarative_base()
