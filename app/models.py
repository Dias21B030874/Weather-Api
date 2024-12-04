from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class City(Base):
    """
    Модель для таблицы 'cities' в базе данных.
    Хранит информацию о городах и их погодных данных.
    """
    __tablename__ = "cities"

    id: int = Column(Integer, primary_key=True, index=True)
    city_name: str = Column(String, unique=True, index=True, nullable=False)
    temperature: float = Column(Float, nullable=False)
    weather_description: str = Column(String, nullable=False)
    humidity: int = Column(Integer, nullable=False)


class User(Base):
    """
    Модель для таблицы 'users' в базе данных.
    Хранит информацию о пользователях.
    """
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    disabled: bool = Column(Boolean, default=False)
