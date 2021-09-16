from enum import Enum

class GameStatus(Enum):
    InProgress = "0"
    Final = "1"
    Scheduled = "2"
    Postponed = "3"
    Cancelled = "4"