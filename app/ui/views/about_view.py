"""Informacje o programie i instrukcja."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt

from app.config import APP_NAME, APP_VERSION


class AboutView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        title = QLabel(APP_NAME)
        title.setStyleSheet("font-size: 32px; font-weight: 800; color: #2e7d32;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        version = QLabel(f"Wersja: {APP_VERSION}")
        version.setStyleSheet("font-size: 14px; color: #757575; margin-bottom: 20px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version)

        card = QFrame()
        card.setStyleSheet("background-color: white; border: 1px solid #e0e0e0; border-radius: 14px;")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)

        desc = QLabel(
            "<b>System Zarządzania Budynkiem Mieszkalnym</b> to lokalna aplikacja desktopowa "
            "służąca do kompleksowej ewidencji danych i obsługi administracyjnej pojedynczego bloku mieszkalnego.<br><br>"
            "Główne funkcjonalności:<br>"
            "<ul>"
            "<li>Ewidencja mieszkań i ich parametrów</li>"
            "<li>Rejestr właścicieli, lokatorów i najemców</li>"
            "<li>Rozliczanie płatności i ewidencja zaległości</li>"
            "<li>Zarządzanie usterkami i zgłoszeniami z priorytetami</li>"
            "<li>Interaktywna wizualizacja siatki budynku</li>"
            "<li>Generowanie raportów i eksport danych do CSV</li>"
            "</ul><br>"
            "Projekt zrealizowany jako praktyczna aplikacja zaliczeniowa z przedmiotu <i>Python</i>.<br>"
            "Wykorzystuje Python 3, framework PySide6 (Qt) oraz relacyjną bazę danych SQLite obsługiwaną przez SQLAlchemy ORM."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 14px; color: #334155; line-height: 1.6;")
        card_layout.addWidget(desc)

        layout.addWidget(card)
        layout.addStretch()
