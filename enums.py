from enum import Enum
class blockCode(Enum):
    BASE = -1
    BLOCK= 0
    INDENT=1
    PRINT =2
    FOR=3
    VARGET = 4
    CLASS = 5
    WHILE = 6

class dropType(Enum):
    BACKGROUND = 0
    INDENT = 1
    VARGET = 2