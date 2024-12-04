from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud, services
from app.dependencies import get_db

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
    weather_data = await services.openweather_service.get_weather(city_name)
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
