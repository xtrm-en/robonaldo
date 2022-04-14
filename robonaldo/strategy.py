from robonaldo.context.game import GameContext
from robonaldo.context.robot import Robot
from robonaldo.context.updater import ContextUpdater
from robonaldo.controller import RobotController
from robonaldo.strategies.attack import AttackStrategy
from robonaldo.strategies.defense import DefenseStrategy
from robonaldo.utils import Singleton

class RobotStrategy:
    def update(self, ctx: GameContext, robot: Robot, controller: RobotController) -> None:
        pass

class StrategyManager(metaclass = Singleton):
    __reg = False
    __robots = None
    __ctrls = None

    def construct(self) -> None:
        self.__attack = AttackStrategy()
        self.__defense = DefenseStrategy()

    def register_on(self, updater: ContextUpdater) -> None:
        if self.__reg is not True:
            self.__reg = True
            updater.register(lambda ctx, dt: self.__update(ctx, dt))
        else:
            raise Exception("Tried registering StrategyManager twice.")

    def __update(self, ctx: GameContext, delta_time: float) -> None:
        if self.__robots is None:
            rbts = ctx.robots(ownership=RobotOwnership.ALLY)
            self.__robots = [rbts[0], rbts[1]]
            self.__ctrls = [RobotController.of(rbts[0]), RobotController.of(rbts[1])]

        self.__attack.update(ctx, self.__robots[0], self.__ctrls[0])
        self.__defense.update(ctx, self.__robots[1], self.__ctrls[1])