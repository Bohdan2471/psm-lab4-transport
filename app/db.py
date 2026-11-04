"""Підключення до бази даних: engine та сесії SQLModel."""

from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    """Створює всі таблиці, описані в моделях SQLModel (якщо їх ще немає)."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Залежність FastAPI: відкриває сесію БД на час обробки запиту."""
    with Session(engine) as session:
        yield session
