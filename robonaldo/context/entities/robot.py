from attrs import define
from enum import Enum
from robonaldo import config
import rsk
from rsk import utils, constants
import time
from typing import List
from ...wrapper import EntityRotatable
from ...utils import Position, Vector


class TeamColor(Enum):
    GREEN = "GREEN"
    BLUE = "BLUE"

    @property
    def opposite(self) -> "TeamColor":
        return self.BLUE if self == self.GREEN else self.GREEN


GHOST_TIMEOUT = 20  # [s]


class Robot(EntityRotatable):
    def __init__(self, index: int, color: TeamColor):
        EntityRotatable.__init__(self)

        self.__index: int = index
        self.__color: TeamColor = color
        self.__controller = None

        self.x_max = constants.field_length / 2 + constants.border_size / 2.0
        self.x_min = -self.x_max
        self.y_max = constants.field_width / 2 + constants.border_size / 2.0
        self.y_min = -self.y_max

    def update(self, client: rsk.Client, delta: float, controller=None) -> bool:
        self.__controller = controller if controller is not None else self.__controller

        c_robot = client.robots[self.__color.name.lower()][self.__index]

        if self.is_ghost:
            spent = time.time() - self.last_updated
            if spent > GHOST_TIMEOUT:
                return False

        if (
            type(c_robot) == type(None)
            or type(c_robot.position) == type(None)
            or type(c_robot.orientation) == type(None)
        ):
            self.is_ghost = True
            return True

        if self.is_ghost:
            spent = time.time() - self.last_updated
            print("Spent %f in ghost." % spent)

        self.is_ghost = False
        self.position = Position.at_tuple(c_robot.position)
        self.orientation = c_robot.orientation

        super().update_age()

        return True

    @property
    def index(self) -> int:
        return self.__index

    @property
    def color(self) -> TeamColor:
        return self.__color

    @property
    def identifier(self) -> str:
        return self.__color.name.lower() + str(self.__index)

    @property
    def controller(self) -> "RobotController":
        return self.__controller

    def goto(self, position: Position, orientation: float = None, wait: bool = True) -> bool:
        return self.__controller.goto(position, orientation=orientation, wait=wait)

    def goto(self, x: float, y: float, orientation: float = None, wait: bool = True) -> bool:
        return self.__controller.goto(x, y, orientation=orientation, wait=wait)


class RobotContainer:
    def __init__(self):
        self.__robots = []
        self.__ally_robots = []
        self.__controllers = []
        self.__enemy_robots = []

    def update(self, client: rsk.Client, delta: float):
        if client == None:
            self.__robot = []
            self.__ally_robots = []
            self.__controllers = []
            self.__enemy_robots = []
            return

        ally_color = config.cfg["rsk.client.color"]

        remove = []
        for robot in self.__robots:
            if not robot.update(client, delta):
                remove.append(robot)
        for r in remove:
            self.__robots.remove(r)
            self.__controllers.remove(r.controller)

        for color, number in utils.all_robots():
            robot_id = utils.robot_list2str(color, number)
            already = False
            for rob in self.__robots:
                if rob.identifier == robot_id:
                    already = True

            if already:
                continue

            robot = client.robots[color][number]

            upd = robot.last_update
            if upd is None:
                continue

            diff = time.time() - upd
            if diff < 10:
                from ...core import RobotController

                r = Robot(number, TeamColor[color.upper()])
                controller = RobotController(r)
                r.update(client, delta, controller)

                self.__robots.append(r)
                self.__controllers.append(controller)

        self.__ally_robots = []
        self.__enemy_robots = []

        for robot in self.__robots:
            if robot.color == ally_color:
                self.__ally_robots.append(robot)
            else:
                self.__enemy_robots.append(robot)

    @property
    def ally(self) -> List[Robot]:
        return self.__ally_robots

    @property
    def enemies(self) -> List[Robot]:
        return self.__enemy_robots

    @property
    def all(self) -> List[Robot]:
        return self.__robots

    @property
    def controllers(self) -> List["RobotController"]:
        return self.__controllers

    def for_team(self, color: TeamColor) -> List[Robot]:
        return (
            self.__ally_robots
            if color == config.cfg["rsk.client.color"]
            else self.__enemy_robots
        )

    def __repr__(self) -> str:
        return str(self.__robots)

    def __str__(self) -> str:
        return self.__repr__()
