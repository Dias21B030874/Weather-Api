from fastapi import APIRouter

from .auth import router as auth_router
from .cities import router as cities_router
from .weather import router as weather_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(cities_router)
api_router.include_router(weather_router)
