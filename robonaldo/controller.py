import numpy as np
import random
from robonaldo.context.robot import Robot, RobotColor, RobotOwnership
from robonaldo.network import NetworkHandler
from robonaldo.utils import Singleton
from rsk import field_dimensions, utils
import time
from typing import List

class RobotController: ...


class GameController(metaclass=Singleton):
    __controllers = []
    __owned_controllers = []

    def construct(self) -> None:
        self.team_color = None
        for color in RobotColor:
            for i in range(2):
                self.__controllers.append(RobotController(self, color, i))

    def set_network(self, network_handler: NetworkHandler) -> None:
        self.network_handler = network_handler

    def set_color(self, color: RobotColor) -> None:
        self.team_color = color
        self.__owned_controllers = []
        for ctrl in self.__controllers:
            if ctrl.robot_color == color:
                self.__owned_controllers.append(ctrl)

    def command(self, color: RobotColor, robot_index, command, *parameters) -> str:
        return self.network_handler.send(color, robot_index, command, *parameters)

    @property
    def controllers(self) -> List[RobotController]:
        return self.__controllers

    @property
    def owned_controllers(self) -> List[RobotController]:
        return self.__owned_controllers

    def random(self, owned: bool = False) -> RobotController:
        if owned:
            if self.team_color is None:
                raise Exception("Undefined team for now.")
            
            return random.choice(self.__owned_controllers)
        return random.choice(self.__controllers)


class RobotController: # pylint: disable=function-redefined
    def __init__(self, controller: GameController, robot_color: RobotColor, index: int):
        self.__controller = controller
        self.__robot_color = robot_color
        self.__index = index

        self.__x_max = field_dimensions.length / 2 + field_dimensions.border_size / 2
        self.__x_min = -self.__x_max
        self.__y_max = field_dimensions.width / 2 + field_dimensions.border_size / 2
        self.__y_min = -self.__y_max

    @property
    def robot_color(self) -> RobotColor:
        return self.__robot_color

    def goto(self, x: float, y: float, orientation: float, wait=True, wait_delay: float = 0.05) -> bool:
        if wait:
            while not self.goto(x, y, orientation, wait=False):
                time.sleep(wait_delay)
            self.control(0, 0, 0)
            return True

        x = min(self.__x_max, max(self.__x_min, x))
        y = min(self.__y_max, max(self.__y_min, y))

        rx, ry = self.__controller.network_handler.__robot.position[0], self.__robot.position[1]

        Ti = utils.frame_inv(utils.frame(rx, ry, self.__robot.rotation))
        target_in_robot = Ti @ np.array([x, y, 1])

        error_x = target_in_robot[0]
        error_y = target_in_robot[1]
        error_orientation = utils.angle_wrap(
            orientation - self.__robot.rotation)

        self.control(1.5*error_x, 1.5*error_y, 1.5*error_orientation)

        return np.linalg.norm([error_x, error_y, error_orientation]) < 0.05

    def control(self, dx: float, dy: float, dt: float) -> bool:
        return self.command('control', dx, dy, dt)

    def command(self, command, *parameters) -> str:
        return self.__controller.command(self.__robot_color, self.__index, command, *parameters)


GameController().construct()