from datetime import date, datetime

from project_argos.models.game_copy import GameCopy
from project_argos.models.game_session import GameSession
from project_argos.models.game_entry import GameEntry

copy = GameCopy(
    platform="PC",
    format="Digital",
    ownership_type="Owned",
)

# A. Historical session with exact timestamps: duration is calculated.
timed_session = GameSession(
    game_copy=copy,
    start_time=datetime(2026, 10, 20, 19, 0),
    end_time=datetime(2026, 10, 20, 21, 30),
)
print("Timed session:", timed_session.duration_hours(), "hours")

# B. Historical session without exact timestamps.
manual_session = GameSession(
    game_copy=copy,
    session_date=date(2026, 10, 21),
    manual_duration_hours=2.0,
)
print("Manual session:", manual_session.duration_hours(), "hours")


game = GameEntry("Test Game")

game.add_copy(copy)
game.add_session(timed_session)
game.add_session(manual_session)

print(
    "Total session hours:",
    game.total_session_hours(),
)