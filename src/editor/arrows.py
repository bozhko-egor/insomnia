import pygame
from pygame.locals import *
import math


class Arrow(pygame.sprite.Sprite):

    def __init__(self, x, y, x1, y1, w=10, h=95):
        self.x = x
        self.y = y
        self.dx = x - x1
        self.dy = y - y1
        self.x1 = x1
        self.y1 = y1
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        pygame.draw.polygon(self.image, (0, 0, 0), ((3, 0), (3, 85), (0, 80), (4, 95), (8, 80), (5, 85), (5, 0)))

    def redraw(self):
        self.angle = math.atan2(self.x1 - self.x, self.y1 - self.y)
        self.angle = math.degrees(self.angle)
        self.length = ((self.x - self.x1)**2 + (self.y - self.y1)**2)**0.5
        self.image = pygame.transform.scale(self.image, (5, int(self.length)))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.width, self.height = self.image.get_rect().width, self.image.get_rect().height
        if self.dx < 0:
            x_coord = self.x
        else:
            x_coord = self.x - self.width

        if self.dy < 0:
            y_coord = self.y
        else:
            y_coord = self.y - self.height

        self.rect = Rect(x_coord, y_coord, self.width, self.height)
