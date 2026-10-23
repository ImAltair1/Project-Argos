

from project_argos.models.media_library import MediaLibrary
from project_argos.persistence.database import Database

from project_argos.models.game_entry import GameEntry
from project_argos.models.media_entry import MediaEntry
from project_argos.models.game_copy import GameCopy


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

                # Find the IDs that currently belong to the library.
                current_entry_ids = {
                    entry.id for entry in entries
                }
                #print("DEBUG: Entries passed to save:", len(entries))

                # Find entries that are still stored in the database.
                stored_entries = connection.execute(
                    "SELECT id, title FROM media_entries"
                ).fetchall()

                #print("DEBUG: Entries currently in database:", len(stored_entries))

                # Delete entries that are no longer in the library.
                for row in stored_entries:
                    if row["id"] not in current_entry_ids:
                        #print("DEBUG: Deleting entry:", row["title"])
                        connection.execute(
                            "DELETE FROM media_entries WHERE id = ?",
                            (row["id"],),
                        )


                # Save game-specific data
                for entry in entries:
                    if isinstance(entry, GameEntry):
                        connection.execute(
                            """
                            INSERT INTO game_entries (
                                entry_id, manual_hours_played
                            )
                            VALUES (?, ?)
                            ON CONFLICT(entry_id) DO UPDATE SET
                                manual_hours_played = excluded.manual_hours_played
                            """,
                            (entry.id, entry.manual_hours_played),
                        )

                # Save the copies belonging to each game.
                for entry in entries:
                    if not isinstance(entry, GameEntry):
                        continue

                    for copy in entry.copies:
                        connection.execute(
                            """
                            INSERT INTO game_copies (
                                id,
                                entry_id,
                                platform,
                                format,
                                ownership_type
                            )
                            VALUES (?, ?, ?, ?, ?)
                            ON CONFLICT(id) DO UPDATE SET
                                entry_id = excluded.entry_id,
                                platform = excluded.platform,
                                format = excluded.format,
                                ownership_type = excluded.ownership_type
                            """,
                            (
                                copy.id,
                                entry.id,
                                copy.platform,
                                copy.format,
                                copy.ownership_type,
                            ),
                        )

                # Remove copies no longer present in the library.
                current_copy_ids = {
                    copy.id
                    for entry in entries
                    if isinstance(entry, GameEntry)
                    for copy in entry.copies
                }

                stored_copies = connection.execute(
                    "SELECT id FROM game_copies"
                ).fetchall()

                for row in stored_copies:
                    if row["id"] not in current_copy_ids:
                        connection.execute(
                            "DELETE FROM game_copies WHERE id = ?",
                            (row["id"],),
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

            # Load game copies from the database.
            rows = connection.execute(
                """
                SELECT id, entry_id, platform, format, ownership_type
                FROM game_copies
                ORDER BY id
                """
            ).fetchall()

            for row in rows:
                entry = entries_by_id.get(row["entry_id"])

                if isinstance(entry, GameEntry):
                    game_copy = GameCopy(
                        platform=row["platform"],
                        format=row["format"],
                        ownership_type=row["ownership_type"],
                        copy_id=row["id"],
                    )

                    entry.add_copy(game_copy)

            # Load game-specific data
            rows = connection.execute(
                """
                SELECT entry_id, manual_hours_played
                FROM game_entries
                """
            ).fetchall()

            for row in rows:
                entry = entries_by_id.get(row["entry_id"])

                if isinstance(entry, GameEntry):
                    entry.manual_hours_played = row["manual_hours_played"]


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
        
