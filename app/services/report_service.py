"""Serwis raportów — dane do widoku raportów i eksportu."""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.apartment import Apartment
from app.models.payment import Payment
from app.models.issue import Issue


class ReportService:

    @staticmethod
    def apartments_by_status(session: Session) -> list[dict]:
        results = (
            session.query(Apartment.status, func.count(Apartment.id))
            .group_by(Apartment.status)
            .all()
        )
        return [{"status": r[0], "count": r[1]} for r in results]

    @staticmethod
    def apartments_by_rooms(session: Session) -> list[dict]:
        results = (
            session.query(Apartment.rooms, func.count(Apartment.id))
            .group_by(Apartment.rooms)
            .order_by(Apartment.rooms)
            .all()
        )
        return [{"rooms": r[0], "count": r[1]} for r in results]

    @staticmethod
    def apartments_with_debt(session: Session) -> list[dict]:
        overdue = (
            session.query(Payment)
            .filter(Payment.status.in_(["nieopłacone", "po terminie", "częściowo opłacone"]))
            .all()
        )
        debt_by_apt: dict[int, float] = {}
        for p in overdue:
            debt_by_apt[p.apartment_id] = debt_by_apt.get(p.apartment_id, 0) + p.balance

        result = []
        for apt_id, debt in sorted(debt_by_apt.items()):
            apt = session.query(Apartment).get(apt_id)
            if apt:
                result.append({
                    "apartment_number": apt.number,
                    "staircase": apt.staircase,
                    "floor": apt.floor,
                    "debt": debt,
                })
        return result

    @staticmethod
    def issues_by_status(session: Session) -> list[dict]:
        results = (
            session.query(Issue.status, func.count(Issue.id))
            .group_by(Issue.status)
            .all()
        )
        return [{"status": r[0], "count": r[1]} for r in results]

    @staticmethod
    def issues_by_priority(session: Session) -> list[dict]:
        results = (
            session.query(Issue.priority, func.count(Issue.id))
            .group_by(Issue.priority)
            .all()
        )
        return [{"priority": r[0], "count": r[1]} for r in results]

    @staticmethod
    def active_issues(session: Session) -> list[Issue]:
        return (
            session.query(Issue)
            .filter(Issue.status.in_(["nowe", "przyjęte", "w trakcie"]))
            .order_by(Issue.reported_at.desc())
            .all()
        )
