"""Конфігурація підключення до бази даних."""

import os

# DSN для SQLAlchemy/SQLModel (драйвер psycopg 3).
# Дані збігаються з docker-compose.yaml (postgres:postgres@localhost:5432).
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/postgres",
)
