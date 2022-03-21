import time


class Updatable:
    def __init__(self, last_update: int = -1):
        self.last_update = last_update

    def update(self) -> None:
        self.last_update = int(time.time() * 1000)


class Positionable(Updatable):
    def __init__(self, position: (int, int) = (0, 0), last_update: int = -1):
        super().__init__(last_update)
        self.position = position


class Rotatable(Positionable):
    def __init__(self, position: (int, int), rotation: float):
        super().__init__(position)
        self.rotation = rotation
