
from tokenize import String
from project_argos.models.media_entry import MediaEntry
from project_argos.models.game_copy import GameCopy

# This GameEntry class INHERITS MediaEntry (thats why its inside the parentheses)
# so GameEntry is a specialized versin of MediaEntry. 
# Conceptually, every GameEntry is a MediaEntry, but not every MediaEntry is a GameEntry
class GameEntry(MediaEntry): 
    def __init__(self, title, entry_id = None):
          # super() refers to the parents class from the perspective of GameEntry
          # this line basically means: run the __init__ method of MediaEntry with these values
        super().__init__(title, 'game', entry_id) #as we can see, this is already a "game", which came with being a GameEntry

        self.hours_played = 0.0
        self.copies = [] #every GameEntry starts off with a empty list of copies 
        self.sessions = []



    # Eventually some parts might be moved to MediaEntry parent class
    def add_copy(self, game_copy):
        self.copies.append(game_copy)

    def add_session(self, session):
        self.sessions.append(session)

    def total_session_hours(self): #for future
        return sum(session.duration_hours() for session in self.sessions)


    ### practice functions (idk if it will be kept or not, depends)
    def add_alternative_title(self, alt_title: str):
        self.alternative_titles.append(alt_title)

    def has_alternative_title(self, alt_title: str):
        return alt_title in self.alternative_titles

    def remove_alternative_title(self, alt_title: str):
        if alt_title in self.alternative_titles:
            self.alternative_titles.remove(alt_title)
            print(f'Removed "{alt_title}" from list.')
        else:
            print('Alternative title doesnt exist')
            return

    def alt_title_count(self):
        return len(self.alternative_titles)







