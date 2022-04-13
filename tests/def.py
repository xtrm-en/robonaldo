try:
    import rsk2 as rsk
except Exception as e:
    import rsk

import numpy as np
import zmq
import threading
import time
from rsk import field_dimensions, utils

import math

key = ''
target = ("blue", 1)


def update(client: rsk.Client, deltaTime: float):
    ball_pos = client.ball
    if str(ball_pos) == "None":
        return

    ball_y: float = ball_pos[1]

    robot: rsk.client.ClientRobot = client.robots[target[0]][target[1]]
    robot_pos = robot.position

    x_diff = 0 # ball_x - robot_pos[0]

    y_diff = ball_y - robot_pos[1]

    target_rot = math.pi

    fact = 1.5
    if abs(y_diff) > 0.1:
        print("SPEEDEDD")
        fact = 1.5
    #print(y_diff)

    # if y_diff < 0.1 and x_diff < 0.2:
    #     print("attck")
    # else:
    goto(robot, (robot_pos[0] + x_diff, robot_pos[1] + y_diff, target_rot), factor=fact)


def goto(robot, target, factor: float = 10):
    if robot.has_position():
        if callable(target):
            target = target()

        x, y, orientation = target
        x = min(robot.x_max, max(robot.x_min, x))
        y = min(robot.y_max, max(robot.y_min, y))
        Ti = utils.frame_inv(utils.robot_frame(robot))
        target_in_robot = Ti @ np.array([x, y, 1])

        error_x = target_in_robot[0]
        error_y = target_in_robot[1]
        error_orientation = utils.angle_wrap(
            orientation - robot.orientation)

        control(robot, factor*error_x, factor*error_y, float(int(factor // 2)*error_orientation))

        return np.linalg.norm([error_x, error_y, error_orientation]) < 0.05
    else:
        control(robot, 0, 0, 0)
        return False


def control(robot, dx, dy, do):
    params = [dx, dy, do]

    client.req.send_json([key, target[0], target[1], ['control', *params]])
    success, message = client.req.recv_json()
    if not success:
        print("why?????", message)

with rsk.Client(host='172.19.39.223') as client:
    client.on_update = update
    # robot = client.robots[target[0]][target[1]]
    # robot.control(0,0,0)
    # i = 0
    while True:
        pass
    #     time.sleep(0.1)
    #     i += 0.1
    #     robot = client.robots[target[0]][target[1]]

    #     print(i)
    #     control(robot, i, 0, i)
