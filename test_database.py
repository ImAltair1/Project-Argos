from pathlib import Path
from tempfile import TemporaryDirectory

from project_argos.demo_data import create_demo_entries
from project_argos.persistence.database import Database
from project_argos.persistence.library_repository import LibraryRepository
from project_argos.models.media_library import MediaLibrary

with TemporaryDirectory() as folder:
    database = Database(Path(folder) / "test.sqlite3")
    database.initialize()

    repository = LibraryRepository(database)

    entries = create_demo_entries()
    media_library = MediaLibrary(entries=entries)

    #test
    media_library.add_custom_tag("Comfort game")

    repository.save_library(media_library)

    loaded_library = repository.load_library()
    loaded_entries = loaded_library.entries

    print(f"Loaded {len(loaded_entries)} media entries:")
    for entry in loaded_entries:
        print(f"- {entry.title} ({type(entry).__name__})")

    print("Loaded alternative titles:")
    for entry in loaded_entries:
        if entry.alternative_titles:
            print(f"- {entry.title}: {', '.join(entry.alternative_titles)}")

    print("Loaded categories:")
    for entry in loaded_entries:
        if entry.categories:
            print(f"- {entry.title}: {', '.join(entry.categories)}")


    print("Loaded custom tags:")
    for entry in loaded_entries:
        if entry.custom_tags:
            print(f"- {entry.title}: {', '.join(entry.custom_tags)}")

    print("All available custom tags:")
    for tag in loaded_library.available_custom_tags:
        print(f"- {tag}")



    print("STARTING CONNECTION TO DATABASE")
    # Read the saved rows directly from SQLite for verification
    connection = database.connect()
    print("DATABASE CONNECTED")
    try:
        rows = connection.execute(
            """
            SELECT e.title AS entry_title, a.title AS alternative_title
            FROM alternative_titles AS a
            JOIN media_entries AS e ON e.id = a.entry_id
            ORDER BY e.title, a.position
            """
        ).fetchall()

        print("Alternative titles:")
        for row in rows:
            print(f"- {row['entry_title']}: {row['alternative_title']}")

        
        rows = connection.execute(
            """
            SELECT e.title AS entry_title,
                   ec.category_name AS category
            FROM entry_categories AS ec
            JOIN media_entries AS e ON e.id = ec.entry_id
            ORDER BY e.title, ec.category_name
            """
        ).fetchall()

        print("Entry categories:")
        for row in rows:
            print(f"- {row['entry_title']}: {row['category']}")


        tags = connection.execute(
            "SELECT name FROM custom_tags ORDER BY name"
        ).fetchall()

        print("Available custom tags:")
        for row in tags:
            print("-", row["name"])


        assignments = connection.execute(
            """
            SELECT e.title AS entry_title, ect.tag_name AS tag
            FROM entry_custom_tags AS ect
            JOIN media_entries AS e ON e.id = ect.entry_id
            ORDER BY e.title, ect.tag_name
            """
        ).fetchall()

        print("Custom tag assignments:")
        for row in assignments:
            print(f"- {row['entry_title']}: {row['tag']}")

    finally:
        connection.close()
