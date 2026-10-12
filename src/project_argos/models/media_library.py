from project_argos.models.media_entry import MediaEntry


# Will manage the data side of things for the Library
# This is being done initially to better manage the custom tags, which are managed by the user
class MediaLibrary:
    def __init__(
        self,
        entries: list[MediaEntry] | None = None, #list of all library entries
        available_custom_tags: list[str] | None = None, # list of available custom tags - for importing in the future
    ): #eventaully i assume we will have more stuff on here
        
        
        # The entries belonging to this library
        self.entries = entries if entries is not None else []

        # The custom tags available throughout this library
        if available_custom_tags is not None:
            self.available_custom_tags = list(available_custom_tags)
        else:
            # Preserve existing tags assigned to entries
            self.available_custom_tags = []

            for entry in self.entries:
                for tag in entry.custom_tags:
                    if not any(
                        existing.casefold() == tag.casefold()
                        for existing in self.available_custom_tags
                    ):
                        self.available_custom_tags.append(tag)

        self.available_custom_tags.sort(key=str.casefold)


    #### Custom tag related methods #####
    def add_custom_tag(self, tag: str) -> bool:
        tag = tag.strip() #remove spaces

        if not tag:
            return False

        # Don't allow duplicates, even with different capitalization.
        if any(
            existing.casefold() == tag.casefold()
            for existing in self.available_custom_tags
        ):
            return False

        self.available_custom_tags.append(tag)
        self.available_custom_tags.sort(key=str.casefold) #sort alphabetically aswell

        return True #return true when new tag is added or false when input is blank or tag already exists

    def remove_custom_tag(self, tag: str) -> bool:
        # Find the existing tag, ignoring capitalization.
        existing_tag = next(
            (
                existing
                for existing in self.available_custom_tags
                if existing.casefold() == tag.casefold()
            ),
            None,
        )

        if existing_tag is None:
            return False

        # Remove it from the shared collection.
        self.available_custom_tags.remove(existing_tag)

        # Remove its assignments from every entry.
        for entry in self.entries:
            entry.custom_tags[:] = [
                assigned_tag
                for assigned_tag in entry.custom_tags
                if assigned_tag.casefold() != existing_tag.casefold()
            ]

        return True
