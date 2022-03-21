import rsk
import time
from math import sqrt


class Predict:
    def __init__(self, team):
        self.team = team

    def delta(self):
        old = rsk.ball()
        time.sleep(0.10)
        return (old[0]-rsk.ball[0], old[1]-rsk.ball[1])

    def distance(self, team):
        return (sqrt((rsk.robots[team][0]-rsk.ball[0])**2+(rsk.robots[team][1]-rsk.ball[1])**2), team)

    def plus_proche(self):
        if self.distance(self.team)[0] > self.distance(self.team)[1]:
            return 1
        else:
            return 0

    def next_pos(self, i):
        tolerance = i
        return (self.delta()[0]*tolerance, self.delta[1]*tolerance)

    def out_of_bound(self):
        if rsk.ball()[0] > 1.83 or rsk.ball()[0] < -1.83:
            if rsk.ball()[1] > 1.22 or rsk.ball()[1] < -1.22:
                return True
        else:
            return False

    def out_of_bound_value(x, y):
        if x > 1.83 or x < -1.83:
            if y > 1.22 or y < -1.22:
                return True
        else:
            return False

    def predict_in_goal(self):
        if self.team == 'green':
            if self.next_pos[0] > 1.82 and self.next_pos[1] > 1.22:
                return True
            else:
                return False
        else:
            if self.next_pos[0] < -1.82 and self.next_pos[1] < -1.22:
                return True
            else:
                return False


Predict = Predict()


class Defense:
    def __init__(self, team, nbr: int):
        self.defenseur = rsk.robots[team][nbr]
        self.team = team

    def reset_placement(self):
        if self.team == 'green':
            self.defenseur.goto(-1.70, 0, 0)
        else:
            self.defenseur.goto(1.70, 0, 0)

    def intercept(self, Predict):
        if Predict.predict_in_goal() == True:
            delta_list = []
            for i in range(1, 10):
                delta_list.append(Predict.next_pos(i)[
                                  0]-self.defenseur.position[0], Predict.next_pos(i)[1]-self.defenseur.position[1])
            return self.defenseur.goto(min(delta_list), 0)
        else:
            return False

    def can_kick(self):
        pass
