"""Players service tests."""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from models import Player
from services.players_service import PlayerAlreadyExistsError, add_player, hash_password, validate_password

# ruff: noqa: S105 - Ignore password warnings in this file


@pytest.fixture()
def mock_session() -> Generator[MagicMock, None, None]:
    """Mock session fixture."""
    with patch('services.players_service.get_session') as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        yield mock_session


def test_hash_password() -> None:
    """Test hash password."""
    # Arrange
    password = 'securepassword'

    # Act
    hashed_password = hash_password(password)

    # Assert
    assert password != hashed_password
    assert hashed_password.startswith('$2b$')


def test_validate_password(mock_session: MagicMock) -> None:
    """Test validate password."""
    # Arrange
    email = 'test@example.com'
    password = 'securepassword'
    player_name = 'Test Player'

    # Act
    hashed_password = hash_password(password)
    mock_session.exec.return_value.first.return_value = Player(email=email, name=player_name, password=hashed_password)

    # Assert
    assert validate_password(email, password)
    assert not validate_password(email, 'wrongpassword')


def test_add_player(mock_session: MagicMock) -> None:
    """Test add player."""
    # Arrange
    player_data = {'name': 'Test Player', 'email': 'test@example.com', 'password': 'securepassword'}
    mock_session.exec.return_value.first.return_value = None

    # Act
    new_player = add_player(player_data)

    # Assert
    assert new_player.name == player_data['name']
    assert new_player.email == player_data['email']
    assert new_player.password != player_data['password']
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_add_player_already_exists(mock_session: MagicMock) -> None:
    """Test add player already exists."""
    # Arrange
    player_data = {'name': 'Test Player', 'email': 'test@example.com', 'password': 'securepassword'}

    # Act
    mock_session.exec.return_value.first.return_value = Player(
        email=player_data['email'], name=player_data['name'], password=player_data['password'],
    )

    # Assert
    with pytest.raises(PlayerAlreadyExistsError):
        add_player(player_data)
