"""Точка входу REST API «Автотранспортне підприємство» (FastAPI).

Запуск: uv run uvicorn app.main:app --reload
Документація: http://localhost:8000/docs
"""

from fastapi import FastAPI

from app.db import create_db_and_tables
from app.models import Driver, Trip, Vehicle
from app.routers import crud_router
from app.schemas import (
    DriverCreate,
    DriverUpdate,
    TripCreate,
    TripUpdate,
    VehicleCreate,
    VehicleUpdate,
)

app = FastAPI(title="Автотранспортне підприємство — REST API", version="1.0")


@app.on_event("startup")
def on_startup() -> None:
    """Створює таблиці при старті, якщо їх ще немає."""
    create_db_and_tables()


@app.get("/")
def root() -> dict[str, str]:
    """Коротка довідка."""
    return {"service": "Автотранспортне підприємство", "docs": "/docs"}


# Реєстрація ресурсів. Додати новий ресурс = додати ще один виклик crud_router,
# не змінюючи наявні роутери, репозиторій чи моделі (принцип OCP).
app.include_router(
    crud_router(
        prefix="/vehicles",
        tag="vehicles",
        model=Vehicle,
        pk_name="license_plate",
        create_schema=VehicleCreate,
        update_schema=VehicleUpdate,
    )
)
app.include_router(
    crud_router(
        prefix="/drivers",
        tag="drivers",
        model=Driver,
        pk_name="driver_id",
        create_schema=DriverCreate,
        update_schema=DriverUpdate,
    )
)
app.include_router(
    crud_router(
        prefix="/trips",
        tag="trips",
        model=Trip,
        pk_name="trip_id",
        create_schema=TripCreate,
        update_schema=TripUpdate,
    )
)
