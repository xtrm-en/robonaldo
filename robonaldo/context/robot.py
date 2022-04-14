from enum import Enum
from .entities import Rotatable
from math import pi
from rsk import Client, field_dimensions


class RobotOwnership(Enum):
    ALLY = 'ALLY'
    ENEMY = 'ENEMY'
    ANY = 'ANY'


class RobotColor(Enum):
    GREEN = 'GREEN'
    BLUE = 'BLUE'

    def get_other(self) -> 'RobotColor':
        return self.BLUE if self == self.GREEN else self.GREEN


class Robot(Rotatable):
    def __init__(self, position: (float, float), rotation: float, color: RobotColor, index: int):
        super().__init__(position, rotation)
        self.color = color
        self.index = index

    def update(self, client: Client) -> None:
        robot = client.robots[self.color.name][self.index]
        if robot is None or robot.position is None or robot.rotation is None: return
        super().update(robot.position, robot.rotation)
