from .levels import *
from .effects import InertiaEffect


class Level:

    def __init__(self, layout, number, effects=[]):
        self.name = None
        self.layout = layout
        self.effects = effects
        self.highscore = 0
        self.best_time = 0
        self.number = number

levels = [Level(level1, 0), Level(level2, 1, [InertiaEffect])]
