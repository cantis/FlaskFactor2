"""Database Models."""

from __future__ import annotations

import os
from contextlib import contextmanager
from enum import Enum
from sqlite3 import DatabaseError
from typing import TYPE_CHECKING, Generator

from flask_login import UserMixin
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

if TYPE_CHECKING:
    from datetime import date

DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///flask_factor.db'
engine = create_engine(url=DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    """Create database and tables."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Return a database session."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except DatabaseError as e:
            e.add_note('An error occurred with the database')
            session.rollback()
            raise


class Player(SQLModel, UserMixin, table=True):
    """Player model."""

    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str
    name: str
    password_attempts: int = Field(default=0)
    reset_password: bool = Field(default=False)
    is_active: bool = Field(default=True)


def seed_data() -> None:
    """Seed data."""
    with Session(engine) as session:
        # Add seed data here
        pass
