import pygame
from pygame.locals import *
from .effects import SlowEffect


class Platform(pygame.sprite.Sprite):

    def __init__(self, engine, x, y):
        super().__init__()
        self.engine = engine
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

    def __init__(self, engine, x, y):
        super().__init__(engine, x, y)
        self.image.fill(Color("#FFFF00"))
        self.images = []
        for i in range(2):
            self.images.append(pygame.image.load('src/sprites/platforms/alarmclock/INS_ALARM{}.png'.format(i + 1)))
        self.rect = Rect(x, y, 25, 11)
        self.period = 1
        self.image = self.images[0]
        self.img_gen = self.next_image()
        self.time_stamp = 0

    def update(self):
        if self.time_stamp < self.engine.player.timer and not self.engine.player.timer % self.period:
            self.image = next(self.img_gen)
            self.time_stamp = self.engine.player.timer


class PowerUp(Platform):

    def __init__(self, *args):
        super().__init__(*args)
        self.image.fill(Color("#0000FF"))


class ExitBlock(Platform):

    def __init__(self, *args):
        super().__init__(*args)
        self.image.fill(Color("#DD00FF"))


class SlowDown(Platform):

    def __init__(self, *args):
        super().__init__(*args)
        self.image.fill(Color("#00FFFF"))
        self.effect = SlowEffect
