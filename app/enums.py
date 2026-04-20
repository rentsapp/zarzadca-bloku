"""Definicje enumów i kontrolowanych zestawów wartości."""

import enum


class ApartmentStatus(enum.Enum):
    """Status mieszkania."""
    WOLNE = "wolne"
    ZAMIESZKANE = "zamieszkane"
    ZAREZERWOWANE = "zarezerwowane"
    W_REMONCIE = "w remoncie"

    @property
    def label(self) -> str:
        return self.value.capitalize()


class OwnershipType(enum.Enum):
    """Typ własności mieszkania."""
    WLASNOSCIOWE = "własnościowe"
    WYNAJMOWANE = "wynajmowane"
    KOMUNALNE = "komunalne"
    SLUZBOWE = "służbowe"
    INNE = "inne"

    @property
    def label(self) -> str:
        return self.value.capitalize()


class PersonRole(enum.Enum):
    """Rola osoby."""
    WLASCICIEL = "właściciel"
    LOKATOR = "lokator"
    NAJEMCA = "najemca"
    WSPOLWLASCICIEL = "współwłaściciel"
    OPIEKUN = "opiekun kontaktowy"

    @property
    def label(self) -> str:
        return self.value.capitalize()


class PaymentStatus(enum.Enum):
    """Status płatności."""
    OPLACONE = "opłacone"
    CZESCIOWO = "częściowo opłacone"
    NIEOPLACONE = "nieopłacone"
    PO_TERMINIE = "po terminie"

    @property
    def label(self) -> str:
        return self.value.capitalize()


class IssuePriority(enum.Enum):
    """Priorytet usterki."""
    NISKI = "niski"
    SREDNI = "średni"
    WYSOKI = "wysoki"
    PILNY = "pilny"

    @property
    def label(self) -> str:
        return self.value.capitalize()


class IssueStatus(enum.Enum):
    """Status usterki."""
    NOWE = "nowe"
    PRZYJETE = "przyjęte"
    W_TRAKCIE = "w trakcie"
    ZAKONCZONE = "zakończone"
    ANULOWANE = "anulowane"

    @property
    def label(self) -> str:
        return self.value.capitalize()
