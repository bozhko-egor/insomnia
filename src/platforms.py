import pygame
from pygame.locals import *
from .effects import SlowEffect
from math import cos, sin, pi


class Platform(pygame.sprite.Sprite):

    def __init__(self, gamestate, x, y, w=32, h=32):
        super().__init__()
        self.images = []
        self.gamestate = gamestate
        self.image = pygame.Surface((w, h))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, w, h)
        self.tick_period = None
        self.args = []

    def next_image(self):
        while True:
            for i in self.images:
                yield i

    def update(self):
        pass


class MovingPlatform(Platform):

    def __init__(self, gamestate, x, y):
        super().__init__(gamestate, x, y)
        self.image = pygame.Surface((256, 10))
        self.rect = Rect(x, y, 256, 10)
        self.image.fill(Color("#555500"))
        self.starting_point = (x, y)
        self.speed = 1
        self.distance = 200
        self.radius = 75
        self.pi_gene = self.pi_generator()
        self.delta = None

    def update(self):
        t = next(self.pi_gene)
        self.rect.left = self.x_func(t)
        self.rect.top = self.y_func(t)

    def x_func(self, t):
        x = self.starting_point[0] + self.radius * cos(t)
        return x

    def y_func(self, t):
        y = self.starting_point[1] + self.radius * sin(t)
        return y

    def pi_generator(self):
        point = 0
        while True:
            if point > 2 * pi:
                point = 0
            yield point
            point += 0.01

    def collision_handler(self, xvel, yvel, player):
        if player.rect.bottom >= self.rect.top:
            player.rect.bottom = self.rect.top
            if yvel > 0:
                player.onGround = True
                player.yvel = 0
        else:
            if xvel > 0:
                player.rect.right = self.rect.left
                player.xvel = 0  # remove xvel on contact
            if xvel < 0:
                player.rect.left = self.rect.right
                player.xvel = 0


class AlarmClock(Platform):

    def __init__(self, gamestate, x, y, w=25, h=11):
        super().__init__(gamestate, x, y)
        for i in range(2):
            self.images.append(pygame.image.load('src/sprites/platforms/alarmclock/INS_ALARM{}.png'.format(i + 1)))
        self.rect = Rect(x, y, w, h)
        self.period = 1
        self.image = self.images[0]
        self.img_gen = self.next_image()
        self.time_stamp = 0

    def update(self):
        if self.time_stamp < self.gamestate.player.timer and not self.gamestate.player.timer % self.period:
            self.image = next(self.img_gen)
            self.time_stamp = self.gamestate.player.timer


class PowerUp(Platform):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image.fill(Color("#0000FF"))


class ExitBlock(Platform):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image.fill(Color("#DD00FF"))


class SlowDown(Platform):

    def __init__(self, gamestate, x, y, w=32, h=32):
        super().__init__(gamestate, x, y)
        self.effect = SlowEffect
        for i in range(4):
            self.images.append(pygame.image.load('src/sprites/platforms/slowdown/INS_PWRUP{}.png'.format(i + 1)))
        self.rect = Rect(x, y, w, h)
        self.period = 0.5
        self.image = self.images[0]
        self.img_gen = self.next_image()
        self.time_stamp = 0

    def update(self):
        if self.time_stamp < self.gamestate.player.timer and not self.gamestate.player.timer % self.period:
            self.image = next(self.img_gen)
            self.time_stamp = self.gamestate.player.timer


class WindArea(Platform):

    def __init__(self, gamestate, x, y, *args, w=32, h=32):
        super().__init__(gamestate, x, y)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.rect = Rect(x, y, w, h)
        self.image.fill((255, 0, 0, 150))
        self.starting_point = (x, y)
        self.coef = 0.5
        if args:
            x1, y1 = args
        else:
            x1, y1 = 0, 0
        self.x_speed = (x - x1) * self.coef
        self.y_speed = (y - y1) * self.coef
        self.args += [x1, y1]

    def collision_handler(self, player):
        if self.rect.colliderect(player.rect):
            player.xvel += self.x_speed
            player.yvel += self.y_speed


class Teleport(Platform):

    _instances = []

    def __init__(self, gamestate, x, y, index, w=32, h=32):
        super().__init__(gamestate, x, y)
        self.image = pygame.Surface((w, h))
        self.index = index
        self.rect = Rect(x, y, w, h)
        self.image.fill((255, 255, 255))
        self.starting_point = (x, y)
        self._instances.append(self)
        self.linked_tp = self.get_linked_tp()

    def get_linked_tp(self):
        tp = None
        for instance in self._instances:
            if self.index == instance.index and instance != self:
                tp = instance
        if tp and not tp.linked_tp:
            tp.linked_tp = self
        return tp

    def collision_handler(self, xvel, yvel, player):
        if xvel > 0:
            player.rect.left = self.linked_tp.rect.right
            player.rect.top = self.linked_tp.rect.top
        if xvel < 0:
            player.rect.right = self.linked_tp.rect.left
            player.rect.top = self.linked_tp.rect.top
        if yvel > 0:
            player.rect.top = self.linked_tp.rect.bottom
            player.rect.left = self.linked_tp.rect.left
        if yvel < 0:
            player.rect.bottom = self.linked_tp.rect.top
            player.rect.left = self.linked_tp.rect.left
