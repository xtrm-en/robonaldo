from enum import Enum
import os
from robonaldo.context.game import GameContext
from robonaldo.context.updater import ContextUpdater
from robonaldo.context.robot import Robot
from robonaldo.controller import RobotController
from robonaldo.log import Logger, LogLevel
from robonaldo.utils import Singleton
from typing import List
import sys


class RobotStrategy:
    """Strategise UwU
    """

    def __init__(self, id: str):
        self.__id = id

    @property
    def id(self) -> str:
        return self.__id

    def update(self, ctx: GameContext, controller: RobotController) -> None:
        pass

    def activate_on(self, ctx: GameContext) -> List[Robot]:
        return None

    def should_override(self, ctx: GameContext, robot: Robot, strat_id: str) -> bool:
        return False


class StrategyManager(metaclass = Singleton):
    __reg = False
    __target = 'robonaldo/strategies'
    __logger = Logger("StrategyManager", priority = LogLevel.TRACE)
    strategies = {}

    def register_all(self) -> None:
        sys.path.append(self.__target)
        for file in os.listdir(self.__target):
            if '.py' in file and '.pyc' not in file and '__' not in file:
                name = file.replace('.py', '')
                __import__(name)

    def register(self, strat: RobotStrategy, state: bool) -> None:
        self.__logger.trace("Registering strategy \'" + strat.id + "\'.")
        self.strategies[strat.id] = (strat, state)

    def register_on(self, updater: ContextUpdater) -> None:
        if self.__reg is not True:
            self.__reg = True
            updater.register(lambda ctx, dt: self.__update(ctx, dt))
        else:
            raise Exception("Tried registering StrategyManager twice.")

    def __update(self, context: GameContext, delta_time: float) -> None:
        pass