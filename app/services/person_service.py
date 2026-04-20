"""Serwis osób — operacje CRUD i filtrowanie."""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.person import Person
from app.models.apartment_person_link import ApartmentPersonLink


class PersonService:

    @staticmethod
    def get_all(session: Session) -> list[Person]:
        return session.query(Person).order_by(Person.last_name, Person.first_name).all()

    @staticmethod
    def get_by_id(session: Session, person_id: int) -> Optional[Person]:
        return session.query(Person).get(person_id)

    @staticmethod
    def add(session: Session, **kwargs) -> Person:
        person = Person(**kwargs)
        session.add(person)
        session.commit()
        return person

    @staticmethod
    def update(session: Session, person_id: int, **kwargs) -> Optional[Person]:
        person = session.query(Person).get(person_id)
        if person:
            for k, v in kwargs.items():
                if hasattr(person, k):
                    setattr(person, k, v)
            session.commit()
        return person

    @staticmethod
    def delete(session: Session, person_id: int) -> bool:
        person = session.query(Person).get(person_id)
        if person:
            session.delete(person)
            session.commit()
            return True
        return False

    @staticmethod
    def filter_persons(
        session: Session,
        name: str = "",
        role: str = "",
        is_active: Optional[bool] = None,
    ) -> list[Person]:
        query = session.query(Person)
        if name:
            query = query.filter(
                (Person.first_name.ilike(f"%{name}%")) | (Person.last_name.ilike(f"%{name}%"))
            )
        if role:
            query = query.filter(Person.role == role)
        if is_active is not None:
            query = query.filter(Person.is_active == is_active)
        return query.order_by(Person.last_name, Person.first_name).all()

    @staticmethod
    def assign_to_apartment(
        session: Session,
        person_id: int,
        apartment_id: int,
        role_in_apartment: str = "lokator",
        is_primary: bool = False,
        from_date=None,
    ) -> ApartmentPersonLink:
        link = ApartmentPersonLink(
            person_id=person_id,
            apartment_id=apartment_id,
            role_in_apartment=role_in_apartment,
            is_primary=is_primary,
            from_date=from_date,
        )
        session.add(link)
        session.commit()
        return link

    @staticmethod
    def remove_from_apartment(session: Session, link_id: int) -> bool:
        link = session.query(ApartmentPersonLink).get(link_id)
        if link:
            session.delete(link)
            session.commit()
            return True
        return False

    @staticmethod
    def get_apartments_for_person(session: Session, person_id: int) -> list[ApartmentPersonLink]:
        return (
            session.query(ApartmentPersonLink)
            .filter(ApartmentPersonLink.person_id == person_id)
            .all()
        )
