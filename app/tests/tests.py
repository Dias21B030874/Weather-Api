import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base
from app.dependencies import get_db
import app.models
from dotenv import load_dotenv

load_dotenv()

# Создаем тестовую базу данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Создаем все таблицы
Base.metadata.create_all(bind=engine)


# Переопределяем зависимость для тестов
def override_get_db():
    """
    Переопределение зависимости get_db для тестирования.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Подключаем переопределенную зависимость
app.dependency_overrides[get_db] = override_get_db


@pytest.mark.asyncio
async def test_read_main():
    """
    Тестирование тестового эндпоинта /weather/test.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/weather/test", params={"city_name": "London"})
    assert response.status_code == 200
    data = response.json()
    assert data["city_name"] == "London"
    assert "temperature" in data
    assert "weather_description" in data
    assert "humidity" in data


@pytest.mark.asyncio
async def test_create_city_unauthorized():
    """
    Тестирование создания города без авторизации.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/cities/", json={
            "city_name": "New York",
            "temperature": 20.5,
            "weather_description": "clear sky",
            "humidity": 60
        })
    assert response.status_code == 401  # Unauthorized
