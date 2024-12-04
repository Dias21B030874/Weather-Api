import httpx
from typing import Any, Dict, Optional
import os

# Получение API ключа из переменных окружения
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY не установлен в переменных окружения")

BASE_URL = "https://api.openweathermap.org/data/2.5"


async def get_weather(city_name: str, units: str = "metric") -> Optional[Dict[str, Any]]:
    """
    Получить текущую погоду для заданного города из OpenWeatherMap API.

    :param city_name: Название города
    :param units: Единицы измерения (default: "metric")
    :return: Словарь с данными о погоде или None, если город не найден
    :raises httpx.HTTPStatusError: При ошибке запроса
    """
    params = {
        "q": city_name,
        "appid": OPENWEATHER_API_KEY,
        "units": units
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/weather", params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            response.raise_for_status()
