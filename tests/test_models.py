"""Tests for models.py."""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import Session, SQLModel

from models import Player, create_db_and_tables, engine, get_session, seed_data


@pytest.fixture()
def mock_session() -> Generator[MagicMock, None, None]:
    """Mock session fixture."""
    with patch('models.get_session') as mock_get_session:
        mock_session = MagicMock()
        mock_get_session.return_value.__enter__.return_value = mock_session
        yield mock_session


def test_create_db_and_tables() -> None:
    """Test create_db_and_tables function."""
    # Act
    create_db_and_tables()

    # Assert
    assert SQLModel.metadata.tables['player'] is not None


def test_get_session(mock_session: MagicMock) -> None:
    """Test get_session context manager."""
    # Arrange
    with patch('models.Session', return_value=mock_session):
        # Act
        with get_session() as session:
            # Assert
            assert session == mock_session
            mock_session.commit.assert_not_called()
            mock_session.rollback.assert_not_called()

        # Assert after context manager exits
        mock_session.commit.assert_called_once()
        mock_session.rollback.assert_not_called()


def test_get_session_rollback_on_exception(mock_session: MagicMock) -> None:
    """Test get_session context manager rolls back on exception."""
    # Arrange
    with patch('models.Session', return_value=mock_session):
        # Act & Assert
        with pytest.raises(Exception):
            with get_session():
                raise Exception('Test exception')

        # Assert after context manager exits
        mock_session.commit.assert_not_called()
        mock_session.rollback.assert_called_once()


def test_player_model() -> None:
    """Test Player model instantiation."""
    # Arrange
    player_data = {
        'email': 'test@example.com',
        'password': 'hashedpassword',
        'name': 'Test Player',
        'password_attempts': 0,
        'reset_password': False,
        'is_active': True,
    }

    # Act
    player = Player(**player_data)

    # Assert
    assert player.email == player_data['email']
    assert player.password == player_data['password']
    assert player.name == player_data['name']
    assert player.password_attempts == player_data['password_attempts']
    assert player.reset_password == player_data['reset_password']
    assert player.is_active == player_data['is_active']


def test_seed_data() -> None:
    """Test seed_data function."""
    # Act
    seed_data()

    # Assert
    # No specific assertions as seed_data currently does nothing
    assert True
