"""Walidatory danych formularzy."""

import re
from typing import Optional


def validate_not_empty(value: str, field_name: str) -> Optional[str]:
    """Sprawdza, czy wartość nie jest pusta. Zwraca komunikat błędu lub None."""
    if not value or not value.strip():
        return f"Pole '{field_name}' nie może być puste."
    return None


def validate_positive_number(value, field_name: str) -> Optional[str]:
    """Sprawdza, czy wartość jest liczbą dodatnią."""
    try:
        num = float(value)
        if num <= 0:
            return f"Pole '{field_name}' musi być większe od 0."
    except (ValueError, TypeError):
        return f"Pole '{field_name}' musi być liczbą."
    return None


def validate_non_negative(value, field_name: str) -> Optional[str]:
    """Sprawdza, czy wartość jest liczbą nieujemną."""
    try:
        num = float(value)
        if num < 0:
            return f"Pole '{field_name}' nie może być ujemne."
    except (ValueError, TypeError):
        return f"Pole '{field_name}' musi być liczbą."
    return None


def validate_integer(value, field_name: str) -> Optional[str]:
    """Sprawdza, czy wartość jest liczbą całkowitą."""
    try:
        int(value)
    except (ValueError, TypeError):
        return f"Pole '{field_name}' musi być liczbą całkowitą."
    return None


def validate_positive_integer(value, field_name: str) -> Optional[str]:
    """Sprawdza, czy wartość jest dodatnią liczbą całkowitą."""
    try:
        num = int(value)
        if num <= 0:
            return f"Pole '{field_name}' musi być większe od 0."
    except (ValueError, TypeError):
        return f"Pole '{field_name}' musi być dodatnią liczbą całkowitą."
    return None


def validate_email(value: str) -> Optional[str]:
    """Sprawdza format e-maila, jeśli podany."""
    if not value or not value.strip():
        return None
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, value.strip()):
        return "Podany adres e-mail ma niepoprawny format."
    return None


def validate_phone(value: str) -> Optional[str]:
    """Sprawdza format telefonu, jeśli podany."""
    if not value or not value.strip():
        return None
    cleaned = re.sub(r"[\s\-\(\)\+]", "", value.strip())
    if not cleaned.isdigit() or len(cleaned) < 7:
        return "Podany numer telefonu ma niepoprawny format."
    return None
