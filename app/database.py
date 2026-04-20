"""Moduł bazy danych — inicjalizacja silnika i sesji SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedAsDataclass

from app.config import DATABASE_URL


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    """Bazowa klasa dla wszystkich modeli SQLAlchemy."""
    pass


engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db() -> None:
    """Tworzy wszystkie tabele w bazie danych."""
    import app.models  # noqa: F401 — wymusza rejestrację modeli
    Base.metadata.create_all(bind=engine)


def get_session():
    """Zwraca nową sesję bazy danych."""
    return SessionLocal()
