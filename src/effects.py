import pygame
from pygame.locals import *


class Effect:

    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont('monospace', 17)
        self.name = None

    def update(self, screen, x, y):
        msg = "{} for {}s more".format(self.name, self.time_left)
        label = self.font.render(msg, 1, (255, 0, 255))
        screen.blit(label, (x, y))


class DefaultEffect(Effect):

    def default_effects(self):
        self.player.max_vel = 30


class SlowEffect(Effect):

    def __init__(self, player):
        super().__init__(player)
        self.duration = 2
        self.time_left = 0
        self.start_time = None
        self.name = 'slowed'

    def set_effect(self):
        self.player.max_vel = 5


class InertiaEffect(Effect):
    """level effect"""
    def __init__(self, player):
        super().__init__(player)
        self.name = 'inertia'
        self.duration = float("inf")

    def set_effect(self):
        """x acceleration"""
        pass
