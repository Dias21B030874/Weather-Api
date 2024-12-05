from fastapi import FastAPI, APIRouter
from app.routers import auth, cities, weather

api_router = APIRouter()

# Подключаем маршруты
api_router.include_router(auth.router)
api_router.include_router(cities.router)
api_router.include_router(weather.router)
