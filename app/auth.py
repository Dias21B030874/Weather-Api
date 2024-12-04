from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app import schemas, crud
from app.dependencies import get_db
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

# Загрузка SECRET_KEY из переменных окружения
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY не установлен в переменных окружения")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Схема OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class User(schemas.User):
    """
    Модель пользователя.
    """
    pass


class UserInDB(schemas.UserInDB):
    """
    Модель пользователя с хешированным паролем.
    """
    pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверить соответствие пароля хешу.

    :param plain_password: Введенный пароль
    :param hashed_password: Хешированный пароль
    :return: True если соответствует, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Получить хеш пароля.

    :param password: Пароль
    :return: Хеш пароля
    """
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str) -> Optional[UserInDB]:
    """
    Аутентифицировать пользователя.

    :param db: Сессия базы данных
    :param username: Имя пользователя
    :param password: Пароль
    :return: Объект UserInDB если аутентификация успешна, иначе None
    """
    user = crud.get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return UserInDB(username=user.username, hashed_password=user.hashed_password, disabled=user.disabled)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создать JWT токен.

    :param data: Данные для включения в токен
    :param expires_delta: Время жизни токена
    :return: Закодированный JWT токен
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Получить текущего пользователя из токена.

    :param token: JWT токен
    :param db: Сессия базы данных
    :return: Объект User
    :raises HTTPException: Если токен некорректен или пользователь не найден
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return schemas.User(username=user.username, disabled=user.disabled)
