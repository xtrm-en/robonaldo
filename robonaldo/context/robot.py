from enum import Enum
from .entities import Rotatable
from math import pi
from rsk import field_dimensions


class Robot(Rotatable):
    def __init__(self):
        pass


class RobotDirection(Enum):
    FORWARD = 0
    LEFT = pi/2
    RIGHT = -pi/2
    BACK = pi


class RobotOwnership(Enum):
    ALLY = 'ALLY'
    ENEMY = 'ENEMY'
    ANY = 'ANY'


class RobotColor(Enum):
    GREEN = 'GREEN'
    BLUE = 'BLUE'

    def get_other(self):
        return self.BLUE if self == self.GREEN else self.GREEN
