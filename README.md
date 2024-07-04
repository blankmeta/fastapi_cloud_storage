# Облачное хранилище

Файловое хранилище, которое позволяет хранить различные типы файлов — документы, фотографии, другие данные.

## Запуск:

- В директории ```./infra``` поднять контейнеры:

```console
docker-compose up -d --build
```
### При первом запуске:
- Создать и применить миграции:
```console
alembic revision --autogenerate -m "init"
```
```console
alembic upgrade head
```


## Тестирование

Запустите базу на порту 6000
```
docker run \
  --rm \
  --name postgres-fastapi-test \
  -p 6000:6000 \
  -e POSTGRES_USER=postgres \
  -e PGPORT=6000 \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=collection \
  -d postgres:14.5
```

В корневой директории запустите тесты ```pytest -v```


## Переменные окружения

Шаблон наполнения файла .env в директории /infra/

```
APP_TITLE="FileUploader"
DATABASE_DSN=postgresql+asyncpg://postgres:postgres@db:5432/postgres
SECRET=0a09cdf4fdd932dd05da33ab532e90a60b20e681364224fa8f4097de52e98d8a
FILES_DIR=files
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД

```
Или в файле ```/infra/.env.example```
