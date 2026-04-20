"""Model osoby (właściciel, lokator itp.)."""

from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import String, Boolean, Text, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    pesel: Mapped[Optional[str]] = mapped_column(String(11), nullable=True)
    role: Mapped[str] = mapped_column(String(30), nullable=False, default="lokator")
    move_in_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    move_out_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, init=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, init=False)

    apartment_links: Mapped[List["ApartmentPersonLink"]] = relationship(
        "ApartmentPersonLink", back_populates="person", cascade="all, delete-orphan", init=False
    )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
