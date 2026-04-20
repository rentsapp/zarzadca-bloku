"""Model usterki / zgłoszenia."""

from datetime import datetime, date
from typing import Optional

from sqlalchemy import Integer, Float, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    apartment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("apartments.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location_description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    reporter_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    reported_at: Mapped[date] = mapped_column(Date, default=date.today)
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="średni")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="nowe")
    estimated_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    actual_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    resolved_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, init=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, init=False)

    apartment = relationship("Apartment", back_populates="issues", init=False)
