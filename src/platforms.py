import pygame
from pygame.locals import *
from .effects import SlowEffect


class Platform(pygame.sprite.Sprite):

    def __init__(self, gamestate, x, y):
        super().__init__()
        self.images = []
        self.gamestate = gamestate
        self.image = pygame.Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)
        self.tick_period = None

    def next_image(self):
        while True:
            for i in self.images:
                yield i

    def update(self):
        pass


class AlarmClock(Platform):

    def __init__(self, gamestate, x, y):
        super().__init__(gamestate, x, y)
        for i in range(2):
            self.images.append(pygame.image.load('src/sprites/platforms/alarmclock/INS_ALARM{}.png'.format(i + 1)))
        self.rect = Rect(x, y, 25, 11)
        self.period = 1
        self.image = self.images[0]
        self.img_gen = self.next_image()
        self.time_stamp = 0

    def update(self):
        if self.time_stamp < self.gamestate.player.timer and not self.gamestate.player.timer % self.period:
            self.image = next(self.img_gen)
            self.time_stamp = self.gamestate.player.timer


class PowerUp(Platform):

    def __init__(self, *args):
        super().__init__(*args)
        self.image.fill(Color("#0000FF"))


class ExitBlock(Platform):

    def __init__(self, *args):
        super().__init__(*args)
        self.image.fill(Color("#DD00FF"))


class SlowDown(Platform):

    def __init__(self, gamestate, x, y):
        super().__init__(gamestate, x, y)
        self.effect = SlowEffect
        for i in range(4):
            self.images.append(pygame.image.load('src/sprites/platforms/slowdown/INS_PWRUP{}.png'.format(i + 1)))
        self.rect = Rect(x, y, 32, 32)
        self.period = 0.5
        self.image = self.images[0]
        self.img_gen = self.next_image()
        self.time_stamp = 0

    def update(self):
        if self.time_stamp < self.gamestate.player.timer and not self.gamestate.player.timer % self.period:
            self.image = next(self.img_gen)
            self.time_stamp = self.gamestate.player.timer
