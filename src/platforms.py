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
