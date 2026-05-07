# Ads Service (FastAPI)

Сервис объявлений купли/продажи на FastAPI и PostgreSQL.

## Стек
- Python 3.11
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Docker / Docker Compose

## Запуск

1. Клонируйте репозиторий и перейдите в папку проекта:

   cd webpy-134-fastapi-1

2. Запустите контейнеры:

   docker-compose up --build -d

3. Откройте Swagger UI в браузере:

   http://localhost:8000/docs

## Проверка работы (Client Script)

Для проверки всех методов API (Create, Read, Update, Delete, Search) запустите скрипт-клиент:

1. Убедитесь, что установлен httpx:

   pip install httpx

2. Запустите тестовый клиент:

   python test_client.py

Скрипт последовательно создаст, обновит, найдет и удалит тестовое объявление, выведя результаты в консоль.

## Структура проекта

app/ — исходный код приложения

app.py — роуты и логика API

models.py — модели базы данных (SQLAlchemy)

schemas.py — схемы валидации данных (Pydantic)

services.py — бизнес-логика работы с БД

database.py — настройка подключения к БД

lifespan.py — создание таблиц при старте

config.py — конфигурация из .env

docker-compose.yml — оркестрация сервисов

Dockerfile — образ приложения

test_client.py — скрипт для проверки API

.env — переменные окружения 

## Переменные окружения

Создайте файл `.env` в корне проекта:

POSTGRES_USER=postgres

POSTGRES_PASSWORD=postgres

POSTGRES_DB=ads_db

POSTGRES_HOST=localhost

POSTGRES_PORT=5432

Все переменные уже настроены для работы с Docker.

