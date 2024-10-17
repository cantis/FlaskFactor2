"""Database Models."""

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from sqlite3 import DatabaseError
from typing import TYPE_CHECKING, Generator

from flask_login import UserMixin
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from datetime import date

DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///flask_factor.db'
engine = create_engine(url=DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    """Create database and tables."""
    SQLModel.metadata.create_all(engine)
    logger.info('Database and tables created')


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Return a database session."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except DatabaseError as e:
            e.add_note('An error occurred with the database')
            logging.exception('Database error occurred %s')
            if session:
                session.rollback()
            raise
        except Exception as e:
            logging.exception('General error occurred %s')
            if session:
                session.rollback()
            e.add_note('General error occurred')
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
