"""Players service tests."""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from models import Player
from services.players_service import (
    PlayerAlreadyExistsError,
    PlayerNotFoundError,
    add_player,
    delete_player,
    get_player_by_email,
    get_player_by_id,
    hash_password,
    update_player,
    validate_password,
)

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
        email=player_data['email'],
        name=player_data['name'],
        password=player_data['password'],
    )

    # Assert
    with pytest.raises(PlayerAlreadyExistsError):
        add_player(player_data)


def test_get_player_by_email_ok(mock_session: MagicMock) -> None:
    """Test get player by email."""
    # Arrange
    email = 'test@example.com'
    player_name = 'Test Player'
    player = Player(email=email, name=player_name, password='hashedpassword')  # noqa: S106
    mock_session.exec.return_value.first.return_value = player

    # Act
    result = get_player_by_email(email)

    # Assert
    assert result.email == email
    assert result.name == player_name
    mock_session.exec.assert_called_once()


def test_get_player_by_email_not_found(mock_session: MagicMock) -> None:
    """Test get player by email not found."""
    # Arrange
    email = 'nonexistent@example.com'
    mock_session.exec.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(PlayerNotFoundError):
        get_player_by_email(email)
    mock_session.exec.assert_called_once()


def test_get_player_by_id_ok(mock_session: MagicMock) -> None:
    """Test get player by id."""
    # Arrange
    player_id = 1
    player_name = 'Test Player'
    email = 'test@example.com'
    player = Player(id=player_id, email=email, name=player_name, password='hashedpassword')  # noqa: S106
    mock_session.exec.return_value.first.return_value = player

    # Act
    result = get_player_by_id(player_id)

    # Assert
    assert result.id == player_id
    assert result.email == email
    assert result.name == player_name
    mock_session.exec.assert_called_once()


def test_get_player_by_id_not_found(mock_session: MagicMock) -> None:
    """Test get player by id not found."""
    # Arrange
    player_id = 999
    mock_session.exec.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(PlayerNotFoundError):
        get_player_by_id(player_id)
    mock_session.exec.assert_called_once()


def test_update_player_ok(mock_session: MagicMock) -> None:
    """Test update player."""
    # Arrange
    player_id = 1
    update_data = {'name': 'Updated Player', 'email': 'updated@example.com'}
    player = Player(id=player_id, email='test@example.com', name='Test Player', password='hashedpassword')
    mock_session.exec.return_value.first.return_value = player

    # Act
    updated_player = update_player(player_id, update_data)

    # Assert
    assert updated_player.id == player_id
    assert updated_player.name == update_data['name']
    assert updated_player.email == update_data['email']
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


def test_update_player_not_found(mock_session: MagicMock) -> None:
    """Test update player not found."""
    # Arrange
    player_id = 999
    update_data = {'name': 'Updated Player', 'email': 'updated@example.com'}
    mock_session.exec.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(PlayerNotFoundError):
        update_player(player_id, update_data)
    mock_session.exec.assert_called_once()


def test_delete_player_ok(mock_session: MagicMock) -> None:
    """Test delete player."""
    # Arrange
    player_id = 1
    player = Player(id=player_id, email='test@example.com', name='Test Player', password='hashedpassword')
    mock_session.exec.return_value.first.return_value = player

    # Act
    delete_player(player_id)

    # Assert
    mock_session.delete.assert_called_once_with(player)
    mock_session.commit.assert_called_once()


def test_delete_player_not_found(mock_session: MagicMock) -> None:
    """Test delete player not found."""
    # Arrange
    player_id = 999
    mock_session.exec.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(PlayerNotFoundError):
        delete_player(player_id)
    mock_session.exec.assert_called_once()
