from typing import Tuple, List


class Position:
    def __init__(self, x: float, y: float):
        self.__x = round(x, 2)
        self.__y = round(y, 2)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    def offset(self, x: float, y: float) -> "Position":
        return Position(self.__x + x, self.__y + y)

    def offset_vec(self, vector: "Vector") -> "Position":
        return Position(self.__x + vector.x, self.__y + vector.y)

    def add(self, x: float, y: float) -> "Position":
        self.__x += x
        self.__y += y
        return self

    def add_vec(self, vector: "Vector") -> "Position":
        self.__x += vector.x
        self.__y += vector.y
        return self

    def multiply(self, x: float, y: float = None) -> "Position":
        self.__x *= x
        self.__y *= y if y is not None else x
        return self

    def multiplied(self, x: float, y: float = None) -> "Position":
        return Position(self.__x * x, self.__y * (y if y is not None else x))

    def distance_to(self, x: float, y: float) -> float:
        from .vector import Vector

        return Vector.of(self, Position.at(x, y)).norm

    def distance_to_pos(self, pos: "Position") -> float:
        from .vector import Vector

        return Vector.of(self, pos).norm

    def as_tuple(self) -> Tuple[float, float]:
        return (self.__x, self.__y)

    def as_list(self) -> List[float]:
        return [self.__x, self.__y]

    def __getitem__(self, index: int) -> float:
        assert type(index) == "int", "index type must be 'int'"

        if index < 0 or index > self.__len__():
            raise IndexError(
                "index "
                + str(index)
                + " is out of range: [0, "
                + str(self.__len__())
                + "]"
            )

        return self.__x if index == 0 else self.__y

    def __len__(self) -> int:
        return 2

    def __eq__(self, other) -> bool:
        return isinstance(other, Position) and (
            other.x == self.__x and other.y == self.__y
        )

    def __repr__(self) -> str:
        return "Position[%.2f, %.2f]" % (self.__x, self.__y)

    def __str__(self) -> str:
        return self.__repr__()

    @staticmethod
    def at(x: float, y: float) -> "Position":
        assert type(x) != "NoneType"
        assert type(y) != "NoneType"

        return Position(x, y)

    @staticmethod
    def at_tuple(position: Tuple[float, float]) -> "Position":
        x: float = position[0]
        y: float = position[1]

        return Position.at(x, y)


Position.ORIGIN: Position = Position.at(0, 0)


if __name__ == "__main__":
    first = Position.at(0, 0)
    second = Position.at(0.0, 0.0)

    assert first == second

    third = Position.at(5.1, 5.5)
