from robonaldo.context.game import GameContext
from robonaldo.context.robot import Robot, RobotOwnership
from robonaldo.controller import RobotController
from robonaldo.strategy import RobotStrategy, StrategyManager
from typing import List

DEFENSE_LINES = 0.2


class FarTracked(RobotStrategy):
    """Strategise UwU
    """

    def __init__(self):
        super().__init__("def_far_track")

    def update(self, ctx: GameContext, controller: RobotController) -> None:
        pass

    def activate_on(self, ctx: GameContext) -> List[Robot]:
        closest = None
        for robot in ctx.robots(side = RobotOwnership.ALLY):
            if closest is None:
                closest = robot
            else:
                if robot.get_relative_position() < closest.get_relative_position():
                    closest = robot

        return [closest] if closest is not None else []

    def should_override(self, ctx: GameContext, robot: Robot, strat_id: str) -> bool:
        '''Don't override anything as this is the least useful strategy
        '''
        return False

StrategyManager().register(FarTracked(), True)