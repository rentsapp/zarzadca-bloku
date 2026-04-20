"""Konfiguracja aplikacji Zarządca Bloku."""

import os

APP_NAME = "Zarządca Bloku"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "System Zarządzania Budynkiem Mieszkalnym"

# Ścieżka do bazy danych SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "zarzadca_bloku.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Domyślne ustawienia okna
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 1024
WINDOW_MIN_HEIGHT = 700
