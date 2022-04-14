
import rsk
import time
from math import sqrt, radians, pi


class Predict:
    def __init__(self, client, team):
        self.client = client
        self.team = team
        self.couleur = ['green', 'blue']
        self.numero = [1, 2]

    def delta(self):
        '''Calcule inertie de la balle'''
        if str(self.client.ball) == "None":
            return
        old = self.client.ball
        time.sleep(0.05)
        return (self.client.ball[0]-old[0], self.client.ball[1]-old[1])

    def arr(self):
        '''Je sais pas lol (sert a rien ???)'''
        i = 1
        if self.team == 'green' and self.delta()[1] < -0.05:
            while self.delta()[0]*i > -0.9 or abs(self.delta()[1]) < 0.6:
                i += 1
            return i
        if self.team == 'blue' and self.delta()[1] > 0.05:
            while self.delta()[0]*i < 0.9 or abs(self.delta()[1]) < 0.6:
                i += 1
            return i
        return 1

    def out_of_bound(self):
        '''True si balle hors terrain (pas utilisé)'''
        if client.ball[0] > 0.9 or client.ball[0] < -0.9:
            return True
        elif client.ball[1] > 0.6 or client.ball[1] < -0.6:
            return True
        else:
            return False

    def plus_proche(self):
        '''Return tuple du robot plus proche de la balle ('team',nombre)'''
        plus_proche = 100
        robot_pp = None
        client = self.client
        for i in self.couleur:
            for j in self.numero:
                if str(client.robots[i][j].position) != 'None' and str(client.ball) != 'None':
                    robot = client.robots[i][j]
                    if abs(client.ball[0]-robot.position[0])+abs(client.ball[1]-robot.position[1]) < plus_proche:
                        plus_proche = abs(
                            client.ball[0]-robot.position[0])+abs(client.ball[1]-robot.position[1])
                        robot_pp = (i, j)
        return robot_pp

    def segment(self):
        '''Vecteur robot_plus_proche->balle'''
        client = self.client
        return (client.ball[0]-client.robots[self.plus_proche()[0]][self.plus_proche()[1]].position[0], client.ball[1]-client.robots[self.plus_proche()[0]][self.plus_proche()[1]].position[1])
 
    def segment_nomee(self,couleur,numero):
        '''Vecteur robot_au_choix->balle'''
        robot = client.robots[couleur][numero]
        return (client.ball[0]-robot.position[0],client.ball[1]-robot.position[1])
 
    def prolongation_seg(self, i=1):
        '''Prolonge de vecteur robot_plus_proche->balle jusqu'à sortir du terrain, None si sort sans finir sur l'axe des goals
        Return l'axe y de la cage correspondant au cages du goal'''
        client = self.client
        while abs(self.segment()[0]*i) < 0.9 and abs(self.segment()[1]) < 0.7:
            i += 1
            if abs(self.segment()[1]*i) > 0.7:
                return None
        if self.segment()[0]*i < 0 and self.team == 'green': return client.ball[1] + self.segment()[1]*i
        if self.segment()[0]*i > 0 and self.team == 'blue': return client.ball[1] + self.segment()[1]*i
        
    def print_info(self):
        '''ça print beaucoup d'info pour faire stylé'''
        if str(client.ball) == "None":
            return
        print("DELTA :", self.delta())
        print("PREDICT :", self.prolongation_seg())
        print('POS :', defe.defenseur.position[1])

        print('PLUS PROCHE :', self.plus_proche())
        print('BALLE :', client.ball[0], client.ball[1])
        print('PROCHE,FACE A :', defe.proche_de(), defe.face_a())
        print('---------------------------------')
        
    def seg_in_way(self,couleur,numero):
        '''PAS FINI /!\, censé return une liste de coordonnées du vecteur robot->balle'''
        i = 1
        liste = []

        client = self.client
        segment = self.segment_nomee(couleur,numero)
        if abs(segment[0]) != 0:
            while abs(self.segment()[0]*i) < 0.9 and abs(self.segment()[1]*i) > 0.7:
                i += 1
                liste.append(client.ball[0] + self.segment()[0]*i, client.ball[1] + self.segment()[1]*i)
            return liste
        return []

    def robot_in_way(self,couleur,numero):
        '''Prend la liste faite précedement et regarde si un robot est dessus (Tolérance 0.05)'''
        liste = self.seg_in_way(couleur,numero)
        for i in self.couleur:
            for j in self.numero:
                if str(client.robots[i][j].position) != 'None' and str(client.ball) != 'None':
                    robot = client.robots[i][j]
                    for k in range(len(liste)):
                        if abs(abs(int(robot.position[0]))-abs(int(liste[k]))) < 0.05 and abs(abs(int(robot.position[1]))-abs(int(liste[k]))) < 0.05:
                            return True
'''----------------------------------------CHANGEMENT DE CLASSE WOUHOU--------------------------------------------------------'''
class Defense:
    def __init__(self, predict: Predict, ctx: GameContext, robot: Robot, controller: RobotController):
        self.predict = predict
        self.ctx = ctx
        self.robot = robot
        self.controller = controller

    def reset_placement(self):
        '''Replace le goal à sa place de défaut'''
        if self.team == 'green':
            self.controller.goto(-0.9, 0, 0)
        else:
            self.controller.goto(0.9, 0, pi)

    def in_zone(self):
        if self.team == 'blue':
            return self.ctx.ball.x > 0 and self.ctx.ball.y > -0.6 and self.ctx.ball.y < 0.6
        else:
            return self.ctx.ball.x < -0 and self.ctx.ball.y > -0.6 and self.ctx.ball.y < 0.6

    def next_to_goal(self):
        return abs(self.ctx.ball.x) > 0.75 and abs(self.ctx.ball.y) < 0.6

    def proche_de(self):
        return abs(self.ctx.ball.x - self.robot.x) < 0.4

    def face_a(self):
        return abs(abs(self.ctx.ball.y) - abs(self.robot.y)) < 0.05

    def degagement(self):
        self.reset_angle()

        time.sleep(0.2)

        if self.team == 'green':
            self.controller.goto(self.ctx.ball.x - 0.10, self.ctx.ball.y, 0, True)
        else:
            self.controller.goto(self.ctx.ball.x + 0.10, self.ctx.ball.y, 0, True)

        self.controller.control(0.25, 0, 0)
        time.sleep(0.5)
        self.controller.kick()

    def reset_angle(self):
        if self.team == 'green':
            self.controller.goto(self.robot.x, self.robot.y, 0, False)
        else:
            self.controller.goto(self.robot.x, self.robot.y, pi, False)

    def deplace_cage(self):
        if self.team == 'green':
            while self.ctx.ball.y - self.robot.y > 0.05 and abs(self.ctx.ball.y) > 0.4:
                self.controller.control(0, 0.4, 0)
            while self.ctx.ball.y - self.robot.y < -0.05 and abs(self.ctx.ball.y) > 0.4:
                self.controller.control(0, -0.4, 0)
            if abs(self.ctx.ball.y) > 0.4:
                self.controller.control(0, 0, 0)
        else:
            while self.ctx.ball.y - self.robot.y > 0.05:
                self.controller.control(0, -0.4, 0)
            while self.ctx.ball.y - self.robot.y < -0.05:
                self.controller.control(0, 0.4, 0)

    def avance(self):
        self.controller.control(0.4, 0, 0)

    def deplace_cage_avance(self):
        self.reset_angle()

        prolongation = self.predict.prolongation_seg()
        if prolongation == None:    
            return

        # STOPPED HERE

        if self.team == 'green':
            while True:
                prolongation = predict.prolongation_seg()

                if prolongation is None:
                    self.defenseur.control(0, 0, 0)
                    break

                if prolongation-self.defenseur.position[1] > 0.05 and abs(prolongation) < 0.4:
                    self.defenseur.control(0, 0.40, 0)
                else:
                    break
            while True:
                prolongation = predict.prolongation_seg()

                if prolongation is None:
                    self.defenseur.control(0, 0, 0)
                    break

                if prolongation-self.defenseur.position[1] < -0.05 and abs(prolongation) < 0.4:
                    self.defenseur.control(0, -0.40, 0)
                else:
                    break
        else:
            while True:
                prolongation = predict.prolongation_seg()

                if prolongation is None:
                    self.defenseur.control(0, 0, 0)
                    break

                if prolongation-self.defenseur.position[1] > 0.05 and abs(prolongation) < 0.4:
                    self.defenseur.control(0, -0.40, 0)
                else:
                    break
            while True:
                prolongation = predict.prolongation_seg()

                if prolongation is None:
                    self.defenseur.control(0, 0, 0)
                    break

                if prolongation-self.defenseur.position[1] < -0.05 and abs(prolongation) < 0.5:
                    self.defenseur.control(0, 0.40, 0)
                else:
                    break

    def reset_axe_avance(self):
        if self.team == 'green':
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
        if self.team == 'green':
            self.defenseur.goto((-0.9, self.defenseur.position[1], 0), True)
        if self.team == 'blue':
            self.defenseur.goto((0.9, self.defenseur.position[1], pi), True)

    def threshold_cage(self):
        if self.team=='green':
            return self.client.ball[0] < -0.8
        else:
            return self.client.ball[0] > 0.8

    def retreat(self):
        if self.team == 'green':
            self.defenseur.goto((-1.075, self.defenseur.position[1], 0), True)
        else:
            self.defenseur.goto((1.075, self.defenseur.position[1], pi), True)

    def rotete(self, team, nbr):
        client = self.client
        client.robots[team][nbr].control(0, 0, radians(10))

from robonaldo.strategy import RobotStrategy

GOAL_THRESHOLD = -.8 / .9
BACK_POS = -1.195


class DefenseStrategy(RobotStrategy):
    # def update(self, ctx: GameContext, robot: Robot, controller: RobotController) -> None:
    #     if ctx.ball.x < GOAL_THRESHOLD:
    #         contoller.goto_rel(BACK_POS, robot.y, 0)
    def __init__(self):
        self.defe = Defense(robot)
        self.predict = Predict(robot)

    def update(self, ctx: GameContext, robot: Robot, ctrl: RobotController):
        defe.reset_angle()
        defe.reset_placement()
        while True:
            try:
                if display:
                    predict.print_info()

                if defe.threshold_cage():

                    defe.retreat()
                    defe.deplace_cage()

                    while defe.face_a():
                        defe.deplace_cage()
                        defe.reset_axe_avance()
                        time.sleep(0.7)
                        defe.degagement()

                if predict.prolongation_seg() == None or abs(predict.prolongation_seg()) > 0.4 or defe.next_to_goal() or venere:
                    defe.reset_axe_avance()
                    defe.deplace_cage()
                    defe.reset_angle()

                    if defe.proche_de() and defe.face_a() or predict.plus_proche() == (defe.team,defe.nbr) and defe.face_a() or venere:
                        defe.deplace_cage()
                        defe.reset_angle()
                        time.sleep(0.2)
                        defe.degagement()
                        defe.reset_placement()
                else:
                    defe.deplace_cage_avance()
                    defe.reset_axe_avance()
                    defe.reset_angle()
            except:
                defe.control(0,0,0)

StrategyManager().defense = DefenseStrategy()

# with rsk.Client(host='172.19.39.223', key='') as client:
    # defe = Defense(client, team, nbr)
    # predict = Predict(client, team)
    # defe.reset_angle()
    # defe.reset_placement()
    # while True:
    #     try:
    #         if str(client.ball) == "None":
    #             continue
    #         if display:
    #             predict.print_info()

    #         if defe.threshold_cage():

    #             defe.retreat()
    #             defe.deplace_cage()

    #             while defe.face_a():
    #                 defe.deplace_cage()
    #                 defe.reset_axe_avance()
    #                 time.sleep(0.7)
    #                 defe.degagement()

    #         if predict.prolongation_seg() == None or abs(predict.prolongation_seg()) > 0.4 or defe.next_to_goal() or venere:
    #             defe.reset_axe_avance()
    #             defe.deplace_cage()
    #             defe.reset_angle()

    #             if defe.proche_de() and defe.face_a() or predict.plus_proche() == (defe.team,defe.nbr) and defe.face_a() or venere:
    #                 defe.deplace_cage()
    #                 defe.reset_angle()
    #                 time.sleep(0.2)
    #                 defe.degagement()
    #                 defe.reset_placement()
    #         else:
    #             defe.deplace_cage_avance()
    #             defe.reset_axe_avance()
    #             defe.reset_angle()
    #     except:
    #         defe.control(0,0,0)