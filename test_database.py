
from pathlib import Path
from tempfile import TemporaryDirectory

from project_argos.demo_data import create_demo_entries
from project_argos.models.game_copy import GameCopy
from project_argos.models.media_library import MediaLibrary
from project_argos.persistence.database import Database
from project_argos.persistence.library_repository import LibraryRepository

from datetime import date, datetime
from project_argos.models.game_session import GameSession

with TemporaryDirectory() as folder:
    # Create a temporary database for this test.
    database = Database(Path(folder) / "test.sqlite3")
    database.initialize()
    repository = LibraryRepository(database)

    # Check that the expected tables exist.
    connection = database.connect()

    try:
        tables = {
            row["name"]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """
            ).fetchall()
        }
    finally:
        connection.close()

    expected_tables = {
        "media_entries",
        "alternative_titles",
        "categories",
        "entry_categories",
        "custom_tags",
        "entry_custom_tags",
        "game_entries",
        "game_copies",
        "game_sessions",
    }

    assert expected_tables.issubset(tables), (
        f"Missing database tables: {expected_tables - tables}"
    )

    # Create test data.
    library = MediaLibrary(entries=create_demo_entries())

    p5r = next(
        entry
        for entry in library.entries
        if entry.title == "Persona 5 Royal"
    )

    p5r.manual_hours_played = 120.5

    p5r_copy = GameCopy(
        platform="PC",
        format="Digital",
        ownership_type="Owned",
    )
    p5r.add_copy(p5r_copy)

    # Session with exact start and end times: 2.5 hours
    p5r.add_session(
        GameSession(
            game_copy=p5r_copy,
            start_time=datetime(2026, 10, 20, 19, 0),
            end_time=datetime(2026, 10, 20, 21, 30),
        )
    )

    # Historical session with a manually entered duration: 2 hours
    p5r.add_session(
        GameSession(
            game_copy=p5r_copy,
            session_date=date(2026, 10, 21),
            manual_duration_hours=2.0,
        )
    )


    # Test a shared tag that no entry uses.
    library.add_custom_tag("Comfort game")

    # Save and load the library.
    repository.save_library(library)
    connection = database.connect()
    try:
        rows = connection.execute(
            """
            SELECT
                session_date,
                start_time,
                end_time,
                manual_duration_hours
            FROM game_sessions
            ORDER BY session_date
            """
        ).fetchall()

        print("Saved sessions:")

        for row in rows:
            print(
                f"- Date: {row['session_date']}, "
                f"Start: {row['start_time']}, "
                f"End: {row['end_time']}, "
                f"Manual duration: {row['manual_duration_hours']}"
            )

    finally:
        connection.close()
    loaded_library = repository.load_library()

    # Verify entries and relationships were restored.
    assert len(loaded_library.entries) == 8

    loaded_p5r = next(
        entry
        for entry in loaded_library.entries
        if entry.title == "Persona 5 Royal"
    )

    assert loaded_p5r.id == p5r.id
    assert loaded_p5r.alternative_titles == ["P5R"]
    assert loaded_p5r.categories == ["JRPG"]
    assert "Persona series" in loaded_p5r.custom_tags
    assert loaded_p5r.manual_hours_played == 120.5

    assert len(loaded_p5r.sessions) == 2

    loaded_durations = sorted(
        session.duration_hours()
        for session in loaded_p5r.sessions
    )

    assert loaded_durations == [2.0, 2.5]

    print("Loaded P5R session durations:", loaded_durations)

    assert len(loaded_p5r.copies) == 1

    loaded_copy = loaded_p5r.copies[0]

    assert loaded_copy.id == p5r_copy.id
    assert loaded_copy.platform == "PC"
    assert loaded_copy.format == "Digital"
    assert loaded_copy.ownership_type == "Owned"

    assert "Comfort game" in loaded_library.available_custom_tags
    assert not any(
        "Comfort game" in entry.custom_tags
        for entry in loaded_library.entries
    )

    # Verify that deleting an entry is reflected in SQLite.
    removed_entry = library.entries.pop()
    repository.save_library(library)

    library_after_deletion = repository.load_library()

    assert len(library_after_deletion.entries) == 7
    assert all(
        entry.id != removed_entry.id
        for entry in library_after_deletion.entries
    )

    print("All database and repository checks passed!")
