"""Serwis płatności — operacje CRUD i filtrowanie."""

from typing import Optional
from datetime import date
from sqlalchemy.orm import Session
from app.models.payment import Payment


class PaymentService:

    @staticmethod
    def get_all(session: Session) -> list[Payment]:
        return session.query(Payment).order_by(Payment.year.desc(), Payment.month.desc()).all()

    @staticmethod
    def get_by_id(session: Session, payment_id: int) -> Optional[Payment]:
        return session.query(Payment).get(payment_id)

    @staticmethod
    def add(session: Session, **kwargs) -> Payment:
        payment = Payment(**kwargs)
        payment.recalculate()
        session.add(payment)
        session.commit()
        return payment

    @staticmethod
    def update(session: Session, payment_id: int, **kwargs) -> Optional[Payment]:
        payment = session.query(Payment).get(payment_id)
        if payment:
            for k, v in kwargs.items():
                if hasattr(payment, k):
                    setattr(payment, k, v)
            payment.recalculate()
            session.commit()
        return payment

    @staticmethod
    def delete(session: Session, payment_id: int) -> bool:
        payment = session.query(Payment).get(payment_id)
        if payment:
            session.delete(payment)
            session.commit()
            return True
        return False

    @staticmethod
    def mark_as_paid(session: Session, payment_id: int) -> Optional[Payment]:
        payment = session.query(Payment).get(payment_id)
        if payment:
            payment.paid_amount = payment.total_amount
            payment.balance = 0.0
            payment.status = "opłacone"
            payment.paid_date = date.today()
            session.commit()
        return payment

    @staticmethod
    def filter_payments(
        session: Session,
        apartment_id: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        status: str = "",
    ) -> list[Payment]:
        query = session.query(Payment)
        if apartment_id is not None:
            query = query.filter(Payment.apartment_id == apartment_id)
        if month is not None:
            query = query.filter(Payment.month == month)
        if year is not None:
            query = query.filter(Payment.year == year)
        if status:
            query = query.filter(Payment.status == status)
        return query.order_by(Payment.year.desc(), Payment.month.desc()).all()

    @staticmethod
    def get_overdue(session: Session) -> list[Payment]:
        return (
            session.query(Payment)
            .filter(Payment.status.in_(["nieopłacone", "po terminie", "częściowo opłacone"]))
            .order_by(Payment.year.desc(), Payment.month.desc())
            .all()
        )

    @staticmethod
    def get_total_debt(session: Session) -> float:
        payments = PaymentService.get_overdue(session)
        return sum(p.balance for p in payments if p.balance > 0)

    @staticmethod
    def get_recent(session: Session, limit: int = 5) -> list[Payment]:
        return (
            session.query(Payment)
            .order_by(Payment.created_at.desc())
            .limit(limit)
            .all()
        )
