from uuid import uuid4 #ID system for all entries


# Media entry for library

# MediaEntry is the base abstraction, while we will then create other classes that connect to it for the specifications:
# MediaEntry
#  │
#  ├── GameEntry
#  │
#  ├── AnimeEntry
#  │
#  ├── BookEntry
#  │
#  └── MovieEntry
# A GameEntry will then inhreit everything from MediaEntry, but then have specific things in it


class MediaEntry:
    
    #method that runs when we create a new MediaEntry eg. entry = MediaEntry("Persona 5 Royal", "game")
    def __init__(self, title, media_type,
                entry_id=None, #ID when starting is empty, but in the future we'll want to give the original ID created as a parameter when the program opens up again
                ): 
        
        self.id = entry_id if entry_id is not None else str(uuid4())
        self.title = title
        self.media_type = media_type
        self.alternative_titles = [] 
        self.cover_art = None # not in the obligatory params since it may not have one
        
        #
        self.categories = []
        self.custom_tags = []




    ## repr is a special method for debugging and inspecting
    def __repr__(self): #how a print of this a MediaEntry object should look like
        return (
            f"MediaEntry("
            f"id='{self.id}', "
            f"title='{self.title}',"
            f"media_type='{self.media_type}'"
            f")"
            )

    ## another special method, how this object should look to a normal user
    def __str__(self):
        return self.title


     ### practice functions (idk if it will be kept or not, depends)
    def add_alternative_title(self, alt_title: str):
        self.alternative_titles.append(alt_title)

    def has_alternative_title(self, alt_title: str):
        return alt_title in self.alternative_titles

    def remove_alternative_title(self, alt_title: str):
        if alt_title in self.alternative_titles:
            self.alternative_titles.remove(alt_title)
            return True
        else:
            return False

    def alt_title_count(self):
        return len(self.alternative_titles)

        #####
    def add_category(self, category: str):
        if category not in self.categories:
            self.categories.append(category)
            return True
        else:
            return False 

    def has_category(self, category: str):
        return category in self.categories

    def remove_category(self, category: str):
        if category in self.categories:
            self.categories.remove(category)
            return True
        else:
            return False

    def category_count(self):
        return len(self.categories)

        #####
    def add_custom_tag(self, custom_tag: str):
        if custom_tag not in self.custom_tags:
            self.custom_tags.append(custom_tag)
            return True
        else:
            return False

    def has_custom_tag(self, custom_tag: str):
        return custom_tag in self.custom_tags

    def remove_custom_tag(self, custom_tag: str):
        if custom_tag in self.custom_tags:
            self.custom_tags.remove(custom_tag)
            return True
        else:
            return False

    def custom_tag_count(self):
        return len(self.custom_tags)

    