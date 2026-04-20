# Zarządca Bloku
Kompletny, lokalny program desktopowy do administracji i zarządzania budynkiem mieszkalnym (blokiem). Aplikacja stworzona jako zaliczeniowy projekt studencki. 

Program zapewnia intuicyjny graficzny interfejs użytkownika (GUI) z nowoczesnym panelem nawigacyjnym, kompleksowym podsumowaniem danych (Dashboard), wbudowaną bazą danych oraz zestawem narzędzi raportujących.

---

# Główne funkcjonalności

1. Dashboard – ekran podsumowujący kluczowe wskaźniki (wolne/zajęte mieszkania, zaległości, usterki, najnowsze wpłaty).
2. Mieszkania – dodawanie, edycja i usuwanie mieszkań z ewidencją metrażu, statusu i czynszu.
3. Rolowanie Lokatorów – rejestr właścicieli, najemców, przypisywanie ich do poszczególnych mieszkań z datą wprowadzenia.
4. Rozliczenia – dodawanie płatności (czynsz, media), oznaczanie jako opłacone, śledzenie salda i zadłużeń.
5. Rejestr Usterek – zgłaszanie problemów w częściach wspólnych lub mieszkaniach, nadawanie celów i priorytetów.
6. Wizualizacja Budynku – graficzne zestawienie pięter i klatek ze statusami kolorystycznymi mieszkań.
7. Eksport do CSV – zapis wszystkich zestawień i zaległości do arkusza kalkulacyjnego w formacie obsługiwanym np. przez Excel.

---

# Technologie

- Python 3.11+
- PySide6 (Qt for Python) – do budowy profesjonalnego GUI
- SQLAlchemy 2.0+ – warstwa ORM do integracji z bazą danych
- SQLite – lekka i bezobsługowa lokalna baza danych

---

# Struktura katalogów

```text
PROGRAM DO ZARZADZANIA/
│
├── main.py                   # Główny plik startowy aplikacji
├── requirements.txt          # Zależności projektu
├── README.md                 # Dokumentacja, którą m.in. czytasz
├── zarzadca_bloku.db         # Lokalnie generowana baza SQLite
│
└── app/                      # Kod źródłowy aplikacji
    ├── __init__.py
    ├── config.py             # Globalna konfiguracja, stałe
    ├── database.py           # Narzędzia instalacji i logowania do bazy (engine)
    ├── enums.py              # Statusy i opcje wyboru w bazie i interfejsie
    │
    ├── models/               # Tabele bazy - schemat ORM
    │   ├── building.py, apartment.py, person.py, payment.py, issue.py, ...
    │
    ├── services/             # Rozszerzona logika CRUD + obliczenia dla dashboardu
    │
    ├── ui/                   # Warstwa wizualna i PyQt
    │   ├── main_window.py    # Kontener główny, okno i nawigacja boczna
    │   ├── styles.py         # Formaty i kolory (QSS - Qt Style Sheets)
    │   ├── views/            # Główne zakładowe panele robocze
    │   └── dialogs/          # Wyskakujące formularze dodawania/edycji
    │
    └── utils/                # Walidatory, Exportery i Seed Data
        └── seed_data.py      # Zestaw przykładowych "żywych" danych na pierwszy start
```

---

# Instrukcja Instalacji i Uruchomienia

Aplikację łatwo można uruchomić w czystym środowisku wirtualnym Pythona. W katalogu głównym projektu (tam gdzie znajduje się `main.py`) uruchom w terminalu (np. PowerShell lub Command Prompt):

1. Utwórz środowisko wirtualne:
   ```bash
   python -m venv .venv
   ```

2. Aktywuj środowisko:
   - W systemie Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - W systemie Linux/MacOS:
     ```bash
     source .venv/bin/activate
     ```

3. Zainstaluj wymagane biblioteki:
   ```bash
   pip install -r requirements.txt
   ```

4. Uruchom aplikację:
   ```bash
   python main.py
   ```

*(Przy pierwszym uruchomieniu zostanie automatycznie wygenerowana baza danych zawierająca **Przykładowe / Demonstracyjne** dane startowe — blok, kilkunastu mieszkańców i płatności)*

---

# Informacje o Pustej Bazie i Seed Data

Jeżeli aplikacja zostanie uruchomiona po raz pierwszy i nie znajdzie pliku `zarzadca_bloku.db`, sama go utworzy, a funkcja `seed_database()` automatycznie wypełni go bezpiecznymi, testowymi wpisami symulującymi rzeczywisty miesięczny przemiał bloku.


# Możliwe Kierunki Rozwoju

Wdrożone oprogramowanie (Aplikacja MVP) jest w pełni elastyczne i przygotowane do rozbudowywania w ramach np. kolejnych projektów czy praktyk:
- Moduł drukowania faktur dla danego zalegającego w PDF.
- Import zewnętrznej bazy liczników gazu lub wody.
- Tworzenie paneli i harmonogramów dyżurów do śmieci, prac czy sprzątaczy.
- Statystyczne wykresy z wykorzystaniem `matplotlib` bądź `PyQtGraph`.
- Zaawansowane wyszukiwarki pełnotekstowe. 
