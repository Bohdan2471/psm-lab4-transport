# Лабораторна робота №4 — Автотранспортне підприємство (REST API)

REST API для предметної області «Автотранспортне підприємство» (варіант 28) з
дисципліни «Програмування скриптовими мовами».

## Стек технологій
- **Python 3.12** + **uv** (менеджер пакетів)
- **PostgreSQL 18** у **Docker**
- **FastAPI** — веб-фреймворк (REST API)
- **SQLModel** (SQLAlchemy + psycopg) — ORM
- **Ruff** + **Mypy** — лінтер і перевірка типів (CI на GitHub Actions)

## Структура
```
app/
  config.py       рядок підключення до БД (DSN)
  db.py           engine, сесії, створення таблиць
  models.py       таблиці: Vehicle, Driver, Trip, DriverVehiclePermit
  validators.py   regex-валідація (email, телефон, номерний знак)
  schemas.py      схеми вхідних даних Create/Update
  repository.py   абстракція Repository + реалізація для SQL (OCP)
  routers.py      фабрика CRUD-ендпоінтів
  main.py         точка входу FastAPI
scripts/init_db.py   створення таблиць + 117 тестових записів
docker-compose.yaml  контейнер PostgreSQL
```

## Сутності та зв'язки
- `vehicles` 1 — N `trips` (автомобіль виконує багато рейсів)
- `drivers` 1 — N `trips` (водій керує багатьма рейсами)
- `drivers` N — M `vehicles` через `driver_vehicle_permits` (допуски)

## Запуск
```bash
# 1. База даних
docker compose up -d

# 2. Залежності
uv sync

# 3. Ініціалізація БД тестовими даними
uv run python -m scripts.init_db

# 4. Веб-сервер
uv run uvicorn app.main:app --reload
```
Документація API: http://localhost:8000/docs

## REST API
Для кожного ресурсу (`/vehicles`, `/drivers`, `/trips`):

| Метод | Шлях | Дія |
|-------|------|-----|
| GET | `/{resource}` | список записів |
| GET | `/{resource}/{id}` | один запис |
| POST | `/{resource}` | створення |
| PUT | `/{resource}/{id}` | оновлення |
| DELETE | `/{resource}/{id}` | видалення |

## Перевірка якості коду
```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy app
```
