import sqlite3


def create_table_and_user_if_nexists(connection: sqlite3.Connection) -> None:
    """Create the table and a user if they don't exist yet."""
    connection.execute("""
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY CHECK (id = 1),  -- ensure there's only 1 user
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

def cursor(connection: sqlite3.Connection) -> sqlite3.Cursor:
    """Return a database cursor."""
    return connection.cursor()


def get_highest_streak(connection: sqlite3.Connection) -> int:
    """Return the stored highest streak value."""
    row = connection.execute(
        """SELECT highest_streak FROM User WHERE id = 1""",
    )
    return row.fetchone()[0]

def set_highest_streak(connection: sqlite3.Connection, highest_streak: int) -> None:
    """Store the given highest streak value."""
    connection.execute(
        """UPDATE User SET highest_streak = ? WHERE id = 1""",
        (highest_streak,)
    )
    connection.commit()


def get_show_kana_reading(connection: sqlite3.Connection) -> bool:
    """Set whether to show the kana reading."""
    row = connection.execute(
        """SELECT show_kana_reading FROM User WHERE id = 1""",
    )
    return row.fetchone()[0]

def set_show_kana_reading(connection: sqlite3.Connection, show_kana: bool) -> None:
    """Set whether to show the kana reading."""
    connection.execute(
        """UPDATE User SET show_kana_reading = ? WHERE id = 1""",
        (show_kana,)
    )
    connection.commit()


def get_show_word_type(connection: sqlite3.Connection) -> bool:
    """Set whether to show the kana reading."""
    row = connection.execute(
        """SELECT show_word_type FROM User WHERE id = 1""",
    )
    return row.fetchone()[0]

def set_show_word_type(connection: sqlite3.Connection, show_word_type: bool) -> None:
    """Set whether to show the word type."""
    connection.execute(
        """UPDATE User SET show_word_type = ? WHERE id = 1""",
        (show_word_type,)
    )
    connection.commit()
