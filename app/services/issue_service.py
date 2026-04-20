"""Serwis usterek — operacje CRUD i filtrowanie."""

from typing import Optional
from sqlalchemy.orm import Session
from app.models.issue import Issue


class IssueService:

    @staticmethod
    def get_all(session: Session) -> list[Issue]:
        return session.query(Issue).order_by(Issue.reported_at.desc()).all()

    @staticmethod
    def get_by_id(session: Session, issue_id: int) -> Optional[Issue]:
        return session.query(Issue).get(issue_id)

    @staticmethod
    def add(session: Session, **kwargs) -> Issue:
        issue = Issue(**kwargs)
        session.add(issue)
        session.commit()
        return issue

    @staticmethod
    def update(session: Session, issue_id: int, **kwargs) -> Optional[Issue]:
        issue = session.query(Issue).get(issue_id)
        if issue:
            for k, v in kwargs.items():
                if hasattr(issue, k):
                    setattr(issue, k, v)
            session.commit()
        return issue

    @staticmethod
    def delete(session: Session, issue_id: int) -> bool:
        issue = session.query(Issue).get(issue_id)
        if issue:
            session.delete(issue)
            session.commit()
            return True
        return False

    @staticmethod
    def filter_issues(
        session: Session,
        title: str = "",
        status: str = "",
        priority: str = "",
        apartment_id: Optional[int] = None,
    ) -> list[Issue]:
        query = session.query(Issue)
        if title:
            query = query.filter(Issue.title.ilike(f"%{title}%"))
        if status:
            query = query.filter(Issue.status == status)
        if priority:
            query = query.filter(Issue.priority == priority)
        if apartment_id is not None:
            query = query.filter(Issue.apartment_id == apartment_id)
        return query.order_by(Issue.reported_at.desc()).all()

    @staticmethod
    def get_active(session: Session) -> list[Issue]:
        return (
            session.query(Issue)
            .filter(Issue.status.in_(["nowe", "przyjęte", "w trakcie"]))
            .order_by(Issue.reported_at.desc())
            .all()
        )

    @staticmethod
    def get_active_count(session: Session) -> int:
        return (
            session.query(Issue)
            .filter(Issue.status.in_(["nowe", "przyjęte", "w trakcie"]))
            .count()
        )

    @staticmethod
    def get_recent(session: Session, limit: int = 5) -> list[Issue]:
        return (
            session.query(Issue)
            .order_by(Issue.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_active_for_apartment(session: Session, apartment_id: int) -> int:
        return (
            session.query(Issue)
            .filter(Issue.apartment_id == apartment_id)
            .filter(Issue.status.in_(["nowe", "przyjęte", "w trakcie"]))
            .count()
        )
