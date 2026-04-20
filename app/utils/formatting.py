"""Funkcje formatujące dane do wyświetlania."""


def format_currency(value: float) -> str:
    """Formatuje kwotę jako walutę PLN."""
    if value is None:
        return "0,00 zł"
    return f"{value:,.2f} zł".replace(",", " ").replace(".", ",")


def format_area(value: float) -> str:
    """Formatuje metraż."""
    if value is None:
        return "—"
    return f"{value:.1f} m²".replace(".", ",")


def format_date(value) -> str:
    """Formatuje datę do wyświetlania."""
    if value is None:
        return "—"
    if hasattr(value, "strftime"):
        return value.strftime("%d.%m.%Y")
    return str(value)


def month_name(month: int) -> str:
    """Zwraca nazwę miesiąca po polsku."""
    names = {
        1: "Styczeń", 2: "Luty", 3: "Marzec", 4: "Kwiecień",
        5: "Maj", 6: "Czerwiec", 7: "Lipiec", 8: "Sierpień",
        9: "Wrzesień", 10: "Październik", 11: "Listopad", 12: "Grudzień",
    }
    return names.get(month, str(month))


def bool_to_text(value: bool) -> str:
    """Konwertuje wartość logiczną na tekst."""
    return "Tak" if value else "Nie"
