import pygame
from pygame.locals import *


class DefaultEffect:

    def __init__(self, player):
        self.player = player

    def default_effects(self):
        self.player.max_vel = 30


class SlowEffect:

    def __init__(self, player):
        self.player = player
        self.duration = 2
        self.start_time = None

    def set_effect(self):
        self.player.max_vel = 5


class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)


class AlarmClock(Platform):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill(Color("#FFFF00"))


class PowerUp(Platform):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill(Color("#0000FF"))


class ExitBlock(Platform):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill(Color("#DDDDFF"))


class SlowDown(Platform):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image.fill(Color("#00FFFF"))
        self.effect = SlowEffect
