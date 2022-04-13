from typing import List, Dict
from .entities import Positionable
from .robot import Robot, RobotColor, RobotOwnership


class Ball(Positionable):
    def __init__(self, position: (float, float)):
        super().__init__(position)


class GameContext():
    @staticmethod
    def empty() -> 'GameContext':
        return GameContext([], Ball((.5, .5)), {})

    def __init__(self, robots: List[Robot], ball: Ball, ally_map: Dict[RobotColor, RobotOwnership]):
        self.__robots = robots
        self.__ball = ball
        self.__ally_robots = []
        self.__enemy_robots = []

        self.__ally_map = ally_map

        for robot in self.__robots:
            if self.__ally_map[robot.color] == RobotOwnership.ALLY:
                self.__ally_robots.append(robot)
            else:
                self.__enemy_robots.append(robot)

    def robots(self, ownership: RobotOwnership = RobotOwnership.ANY) -> List[Robot]:
        if ownership == RobotOwnership.ALLY:
            return self.__ally_robots
        if ownership == RobotOwnership.ENEMY:
            return self.__enemy_robots
        return self.__robots

    @property
    def ball(self) -> Ball:
        return self.__ball

    def closest_to(entity: Positionable, ownership: RobotOwnership = RobotOwnership.ANY) -> Robot:
        closest = None
        for robot in self.robots(ownership = ownership):
            if closest is None:
                closest = robot
            else:
                if robot.distance_to(entity) < closest.distance_to(entity):
                    closest = robot
        return closest

