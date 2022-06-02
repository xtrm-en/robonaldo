import copy
import logging
import rsk
from threading import Lock
from .entities import Ball, Robot, RobotContainer


class GameContext:
    def __init__(self):
        self.__ball: Ball = Ball()
        self.__robots: RobotContainer = RobotContainer()

    def update(self, client: rsk.Client, delta: float) -> None:
        if self.__ball is not None:
            ghost_ball = not self.__ball.update(client, delta)
            if ghost_ball:
                # TODO: stop all robots
                raise Exception("Ball went out for like 10s bro wtf is this")

        if self.__robots is not None:
            self.__robots.update(client, delta)

    @property
    def ball(self) -> Ball:
        return self.__ball

    @property
    def robots(self) -> RobotContainer:
        return self.__robots

    def __repr__(self) -> str:
        return "GameContext(ball=%s,robots=%s)" % (str(self.__ball), str(self.__robots))

    def __str__(self) -> str:
        return self.__repr__()


ctx_lock = Lock()
ctx_obj: GameContext = None


def set_ctx(ctx: GameContext):
    global ctx_obj, ctx_lock

    ctx_lock.acquire()
    ctx_obj = ctx
    ctx_lock.release()


def get_context() -> GameContext:
    global ctx_obj, ctx_lock

    ctx_lock.acquire()
    ctx = copy.deepcopy(ctx_obj)
    ctx_lock.release()
    return ctx


def test():
    print("why")
    context = GameContext()
    print("gogogogogogo", context)
    copied = copy.deepcopy(context)
    print("Yaya", copied)
