import time
from robonaldo.wrapper import Positioned, Rotatable, Updatable


class Entity(Positioned, Updatable):
    def __init__(self):
        Positioned.__init__(self)
        Updatable.__init__(self)
        self.is_ghost: bool = False


class EntityRotatable(Entity, Rotatable):
    def __init__(self):
        Entity.__init__(self)
        Rotatable.__init__(self)
