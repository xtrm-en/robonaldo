from typing import List
from .entities import Positionable
from .robot import Robot

class Terrain(Positionable):
    def __init__(self, x, y, width, height):
        super().__init__((x, y))
        self.width = width
        self.height = height


class Ball(Positionable):
    def __init__(self, position: (float, float)):
        super().__init__(position)


class GameContext():
    @staticmethod
    def empty() -> 'GameContext':
        return GameContext(Terrain(0, 0, 1, 1), [], Ball((.5, .5)))

    def __init__(self, terrain: Terrain, robots: List[Robot], ball: Ball):
        self.__terrain = terrain


