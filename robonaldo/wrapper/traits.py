from attrs import define, field
from math import cos, sin
from robonaldo.utils import Position, Vector
from time import sleep, time
from typing import Callable, List


class Positioned:
    """A position trait/interface."""

    def __init__(self):
        self.position: Position = Position.ORIGIN

    @property
    def x(self) -> float:
        return self.position.x

    @property
    def y(self) -> float:
        return self.position.y


class Rotatable:
    """A rotation trait/interface."""

    def __init__(self):
        self.rotation: float = None

    @property
    def rotation_vector(self) -> Vector:
        if self.rotation is None:
            raise Exception("Cannot get rotation vector as the rotation is null.")

        x = cos(self.rotation)
        y = sin(self.rotation)

        origin = Position.ORIGIN

        return Vector.of(origin, Position.at(x, y))


class Updatable:
    """An updatable trait/interface."""

    def __init__(self):
        self.last_updated: float = None
        self.__update_hooks: List[Callable[["Updatable", float], None]] = []

        self.update_age()

    def update_age(self) -> None:
        delta = self.age
        self.last_updated = time()

        for hook in self.__update_hooks:
            hook(self, delta)

    @property
    def hooks(self) -> List[Callable[["Updatable", float], None]]:
        return self.__update_hooks

    @property
    def age(self) -> float:
        return time() - (self.last_updated if self.last_updated is not None else time())


if __name__ == "__main__":
    updatable = Updatable()
    print(updatable)

    sleep(0.2)

    print(updatable)
    updatable.update_age()
    print(updatable)
