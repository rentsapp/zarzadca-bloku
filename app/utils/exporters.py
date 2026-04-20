"""Eksport danych do CSV."""

import csv
import os
from typing import Any


def export_to_csv(filepath: str, headers: list[str], rows: list[list[Any]]) -> str:
    """Eksportuje dane do pliku CSV. Zwraca ścieżkę do pliku."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(headers)
        writer.writerows(rows)
    return filepath
