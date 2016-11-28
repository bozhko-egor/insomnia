import pygame
from pygame.locals import *


class Effect:

    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont('monospace', 17)
        self.name = None

    def update(self, x, y):
        msg = "{} {}s".format(self.name, self.time_left)
        label = self.font.render(msg, 1, (255, 0, 255))
        self.player.gamestate.screen.blit(label, (x, y))


class DefaultEffect(Effect):

    def default_effects(self):
        self.player.max_vel = 10


class SlowEffect(Effect):

    def __init__(self, player):
        super().__init__(player)
        self.duration = 5
        self.time_left = 0
        self.start_time = None
        self.name = 'slowed'

    def set_effect(self):
        self.player.max_vel = 5

class Friction(SlowEffect):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = 1.5


class InertiaEffect(Effect):
    """level effect"""
    def __init__(self, player):
        super().__init__(player)
        self.name = 'inertia'

    def set_effect(self, up, down, left, right):
        """x acceleration"""
        if up:
            if self.player.onGround:
                self.player.yvel -= 10
        if down:
            pass
        if left:
            self.player.xvel += -0.3
        if right:
            self.player.xvel += 0.3
        if not self.player.onGround:
            self.player.yvel += 0.3
            if self.player.yvel > self.player.max_vel:
                self.player.yvel = self.player.max_vel
        if self.player.xvel < 0:
            self.player.xvel += 0.1
        if self.player.xvel > 0:
            self.player.xvel -= 0.1
        if abs(self.player.xvel) < 0.1:
            self.player.xvel = 0

    def update(self, x, y):
        label = self.font.render(self.name, 1, (255, 0, 255))
        self.player.gamestate.screen.blit(label, (x, y))
