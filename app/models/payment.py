"""Model płatności."""

from datetime import datetime, date
from typing import Optional

from sqlalchemy import Integer, Float, String, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"), nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    rent_amount: Mapped[float] = mapped_column(Float, default=0.0)
    utilities_amount: Mapped[float] = mapped_column(Float, default=0.0)
    other_amount: Mapped[float] = mapped_column(Float, default=0.0)
    total_amount: Mapped[float] = mapped_column(Float, default=0.0)
    paid_amount: Mapped[float] = mapped_column(Float, default=0.0)
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    paid_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="nieopłacone")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, init=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, init=False)

    apartment = relationship("Apartment", back_populates="payments", init=False)

    def recalculate(self) -> None:
        """Przelicza sumę i saldo."""
        self.total_amount = (self.rent_amount or 0) + (self.utilities_amount or 0) + (self.other_amount or 0)
        self.balance = self.total_amount - (self.paid_amount or 0)
