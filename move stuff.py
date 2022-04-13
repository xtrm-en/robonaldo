import rsk
from math import*
import time
from tire_pos import Tir_pos


class Moving:

    def __init__(self, robot: str, n: int):
        self.ball = client.ball
        self.team = robot
        self.nbr = n
        self.robot_pos = client.robots[self.team][self.nbr].pose
        self.robot = client.robots[self.team][self.nbr]
         
    def vecteur(self):
        vect =  (self.robot_pos[0] - self.ball[0], self.robot_pos[1] - self.ball[1])
        return vect
    
    def teta(self):
        return atan2(self.vecteur()[1], self.vecteur()[0])
    

    def go_ball(self):
        ori = self.teta()
        client.robots[self.team][self.nbr].goto((self.ball[0]*0.8, self.ball[1]*0.8, ori-pi))
        time.sleep(0.5)
        client.robots[self.team][self.nbr].goto((self.ball[0]*0.95, self.ball[1]*0.95, ori-pi))
        print(5)
        return 5




with rsk.Client(host='172.19.39.223', key='') as client:
    robot_move = Moving("blue", 2)
    robot_shoot = Tir_pos("blue", 2)
    robot_move.go_ball()
    while True:
        if robot_move.go_ball() == 6:
            robot_shoot.tirer_pos(-0.8, 0)
