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

    def update(self, robot: Robot, ctx: GameContext, controller: RobotController) -> None:
        pass

    def activate_on(self, ctx: GameContext) -> List[Robot]:
        return None

    def override(self, robot: Robot, ctx: GameContext) -> List[str]:
        return []


class StrategyManager(metaclass = Singleton):
    __reg = False
    __target = 'robonaldo/strategies'
    __logger = Logger("StrategyManager", priority = LogLevel.TRACE)
    strategies = {}
    enabled = []

    def register_all(self) -> None:
        sys.path.append(self.__target)
        for file in os.listdir(self.__target):
            if '.py' in file and '.pyc' not in file and '__' not in file:
                name = file.replace('.py', '')
                __import__(name)

    def by_name(self, name: str) -> RobotStrategy:
        return self.strategies.get(name)

    def is_enabled(self, strategy: RobotStrategy) -> bool:
        return strategy in self.enabled

    def set_enabled(self, strategy: RobotStrategy, state: bool) -> None:
        if state:
            if strategy not in self.enabled:
                self.enabled.append(strategy)
            self.__logger.info("Enabled strategy \'" + strategy.id + "\'.")
        else:
            if strategy in self.enabled:
                self.enabled.remove(strategy)
            self.__logger.info("Disabled strategy \'" + strategy.id + "\'.")


    def register(self, strategy: RobotStrategy, state: bool) -> None:
        self.__logger.trace("Registering strategy \'" + strategy.id + "\'.")
        self.strategies[strategy.id] = strategy
        self.set_enabled(strategy, state)

    def register_on(self, updater: ContextUpdater) -> None:
        if self.__reg is not True:
            self.__reg = True
            updater.register(lambda ctx, dt: self.__update(ctx, dt))
        else:
            raise Exception("Tried registering StrategyManager twice.")

    def __update(self, context: GameContext, delta_time: float) -> None:
        pass
