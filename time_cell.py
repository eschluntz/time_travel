#! /usr/bin/python3

from typing import Tuple
import pygame
from copy import copy
import time
from collections import namedtuple
import numpy as np
import random

screen = None
WIDTH = 1280
HEIGHT = 720

def rect(color : Tuple, left : float, top : float, width : float, height : float):
    py_rect = pygame.Rect(left, top, width, height)
    pygame.draw.rect(screen, color, py_rect)

Result = namedtuple("Result", "cycle_start cycle_end cycle_length")
Config = namedtuple("Config", "rule ratio t_enter t_exit portal_w")

def rule_name_to_list(rule_name : int):
    """Takes in a rule's wolfram name and converts it to the binary list to parse,
    i.e. 110 -> [0,1,1,0,1,1,1,0]"""

    rule_bin_str = np.binary_repr(rule_name, width=8)
    return tuple( int(x) for x in rule_bin_str )

class TimeCell:
    def __init__(self, config=None, quick_compute=True, center=False):
        """Class to represent a 1D Cellular Automata, with support for time travel.
        config: Config object. Controls settings for this run. Default supplied.
        quick_compute: bool. only update the earliest timed row. Less pretty but faster.
        center: bool. Just starts with 1 cell in the center. overrides config.ratio."""

        self.scl = 5  # How many pixels wide/high is each cell?
        self.num_cells = int(WIDTH / self.scl)
        self.num_gens = int(HEIGHT / self.scl)

        self.num_steps = None
        self.active_generations = None
        self.universe = None
        self.quick_compute = quick_compute
        self.result = None

        # config
        self.config = config or Config(rule=110, ratio=.2, t_enter=80, t_exit=40, portal_w=32)
        self.rules = rule_name_to_list(self.config.rule)
        self.restart(self.config.ratio, center)  # Sets generations to [0], only middle cell to 1

        # time portal
        self.t_enter = self.config.t_enter
        self.t_exit = self.config.t_exit
        self.x_enter = int(self.num_cells / 2 + 5)
        self.x_exit = int(self.num_cells / 2 + 5)
        self.w = self.config.portal_w
        self.history = {}  # store what's gone through portal
        self.trips = 0

    def restart(self, ratio, center=False):
        """Resets the universe to time = 0"""
        self.num_steps = 0
        self.universe = []
        for _ in range(self.num_gens):
            self.universe.append([0] * self.num_cells)
        self.active_generations = [0]

        # We arbitrarily start with just the middle cell having a state of "1"
        if center:
            self.universe[0][self.num_cells // 2] = 1
        else:
            for i in range(self.num_cells):
                self.universe[0][i] = int(random.random() < ratio)

    def generate(self):
        """Simulates forward all active rows"""
        # filter out ones that have reached the max age
        self.num_steps += 1
        self.active_generations = [t for t in self.active_generations if t < self.num_gens -1]

        if self.quick_compute:
            # if we're trying to go fast and just detect a time loop, we can throw away anything
            # after the portal
            self.active_generations = [min(self.active_generations)]

        for i in range(len(self.active_generations)):
            # ASSUMPTION: two active generations are never right next to each other
            t = self.active_generations[i]
            self.active_generations[i] += 1
            next1 = self.generate_row_np(t)
            next2 = self.generate_row(t)
            assert next1 == next2, "not equal! {} vs {}".format(next1, next2)
            self.universe[t + 1] = copy(next1)
            self.check_row_for_portal_and_loops(t)

    def generate_row_np(self, t):
        """Vectorized"""
        row_l = np.array(self.universe[t][0:-2])
        row_c = np.array(self.universe[t][1:-1])
        row_r = np.array(self.universe[t][2:])  # sad syntax
        # binary_mat = np.array(4,2,1))
        row_code = 4 * row_l + 2 * row_c + 1 * row_r
        rules = np.array(self.rules)
        result = rules[7 - row_code]  # vectorized lookup
        new_row = copy(self.universe[t + 1])
        new_row[1:-1] = list(result)
        return new_row

    def generate_row(self, t):
        """ Generates a single next row of the CA.
        Edges are treated as constants.
        t: int, the current time row
        """
        # First we create an empty array for the new values
        nextgen = [0] * self.num_cells
        # Ignore edges that only have one neighor
        for i in range(1, self.num_cells - 1):

            left, me, right = self.universe[t][i - 1 : i + 2]
            nextgen[i] = self.executeRules(left, me, right)

        # Copy the array into universe
        return nextgen
        # self.universe[t + 1] = copy(nextgen)

    # Implementing the Wolfram rules
    # Could be improved and made more concise, but here we can
    # explicitly see what is going on for each case
    def executeRules(self, a, b, c):
        if a == 1 and b == 1 and c == 1:
            return self.rules[0]
        if a == 1 and b == 1 and c == 0:
            return self.rules[1]
        if a == 1 and b == 0 and c == 1:
            return self.rules[2]
        if a == 1 and b == 0 and c == 0:
            return self.rules[3]
        if a == 0 and b == 1 and c == 1:
            return self.rules[4]
        if a == 0 and b == 1 and c == 0:
            return self.rules[5]
        if a == 0 and b == 0 and c == 1:
            return self.rules[6]
        if a == 0 and b == 0 and c == 0:
            return self.rules[7]
        return 0

    def check_row_for_portal_and_loops(self, t):
        """Handles copying data back in time if we just entered a portal.
        Detects if we've sent back exactly the same thing before and records data.
        t: int: current generation."""
        if t == self.t_enter:
            # reset time
            self.active_generations.append(self.t_exit)  # TODO modifying a list while we loop through it is dangerous

            # copy the portal back
            portal_contents = copy(self.universe[t+1][self.x_enter : self.x_enter + self.w])
            self.universe[self.t_exit][self.x_exit : self.x_exit + self.w] = portal_contents

            # save
            self.trips += 1
            portal_contents_tup = tuple(portal_contents)

            # check if we've sent back the same thing before
            if portal_contents_tup in self.history:
                r = Result(
                    cycle_start=self.history[portal_contents_tup],
                    cycle_end=self.trips,
                    cycle_length=self.trips - self.history[portal_contents_tup],
                )
                self.result = r  # this not being None tells us to stop

            self.history[portal_contents_tup] = self.trips

    def gen_until_time_loop(self, max_trips=200, render=False):
        """Runs generate in a loop until it detects a time loop.
        max_trips: break if we havenot found a time loop after that many trips.
        returns: Result object or None"""

        if render:
            pygame.init()
            global screen
            screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.quick_compute = True  # speeds things up
        while self.result is None:
            if max_trips is not None and self.trips > max_trips:
                return
            if render:
                self.render()
            self.generate()

        return self.result

    def render(self):
        for t in self.active_generations:
            self.render_row(t)

        red = (255, 0, 0)
        green = (0, 255, 0)
        scl = self.scl

        # draw exit portal
        rect(red, self.x_exit * scl, self.t_exit * scl, self.w * scl, scl / 5)

        # draw enter portal
        rect(green, self.x_enter * scl, self.t_enter * scl, self.w * scl, scl / 5)

        pygame.display.flip()

    def render_row(self, t):
        scl = self.scl
        black = (0, 0, 0)
        white = (255, 255, 255)

        for i in range(self.num_cells):
            if self.universe[t][i] == 1:
                color = white
            else:
                color = black
            rect(color, i * scl, t * scl, scl, scl)


def loop():
    quick = False
    cfg = Config(rule=30, ratio=.2, t_enter=80, t_exit=40, portal_w=32)
    ca = TimeCell(config=cfg, quick_compute=quick, center=True)
    while True:
        ca.render()
        ca.generate()

        if ca.result is not None:
            print("Time loop found!")
            print(ca.result)
            if quick:
                return
        # print("render: {}\t generate: {}".format(t1 - t0, t2 - t1))

        # handle user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def several_loops():
    rules = list(range(22, 256))
    ratios = [.1, .5, .9]
    for rule in rules:
        for ratio in ratios:
            cfg = Config(rule=rule, ratio=ratio, t_enter=80, t_exit=40, portal_w=32)
            print(cfg)
            ca = TimeCell(config=cfg, quick_compute=True)

            done_count = 0
            for i in range(1000):
                ca.render()
                ca.generate()

                if ca.result is not None:
                    done_count += 1
                    if done_count >= 200:
                        break

                # handle user input
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    loop()
