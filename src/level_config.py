import pickle
import pygame
from pygame.locals import *


class Level:

    def __init__(self, layout, number, effects=[]):
        self.name = None
        self.platforms = []
        with open("src/levels/{}".format(layout), "rb") as f:
            level = pickle.load(f)
            self.level = level
        self.effects = effects
        self.highscore = 0
        self.best_time = 0
        self.number = number


level_list = ['123']
levels = [Level(name, i) for i, name in enumerate(level_list)]
