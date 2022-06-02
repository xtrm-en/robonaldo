from ..context.entities import Robot
from .net import NetworkManager
from ..utils import Position, Vector


class RobotController:
    def __init__(self, robot: Robot):
        self.__robot = robot

    def kick(self, power: float = 1.0) -> bool:
        if power == 0:
            print("noah t'es con")
            return False
        return self.command("kick", power)

    def leds(self, r: int, g: int, b: int) -> bool:
        return self.command("leds", r, g, b)

    def control(self, dx: float, dy: float, dt: float) -> bool:
        return self.command("control", dx, dy, dt)

    def control_vec(self, vector: Vector, dt: float) -> bool:
        return self.control(vector.x, vector.y, dt)

    def goto_compute_order(self, x: float, y: float, orientation: float = 0, skip_old=True):
        if not self.__robot.age() < 1:
            return False, (0.0, 0.0, 0.0)

        x = min(self.x_max, max(self.x_min, x))
        y = min(self.y_max, max(self.y_min, y))
        Ti = utils.frame_inv(utils.robot_frame(self))
        target_in_robot = Ti @ np.array([x, y, 1])

        error_x = target_in_robot[0]
        error_y = target_in_robot[1]
        error_orientation = utils.angle_wrap(orientation - self.orientation)

        arrived = np.linalg.norm([error_x, error_y, error_orientation]) < 0.05
        order = 1.5 * error_x, 1.5 * error_y, 1.5 * error_orientation

        return arrived, order

    def goto(self, target, wait=True, skip_old=True):
        if wait:
            while not self.goto(target, wait=False):
                time.sleep(0.05)
            self.control(0, 0, 0)
            return True

        arrived, order = self.goto_compute_order(target, skip_old)
        self.control(*order)

        return arrived


    def stop(self) -> bool:
        return self.control(0, 0, 0)

    def command(self, command: str, *parameters) -> str:
        color = self.__robot.color.name.lower()
        index = self.__robot.index
        return NetworkManager.INSTANCE.send(color, index, command, *parameters)
