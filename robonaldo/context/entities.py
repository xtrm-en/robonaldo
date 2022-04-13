import time


class Updatable:
    def __init__(self, last_update: int = -1):
        self.last_update = last_update

    def update(self) -> None:
        self.last_update = int(time.time() * 1000)

    def get_delta(self) -> int:
        return time.time() * 1000 - self.last_update


class Positionable(Updatable):
    def __init__(self, position: (float, float) = (0, 0), last_update: int = -1):
        super().__init__(last_update)
        self.position = position

    def update(self, position: (float, float)) -> None:
        super().update()
        self.position = position


class Rotatable(Positionable):
    def __init__(self, position: (float, float), rotation: float):
        super().__init__(position)
        self.rotation = rotation
    
    def update(self, position: (float, float), rotation: float) -> None:
        super().update(position)
        self.rotation = rotation
