

from project_argos.models.media_library import MediaLibrary
from project_argos.persistence.database import Database

from project_argos.models.game_entry import GameEntry
from project_argos.models.media_entry import MediaEntry

class LibraryRepository:
    def __init__(self, database: Database): #receive database obj
        self.database = database


    def save_library(self, library: MediaLibrary) -> None:
        entries = library.entries
        connection = self.database.connect()

        try:
            with connection:
                ### ADD ALL THE BASE MEDIAENTRY INFO INTO THE TABLES
                connection.executemany(
                    """
                    INSERT INTO media_entries (
                        id, title, media_type, cover_art
                    )
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET 
                        title = excluded.title,
                        media_type = excluded.media_type,
                        cover_art = excluded.cover_art
                    """, # CONFLICT part basically means that if the id already exists it updates with the new info given
                    [
                        (
                            entry.id,
                            entry.title,
                            entry.media_type,
                            entry.cover_art,
                        )
                        for entry in entries
                    ],
                )

                ### POPULATE THE ALT TITLES TABLES
                for entry in entries:
                    ## we delete first and populate again so that if we remove alt titles 
                    ## it gets updated normally

                    # Remove the previously saved alternative titles
                    connection.execute(
                        "DELETE FROM alternative_titles WHERE entry_id = ?",
                        (entry.id,),
                    )

                    # Save the current alternative titles in their original order
                    connection.executemany(
                        """
                        INSERT INTO alternative_titles (entry_id, position, title)
                        VALUES (?, ?, ?)
                        """,
                        [
                            (entry.id, position, title)
                            for position, title in enumerate(entry.alternative_titles)
                        ],
                    )

                ### POPULATE THE CATEGORIES TABLE 
                for entry in entries:
                    # Remove the previously saved category assignments
                    connection.execute(
                        "DELETE FROM entry_categories WHERE entry_id = ?",
                        (entry.id,),
                    )

                    # Save the current category assignments
                    connection.executemany(
                        """
                        INSERT INTO entry_categories (
                            entry_id, category_name
                        )
                        VALUES (?, ?)
                        """,
                        [
                            (entry.id, category)
                            for category in entry.categories
                        ],
                    )

                ### POPULATE CUSTOM TAGS TABLE
                # Find tags that have been deleted from the library
                available_tags = {
                    tag.casefold()
                    for tag in library.available_custom_tags
                }

                stored_tags = connection.execute(
                    "SELECT name FROM custom_tags"
                ).fetchall()

                    # delete custom tags if they arent in available tags
                for row in stored_tags:
                    if row["name"].casefold() not in available_tags:
                        connection.execute(
                            "DELETE FROM custom_tags WHERE name = ?",
                            (row["name"],),
                        )

                # Insert any tags that aren't already stored
                connection.executemany(
                    """
                    INSERT INTO custom_tags (name)
                    VALUES (?)
                    ON CONFLICT(name) DO NOTHING
                    """,
                    [(tag,) for tag in library.available_custom_tags],
                )
                # Update the custom tags assigned to each entry
                for entry in entries:
                    connection.execute(
                        "DELETE FROM entry_custom_tags WHERE entry_id = ?",
                        (entry.id,),
                    )

                    connection.executemany(
                        """
                        INSERT INTO entry_custom_tags (entry_id, tag_name)
                        VALUES (?, ?)
                        """,
                        [
                            (entry.id, tag)
                            for tag in entry.custom_tags
                        ],
                    )
                
        finally:
            connection.close()

    # Populate Python side data from database
    def load_media_entries(self) -> list[MediaEntry]:
        connection = self.database.connect()

        try:
            rows = connection.execute(
                """
                SELECT id, title, media_type, cover_art
                FROM media_entries
                ORDER BY title
                """
            ).fetchall()

            entries = []

            for row in rows:
                # Reconstruct the appropriate model type.
                if row["media_type"] == "game":
                    entry = GameEntry(
                        row["title"],
                        entry_id=row["id"],
                    )
                else:
                    entry = MediaEntry(
                        row["title"],
                        row["media_type"],
                        entry_id=row["id"],
                    )

                entry.cover_art = row["cover_art"]
                entries.append(entry)



            # Map each entry ID to its Python object.
            entries_by_id = {
                entry.id: entry
                for entry in entries
            }

            # Load all alternative titles in their original order.
            rows = connection.execute(
                """
                SELECT entry_id, title
                FROM alternative_titles
                ORDER BY entry_id, position
                """
            ).fetchall()

            for row in rows:
                entry = entries_by_id.get(row["entry_id"])

                if entry is not None:
                    entry.alternative_titles.append(row["title"])


            ### CATEGORY STUFF
            # Load category assignments.
            rows = connection.execute(
                """
                SELECT entry_id, category_name
                FROM entry_categories
                ORDER BY entry_id, category_name
                """
            ).fetchall()

            for row in rows:
                entry = entries_by_id.get(row["entry_id"])

                if entry is not None:
                    entry.add_category(row["category_name"])


            ### CUSTOM TAG STUFF
            # Load custom-tag assignments
            rows = connection.execute(
                """
                SELECT entry_id, tag_name
                FROM entry_custom_tags
                ORDER BY entry_id, tag_name
                """
            ).fetchall()

            for row in rows:
                entry = entries_by_id.get(row["entry_id"])

                if entry is not None:
                    entry.add_custom_tag(row["tag_name"])


            return entries


        finally:
            connection.close()
        

    def load_library(self) -> MediaLibrary:
        entries = self.load_media_entries()

        connection = self.database.connect()

        try:
            rows = connection.execute(
                """
                SELECT name
                FROM custom_tags
                ORDER BY name
                """
            ).fetchall()

            available_custom_tags = [
                row["name"] for row in rows
            ]

        finally:
            connection.close()

        return MediaLibrary(
            entries=entries,
            available_custom_tags=available_custom_tags,
        )
        
