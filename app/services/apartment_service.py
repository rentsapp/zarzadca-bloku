"""Serwis mieszkań — operacje CRUD i filtrowanie."""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.apartment import Apartment
from app.models.apartment_person_link import ApartmentPersonLink
from app.database import get_session


class ApartmentService:

    @staticmethod
    def get_all(session: Session) -> list[Apartment]:
        return session.query(Apartment).order_by(Apartment.number).all()

    @staticmethod
    def get_by_id(session: Session, apartment_id: int) -> Optional[Apartment]:
        return session.query(Apartment).get(apartment_id)

    @staticmethod
    def add(session: Session, **kwargs) -> Apartment:
        apartment = Apartment(**kwargs)
        session.add(apartment)
        session.commit()
        return apartment

    @staticmethod
    def update(session: Session, apartment_id: int, **kwargs) -> Optional[Apartment]:
        apartment = session.query(Apartment).get(apartment_id)
        if apartment:
            for key, value in kwargs.items():
                if hasattr(apartment, key):
                    setattr(apartment, key, value)
            session.commit()
        return apartment

    @staticmethod
    def delete(session: Session, apartment_id: int) -> bool:
        apartment = session.query(Apartment).get(apartment_id)
        if apartment:
            session.delete(apartment)
            session.commit()
            return True
        return False

    @staticmethod
    def filter_apartments(
        session: Session,
        number: str = "",
        staircase: str = "",
        floor: Optional[int] = None,
        status: str = "",
        rooms: Optional[int] = None,
    ) -> list[Apartment]:
        query = session.query(Apartment)
        if number:
            query = query.filter(Apartment.number.ilike(f"%{number}%"))
        if staircase:
            query = query.filter(Apartment.staircase == staircase)
        if floor is not None:
            query = query.filter(Apartment.floor == floor)
        if status:
            query = query.filter(Apartment.status == status)
        if rooms is not None:
            query = query.filter(Apartment.rooms == rooms)
        return query.order_by(Apartment.number).all()

    @staticmethod
    def get_persons_for_apartment(session: Session, apartment_id: int) -> list:
        links = (
            session.query(ApartmentPersonLink)
            .filter(ApartmentPersonLink.apartment_id == apartment_id)
            .all()
        )
        return links

    @staticmethod
    def get_staircases(session: Session) -> list[str]:
        results = session.query(Apartment.staircase).distinct().order_by(Apartment.staircase).all()
        return [r[0] for r in results]

    @staticmethod
    def get_floors(session: Session) -> list[int]:
        results = session.query(Apartment.floor).distinct().order_by(Apartment.floor).all()
        return [r[0] for r in results]
