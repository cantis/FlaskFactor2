"""Module contains the services for the players endpoints."""

from __future__ import annotations

import bcrypt

from models import Player


class PlayerNotFoundError(Exception):
    """Custom exception for player_id not found."""

    def __init__(self, player_id: int, message: str ) -> None:
        """Initialize the exception."""
        self.player_id = player_id
        self.message = message or f'Player with id {player_id} not found!'
        super().__init__(self.message)


class PlayerAlreadyExistsError(Exception):
    """Custom exception for player already exists."""

    def __init__(self, email: str, message: str = None) -> None:
        """Initialize the exception."""
        self.email = email
        self.message = message or f'Player with email {email} already exists!'
        super().__init__(self.message)


def _hash_password(password: str) -> str:
    """Hash the password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def validate_password(session, email: str, password: str) -> bool:
    """Validate a user's password."""
    player = session(Player).filter(Player.email == email).first()
    if not player:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), player.password.encode('utf-8'))


def add_player(session, player_data) -> Player:
    """Create a new player."""
    # check if the player already exists
    player = session(Player).filter(Player.email == player_data['email']).first()
    if player:
        raise PlayerAlreadyExistsError(player_data['email'])

    # hash the password
    hashed_password = _hash_password(player_data['password'])

    # create new player
    new_player = Player(name=player_data['name'], email=player_data['email'], password=hashed_password)
    session.add(new_player)
    session.commit()
    session.refresh(new_player)  # Refresh the instance to get the updated data
    return new_player


def get_player_by_id(session, player_id: int) -> Player:
    """Get a player by id."""
    player = session(Player).filter(Player.id == player_id).first()
    if not player:
        raise PlayerNotFoundError(player_id)
    return player


def get_player_by_email(session, email: str) -> Player:
    """Get a player by email."""
    # get the player by email
    player = session(Player).filter(Player.email == email).first()
    if not player:
        raise PlayerNotFoundError()
    return player


def get_all_players(session) -> list[Player]:  # Modify the return type annotation
    """Get all players."""
    players = session.query(Player).all()
    return list(players)


def update_player(session, player_id: int, update_data: dict) -> Player:
    """Update a player."""
    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if not player:
        raise PlayerNotFoundError(player_id)

    for key, value in update_data.items():
        setattr(player, key, value)

    session.commit()
    session.refresh(player)  # Refresh the instance to get the updated data
    return player


def delete_player(session, player_id: int) -> None:
    """Delete a player by id."""
    player = session.exec(select(Player).where(Player.id == player_id)).first()
    if not player:
        raise PlayerNotFoundError(player_id)

    session.delete(player)
    session.commit()
