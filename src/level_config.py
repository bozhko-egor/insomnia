import pickle
import pygame
from os import listdir
from pygame.locals import *
from src.platforms import SpawnPoint


class Level:

    def __init__(self, layout, number, effects=[]):
        self.name = None
        self.platforms = []
        with open("src/levels/{}".format(layout), "rb") as f:
            self.level = pickle.load(f)
        self.effects = effects
        self.highscore = 0
        self.best_time = 0
        self.number = number
        self.spawnpoint = next(([x[1].left, x[1].top] for x in self.level if x[0] == SpawnPoint), [64, 64])  # САМОДОКУМЕНТИРУЮЩИЙСЯ КОД


level_list = listdir(path='src/levels')
if '.DS_Store' in level_list:
    level_list.remove('.DS_Store')

levels = [Level(name, i) for i, name in enumerate(level_list)]
