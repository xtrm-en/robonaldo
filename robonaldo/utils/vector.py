from typing import Tuple
from .position import Position
from math import sqrt, atan2, pi


class Vector:
    def __init__(self, origin: Position, to: Position):
        self.__x = None
        self.__y = None

        self.__origin = origin
        self.__to = to

        self.__recalculate_offsets()

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def origin(self) -> Position:
        return self.__origin

    @property
    def to(self) -> Position:
        return self.__to

    @property
    def norm(self):
        return sqrt((self.__x**2) + (self.__y**2))

    def multiply(self, x: float, y: float = None) -> "Vector":
        self.__x *= x
        self.__y *= y if y is not None else x
        return self

    def multiplied(self, x: float, y: float = None) -> "Vector":
        return Vector(self.__x * x, self.__y * (y if y is not None else x))

    @property
    def theta(self):
        return atan2(self.__y, self.__x)

    def collides_with(self, vect: "Vecteur", margin: float = 0.5) -> bool:
        collides = -margin < self.theta - vect.theta < margin
        collides_reverse = -margin < self.theta - (vect.theta - pi) < margin

        return collides or collides_reverse

    def orthogonal_with(self, vect: "Vecteur", margin: float = 0.5) -> bool:
        return -margin < (self.__x * vect.x) - (self.__y * vect.y) < margin

    def __recalculate_offsets(self):
        self.__x = self.__to.x - self.__origin.x
        self.__y = self.__to.y - self.__origin.y

    def __repr__(self) -> str:
        return "Vector[%.2f,%.2f]" % (self.__x, self.__y)

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def of(origin: Position, to: Position) -> "Vector":
        assert type(origin) != "NoneType"
        assert type(to) != "NoneType"

        return Vector(origin, to)

    @staticmethod
    def of_tuple(origin: Tuple[float, float], to: Tuple[float, float]) -> "Vector":
        return Vector(Position.at_tuple(origin), Position.at_tuple(to))


Vector.NULL: Vector = Vector.of(Position.at(0, 0), Position.at(0, 0))


if __name__ == "__main__":
    first_pos = Position.at(5, 5)
    second_pos = Position.at(0, 0)

    vec = Vector.of(first_pos, second_pos)
    assert vec.x == -5 and vec.y == -5
