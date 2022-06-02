import rsk
import time
from robonaldo import config
from robonaldo.context.entities import Robot
from robonaldo.context import ball, robots
from robonaldo.core.net import NetworkManager
from math import pi


"""----------------------------------------CHANGEMENT DE CLASSE WOUHOU--------------------------------------------------------"""


class Defense:
    def __init__(self, robot: Robot):
        self.__robot = robot
        self.coords = {}

        team = config.cfg["rsk.client.color"].name.lower()
        x_positive = NetworkManager.INSTANCE.client.referee["teams"][team]["x_positive"]

        self.__side_multiplier = 1 if x_positive else -1
        self.__init(x_positive)

    def __init(self, x_positive: bool):
        if x_positive:
            self.coords["cage"] = 0.9
            self.coords["retreat_cage"] = 1.075
            self.coords["angle"] = pi
            self.coords["threshold_cage"] = 0.8
            self.coords["degagement"] = -0.1
            self.coords["deplace_cage"] = 0.3
            self.coords["deplace_cage2"] = -0.3
        else:
            self.coords["cage"] = -0.9
            self.coords["retreat_cage"] = -1.075
            self.coords["angle"] = 0
            self.coords["threshold_cage"] = -0.8
            self.coords["degagement"] = 0.1
            self.coords["deplace_cage"] = -0.3
            self.coords["deplace_cage2"] = 0.3

    def reset_placement(self):
        """Replace le goal à sa place de défaut"""
        self.__robot.goto(
            (
                self.__robot.position,
                pi - self.coords["angle"],
            ),
            True,
        )
        self.__robot.goto(
            (self.coords["cage"], 0, pi - self.coords["angle"]), True
        )
        self.__robot.goto(
            (
                self.__robot.position,
                self.coords["angle"],
            ),
            True,
        )

    def kick(self):
        self.__robot.kick(1)

    def next_to_goal(self):
        if abs(client.ball[0]) > 0.75 and abs(client.ball[1]) < 0.6:
            return True

    def proche_de(self):
        return abs(ball.x - self.__robot.x) < 0.4

    def face_a(self):
        return abs(ball.y - self.__robot.y) < 0.05

    def control(self, x, y, z):
        self.__robot.controller.control(x, y, z)

    def degagement(self):
        defe.reset_angle()
        self.defenseur.goto(
            (
                client.ball[0] - self.coords["degagement"],
                client.ball[1],
                self.coords["angle"],
            ),
            True,
        )
        time.sleep(0.5)
        self.defenseur.goto(
            (
                client.ball[0] - self.coords["degagement"],
                client.ball[1],
                self.coords["angle"],
            ),
            True,
        )
        self.defenseur.control(0.25, 0, 0)
        time.sleep(0.25)
        self.defenseur.kick()
        time.sleep(0.5)

    def reset_angle(self):
        self.defenseur.goto(
            (
                self.defenseur.position[0],
                self.defenseur.position[1],
                self.coords["angle"],
            ),
            False,
        )

    def deplace_cage(self):
        client = self.client
        while (
            client.ball[1] - self.defenseur.position[1] > 0.05
            and abs(client.ball[1]) < 0.6
        ):
            self.defenseur.control(0, self.coords["deplace_cage2"], 0)
        while (
            client.ball[1] - self.defenseur.position[1] < -0.05
            and abs(client.ball[1]) < 0.6
        ):
            self.defenseur.control(0, self.coords["deplace_cage"], 0)
        if abs(client.ball[1]) > 0.6:
            self.defenseur.control(0, 0, 0)

    def deplace_cage_avance(self):
        self.reset_angle()

        prolongation = predict.prolongation_seg()
        if prolongation == None:
            return

        while True:
            prolongation = predict.prolongation_seg()

            if prolongation is None or abs(prolongation) > 0.4:
                self.defenseur.control(0, 0, 0)
                break

            if (
                prolongation - self.defenseur.position[1] > 0.05
                and abs(prolongation) < 0.4
            ):
                self.defenseur.control(0, self.coords["deplace_cage2"], 0)
            else:
                break
        while True:
            prolongation = predict.prolongation_seg()

            if prolongation is None or abs(prolongation) > 0.4:
                self.defenseur.control(0, 0, 0)
                break

            if (
                prolongation - self.defenseur.position[1] < -0.05
                and abs(prolongation) < 0.4
            ):
                self.defenseur.control(0, self.coords["deplace_cage"], 0)
            else:
                break

    def reset_axe_avance(self):
        if self.side == "left":
            while self.defenseur.position[0] > -0.85:
                self.defenseur.control(-0.15, 0, 0)
            while self.defenseur.position[0] < -0.95:
                self.defenseur.control(0.15, 0, 0)
        else:
            while self.defenseur.position[0] < 0.85:
                self.defenseur.control(-0.15, 0, 0)
            while self.defenseur.position[0] > 0.95:
                self.defenseur.control(0.15, 0, 0)

    def reset_axe(self):
        self.defenseur.goto(
            (self.coords["cage"], self.defenseur.position[1], self.coords["angle"]),
            True,
        )

    def threshold_cage(self):
        if self.side == "right":
            return self.client.ball[0] > 0.8 and abs(client.ball[1]) < 0.6
        return self.client.ball[0] < -0.8 and abs(client.ball[1]) < 0.6

    def retreat(self):
        self.defenseur.goto(
            (
                self.coords["retreat_cage"],
                self.defenseur.position[1],
                self.coords["angle"],
            ),
            True,
        )


team = "green"
nbr = 1
display = True
venere = False
with rsk.Client(host="172.19.39.223", key="") as client:
    print("Attempt to connect...")
    if client.referee["teams"][team]["x_positive"]:
        side = "right"
    else:
        side = "left"
    defe = Defense(client, team, nbr, side)
    predict = Predict(client, team, side)
    defe.reset_angle()
    defe.reset_placement()
    print("Connected")
    while True:
        try:
            if str(client.ball) == "None":
                continue
            if display:
                predict.print_info()

            while defe.threshold_cage():
                print("STRAT : Threshold")
                defe.retreat()
                defe.defenseur.goto(
                    (defe.defenseur.position[0], client.ball[1], defe.coords["angle"]),
                    True,
                )
                defe.defenseur.goto(
                    (defe.defenseur.position[0], client.ball[1], defe.coords["angle"]),
                    True,
                )
                while defe.face_a():
                    defe.deplace_cage()
                    defe.reset_axe_avance()
                    time.sleep(0.7)
                    defe.degagement()
                    defe.reset_placement()

            if (
                predict.prolongation_seg() == None
                or abs(predict.prolongation_seg()) > 0.4
                or defe.next_to_goal()
                or venere
            ):
                print("STRAT : SUIVRE BALLE SIMPLE")
                defe.deplace_cage()
                defe.reset_axe_avance()
                defe.reset_angle()

                if (
                    defe.proche_de()
                    and defe.face_a()
                    or predict.plus_proche() == (defe.team, defe.nbr)
                    and defe.face_a()
                    or venere
                ):
                    print("STRAT : DEGAGEMENT")
                    defe.deplace_cage()
                    defe.reset_angle()
                    time.sleep(0.7)
                    defe.degagement()
            else:
                print("STRAT : PREDIRE BALLE")
                defe.deplace_cage_avance()
                defe.reset_axe_avance()
                defe.reset_angle()
        except Exception as e:
            print("STRAT : EXCEPTION")
            defe.control(0, 0, 0)
            defe.reset_angle()

            if "keyboard" in str(e).lower():
                break
