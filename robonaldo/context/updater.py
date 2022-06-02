import logging
import rsk
from .context import GameContext, set_ctx, ctx_lock


class ContextUpdater:
    def __init__(self):
        self.__log = logging.getLogger("robonaldo-updater")
        self.__context = GameContext()

    def handle_update(self, client: rsk.Client, delta: float) -> None:
        self.__context.update(client, delta)
        set_ctx(self.__context)
