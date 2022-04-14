from robonaldo.context.game import GameContext
from robonaldo.context.robot import Robot, RobotOwnership
from robonaldo.controller import RobotController
from robonaldo.strategy import RobotStrategy, StrategyManager
from typing import List

DEEP_THRESHOLD = -.8 / .9 # -.88888


class CloseDeep(RobotStrategy):

    def __init__(self):
        super().__init__("def_close_deep")

    def update(self, robot: Robot, ctx: GameContext, controller: RobotController) -> None:
        controller.goto(ctx.terrain.rel_x(-1), ctx.terrain.rel_y(ctx.ball.y), ctx.terrain.rot(0))

    def activate_on(self, ctx: GameContext) -> List[Robot]:
        # only activate if the ball is *deep* 
        if ctx.ball.x > DEEP_THRESHOLD:
            return []

        closest = None
        for robot in ctx.robots(side = RobotOwnership.ALLY):
            if closest is None:
                closest = robot
            else:
                if robot.x < closest.x:
                    closest = robot

        return [closest] if closest is not None else []

    def override(self, robot: Robot, ctx: GameContext) -> List[str]:
        return ['def_far_tracked']

StrategyManager().register(FarTracked(), True)