"""
Główny punkt startowy aplikacji Zarządca Bloku.
Inicjalizuje bazę danych, ładuje dane demonstracyjne i uruchamia GUI (PySide6).
"""

import sys
import os
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QIcon

from app.database import init_db, get_session
from app.utils.seed_data import seed_database
from app.ui.main_window import MainWindow
from app.ui.styles import MAIN_STYLE


def handle_exception(exc_type, exc_value, exc_traceback):
    """Globalny handler nieobsłużonych błędów zabezpieczający przed crashem."""
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"KRYTYCZNY BŁĄD:\n{error_msg}")
    
    # Próbujemy pokazać okno z błędem (może się nie udać, jeśli GUI padło całkowicie)
    if QApplication.instance():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Błąd krytyczny aplikacji")
        msg.setText("Wystąpił nieoczekiwany błąd. Aplikacja musi zostać zamknięta.")
        msg.setDetailedText(error_msg)
        msg.exec()
    
    sys.exit(1)


def main():
    # Ustawienie globalnego handlera błędów
    sys.excepthook = handle_exception
    
    # 1. Inicjalizacja bazy danych (SQLite) z obsługą modeli SQLAlchemy
    print("Inicjalizacja bazy danych...")
    init_db()

    # 2. Utworzenie środowiska PyQt / PySide6
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Czysty, nowoczesny styl bazowy
    app.setStyleSheet(MAIN_STYLE)

    # 3. Wypełnienie bazy danymi demonstracyjnymi (jeśli wymagane - seed data)
    print("Sprawdzanie danych demonstracyjnych...")
    session = get_session()
    try:
        seed_database(session)
    except Exception as e:
        print(f"Błąd podczas ładowania danych startowych: {e}")
        session.rollback()
    finally:
        session.close()

    # 4. Uruchomienie głównego okna aplikacji
    print("Uruchamianie GUI...")
    window = MainWindow()
    window.show()

    # Pętla zdarzeń
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
