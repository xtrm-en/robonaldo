from entities import Positionable, Robot

class Terrain(Positionable):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, 0)
        self.__width = width
        self.__height = height


class Ball(Positionable):
    def __init__(self, position: (int, int)):
        super().__init__(position)


class GameContext():
    def __init__(self, terrain: Terrain, robots: List[Robot], ball: Positionable):
        pass

