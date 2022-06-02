from robonaldo.utils import Position
from robonaldo.wrapper import Entity
import rsk
import time


GHOST_TIMEOUT = 10  # [s]


class Ball(Entity):
    """Representation of the game Ball."""

    def update(self, client: rsk.Client, delta: float) -> bool:
        if client is None:
            self.position = Position.ORIGIN
            self.is_ghost = False
            return True

        if self.is_ghost:
            spent = time.time() - self.last_updated
            if spent > GHOST_TIMEOUT:
                return False

        if type(client.ball) == type(None):
            self.is_ghost = True
            return True

        if self.is_ghost:
            spent = time.time() - self.last_updated
            print("Spent %f in ghost." % spent)

        self.is_ghost = False
        self.position = Position.at_tuple(client.ball)

        super().update_age()

        return True
