import pygame
from pygame.locals import *


class DummyPlayer(pygame.sprite.Sprite):

    def __init__(self, x, y, gamestate):
        super().__init__()
        self.gamestate = gamestate
        self.xvel = 0
        self.yvel = 0
        self.image = pygame.Surface((32, 32))
        self.image.fill(Color("#000000"))
        self.image2 = pygame.Surface((32, 32))
        self.image2.fill(Color("#FFFFFF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)
        self.speed = 8
        self.color = self.color_generator()
        self.colors = [self.image, self.image2]
        self.time = 0
        self.time2 = 0
        self.font = pygame.font.SysFont('monospace', 20)
        self.current_block = None
        self.collision = False
        self.in_increments = False
        self.t_move = False

    def update(self, up, down, left, right, platforms):

        for i, msg in enumerate(['{}: {}'.format(name, coord) for coord, name in zip([self.rect.left, self.rect.top], ('x', 'y'))]):
            label = self.font.render(msg, 1, (0, 0, 0))
            self.gamestate.screen.blit(label, (15, 15 + i * 15))
        if self.current_block:
            if self.colors[0] != self.current_block.image:
                self.colors[0] = self.current_block.image
        if self.time < self.gamestate.time:
            self.time = self.gamestate.time + 0.5
            next(self.color)

        if self.t_move:
            self.time2 += 1
            if self.time2 == 5:
                self.time2 = 0
            if self.time2:
                return

            if up:
                self.rect.top -= 32
            if down:
                self.rect.top += 32
            if left:
                self.rect.left -= 32
            if right:
                self.rect.left += 32
            return
        if up:
            self.yvel = -self.speed
        if down:
            self.yvel = self.speed
        if left:
            self.xvel = -self.speed
        if right:
            self.xvel = self.speed
        if not(left or right):
            self.xvel = 0
        if not(up or down):
            self.yvel = 0

        if self.in_increments:
            t = self.rect.top % 32
            l = self.rect.left % 32
            if t or l:
                if t >= 16:
                    self.rect.top += 32 - t
                else:
                    self.rect.top -= t
                if l >= 16:
                    self.rect.left += 32 - l
                else:
                    self.rect.left -= l

        self.rect.left += self.xvel
        if self.collision:
            self.collide(self.xvel, 0, platforms)
        self.rect.top += self.yvel
        if self.collision:
            self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms[:]:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = 0
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = 0
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                if yvel < 0:
                    self.yvel = 0
                    self.rect.top = p.rect.bottom

    def color_generator(self):
        while True:
            for i in self.colors:
                self.image = i
                yield
