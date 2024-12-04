from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from app import auth as auth_module


def get_city(db: Session, city_id: int) -> Optional[models.City]:
    """
    Получить город по его ID.
    """
    return db.query(models.City).filter(models.City.id == city_id).first()


def get_city_by_name(db: Session, city_name: str) -> Optional[models.City]:
    """
    Получить город по его названию.
    """
    return db.query(models.City).filter(models.City.city_name.ilike(city_name)).first()


def get_cities(db: Session, skip: int = 0, limit: int = 100) -> List[models.City]:
    """
    Получить список городов с возможностью пропуска и ограничения количества.
    """
    return db.query(models.City).offset(skip).limit(limit).all()


def create_city(db: Session, city: schemas.CityCreate) -> models.City:
    """
    Создать новый город в базе данных.
    """
    db_city = models.City(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int) -> None:
    """
    Удалить город по его ID.
    """
    db_city = get_city(db, city_id)
    if db_city:
        db.delete(db_city)
        db.commit()


# Функции для работы с пользователями
def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """
    Получить пользователя по имени пользователя.
    """
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Создать нового пользователя.
    """
    hashed_password = auth_module.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        disabled=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
