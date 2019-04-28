"""
Reinforcement learning robot path planning for small grid (8x8). For DQ Learning

Red rectangle:          UGV.
Black rectangles:       IoT regions (denoted by hell)     [reward = 5].
Yellow bin circle:      goal    [reward = 10 + x*5 where x is the number of users].
All other states:       ground      [reward = -1].
This script is the main environment part. The RL is in RL_brain.py.

reference : Morvan Zhou https://github.com/MorvanZhou/Reinforcement-learning-with-tensorflow which is open source
"""
import numpy as np
import time
import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 40   # pixels
MAZE_H = 8  # grid height
MAZE_W = 8  # grid width


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.iot1 = 0 # if a particular iot device is visited or not (true if UGV enters at least one iot charging region)
        self.iot2 = 0
        self.iot3 = 0
        self.n_actions = len(self.action_space)
        self.n_features = 2  # state finished or not
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # create origin
        origin = np.array([20, 20])

        # iot 3
        hell31_center = origin + np.array([UNIT * 3, UNIT * 2])
        self.hell31 = self.canvas.create_rectangle(
            hell31_center[0] - 15, hell31_center[1] - 15,
            hell31_center[0] + 15, hell31_center[1] + 15,
            fill='black')
        hell32_center = origin + np.array([UNIT * 3, UNIT * 3])
        self.hell32 = self.canvas.create_rectangle(
            hell32_center[0] - 15, hell32_center[1] - 15,
            hell32_center[0] + 15, hell32_center[1] + 15,
            fill='black')

        # iot 2
        hell21_center = origin + np.array([UNIT * 1, UNIT * 6])
        self.hell21 = self.canvas.create_rectangle(
            hell21_center[0] - 15, hell21_center[1] - 15,
            hell21_center[0] + 15, hell21_center[1] + 15,
            fill='blue')
        hell22_center = origin + np.array([UNIT * 2, UNIT * 6])
        self.hell22 = self.canvas.create_rectangle(
            hell22_center[0] - 15, hell22_center[1] - 15,
            hell22_center[0] + 15, hell22_center[1] + 15,
            fill='blue')

        # iot 1
        hell11_center = origin + np.array([UNIT * 1, UNIT * 4])
        self.hell11 = self.canvas.create_rectangle(
            hell11_center[0] - 15, hell11_center[1] - 15,
            hell11_center[0] + 15, hell11_center[1] + 15,
            fill='red')
        hell12_center = origin + np.array([UNIT * 1, UNIT * 5])
        self.hell12 = self.canvas.create_rectangle(
            hell12_center[0] - 15, hell12_center[1] - 15,
            hell12_center[0] + 15, hell12_center[1] + 15,
            fill='red')
        hell13_center = origin + np.array([UNIT * 2, UNIT * 5])
        self.hell13 = self.canvas.create_rectangle(
            hell13_center[0] - 15, hell13_center[1] - 15,
            hell13_center[0] + 15, hell13_center[1] + 15,
            fill='red')

        # create goal
        oval_center = origin + np.array([UNIT * 7, UNIT * 7])
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        # create UGV
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='gray')


        # pack all
        self.canvas.pack()
        # for saving the final path
        self.canvas.postscript(file="map.ps", colormode='color')

    def reset_dq(self):
        self.update()
        time.sleep(0.1)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.iot1 = 0
        self.iot2 = 0
        self.iot3 = 0
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='gray')
         # return observation
        return (np.array(self.canvas.coords(self.rect)[:2]) - np.array(self.canvas.coords(self.oval)[:2]))/(MAZE_H*UNIT)


    def step_dq(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:   # right
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 3:   # left
            if s[0] > UNIT:
                base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        next_coords = self.canvas.coords(self.rect)  # next state

         # reward function for goal, iots and ground
        if next_coords == self.canvas.coords(self.oval):
            reward = 10 + self.iot1 * 5 + self.iot2 * 5 + self.iot3 * 5
            done = True
        elif (next_coords in [self.canvas.coords(self.hell11)]) or (next_coords in [self.canvas.coords(self.hell12)]) or (next_coords in [self.canvas.coords(self.hell13)]) and self.iot1 == 0:
            reward = 10
            self.iot1 = 1
            done = False
        elif (next_coords in [self.canvas.coords(self.hell21)]) or (next_coords in [self.canvas.coords(self.hell22)]) and self.iot2 == 0:
            reward = 10
            self.iot2 = 1
            done = False
        elif (next_coords in [self.canvas.coords(self.hell31)]) or (next_coords in [self.canvas.coords(self.hell32)]) and self.iot3 == 0:
            reward = 10
            self.iot3 = 1
            done = False
        else:
            reward = -1
            done = False
        s_ = (np.array(next_coords[:2]) - np.array(self.canvas.coords(self.oval)[:2]))/(MAZE_H*UNIT)
        return s_, reward, done



    def render(self):
        # time.sleep(0.01)
        self.update()

     #create path line
    def _create_line_dq(self, x, y):
     # transfomation of coordinates necessary for line creation
        xtemp = x* (MAZE_H * UNIT) + np.array(self.canvas.coords(self.oval)[:2])
        xtemp2 = np.array(xtemp) + np.array([30,30])
        xnn = np.concatenate((xtemp, xtemp2), axis=None)
        x = xnn
        ytemp = y * (MAZE_H * UNIT) + np.array(self.canvas.coords(self.oval)[:2])
        ytemp2 = np.array(ytemp) + np.array([30, 30])
        ynn = np.concatenate((ytemp, ytemp2), axis=None)
        y=ynn

         #main line
        if not(np.array_equal(y, self.canvas.coords(self.oval))):
            x1 = (x[0] + x[2]) / 2
            y1 = (x[1] + x[3]) / 2
            x2 = (ynn[0] + ynn[2]) / 2
            y2 = (ynn[1] + ynn[3]) / 2
            self.canvas.create_line(x1, y1, x2, y2, fill='red')



    def _save(self):
        self.canvas.postscript(file="map.ps", colormode='color')


    #tells if iot user is charged or not
    def _not_charged(self):
        i = 0
        if self.iot1 == 0 and self.iot2 == 0 and self.iot3 == 0:
            return 3
        elif (self.iot1 == 0 and self.iot2 == 0) or (self.iot1 == 0 and self.iot3 == 0) or (
                self.iot3 == 0 and self.iot2 == 0):
            return 2
        elif self.iot1 == 0 or self.iot2 == 0 or self.iot3 == 0:
            return 1
        else:
            return 0
