#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

## player_simul.py


from time import sleep
import threading


#                  x1     y1     x2     y2   sec
BAT_D = {   0 : (-0.45, -8.93, -4.89, -7.49, 2),    # cas 2
            1 : (-8.95, -2.35, -5.55, -6.98, 3),    # cas
            2 : (-8.70,  2.29, -8.40, -2.35, 3.5),  # cas 4
            3 : (-8.34,  3.19, -5.55,  6.97, 4.5),  # cas 1
            4 : (-0.45,  8.94, -4.87,  7.50, 5),    # cas 4
            5 : ( 0.48,  8.92,  4.83,  7.50, 5.5),
            6 : ( 8.25,  3.26,  5.63,  6.96, 1.5),
            7 : ( 8.70, -2.35,  8.40,  2.27, 1.0),  # cas 2
            8 : ( 8.32, -3.18,  5.58, -6.95, 6.5),  # cas 3
            9 : ( 4.83, -7.50,  0.44, -8.94, 7)   } # cas 3


class BatSimul:
    '''Simulation des bats level 10 de MPFF.
    Tourne à 60 Hz
    '''

    def __init__(self, sec, x1, y1, x2, y2):
        '''sec != 0'''

        # Période de mise à jour
        self.periode = 0.015

        # Raquette
        self.bat = [x1, y1]

        # déplacement par frame
        if sec != 0: bat_speed = 1 / (60 * sec)
        else: bat_speed = 1

        self.sens_x = 1
        self.sens_y = 1
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.dx = abs(x2 - x1) * bat_speed
        self.dy = abs(y2 - y1) * bat_speed

        self.animation_thread()

    def animation_thread(self):
        self.t = threading.Thread(target=self.animation)
        self.t.start()

    def animation(self):
        while 1:
            sleep(self.periode)
            self.bat_simul()

    def bat_simul(self):
        '''La bat va de x1,y1 à x2,y2 en self.bat_speed secondes par frames
        et retour.'''

        x = self.bat[0]
        y = self.bat[1]

        x += self.sens_x * self.dx
        y += self.sens_y * self.dy

        # cas 1
        if self.x1 < self.x2 and self.y1 < self.y2:

            if x > self.x2 or y > self.y2:
                self.sens_x = -1
                self.sens_y = -1

            if x < self.x1 or y < self.y1:
                self.sens_x = 1
                self.sens_y = 1

        # cas 2
        if self.x1 > self.x2 and self.y1 < self.y2:

            if x < self.x2 or y > self.y2:
                self.sens_x = 1
                self.sens_y = -1

            if x > self.x1 or y < self.y1:
                self.sens_x = -1
                self.sens_y = 1

        # cas 3
        if self.x1 > self.x2 and self.y1 > self.y2:

            if x < self.x2 or y < self.y2:
                self.sens_x = 1
                self.sens_y = 1

            if x > self.x1 or y > self.y1:
                self.sens_x = -1
                self.sens_y = -1

        # cas 4
        if self.x1 < self.x2 and self.y1 > self.y2:

            if x > self.x2 or y < self.y2:
                self.sens_x = -1
                self.sens_y = 1

            if x < self.x1 or y > self.y1:
                self.sens_x = 1
                self.sens_y = -1

        self.bat[0] = x
        self.bat[1] = y


if __name__ == "__main__":

    bat_simul = []
    for num in range(10):
        sim = BatSimul(BAT_D[num][4], BAT_D[num][0], BAT_D[num][1],
                                      BAT_D[num][2], BAT_D[num][3])
        bat_simul.append(sim)

    while 1:
        for p in range(10):
            print(  bat_simul[0].bat, bat_simul[1].bat, bat_simul[2].bat,
                    bat_simul[3].bat, bat_simul[4].bat, bat_simul[5].bat,
                    bat_simul[6].bat, bat_simul[7].bat, bat_simul[8].bat,
                    bat_simul[9].bat)
            sleep(0.0051)