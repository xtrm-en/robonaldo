import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from robonaldo.controller import GameController
from robonaldo.context.wrap.game import GameContext
from robonaldo.context.updater import ContextUpdater


def dispatch_updates(controller: GameController, ctx: GameContext):
    pass


if __name__ == "__main__":
    print("Loading updater")
    updater = ContextUpdater(host="172.19.39.223")
    updater.target(lambda ctrl, ctx: dispatch_updates(ctrl, ctx))
