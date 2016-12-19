import pygame
from pygame import *
from .platforms import PowerUp


class Item:

    def __init__(self):
        self.cooldown = None
        self.blocks_affecting = []


class Magnet(Item):

    def __init__(self, gamestate):
        self.gamestate = gamestate
        self.cooldown = 5
        self.start_time = None
        self.cd_left = 0
        self.duration = 3
        self.blocks_affecting = [PowerUp]
        self.radius = 200
        self.speed = 5
        self.font = pygame.font.SysFont('monospace', 17)

    def update(self):
        if self.start_time:
            self.cd_left = self.cooldown - (self.gamestate.player.timer - self.start_time)
        if self.cd_left < 0:
            self.cd_left = 0
        if self.cd_left > self.cooldown - self.duration:
            self.on_use_effect()
        label = self.font.render('item: {}s cd'.format(self.cd_left), 1, (255, 0, 255))
        self.gamestate.screen.blit(label, (35 + 320, 75))

    def on_use_effect(self):  # in dire need of refactoring
        for e in self.gamestate.entities:
            if type(e) not in self.blocks_affecting:
                continue
            x = e.rect.left
            y = e.rect.top
            x1 = self.gamestate.player.rect.left
            y1 = self.gamestate.player.rect.top
            if (x - x1)**2 + (y - y1)**2 > self.radius**2:
                continue
            index = self.gamestate.platforms.index(e)
            if x1 - x == 0:
                if y1 > y:
                    new_value = y + self.speed
                elif y1 < y:
                    new_value = y - self.speed
                e.rect.top = self.gamestate.platforms[index].rect.top = new_value
                continue
            if y1 - y == 0:
                if x1 > x:
                    new_value = x + self.speed
                elif x1 < x:
                    new_value = x - self.speed
                e.rect.left = self.gamestate.platforms[index].rect.left = new_value
                continue
            tg = (y1 - y) / (x1 - x)
            dx = (self.speed**2 / (tg**2 + 1)) ** 0.5
            dy = self.speed * (tg**2 / (1 + tg**2))**0.5
            dx = - dx if x1 < x else dx
            dy = - dy if y1 < y else dy
            e.rect.left += dx
            e.rect.top += dy
            self.gamestate.platforms[index].rect.left += dx
            self.gamestate.platforms[index].rect.top += dy

    def turn_on(self):
        self.start_time = self.gamestate.player.timer

    def draw(self):
        pass
