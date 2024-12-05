import httpx
from typing import Any, Dict, Optional
import os

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

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/weather", params=params)
            response.raise_for_status()  # выбрасывает исключение при 4xx или 5xx ошибках

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Неизвестный статус ответа: {response.status_code}")
                return None

    except httpx.RequestError as e:
        print(f"Ошибка при запросе: {e}")
    except httpx.HTTPStatusError as e:
        print(f"Ошибка HTTP: {e}")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
    return None
