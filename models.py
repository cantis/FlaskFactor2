"""Database Models."""

import os
from contextlib import contextmanager
from datetime import date
from sqlite3 import DatabaseError
from typing import Generator, List, Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)


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


class Player(SQLModel, table=True):
    """Player model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    password: str
    name: str
    characters: List['Character'] = Relationship(back_populates='player')
    campaigns: List['Campaign'] = Relationship(back_populates='players', link_model='CampaignPlayerLink')


class CampaignPlayerLink(SQLModel, table=True):
    """Link table between Campaign and Player."""

    campaign_id: Optional[int] = Field(default=None, foreign_key='campaign.id', primary_key=True)
    player_id: Optional[int] = Field(default=None, foreign_key='player.id', primary_key=True)


class Campaign(SQLModel, table=True):
    """Campaign model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    players: List[Player] = Relationship(back_populates='campaigns', link_model=CampaignPlayerLink)
    characters: List['Character'] = Relationship(back_populates='campaign')
    sessions: List['Session'] = Relationship(back_populates='campaign')


class GameSession(SQLModel, table=True):
    """Session model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    session_number: int
    date: date
    campaign_id: Optional[int] = Field(default=None, foreign_key='campaign.id')
    campaign: 'Campaign' = Relationship(back_populates='sessions')
    items: List['Item'] = Relationship(back_populates='session')


class ItemCategory(str, SQLModel):
    """Item category."""

    weapon = 'Weapon'
    armor = 'Armor'
    potion = 'Potion'
    other = 'Other'


class Item(SQLModel, table=True):
    """Item model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    value: float
    category: ItemCategory
    session_id: Optional[int] = Field(default=None, foreign_key='session.id')
    session: 'Session' = Relationship(back_populates='items')


class Character(SQLModel, table=True):
    """Character model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    retired: bool = Field(default=False)
    player_id: Optional[int] = Field(default=None, foreign_key='player.id')
    player: Player = Relationship(back_populates='characters')
    campaign_id: Optional[int] = Field(default=None, foreign_key='campaign.id')
    campaign: Campaign = Relationship(back_populates='characters')
    items: List['CharacterItem'] = Relationship(back_populates='character')


class CharacterItem(SQLModel, table=True):
    """Link table between Character and Item."""
    character_id: Optional[int] = Field(default=None, foreign_key='character.id', primary_key=True)
    item_id: Optional[int] = Field(default=None, foreign_key='item.id', primary_key=True)
    character: Character = Relationship(back_populates='items')
    item: Item = Relationship()


def seed_data():
    """Seed data."""a
    with Session(engine) as session:
        # Add seed data here
        pass
