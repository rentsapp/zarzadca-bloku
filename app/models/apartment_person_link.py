"""Tabela relacyjna łącząca osoby z mieszkaniami."""

from datetime import date
from typing import Optional

from sqlalchemy import Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ApartmentPersonLink(Base):
    __tablename__ = "apartment_person_links"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"), nullable=False)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), nullable=False)
    role_in_apartment: Mapped[str] = mapped_column(String(30), nullable=False, default="lokator")
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    from_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    to_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    apartment = relationship("Apartment", back_populates="person_links", init=False)
    person = relationship("Person", back_populates="apartment_links", init=False)
