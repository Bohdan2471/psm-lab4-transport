"""Ініціалізація бази даних: створення таблиць та вставка тестових даних (50+).

Запуск: uv run python -m scripts.init_db
"""

import random
from datetime import date, datetime, timedelta

from sqlalchemy import text
from sqlmodel import Session

from app.db import create_db_and_tables, engine
from app.models import Driver, DriverVehiclePermit, Trip, Vehicle

BRANDS = ["MAN TGX", "Volvo FH", "Mercedes Actros", "Scania R", "DAF XF", "Renault T"]
CONDITIONS = ["Справний", "Потребує ТО", "На ремонті"]
CITIES = ["Львів", "Київ", "Одеса", "Харків", "Дніпро", "Рівне", "Луцьк", "Тернопіль"]
FUELS = ["Дизель", "Бензин", "Газ"]
SURNAMES = [
    "Коваль",
    "Сидоренко",
    "Мельник",
    "Бойко",
    "Ткаченко",
    "Шевчук",
    "Поліщук",
    "Кравець",
    "Гнатюк",
    "Савченко",
]
NAMES = [
    "Андрій Іванович",
    "Василь Петрович",
    "Дмитро Олексійович",
    "Ігор Богданович",
    "Олег Романович",
    "Тарас Миколайович",
    "Юрій Степанович",
    "Роман Васильович",
]


def plate(i: int) -> str:
    """Генерує номерний знак у форматі BC1234AA."""
    letters = "ABCEHIKMOPTX"
    a, b = random.choice(letters), random.choice(letters)
    c, d = random.choice(letters), random.choice(letters)
    return f"{a}{b}{1000 + i}{c}{d}"


def seed() -> None:
    """Створює таблиці та заповнює їх тестовими даними."""
    random.seed(28)
    create_db_and_tables()

    with Session(engine) as session:
        # Очищення таблиць перед повторним запуском. TRUNCATE ... RESTART IDENTITY
        # скидає й лічильники первинних ключів, тож id щоразу починаються з 1.
        session.exec(
            text(
                "TRUNCATE driver_vehicle_permits, trips, drivers, vehicles RESTART IDENTITY CASCADE"
            )
        )
        session.commit()

        # --- Автомобілі (12) ---
        plates = [plate(i) for i in range(12)]
        for p in plates:
            session.add(
                Vehicle(
                    license_plate=p,
                    brand=random.choice(BRANDS),
                    tech_condition=random.choice(CONDITIONS),
                    current_location=f"м. {random.choice(CITIES)}, гараж №{random.randint(1, 5)}",
                    avg_speed=random.randint(65, 90),
                    load_capacity=random.choice([15000, 18000, 20000, 22000]),
                    fuel_consumption=round(random.uniform(26.0, 32.0), 1),
                )
            )

        # --- Водії (15) ---
        driver_ids = []
        for i in range(15):
            birth = date(random.randint(1975, 2000), random.randint(1, 12), random.randint(1, 28))
            d = Driver(
                full_name=f"{random.choice(SURNAMES)} {random.choice(NAMES)}",
                birth_date=birth,
                experience_years=random.randint(1, 30),
                salary=round(random.uniform(22000, 40000), 2),
                phone=f"+380{random.randint(500000000, 999999999)}",
                email=f"driver{i + 1}@avtopark.ua",
            )
            session.add(d)
            session.commit()
            session.refresh(d)
            driver_ids.append(d.driver_id)

        # --- Рейси (60) ---
        for _ in range(60):
            dep = datetime(
                2026, random.randint(1, 10), random.randint(1, 28), random.randint(6, 20), 0
            )
            session.add(
                Trip(
                    license_plate=random.choice(plates),
                    driver_id=random.choice(driver_ids),
                    departure_date=dep,
                    arrival_date=dep + timedelta(hours=random.randint(2, 48)),
                    destination=f"м. {random.choice(CITIES)}",
                    distance=random.randint(80, 1200),
                    fuel_used=round(random.uniform(30, 350), 1),
                    fuel_type=random.choice(FUELS),
                    cargo_weight=random.randint(2000, 20000),
                )
            )

        # --- Допуски водіїв до авто, N:M (30) ---
        pairs = set()
        while len(pairs) < 30:
            pairs.add((random.choice(driver_ids), random.choice(plates)))
        for did, p in pairs:
            session.add(
                DriverVehiclePermit(
                    driver_id=did, license_plate=p, category=random.choice(["C", "CE"])
                )
            )

        session.commit()

        # Прямий SQL-запит до БД з Python (пункт 6a): підрахунок записів
        total = 0
        for table in ("vehicles", "drivers", "trips", "driver_vehicle_permits"):
            count = session.exec(text(f"SELECT COUNT(*) FROM {table}")).one()[0]  # type: ignore[call-overload]
            print(f"{table:25} : {count} записів")
            total += count
        print(f"{'РАЗОМ':25} : {total} записів")


if __name__ == "__main__":
    seed()
