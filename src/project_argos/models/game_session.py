

# datetime is Python's built-in way of representing a date and time
#   example: start = datetime(2026, 9, 25, 19, 0) 
#           represents September 25th, 2026, at 19:00
# much better than storing this info as strings, and makes it easier to handle the data
from datetime import date, datetime
from uuid import uuid4

from project_argos.models.game_copy import GameCopy


class GameSession:
    def __init__(
        self,
        game_copy: GameCopy,
        session_date: date | None = None,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        manual_duration_hours: float | None = None,
        session_id: str | None = None,
    ):
        # A session cannot have an end time without a start time.
        if end_time is not None and start_time is None:
            raise ValueError("An end time requires a start time.")

        if start_time is not None:
            if manual_duration_hours is not None:
                raise ValueError("Use timestamps or a manual duration, not both.")

            if session_date is None:
                session_date = start_time.date()
            elif session_date != start_time.date():
                raise ValueError("The session date must match the start date.")

            if end_time is not None and end_time < start_time:
                raise ValueError("End time cannot precede start time.")


        self.id = session_id if session_id is not None else str(uuid4())
        self.game_copy = game_copy
        self.session_date = session_date
        self.start_time = start_time
        self.end_time = end_time
        self.manual_duration_hours = manual_duration_hours


    def __repr__(self):
        return (
            f"GameSession("
            f"id='{self.id}', "
            f"start_time='{self.start_time}', "
            f"end_time='{self.end_time}', "
            f"game_copy={self.game_copy}, "
            f")"
        )

    def duration_hours(self) -> float:
        # If there are no timestamps, use the manually entered duration.
        if self.start_time is None:
            return self.manual_duration_hours

        # If the session is still running, use the current time.
        effective_end = self.end_time

        if effective_end is None:
            effective_end = datetime.now(tz=self.start_time.tzinfo)

        duration = effective_end - self.start_time
        return duration.total_seconds() / 3600

    
