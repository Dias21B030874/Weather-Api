from fastapi import FastAPI
from app.routers import auth, cities, weather

app = FastAPI(
    title="Weather API",
    description="API для работы с погодными данными.",
    version="1.0.0",
)

# Подключаем маршруты
app.include_router(auth.router)
app.include_router(cities.router)
app.include_router(weather.router)
