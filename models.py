"""Database Models."""

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from sqlite3 import DatabaseError
from typing import Generator

from flask import g
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///flask_factor.db'
engine = create_engine(url=DATABASE_URL, echo=True)
Session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


def create_db_and_tables() -> None:
    """Create database and tables."""
    Base.metadata.create_all(engine)
    logger.info('Database and tables created')


@contextmanager
def get_session() -> Generator:
    """Return a database session."""
    session = Session()
    try:
        yield session
    except DatabaseError as e:
        e.add_note('An error occurred with the database')
        logging.exception('Database error occurred %s')
        session.rollback()
        raise
    except Exception as e:
        logging.exception('General error occurred %s')
        e.add_note('General error occurred')
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        if session:
            session.close()


class Player(Base, UserMixin):
    """Player model."""

    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    password_attempts = Column(Integer, default=0)
    reset_password = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


def get_db_session() -> scoped_session:
    """Get a scoped database session."""
    if 'db_session' not in g:
        g.db_session = Session
    return g.db_session


def shutdown_db_session(e=None) -> None:
    """Remove the database session."""
    if 'db_session' in g:
        g.db_session.remove()
