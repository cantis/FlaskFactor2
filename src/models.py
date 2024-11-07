'''Database Models.'''

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from sqlite3 import DatabaseError
from typing import Generator

from flask import g
from flask_login import UserMixin
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlmodel import Field, SQLModel, create_engine

logger = logging.getLogger(__name__)


DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///flask_factor.db'
engine = create_engine(url=DATABASE_URL, echo=True)
Session = scoped_session(sessionmaker(bind=engine))


def create_db_and_tables() -> None:
    '''Create database and tables.'''
    SQLModel.metadata.create_all(engine)
    logger.info('Database and tables created')


@contextmanager
def get_session() -> Generator:
    '''Return a database session.'''
    try:
        session = Session()
        yield session
    except DatabaseError as e:
        e.add_note('An error occurred with the database')
        logging.exception('Database error occurred %s')
        raise
    except Exception as e:
        logging.exception('General error occurred %s')
        e.add_note('General error occurred')
        raise
    finally:
        if session:
            session.close()


class Player(SQLModel, UserMixin, table=True):
    '''Player model.'''

    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str
    name: str
    password_attempts: int = Field(default=0)
    reset_password: bool = Field(default=False)
    is_active: bool = Field(default=True)


def get_db_session() -> scoped_session:
    '''Get a scoped database session.'''
    if 'db_session' not in g:
        g.db_session = scoped_session(Session)
    return g.db_session


def shutdown_db_session(e=None) -> None:
    '''Remove the database session.'''
    if 'db_session' in g:
        g.db_session.remove()
