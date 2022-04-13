from math import *
import rsk
import time
import random



class Tir_pos :

        def __init__(self, robot: str, n: int):
            self.ball = client.ball
            self.robot_x = robot
            self.n = n
            self.robot_pos = client.robots[self.robot_x][self.n].pose


        def vecteur(self, x: float, y: float):
            ball_robot = (self.robot_pos[0] - self.ball[0], self.robot_pos[1] - self.ball[1])
            pos_robot =  (self.robot_pos[0] - x, self.robot_pos[1] - y)
            ball_pos = (x - self.ball[0], y - self.ball[1])
            return [ball_robot, pos_robot, ball_pos]
        
        def vecteur2(self):
            return (self.robot_pos[0] - self.ball[0], self.robot_pos[1] - self.ball[1])
        
        def teta2(self):
            return atan2(self.vecteur2()[1], self.vecteur2()[0])
            

        def teta(self, x: float, y: float):
            teta_ball_robot = atan2(self.vecteur(x, y)[0][1],self.vecteur(x, y)[0][0])
            teta_pos_robot = atan2(self.vecteur(x, y)[1][1],self.vecteur(x, y)[1][0])
            teta_pos_ball = atan2(self.vecteur(x, y)[2][1],self.vecteur(x, y)[2][0])
            return [teta_ball_robot, teta_pos_robot, teta_pos_ball]


        def norme(self, v):
            return sqrt((v[0]**2) + (v[1]**2))


        def vitesse(self, x: float, y: float):
            v = [self.vecteur(x, y)[0][1], -self.vecteur(x, y)[0][0]]

            norm = self.norme(v)

            v = [v[0]*(0.25 / norm), v[1]*(0.25 / norm)]

            return v


        def stop(self, x: float, y: float):
            '''
            Condition d'arret pour le robot selon théta de la balle et théta du robot
            in : floats
            out : boolean
            '''
            self.update()
            #teta_robot = degrees(client.robots[self.robot_x][self.n].position[0])
            teta_robot = (client.robots[self.robot_x][self.n].pose[2]+(2*3.141)) % (2*3.141)#Modif Liam
            teta_vect = (self.teta(x, y)[2]+(2*3.141)) % (2*3.141)
            #print(teta_robot,teta_vect)
            if -0.2 < teta_robot-teta_vect < 0.2:
                print("ok")
                return True
            return False
            
        
        def update(self):
            self.robot_pos = client.robots[self.robot_x][self.n].pose
            self.ball = client.ball
            

        def tirer_pos(self, x: float, y: float):
            client.robots[self.robot_x][self.n].control(-0.15, 0, 0)
            time.sleep(0.3)
            client.robots[self.robot_x][self.n].control(0, 0,0)
            time.sleep(0.2)
            self.update()
            ball_robot = self.vecteur(x, y)[0]
            pos_robot = self.vecteur(x, y)[1]
            vitesse = self.vitesse(x, y)
            self.update()
            teta_robot = (client.robots[self.robot_x][self.n].pose[2]+(2*pi)) % (2*pi)#Modif Liam
            teta_vect = (self.teta(x, y)[2]+(2*pi)) % (2*pi)
            print(teta_robot, teta_vect)
            if 0 > teta_robot-teta_vect >= -2*pi: #teta_robot-teta_vect > pi or teta_robot-teta_vect < -pi :
                vi = -0.15
                w = (0.15 / self.norme(ball_robot))
            elif 0 < teta_robot-teta_vect < 2*pi:
                vi = 0.15
                w = -(0.15 / self.norme(ball_robot))
            
            client.robots[self.robot_x][self.n].control(0, vi, w)
            while not self.stop(x, y):
                print(teta_robot, teta_vect)
                pass
            client.robots[self.robot_x][self.n].control(0,0,0)
            client.robots[self.robot_x][self.n].control(0.5,0,0)
            time.sleep(0.7)
            client.robots[self.robot_x][self.n].kick(1)
        def go_ball(self):
            ori = self.teta2()
            client.robots[self.robot_x][self.n].goto((self.ball[0]*0.8, self.ball[1]*0.8, ori-pi))
            time.sleep(0.5)
            client.robots[self.robot_x][self.n].goto((self.ball[0]*0.95, self.ball[1]*0.95, ori-pi))
            print(5)
            return 5
            

    
with rsk.Client(host='172.19.39.223', key='') as client:
    robot = Tir_pos("blue",2)
    while True:
        if robot.go_ball() == 5:
            robot.tirer_pos(-0.8,0)
            break
    