import sqlite3

import pytest

import dbapi


@pytest.fixture
def connection_empty_db() -> sqlite3.Connection:
    """Return a connection to an empty in-memory database."""
    return sqlite3.connect(':memory:')


@pytest.fixture
def connection() -> sqlite3.Connection:
    """Return a connection to an in-memory database with a user already created."""
    connection = sqlite3.connect(':memory:')
    connection.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            highest_streak INT NOT NULL,
            show_kana_reading BOOLEAN NOT NULL,
            show_word_type BOOLEAN NOT NULL
        )
    """)
    user = connection.execute("""SELECT id from User where id = 1""")
    if not user.fetchone():
        connection.execute(
            """
                INSERT INTO User (
                    highest_streak, show_kana_reading, show_word_type
                ) VALUES (
                    ?, ?, ?
                )
            """,
            (0, True, True)
        )
    connection.commit()
    return connection


def test_create_table_and_user_if_nexists(connection_empty_db: sqlite3.Connection):
    dbapi.create_table_and_user_if_nexists(connection_empty_db)
    result = connection_empty_db.execute("""SELECT id FROM User where id=1""")
    row = result.fetchone()
    assert row[0] == 1


def test_get_highest_streak(connection: sqlite3.Connection):
    connection.execute(
        """UPDATE User set highest_streak = 123 where id=1"""
    )
    highest_streak = dbapi.get_highest_streak(connection)
    assert highest_streak == 123

def test_set_highest_streak(connection: sqlite3.Connection) -> None:
    """Store the given highest streak value."""
    dbapi.set_highest_streak(connection, 123)
    result = connection.execute("""SELECT highest_streak FROM User WHERE id = 1""")
    row = result.fetchone()
    highest_streak = row[0]
    assert highest_streak == 123


def test_get_show_kana_reading(connection: sqlite3.Connection):
    connection.execute(
        """UPDATE User set show_kana_reading = FALSE where id=1"""
    )
    show_kana_reading = dbapi.get_show_kana_reading(connection)
    assert not show_kana_reading

def test_set_show_kana_reading(connection: sqlite3.Connection) -> None:
    dbapi.set_show_kana_reading(connection, False)
    result = connection.execute("""SELECT show_kana_reading FROM User WHERE id = 1""")
    row = result.fetchone()
    show_kana_reading = row[0]
    assert not show_kana_reading


def test_get_show_word_type(connection: sqlite3.Connection):
    connection.execute(
        """UPDATE User set show_word_type = FALSE where id=1"""
    )
    show_word_type = dbapi.get_show_word_type(connection)
    assert not show_word_type

def test_set_show_word_type(connection: sqlite3.Connection) -> None:
    dbapi.set_show_word_type(connection, False)
    result = connection.execute("""SELECT show_word_type FROM User WHERE id = 1""")
    row = result.fetchone()
    show_word_type = row[0]
    assert not show_word_type
