"""Module contains the services for the players endpoints."""

from __future__ import annotations

import bcrypt
from sqlmodel import select

from models import Player, get_session


class PlayerNotFoundError(Exception):
    """Custom exception for player_id not found."""

    def __init__(self, player_id) -> None:
        """Initialize the exception."""
        self.player_id = player_id
        self.message = f'Player with id {player_id} not found!'
        super().__init__(self.message)


class PlayerAlreadyExistsError(Exception):
    """Custom exception for player already exists."""

    def __init__(self, email) -> None:
        """Initialize the exception."""
        self.email = email
        self.message = f'Player with email {email} already exists!'
        super().__init__(self.message)


def hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def validate_password(email: str, password: str) -> bool:
    """Validate a user's password."""
    with get_session() as session:
        player = session.exec(select(Player).where(Player.email == email)).first()
        if not player:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), player.password.encode('utf-8'))


def add_player(player_data) -> Player:
    """Create a new player."""
    with get_session() as session:
        # check if the player already exists
        player = session.exec(select(Player).where(Player.email == player_data['email'])).first()
        if player:
            raise PlayerAlreadyExistsError(player_data['email'])

        # hash the password
        hashed_password = hash_password(player_data['password'])

        # create new player
        new_player = Player(name=player_data['name'], email=player_data['email'], password=hashed_password)
        session.add(new_player)
        session.commit()
        session.refresh(new_player)  # Refresh the instance to get the updated data
        return new_player


def get_player_by_id(player_id) -> Player:
    """Get a player by id."""
    with get_session() as session:
        player = session.exec(select(Player).where(Player.id == player_id)).first()
        if not player:
            raise PlayerNotFoundError(player_id)
        return player


def get_player_by_email(email: str) -> Player:
    """Get a player by email."""
    with get_session() as session:
        player = session.exec(select(Player).where(Player.email == email)).first()
        if not player:
            raise PlayerNotFoundError(email)
        return player


def get_all_players() -> list[Player]:  # Modify the return type annotation
    """Get all players."""
    with get_session() as session:
        players = session.exec(select(Player)).all()
        return list(players)


def update_player(player_id: int, update_data: dict) -> Player:
    """Update a player."""
    with get_session() as session:
        player = session.exec(select(Player).where(Player.id == player_id)).first()
        if not player:
            raise PlayerNotFoundError(player_id)

        for key, value in update_data.items():
            setattr(player, key, value)

        session.commit()
        session.refresh(player)  # Refresh the instance to get the updated data
        return player


def delete_player(player_id) -> None:
    """Delete a player by id."""
    with get_session() as session:
        player = session.exec(select(Player).where(Player.id == player_id)).first()
        if not player:
            raise PlayerNotFoundError(player_id)

        session.delete(player)
        session.commit()
