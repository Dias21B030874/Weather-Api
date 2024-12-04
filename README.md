# FastAPI OpenWeatherMap Integration

## Описание

FastAPI приложение для работы с погодными данными с интеграцией внешнего API OpenWeatherMap. Включает JWT авторизацию, CRUD операции и деплой на бесплатный хостинг.
https://weather-api-production-072b.up.railway.app/docs

## Функционал

- Интеграция с OpenWeatherMap API
- CRUD операции для городов и их погодных данных
- JWT авторизация
- Документация API с использованием Swagger
- Кэширование данных
- Контейнеризация с Docker и Docker Compose

## Установка

### Предварительные требования

- Python 3.7+
- Docker и Docker Compose (для контейнеризации)
- Git

### Шаги

1. **Клонировать репозиторий**

    ```bash
    git clone...
    cd...
    ```

2. **Создать и активировать виртуальное окружение**

    ```bash
    python3 -m venv venv
    source venv\Scripts\activate
    ```

3. **Установить зависимости**

    ```bash
    pip install -r requirements.txt
    ```

4. **Настроить переменные окружения**

    Создайте файл `.env` в корне проекта и добавьте следующие переменные:

    ```
    SECRET_KEY=
    OPENWEATHER_API_KEY=
    ```

5. **Запустить приложение локально**

    ```bash
    uvicorn app.main:app --reload
    ```

6. **Доступ к документации API**

    Перейдите по адресу `http://127.0.0.1:8000/docs` для просмотра Swagger UI.

## API Эндпоинты

### Аутентификация

- **POST /auth/token**: Получить JWT токен.

    **Параметры формы:**

    - `user`: string
    - `password`: string 

    **Пример запроса:**

    ```bash
    curl -X POST "http://127.0.0.1:8000/auth/token" -d "username=user@example.com&password=password123"
    ```

    **Пример ответа:**

    ```json
    {
      "access_token": "your_jwt_token",
      "token_type": "bearer"
    }
    ```

### Города

- **GET /cities/**: Получить список всех городов с погодными данными.

    **Пример запроса:**

    ```bash
    curl -X GET "http://127.0.0.1:8000/cities/"
    ```

    **Пример ответа:**

    ```json
    [
      {
        "id": 1,
        "city_name": "New York",
        "temperature": 20.5,
        "weather_description": "clear sky",
        "humidity": 60
      },
      ...
    ]
    ```

- **GET /cities/{city_id}**: Получить город по его ID.

    **Пример запроса:**

    ```bash
    curl -X GET "http://127.0.0.1:8000/cities/1"
    ```

    **Пример ответа:**

    ```json
    {
      "id": 1,
      "city_name": "New York",
      "temperature": 20.5,
      "weather_description": "clear sky",
      "humidity": 60
    }
    ```

- **POST /cities/**: Создать новый город с погодными данными. Требуется авторизация.

    **Заголовок:**

    ```
    Authorization: Bearer your_jwt_token
    ```

    **Тело запроса:**

    ```json
    {
      "city_name": "London",
      "temperature": 15.5,
      "weather_description": "light rain",
      "humidity": 80
    }
    ```

    **Пример ответа:**

    ```json
    {
      "id": 2,
      "city_name": "London",
      "temperature": 15.5,
      "weather_description": "light rain",
      "humidity": 80
    }
    ```

- **DELETE /cities/{city_id}**: Удалить город по его ID. Требуется авторизация.

    **Заголовок:**

    ```
    Authorization: Bearer your_jwt_token
    ```

    **Пример запроса:**

    ```bash
    curl -X DELETE "http://127.0.0.1:8000/cities/1" -H "Authorization: Bearer your_jwt_token"
    ```

    **Пример ответа:**

    ```json
    {
      "detail": "Город удален"
    }
    ```

- **POST /cities/fetch-and-save/{city_name}**: Получить погодные данные города из OpenWeatherMap и сохранить в базу данных.

    **Пример запроса:**

    ```bash
    curl -X POST "http://127.0.0.1:8000/cities/fetch-and-save/London"
    ```

    **Пример ответа:**

    ```json
    {
      "id": 3,
      "city_name": "London",
      "temperature": 15.5,
      "weather_description": "light rain",
      "humidity": 80
    }
    ```

### Тестовый Эндпоинт

- **GET /weather/test**: Тестовый эндпоинт для получения погодных данных города из OpenWeatherMap.

    **Параметры запроса:**

    - `city_name`: Название города (например, `London`)

    **Пример запроса:**

    ```bash
    curl -X GET "http://127.0.0.1:8000/weather/test?city_name=London"
    ```

    **Пример ответа:**

    ```json
    {
      "id": 0,
      "city_name": "London",
      "temperature": 15.5,
      "weather_description": "light rain",
      "humidity": 80
    }
    ```
