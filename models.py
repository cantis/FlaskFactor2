"""Database Models."""

from __future__ import annotations

import os
from contextlib import contextmanager
from enum import Enum
from sqlite3 import DatabaseError
from typing import TYPE_CHECKING, Generator

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

if TYPE_CHECKING:
    from datetime import date

DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
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


class CampaignPlayerLink(SQLModel, table=True):
    """Link table between Campaign and Player."""

    campaign_id: int | None = Field(default=None, foreign_key='campaign.id', primary_key=True)
    player_id: int | None = Field(default=None, foreign_key='player.id', primary_key=True)


class Campaign(SQLModel, table=True):
    """Campaign model."""

    id: int | None = Field(default=None, primary_key=True)
    name: str
    players: list[Player] = Relationship(back_populates='campaigns', link_model=CampaignPlayerLink)
    characters: list[Character] = Relationship(back_populates='campaign')
    game_sessions: list[GameSession] = Relationship(back_populates='campaign')


class Player(SQLModel, table=True):
    """Player model."""

    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str
    name: str
    characters: list[Character] = Relationship(back_populates='player')
    campaigns: list[Campaign] = Relationship(back_populates='players', link_model=CampaignPlayerLink)


class ItemCategory(str, Enum):
    """Item category enum."""

    weapon = 'Weapon'
    armor = 'Armor'
    potion = 'Potion'
    other = 'Other'


class Item(SQLModel, table=True):
    """Item model."""

    id: int | None = Field(default=None, primary_key=True)
    name: str
    value: float
    category: ItemCategory
    session_id: int | None = Field(default=None, foreign_key='game_session.id')
    game_session: GameSession = Relationship(back_populates='items')
    notes: str | None = ''


class Character(SQLModel, table=True):
    """Character model."""

    id: int | None = Field(default=None, primary_key=True)
    name: str
    retired: bool = Field(default=False)
    player_id: int | None = Field(default=None, foreign_key='player.id')
    player: Player = Relationship(back_populates='characters')
    campaign_id: int | None = Field(default=None, foreign_key='campaign.id')
    campaign: Campaign = Relationship(back_populates='characters')
    items: list[CharacterItem] = Relationship(back_populates='character')


class CharacterItem(SQLModel, table=True):
    """Link table between Character and Item."""

    character_id: int | None = Field(default=None, foreign_key='character.id', primary_key=True)
    item_id: int | None = Field(default=None, foreign_key='item.id', primary_key=True)
    character: Character = Relationship(back_populates='items')
    item: Item = Relationship()


class GameSession(SQLModel, table=True):
    """Game Session model."""

    id: int | None = Field(default=None, primary_key=True)
    session_number: int
    session_date: date
    campaign_id: int | None = Field(default=None, foreign_key='campaign.id')
    campaign: Campaign = Relationship(back_populates='game_sessions')
    items: list[Item] = Relationship(back_populates='game_session')


def seed_data() -> None:
    """Seed data."""
    with Session(engine) as session:
        # Add seed data here
        pass
