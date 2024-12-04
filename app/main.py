from fastapi import FastAPI
from sqlalchemy.orm import Session
import os
from app.routers import weather_router

from dotenv import load_dotenv
load_dotenv()  # Загрузка переменных окружения из .env файла

from app.database import engine, Base
from app.routers import api_router
from app.dependencies import get_db
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi.middleware.cors import CORSMiddleware

# Проверка наличия обязательных переменных окружения
SECRET_KEY = os.getenv("SECRET_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY не установлен в переменных окружения")
if not OPENWEATHER_API_KEY:
    raise ValueError("OPENWEATHER_API_KEY не установлен в переменных окружения")

app = FastAPI(
    title="FastAPI OpenWeatherMap Integration",
    description="API для работы с погодными данными с интеграцией OpenWeatherMap, авторизацией и CRUD операциями.",
    version="1.0.0"
)

# Создание таблиц при запуске приложения
Base.metadata.create_all(bind=engine)

# Разрешенные CORS (можно настроить по необходимости)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Включение всех маршрутов
app.include_router(api_router)
app.include_router(weather_router)

@app.on_event("startup")
async def startup_event():
    # Для InMemoryBackend (подходит для разработки)
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")