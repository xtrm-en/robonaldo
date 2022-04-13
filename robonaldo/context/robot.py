from enum import Enum
from .entities import Rotatable
from rsk import field_dimensions


class Robot(Rotatable):
    def __init__(self):
        pass


class RobotOwnership(Enum):
    ALLY = 'ALLY'
    ENEMY = 'ENEMY'


class RobotColor(Enum):
    GREEN = 'GREEN'
    BLUE = 'BLUE'

    def get_other(self):
        return self.BLUE if self == self.GREEN else self.GREEN
