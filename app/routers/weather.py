from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud, services
from app.dependencies import get_db
from app.services.openweather_service import get_weather

router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


@router.get("/test", response_model=schemas.City, summary="Тестовый эндпоинт для получения погодных данных города")
async def test_weather(city_name: str, db: Session = Depends(get_db)) -> schemas.City:
    """
    Тестовый эндпоинт для проверки интеграции с внешним API OpenWeatherMap.
    Возвращает погодные данные для указанного города.

    :param city_name: Название города
    :param db: Сессия базы данных
    :return: Объект City с погодными данными
    :raises HTTPException: Если город не найден во внешнем API
    """
    weather_data = await get_weather(city_name)  # Используем функцию get_weather
    if not weather_data:
        raise HTTPException(status_code=404, detail="Город не найден во внешнем API")

    city = schemas.City(
        id=0,  # В тестовом эндпоинте ID не используется
        city_name=weather_data["name"],
        temperature=weather_data["main"]["temp"],
        weather_description=weather_data["weather"][0]["description"],
        humidity=weather_data["main"]["humidity"]
    )
    return city


@router.get("/{city_name}", response_model=schemas.City, summary="Получить данные о городе с погодой")
async def get_weather_for_city(city_name: str, db: Session = Depends(get_db)) -> schemas.City:
    """
    Получить данные о городе с погодой.
    Сначала ищем город в базе данных, если его нет, запрашиваем погоду из внешнего API и сохраняем город в БД.

    :param city_name: Название города
    :param db: Сессия базы данных
    :return: Данные о городе с погодой
    :raises HTTPException: Если город не найден ни в базе данных, ни во внешнем API
    """
    # Ищем город в базе данных
    city = crud.get_city_by_name(db=db, city_name=city_name)

    if city:
        # Если город найден в базе, возвращаем его данные
        return city

    # Если города нет в базе, получаем данные с внешнего API
    weather_data = await services.openweather_service.get_weather(city_name)

    if not weather_data:
        raise HTTPException(status_code=404, detail="Город не найден во внешнем API")

    # Создаем объект города с данными из внешнего API с использованием CityCreate
    city_create = schemas.CityCreate(
        city_name=weather_data["name"],
        temperature=weather_data["main"]["temp"],
        weather_description=weather_data["weather"][0]["description"],
        humidity=weather_data["main"]["humidity"]
    )

    # Сохраняем новый город в базу данных
    city = crud.create_city(db=db, city=city_create)

    return city