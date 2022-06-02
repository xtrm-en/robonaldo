from .context import GameContext, get_context
from .updater import ContextUpdater


# Python is whiney and a fucking bitch
class ContextProxy:
    def __init__(self, getter):
        self.__getter = getter

    def __getattr__(self, attr: str):
        return getattr(self.__getter(), attr, None)

    def __repr__(self) -> str:
        return self.__getter().__repr__()

    def __str__(self) -> str:
        return self.__getter().__str__()


ctx = ContextProxy(lambda: get_context())
ball = ContextProxy(lambda: ctx.ball)
robots = ContextProxy(lambda: ctx.robots)


__all__ = ["ball", "robots", "ctx", "ContextUpdater"]
