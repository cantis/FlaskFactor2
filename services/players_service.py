"""Module contains the services for the players endpoints."""

from __future__ import annotations

from sqlmodel import select

from models import Player, get_session


class PlayerNotFoundError(Exception):
    """Custom exception for player not found."""

    def __init__(self, player_id) -> None:
        """Initialize the exception."""
        self.player_id = player_id
        self.message = f'Player with id {player_id} not found'
        super().__init__(self.message)


class PlayerAlreadyExistsError(Exception):
    """Custom exception for player already exists."""

    def __init__(self, email) -> None:
        """Initialize the exception."""
        self.email = email
        self.message = f'Player with email {email} already exists'
        super().__init__(self.message)


def add_player(player_data) -> Player:
    """Create a new player."""
    with get_session() as session:
        # check if the player already exists
        player = session.exec(select(Player).where(Player.email == player_data['email'])).first()
        if player:
            raise PlayerAlreadyExistsError(player_data['email'])

        # create new player
        new_player = Player(name=player_data['name'], email=player_data['email'], password=player_data['password'])
        session.add(new_player)
        session.commit()
        session.refresh(new_player)  # Refresh the instance to get the updated data
        return new_player


def get_player(player_id) -> Player:
    """Get a player by id."""
    with get_session() as session:
        player = session.exec(select(Player).where(Player.id == player_id)).first()
        if not player:
            raise PlayerNotFoundError(player_id)
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
