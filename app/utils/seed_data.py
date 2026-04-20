"""Dane startowe — realistyczne dane demonstracyjne."""

from datetime import date
from sqlalchemy.orm import Session

from app.models.building import Building
from app.models.apartment import Apartment
from app.models.person import Person
from app.models.apartment_person_link import ApartmentPersonLink
from app.models.payment import Payment
from app.models.issue import Issue


def seed_database(session: Session) -> None:
    """Wypełnia bazę danymi demonstracyjnymi, jeśli jest pusta."""
    if session.query(Building).count() > 0:
        return

    # --- Budynek ---
    building = Building(
        name="Blok Słoneczny",
        street="ul. Kwiatowa",
        building_number="12",
        postal_code="00-001",
        city="Warszawa",
        staircases_count=2,
        floors_count=4,
        apartments_count=16,
        notes="Budynek wielorodzinny wybudowany w 2005 roku.",
    )
    session.add(building)
    session.flush()

    # --- Mieszkania ---
    apartments_data = [
        # Klatka A
        {"number": "1", "staircase": "A", "floor": 0, "area": 35.0, "rooms": 1, "status": "zamieszkane", "ownership_type": "własnościowe", "base_rent": 850.00, "has_balcony": False, "has_storage": True},
        {"number": "2", "staircase": "A", "floor": 0, "area": 48.5, "rooms": 2, "status": "zamieszkane", "ownership_type": "własnościowe", "base_rent": 1200.00, "has_balcony": False, "has_storage": True},
        {"number": "3", "staircase": "A", "floor": 1, "area": 55.0, "rooms": 3, "status": "zamieszkane", "ownership_type": "wynajmowane", "base_rent": 1450.00, "has_balcony": True, "has_storage": False},
        {"number": "4", "staircase": "A", "floor": 1, "area": 42.0, "rooms": 2, "status": "wolne", "ownership_type": "własnościowe", "base_rent": 1100.00, "has_balcony": True, "has_storage": False},
        {"number": "5", "staircase": "A", "floor": 2, "area": 62.5, "rooms": 3, "status": "zamieszkane", "ownership_type": "własnościowe", "base_rent": 1600.00, "has_balcony": True, "has_storage": True},
        {"number": "6", "staircase": "A", "floor": 2, "area": 38.0, "rooms": 1, "status": "w remoncie", "ownership_type": "komunalne", "base_rent": 750.00, "has_balcony": False, "has_storage": False},
        {"number": "7", "staircase": "A", "floor": 3, "area": 72.0, "rooms": 4, "status": "zamieszkane", "ownership_type": "własnościowe", "base_rent": 1850.00, "has_balcony": True, "has_storage": True},
        {"number": "8", "staircase": "A", "floor": 3, "area": 45.0, "rooms": 2, "status": "zarezerwowane", "ownership_type": "wynajmowane", "base_rent": 1150.00, "has_balcony": True, "has_storage": False},
        # Klatka B
        {"number": "9", "staircase": "B", "floor": 0, "area": 40.0, "rooms": 2, "status": "zamieszkane", "ownership_type": "własnościowe", "base_rent": 1050.00, "has_balcony": False, "has_storage": True},
        {"number": "10", "staircase": "B", "floor": 0, "area": 50.0, "rooms": 2, "status": "zamieszkane", "ownership_type": "służbowe", "base_rent": 1300.00, "has_balcony": False, "has_storage": True},
        {"number": "11", "staircase": "B", "floor": 1, "area": 55.5, "rooms": 3, "status": "zamieszkane", "ownership_type": "własnościowe", "base_rent": 1400.00, "has_balcony": True, "has_storage": False},
        {"number": "12", "staircase": "B", "floor": 1, "area": 36.0, "rooms": 1, "status": "wolne", "ownership_type": "wynajmowane", "base_rent": 900.00, "has_balcony": False, "has_storage": False},
        {"number": "13", "staircase": "B", "floor": 2, "area": 68.0, "rooms": 3, "status": "zamieszkane", "ownership_type": "własnościowe", "base_rent": 1700.00, "has_balcony": True, "has_storage": True},
        {"number": "14", "staircase": "B", "floor": 2, "area": 44.0, "rooms": 2, "status": "zamieszkane", "ownership_type": "komunalne", "base_rent": 1050.00, "has_balcony": True, "has_storage": False},
        {"number": "15", "staircase": "B", "floor": 3, "area": 80.0, "rooms": 4, "status": "zamieszkane", "ownership_type": "własnościowe", "base_rent": 2000.00, "has_balcony": True, "has_storage": True},
        {"number": "16", "staircase": "B", "floor": 3, "area": 42.0, "rooms": 2, "status": "w remoncie", "ownership_type": "własnościowe", "base_rent": 1100.00, "has_balcony": False, "has_storage": False},
    ]

    apartments = []
    for data in apartments_data:
        apt = Apartment(building_id=building.id, **data)
        session.add(apt)
        apartments.append(apt)
    session.flush()

    # --- Osoby ---
    persons_data = [
        {"first_name": "Jan", "last_name": "Kowalski", "phone": "601234567", "email": "jan.kowalski@email.pl", "role": "właściciel", "is_active": True, "move_in_date": date(2018, 3, 1)},
        {"first_name": "Anna", "last_name": "Nowak", "phone": "602345678", "email": "anna.nowak@email.pl", "role": "właściciel", "is_active": True, "move_in_date": date(2019, 6, 15)},
        {"first_name": "Piotr", "last_name": "Wiśniewski", "phone": "603456789", "email": "piotr.w@email.pl", "role": "lokator", "is_active": True, "move_in_date": date(2020, 1, 1)},
        {"first_name": "Maria", "last_name": "Wójcik", "phone": "604567890", "email": "maria.wojcik@email.pl", "role": "najemca", "is_active": True, "move_in_date": date(2021, 9, 1)},
        {"first_name": "Tomasz", "last_name": "Kamiński", "phone": "605678901", "email": "tomasz.k@email.pl", "role": "właściciel", "is_active": True, "move_in_date": date(2017, 5, 10)},
        {"first_name": "Katarzyna", "last_name": "Lewandowska", "phone": "606789012", "email": "kasia.l@email.pl", "role": "lokator", "is_active": True, "move_in_date": date(2022, 2, 1)},
        {"first_name": "Michał", "last_name": "Zieliński", "phone": "607890123", "email": "michal.z@email.pl", "role": "właściciel", "is_active": True, "move_in_date": date(2016, 8, 1)},
        {"first_name": "Agnieszka", "last_name": "Szymańska", "phone": "608901234", "email": "agnieszka.sz@email.pl", "role": "współwłaściciel", "is_active": True, "move_in_date": date(2016, 8, 1)},
        {"first_name": "Krzysztof", "last_name": "Woźniak", "phone": "609012345", "email": "krzysztof.w@email.pl", "role": "lokator", "is_active": True, "move_in_date": date(2023, 4, 1)},
        {"first_name": "Ewa", "last_name": "Dąbrowska", "phone": "610123456", "email": "ewa.d@email.pl", "role": "właściciel", "is_active": True, "move_in_date": date(2019, 11, 15)},
        {"first_name": "Robert", "last_name": "Kozłowski", "phone": "611234567", "email": "", "role": "najemca", "is_active": True, "move_in_date": date(2024, 1, 1)},
        {"first_name": "Magdalena", "last_name": "Jankowska", "phone": "612345678", "email": "magda.j@email.pl", "role": "właściciel", "is_active": False, "move_in_date": date(2015, 3, 1), "move_out_date": date(2023, 6, 30)},
    ]

    persons = []
    for data in persons_data:
        person = Person(**data)
        session.add(person)
        persons.append(person)
    session.flush()

    # --- Przypisania osób do mieszkań ---
    links_data = [
        (0, 0, "właściciel", True),   # Jan Kowalski -> m.1
        (1, 1, "właściciel", True),   # Anna Nowak -> m.2
        (2, 2, "lokator", True),      # Piotr Wiśniewski -> m.3
        (3, 2, "najemca", False),     # Maria Wójcik -> m.3
        (4, 4, "właściciel", True),   # Tomasz Kamiński -> m.5
        (5, 4, "lokator", False),     # Katarzyna Lewandowska -> m.5
        (6, 6, "właściciel", True),   # Michał Zieliński -> m.7
        (7, 6, "współwłaściciel", False),  # Agnieszka Szymańska -> m.7
        (8, 8, "lokator", True),      # Krzysztof Woźniak -> m.9
        (9, 9, "właściciel", True),   # Ewa Dąbrowska -> m.10
        (10, 10, "najemca", True),    # Robert Kozłowski -> m.11
        (9, 12, "właściciel", True),  # Ewa Dąbrowska -> m.13
        (4, 13, "właściciel", True),  # Tomasz Kamiński -> m.14
        (6, 14, "właściciel", True),  # Michał Zieliński -> m.15
    ]

    for person_idx, apt_idx, role, is_primary in links_data:
        link = ApartmentPersonLink(
            apartment_id=apartments[apt_idx].id,
            person_id=persons[person_idx].id,
            role_in_apartment=role,
            is_primary=is_primary,
            from_date=persons[person_idx].move_in_date,
        )
        session.add(link)
    session.flush()

    # --- Płatności ---
    # Generujemy płatności za ostatnie 3 miesiące dla zamieszkanych mieszkań
    occupied_indices = [i for i, a in enumerate(apartments) if a.status == "zamieszkane"]

    payments_config = [
        # (miesiąc, rok, termin, opłata_pełna, status configs)
        (1, 2026, date(2026, 1, 10)),
        (2, 2026, date(2026, 2, 10)),
        (3, 2026, date(2026, 3, 10)),
    ]

    for apt_idx in occupied_indices:
        apt = apartments[apt_idx]
        for month_num, year_num, due in payments_config:
            rent = apt.base_rent
            utilities = round(apt.area * 8.5, 2)  # ~8.5 zł/m² na media
            other = 50.0
            total = rent + utilities + other

            # Różne statusy opłat
            if month_num == 1:
                paid = total
                status = "opłacone"
                paid_date = date(2026, 1, 8)
            elif month_num == 2:
                if apt_idx in [0, 2, 4]:
                    paid = total
                    status = "opłacone"
                    paid_date = date(2026, 2, 9)
                elif apt_idx in [8, 9]:
                    paid = total * 0.5
                    status = "częściowo opłacone"
                    paid_date = date(2026, 2, 15)
                else:
                    paid = total
                    status = "opłacone"
                    paid_date = date(2026, 2, 7)
            else:  # marzec
                if apt_idx in [0, 4, 6]:
                    paid = total
                    status = "opłacone"
                    paid_date = date(2026, 3, 5)
                elif apt_idx in [2, 10]:
                    paid = 0.0
                    status = "nieopłacone"
                    paid_date = None
                elif apt_idx in [12, 13]:
                    paid = 0.0
                    status = "po terminie"
                    paid_date = None
                else:
                    paid = 0.0
                    status = "nieopłacone"
                    paid_date = None

            balance = total - paid

            payment = Payment(
                apartment_id=apt.id,
                month=month_num,
                year=year_num,
                rent_amount=rent,
                utilities_amount=utilities,
                other_amount=other,
                total_amount=total,
                paid_amount=paid,
                balance=balance,
                due_date=due,
                paid_date=paid_date,
                status=status,
            )
            session.add(payment)

    session.flush()

    # --- Usterki ---
    issues_data = [
        {
            "apartment_id": apartments[2].id,
            "title": "Cieknący kran w kuchni",
            "description": "Kran w kuchni cieknie przy zakręcaniu, wymaga wymiany uszczelki lub całego kranu.",
            "reporter_name": "Piotr Wiśniewski",
            "reported_at": date(2026, 2, 15),
            "priority": "średni",
            "status": "przyjęte",
            "estimated_cost": 200.0,
        },
        {
            "apartment_id": apartments[6].id,
            "title": "Uszkodzona klamka okna",
            "description": "Klamka okna w salonie jest obluzowana i nie zamyka się prawidłowo.",
            "reporter_name": "Michał Zieliński",
            "reported_at": date(2026, 3, 1),
            "priority": "niski",
            "status": "nowe",
            "estimated_cost": 80.0,
        },
        {
            "apartment_id": apartments[0].id,
            "title": "Awaria ogrzewania",
            "description": "Kaloryfer w sypialni nie grzeje, pomimo odkręcenia termostatu. Prawdopodobnie zapowietrzona instalacja.",
            "reporter_name": "Jan Kowalski",
            "reported_at": date(2026, 3, 10),
            "priority": "wysoki",
            "status": "w trakcie",
            "estimated_cost": 350.0,
        },
        {
            "apartment_id": None,
            "title": "Niedziałające oświetlenie na klatce B",
            "description": "Na klatce schodowej B na 2. piętrze nie działa oświetlenie. Prawdopodobnie przepalona żarówka lub uszkodzony czujnik ruchu.",
            "location_description": "Klatka B, 2. piętro",
            "reporter_name": "Krzysztof Woźniak",
            "reported_at": date(2026, 3, 5),
            "priority": "średni",
            "status": "przyjęte",
            "estimated_cost": 50.0,
        },
        {
            "apartment_id": apartments[4].id,
            "title": "Wilgoć na ścianie",
            "description": "Na ścianie północnej w łazience pojawia się wilgoć i zaczyna się pleśń.",
            "reporter_name": "Tomasz Kamiński",
            "reported_at": date(2026, 1, 20),
            "priority": "pilny",
            "status": "w trakcie",
            "estimated_cost": 1500.0,
        },
        {
            "apartment_id": apartments[9].id,
            "title": "Zepsuty domofon",
            "description": "Domofon w mieszkaniu nie odbiera połączeń z panelu przy wejściu.",
            "reporter_name": "Ewa Dąbrowska",
            "reported_at": date(2026, 2, 28),
            "priority": "średni",
            "status": "zakończone",
            "estimated_cost": 150.0,
            "actual_cost": 120.0,
            "resolved_at": date(2026, 3, 8),
        },
        {
            "apartment_id": None,
            "title": "Uszkodzony chodnik przed budynkiem",
            "description": "Płyty chodnikowe przed wejściem do klatki A są popękane i nierówne — ryzyko potknięcia.",
            "location_description": "Przed wejściem do klatki A",
            "reporter_name": "Anna Nowak",
            "reported_at": date(2026, 3, 12),
            "priority": "wysoki",
            "status": "nowe",
            "estimated_cost": 800.0,
        },
    ]

    for data in issues_data:
        issue = Issue(**data)
        session.add(issue)

    session.commit()
