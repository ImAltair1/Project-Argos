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

    def __init__(self, title, media_type): #method that runs when we create a new MediaEntry eg. entry = MediaEntry("Persona 5 Royal", "game")
        self.title = title
        self.media_type = media_type

        # important python concept = storing a collection of data inside an object
        # this is in __init__ so that every time we create a new MediaEntry, each new object has its seperate alt_titles list
        # if we put outsode the __init__ method, right above the "def __init__" line, it would become a class attr, which is different from a instance attr
        # which, for example, would mean all objects would have the same list - if we add P5R to entry1, entry2 would also have it added aswell
        # self.something = belongs to this specific OBJECT / ClassName.something = belongs to the class itself, to ALL objects
        self.alternative_titles = [] 

    ## repr is a special method for debugging and inspecting
    def __repr__(self): #how a print of this a MediaEntry object should look like
        return f"MediaEntry(title='{self.title}', media_type='{self.media_type}')"

    ## another special method, how this object should look to a normal user
    def __str__(self):
        return self.title