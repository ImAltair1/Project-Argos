
from pathlib import Path
import sqlite3

from project_argos.constants import GAME_CATEGORIES


class Database: 
    def __init__(self, 
                db_path: str | Path #we give it the path manually
                ):
        #Eventually i want this path to be something that the user can set when launching
        # the app for the first time and change in the settings
        self.db_path = Path(db_path)

        # Create the parent directory if it doesn't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)


    #Opens the connection and lets us retrive values by column name and enables FK
    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)

        #Allow rows to be accessed by column name~
        connection.row_factory = sqlite3.Row

        # Enable FK enforcement for this connection
        connection.execute("PRAGMA foreign_kets = ON")

        return connection

    # Schema initialization
    def initialize(self):
        connection = self.connect()

        try:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS media_entries (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    media_type TEXT NOT NULL,
                    cover_art TEXT
                );

                CREATE TABLE IF NOT EXISTS game_entries (
                    entry_id TEXT PRIMARY KEY,
                    manual_hours_played REAL,

                    FOREIGN KEY (entry_id)
                        REFERENCES media_entries(id)
                        ON DELETE CASCADE,

                    CHECK (
                        manual_hours_played IS NULL
                        OR manual_hours_played >= 0
                    )
                );

                CREATE TABLE IF NOT EXISTS game_copies (
                    id TEXT PRIMARY KEY,
                    entry_id TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    format TEXT NOT NULL,
                    ownership_type TEXT NOT NULL,

                    FOREIGN KEY (entry_id)
                        REFERENCES game_entries(entry_id)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS alternative_titles (
                    entry_id TEXT NOT NULL,
                    position INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    PRIMARY KEY (entry_id, position),
                    FOREIGN KEY (entry_id)
                        REFERENCES media_entries(id)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS categories (
                    name TEXT PRIMARY KEY COLLATE NOCASE
                );

                CREATE TABLE IF NOT EXISTS entry_categories (
                    entry_id TEXT NOT NULL,
                    category_name TEXT NOT NULL,
                    PRIMARY KEY (entry_id, category_name),
                    FOREIGN KEY (entry_id)
                        REFERENCES media_entries(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (category_name)
                        REFERENCES categories(name)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS custom_tags (
                    name TEXT PRIMARY KEY COLLATE NOCASE
                );

                CREATE TABLE IF NOT EXISTS entry_custom_tags (
                    entry_id TEXT NOT NULL,
                    tag_name TEXT NOT NULL,
                    PRIMARY KEY (entry_id, tag_name),
                    FOREIGN KEY (entry_id)
                        REFERENCES media_entries(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (tag_name)
                        REFERENCES custom_tags(name)
                        ON DELETE CASCADE
                );
            """)

            connection.executemany( #executs the same SQL statement for each category
                "INSERT OR IGNORE INTO categories (name) VALUES (?)", #insert or ignore prevents duplicate categories
                    [(category,) for category in GAME_CATEGORIES], #(category,) supplies a one item tuple, 
                )

            connection.commit()

        finally:
            connection.close()
