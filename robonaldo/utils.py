from robonaldo.context.entities import Positionable

class Singleton(type):
    """Implementation of the singleton design pattern.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]

class Vector:
    def __init__(self, source, to):
        if isinstance(source, Positionable):
            self.__source = source.position
        else:
            self.__source = source

        if isinstance(to, Positionable):
            self.__to = to.position
        else:
            self.__to = to

        assert isinstance(self.__source, tuple) 
        assert isinstance(self.__to, tuple) 

        self.__x = self.__to[0] - self.__source[0]
        self.__y = self.__to[1] - self.__source[1]

    def __repr__(self) -> str:
        return "Vector(x=" + str(self.__x) + ", y=" + str(self.__y) + ")"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    def multiply(self, factor_x: float, factor_y: float = None) -> None:
        self.__x *= factor_x
        self.__y *= factor_x if factor_y is None else factor_y

        return self



if __name__ == "__main__":
    vec = Vector(source = (0.5, 0.5), to = (1.5, 1.5))
    print(vec)
    print(vec.multiply(2))
    print(vec.multiply(2))
    print(vec.x, vec.y)