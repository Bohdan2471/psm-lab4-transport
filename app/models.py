"""Доменні моделі (таблиці) предметної області «Автотранспортне підприємство».

Сутності та зв'язки:
  - Vehicle (автомобіль)  1 — N  Trip
  - Driver  (водій)       1 — N  Trip
  - Driver  N — M  Vehicle  (через таблицю допусків DriverVehiclePermit)
"""

from datetime import date

from pydantic import NaiveDatetime
from sqlmodel import Field, SQLModel


class Vehicle(SQLModel, table=True):
    """Автомобіль підприємства."""

    __tablename__ = "vehicles"

    license_plate: str = Field(primary_key=True, max_length=10)
    brand: str = Field(max_length=50)
    tech_condition: str = Field(max_length=30)
    current_location: str | None = Field(default=None, max_length=100)
    avg_speed: int | None = Field(default=None)
    load_capacity: int
    fuel_consumption: float


class Driver(SQLModel, table=True):
    """Водій підприємства."""

    __tablename__ = "drivers"

    driver_id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=100)
    birth_date: date
    experience_years: int
    salary: float
    phone: str = Field(max_length=20)
    email: str = Field(max_length=100)


class Trip(SQLModel, table=True):
    """Рейс: пов'язує автомобіль і водія (зв'язки N:1)."""

    __tablename__ = "trips"

    trip_id: int | None = Field(default=None, primary_key=True)
    license_plate: str = Field(foreign_key="vehicles.license_plate", max_length=10)
    driver_id: int = Field(foreign_key="drivers.driver_id")
    departure_date: NaiveDatetime
    arrival_date: NaiveDatetime | None = Field(default=None)
    destination: str = Field(max_length=100)
    distance: int
    fuel_used: float | None = Field(default=None)
    fuel_type: str = Field(max_length=20)
    cargo_weight: int | None = Field(default=None)


class DriverVehiclePermit(SQLModel, table=True):
    """Допуск водія до керування автомобілем — зв'язок N:M між Driver і Vehicle."""

    __tablename__ = "driver_vehicle_permits"

    id: int | None = Field(default=None, primary_key=True)
    driver_id: int = Field(foreign_key="drivers.driver_id")
    license_plate: str = Field(foreign_key="vehicles.license_plate", max_length=10)
    category: str | None = Field(default=None, max_length=10)
