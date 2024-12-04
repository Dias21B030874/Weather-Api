from pydantic import BaseModel, Field
from typing import Optional


class CityBase(BaseModel):
    """
    Базовая схема для города.
    """
    city_name: str = Field(..., example="London")
    temperature: float = Field(..., example=15.5)
    weather_description: str = Field(..., example="light rain")
    humidity: int = Field(..., example=80)


class CityCreate(CityBase):
    """
    Схема для создания нового города.
    """
    pass


class City(CityBase):
    """
    Схема города с дополнительным полем 'id'.
    """
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    """
    Базовая схема пользователя.
    """
    username: str = Field(..., example="user@example.com")


class UserCreate(UserBase):
    """
    Схема для создания нового пользователя.
    """
    password: str = Field(..., min_length=6, example="password123")


class User(UserBase):
    """
    Схема пользователя.
    """
    disabled: Optional[bool] = False

    class Config:
        orm_mode = True


class UserInDB(User):
    """
    Схема пользователя с хешированным паролем.
    """
    hashed_password: str


class Token(BaseModel):
    """
    Схема токена авторизации.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Схема данных внутри токена.
    """
    username: Optional[str] = None
