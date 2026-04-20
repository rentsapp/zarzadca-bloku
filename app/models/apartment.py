"""Model mieszkania."""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Integer, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Apartment(Base):
    __tablename__ = "apartments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"), nullable=False)
    number: Mapped[str] = mapped_column(String(20), nullable=False)
    staircase: Mapped[str] = mapped_column(String(10), nullable=False)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    area: Mapped[float] = mapped_column(Float, nullable=False)
    rooms: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="wolne")
    ownership_type: Mapped[str] = mapped_column(String(30), nullable=False, default="własnościowe")
    base_rent: Mapped[float] = mapped_column(Float, default=0.0)
    has_balcony: Mapped[bool] = mapped_column(Boolean, default=False)
    has_storage: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, init=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, init=False)

    building = relationship("Building", back_populates="apartments", init=False)
    person_links: Mapped[List["ApartmentPersonLink"]] = relationship(
        "ApartmentPersonLink", back_populates="apartment", cascade="all, delete-orphan", init=False
    )
    payments: Mapped[List["Payment"]] = relationship(
        "Payment", back_populates="apartment", cascade="all, delete-orphan", init=False
    )
    issues: Mapped[List["Issue"]] = relationship(
        "Issue", back_populates="apartment", cascade="all, delete-orphan", init=False
    )
