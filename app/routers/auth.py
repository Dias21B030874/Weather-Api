from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app import schemas, auth as auth_module, crud
from app.dependencies import get_db
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/token", response_model=schemas.Token, summary="Получить токен авторизации")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> schemas.Token:
    """
    Аутентификация пользователя и получение JWT токена.

    :param form_data: Данные формы с именем пользователя и паролем
    :param db: Сессия базы данных
    :return: Токен авторизации
    :raises HTTPException: Если аутентификация не удалась
    """
    user = auth_module.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверное имя пользователя или пароль"
        )
    access_token_expires = timedelta(minutes=auth_module.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_module.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
