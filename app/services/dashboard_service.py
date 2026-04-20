"""Serwis dashboardu — agregaty i statystyki."""

from sqlalchemy.orm import Session
from app.models.apartment import Apartment
from app.models.person import Person
from app.models.payment import Payment
from app.models.issue import Issue


class DashboardService:

    @staticmethod
    def get_stats(session: Session) -> dict:
        total_apartments = session.query(Apartment).count()
        free = session.query(Apartment).filter(Apartment.status == "wolne").count()
        occupied = session.query(Apartment).filter(Apartment.status == "zamieszkane").count()
        reserved = session.query(Apartment).filter(Apartment.status == "zarezerwowane").count()
        renovation = session.query(Apartment).filter(Apartment.status == "w remoncie").count()
        active_persons = session.query(Person).filter(Person.is_active == True).count()

        overdue_payments = (
            session.query(Payment)
            .filter(Payment.status.in_(["nieopłacone", "po terminie", "częściowo opłacone"]))
            .all()
        )
        overdue_count = len(overdue_payments)
        total_debt = sum(p.balance for p in overdue_payments if p.balance > 0)

        active_issues = (
            session.query(Issue)
            .filter(Issue.status.in_(["nowe", "przyjęte", "w trakcie"]))
            .count()
        )

        recent_payments = (
            session.query(Payment)
            .order_by(Payment.created_at.desc())
            .limit(5)
            .all()
        )
        recent_issues = (
            session.query(Issue)
            .order_by(Issue.created_at.desc())
            .limit(5)
            .all()
        )

        return {
            "total_apartments": total_apartments,
            "free": free,
            "occupied": occupied,
            "reserved": reserved,
            "renovation": renovation,
            "active_persons": active_persons,
            "overdue_count": overdue_count,
            "total_debt": total_debt,
            "active_issues": active_issues,
            "recent_payments": recent_payments,
            "recent_issues": recent_issues,
        }
