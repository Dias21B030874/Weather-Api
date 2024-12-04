from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.dependencies import get_db
from app.auth import get_current_user, User

router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)

@router.get("/", response_model=List[schemas.City], summary="Получить список всех городов с погодными данными")
def read_cities(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[schemas.City]:
    """
    Получить список всех городов с погодными данными с возможностью пропуска и ограничения количества.

    :param skip: Количество записей для пропуска
    :param limit: Максимальное количество записей для возврата
    :param db: Сессия базы данных
    :return: Список объектов City
    """
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities

@router.get("/{city_id}", response_model=schemas.City, summary="Получить город по ID")
def read_city(
    city_id: int,
    db: Session = Depends(get_db)
) -> schemas.City:
    """
    Получить город по его ID.

    :param city_id: ID города
    :param db: Сессия базы данных
    :return: Объект City
    :raises HTTPException: Если город не найден
    """
    db_city = crud.get_city(db, city_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="Город не найден")
    return db_city

@router.post("/", response_model=schemas.City, summary="Создать новый город с погодными данными", status_code=status.HTTP_201_CREATED)
def create_city_endpoint(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> schemas.City:
    """
    Создать новый город с погодными данными в базе данных. Эндпоинт защищен авторизацией.

    :param city: Данные для создания города
    :param db: Сессия базы данных
    :param current_user: Текущий аутентифицированный пользователь
    :return: Созданный объект City
    :raises HTTPException: Если город уже существует
    """
    db_city = crud.get_city_by_name(db, city_name=city.city_name)
    if db_city:
        raise HTTPException(status_code=400, detail="Город уже существует в базе данных")
    db_city = crud.create_city(db, city)
    return db_city

@router.delete("/{city_id}", summary="Удалить город по ID")
def delete_city_endpoint(
    city_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Удалить город по его ID. Эндпоинт защищен авторизацией.

    :param city_id: ID города для удаления
    :param db: Сессия базы данных
    :param current_user: Текущий аутентифицированный пользователь
    :return: Сообщение об успешном удалении
    :raises HTTPException: Если город не найден
    """
    db_city = crud.get_city(db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="Город не найден")
    crud.delete_city(db, city_id)
    return {"detail": "Город удален"}
