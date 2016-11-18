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
        self.font = pygame.font.SysFont('monospace', 20)
        self.current_block = None

    def update(self, up, down, left, right, platforms):

        for i, msg in enumerate(['{}: {}'.format(name, coord) for coord, name in zip([self.rect.left, self.rect.top], ('x', 'y'))]):
            label = self.font.render(msg, 1, (0, 0, 0))
            self.gamestate.screen.blit(label, (15, 15 + i * 15))
        if self.current_block:
            if self.colors[0] != self.current_block.image:
                self.colors[0] = self.current_block.image
        if self.time < self.gamestate.time:
            self.time = self.gamestate.time
            next(self.color)
        if up:
            self.yvel = -self.speed
        if down:
            self.yvel = self.speed
        if left:
            self.xvel = -self.speed
        if right:
            self.xvel = +self.speed
        if not(left or right):
            self.xvel = 0
        if not(up or down):
            self.yvel = 0

        self.rect.left += self.xvel
        self.rect.top += self.yvel

    def color_generator(self):
        while True:
            for i in self.colors:
                self.image = i
                yield
