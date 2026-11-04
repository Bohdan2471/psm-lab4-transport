"""Валідація вхідних даних за допомогою регулярних виразів (regex)."""

import re

# Український номерний знак: дві літери, чотири цифри, дві літери (напр. BC1234AA)
LICENSE_PLATE_RE = re.compile(r"^[A-ZА-ЯІЇЄ]{2}\d{4}[A-ZА-ЯІЇЄ]{2}$")
# Телефон у форматі +380XXXXXXXXX
PHONE_RE = re.compile(r"^\+380\d{9}$")
# Email
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_license_plate(value: str) -> str:
    """Перевіряє номерний знак; повертає значення або кидає ValueError."""
    if not LICENSE_PLATE_RE.match(value):
        raise ValueError("Номерний знак має бути у форматі BC1234AA")
    return value


def validate_phone(value: str) -> str:
    """Перевіряє телефон у форматі +380XXXXXXXXX."""
    if not PHONE_RE.match(value):
        raise ValueError("Телефон має бути у форматі +380XXXXXXXXX")
    return value


def validate_email(value: str) -> str:
    """Перевіряє коректність email."""
    if not EMAIL_RE.match(value):
        raise ValueError("Некоректний email")
    return value
