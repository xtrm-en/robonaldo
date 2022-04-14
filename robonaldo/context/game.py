from typing import List, Dict
from .entities import Positionable, Updatable
from math import pi
from .robot import Robot, RobotColor, RobotOwnership
from rsk import Client, field_dimensions
import time

class Terrain(Positionable):
    def __init__(self, x, y, width, height, side_multiplier: int = 1):
        super().__init__((x, y))
        self.width = width
        self.height = height
        self.side_multiplier = side_multiplier

    def rel_x(value: float) -> float:
        return value * self.width * self.side_multiplier

    def rel_y(value: float) -> float:
        return value * self.height

    def rel_rot(value: float) -> float:
        return value * (1 if self.side_multiplier == 1 else pi)


class Ball(Positionable):
    def __init__(self, position: (float, float)):
        super().__init__(position)


ROBOT_REMOVE_TIMEOUT = 5 * 1000


class GameContext(Updatable):
    @staticmethod
    def empty(ally_map: Dict[RobotColor, RobotOwnership]) -> 'GameContext':
        return GameContext(Terrain(0, 0, field_dimensions.length, field_dimensions.width, 1), [], Ball((.5, .5)), ally_map)

    def __init__(self, terrain: Terrain, robots: List[Robot], ball: Ball, ally_map: Dict[RobotColor, RobotOwnership]):
        self.__terrain = terrain
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

    def update(self, client: Client) -> None:
        super().update()
        self.terrain.update((0, 0))
        self.ball.update(client.ball)
        
        for rsk_color, dct in client.robots.items():
            for rsk_index in dct.keys():
                found = False
                for robot in self.__robots:
                    if robot.color.name.lower() == rsk_color and robot.index == rsk_index:
                        found = True
                if not found:
                    rsk_robot = client.robots[rsk_color][rsk_index]
                    bot = Robot((0, 0), 0, RobotColor[rsk_color.upper()], rsk_index)
                    bot.update(client)
                    self.__robots.append(bot)
        
        for robot in self.__robots:
            if int(time.time() * 1000) - robot.last_update > ROBOT_REMOVE_TIMEOUT:
                self.__robots.remove(robot)
            robot.update(client)

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

