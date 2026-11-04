"""Схеми вхідних даних (Create/Update) з валідацією regex.

Окремі від таблиць класи потрібні, щоб id/ключі не приходили від клієнта,
а поля з форматом (номер, телефон, email) перевірялися регулярними виразами.
"""

from datetime import date, datetime

from pydantic import BaseModel, field_validator

from app.validators import validate_email, validate_license_plate, validate_phone

# --------------------------- Vehicle ---------------------------------------


class VehicleCreate(BaseModel):
    license_plate: str
    brand: str
    tech_condition: str
    current_location: str | None = None
    avg_speed: int | None = None
    load_capacity: int
    fuel_consumption: float

    @field_validator("license_plate")
    @classmethod
    def _plate(cls, v: str) -> str:
        return validate_license_plate(v)


class VehicleUpdate(BaseModel):
    brand: str
    tech_condition: str
    current_location: str | None = None
    avg_speed: int | None = None
    load_capacity: int
    fuel_consumption: float


# --------------------------- Driver ----------------------------------------


class DriverCreate(BaseModel):
    full_name: str
    birth_date: date
    experience_years: int
    salary: float
    phone: str
    email: str

    @field_validator("phone")
    @classmethod
    def _phone(cls, v: str) -> str:
        return validate_phone(v)

    @field_validator("email")
    @classmethod
    def _email(cls, v: str) -> str:
        return validate_email(v)


class DriverUpdate(DriverCreate):
    pass


# --------------------------- Trip ------------------------------------------


class TripCreate(BaseModel):
    license_plate: str
    driver_id: int
    departure_date: datetime
    arrival_date: datetime | None = None
    destination: str
    distance: int
    fuel_used: float | None = None
    fuel_type: str
    cargo_weight: int | None = None

    @field_validator("license_plate")
    @classmethod
    def _plate(cls, v: str) -> str:
        return validate_license_plate(v)


class TripUpdate(TripCreate):
    pass
