

# datetime is Python's built-in way of representing a date and time
#   example: start = datetime(2026, 9, 25, 19, 0) 
#           represents September 25th, 2026, at 19:00
# much better than storing this info as strings, and makes it easier to handle the data
from datetime import datetime

from uuid import uuid4

from project_argos.models.game_copy import GameCopy

class GameSession:
    def __init__(
        self,
        start_time: datetime,
        end_time: datetime,
        game_copy: GameCopy, #here we see how we can define a session and in which copy the session was done
                             # - in the future we can, for example, for the GameEntry itself, sum up the hours
                             #   for all GameCopy :)
        session_id=None,
    ):

        self.id = session_id if session_id is not None else str(uuid4())
        self.start_time = start_time
        self.end_time = end_time
        self.game_copy = game_copy

    def __repr__(self):
        return (
            f"GameSession("
            f"id='{self.id}', "
            f"start_time='{self.start_time}', "
            f"end_time='{self.end_time}', "
            f"game_copy={self.game_copy}"
            f")"
        )

    def duration_hours(self):
        duration = self.end_time - self.start_time 
        return duration.total_seconds() / 3600 

    
