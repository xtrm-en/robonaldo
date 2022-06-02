from attrs import define
from robonaldo.utils import Position, Vector
import time
from typing import List, Tuple
from robonaldo.core.net import NetworkManager
from robonaldo import config
from robonaldo.wrapper import Entity
from robonaldo.context.entities import Robot
from robonaldo.context import ctx, ball, robots


class Predict:
    def __init__(self):
        team = config.cfg["rsk.client.color"].name.lower()
        x_positive = NetworkManager.INSTANCE.client.referee["teams"][team]["x_positive"]
        self.__side_multiplier = 1 if x_positive else -1

    def delta(self) -> Vector:
        """Calcule inertie de la balle"""
        #TODO: find a less shitty way of doing this
        try:
            old_pos = Position.at_tuple(NetworkManager.INSTANCE.client.ball)
            time.sleep(0.05)
            new_pos = Position.at_tuple(NetworkManager.INSTANCE.client.ball)
            return Vector.of(old_pos, new_pos)
        except:
            return Vector.NULL

    def plus_proche(self) -> Robot:
        """Return tuple du robot plus proche de la balle ('team',nombre)"""
        dist = 10000
        nearest = None
        ball_pos = ball.position
        for robot in robots.all:
            d = robot.position.distance_to(ball_pos)
            if d < dist:
                dist = d
                nearest = robot
        return nearest

    @property
    def segment(self):
        """Vecteur robot_plus_proche->balle"""
        nearest = self.plus_proche()
        return self.segment_nomee(nearest)

    def segment_nomee(self, robot: Robot):
        """Vecteur robot_au_choix->balle"""
        if robot is None:
            return None

        return Vector.of(robot.position, ball.position)

    def prolongation_seg(self, i=1):
        """Prolonge de vecteur robot_plus_proche->balle jusqu'à sortir du terrain, None si sort sans finir sur l'axe des goals
        Return l'axe y de la cage correspondant au cages du goal"""
        while abs(self.segment.x * i) < 0.8 and abs(self.segment.y) < 0.7:
            i += 1
            if abs(self.segment.y * i) > 0.7:
                return None

        if self.__side_multiplier * (self.segment.x * i) < 0:
            return ball.y + self.segment.y * i * 0.75

        return None

    def prolongation_seg_xy(self, i=1):
        """Prolonge de vecteur robot_plus_proche->balle jusqu'à sortir du terrain, None si sort sans finir sur l'axe des goals
        Return l'axe y de la cage correspondant au cages du goal"""

        while abs(self.segment.x * i) < 0.9 and abs(self.segment.y) < 0.7:
            i += 1

        return ball.position.offset_vec(self.segment.multiplied(i))
